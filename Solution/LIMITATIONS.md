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

4. **Adding or changing a source still uses more tokens than it needs to.**
   Incremental reruns keep untouched sections, but several steps still work on
   everything:
   - a changed source is normalised and extracted again in full, not only its
     changed parts;
   - the knowledge delta sends the whole previous model to the agent, even
     when a handful of facts changed;
   - dev refinement and the reviewer re-read the whole spec although most of
     it is unchanged (the trace judge reuses verdicts of unchanged elements);
   - any change to guidance, a directive or a prompt rebuilds the model and
     every section from scratch.
   In practice a small new source costs about $4.50 (one new story, 29
   untouched), against about $10-13 for a full rebuild.
   Possible optimisations: extract only changed units, send the delta agent
   only the elements related to the new facts, and treat a changed directive
   as a delta of the elements that cite it.
   The delta guard is a cause check, not a meaning check: a change that cites
   a new fact is accepted even if the fact does not really require it, and a
   new high-precedence source that contradicts much of the model may need
   changes the guard reverts. The reverted changes are listed in review.md;
   `--force knowledge.raw` rebuilds in full when they are wanted.
