# Bundled Setup Inputs

These references let `setup-lean-coding-agent` initialize a project using only the installed plugin. They are snapshots of canonical sources in this repository:

- [Agent TOML templates](agents/) are snapshots of `.codex/agents/*.toml`.
- [`config.toml`](config.toml) is the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- [`baseline/AGENTS.md`](baseline/AGENTS.md) and [`baseline/CLAUDE.md`](baseline/CLAUDE.md) are snapshots of the repository baseline files.
- [`docs/incidents/README.md`](docs/incidents/README.md) is the incident report template.
- [Skill override files](skill-overrides/) are snapshots of `skills/skill-overrides/`.
- [`release.json`](release.json) records the bundle version and repository for project-local update checks.

Update these copies whenever their source files change. The setup script copies other bundled skills from their sibling directories in the installed plugin.
