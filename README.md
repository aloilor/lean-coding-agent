# Lean Coding Agent

A managed Codex plugin and skill collection for working on real codebases. It gives Codex a shared project baseline, practical engineering guidance, and repeatable ways to set up and understand a repository. `AGENTS.md` is the active baseline; the initializer also copies `CLAUDE.md` for compatibility but does not configure Claude Code.

The skills are small and composable. Install the complete bundle as a plugin, or choose selected skills with the Skills CLI. The project setup skill installs the shared baseline and prepares the repository for day-to-day work.

## Installation

### 1. Install the skills

For the complete, managed Codex bundle, add the marketplace:

```sh
codex plugin marketplace add aloilor/lean-coding-agent
```

Then open Codex's Plugins directory, select the Lean Coding Agent marketplace, and install **Lean Coding Agent** (`lean-coding-agent`).

To choose individual skills instead, run:

```sh
npx skills@latest add aloilor/lean-coding-agent
```

In the installer, select `setup-lean-coding-agent` and Codex. Add any other skills you want available.

### 2. Set up your project

Open the target repository in Codex and run:

```text
$setup-lean-coding-agent
```

The setup skill installs the shared project guidance, skills, skill overrides, Codex subagents, and a project-local session-start version check. It also installs Agent Browser and the upstream skills used by the baseline, then offers to run project-specific onboarding. Node.js is required for setup.

### 3. Use the skills

Ask Codex for help as usual, or call a skill by name when you want it. For example, use `$codebase-onboarding` to understand an unfamiliar repository or `$workflow-feature-development` to explicitly start that workflow.

## Updates

The plugin ships as a versioned bundle. To refresh its marketplace source when a release is available, run:

```sh
codex plugin marketplace upgrade lean-coding-agent
```

For skills installed through the Skills CLI, update project-installed skills from the project directory with:

```sh
npx skills update -p
```

The CLI updates skills already installed from their tracked sources. To add skills introduced since your last selection, rerun `npx skills@latest add aloilor/lean-coding-agent` and select them. See the [Skills CLI update documentation](https://github.com/vercel-labs/skills#skills-update) for scope options.

Make changes in this repository; do not edit the installed plugin cache.

## Skill reference

### Setup and project context

- [`setup-lean-coding-agent`](skills/setup-lean-coding-agent/SKILL.md) — install the baseline into the current project after installing the plugin.
- [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) — analyze a repository and write structured project context.
- [`grill-with-docs`](skills/grill-with-docs/SKILL.md) — clarify a plan against project terminology and documented decisions.

### Change workflows

These skills are invoked explicitly and guide a task from its requirements or diagnosis through implementation and review.

- [`workflow-feature-specification`](skills/workflow-feature-specification/SKILL.md) — resolve requirements and produce an approved specification plan.
- [`workflow-feature-development`](skills/workflow-feature-development/SKILL.md) — plan and implement a behavior change.
- [`workflow-bug-fixing`](skills/workflow-bug-fixing/SKILL.md) — investigate and repair a bug with a durable incident report.
- [`workflow-refactor`](skills/workflow-refactor/SKILL.md) — restructure code while preserving behavior.
- [`workflow-review`](skills/workflow-review/SKILL.md) — perform a review or risk assessment and record its findings.

Planning workflows keep an approved plan under `.agents/plans/`. Feature, refactor, and bug-fixing workflows also produce implementation reports and review passes; bug fixes include a durable report under `docs/incidents/`. Specification workflows produce the plan, and the review workflow produces a review pass.

### Engineering and Git

- [`engineering-standards`](skills/engineering-standards/SKILL.md) — shared quality guidance for code changes.
- [`rest-api-design`](skills/rest-api-design/SKILL.md) — design and review REST API contracts.
- [`git-conventional-commit`](skills/git-conventional-commit/SKILL.md) — create Conventional Commits when asked to commit.
- [`git-commit-and-push`](skills/git-commit-and-push/SKILL.md) — commit and push when explicitly requested.

### Upstream skills installed by setup

Setup also installs these skills from upstream repositories. Use this list to choose a skill for a task; each skill name links to its upstream definition.

| Skill | Source | Use when |
| --- | --- | --- |
| [`agent-browser`](https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md) | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Navigate and interact with websites, fill forms, extract page data, or test web apps through a browser. |
| [`handoff`](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Pass ongoing work to another agent or session with a concise summary, next steps, and links to existing artifacts. |
| [`resolving-merge-conflicts`](https://github.com/mattpocock/skills/blob/main/skills/engineering/resolving-merge-conflicts/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Resolve active Git merge or rebase conflicts by tracing each change to its intent and completing the merge checks. |
| [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Build a feature or fix a bug test-first, one behavior slice at a time, using red-green-refactor. |
| [`changelog-automation`](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/changelog-automation/SKILL.md) | [wshobson/agents](https://github.com/wshobson/agents) | Create or automate changelogs and release notes from commits, using commit conventions and versioning. |
| [`create-readme`](https://github.com/github/awesome-copilot/blob/main/skills/create-readme/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Draft a project README after reviewing the codebase and its existing documentation. |
| [`refactor`](https://github.com/github/awesome-copilot/blob/main/skills/refactor/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Improve code structure or readability while preserving externally visible behavior. |
| [`sql-code-review`](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Review SQL for injection risks, access control, correctness, maintainability, and database best practices. |
| [`sql-optimization`](https://github.com/github/awesome-copilot/blob/main/skills/sql-optimization/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Analyze query performance and improve SQL queries, indexes, and execution plans. |

The setup also applies a local override to [`tdd`](skills/setup-lean-coding-agent/references/skill-overrides/tdd.md).

## Working on this repository

The root [`package.json`](package.json) is the plugin release version source, and root [`plugin.json`](plugin.json) is synchronized from it. The setup skill's [`release.json`](skills/setup-lean-coding-agent/references/release.json) is synchronized at the same time and supplies the version recorded for project-installed skill copies. The root `plugin.json` and [`skills/`](skills/) are canonical plugin content. The build script generates [`plugins/lean-coding-agent/`](plugins/lean-coding-agent/); do not edit generated files directly.

All utilities in `scripts/` run on Node.js built-in modules and need no package installation.

To compare this checkout's `plugin.json` version with the latest stable GitHub Release, run:

```sh
node scripts/check_skill_updates.mjs
```

When shipping skill changes, bump the version in `package.json`, then run `npm run version` to sync `plugin.json`. Run `npm run check-plugin-version` to verify the manifests match, rebuild the plugin with `node scripts/build_codex_plugin.mjs`, then publish a matching `vMAJOR.MINOR.PATCH` release tag. This checks the source checkout; it does not inspect a separate project's installed plugin version.

```sh
node scripts/build_codex_plugin.mjs
node scripts/build_codex_plugin.mjs --check
```

To try the local build, add this checkout as a marketplace, rebuild the plugin, and upgrade the marketplace entry:

```sh
codex plugin marketplace add .
node scripts/build_codex_plugin.mjs
codex plugin marketplace upgrade lean-coding-agent
```

## License

Available under the [MIT License](LICENSE).
