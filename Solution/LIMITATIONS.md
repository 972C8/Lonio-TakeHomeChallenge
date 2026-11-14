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
