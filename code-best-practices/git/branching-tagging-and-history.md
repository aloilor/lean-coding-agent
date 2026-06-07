# Branching Tagging And History

## Start From A Clean Main Branch

- Do not develop directly on `main`.
- Update your local `main` before creating a branch so you do not start from stale history.
- Prefer a short branch name that explains the purpose.

Example:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/invoice-export
```

## Keep Branches Short-Lived And Focused

- Use one branch for one change, bug fix, or small related set of edits.
- Merge or close branches quickly so they do not drift far from `main`.
- Avoid mixing refactors, behavior changes, and formatting-only edits unless they must land together.

Good branch names:

- `feature/invoice-export`
- `fix/login-timeout`
- `docs/setup-clarification`

## Commit In Small Reviewable Steps

- Make each commit represent one clear idea that can be reviewed and reverted safely.
- Stage intentionally instead of adding every changed file by default.
- Write commit messages that explain the change in terms of behavior or intent.

Better commit message examples:

- `feat: add CSV export for invoices`
- `fix: handle null email during signup`
- `docs: clarify local development steps`

## Rebase Carefully And Merge Deliberately

- Rebase your branch on top of the latest remote `main` to reduce noisy merge commits in your feature branch.
- Do not rebase shared history that other people are already using.
- Use merge when you want to preserve the branch integration point exactly as it happened.

Example branch refresh:

```bash
git fetch origin
git rebase origin/main
```

## Push Safely

- Push feature branches early so work is backed up and visible.
- Use `--force-with-lease` instead of `--force` when you must push rebased history from your own branch.
- Never force-push `main` or another shared branch.

Example:

```bash
git push -u origin feature/invoice-export
git push --force-with-lease
```

## Tag Releases Clearly

- Use annotated tags for releases because they include metadata and a message.
- Tag commits that already represent a reviewed release state, usually on `main`.
- Use a consistent versioning scheme such as semantic versioning when the project releases versions.

Example:

```bash
git tag -a v1.4.0 -m "Release v1.4.0"
git push origin v1.4.0
```

## Recover Without Panic

- Use `git restore` to discard local file changes instead of older checkout patterns.
- Use `git restore --staged` when you staged the wrong file.
- Use `git reflog` when you need to recover a lost commit, branch tip, or pre-rebase state.
- Use `git stash` sparingly for short interruptions, not as long-term storage.

Example recovery commands:

```bash
git restore src/app.js
git restore --staged src/app.js
git reflog
git stash push -m "wip before rebase"
```

## Avoid High-Risk Habits

- Avoid `git add .` unless you already reviewed the full worktree carefully.
- Avoid large mixed commits with unrelated changes.
- Avoid long-lived branches that require repeated conflict-heavy rebases.
- Avoid publishing every local tag with `git push --tags` unless that is your intent.

## Practical Checks

- Is this branch focused on one change that can be reviewed on its own?
- Would each commit message still make sense to another engineer next month?
- Am I rewriting only history that is safe for me to rewrite?
- Did I tag only a release-worthy commit, and did I use an annotated tag?
- If I need to undo something, do I know whether `restore`, `reflog`, or `stash` is the right tool?
