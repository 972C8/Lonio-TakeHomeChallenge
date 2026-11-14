"""Optional step 8: send the feature specs to Linear through the Linear MCP server.

Runs only when explicitly asked (`pipeline publish --team <key>`). The agent's
instructions are in pipeline/agents/linear_publisher.md. Auth: a Linear API key
in the LINEAR_API_KEY environment variable. `--dry-run` connects to Linear's
read-only endpoint, so nothing can be written.
"""
from __future__ import annotations

import os

from pydantic import BaseModel, Field as F

from ..engine.context import Context
from ..engine.llm import load_prompt, run_agent
from ..engine.paths import PIPELINE, REQUIREMENTS


class Entry(BaseModel):
    spec_id: str
    linear_id: str = ""
    note: str = ""


class PublishReport(BaseModel):
    created: list[Entry] = F(default_factory=list)
    updated: list[Entry] = F(default_factory=list)
    unchanged: list[Entry] = F(default_factory=list)
    skipped: list[Entry] = F(default_factory=list)
    would_create: list[Entry] = F(default_factory=list)
    would_update: list[Entry] = F(default_factory=list)


async def publish(problem: str, team: str, project: str | None, dry_run: bool) -> dict:
    ctx = Context(problem)
    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        raise SystemExit("Set LINEAR_API_KEY (a Linear API key) to publish.")
    url = "https://mcp.linear.app/mcp/readonly" if dry_run else "https://mcp.linear.app/mcp"
    req = REQUIREMENTS / problem
    mode = "dry-run" if dry_run else "apply"
    report = await run_agent(
        f"publish_linear/{mode}", load_prompt(PIPELINE / "agents" / "linear_publisher.md"),
        f"Mode: {mode}\nTeam: {team}\nProject: {project or ctx.profile['title']}\n"
        f"Feature specs folder: {req}\nPublish the feature specs as instructed.",
        PublishReport, model=ctx.model("default"), tools=["Read", "Glob", "mcp__linear__*"],
        mcp_servers={"linear": {"type": "http", "url": url, "headers": {"Authorization": f"Bearer {key}"}}},
        add_dirs=[req], max_turns=200)
    ctx.write(f"linear_publish.{mode}", report)
    return report
