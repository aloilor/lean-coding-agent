---
"lean-coding-agent": minor
---

Rename `grill-with-docs` to `lean-grill-with-docs` to identify it as part of Lean Coding Agent. Update existing invocations to `$lean-grill-with-docs` and rename any project override from `.agents/skill-overrides/grill-with-docs.md` to `.agents/skill-overrides/lean-grill-with-docs.md`, updating its index entry and skill references. Remove the old installed skill folder after reinstalling.

`lean-grill-with-docs` now keeps its documentation in `docs/conventions/`: `docs/conventions/GLOSSARY.md` (and `docs/conventions/GLOSSARY-MAP.md`) instead of the repo root, and ADRs in `docs/conventions/adr/` instead of `docs/adr/`; move existing files there. Add a `--docs-dir <folder>` option to setup. It writes a `lean-grill-with-docs` skill override so the project's `GLOSSARY.md`, `GLOSSARY-MAP.md`, and ADRs live in the chosen folder instead of `docs/conventions/`. Projects can also set the folder by writing that override by hand.
