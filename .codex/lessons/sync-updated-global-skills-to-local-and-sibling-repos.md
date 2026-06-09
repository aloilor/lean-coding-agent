# Sync Updated Global Skills To Local And Sibling Repos

## Mistake Pattern

I updated a shared skill in `global-skills/` without also making sure the same maintained copy was available in this repo and ready to be synced into sibling project repos.

## Rule

When a shared skill in `global-skills/` is used locally or copied into project repos, keep a maintained local copy where needed and provide a sync path that updates matching `.codex/skills/<skill>` directories in this repo and sibling project repos under `../`.
