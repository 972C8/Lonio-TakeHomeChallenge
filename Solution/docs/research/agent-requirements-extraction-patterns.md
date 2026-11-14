# Agent-driven requirements extraction: patterns and sources

_13 Nov 2026 · Research for the Lonio take-home (HR transcript + pension portal screenshots + Zurich source tax calculator → traceable onboarding requirements)_

## TL;DR

Nobody serious is doing "dump everything into one prompt, get a PRD". The teams and papers that report good results all converge on the same shape: **split by source, extract small facts with an anchor back to the source, synthesize requirements from those facts, then verify mechanically (every requirement cites something; every source chunk is covered or explicitly dropped), and keep a human gate.** The Claude Agent SDK gives you most of the plumbing for this: subagents for per-source isolation, JSON-schema structured outputs, and a gather → act → verify loop.

## How companies are actually doing it

**Uber, "PRD Evaluator" (May 2026).** An AI first-pass reviewer that sits before human PRD reviews. It (1) builds a knowledge base from linked docs, decks, meeting notes and past experiments, (2) classifies the PRD to pick review depth (lighter for UX parity, full for net-new, extra scrutiny for pricing/policy), (3) scores fixed dimensions such as scope, UX impact and metric rigor, and (4) outputs a scorecard: Ready / Ready with Caveats / Not Ready, with per-gap findings that include suggested replacement text and evidence from the linked docs. Their lessons: a fixed framework beats generic critique, "hard boundaries make output more honest", and prioritizing findings is part of the product. Sources: [Uber blog: First-pass PRD](https://www.uber.com/ad/en/blog/first-pass-prd/), [Department of Product write-up](https://departmentofproduct.substack.com/p/how-ubers-product-teams-built-a-prd).

**Cloudflare and DoorDash (review agents).** Cloudflare found that several tightly scoped reviewer agents beat one general reviewer, and that defining what *not* to flag matters as much as what to flag. DoorDash optimized for "fewer comments, more useful feedback". Humans keep final authority. Source: [InfoQ, June 2026](https://www.infoq.com/news/2026/06/ai-prd-code-review-governance).

**Anthropic (Agent SDK guidance).** The recommended loop is gather context → take action → verify work → repeat. Use agentic search over files before embeddings, use subagents to parallelize and keep each context clean (they return only the relevant excerpts), and verify with rules first (linters, schema checks, screenshots); LLM-as-judge is called "generally not a very robust method" and is best kept for fuzzy checks. Build a small eval set from real cases. Source: [Building agents with the Claude Agent SDK](https://claude.com/resources/articles/building-agents-with-the-claude-agent-sdk).

**GitHub Spec Kit / AWS Kiro (spec-driven development).** Not extraction tools, but they set the output conventions engineering teams now expect: a chain of Markdown artifacts (Spec → Plan → Tasks), templates and quality checklists per stage, and in Kiro's case acceptance criteria in EARS notation ("WHEN … THE SYSTEM SHALL …"). Sources: [Spec Kit](https://github.github.com/spec-kit/), [Spec Kit vs Kiro vs Claude Code](https://glukhov.org/ai-devtools/ai-coding-assistants/spec-kit-vs-kiro-vs-claude-code/).

## What research says about transcript → requirements

**LENS (Univ. Ottawa + eSentire, 2026).** Claude Sonnet 4.5 extracted user stories from 12 one-hour stakeholder interviews, each with a timestamp and transcript excerpt. At temperature 0.7: 100% recall, 73% precision. The false positives are instructive: current manual work mistaken for a requirement (66%), existing automation mistaken for a requirement (17%), and confirmation-seeking "…, right?" phrasing (17%). A second pass inferred *latent* requirements; experts liked most of them, but the authors say to treat them as discussion starters because they "may appear plausible while remaining misaligned with actual system constraints." Source: [arXiv 2606.25867](https://arxiv.org/html/2606.25867).

**Inter2US (2026).** A concrete, reusable way to measure traceability. Chunk the transcript into overlapping 3-speaker-turn windows, then ask a judge per (chunk, requirement) pair: "could a knowledgeable reader infer this from the chunk alone?" That yields **faithfulness** (share of requirements supported by at least one chunk) and **coverage** (share of chunks used by at least one requirement). Pairwise judging scored 0.84 F1 vs 0.49 for whole-transcript judging, so chunking matters a lot. Source: [arXiv 2510.08622](https://arxiv.org/html/2510.08622).

**Broader reading.** [LLMs for Requirements Engineering: a cross-task evaluation](https://arxiv.org/abs/2608.21531), and [From Regulation to Requirements](https://pith.science/paper/2607.04448) (regulatory text → requirements with explanations, relevant to the source tax rules).

## Tooling worth knowing

- **Agent SDK structured outputs.** Pass a JSON Schema (generated from Pydantic or Zod); the SDK validates and re-prompts on mismatch, and returns `error_max_structured_output_retries` if it can't comply, so you can fail closed. Make fields optional where a source may not provide them. [Docs](https://code.claude.com/docs/en/agent-sdk/structured-outputs).
- **Claude Citations API.** Pass sources as `document` blocks with citations enabled; the model returns `cited_text` with character, page or block locations. It won't cite locations you didn't provide, and Anthropic reports better recall and precision than prompt-based quoting. Plain text is cited per sentence; use custom content blocks to cite per speaker turn. [Cookbook](https://platform.claude.com/cookbook/misc-using-citations), [announcement](https://www.anthropic.com/news/introducing-citations-api).
- **Google LangExtract.** Open-source library that maps every extracted entity to exact character offsets in the source; a good reference design even if you stay on Claude. [Comparison with LlamaIndex extraction](https://www.nutrient.io/blog/langextract-vs-llamaindex-extraction-comparison/).

## Suggested pipeline for the Lonio challenge

This section is my synthesis of the sources above, applied to your three inputs.

1. **Normalize each source into addressable units** (one subagent per source type, in parallel).
   - Transcript: split into speaker turns with IDs (`T-042`), keep timestamps. Flag confirmation-seeking phrasing ("…, right?") per LENS.
   - Portal screenshots: a vision pass that outputs a field inventory (screen, label, field type, required/optional, options, validation hints), each with an ID like `S2-F07` and the screenshot file name.
   - Tax calculator: don't let the model do the math. Have an agent drive it through a tool (or read its rules) and record input → output test vectors (`C-03`). These become acceptance criteria.
2. **Extract atomic facts, not requirements.** One claim per fact, with its anchor and a verbatim quote. Tag `explicit` vs `inferred`, and `current-state` (how they do it today) vs `desired` (what the product should do). The second tag targets LENS's biggest error class.
3. **Synthesize requirements from facts** with a structured-output schema, roughly: `id`, `statement` (EARS style), `type` (functional / data field / validation / calculation / compliance), `source_refs[]` (anchor + quote), `confidence`, `status` (confirmed / inferred / open question), `conflicts_with[]`. Inferred items go to an "Open questions" section, never silently into the spec.
4. **Verify mechanically before any LLM judge.**
   - Every requirement has at least one `source_ref`, and every quote is an exact substring of its source (plain string check).
   - Coverage report: transcript turns, screenshot fields and calculator vectors no requirement uses, listed so a human can confirm they're intentionally out of scope.
   - Conflict check: the same field described differently by HR vs the portal (e.g. required vs optional) becomes an open question.
   - Only then a scoped LLM judge for faithfulness, Inter2US-style, per requirement against its cited chunk.
5. **Render Markdown deterministically from the JSON** (templates, not free generation): requirements grouped by onboarding step, a traceability matrix (requirement → sources), open questions and conflicts, and calculator test vectors as acceptance criteria.
6. **Reviewer gate, Uber-style.** A final scoped reviewer outputs Ready / Ready with caveats / Not ready with evidence-linked findings; a human signs off.
7. **Small eval set.** Hand-label 15–30 expected requirements from the provided sources and report precision, recall, faithfulness and coverage. That alone makes a take-home submission stand out.

## Pitfalls the sources call out

- Whole-document judging is much worse than chunk-level judging (Inter2US: 0.49 vs 0.84 F1).
- Describing today's process is not a requirement (LENS's main false-positive class).
- Inferred requirements sound plausible and are often wrong on constraints; label them.
- One generalist reviewer is noisier than several narrow ones (Cloudflare).
- LLM-as-judge is the weakest verifier; prefer rules and exact-match checks where you can (Anthropic).
