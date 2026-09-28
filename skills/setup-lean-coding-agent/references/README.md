# Bundled Setup Inputs

These references let `setup-lean-coding-agent` initialize a project using only its installed skill files and the sibling skills installed alongside it. The files here are the canonical agent templates; the remaining references are bundled copies of their canonical sources:

- [Agent TOML templates](agents/) are the canonical templates copied into initialized projects, with each project's selected model applied during setup.
- [`config.toml`](config.toml) is the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- [`baseline/AGENTS.md`](baseline/AGENTS.md) and [`baseline/CLAUDE.md`](baseline/CLAUDE.md) are snapshots of the repository baseline files.
- [`docs/incidents/README.md`](docs/incidents/README.md) is the incident report template.
- [`release.json`](release.json) records the skills collection version and repository for the installed release checker.
- [Skill override files](skill-overrides/) are snapshots of `skills/skill-overrides/`.

Update these copies whenever their source files change. The setup script copies skills from sibling directories in the installed skill directory.
