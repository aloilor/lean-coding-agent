---
"lean-coding-agent": minor
---

Replace `codebase-onboarding` with `init-conventions`, which writes repo-specific, verified conventions to `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md` from repo evidence, commands it runs, and a user interview. Setup no longer seeds `agent-context/`. Projects installed with the Skills CLI need to add `init-conventions` again.