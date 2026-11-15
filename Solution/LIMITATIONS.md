# Limitations

The pipeline is quite robust in terms of knowledge extraction and completeness of requirements.
Together with the skills like /review, a human can provide additional context to improve results.
However, when building the pipeline and testing with additional mock data, I identified two central limitations.

1. **Letting the pipeline process updated sources is more costly than necessary.**
   Even when a new input only affects 1-2 requirements, the agent would double-check and improve all user stories.
   This is especially troublesome when the change is small and the user story could be manually fixed within a couple of
   minutes, but the pipeline takes 20 minutes to run.
   The problem comes from the agents not having enough context about the impact of a new change.
   I ran an overnight cloud session to let the agent self-optimize, which already saw tokens
   fall by 70%: a) use weaker models (e.g. Sonnet) where feasible; b) provide the delta as context rather than letting
   them re-investigate all sources; and c) the dev refinement agent only challenges the changed files rather than
   everything.
   Nonetheless, the pipeline is still overengineered for small source changes. For instance, the dev refinement agent
   challenges to a depth and specificity of details that could just be inferred via best practices.
   Future improvements should look at making the pipeline feasible for everyday use with reasonable run times while
   ensuring the correctness of results. Specifically, I would look into steps to optimize the pipeline for updated info,
   through mechanisms like evaluating the relevance of each existing requirement, focusing only on the relevant parts,
   and loosening the review process for simple requirement changes.

2. **The pipeline is generic only for data-collection processes (questionnaires and forms).**
   Its knowledge model centres on information items: what is asked and in what form, when it is asked, when it is
   required, what it depends on, and who needs it. The executable examples can only assert whether an item is asked
   or required and what a rule yields. Behaviour-heavy requirements (approval workflows and states, notifications and
   timing, permissions, calculations) get squeezed into generic rules and cannot be checked by examples.
   In practice, every new requirement should be used to improve the pipeline. For new types of sources and processes,
   the pipeline could be improved and tested ad-hoc.