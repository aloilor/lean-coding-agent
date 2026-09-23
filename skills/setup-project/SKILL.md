---
name: setup-project
description: Set up or safely synchronize a project with the Lean Coding Agent baseline, selected skills, optional tools, and agent models.
---

# Set Up A Project

Use the bundled scripts/setup_project.py helper from this skill's directory. Resolve the helper relative to this skill resource, never relative to the target project or current working directory. Its assets are bundled with this skill when installed through the Skills CLI, or alongside the plugin package when installed as a Codex plugin; neither route depends on the original repository checkout.

## Gather choices

1. Ask for the target project directory. The helper checks the target and reports whether it is new, already initialized, or a legacy installation.
2. Read the skill catalog with python <skill-directory>/scripts/setup_project.py catalog --json. Present each skill with its recommendation label and reason. Recommendations are suggestions only; select no skill unless the user chooses it.
3. Ask which project-local skills to install. Explain that engineering-standards is recommended for most coding projects, codebase-onboarding for new or unfamiliar projects, and upstream tdd when the project has a test suite. The upstream tdd skill is installed only with the separate community-skills add-on. grill-with-docs and workflow-* are recommended for teams choosing the structured workflow process. REST, Git, SQL, browser, and other specialized skills are contextual options.
4. Ask separately whether to install upstream community skills and whether to install browser tooling. Both default to no. Community skills use npx skills add; browser tooling installs agent-browser with the detected package manager and runs its browser installer.
5. Ask for model IDs separately for implementer, reviewer, and diagnostician. Offer gpt-6-luna as each default. Keep each agent's configured reasoning effort unchanged.

## Preview and apply

Use the same selected options for both helper calls. Pass one --skill NAME for each selected first-party skill, --community-skills and/or --browser-tooling only when chosen, and the selected --implementer-model, --reviewer-model, and --diagnostician-model values. Do not pass either add-on flag when declined on a new setup. During sync, omitted options reuse saved selections.

If the user explicitly turns off a saved add-on during sync, pass --no-community-skills or --no-browser-tooling for that add-on. This updates its saved choice and does not delete files already installed by that add-on.

Run preview --target PATH first. It checks Git status and displays diffs for managed files that would be replaced. Show those paths and changes to the user. If any conflict is shown, ask for explicit approval before continuing. If the user declines, stop without running apply; preview does not write files.

After approval, run apply --target PATH with the same options and the exact --approve-conflicts TOKEN printed by preview. The helper verifies that the files still match that preview before writing. If there are no conflicts, do not pass a token. If the user declines, leave the target untouched.

Never omit skills from later syncs to uninstall them. Saved skills are reapplied and retained. A removal requires the user's explicit choice and a corresponding --remove-skill NAME option; preview its deletions and obtain approval before applying.

The helper writes baseline files before running selected external installs. If an external command fails, report its command and error; the applied local files and unrelated project content remain in place. Automated tests must mock all npx, package-manager, and browser-installer commands.

## Verify

Confirm agent-context/skills-installed.json contains the portable baseline ID, selected skills, add-ons, and all three models. Confirm only the selected first-party skills were copied under .agents/skills/, custom-agent TOMLs use the chosen models, and project-owned context and untracked content remain intact.
