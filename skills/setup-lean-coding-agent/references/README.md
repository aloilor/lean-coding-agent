# Bundled Setup Inputs

These references let `setup-lean-coding-agent` initialize a project using only its installed skill files and the sibling skills installed alongside it. The files here are the canonical agent and artifact templates; the remaining references are bundled copies of their canonical sources:

- [Codex agent templates](agents/codex/) and [Claude Code agent templates](agents/claude-code/) are the canonical subagent templates copied into initialized projects for each selected coding agent, with each project's selected model applied during setup. Keep the instructions in both sets synchronized; the Claude Code copies name skills in neutral wording instead of Codex `$skill` mentions.
- [Plan template](templates/plan.md), [implementation-report template](templates/implementation-report.md), and [code-review template](templates/code-review.md) are the canonical artifact templates shared by both coding agents. Their core sections stay fixed while detail scales to the work; workflow and agent instructions retain ownership of approval gates and review rules. Setup refreshes these three files in `.agents/templates/` on every run while preserving other project-owned templates. Completed artifacts remain in `.agents/plans/`, `.agents/implementation-reports/`, and `.agents/code-reviews/`.
- [`config.toml`](config.toml) is the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- [`baseline/AGENTS.md`](baseline/AGENTS.md) and [`baseline/CLAUDE.md`](baseline/CLAUDE.md) are snapshots of the repository baseline files.
- [`docs/incidents/README.md`](docs/incidents/README.md) is the incident report template.
- [`release.json`](release.json) records the skills collection version and repository for the installed release checker.
- [Skill override files](skill-overrides/) are snapshots of `skills/skill-overrides/`.

Update these copies whenever their source files change. The setup script copies skills from sibling directories in the installed skill directory.
