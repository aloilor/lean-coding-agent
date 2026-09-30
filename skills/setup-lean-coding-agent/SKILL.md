---
name: setup-lean-coding-agent
description: Initialize the current project with the Lean Coding Agent baseline after installing its skills, including project guidance, available skills, skill overrides, configurable Codex subagents, and release and upstream skill update checks.
---

# Setup Lean Coding Agent

Run this skill after installing it with the Skills CLI to initialize the current project. The Node.js script copies the available skills and baseline assets into the project, records the installed release in `agent-context/skills-installed.json`, installs the Codex subagents with the models selected by the user, installs the release and skills update checker at `scripts/check-skill-updates.mjs`, installs the agent-browser development dependency, and adds the upstream skills.

## Workflow

1. Ask which existing project directory to initialize. Offer the current working directory as the recommended default, and let the user choose it or provide another path. Do not silently assume the current directory.
2. Before asking about models, check the current official [OpenAI model catalog](https://developers.openai.com/api/docs/models) and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). Show the latest generally available coding-capable model IDs and their supported reasoning-effort levels, with a short description of each model. Treat this list as a current reference; replace it with newer options if the official documentation has changed:
   - `gpt-6-astra` — most capable for complex reasoning and coding; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6.1-sol` — near-Astra performance for complex work at a lower cost; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-sol` — designed for complex coding and agentic workflows; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-luna` — efficient for focused, high-volume work; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

   Tell the user the current planner default is `gpt-6.1-sol` with `high` reasoning; `bug-diagnostician`, `implementer`, and `code-reviewer` default to `gpt-6-luna` with `xhigh` reasoning. Then ask: “Which model IDs should setup assign to `planner`, `bug-diagnostician`, `implementer`, and `code-reviewer`? Choose the defaults, or provide a model ID for each.” The user may choose the defaults or provide different model IDs for each agent. Preserve each agent's `model_reasoning_effort` setting.
3. Run the bundled Node.js setup script from the target project, passing the selected models:

   ```text
   node "<setup-skill>/scripts/setup-lean-coding-agent.mjs" "<target-project>" --planner-model <model-id> --bug-diagnostician-model <model-id> --implementer-model <model-id> --code-reviewer-model <model-id>
   ```

   Locate `<setup-skill>` from this skill's installed directory. Do not ask the user to find or run the script. It uses Node.js and npm's `npx` on Windows, macOS, and Linux. If setup fails, report the failed command and stop; rerun only after resolving the reported environment or network issue.
4. After setup completes, ask the user whether they want to run `$codebase-onboarding` to fill in project-specific `agent-context/` documentation. Run it only if they agree. If the skill is not available in the active thread, read `<target-project>/.agents/skills/codebase-onboarding/SKILL.md` and follow it directly after they agree.
5. Confirm the project contains the baseline files, `scripts/check-skill-updates.mjs`, `agent-context/skills-installed.json`, `.agents/skill-overrides/` and its index, `.agents/skills/`, `.codex/config.toml` with the bundled multi-agent defaults, `.codex/agents/` with all four model choices and their reasoning effort, and the upstream skills. Summarize the installed skills, selected models and reasoning effort, and whether onboarding was run or deferred.

## Managed Files And Effects

- The script defaults to the current directory if the target path is omitted. It requires an existing directory.
- If `.codex/config.toml` is missing, setup copies the bundled baseline config.
- `AGENTS.md`, `CLAUDE.md`, bundled Codex agents, bundled shared skill copies, baseline override files, and the managed upstream skills are refreshed on each run. Existing project context files, local-private files, and project-owned override index entries are preserved.
- The setup creates `AGENTS.local.md`, `CLAUDE.local.md`, `agent-context/` for release metadata and onboarding docs, `.agents/lessons/`, `.agents/skill-overrides/`, and required `.gitignore` entries when missing. Before onboarding, it seeds missing codebase-onboarding documents directly in `agent-context/`; existing files are preserved so onboarding can update them in place. Managed ignore entries include the local files, agent task/report directories, and `node_modules/`.
- It copies available sibling skill folders into `.agents/skills/`. Those copies are managed outputs; local edits to a copied baseline skill are replaced when setup runs again.
- It records the installed Lean Coding Agent release in `agent-context/skills-installed.json` and copies the version checker into `scripts/check-skill-updates.mjs`. On reruns, it removes old checker hooks while preserving unrelated hooks.
- `references/release.json` records the skills release version and repository. The checker compares that release with GitHub Releases and checks GitHub-backed upstream skills listed in `skills-lock.json`.
- The baseline `AGENTS.md` asks agents to run the checker at session start and recommends `npx skills update -p` when skill updates are available.
- The agent-browser setup installs a development dependency with the detected package manager and installs its browser runtime. Upstream skills are installed through `npx skills add` and require network access.
- The Node.js script is the single cross-platform entry point for both project setup and skill installation.

## Bundled References

The `references/` directory contains the baseline inputs needed when this skill runs outside the source repository:

- `references/agents/` contains the four native Codex subagent TOML templates.
- `references/config.toml` contains the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- `references/baseline/` contains `AGENTS.md` and `CLAUDE.md`.
- `references/docs/incidents/README.md` contains the incident report template.
- `references/skill-overrides/` contains the baseline override index and override files copied into `.agents/skill-overrides/`.
- Sibling skill directories provide the additional skills copied into initialized projects when they are installed alongside this setup skill.

These files are snapshots of canonical sources in this repository. Keep their matching copies synchronized when those sources change.
