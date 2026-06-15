# Sync Updated Shared Skills To Local And Sibling Repos

## Mistake Pattern

I updated a shared skill in `skills/` without also making sure the same maintained copy was available in this repo and ready to be synced into sibling project repos.

## Rule

Whenever a skill in `skills/` is updated, sync that skill into every maintained matching `.codex/skills/<skill>` and `.claude/skills/<skill>` directory in this repo and sibling project repos under `../`.
