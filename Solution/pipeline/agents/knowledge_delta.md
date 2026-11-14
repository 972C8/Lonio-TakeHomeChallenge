# Updating an existing knowledge model (delta mode)

You are not building the model from scratch. A model already exists, a product
team has reviewed it, and stories have been written from it. Every change you make
rewrites stories people have already read. Change only what the new or removed
facts force.

- **Minimal change.** Return only the elements a new, changed or removed fact
  forces you to add, change or remove. Do not improve, reword, re-cite or
  reorganise anything else, even if you would write it differently today.
- **Name the cause.** Every element you return must cite at least one of the new
  or changed facts in its `source_refs` (or in a decision-table row). If an
  element changes because a fact it cited was removed, say so in `rationale`.
  Code reverts any change that cites no new, changed or removed fact.
- **Keep ids and names.** An existing item or rule keeps its id and its `name`.
  Code reverts renames, because a renamed label changes every story that shows it.
- **Keep wording.** When you change an element, keep every field the facts do not
  affect exactly as it was, character for character.
- **New topic, new element.** If a new fact introduces something new (a new
  piece of information, a new rule), add a new element. Don't widen an existing
  one so the fact fits.
- **Conflicts.** If a new fact contradicts an existing element, apply source
  precedence as usual. If it is unclear which source wins, add an open question
  rather than silently changing the element.
- **Nothing forced, nothing returned.** A new fact that changes nothing
  (context, a repetition of what the model already says) needs no output.
