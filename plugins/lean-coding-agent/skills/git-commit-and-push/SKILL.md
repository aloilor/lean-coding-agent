---
name: git-commit-and-push
description: Create Conventional Commits for explicitly requested work by invoking $git-conventional-commit, then push the committed branch to its configured remote.
---

# Git Commit And Push

Use this skill only when the user explicitly asks to commit and push. A request to commit without pushing does not activate this workflow.

## Workflow

1. Invoke [$git-conventional-commit](../git-conventional-commit/SKILL.md) and follow its worktree inspection, commit-boundary, staging, Conventional Commit, and verification instructions. Do not create commits outside that skill's workflow.
2. Push only after `$git-conventional-commit` successfully creates and confirms the requested commit or commits. If it reports that there is nothing to commit or fails, stop without pushing.
3. Inspect the current branch and configured push destination. If the branch has an upstream, run `git push`. If it has no upstream and `origin` exists, run `git push --set-upstream origin HEAD`. If there is no `origin` but exactly one remote exists, set that remote as upstream with `git push --set-upstream <remote> HEAD`. If the branch is detached or there is no unambiguous remote, stop and report what is missing.
4. Never force-push or rewrite remote history. If the push is rejected, report the error and stop rather than rebasing or retrying with a different push mode.
5. After a successful push, confirm the branch and worktree state with `git status --short --branch` and report the commit subject and push destination.
