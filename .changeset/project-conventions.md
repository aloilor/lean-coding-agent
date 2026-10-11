---
"lean-coding-agent": minor
---

Replace `codebase-onboarding` with `project-conventions`, which captures only non-obvious conventions in `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md` from repo evidence plus a short interview. Setup no longer seeds `agent-context/`, records the release manifest in `.agents/skills-installed.json` (moving a legacy `agent-context/skills-installed.json`), and removes managed skills a release no longer ships. Projects installed with the Skills CLI need to add `project-conventions` again. Rationale and citations are in `docs/project-conventions.md`.
