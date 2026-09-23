---
name: setup-lean-coding-agent
description: Initialize the current project with the Lean Coding Agent baseline after installation, including project guidance, bundled skills, skill overrides, configurable Codex subagents, and a session-start version check.
---

# Setup Lean Coding Agent

Run this skill after installing Lean Coding Agent to initialize the current project. The bundled Node.js script copies the skills and baseline assets into the project, installs the Codex subagents with the models selected by the user, registers a session-start version check, installs the agent-browser development dependency, and adds the upstream skills.

## Workflow

1. Ask which existing project directory to initialize. Offer the current working directory as the recommended default, and let the user choose it or provide another path. Do not silently assume the current directory.
2. Before asking about models, check the current official [OpenAI model catalog](https://developers.openai.com/api/docs/models) and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). Show the latest generally available coding-capable model IDs and their supported reasoning-effort levels, with a short description of each model. Treat this list as a current reference; replace it with newer options if the official documentation has changed:
   - `gpt-6-astra` — most capable for complex reasoning and coding; supports `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-sol` — designed for complex coding and agentic workflows; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.
   - `gpt-6-luna` — efficient for focused, high-volume work; supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

   Tell the user the current defaults for all three subagents are `gpt-6-luna` with `xhigh` reasoning. Then ask: “Which model IDs should setup assign to `bug-diagnostician`, `implementer`, and `code-reviewer`? Choose the defaults for all three, or provide a model ID for each.” The user may choose the defaults or provide different model IDs for each agent. Preserve each agent's existing `model_reasoning_effort` setting.
3. Run the bundled Node.js setup script from the target project, passing the selected models:

   ```text
   node "<setup-skill>/scripts/setup_lean_coding_agent.mjs" "<target-project>" --bug-diagnostician-model <model-id> --implementer-model <model-id> --code-reviewer-model <model-id>
   ```

   Locate `<setup-skill>` from this skill's installed directory. Do not ask the user to find or run the script. It uses Node.js and npm's `npx` on Windows, macOS, and Linux. If setup fails, report the failed command and stop; rerun only after resolving the reported environment or network issue.
4. After setup completes, ask the user whether they want to run `$codebase-onboarding` to fill in project-specific `agent-context/` documentation. Run it only if they agree. If the skill is not available in the active thread, read `<target-project>/.agents/skills/codebase-onboarding/SKILL.md` and follow it directly after they agree.
5. Confirm the project contains the baseline files, `.agents/skill-overrides/` and its index, `.agents/skills/`, `.codex/config.toml` with the bundled multi-agent defaults, `.codex/agents/` with all three model choices and their reasoning effort, the session-start version hook and checker, `agent-context/skills-installed.json`, and the upstream skills. Summarize the installed skills, selected models and reasoning effort, and whether onboarding was run or deferred.

## Managed Files And Effects

- The script defaults to the current directory if the target path is omitted. It requires an existing directory.
- If `.codex/config.toml` is missing, setup copies the bundled baseline config. Existing config files are preserved, and the version-check hook is added to the selected hook config without replacing existing settings.
- `AGENTS.md`, `CLAUDE.md`, bundled Codex agents, bundled shared skill copies, baseline override files, and the managed upstream skills are refreshed on each run. Existing project context files, local-private files, and project-owned override index entries are preserved.
- The setup creates `AGENTS.local.md`, `CLAUDE.local.md`, `agent-context/` for its setup manifest, `.agents/lessons/`, `.agents/skill-overrides/`, and required `.gitignore` entries when missing. Managed ignore entries include the local files, agent task/report directories, and `node_modules/`.
- It copies the plugin's bundled skill folders into `.agents/skills/`. Those copies are managed outputs; local edits to a copied baseline skill are replaced when setup runs again.
- It records the installed Lean Coding Agent release in `agent-context/skills-installed.json`, copies the version checker into `.codex/hooks/lean-coding-agent/`, and registers a `SessionStart` hook in `.codex/hooks.json` or `.codex/config.toml`. Existing hook definitions are preserved, and rerunning setup does not add duplicate registrations.
- Codex requires review and trust for project-local hooks before they run. The version check runs on startup and resume, stays quiet when current or when GitHub is unavailable, and asks Codex to mention a newer release in its first reply.
- The agent-browser setup installs a development dependency with the detected package manager and installs its browser runtime. Upstream skills are installed through `npx skills add` and require network access.
- The Node.js script is the single cross-platform entry point for both project setup and skill installation.

## Bundled References

The `references/` directory contains the baseline inputs needed after the plugin is installed and the original source repository is unavailable:

- `references/agents/` contains the three native Codex subagent TOML templates.
- `references/config.toml` contains the baseline Codex project configuration copied when the target has no `.codex/config.toml`.
- `references/baseline/` contains `AGENTS.md` and `CLAUDE.md`.
- `references/docs/incidents/README.md` contains the incident report template.
- `references/skill-overrides/` contains the baseline override index and override files copied into `.agents/skill-overrides/`.
- `references/release.json` records the release version and repository so standalone Skills CLI installs can register the same update check.
- `scripts/check_skill_updates.mjs` is the shared checker copied into initialized projects.

These files are bundled snapshots of this repository's canonical files. When updating a canonical source, refresh its matching reference copy before building the plugin.
