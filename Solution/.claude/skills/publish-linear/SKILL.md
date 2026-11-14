---
name: publish-linear
description: Send the finished feature spec to Linear using the pipeline's Linear publisher agent (optional step 8). Does a read-only preview first, asks for an explicit go, then publishes. Use when asked to publish, sync or send the requirements, stories or open questions to Linear.
---

# /publish-linear – send the feature spec to Linear

This skill drives **step 8** of the pipeline. The work is done by the Linear
publisher agent (`pipeline/agents/linear_publisher.md`), which the command
`pipeline publish` starts with the Linear MCP server. You do **not** call
Linear tools from this session yourself: always go through the command, so
the agent's rules apply (look before you write, no duplicates, never delete,
never touch status / assignee / estimate).

Publishing writes to an outside system, so it needs the user's explicit go.

## 0. Check before anything
1. Feature: the one the user names.
2. `requirements/<feature>/feature.md` must exist. If not, say so and suggest
   `/run-pipeline` first.
3. Read the verdict in `build/<feature>/review.md`. If it is not "ready" or
   "ready with caveats", or blocking open questions remain, say so in one
   line and ask whether to publish anyway (they may want `/review` first).
4. `LINEAR_API_KEY` must be set in the environment. Check only whether it is
   set (`[ -n "$LINEAR_API_KEY" ] && echo set`), never print it. If it is
   missing, tell the user to create a Linear API key and export it in the
   terminal where Claude Code runs. Never ask them to paste the key into the
   chat.
5. Ask for the **Linear team key** (e.g. `ONB`) and, optionally, a project
   name (default: the feature title from `profile.yaml`).

## 1. Preview (read-only)
Run, from `Solution/`:

```bash
.venv/bin/python -m pipeline --feature <feature> publish --team <KEY> [--project "<name>"] --dry-run
```

This connects to Linear's **read-only** endpoint, so nothing can be written.
Summarise the report (also saved as `build/<feature>/linear_publish.dry-run.json`):
how many issues would be created, updated and left unchanged, and anything
skipped with its reason (for example several issues matching one title
prefix). Show titles of a few of each, not the whole list.

## 2. Ask for the go
State plainly what will happen: "Create N issues and update M in team
<KEY>, project <name>. Nothing is deleted; status, assignee and estimate are
not touched." Wait for a clear yes. Without it, stop here. If the user wants
changes first, point to `/review` or `/decide` and a rerun.

## 3. Publish
Only after the yes, the same command **without** `--dry-run`:

```bash
.venv/bin/python -m pipeline --feature <feature> publish --team <KEY> [--project "<name>"]
```

Report what was created, updated, unchanged and skipped, with the Linear
identifiers (saved as `build/<feature>/linear_publish.apply.json`). Skipped
items need the user's attention: explain why and what to do.

## 4. Finish
Remind the user: change the **spec** (sources, decisions) and rerun, not the
text of the Linear issues, because the next publish overwrites the
description of issues it owns. Publishing again is safe: existing issues are
found by their id prefix and updated, never duplicated.

If the command fails (for example an authorisation error), show the error in
one sentence and what to check; do not retry in a loop.
