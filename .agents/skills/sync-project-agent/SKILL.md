---
name: sync-project-agent
description: Refresh an existing initialized project repo from this Codex-only agents baseline. Use when Codex needs to propagate the latest baseline files, Codex agents, installable skills, skill overrides, ignore rules, upstream skill installs, browser tooling, and other initializer-managed updates while preserving project-owned context and private local files.
---

# Sync Project Agent

Use the existing initializer as the single synchronization engine. Run this skill from the shared baseline repo and require the target project repo path.

## Workflow

1. Resolve the baseline and target paths. Reject a missing target, a non-directory target, or the baseline repo itself.
2. Confirm `agent-context/skills-installed.json` exists in the target and its `source_root` points to this baseline repo's `skills/` directory. If the target has not been initialized by this baseline, use `$initialize-project-agent` instead.
3. Inspect `git -C <target-repo> status --short`. Do not stash, discard, or rewrite unrelated target changes. If tracked changes overlap initializer-managed files that will be refreshed, show the conflicts and obtain explicit approval before continuing.
4. Run `python scripts/init_project_agent.py <target-repo>` from the baseline repo root.
5. Do not run `codebase-onboarding` during a routine sync. Run it only when the user asks or when the update changes the expected project-context structure and the context must be regenerated.
6. Verify:
   - the initializer completed successfully;
   - `agent-context/skills-installed.json` still names this baseline's `skills/` directory;
   - `python -m unittest tests.test_init_project_agent.InitializationIntegrationTest.test_rerun_refreshes_managed_files_and_preserves_project_owned_files` passes in the baseline repo;
   - `git -C <target-repo> diff --check` passes;
   - the target diff contains only expected baseline-managed updates plus pre-existing target changes.
7. Report the refreshed surfaces, preserved project-owned files, verification results, and any update that remains manual.

## Ownership Rules

- Refresh initializer-managed baseline files, generated agent files, shared skills, shared skill overrides, ignore rules, manifests, and tool installations according to `scripts/init_project_agent.py`.
- Leave legacy files from older baseline versions untouched; removed baseline surfaces require optional manual cleanup.
- Preserve project-owned `agent-context/` content, project lessons, incident indexes, and local-private files whenever the initializer treats them as create-if-missing or merge-only.
- Treat the initializer as authoritative. Do not add a second copy or deletion algorithm to this skill.
- Never claim that every file in the baseline repo is mirrored. Only content owned by the initializer's contract is synchronized.

## Completion

Summarize the target path and resulting diff. Include a `Did Not Do` note, using `No meaningful omissions` when nothing remains.
