# Limitations

1. **The pipeline is generic only for data-collection processes (questionnaires and forms).**
   Its knowledge model centres on information items: what is asked and in what
   form, when it is asked, when it is required, what it depends on, and who
   needs it. The executable examples can only assert whether an item is asked
   or required and what a rule yields. Behaviour-heavy requirements (approval
   workflows and states, notifications and timing, permissions, calculations)
   get squeezed into generic rules and cannot be checked by examples. Making it
   fully generic would need pluggable item types per feature, each with its
   own checklist and kind of example.

2. **Directives are followed by agents, so only their citation is guaranteed.**
   Patch decisions (override, add, exclude, resolve, accept, reject) are applied
   by code and cannot be ignored. A directive (`action: direct`, e.g. "Lonio
   computes the full tariff code") has to steer the agents before they write,
   so it is a precedence-0 instruction in their prompts, not code. The checks
   prove that something in the spec cites it, and the trace judge reads the
   directive's statement when it judges an element that cites it, but no check
   proves that everything the directive implies was written. A directive also
   reruns modelling and writing, so it costs more than a patch.

3. **Incremental reruns trust a few heuristics.** A section counts as affected
   when something it owns, covers or uses in an example (or what their
   conditions reference) changed; a dependency outside that set would not
   trigger a rewrite. The knowledge delta relies on the agent naming every
   element the new facts affect. The checks, dev refinement and review still
   run over the whole spec, and `--force knowledge.raw` / `--force sections`
   rebuild in full. A model from before incremental runs is treated as built
   with the current prompts.
   "Behaviour" is a fixed list of fields (conditions, allowed values, form,
   rule tables and expressions): a change that only rewords a description or
   adds citations is deliberately ignored for sections that merely use the
   element and for decision flags.

4. **Adding or changing a source still costs more than it needs to, mainly
   because the knowledge delta drifts.** A new source that only confirms what
   is known can still change an element in substance and rewrite every section
   that uses it: in the benchmark, an HR call confirming "Swiss yes or no"
   changed the nationality item and rewrote 6 of 8 sections (8 stories), $3.6
   of that run's $6.1; a pension fund email also rewrote an unrelated story
   (US-08.3). Other steps still work on more than changed:
   - a changed source is normalised and extracted again in full, not only its
     changed parts;
   - the knowledge delta sends the whole previous model to the agent, even
     when a handful of facts changed;
   - any change to guidance, a directive or an agent's system prompt rebuilds
     the model and every section from scratch (prompts are part of each
     stage's fingerprint).
   The delta guard is a cause check, not a meaning check: a change that cites
   a new fact is accepted even if the fact does not really require it, and a
   new high-precedence source that contradicts much of the model may need
   changes the guard reverts. The reverted changes are listed in review.md;
   `--force knowledge.raw` rebuilds in full when they are wanted.

   **How we reduced it: an overnight optimisation loop.** An agent ran
   unattended overnight in a cloud session on a branch, on the same Max login:
   1. It added real token logging per stage (`usage_this_run` in
      report.json).
   2. It built a benchmark (`bench/`): a fresh full rebuild as the frozen
      baseline, plus three mock sources with expected changes (an HR email
      asking for an email copy of the answers, a pension fund email with a
      2027 insurance rule and the canton for employees abroad, an HR call that
      contradicts decision D-007). Each case measures tokens, changed stories,
      errors, examples, open questions and the verdict, and a no-op rerun
      right after must call no agent.
   3. It applied the optimisations one at a time, unit-tested without AI, and
      gated them on the benchmark: no check that held before may fail, the
      verdict must stay the same, and tokens must go down. A failing case was
      rerun once to rule out model noise. When the Max 5-hour limit stopped a
      run, it resumed after the reset.

   Four savings passed the gate. Over the three new-source cases tokens fell
   75% (5.85M to 1.44M) and the SDK cost estimate 39% ($17.98 to $10.92):
   - dev refinement on reruns: one call on the changed files (plus feature.md
     and related stories) instead of a 39-turn read loop over every file
     (-$2.67);
   - section writers get only the part of the knowledge model their section
     owns or uses, the rest as a one-line index (-$2.14);
   - the fact judge caches verdicts per fact, so only new facts are judged
     (-$1.13);
   - review, flow and section assignment run on Sonnet instead of Opus
     (-$0.87).
   The no-op check also found two defects, now fixed: a decision flagged for
   new evidence lost its flag on the next rerun without being re-confirmed,
   and a rerun with nothing new re-ran the reviewer. Results:
   `bench/SUMMARY.md`. Not yet re-measured: a full rebuild after the changes.
   Next: stop the knowledge-delta drift above, then send the delta agent only
   the elements related to the new facts and extract only changed units.
