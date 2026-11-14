# Publishing feature specs to Linear

Status: **designed; dry run implemented** (`pipeline publish --dry-run`).
Nothing has been sent to a real Linear workspace.

## Principles

1. **Git is the source of truth; Linear is a projection.** Feature specs are
   generated, reviewed and versioned as Markdown in the repo. Linear receives a
   copy that engineering works from. The Markdown files remain the deliverable.
2. **Plan in code, execute with a narrow agent, verify in code.** What to
   create, update or cancel is computed deterministically. An agent only
   executes that plan through the Linear MCP server and cannot improvise.
3. **Idempotent.** Re-publishing unchanged specs is a no-op. A source change
   becomes a small, explained set of updates, never duplicates.
4. **Clear ownership.** The pipeline owns issue *content*. Engineering owns
   *workflow*: status, assignee, estimate, cycle and their own labels. The
   pipeline never touches those, and never deletes anything.
5. **Outward-facing, so a human approves.** Every publish shows a dry run
   first. Writing requires an explicit `--apply` from the product owner.

## The Linear MCP server

- Endpoint `https://mcp.linear.app/mcp` (Streamable HTTP; the SSE endpoint is
  deprecated). Read-only variant: `https://mcp.linear.app/mcp/readonly`.
- Auth: interactive OAuth 2.1, or `Authorization: Bearer <API key or OAuth
  token>`. For an unattended pipeline run, that means a restricted API key or
  an app-user token.
- Officially it can "find, create and update" issues, projects, comments and
  documents. Linear's docs don't list the tools; the connector exposes these,
  among others:
  - `save_project`, `save_milestone`
  - `save_issue`: creates without an id and updates with one. It supports
    `parentId`, and labels via `addLabels` / `removeLabels`. A team is required.
  - `save_document`, `save_comment`
  - `list_issues`, `list_issue_labels`, `list_issue_statuses`
  
  The exact tool set is read from the server's `tools/list` at run time.
- Rate limits are Linear's API limits: HTTP 429 with `Retry-After`, and 200
  comments per minute per issue.
- Descriptions are Markdown and support a collapsible section
  (`+++ title … +++`). We use it to keep evidence out of the way.
- Linear's own guidance for agent workflows matches our principles: show
  proposed changes before applying, match only on strong evidence, and report
  anything unmatched instead of guessing.

Sources: [Linear MCP docs](https://linear.app/docs/mcp),
[changelog](https://linear.app/changelog).

## Mapping

| Feature spec | Linear | Content |
|---|---|---|
| problem (e.g. employee onboarding) | **project** | goal + stakeholders (from the package README) |
| package overview, information catalogue, out of scope | **project documents** | rendered Markdown, one document each |
| feature `FEAT-02-…` | **parent issue** `[FEAT-02] <title>` + **milestone** of the same name | goal, context, information needed, business rules (decision tables) |
| user story `US-02.1` | **sub-issue** of the feature, `[US-02.1] <title>` | *As / I want / so that*, priority reason, acceptance criteria with example tables; evidence in a collapsed `+++ Evidence +++` section |
| open question `OQ-03` | **issue** `[OQ-03] Decision needed: …`, label `needs-decision`, assigned to the product owner, linked from the affected story | question, why it matters, options, recommendation |
| traceability | inside each issue (collapsed evidence: fact ids + verbatim quotes) and a link to the spec file in git | |

**Priority:** story P1/P2/P3 → Linear priority Urgent/High/Medium.

**Labels:**
- The pipeline only adds or removes labels in its own `spec:` namespace: `spec:P1`, `spec:inferred`, `spec:needs-decision`, `spec:stakeholder/hr`.
- It never sets plain labels; those belong to engineering.

## Identity and idempotent re-publish

- **Stable ids.** Feature, story, criterion and open-question ids come from the
  spec and stay stable across runs. The pipeline reuses existing ids, and
  decisions pin them.
- **Mapping file.** `problems/<problem>/linear_map.yaml` is committed to git.
  It maps each spec id to the Linear issue id and identifier (e.g.
  `ONB-42`) and the hash of the content last published. After a publish, the
  rendered front matter shows `linear: ONB-42`, so the Markdown and Linear
  point at each other.
- **Recovery.** If the map is lost, `list_issues` by the `[US-…]` title prefix
  rebuilds it. Only exact prefix matches count; anything else is reported, not
  guessed.

What a re-publish does, per element:

| Situation | Action |
|---|---|
| new id | create (story as a sub-issue of its feature) |
| same id, same content hash | nothing |
| same id, changed content | update the description and title, plus **add a comment** saying what changed (which criteria or examples) and **why** (which source facts or decisions changed) |
| same id, but someone edited the description in Linear (its current hash ≠ the last published hash) | **do not overwrite**; flag the drift in `review.md` so the product owner can merge the edit into a decision or source |
| id removed from the spec, issue not started | move to **Canceled** with a comment explaining the reason |
| id removed, issue in progress or done | do **not** cancel; comment and add `spec:needs-decision` (engineering and the product owner decide) |
| open question resolved by a decision | comment with the decision, then close as Done |

## Agent or API?

| | MCP from an agent (chosen) | GraphQL API from code |
|---|---|---|
| auth | OAuth or a bearer key, handled by the MCP client | API key handled in our code |
| determinism | plan computed in code; agent limited to `save_*` / `list_*` tools; read-back verified in code | fully deterministic |
| fits the pipeline | same Agent SDK wrapper as every other stage; the same server works interactively in Claude Code | separate client and error handling to maintain |
| main risk | an agent mis-executing a step, which the code read-back catches | none beyond API changes |

Both work. MCP is chosen because publishing is a small, plan-driven step,
the same connector serves interactive use (e.g. "pull my comments from Linear
into decisions"), and the read-back check makes it as safe as code. If the
volume grew, the executor could be swapped for direct API calls without
changing the plan or the mapping file.

## Flow

```
pipeline publish --dry-run   → linear_map.yaml + spec  → build/<p>/linear-plan.md  (create / update / cancel / drift, with payload previews)
pipeline publish --apply     → human confirms the plan → publisher agent executes it via Linear MCP
                             → code reads every touched issue back, compares hashes → updates linear_map.yaml, commits
pipeline pull-decisions      → reads comments on needs-decision issues → drafts decisions.yaml entries for the product owner
```

The `--apply` and `pull-decisions` commands are designed but not
implemented. They need a Linear workspace and the product owner's go.
