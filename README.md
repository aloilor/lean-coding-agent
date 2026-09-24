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

The setup skill installs the shared project guidance, skills, skill overrides, Codex subagents, and a cross-tool update checker that agents run at session start. It also installs Agent Browser and the upstream skills used by the baseline, then offers to run project-specific onboarding. Node.js is required for setup.

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

Run `node scripts/check-skill-updates.mjs` to compare this checkout with the latest stable release. Initialized projects also receive the checker at `scripts/check-skill-updates.mjs`; their `AGENTS.md` instructs agents to run it at session start and report the output. In an initialized project, pass `--project --manifest agent-context/skills-installed.json` to compare the installed skill copies and get setup-specific update guidance.

Make changes in this repository; do not edit the installed plugin cache.

## Skill reference

### Setup and project context

- [`setup-lean-coding-agent`](skills/setup-lean-coding-agent/SKILL.md) — install the baseline into the current project after installing the plugin.
- [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) — analyze a repository and write structured project context.
- [`grill-with-docs`](skills/grill-with-docs/SKILL.md) — clarify a plan against project terminology and documented decisions.

### Change workflows

Workflows are opt-in: name the matching skill in your request to start one. They provide a defined process and durable records for work that benefits from planning, diagnosis, or independent review.

| Workflow | Use it for | Process and output |
| --- | --- | --- |
| [`workflow-feature-specification`](skills/workflow-feature-specification/SKILL.md) | Clarifying requirements and contracts before implementation. | Resolve requirements and acceptance criteria, then obtain approval for a specification plan in `.agents/plans/`. |
| [`workflow-feature-development`](skills/workflow-feature-development/SKILL.md) | Changing externally observable behavior. | Clarify and plan the change, get approval, implement test-first, then run an independent review and verification. Produces a plan, implementation report, and review pass. |
| [`workflow-bug-fixing`](skills/workflow-bug-fixing/SKILL.md) | Investigating and repairing a bug or regression. | Record the symptom and diagnosis, get approval for the repair, reproduce and fix test-first, then review and verify. Produces a plan, incident report in `docs/incidents/`, implementation report, and review pass. |
| [`workflow-refactor`](skills/workflow-refactor/SKILL.md) | Restructuring code while preserving behavior. | Establish a baseline, get approval for a plan, make small behavior-preserving changes, then review and verify. Produces a plan, implementation report, and review pass. |
| [`workflow-review`](skills/workflow-review/SKILL.md) | Reviewing code or assessing risk. | An independent review records findings in a review pass; it does not make fixes unless you ask for them. |

Planning workflows save approved plans under `.agents/plans/`. Implementation reports and review passes are saved under `.agents/implementation-reports/` and `.agents/code-reviews/` respectively. Bug-fixing workflows also keep a durable incident report under `docs/incidents/`.

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

### Skill overrides

Overrides add project guidance to an installed skill without changing the skill itself. The setup copies bundled overrides into `.agents/skill-overrides/` and maintains an `INDEX.md` there that maps skill names to their override files. Before using a skill, Codex checks this index and reads the matching `<skill-name>.md` file when one is listed. The override extends the skill's instructions; if they conflict, the override takes precedence.

For example, the bundled [`tdd` override](skills/setup-lean-coding-agent/references/skill-overrides/tdd.md) applies the baseline's testing guidance whenever tests are planned, written, or reviewed. To add project-specific guidance for another skill, create a matching Markdown file in `.agents/skill-overrides/` and add a link for it to `INDEX.md`. Setup refreshes bundled override files while preserving project-owned entries in the index.

## Workflow guide

Workflow skills define a consistent process for specification, implementation, bug repair, refactoring, and review. In this repository, they are opt-in: ask Codex to run the relevant skill, such as `$workflow-feature-development`. A request to make a change does not start a workflow by itself.

The specification, feature-development, bug-fixing, and refactoring workflows begin with `$grill-with-docs`, which resolves the task against project terminology and documentation. They then produce an approved plan under `.agents/plans/`. Get approval for that plan before implementation or repair begins. The review workflow is review-only and does not use this planning gate.

### Feature specification

Use [`workflow-feature-specification`](skills/workflow-feature-specification/SKILL.md) when requirements, acceptance criteria, or contracts need to be settled before coding. After the documentation grill, consolidate the resolved requirements, boundaries, decisions, and verification expectations into a specification plan. Once approved, that plan is the handoff for a later implementation task; this workflow does not implement the feature.

