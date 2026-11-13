"""Thin wrapper around the Claude Agent SDK.

Every agent call in the pipeline goes through `run_agent`, which
- runs an isolated agent (no user settings, only the tools we allow),
- forces a JSON-schema structured output (fails closed if the agent cannot comply),
- logs prompt, result, cost and duration to build/logs/ for auditability.
"""
from __future__ import annotations

import asyncio
import copy
import json
import time
from pathlib import Path
from typing import Any

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query
from pydantic import BaseModel

from .paths import LOG_DIR, ROOT

_SEM = asyncio.Semaphore(6)
COSTS: list[dict] = []


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


def _log(name, attempt, prompt, system, model, result, out, texts, secs):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    cost = getattr(result, "total_cost_usd", None) or 0.0
    COSTS.append({"agent": name, "cost_usd": cost, "seconds": round(secs, 1)})
    safe = name.replace("/", "_")
    (LOG_DIR / f"{safe}.attempt{attempt}.json").write_text(json.dumps({
        "agent": name, "model": model, "seconds": round(secs, 1), "cost_usd": cost,
        "subtype": getattr(result, "subtype", None), "system_prompt": system, "prompt": prompt,
        "assistant_text": texts, "output": out,
    }, indent=2, ensure_ascii=False, default=str))
