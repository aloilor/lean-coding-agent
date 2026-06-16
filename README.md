# dev-agent-baseline

This repository is the shared base I want to reuse across all of my projects.

It contains the general agent guidance that should apply everywhere, regardless of stack, folder structure, or project type. The goal is to keep one central set of broad rules and standards that I can reference from each individual project.

The shared baseline stays in `AGENTS.md` and `CLAUDE.md`. This repo bootstraps both files into each project as exact copies of the shared defaults.

Reusable coding, design, API, refactoring, debugging, and review guidance lives in the installable `engineering-standards` skill. Each project should keep its shared project-specific context in `agent-context/`, such as:

- folder structure
- tech stack
- architecture conventions
- testing expectations
- project-specific workflows

Each project can also keep private local overrides in:

- `AGENTS.override.md`
- `CLAUDE.override.md`

Those override files are ignored by git and are meant for local-only notes.

In other words:

- this repo defines the default baseline
- each project documents shared project-specific context in `agent-context/`
- each machine can keep private overrides in the override files

This setup keeps the global guidance consistent while still allowing every project to document what makes it unique.

## Initialize A New Project

Run the bootstrap script from this repo and point it at the target project repo:

```bash
python scripts/init_project_agent.py ../your-project-repo
```

The script will:

- copy this repo's `AGENTS.md` into the target repo
- copy this repo's `CLAUDE.md` into the target repo
- create `AGENTS.override.md` and `CLAUDE.override.md` when they do not already exist
- add the override files to the target repo's `.gitignore`
- create `agent-context/` in the target repo
- copy missing baseline project-context starter files from this repo's `agent-context/`
- create `agent-context/README.md` when it does not already exist
- create `.agents/lessons/LESSONS.md` when it does not already exist
- copy every installable skill from this repo's `skills/` folder into the target repo's `.codex/skills/` and `.claude/skills/`
- write `agent-context/skills-installed.json` so the setup can be rerun cleanly

To change which skills get installed into future projects, add or remove skill folders in [skills](skills).

Repo-only skills for maintaining this shared repo are kept in [.codex/skills](.codex/skills) and mirrored into [.claude/skills](.claude/skills) so both tools can use them locally. Do not place repo-only skills in `skills/`, because everything installable there is copied into new project repos.

Why both skill folders:

- Codex looks for repo-local skills under `.codex/skills/`
- Claude Code looks for repo-local skills under `.claude/skills/`
- the shared `SKILL.md` format works for both, so this repo installs the same shared skills into each tool's expected location

## Sync Updated Shared Skills

When you want to propagate an updated shared skill from `skills/`, sync that change into any maintained copies in this repo and sibling project repos under `../`:

```bash
python scripts/sync_skills.py
```

To sync only one shared skill:

```bash
python scripts/sync_skills.py git-conventional-commit
```

The sync script only updates matching `.codex/skills/<skill>/` and `.claude/skills/<skill>/` directories that already exist. It does not install missing shared skills into every sibling repo automatically.
