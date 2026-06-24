# Prefer Engineering Standards Over Local Style

## Mistake Pattern

I treated nearby code style as the default source of truth, even when the project expects reusable style guidance to come from the `engineering-standards` skill.

## Rule

When style guidance is needed and `engineering-standards` is available, follow that skill instead of preserving inconsistent local style. Use nearby code as context only when it does not conflict with the skill or an explicit project rule.
