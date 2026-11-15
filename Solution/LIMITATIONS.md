# Limitations

Each limitation says what it is, where we think it comes from, and in which
direction we would improve it. Items 5 to 8 come from rerunning the onboarding
feature from scratch on 2026-11-15.

1. **The pipeline is generic only for data-collection processes (questionnaires and forms).**
   Its knowledge model centres on information items: what is asked and in what
   form, when it is asked, when it is required, what it depends on, and who
   needs it. The executable examples can only assert whether an item is asked
   or required and what a rule yields. Behaviour-heavy requirements (approval
   workflows and states, notifications and timing, permissions, calculations)
   get squeezed into generic rules and cannot be checked by examples.

   *Where it comes from:* the knowledge model and the example format were designed around the
   onboarding questionnaire, the first and only feature so far.

   *Direction:* pluggable item types per feature (state machine, notification, permission,
   calculation), each with its own completeness checklist and its own kind of
   executable example, chosen in the feature profile.

2. **Directives are followed by agents, so only their citation is guaranteed.**
   Patch decisions (override, add, exclude, resolve, accept, reject) are applied
   by code and cannot be ignored. A directive (`action: direct`, e.g. "Lonio
   computes the full tariff code") has to steer the agents before they write,
   so it is a precedence-0 instruction in their prompts, not code. The checks
   prove that something in the spec cites it, and the trace judge reads the
   directive's statement when it judges an element that cites it, but no check
   proves that everything the directive implies was written. A directive also
   reruns modelling and writing, so it costs more than a patch.

   *Where it comes from:* a directive is free text; code can check that it is cited, but not what
   it implies.

   *Direction:* turn common directives into patch decisions where possible, and let the
   review ask a judge, per directive, "what must the spec say now?" and check
   each answer against the spec.

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

   *Where it comes from:* incremental reruns save cost by guessing what a change touches; the
   guess is a dependency list built from the model, not a full impact analysis.

   *Direction:* record every dependency (including those inside rule expressions and
   notices) in the model, and run a periodic full rebuild as a control
   against the incremental result.

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

   *Where it comes from:* the delta agent rewrites elements it was only asked to confirm, and the
   guard accepts any change that cites a new fact. Whole-source extraction and
   whole-model prompts are the simple first version.

   *Direction:* make "confirms, no change" an explicit delta outcome that leaves the
   element untouched; send the delta agent only the elements related to the
   new facts; extract only the changed units of a source.

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

5. **Fact ids and source unit ids are not stable, so decisions can lose their
   target.** Rerunning the onboarding feature from scratch on 2026-11-15
   produced new ids for many facts: 19 of the 38 restored decisions (all
   `accept` decisions on inferred facts) pointed at facts that no longer
   existed and had to be retargeted by hand. Editing a transcript (inserting
   or deleting a speaker turn) shifts every later unit id (T-001, T-002 ...),
   so decisions citing those units get a stale evidence hash and must be
   re-confirmed although nothing they rely on changed.

   *Where it comes from:* a fact id is a hash of its kind and the exact
   quotes the agent chose (`make_fact_id` in `pipeline/adapters/base.py`); a
   fresh extraction quotes slightly differently and gets a new id. Unit ids
   are positional (`pipeline/adapters/transcript`).

   *Direction:* give units content-based ids (or align old and new units by
   text diff before numbering), and let decisions anchor on quotes as well as
   ids, so the pipeline can retarget them itself and only ask when the match
   is unclear.

6. **LLM judgments vary between runs.** The same dev-refinement question was
   rated a blocker in one benchmark run and not in the next with the same
   input (case B3), and review findings and wording shift between runs.

   *Where it comes from:* severity, review findings and trace verdicts are
   single samples from a model; only the gates around them are deterministic.

   *Direction:* score severity against a written rubric, take a majority of
   two or three samples for judgments that gate the verdict, and cache
   verdicts on unchanged input (as the fact judge now does).

7. **Some requirements rest on assumptions, not sources.** Where the sources
   are silent (canton for employees abroad, registered partnership and
   separated at the pension fund, spouse data for divorced or widowed
   employees, weekend start dates, Liechtenstein tariff order), the product
   owner decided provisionally (D-002 to D-004, D-039 to D-046). The stories
   state these as assumptions to be verified by a domain expert, but the
   pipeline cannot verify them.

   *Where it comes from:* the sources are a short HR call, portal screenshots
   and a calculator; they do not cover every case, and the people who can
   answer (HR, Pensionskasse Muster, the tax office) are not in the loop.

   *Direction:* publish the assumptions as tasks for the domain expert (the
   Linear step), and when the answer comes back add it as a source, so the
   decision is confirmed or replaced by cited evidence.

8. **Live sources are only as fresh as the last exploration.** The Zurich
   source tax calculator is explored on demand (`pipeline explore`); if the
   site changes, nothing notices until someone explores again. A full rebuild
   after the token optimisations has not been re-measured either, so its cost
   is only known from before them; on Claude Max a full rebuild plus two
   reruns is about what one 5-hour usage window allows.

   *Where it comes from:* exploring the site drives a browser through every
   branch, which is slow and costly, so it is not part of a normal run.

   *Direction:* a scheduled, cheap check that replays the recorded paths and
   compares results, and a full exploration only when they differ.
