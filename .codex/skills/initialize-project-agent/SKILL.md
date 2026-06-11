---
name: initialize-project-agent
description: Initialize a new project repo so it uses this shared agents baseline. Use when Codex needs to bootstrap a project with a local AGENTS.md that references this repo, create `agent-context`, add a local `CLAUDE.md`, and copy the installable skills from this repo's `global-skills/` folder into the target repo's `.codex/skills` and `.claude/skills`.
---

# Initialize Project Agent

Use the shared bootstrap script instead of recreating the setup manually.

## Workflow

1. Identify the target project repo path.
2. Run `python scripts/init_project_agent.py <target-repo>` from this repo root.
3. Verify the target repo now contains:
   - `AGENTS.md` with a relative reference back to this repo's `AGENTS.md`
   - `CLAUDE.md` that tells Claude to read the local `AGENTS.md`
   - `agent-context/`
   - `agent-context/global-skills-installed.json`
   - `.codex/skills/` and `.claude/skills/` with the copied skill folders from this repo's `global-skills/`
4. Tell the user which skills were installed.

## Notes

- Keep the folder name `agent-context` exactly as requested by this repo's convention.
- Keep this skill in this repo's `.codex/skills/` folder because it is only for maintaining this shared repo itself.
- Do not place this skill in `global-skills/`, because `global-skills/` is the source copied into initialized project repos.
- The bootstrap script is idempotent for the managed pieces:
  - It creates or updates the target `AGENTS.md` shared-baseline block.
  - It recopies the current repo-local global skills into the target repo.
  - It removes previously managed installed skills that are no longer present in `global-skills/`.
- The bootstrap script also cleans up legacy external-skill bootstrap artifacts if an older target repo still has them.
