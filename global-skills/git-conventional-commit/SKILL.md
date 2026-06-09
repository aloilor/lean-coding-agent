---
name: git-conventional-commit
description: Review git changes, propose commit messages, and create commits using Conventional Commits 1.0.0. Use when asked to commit work, suggest a commit message, stage the right files, or enforce a safe conventional commit workflow with type, optional scope, description, optional body, and optional footers.
---

# Git Conventional Commit

Follow the Conventional Commits 1.0.0 specification:
https://www.conventionalcommits.org/en/v1.0.0/

Use this header format:
`<type>[optional scope][!]: <description>`

The `<description>` should be a concise, repository-specific summary of the change.

Optional sections:
- body
- footer(s)

## Workflow

1. Inspect the repo state before staging or committing anything.
   Run `git status --short` first.
   Review the actual content with `git diff` for unstaged changes and `git diff --cached` for staged changes.

2. Define the intended commit set.
   Commit only the files that match the user's request.
   If unrelated files are dirty, leave them alone unless the user explicitly asks to include them.
   Treat existing worktree changes as intentional user work by default. Never revert, delete, or "clean up" manual edits just to make the commit set simpler unless the user explicitly asks for that.
   If many changed files are not part of one coherent change, split them into separate commits for each independent logical change set instead of forcing one mixed commit.

3. Stage only the intended files.
   Use targeted `git add <paths>` commands.
   Avoid broad staging like `git add .` or `git add -A` unless the user clearly wants every change included.
   When splitting a large mixed worktree, stage and commit one independent logical change set at a time, reviewing each staged subset before moving to the next one.

4. Review exactly what will be committed.
   Run `git diff --cached --stat` and `git diff --cached`.
   If the staged diff does not match the requested change set, fix the staging before writing the commit message.
   Fix the staging by adjusting what is staged, not by reverting unrelated working-tree changes.

5. Choose the Conventional Commit header.
   Pick the type from the actual change intent.
   Add a short scope when it helps identify the changed area.
   Keep the description concise, imperative, and without a trailing period.

6. Add body or footers only when they add real value.
   Use a body for context that is useful to future readers.
   Use footers for metadata such as `BREAKING CHANGE:` or issue references.

7. Commit only when there is something to commit.
   If the staged diff is empty, report that clearly instead of creating an empty commit.
   If the user only asked for a proposed message, stop after proposing it.
   If the requested work requires multiple commits, keep going commit by commit until no intended logical change sets remain.
   After each commit in a multi-commit run, rerun `git status --short` and continue if remaining changes still match the user's requested work.
   If you stop while changes remain, say exactly what is left and whether it is excluded as unrelated worktree state or still pending for a later commit.

8. Confirm the result after committing.
   Run `git log -1 --pretty=format:%s` to confirm the final subject line.

## Commit Types

Use these common types:

- `feat`: add a new feature or behavior
- `fix`: fix a bug or incorrect behavior
- `docs`: documentation-only changes
- `style`: formatting-only changes with no logic changes
- `refactor`: restructure code without changing feature behavior
- `perf`: improve performance
- `test`: add or update tests
- `build`: change build tooling or dependencies
- `ci`: change CI configuration or automation
- `chore`: maintenance work that does not fit the other types
- `revert`: revert a previous commit

## Scope Guidance

- Prefer a short scope derived from the changed area.
- Use lowercase scopes.
- Omit the scope when the change spans multiple unrelated areas.

Examples of useful scopes:

- `readme`
- `agents`
- `skills`
- `git-commit`
- `src`
- `api`
- `auth`

## Message Rules

- Keep the description imperative: `add`, `update`, `remove`, `fix`, `rename`.
- Make the description a concise summary tied to this repository's actual change.
- Keep the type and scope lowercase.
- Do not end the description with a period.
- Use `!` in the header for breaking changes when appropriate.
- Add a `BREAKING CHANGE:` footer when the migration impact needs explanation.

## Examples

Simple documentation update:
- `docs(readme): explain shared baseline and project overrides`

Add a new reusable skill:
- `feat(skills): add git commit workflow skill`

Fix a bug in a focused area:
- `fix(auth): handle expired session token during refresh`

Refactor with breaking change:
- `refactor(api)!: rename agent config endpoint`

Commit with body:

```text
feat(git-commit): add staged diff review workflow

Require reviewing git diff and git diff --cached before committing.
Document safer staging guidance for partially dirty repositories.
```

Commit with breaking change footer:

```text
refactor(config)!: replace agents root path setting

Move project-level agent config to a new key used across all repos.

BREAKING CHANGE: existing automation that reads the old config key must be updated.
```

## Safety Rules

- Never run destructive git commands unless the user explicitly requests them.
- Treat `git reset --hard`, `git checkout -- <path>`, `git clean -fd`, history rewrites, and force pushes as destructive.
- Do not amend an existing commit unless the user explicitly asks for it.
- Do not include unrelated changes just because they are already present in the worktree.
- When the worktree contains multiple unrelated logical change sets, do not combine them into one commit just to reduce the commit count.
- Do not revert, delete, or overwrite existing user changes in order to make a commit cleaner or narrower. Preserve manual edits unless the user explicitly asks to discard them.
- If there is nothing to commit, say so clearly and do not create an empty commit.
- If the requested commit boundaries are unclear, pause and clarify before committing.

## Output Checklist

- Review `git status --short` first.
- Review `git diff` and `git diff --cached` before finalizing the commit.
- Stage only the intended files.
- Use a valid Conventional Commits header.
- Add body or footers only when they help.
- Confirm the final commit subject after `git commit`.
