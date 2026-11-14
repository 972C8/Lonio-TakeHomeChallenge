# Open-source pipelines: sources → requirements via AI agents

_13 Nov 2026 · Survey for the Lonio take-home. Stars and last push from the GitHub API on 13 Nov._

## Bottom line

There is **no established, widely used open-source project** that does what the challenge asks: take several kinds of sources (a meeting, portal screenshots, a web calculator) and produce traceable requirements with agents. The large projects in this space solve neighbouring problems: **GitHub Spec Kit** (≈150k ★) turns an idea into a spec but extracts nothing from sources, and **Google LangExtract** (≈39k ★) extracts facts with character offsets but stops there. Everything that does the full job is a research prototype or a solo project with 0 to 2 stars.

That is useful for the video. Your pipeline is not reinventing a standard tool; it combines patterns that only exist separately. The best ideas to borrow, and to cite as prior art, are below.

## The candidates

| Repo | ★ / last push | Inputs | Output | How it keeps output correct | Fit |
|---|---|---|---|---|---|
| [ReqLens](https://github.com/pld4kor-dot/ReqLens) ([AACL 2026 demo paper](https://aclanthology.org/2026.aacl-demo.10.pdf)) | 0 / Jul 2026, MIT | PDF, DOCX, MD, CSV, text (interviews, policies, legacy specs) | SRS + traceability matrix + requirements graph + conflict report + clarification questions | 10 agents. An **Evidence agent** labels every candidate ENTAILED / CONTRADICTED / INSUFFICIENT against source spans; graph checks for conflicts and duplicates; mandatory human review queue | **Closest architecture match.** No image input. Heavy stack (FastAPI, Streamlit, Postgres, Azure OpenAI) |
| [requirements-to-backlog](https://github.com/pablodpavon/requirements-to-backlog) | 0 / Nov 2026, MIT | One workshop transcript, numbered turns | **Epics + user stories with Given/When/Then**, open questions, assumptions, contradictions; MD, CSV, HTML demo | One Claude call with a JSON schema, then **deterministic checks only**: quote must exist in the cited turn, IDs valid, duplicates, untestable words in criteria, **coverage of turns that produced nothing** | Best small example of a **user-story output done rigorously**. Single source only |
| [agentic-requirements-engineering](https://github.com/Zaryab111/agentic-requirements-engineering) | 0 / Oct 2026, MIT | Stakeholder interview transcripts | **EARS** requirements as Markdown with front matter, ISO 29148 | Built on **Claude Code**: `AGENTS.md` roles (Elicitor, Specifier), a skill, a **JSON Schema for front matter**, a banned-vague-words linter, a hook that makes evidence files read-only, CI that checks every quote character by character | Very close to your setup (Claude Code, Markdown + front matter). Single source |
| [youtube-to-spec](https://github.com/alikmlsipahi/youtube-to-spec) | 1 / Aug 2026 | Videos | Module → Feature → Requirement, each with timestamps | Two decoupled Claude Code skills sharing a **versioned data contract**; resumable | Nice "collector vs distiller" split. Video only |
| [Meeting-audio-to-requirements](https://github.com/gabrielsfg/Meeting-audio-to-requirements) ([paper](https://cbsoft.sbc.org.br/2026/data/papers/workshops/From%20Meeting%20Audio%20to%20Requirements%20A%20Generative-AI%20Multi-Agent%20Pipeline.pdf)) | 2 / Sep 2026, MIT | Meeting audio or transcript | INVEST user stories → IEEE 830 SRS (MD/PDF) with diagrams | 4 sequential agents (Whisper, Haiku, Sonnet); **no source links or verifier**. 72.7% recall against a human gold standard | Shows the failure modes: a transcription error carried all the way through, and **UI-only requirements missed because the pipeline can't see screens** |
| [agile_v_skills](https://github.com/Agile-V/agile_v_skills) | 55 / Oct 2026, CC BY-SA | A change description (no source extraction) | `REQ-XXXX` with acceptance criteria, 18 JSON Schemas for evidence | Separate requirement-architect, logic-gatekeeper and red-team verifier agents; two human gates; typed links REQ ← implements / verifies | Downstream governance, not extraction |
| [MARARE-Elicitation](https://github.com/GPT-Laboratory/MARARE-Elicitation) | – | Live meetings (React + Flask) | Functional requirements | – | README says it is no longer maintained |

Adjacent, large and maintained: [GitHub Spec Kit](https://github.com/github/spec-kit) (spec format and workflow, 149,650 ★) and [Google LangExtract](https://github.com/google/langextract) (grounded extraction with character offsets, 39,310 ★).

## What to borrow for the Lonio pipeline

1. **ReqLens: three-way evidence labels.** Supported / contradicted / insufficient is sharper than a plain "supported or not" judge, and "contradicted" maps directly onto your conflict-based open questions.
2. **requirements-to-backlog: coverage report.** It lists the source units that produced nothing and blocks items whose quote isn't found in the cited turn. If your pipeline doesn't already list uncovered transcript turns and screenshot fields, that check is cheap and convincing.
3. **agentic-requirements-engineering: harness guardrails.** A JSON Schema for front matter (matches my earlier template recommendation), a hook that makes sources read-only, and a vague-word linter, all in Claude Code. This is the closest public repo to your setup and worth a look before the video.
4. **Meeting-audio-to-requirements: proof that one source isn't enough.** Its authors report that requirements only visible in the UI are missed. That's a good argument for your screenshot and calculator stages.
5. **On user stories:** requirements-to-backlog shows stories can be rigorous when every one cites its source and has testable criteria. That supports the two-layer recommendation: stories on top, linked to the field specs.

## Caveats

- Star counts are near zero for everything except Spec Kit, LangExtract and agile_v_skills. Treat these as references for ideas, not dependencies.
- ReqLens's evaluation is partly synthetic (adversarially poisoned PROMISE/PURE datasets) with a 4-person expert study.
- Only the README (and the ReqLens and Meeting-audio papers) was read for each repo; the code was not run.
