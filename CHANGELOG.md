# lean-coding-agent

## 2.3.2

### Patch Changes

- [#14](https://github.com/aloilor/lean-coding-agent/pull/14) [`171b977`](https://github.com/aloilor/lean-coding-agent/commit/171b9776b567355a7fc23864d1411e2d01b91c1b) Thanks [@aloilor](https://github.com/aloilor)! - Setup adds `Artifact` and `PowerShell` to `permissions.deny` in `.claude/settings.json` when missing, keeping existing deny rules.

## 2.3.1

### Patch Changes

- [#12](https://github.com/aloilor/lean-coding-agent/pull/12) [`a242a5b`](https://github.com/aloilor/lean-coding-agent/commit/a242a5b113e03f4be2eb79b8a3464737ad9cfe5b) Thanks [@aloilor](https://github.com/aloilor)! - Change the Codex `bug-diagnostician` default reasoning effort from `max` to `xhigh`.

## 2.3.0

### Minor Changes

- [#10](https://github.com/aloilor/lean-coding-agent/pull/10) [`2d76456`](https://github.com/aloilor/lean-coding-agent/commit/2d76456523bdf152053ff52fb979ef4c8dd5c879) Thanks [@aloilor](https://github.com/aloilor)! - Setup now adds default Claude Code auto-compaction limits (`modelSettings.<model>.autoCompactWindow`) to `.claude/settings.json` for each model that has none.

## 2.2.0

### Minor Changes

- [`c49005c`](https://github.com/aloilor/lean-coding-agent/commit/c49005c64ec32cbfbe78fd37f1f9c521916866fd) Thanks [@aloilor](https://github.com/aloilor)! - Setup now installs a Claude Code status line in `.claude/statusline.mjs` and registers it in `.claude/settings.json` when no status line is set.

- [`a382dcd`](https://github.com/aloilor/lean-coding-agent/commit/a382dcd1f1696360e7b4871f31b9aa89c9ffc025) Thanks [@aloilor](https://github.com/aloilor)! - Run `workflow-*` skills only when the user explicitly invokes them.

## 2.1.0

### Minor Changes

- [#7](https://github.com/aloilor/lean-coding-agent/pull/7) [`247a3ef`](https://github.com/aloilor/lean-coding-agent/commit/247a3ef0a6b978e1681434bd26199793903e89f4) Thanks [@aloilor](https://github.com/aloilor)! - Make incident reports opt-in. `workflow-bug-fixing` now creates `docs/incidents/incident_YYYYMMDD_<name>.md` only when the user requests one, and carries the diagnosis through the approved plan otherwise. Rerun setup to update the installed baseline, agents, and templates.

## 2.0.0

### Major Changes

- [#5](https://github.com/aloilor/lean-coding-agent/pull/5) [`a3d9a15`](https://github.com/aloilor/lean-coding-agent/commit/a3d9a15629071df1df447d803a5235979824266f) Thanks [@aloilor](https://github.com/aloilor)! - Replace `init-conventions` with `define-conventions`, rebuilt from scratch as a grill on the rules a repo cannot show. The old skill name is gone, with no alias. Convention output changes too: `WORKFLOWS.md` is replaced by `CHANGE-PROCESS.md` and `DEPLOYMENT.md`, with setup traps moving to `TESTING.md` and generated files to `CODING-STANDARDS.md`. The general commands section and fixed templates are gone. The baseline `AGENTS.md` now says when to load the new files. Rerun the skill to migrate an existing `WORKFLOWS.md`; it grills migrated content before keeping it.

## 1.1.0

### Minor Changes

- [`392e2d8`](https://github.com/aloilor/lean-coding-agent/commit/392e2d87afe8ce6742cad5f1101d751a6529ec73) Thanks [@aloilor](https://github.com/aloilor)! - Add an `explorer` subagent, and have `lean-grill-with-docs` use it for fact lookups when available.

## 1.0.0

### Major Changes

- [`65913b7`](https://github.com/aloilor/lean-coding-agent/commit/65913b78f465c087aec36d135ab9ab8b06a4a5bf) Thanks [@aloilor](https://github.com/aloilor)! - Replace the feature-specification workflow with a general planning-only workflow.

- [`c5aa456`](https://github.com/aloilor/lean-coding-agent/commit/c5aa4564f8dbc306ff3a899cb60ecab217571c1a) Thanks [@aloilor](https://github.com/aloilor)! - Remove Codex plugin packaging; install selected skills from this repository with the Skills CLI.

### Minor Changes

- [`5c795da`](https://github.com/aloilor/lean-coding-agent/commit/5c795da8a0a98af8759cd1449f5c182a04db74ab) Thanks [@aloilor](https://github.com/aloilor)! - Add an implementation-report template and tighten the plan and code-review templates: open-question approval gate, declared new dependencies, revision log, verdict-first reviews, and finding IDs tracked across review passes.

- [`3b31261`](https://github.com/aloilor/lean-coding-agent/commit/3b312617305eb88f400de46aee4d695e42ba323b) Thanks [@aloilor](https://github.com/aloilor)! - Change Claude Code subagent defaults: `planner` and `code-reviewer` now use `opus` with `low` effort, and `bug-diagnostician` and `implementer` use `haiku` with `xhigh` effort. Remove the stale SQL guidance mention from the `code-reviewer` description.

- [`d555503`](https://github.com/aloilor/lean-coding-agent/commit/d55550391082d72ae082476a63fe171ff7ca8ad4) Thanks [@aloilor](https://github.com/aloilor)! - Set up Codex, Claude Code, or both: install Claude Code subagents with selectable models and install upstream skills for the selected coding agents.

- [`7f77c11`](https://github.com/aloilor/lean-coding-agent/commit/7f77c113e65b854520b4d89e224baf82549a0f65) Thanks [@aloilor](https://github.com/aloilor)! - Let the Skills CLI own baseline skill installation, updates, and removal. Setup preserves the selected skills instead of copying sibling folders or pruning retired skills and no longer bundles release metadata. Existing projects should rerun `npx skills add aloilor/lean-coding-agent` to register the desired skills with the CLI.

- [`bec2ede`](https://github.com/aloilor/lean-coding-agent/commit/bec2ede1bad90e1ffce0fe0ca81dc0d5a1444aca) Thanks [@aloilor](https://github.com/aloilor)! - Add the feature-specification skill for writing client-approvable feature specs from a fixed template.

- [`f256cb5`](https://github.com/aloilor/lean-coding-agent/commit/f256cb567be93c0018e732767d9f06b5052e6263) Thanks [@aloilor](https://github.com/aloilor)! - Rename `grill-with-docs` to `lean-grill-with-docs` to identify it as part of Lean Coding Agent. Update existing invocations to `$lean-grill-with-docs` and rename any project override from `.agents/skill-overrides/grill-with-docs.md` to `.agents/skill-overrides/lean-grill-with-docs.md`, updating its index entry and skill references. Remove the old installed skill folder after reinstalling.

  `lean-grill-with-docs` now keeps its documentation in `docs/conventions/`: `docs/conventions/GLOSSARY.md` (and `docs/conventions/GLOSSARY-MAP.md`) instead of the repo root, and ADRs in `docs/conventions/adr/` instead of `docs/adr/`; move existing files there. Add a `--docs-dir <folder>` option to setup. It writes a `lean-grill-with-docs` skill override so the project's `GLOSSARY.md`, `GLOSSARY-MAP.md`, and ADRs live in the chosen folder instead of `docs/conventions/`. Projects can also set the folder by writing that override by hand.

- [`715ce8b`](https://github.com/aloilor/lean-coding-agent/commit/715ce8b888bbe8f971b022074ed3cd0dbb2918a6) Thanks [@aloilor](https://github.com/aloilor)! - Add maintain-changelog to curate meaningful changes from Git history into a Keep a Changelog document, reconcile repeated updates, and apply Semantic Versioning.

- [`beba7f8`](https://github.com/aloilor/lean-coding-agent/commit/beba7f846909a50b5a5ddbf3eabef25695d9b1cf) Thanks [@aloilor](https://github.com/aloilor)! - Replace `codebase-onboarding` with `init-conventions`, which writes repo-specific, verified conventions to `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md` from repo evidence, commands it runs, and a user interview. Setup no longer seeds `agent-context/`. Projects installed with the Skills CLI need to add `init-conventions` again.

- [`bbaa2dd`](https://github.com/aloilor/lean-coding-agent/commit/bbaa2dddee7ffa5440db2194cd11535ef7e128f5) Thanks [@aloilor](https://github.com/aloilor)! - Install Anthropic's skill-creator in projects initialized by setup.

### Patch Changes

- [`2753316`](https://github.com/aloilor/lean-coding-agent/commit/27533162baed9d4dba6d82b1ad3756b61722093f) Thanks [@aloilor](https://github.com/aloilor)! - Fix invalid frontmatter so the Skills CLI discovers the `init-conventions` skill.

- [`03be5c8`](https://github.com/aloilor/lean-coding-agent/commit/03be5c89465ba35f1c4cbc9ef4ee8dc56e47c13d) Thanks [@aloilor](https://github.com/aloilor)! - Stop appending a baseline edit prohibition to initialized `AGENTS.md` and `CLAUDE.md` files. Setup now copies the bundled baseline snapshots verbatim on every run.

- [`07b7498`](https://github.com/aloilor/lean-coding-agent/commit/07b7498ac602dbd42a06041571465698afc4ba00) Thanks [@aloilor](https://github.com/aloilor)! - Remove the custom release and skill update checker in favor of `npx skills check`.

## 0.3.0

### Minor Changes

- [`814d83b`](https://github.com/aloilor/lean-coding-agent/commit/814d83b2f1506f95bb8c7683d27aff3e1688755b) Thanks [@aloilor](https://github.com/aloilor)! - Install a session-start release check with the plugin.
