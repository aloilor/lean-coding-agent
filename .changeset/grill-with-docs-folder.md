---
"lean-coding-agent": minor
---

`grill-with-docs` now keeps the glossary in `docs/GLOSSARY.md` (and `docs/GLOSSARY-MAP.md`) instead of the repo root, next to `docs/adr/`; move an existing root `GLOSSARY.md` there. Add a `--docs-dir <folder>` option to setup. It writes a `grill-with-docs` skill override so the project's `GLOSSARY.md`, `GLOSSARY-MAP.md`, and ADRs live in the chosen folder instead of `docs/`. Projects can also set the folder by writing that override by hand.
