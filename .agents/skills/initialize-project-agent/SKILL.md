---
name: initialize-project-agent
description: Initialize a new project repo so it uses this shared agents baseline. Use when Codex needs to bootstrap a project with copied `AGENTS.md` and `CLAUDE.md`, local-private files, `agent-context`, shared `.agents/lessons`, shared subagents for Claude Code and Codex, and copied installable skills from this repo's `skills/` folder into the target repo's `.agents/skills` and `.claude/skills`.
---

# Initialize Project Agent

Use the shared bootstrap script instead of recreating the setup manually.

## Workflow

1. Identify the target project repo path.
2. Run `python scripts/init_project_agent.py <target-repo>` from this repo root.
3. Verify the target repo now contains:
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
   - `agents/` with shared subagent source files
   - `.claude/agents/` with Claude Code subagent files
   - `.codex/agents/` with Codex custom agent files
   - `agent-context/skills-installed.json`
   - `.agents/skills/` and `.claude/skills/` with the copied skill folders from this repo's `skills/`
4. Tell the user which skills were installed.

## Notes

- Keep the folder name `agent-context` exactly as requested by this repo's convention.
- Keep this skill in this repo's `.agents/skills/` folder because it is only for maintaining this shared repo itself.
- Do not place this skill in `skills/`, because `skills/` is the source copied into initialized project repos.
- The bootstrap script is idempotent for the managed pieces:
  - It recopies the shared `AGENTS.md` and `CLAUDE.md` baseline files.
  - It creates local files only when they do not already exist.
  - It copies missing baseline project-context starter files from this repo's `agent-context/`.
  - It creates `agent-context/README.md` only when it does not already exist.
  - It creates `.agents/lessons/LESSONS.md` only when it does not already exist.
  - It copies shared subagent files only when the target file does not already exist.
  - It creates Codex custom agent TOML files from the shared subagent Markdown only when the target file does not already exist.
  - It recopies the current repo-local shared skills into the target repo.
  - It removes previously managed installed skills that are no longer present in `skills/`.
- The bootstrap script also cleans up legacy external-skill bootstrap artifacts if an older target repo still has them.
