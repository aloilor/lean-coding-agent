---
name: git-conventional-commit
description: Create git commits using Conventional Commits 1.0.0. Use only when the user explicitly asks Codex to commit changes. Do not use for requests that only ask to propose a commit message, review changes, or stage files without committing.
---

# Git Conventional Commit

Complete the request by creating one or more commits. Do not use this skill for advisory-only commit-message work or stop after proposing a message.

Use Conventional Commits 1.0.0:

`<type>[optional scope][!]: <description>`

Add an optional body or footers only when they help future readers.

## Workflow

1. Inspect `git status --short`, `git diff`, and `git diff --cached` before staging or committing.
2. Define coherent commit boundaries. Unless the user narrows the scope, include the entire worktree, split across logical commits when necessary. Do not exclude changes because they predate the current session or were written manually.
3. Stage the intended files. Use targeted `git add <paths>` when splitting changes; use `git add -A` when one commit should include the remaining worktree.
4. Verify each staged set with `git diff --cached --stat` and `git diff --cached`. Correct the staging when it does not match the intended commit; do not revert unrelated working-tree changes.
5. Write a message based on the staged change's intent and create the commit.
6. Commit only a non-empty staged set. For multiple commits, repeat the workflow until `git status --short` is empty unless the user explicitly excluded changes.
7. Confirm each result with `git log -1 --pretty=format:%s`. If explicitly excluded changes remain, identify them and the instruction that excluded them.

## Message Guide

Use the most specific applicable type:

- `feat`: new behavior
- `fix`: corrected behavior
- `docs`: documentation only
- `style`: formatting only
- `refactor`: restructuring without behavior changes
- `perf`: performance improvement
- `test`: test changes
- `build`: build tooling or dependencies
- `ci`: CI configuration or automation
- `chore`: maintenance not covered above
- `revert`: revert a previous commit

Use a short lowercase scope only when it adds useful context. Keep the description concise, repository-specific, imperative, and without a trailing period.

Mark a breaking change with `!`. Add a `BREAKING CHANGE:` footer when migration impact needs explanation. Use bodies for durable context and other footers for metadata such as issue references.

Examples:

- `docs(readme): explain project overrides`
- `feat(skills): add git commit workflow`
- `fix(auth): handle expired refresh tokens`
- `refactor(api)!: rename agent config endpoint`

## Safety

- Do not revert, delete, or overwrite existing user changes to make a commit cleaner or narrower. Preserve manual edits unless the user explicitly asks to discard them.
- Never amend, rewrite history, force-push, or run destructive commands such as `git reset --hard`, `git checkout -- <path>`, or `git clean -fd` unless the user explicitly requests that operation.
- Split unrelated logical changes instead of forcing them into one commit.
- If there is nothing to commit, report it clearly; do not create an empty commit.
- Clarify materially ambiguous commit boundaries before committing.
