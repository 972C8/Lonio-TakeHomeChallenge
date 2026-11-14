"""Thin wrapper around the Claude Agent SDK.

Every agent call in the pipeline goes through `run_agent`, which
- runs an isolated agent (no user settings, only the tools we allow),
- forces a JSON-schema structured output (fails closed if the agent cannot comply),
- logs prompt, result, cost, tokens and duration to build/logs/ for auditability,
- records the token usage of every call in USAGE, summed per stage by `usage_summary`.
"""
from __future__ import annotations

import asyncio
import copy
import json
import os
import time
from pathlib import Path
from typing import Any

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query
from pydantic import BaseModel

from .paths import LOG_DIR, ROOT

_SEM = asyncio.Semaphore(6)
COSTS: list[dict] = []
TOKEN_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


class AgentError(RuntimeError):
    pass


def json_schema(model: type[BaseModel] | dict) -> dict:
    """Pydantic schema with $refs inlined (structured outputs work best with flat schemas)."""
    schema = model if isinstance(model, dict) else model.model_json_schema()
    defs = schema.get("$defs", {})

    def inline(node):
        if isinstance(node, dict):
            if "$ref" in node:
                return inline(copy.deepcopy(defs[node["$ref"].split("/")[-1]]))
            return {k: inline(v) for k, v in node.items() if k not in ("$defs", "title", "default")}
        if isinstance(node, list):
            return [inline(n) for n in node]
        return node

    return inline(schema)


def load_prompt(path: Path, **vars: str) -> str:
    text = path.read_text()
    for k, v in vars.items():
        text = text.replace("{{" + k + "}}", v)
    return text


async def run_agent(
    name: str,
    system_prompt: str,
    prompt: str,
    schema: type[BaseModel] | dict,
    model: str,
    tools: list[str] | None = None,
    mcp_servers: dict | None = None,
    add_dirs: list[Path] | None = None,
    max_turns: int = 20,
    retries: int = 1,
) -> dict[str, Any]:
    if os.environ.get("PIPELINE_NO_AGENTS"):    # benchmark B0: a no-op rerun must not call any agent
        raise AgentError(f"agent call blocked by PIPELINE_NO_AGENTS: {name}")
    opts = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        allowed_tools=tools or [],
        tools=tools or [],
        mcp_servers=mcp_servers or {},
        permission_mode="bypassPermissions" if tools else "default",
        setting_sources=[],          # isolation: ignore user/project CLAUDE.md, skills, hooks
        cwd=str(ROOT),
        add_dirs=[str(d) for d in (add_dirs or [])],
        max_turns=max_turns,
        output_format={"type": "json_schema", "schema": json_schema(schema)},
    )
    last_err = None
    for attempt in range(retries + 1):
        async with _SEM:
            t0 = time.time()
            result, texts = None, []
            try:
                async for msg in query(prompt=prompt, options=opts):
                    if isinstance(msg, AssistantMessage):
                        texts += [b.text for b in msg.content if isinstance(b, TextBlock)]
                    if isinstance(msg, ResultMessage):
                        result = msg
            except Exception as e:  # noqa: BLE001 - surfaced below
                last_err = e
                continue
        out = result.structured_output if result else None
        _log(name, attempt, prompt, system_prompt, model, result, out, texts, time.time() - t0)
        if result and not result.is_error and out is not None:
            if not isinstance(schema, dict):
                schema.model_validate(out)  # double check
            return out
        last_err = AgentError(f"{name}: {result.subtype if result else 'no result'} {result.errors if result else ''}")
    raise AgentError(f"agent {name} failed after {retries + 1} attempts: {last_err}")


def tokens(result) -> dict[str, int]:
    """Token counts of one agent call (summed over all its turns), from the SDK's ResultMessage.usage."""
    usage = getattr(result, "usage", None) or {}
    return {k: int(usage.get(k) or 0) for k in TOKEN_KEYS}


def stage_of(agent: str) -> str:
    """Agent name -> stage for the usage summary: 'write_section/SEC-01' -> 'write_section'."""
    return agent.split("/")[0]


def usage_summary(calls: list[dict]) -> dict:
    """Calls, turns, tokens and SDK cost estimate per stage and in total (report.json `usage_this_run`)."""
    def empty():
        return {"calls": 0, "turns": 0, **{k: 0 for k in TOKEN_KEYS}, "total_tokens": 0, "cost_usd": 0.0, "seconds": 0.0}

    by_stage: dict[str, dict] = {}
    total = empty()
    for c in calls:
        for acc in (by_stage.setdefault(stage_of(c["agent"]), empty()), total):
            acc["calls"] += 1
            acc["turns"] += c.get("turns", 0)
            for k in TOKEN_KEYS:
                acc[k] += c.get(k, 0)
            acc["total_tokens"] += sum(c.get(k, 0) for k in TOKEN_KEYS)
            acc["cost_usd"] = round(acc["cost_usd"] + c.get("cost_usd", 0.0), 4)
            acc["seconds"] = round(acc["seconds"] + c.get("seconds", 0.0), 1)
    return {"by_stage": dict(sorted(by_stage.items(), key=lambda kv: -kv[1]["cost_usd"])), "total": total}


def _log(name, attempt, prompt, system, model, result, out, texts, secs):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    cost = getattr(result, "total_cost_usd", None) or 0.0
    tok = tokens(result)
    turns = getattr(result, "num_turns", 0) or 0
    COSTS.append({"agent": name, "model": model, "cost_usd": cost, "seconds": round(secs, 1), "turns": turns, **tok})
    safe = name.replace("/", "_")
    (LOG_DIR / f"{safe}.attempt{attempt}.json").write_text(json.dumps({
        "agent": name, "model": model, "seconds": round(secs, 1), "cost_usd": cost, "turns": turns, "usage": tok,
        "model_usage": getattr(result, "model_usage", None),
        "subtype": getattr(result, "subtype", None), "system_prompt": system, "prompt": prompt,
        "assistant_text": texts, "output": out,
    }, indent=2, ensure_ascii=False, default=str))
