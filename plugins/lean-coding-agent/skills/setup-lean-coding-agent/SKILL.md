---
name: setup-lean-coding-agent
description: Initialize the current project with the Lean Coding Agent baseline after the plugin is installed, including project guidance, bundled skills, skill overrides, and configurable Codex subagents.
---

# Setup Lean Coding Agent

Run this skill after installing the Lean Coding Agent plugin to initialize the current project. The bundled Node.js script copies the plugin's skills and baseline assets into the project, installs the Codex subagents with the models selected by the user, installs the agent-browser development dependency, and adds the upstream skills.

## Workflow

1. Identify the target project. Use the current working directory when the user invoked this skill from the project; otherwise ask which existing project directory to initialize.
2. Ask which model ID to assign to each Codex subagent:
   - `bug-diagnostician` (default: `gpt-6-luna`)
   - `implementer` (default: `gpt-6-luna`)
   - `code-reviewer` (default: `gpt-6-luna`)

   The user may choose the defaults or provide different model IDs for each agent. Preserve each agent's existing `model_reasoning_effort` setting.
3. Run the bundled Node.js setup script from the target project, passing the selected models:

   ```text
   node "<setup-skill>/scripts/setup_lean_coding_agent.mjs" "<target-project>" --bug-diagnostician-model <model-id> --implementer-model <model-id> --code-reviewer-model <model-id>
   ```

   Locate `<setup-skill>` from this skill's installed directory. Do not ask the user to find or run the script. It uses Node.js and npm's `npx` on Windows, macOS, and Linux. If setup fails, report the failed command and stop; rerun only after resolving the reported environment or network issue.
4. After setup completes, ask the user whether they want to run `$codebase-onboarding` to fill in project-specific `agent-context/` documentation. Run it only if they agree. If the skill is not available in the active thread, read `<target-project>/.agents/skills/codebase-onboarding/SKILL.md` and follow it directly after they agree.
5. Confirm the project contains the baseline files, `.agents/skill-overrides/` and its index, `.agents/skills/`, `.codex/agents/` with all three model choices, `agent-context/skills-installed.json`, and the upstream skills. Summarize the installed skills and selected models, and whether onboarding was run or deferred.

## Managed Files And Effects

- The script defaults to the current directory if the target path is omitted. It requires an existing directory.
- `AGENTS.md`, `CLAUDE.md`, bundled Codex agents, bundled shared skill copies, baseline override files, and the managed upstream skills are refreshed on each run. Existing project context files, local-private files, and project-owned override index entries are preserved.
- The setup creates `AGENTS.local.md`, `CLAUDE.local.md`, `agent-context/` for its setup manifest, `.agents/lessons/`, `.agents/skill-overrides/`, and required `.gitignore` entries when missing.
- It copies the plugin's bundled skill folders into `.agents/skills/`. Those copies are managed outputs; local edits to a copied baseline skill are replaced when setup runs again.
- The agent-browser setup installs a development dependency with the detected package manager and installs its browser runtime. Upstream skills are installed through `npx skills add` and require network access.
- The Node.js script is the single cross-platform entry point for both project setup and skill installation.

## Bundled References

The `references/` directory contains the baseline inputs needed after the plugin is installed and the original source repository is unavailable:

- `references/agents/` contains the three native Codex subagent TOML templates.
- `references/baseline/` contains `AGENTS.md` and `CLAUDE.md`.
- `references/docs/incidents/README.md` contains the incident report template.
- `references/skill-overrides/` contains the baseline override index and override files copied into `.agents/skill-overrides/`.

These files are bundled snapshots of this repository's canonical files. When updating a canonical source, refresh its matching reference copy before building the plugin.
