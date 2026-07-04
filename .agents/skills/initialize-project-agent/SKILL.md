---
name: initialize-project-agent
description: Initialize a new project repo so it uses this shared agents baseline and has populated project context. Use when Codex needs to bootstrap a project with copied `AGENTS.md` and `CLAUDE.md`, local-private files, `agent-context`, shared `.agents/lessons`, shared subagents for Claude Code and Codex, copied installable skills from this repo's `skills/` folder into the target repo's `.agents/skills` and `.claude/skills`, and a follow-up `codebase-onboarding` pass.
---

# Initialize Project Agent

Use this skill as the setup entry point for new projects. Do not ask the user to run the bootstrap script directly; run it as this skill's internal bootstrap step, then run `codebase-onboarding` in the target repo.

## Workflow

1. Identify the target project repo path.
2. Run `python scripts/init_project_agent.py <target-repo>` from this repo root.
3. Switch context to the target repo and use `$codebase-onboarding` to analyze the project and create or update structured `agent-context/` docs. If the newly installed skill is not auto-discovered in the current thread yet, read `<target-repo>/.agents/skills/codebase-onboarding/SKILL.md` and follow it directly.
4. Verify the target repo now contains:
   - `AGENTS.md` copied exactly from this repo's `AGENTS.md`
   - `CLAUDE.md` copied exactly from this repo's `CLAUDE.md`
   - `AGENTS.local.md` for local-private agent notes
   - `CLAUDE.local.md` for local-private Claude notes
   - `.gitignore` entries for local files, local task folders, shared local handoff reports, and Playwright CLI generated artifacts
   - `agent-context/`
   - baseline project-context starter files copied from this repo's `agent-context/`
   - `agent-context/README.md` as a shared project-specific context starter
   - `.agents/lessons/`
   - `.agents/lessons/LESSONS.md` as a shared agent lessons index
   - `.agents/skill-overrides/`
   - `.agents/skill-overrides/INDEX.md` as a shared skill-overrides index
   - `.claude/agents/` with Claude Code subagent files
   - `.codex/agents/` with Codex custom agent files
   - `agent-context/skills-installed.json`
   - for PHP/Laravel targets: `phpstan.neon.dist`, `phpstan-baseline.neon`, `scripts/quality-gate` (executable), PostToolUse hooks in `.claude/settings.json` and `.codex/hooks.json`, and `QUALITY-PIPELINE.md` (agent-only enforcement; no git hook)
   - `.agents/skills/` and `.claude/skills/` with the copied skill folders from this repo's `skills/`
   - `agent-context/` docs created or refreshed by `codebase-onboarding`, including `agent-context/skills.md`
5. Tell the user which skills were installed and which `agent-context/` docs were created or updated by `codebase-onboarding`.

## Notes

- Keep the folder name `agent-context` exactly as requested by this repo's convention.
- Keep this skill in this repo's `.agents/skills/` folder because it is only for maintaining this shared repo itself.
- Do not place this skill in `skills/`, because `skills/` is the source copied into initialized project repos.
- Run `codebase-onboarding` only after the bootstrap script finishes so the generated `agent-context/skills.md` can include the installed project-local skills.
- The bootstrap script is idempotent for the managed pieces:
  - It recopies the shared `AGENTS.md` and `CLAUDE.md` baseline files.
  - It creates local files only when they do not already exist.
  - It copies missing baseline project-context starter files from this repo's `agent-context/`.
  - It creates `agent-context/README.md` only when it does not already exist.
  - It creates `.agents/lessons/LESSONS.md` only when it does not already exist.
  - It creates `.agents/skill-overrides/INDEX.md` only when it does not already exist.
  - It refreshes Claude Code subagent files in `.claude/agents/` from this repo's `agents/` source on every run.
  - It regenerates Codex custom agent TOML files in `.codex/agents/` from the shared subagent Markdown on every run.
  - It recopies the current repo-local shared skills into the target repo.
  - It removes previously managed installed skills that are no longer present in `skills/`.
  - It provisions the PHP/Laravel quality gate (templates + executable `scripts/quality-gate`) only for Laravel targets, copying files only when absent. Enforcement is agent-only via PostToolUse hooks; it installs no git hook.
- The bootstrap script also cleans up legacy external-skill bootstrap artifacts if an older target repo still has them.
