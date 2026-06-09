# agents

This repository is the shared base I want to reuse across all of my projects.

It contains the general agent guidance that should apply everywhere, regardless of stack, folder structure, or project type. The goal is to keep one central set of broad rules and standards that I can reference from each individual project.

Each project will then have its own custom `AGENTS.md` with more specific instructions for that codebase, such as:

- folder structure
- tech stack
- architecture conventions
- testing expectations
- project-specific workflows

In other words:

- this repo defines the default baseline
- each project can extend it with its own local rules

This setup keeps the global guidance consistent while still allowing every project to document what makes it unique.

## Initialize A New Project

Run the bootstrap script from this repo and point it at the target project repo:

```bash
python scripts/init_project_agent.py ../your-project-repo
```

The script will:

- create or update the target repo's `AGENTS.md` so it references this repo's shared `AGENTS.md`
- create `agent-context/` in the target repo
- copy every installable skill from this repo's `global-skills/` folder into the target repo's `.codex/skills/`
- write `agent-context/global-skills-installed.json` so the setup can be rerun cleanly

To change which skills get installed into future projects, add or remove skill folders in [global-skills](/C:/Users/Craas/Desktop/projects/agents/global-skills).

Repo-only skills for maintaining this shared repo should live under [.codex/skills](/C:/Users/Craas/Desktop/projects/agents/.codex/skills). Do not place repo-only skills in `global-skills/`, because everything installable there is copied into new project repos.
