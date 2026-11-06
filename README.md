# Lean Coding Agent

**Engineering discipline for your coding agent, without the bloat.**

Small, composable skills for Codex and Claude Code, built for real codebases. Install the skills, run `setup-lean-coding-agent` once in your project, and your agent is ready for day-to-day work.

## Why Lean Coding Agent?

Lean Coding Agent gives your coding agent a rigorous plan, act, review loop when a change deserves it, and a direct answer when it doesn't. Many frameworks are full of bloat: long instructions on every task, mandatory process for small requests, and extra tooling to learn. This one keeps the loop and drops the rest.

- **Opt-in process.** Ordinary requests are handled directly. A workflow starts only when you name it, and both Codex and Claude Code are configured to stop the agent from starting one itself.
- **Slim workflows.** Each one is a short list of steps that only orchestrates. Detailed instructions stay in dedicated subagents, leaving the main session's context for your work.
- **A bounded review loop.** Feature, bug-fix, and refactor workflows repeat implementation and independent review until the change is approved. After three failed fixes for the same problem, or if success would mean weakening a test or expanding scope, the agent stops and reports back.
- **Workflows that fit the work.** Bug repairs need an approved diagnosis, refactors stop if behavior would change, and reviews don't edit code.
- **Task memory in files.** Plans, implementation reports, reviews, and incident reports outlast auto-compaction and the session. Incident reports in `docs/incidents/` can be committed; the rest are git-ignored by default.
- **Small, verified project context.** [`AGENTS.md`](AGENTS.md) holds only the essential rules. Conventions live in modular files under `docs/conventions/`, loaded on demand, and [`init-conventions`](skills/init-conventions/SKILL.md) runs commands before recording them. [See why](docs/init-conventions-rationale.md).
- **Skills that adapt without forking.** [Skill overrides](#skill-overrides) add project guidance from a separate file, so the installed skill stays unchanged and can keep updating from upstream.
## Installation

Install skills from this repository:

```sh
npx skills@latest add aloilor/lean-coding-agent
```

In the installer, select Codex, Claude Code, or both, and the skills you want. Select `setup-lean-coding-agent` to initialize a project with the shared baseline.

## Set up your project

Open the target repository in Codex and run `$setup-lean-coding-agent`, or in Claude Code run `/setup-lean-coding-agent`.

The setup skill asks whether to set up Codex, Claude Code, or both, and which model each subagent should use. It installs the shared project guidance, available skills, skill overrides, subagents for each selected coding agent (`.codex/agents/` and `.claude/agents/`). It also installs Agent Browser and the upstream skills used by the baseline for the selected coding agents, then offers to capture project conventions. Node.js is required for setup. `AGENTS.md` is the active baseline, and `CLAUDE.md` points Claude Code to it.

For Codex, setup creates `.codex/config.toml` when it is missing, with multi-agent defaults and a status line showing the model and reasoning level, project name, Git branch, context window size, and used tokens. Existing config files are preserved.

## Use the skills

Ask your coding agent for help as usual, or call a skill by name when you want it. For example, use `init-conventions` to record a repository's verified conventions or `workflow-feature-development` to explicitly start that workflow (`$skill-name` in Codex, `/skill-name` in Claude Code).

## Updates

Update project-installed skills from the project directory with:

```sh
npx skills update -p
```

The CLI updates skills already installed from their tracked sources. To add skills introduced since your last selection, rerun `npx skills@latest add aloilor/lean-coding-agent` and select them. See the [Skills CLI update documentation](https://github.com/vercel-labs/skills#skills-update) for scope options.

Run `npx skills check` to check for available skill updates.

## Skill reference

### Setup and project context

- [`setup-lean-coding-agent`](skills/setup-lean-coding-agent/SKILL.md) — install the baseline into the current project after installing the skill.
- [`init-conventions`](skills/init-conventions/SKILL.md) — initialize or refresh `docs/conventions/` with repo-specific, verified commands, examples to follow, boundaries, and traps.
- [`lean-grill-with-docs`](skills/lean-grill-with-docs/SKILL.md) — a personal fork of Matt Pocock’s original skill, adapted to work with my setup; clarifies plans against project terminology and documented decisions.
- [`feature-specification`](skills/feature-specification/SKILL.md) — write a client-approvable feature spec from a fixed template.

### Change workflows

Workflows are user-invoked only. Name the specific workflow skill in your request to start one; the assistant must not select or start one based on the task type or inferred usefulness. Ordinary requests are handled directly. The Claude Code skills set `disable-model-invocation: true`, and Codex skills set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

| Workflow | Use it for | Process and output |
| --- | --- | --- |
| [`workflow-planning`](skills/workflow-planning/SKILL.md) | Planning requested work without implementing it. | Resolve scope, decisions, acceptance criteria, and verification expectations, then obtain approval of the plan in `.agents/plans/`. |
| [`workflow-feature-development`](skills/workflow-feature-development/SKILL.md) | Changing externally observable behavior. | Clarify the change, obtain approval of the plan, implement test-first, then run an independent review and verification. Produces a plan, implementation report, and review pass. |
| [`workflow-bug-fixing`](skills/workflow-bug-fixing/SKILL.md) | Investigating and repairing a bug or regression. | Record the symptom and diagnosis, approve the repair plan, reproduce and fix test-first, then review and verify. Produces a plan, incident report in `docs/incidents/`, implementation report, and review pass. |
| [`workflow-refactor`](skills/workflow-refactor/SKILL.md) | Restructuring code while preserving behavior. | Establish a baseline, obtain approval of the plan, make small behavior-preserving changes, then review and verify. Produces a plan, implementation report, and review pass. |
| [`workflow-review`](skills/workflow-review/SKILL.md) | Reviewing code or assessing risk. | An independent review records findings in a review pass; it does not make fixes unless you ask for them. |

Planning workflows save user-approved plans under `.agents/plans/`. Implementation reports and review passes are saved under `.agents/implementation-reports/` and `.agents/code-reviews/` respectively. Bug-fixing workflows also keep a durable incident report under `docs/incidents/`.

Setup installs shared [plan](skills/setup-lean-coding-agent/references/templates/plan.md), [implementation-report](skills/setup-lean-coding-agent/references/templates/implementation-report.md), and [code-review](skills/setup-lean-coding-agent/references/templates/code-review.md) templates into `.agents/templates/`. Both Codex and Claude Code planners, implementers, and reviewers use them, with stable core sections and detail proportional to the task. Setup refreshes the three bundled templates on reruns while preserving other project-owned templates.

### Engineering and Git

- [`git-conventional-commit`](skills/git-conventional-commit/SKILL.md) — create Conventional Commits when asked to commit, and push when asked.
- [`maintain-changelog`](skills/maintain-changelog/SKILL.md) — inspect Git history in any commit format and curate released or unreleased changes using Keep a Changelog and Semantic Versioning.

### Upstream skills installed by setup

Setup also installs these skills from upstream repositories. Use this list to choose a skill for a task; each skill name links to its upstream definition.

| Skill | Source | Use when |
| --- | --- | --- |
| [`agent-browser`](https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md) | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Navigate and interact with websites, fill forms, extract page data, or test web apps through a browser. |
| [`eli5`](https://www.skills.sh/anthropics/claude-plugins-community/eli5) | [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community) | Explain a topic in beginner-friendly terms using a visual HTML artifact. |
| [`handoff`](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Pass ongoing work to another agent or session with a concise summary, next steps, and links to existing artifacts. |
| [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) | [mattpocock/skills](https://github.com/mattpocock/skills) | Build a feature or fix a bug test-first, one behavior slice at a time, using red-green-refactor. |
| [`refactor`](https://github.com/github/awesome-copilot/blob/main/skills/refactor/SKILL.md) | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Improve code structure or readability while preserving externally visible behavior. |
| [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | [anthropics/skills](https://github.com/anthropics/skills) | Create, improve, and evaluate agent skills with structured test cases and benchmarks. |

### Skill overrides

Overrides add project guidance to an installed skill without changing the skill itself. The setup copies bundled overrides into `.agents/skill-overrides/` and maintains an `INDEX.md` there that maps skill names to their override files. Before using a skill, Codex checks this index and reads the matching `<skill-name>.md` file when one is listed. The override extends the skill's instructions; if they conflict, the override takes precedence.

For example, the bundled [`tdd` override](skills/setup-lean-coding-agent/references/skill-overrides/tdd.md) applies the baseline's testing guidance whenever tests are planned, written, or reviewed. To add project-specific guidance for another skill, create a matching Markdown file in `.agents/skill-overrides/` and add a link for it to `INDEX.md`. Setup refreshes bundled override files while preserving project-owned entries in the index.

To keep `lean-grill-with-docs` documentation somewhere other than the default `docs/conventions/GLOSSARY.md` and `docs/conventions/adr/`, choose a folder during setup (`--docs-dir docs/domain`). Setup generates a `lean-grill-with-docs` override that stores `GLOSSARY.md` and `adr/` in that folder. You can also write that override yourself in `.agents/skill-overrides/lean-grill-with-docs.md`.

## Workflow guide

Workflow skills define a consistent process for planning, implementation, bug repair, refactoring, and review. In this repository, only the user can start one by explicitly requesting its skill, such as `$workflow-feature-development`. The assistant must not choose or start a workflow on the user's behalf, even when a request matches its scope.

See the [workflow guides](docs/workflows/README.md) for process diagrams and detailed overviews of [planning](docs/workflows/planning.md), [feature development](docs/workflows/feature-development.md), [bug fixing](docs/workflows/bug-fixing.md), [refactoring](docs/workflows/refactor.md), and [code review](docs/workflows/review.md). The linked skills remain the canonical instructions.

The planning, feature-development, bug-fixing, and refactoring workflows delegate plan creation to the `planner` subagent ([Codex](skills/setup-lean-coding-agent/references/agents/codex/planner.toml), [Claude Code](skills/setup-lean-coding-agent/references/agents/claude-code/planner.md)). The main agent obtains explicit user approval of the completed plan before implementation or repair. The review workflow does not use a planner.

Setup installs `planner`, `bug-diagnostician`, `implementer`, and `code-reviewer`. Codex subagents default to `gpt-6-luna`; Claude Code subagents default to `sonnet`. In both tools, the planner and code reviewer use `max` reasoning effort, and the bug diagnostician and implementer use `xhigh`. Setup accepts a separate model choice for each agent and tool, such as `--planner-model` for Codex and `--claude-planner-model` for Claude Code. Run `node --test` to check setup initialization, agent installation, reruns, and failure handling in [`tests/`](tests/).

### Planning only

Use [`workflow-planning`](skills/workflow-planning/SKILL.md) when you want the work explored and documented as an approved plan without starting implementation. It can cover feature, bug-fix, refactoring, or other scoped work; the planner resolves open decisions, defines acceptance criteria and verification expectations, and records the plan for a later task.

### Feature development

Use [`workflow-feature-development`](skills/workflow-feature-development/SKILL.md) to change externally observable behavior. After the user approves the planner's plan, the implementer works test-first and records implementation and verification evidence. An independent reviewer checks the change against the plan. If review blocks the change, address its findings and repeat the relevant checks and review. Finish with focused verification, broader checks when needed, and a final diff review.

### Bug fixing

Use [`workflow-bug-fixing`](skills/workflow-bug-fixing/SKILL.md) for bugs, regressions, failing tests, or runtime and CI failures. The planner and `bug-diagnostician` prepare the repair plan and incident report. Obtain explicit approval of the repair plan before changing production or test code, then reproduce the problem and repair it test-first, followed by an independent review and broader verification where needed. The reviewer finalizes the incident report. If the repair expands into feature behavior or contract work, stop and ask for direction.

### Refactoring

Use [`workflow-refactor`](skills/workflow-refactor/SKILL.md) to restructure code while preserving its behavior and contracts. The planner records behavior to preserve, scope, risks, and verification; after user approval, the implementer establishes the test baseline and makes small changes while keeping focused checks green. An independent reviewer checks for behavior drift, scope creep, and missing documentation or tests. If the work reveals a behavior change, stop and ask for direction.

### Code review

Use [`workflow-review`](skills/workflow-review/SKILL.md) for a review, audit, or risk assessment. The reviewer records findings in severity order in a review pass under `.agents/code-reviews/`. This workflow does not draft a plan, run the documentation grill, or make changes. Ask separately for fixes if you want findings addressed.

### Workflow records

Plans use `.agents/plans/plan_YYYYMMDD_<name>.md`. Implementations use `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`, and each review pass uses `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`. Bug-fixing workflows also keep an incident report at `docs/incidents/incident_YYYYMMDD_<name>.md`. These records make the agreed scope, decisions, and verification evidence available for review and follow-up.

## Working on this repository

The [`skills/`](skills/) directory contains the source skills. The setup skill's `references/` directory contains baseline snapshots it needs when installed on its own; update those copies when their source files change.

Edit skill overrides in [`skills/skill-overrides/`](skills/skill-overrides/) only. Enable the repository hooks once with `git config core.hooksPath .githooks`; the pre-commit hook then mirrors staged override changes into the setup skill's `references/skill-overrides/` and stages the copies. Run `npm run sync-skill-overrides` to sync manually, or `npm run check-skill-overrides` to check for drift.

The root [`package.json`](package.json) is the release version source; the setup skill's [`release.json`](skills/setup-lean-coding-agent/references/release.json) is synchronized from it so initialized projects can check for newer skill releases. This repository uses Changesets to version the skills collection and prepare GitHub releases. Install the development dependencies with `npm ci`, then add a changeset for each user-facing change:

```sh
npm run changeset
```

The release workflow opens a version pull request after changesets reach `main`. Merging that pull request updates `package.json` and `CHANGELOG.md`, synchronizes `release.json`, then creates a GitHub tag and release for the skills collection. Run `npm run check-release-version` to check that the release metadata is synchronized.

Run the Node.js test suite with:

```sh
node --test
```

## License

Available under the [MIT License](LICENSE).
