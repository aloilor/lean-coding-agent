# Workflows

## Change Process

- **Branch:** start non-trivial work from an up-to-date `main`. Name branches `<type>/<description>` per [Conventional Branch 1.1.0](https://conventionalbranch.org/), using `feat/`, `fix/`, or `chore/`. `docs`, `refactor`, and `test` work goes under `chore/`.
- **Trunk-based:** `main` is the only long-lived branch. Split larger work into small PRs. Trivial changes can go straight to `main`.
- **Commits:** use the [`git-conventional-commit`](../../skills/git-conventional-commit/SKILL.md) skill.
- **Changeset:** add one with `npm run changeset` in the same PR for changes that reach skill users. Skip it for repo-only changes such as tests, `TODO.md`, or these conventions.
- **PR:** keep to one concern. Write the title as a Conventional Commit, since it becomes the commit on `main`. The body says what changed, why, and how it was verified.
- **Merge:** the author reviews the diff, then runs `gh pr merge --squash --delete-branch`. Agents open PRs but merge only when asked.

## CI And Release

- `.github/workflows/ci.yml` runs `node --test` and `npm run check-skill-overrides` on PRs to `main` and pushes to `main`. Check that it is green before merging: branch protection is unavailable on this repository's GitHub plan, so a failure does not block the merge.
- `.github/workflows/release.yml` runs on every push to `main`. When changesets are pending, it opens the `chore: version skills` PR from `changeset-release/main`, a generated branch exempt from the naming rule.
- Merging that PR updates `package.json` and `CHANGELOG.md`, then creates the tag and GitHub release. Do not bump the version by hand.
