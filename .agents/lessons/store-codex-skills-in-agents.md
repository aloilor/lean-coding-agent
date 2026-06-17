## Mistake Pattern

I mirrored Codex skills into `.codex/skills` after the Skills CLI had already installed them into `.agents/skills`, creating duplicate skill copies.

## Rule

Store Codex skills in `.agents/skills`. Do not copy or mirror those skills into `.codex/skills`; only keep Claude Code copies in `.claude/skills` when needed.
