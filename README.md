# agents

This repository is the shared base I want to reuse across all of my projects.

It contains the general agent guidance that should apply everywhere, regardless of stack, folder structure, or project type. The goal is to keep one central set of broad rules and standards that I can reference from each individual project.

The shared baseline stays in `AGENTS.md`, and this repo now bootstraps both Codex and Claude-friendly project files around that same baseline.

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
- create or update the target repo's `CLAUDE.md` so Claude is told to read the local `AGENTS.md`
- create `agent-context/` in the target repo
- copy every installable skill from this repo's `global-skills/` folder into the target repo's `.codex/skills/` and `.claude/skills/`
- write `agent-context/global-skills-installed.json` so the setup can be rerun cleanly

To change which skills get installed into future projects, add or remove skill folders in [global-skills](/C:/Users/Craas/Desktop/projects/agents/global-skills).

Repo-only skills for maintaining this shared repo are kept in [.codex/skills](/C:/Users/Craas/Desktop/projects/agents/.codex/skills) and mirrored into [.claude/skills](/C:/Users/Craas/Desktop/projects/agents/.claude/skills) so both tools can use them locally. Do not place repo-only skills in `global-skills/`, because everything installable there is copied into new project repos.

Why both skill folders:

- Codex looks for repo-local skills under `.codex/skills/`
- Claude Code looks for repo-local skills under `.claude/skills/`
- the shared `SKILL.md` format works for both, so this repo installs the same shared skills into each tool's expected location

## Sync Updated Shared Skills

When you want to propagate an updated shared skill from `global-skills/`, sync that change into any maintained copies in this repo and sibling project repos under `../`:

```bash
python scripts/sync_global_skills.py
```

To sync only one shared skill:

```bash
python scripts/sync_global_skills.py git-conventional-commit
```

The sync script only updates matching `.codex/skills/<skill>/` and `.claude/skills/<skill>/` directories that already exist. It does not install missing shared skills into every sibling repo automatically.
