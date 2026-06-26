# agent-context/skills.md

Create this file during onboarding so future agents can quickly decide which project-local skill to use.

## Required Structure

```markdown
# Skills Index

## Purpose

[1-2 sentences explaining that this file maps available project-local skills to the situations where agents should use them.]

## Skill Selection

| Skill | Use when | Source | Notes |
| --- | --- | --- | --- |
| `skill-name` | [Trigger or task type from the skill description.] | `path/to/SKILL.md` | [Important constraints, related workflow, or "No extra notes".] |

## Workflow-Mapped Skills

| Workflow or request | Preferred skill | Evidence |
| --- | --- | --- |
| [Bug reports, commits, onboarding, reviews, etc.] | `skill-name` | [`AGENTS.md`, `CLAUDE.md`, or skill path] |

## Missing Or Unclear Skills

- [List task areas where project rules mention a skill that is unavailable, duplicated, stale, or unclear.]
```

## Evidence Rules

- Read each discovered `SKILL.md` frontmatter before writing its row.
- Use the skill `description` as the primary source for "Use when"; read the body only when the description is too vague.
- Deduplicate mirrored copies with the same skill name. Prefer `.agents/skills/<skill>/SKILL.md` as the source path when present; otherwise use `skills/<skill>/SKILL.md`, then `.claude/skills/<skill>/SKILL.md`, then `.codex/skills/<skill>/SKILL.md`.
- Include workflow-to-skill mappings only when project guidance explicitly names the workflow or skill.
- Do not invent missing skills. If `AGENTS.md` references a skill that is unavailable, list it under "Missing Or Unclear Skills".
- Keep rows concise. The skills index should help an agent choose a skill, not duplicate the skill instructions.
