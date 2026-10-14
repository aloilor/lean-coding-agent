---
"lean-coding-agent": minor
---

Replace `codebase-onboarding` with `init-conventions`, which writes repo-specific, verified conventions to `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md` from repo evidence, commands it runs, and a user interview. Setup no longer seeds `agent-context/`, records the release manifest in `.agents/skills-installed.json` (moving a legacy `agent-context/skills-installed.json`), and removes managed skills a release no longer ships. Projects installed with the Skills CLI need to add `init-conventions` again.