### Feature development

Use [`workflow-feature-development`](skills/workflow-feature-development/SKILL.md) to change externally observable behavior. After the grill, inspect the relevant code and documentation and write a plan covering the behavior, scope, constraints, acceptance criteria, and verification. Wait for approval, then have the implementer work test-first and record the implementation and verification evidence. An independent reviewer checks the change against the plan. If the review blocks the change, address its concrete findings and repeat the relevant checks and review. Finish with focused verification, broader checks when the impact calls for them, and a final diff review.

### Bug fixing

Use [`workflow-bug-fixing`](skills/workflow-bug-fixing/SKILL.md) for bugs, regressions, failing tests, or runtime and CI failures. After the documentation grill, investigate the affected code, callers, tests, and project context. Record the symptom, evidence, likely cause, impact, and proposed repair in an incident report and plan. Get approval before changing production or test code. Then reproduce the problem and repair it test-first, followed by an independent review and relevant broader verification. The reviewer finalizes the incident report from the confirmed evidence. If the repair would expand into feature behavior or contract work, stop and ask for direction instead of switching workflows automatically.

### Refactoring

Use [`workflow-refactor`](skills/workflow-refactor/SKILL.md) to restructure code while preserving its behavior and contracts. After the grill and code inspection, document what must remain unchanged, the scope, risks, and verification in a plan. Get approval, establish the test baseline, and make small changes while keeping focused checks green. The implementer records the baseline and verification; an independent reviewer checks for behavior drift, scope creep, and missing documentation or tests. If the work reveals a behavior change, stop and ask for direction rather than continuing as a refactor.

### Code review

Use [`workflow-review`](skills/workflow-review/SKILL.md) for a review, audit, or risk assessment. The reviewer records findings in severity order in a review pass under `.agents/code-reviews/`. This workflow does not draft a plan, run the documentation grill, or make changes. Ask separately for fixes if you want findings addressed.

### Workflow records

Plans use `.agents/plans/plan_YYYYMMDD_<name>.md`. Implementations use `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`, and each review pass uses `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`. Bug-fixing workflows also keep an incident report at `docs/incidents/incident_YYYYMMDD_<name>.md`. These records make the agreed scope, decisions, and verification evidence available for review and follow-up.

## Working on this repository

The root [`package.json`](package.json) is the plugin release version source, and root [`plugin.json`](plugin.json) is synchronized from it. The setup skill's [`release.json`](skills/setup-lean-coding-agent/references/release.json) is synchronized at the same time and supplies the version recorded for project-installed skill copies. The root `plugin.json` and [`skills/`](skills/) are canonical plugin content. The build script generates [`plugins/lean-coding-agent/`](plugins/lean-coding-agent/); do not edit generated files directly.

Utilities in `scripts/` use Node.js built-ins. Changesets is a development dependency for release notes and versioning, installed by `npm ci` in the release workflow.

### Releases

Add a Changeset to each pull request that changes the released plugin or its skills:

```sh
npm run changeset
```

Choose the version bump and write a short release note when prompted. Changesets records that intent in a Markdown file under `.changeset/`. Changes that do not affect the released plugin, such as documentation-only maintenance, do not need a Changeset.

After a Changeset reaches `main`, the Release GitHub Action opens or updates a `chore: version skills` pull request. Its version step updates `package.json` and `CHANGELOG.md`, syncs `plugin.json` and the setup skill's `release.json`, and rebuilds the generated plugin directory. Merge that pull request to create the matching `vMAJOR.MINOR.PATCH` Git tag and GitHub Release. Project setup checks GitHub Releases to detect newer versions.

The repository must allow GitHub Actions to create pull requests. Enable **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** once for the repository.

To compare this checkout's `plugin.json` version with the latest stable GitHub Release, run:

```sh
node scripts/check-skill-updates.mjs
```

This checks the source checkout; it does not inspect a separate project's installed plugin version.

To rebuild or check the generated plugin locally, run:

```sh
node scripts/build-codex-plugin.mjs
node scripts/build-codex-plugin.mjs --check
```

To try the local build, add this checkout as a marketplace, rebuild the plugin, and upgrade the marketplace entry:

```sh
codex plugin marketplace add .
node scripts/build-codex-plugin.mjs
codex plugin marketplace upgrade lean-coding-agent
```

## License

Available under the [MIT License](LICENSE).
