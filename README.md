# Lean Coding Agent

A managed Codex plugin and skill collection for working on real codebases. It gives Codex a shared project baseline, practical engineering guidance, and repeatable ways to set up and understand a repository. `AGENTS.md` is the active baseline; the initializer also copies `CLAUDE.md` for compatibility but does not configure Claude Code.

The skills are small and composable. Install the complete bundle as a plugin, or choose selected skills with the Skills CLI. The project setup skill installs the shared baseline and prepares the repository for day-to-day work.

## Installation (30-second setup)

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

The setup skill installs the shared project guidance, skills, skill overrides, and Codex subagents. It also installs Agent Browser and the upstream skills used by the baseline, then offers to run project-specific onboarding. Node.js is required for setup.

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

## Why these skills exist

### 1. Give the agent the context it needs

An agent joining a repository has to learn its architecture, terminology, testing practices, and local conventions. The shared [`AGENTS.md`](AGENTS.md) provides the baseline; [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) records evidence-backed project context under `agent-context/` so future work can start from it.

### 2. Align on changes before they grow

Misunderstood requirements are expensive to repair after implementation. [`grill-with-docs`](skills/grill-with-docs/SKILL.md) helps clarify a change against the project's domain language and decisions. The specification and feature workflows turn resolved requirements into an agreed plan before implementation.

All `workflow-*` skills are opt-in: Codex runs one only when you explicitly name or call it. When a planning workflow is invoked, it requires `grill-with-docs` before writing the plan or starting implementation.

### 3. Keep feedback and engineering standards close

[`engineering-standards`](skills/engineering-standards/SKILL.md) supplies shared guidance for code changes. [`rest-api-design`](skills/rest-api-design/SKILL.md) covers HTTP contracts, and the workflow skills connect implementation with verification and independent review. The setup skill also installs focused [upstream skills](#upstream-skills-installed-by-setup).

### 4. Keep project setup consistent

The setup skill installs the baseline into each repository and refreshes its managed files when run again after the installed plugin is upgraded.

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

Setup also installs these skills from upstream repositories. Each skill name links to its upstream definition.

| Skill | Source | Purpose |
| --- | --- | --- |
| [`find-skills`](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Find and evaluate skills from the agent skills ecosystem. |
| [`agent-browser`](https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md) | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Automate browser tasks such as navigating pages, filling forms, extracting data, and testing web apps. |
| [`handoff`](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Summarize a session so another agent can continue the work. |
| [`resolving-merge-conflicts`](https://github.com/mattpocock/skills/blob/main/skills/engineering/resolving-merge-conflicts/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Resolve merge and rebase conflicts while preserving the intent of each change. |
| [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Build features and fix bugs with a test-first red-green-refactor workflow. |
| [`changelog-automation`](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/changelog-automation/SKILL.md) | [wshobson/agents](https://github.com/wshobson/agents) | Generate changelog entries from Conventional Commits. |
| [`create-readme`](https://github.com/github/awesome-copilot/blob/main/skills/create-readme/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Create a README based on the project and its documentation. |
| [`create-specification`](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Create a specification written for generative AI consumption. |
| [`prd`](https://github.com/github/awesome-copilot/blob/main/skills/prd/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Generate product requirements documents for software and AI features. |
| [`refactor`](https://github.com/github/awesome-copilot/blob/main/skills/refactor/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Improve code structure and maintainability without changing behavior. |
| [`sql-code-review`](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Review SQL for security, maintainability, and quality across database systems. |
| [`sql-optimization`](https://github.com/github/awesome-copilot/blob/main/skills/sql-optimization/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Tune SQL queries and indexes and analyze database performance. |

The setup also applies local overrides to [`create-specification`](skills/skill-overrides/create-specification.md), [`prd`](skills/skill-overrides/prd.md), and [`tdd`](skills/skill-overrides/tdd.md).

## Working on this repository

The root [`package.json`](package.json) is the release version source, and root [`plugin.json`](plugin.json) is synchronized from it. The root `plugin.json` and [`skills/`](skills/) are canonical plugin content. The build script generates [`plugins/lean-coding-agent/`](plugins/lean-coding-agent/); do not edit generated files directly.

All utilities in `scripts/` run on Node.js built-in modules and need no package installation.

To compare this checkout's `plugin.json` version with the latest stable GitHub Release, run:

```sh
node scripts/check_skill_updates.mjs
```

When shipping skill changes, bump the version in `package.json`, then run `npm run version` to sync `plugin.json`. Run `npm run check-plugin-version` to verify the manifests match, rebuild the plugin with `node scripts/build_codex_plugin.mjs`, then publish a matching `vMAJOR.MINOR.PATCH` release tag. This checks the source checkout; it does not inspect a separate project's installed plugin version.

```sh
node scripts/build_codex_plugin.mjs
node scripts/build_codex_plugin.mjs --check
python -m unittest discover -s tests
```

Manual Codex UI smoke scenarios are documented in [`tests/smoke/README.md`](tests/smoke/README.md). To try the local build, add this checkout as a marketplace, rebuild the plugin, and upgrade the marketplace entry:

```sh
codex plugin marketplace add .
node scripts/build_codex_plugin.mjs
codex plugin marketplace upgrade lean-coding-agent
```

## License

Available under the [MIT License](LICENSE).
