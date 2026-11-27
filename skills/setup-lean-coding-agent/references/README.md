# Bundled Setup Inputs

These references let `setup-lean-coding-agent` initialize a project using only its installed skill files. The files here are the canonical agent templates; the remaining references are bundled copies of their canonical sources:

- [Codex agent templates](agents/codex/) and [Claude Code agent templates](agents/claude-code/) are the canonical subagent templates copied into initialized projects for each selected coding agent, with each project's selected model applied during setup. The planner, bug-diagnostician, implementer, and code-reviewer templates are thin: they load the matching skill (`plan`, `diagnose`, `implement`, `code-review`), which owns the instructions and bundles its artifact template under `references/`. Keep both sets synchronized.
- [`config.toml`](config.toml) is the baseline Codex project configuration copied when the target has no `.codex/config.toml`; its footer status line shows model and reasoning, project name, Git branch, context window size, and used tokens.
- [`statusline.mjs`](statusline.mjs) is the Claude Code status line copied to `.claude/statusline.mjs` when missing and registered in `.claude/settings.json` when no status line is set; the repository's own `.claude/statusline.mjs` is a copy of it.
- [`baseline/AGENTS.md`](baseline/AGENTS.md) and [`baseline/CLAUDE.md`](baseline/CLAUDE.md) are snapshots of the repository baseline files.
- [`docs/incidents/README.md`](docs/incidents/README.md) is copied into projects to explain incident reports; keep its template in sync with [`skills/diagnose/references/incident-report.md`](../../diagnose/references/incident-report.md).
- [Skill override files](skill-overrides/) are snapshots of `skills/skill-overrides/`.

Update these copies whenever their source files change. Skills are installed and tracked by the Skills CLI.
