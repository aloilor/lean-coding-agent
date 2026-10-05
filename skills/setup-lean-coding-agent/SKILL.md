---
name: setup-lean-coding-agent
description: Initialize the current project with the Lean Coding Agent baseline for Codex, Claude Code, or both after installing its skills, including project guidance, available skills, skill overrides, configurable subagents, and release and upstream skill update checks.
---

# Setup Lean Coding Agent

Run this skill after installing it with the Skills CLI to initialize the current project for Codex, Claude Code, or both. The Node.js script copies the available skills and baseline assets into the project, records the installed release in `agent-context/skills-installed.json`, installs the subagents for each selected coding agent with the models chosen by the user, installs the release and skills update checker at `scripts/check-skill-updates.mjs`, installs the agent-browser development dependency, and adds the upstream skills for the selected coding agents.

## Workflow

1. Ask which existing project directory to initialize. Offer the current working directory as the recommended default, and let the user choose it or provide another path. Do not silently assume the current directory.
2. Ask which coding agents to set up: `codex`, `claude-code`, or `both`. Recommend the agent running this skill when the user has no preference. Do not silently assume a selection.
3. For each selected coding agent, show its current models before asking about them. Treat these lists as current references; replace them with newer options if the official documentation has changed.

   **Codex.** Check the official [OpenAI model catalog](https://developers.openai.com/api/docs/models) and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). Show the latest generally available coding-capable model IDs and their supported reasoning-effort levels, with a short description of each model:
   - `gpt-6-astra` — most capable for complex reasoning and coding; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6.1-sol` — near-Astra performance for complex work at a lower cost; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-sol` — designed for complex coding and agentic workflows; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-luna` — efficient for focused, high-volume work; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

   Codex subagents default to `gpt-6-luna`.

   **Claude Code.** Check the official [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [subagent documentation](https://code.claude.com/docs/en/sub-agents). Subagents accept an alias (`fable`, `opus`, `sonnet`, `haiku`), a full model ID, or `inherit` to use the main conversation's model:
   - `fable` (`claude-fable-5-1`) — for demanding reasoning and long-horizon agentic work; slowest and most expensive.
   - `opus` (`claude-opus-5-5`) — for long-running agentic coding and knowledge work.
   - `sonnet` (`claude-sonnet-5-5`) — the best combination of speed and intelligence.
   - `haiku` (`claude-haiku-4-5`) — fastest; does not support the `effort` setting, so the agent's effort level is ignored.

   Claude Code subagents default to `sonnet`.

   In both tools, `planner` and `code-reviewer` use `max` reasoning effort and `bug-diagnostician` and `implementer` use `xhigh`. Then ask: “Which models should setup assign to `planner`, `bug-diagnostician`, `implementer`, and `code-reviewer` for each selected coding agent? Choose the defaults, or provide a model for each.” Preserve each agent's reasoning-effort setting.
4. Run the bundled Node.js setup script from the target project, passing the selected coding agents and only the model options that apply to them:

   ```text
   node "<setup-skill>/scripts/setup-lean-coding-agent.mjs" "<target-project>" --tools <codex|claude-code|both> \
     --planner-model <codex-model> --bug-diagnostician-model <codex-model> --implementer-model <codex-model> --code-reviewer-model <codex-model> \
     --claude-planner-model <claude-model> --claude-bug-diagnostician-model <claude-model> --claude-implementer-model <claude-model> --claude-code-reviewer-model <claude-model>
   ```

   Locate `<setup-skill>` from this skill's installed directory. Do not ask the user to find or run the script. It uses Node.js and npm's `npx` on Windows, macOS, and Linux. If setup fails, report the failed command and stop; rerun only after resolving the reported environment or network issue.
5. After setup completes, ask the user whether they want to run the `codebase-onboarding` skill to fill in project-specific `agent-context/` documentation. Run it only if they agree. If the skill is not available in the active session, read `<target-project>/.agents/skills/codebase-onboarding/SKILL.md` and follow it directly after they agree.
6. Confirm the project contains the baseline files, `scripts/check-skill-updates.mjs`, `agent-context/skills-installed.json`, `.agents/skill-overrides/` and its index, `.agents/templates/plan.md`, `.agents/templates/code-review.md`, `.agents/skills/`, and the upstream skills. For Codex, also confirm `.codex/config.toml` with the bundled multi-agent defaults and `.codex/agents/` with all four agents. For Claude Code, confirm `.claude/agents/` with all four agents. Summarize the selected coding agents, installed skills, selected models and reasoning effort, and whether onboarding was run or deferred.

## Managed Files And Effects

- The script defaults to the current directory if the target path is omitted. It requires an existing directory. `--tools` defaults to `codex`.
- If Codex is selected and `.codex/config.toml` is missing, setup copies the bundled baseline config. Setup does not create `.codex/` files when only Claude Code is selected.
- `AGENTS.md`, `CLAUDE.md`, the bundled subagents for each selected coding agent, bundled shared skill copies, baseline override files, and the managed upstream skills are refreshed on each run. Other agents in `.codex/agents/` or `.claude/agents/`, existing project context files, local-private files, and project-owned override index entries are preserved.
- The setup creates `AGENTS.local.md`, `CLAUDE.local.md`, `agent-context/` for release metadata and onboarding docs, `.agents/lessons/`, `.agents/skill-overrides/`, and required `.gitignore` entries when missing. Before onboarding, it seeds missing codebase-onboarding documents directly in `agent-context/`; existing files are preserved so onboarding can update them in place. Managed ignore entries include the local files, agent task/report directories, and `node_modules/`.
- It copies available sibling skill folders into `.agents/skills/`. Those copies are managed outputs; local edits to a copied baseline skill are replaced when setup runs again.
- It copies the shared plan and code-review templates into `.agents/templates/` for every selected coding agent. The planner and code reviewer read these templates when writing their artifacts. Setup refreshes `plan.md` and `code-review.md` on every run while preserving other project-owned templates.
- It records the installed Lean Coding Agent release in `agent-context/skills-installed.json` and copies the version checker into `scripts/check-skill-updates.mjs`. On reruns, it removes old checker hooks while preserving unrelated hooks.
- `references/release.json` records the skills release version and repository. The checker compares that release with GitHub Releases and checks GitHub-backed upstream skills listed in `skills-lock.json`.
- The baseline `AGENTS.md` asks agents to run the checker at session start and recommends `npx skills update -p` when skill updates are available.
- The agent-browser setup installs a development dependency with the detected package manager and installs its browser runtime. Upstream skills are installed through `npx skills add` for the selected coding agents and require network access.
- The Node.js script is the single cross-platform entry point for both project setup and skill installation.

## Bundled References

The `references/` directory contains the baseline inputs needed when this skill runs outside the source repository:

- `references/agents/codex/` contains the four native Codex subagent TOML templates, and `references/agents/claude-code/` contains the matching Claude Code subagent Markdown templates. Keep their instructions synchronized; the Claude Code copies name skills in neutral wording instead of Codex `$skill` mentions.
- [`references/templates/plan.md`](references/templates/plan.md) and [`references/templates/code-review.md`](references/templates/code-review.md) are the canonical shared artifact templates copied into `.agents/templates/`. Their core sections stay fixed while detail scales to the work; workflow and agent instructions retain ownership of approval gates and review rules.
- `references/config.toml` contains the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- `references/baseline/` contains `AGENTS.md` and `CLAUDE.md`.
- `references/docs/incidents/README.md` contains the incident report template.
- `references/skill-overrides/` contains the baseline override index and override files copied into `.agents/skill-overrides/`.
- Sibling skill directories provide the additional skills copied into initialized projects when they are installed alongside this setup skill.

These files are snapshots of canonical sources in this repository. Keep their matching copies synchronized when those sources change.
