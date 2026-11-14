---
name: new-adapter
description: Scaffold a new source adapter (a new type of source such as email threads, regulation PDFs, spreadsheets, another portal). Use when a new kind of source must be added to the pipeline.
---

# /new-adapter <type>

1. Read `pipeline/adapters/base.py` (the contract) and the closest existing
   adapter (`transcript` for text, `screenshots` for images, `web_calculator`
   for live sites).
2. Create `pipeline/adapters/<type>/` with:
   - `adapter.py` – subclass `Adapter`; set `type`;
     implement `normalize()` returning `Unit`s with **stable ids** built
     with `self.uid(local_id)` (so they start with the source id and never
     clash with another source) and the exact source text (deterministic if at all possible); override
     `verify_anchor()` if exact substring matching does not fit the type;
     extend `normalize_inputs()` with every file whose change must trigger a
     rerun.
   - `agent.md` – the extraction prompt, following the structure of the
     existing ones (fact kinds, anchors verbatim, explicit vs inferred,
     desired vs current_state, `{{guidance}}` placeholder).
   - `config.yaml` – model role and options.
3. Register it in `get_adapter()` in `base.py`.
4. Add the source to the feature's `profile.yaml` with `authority` and
   `precedence`, then `python -m pipeline run`. Check `review.md` coverage for
   the new source.
