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
