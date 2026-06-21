# Preserve Upstream Subagent Shape When Customizing

## Mistake Pattern

I was asked to create the exact same upstream subagent with narrow adaptations, but I rewrote it into a different local prompt instead of preserving the source structure and wording.

## Rule

When the user points to a source subagent and asks for that same subagent with adaptations, use the upstream file as the base. Preserve its model, sections, checklist, examples, and output format unless the requested adaptation directly requires a change.
