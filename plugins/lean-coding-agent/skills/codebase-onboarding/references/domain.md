# agent-context/domain.md

Purpose: project-specific glossary. This is the local replacement for upstream `CONTEXT.md`.

## Quality Rules

- Include only terms specific to this project.
- Keep definitions to one or two sentences.
- Define what the term is, not implementation details.
- Use `_Avoid_` to record ambiguous, deprecated, or less precise terms.

## Template

```md
# Domain

One or two sentences describing the project domain.

## Language

**Canonical Term**:
One or two sentences defining what the term is in this project.
_Avoid_: AmbiguousTerm, LegacyTerm

## Relationships

- **Term A -> Term B**: Short relationship description.

## Flagged Ambiguities

- "Ambiguous word" can mean X or Y. Preferred usage: X.

## Open Questions

- Unknown.
```

## Example

```md
**Task Note**:
A local, uncommitted markdown file that records an agent's plan, progress, and review for one task.
_Avoid_: Daily task file, scratch note
```
