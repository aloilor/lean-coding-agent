# Contributing

## Repository layout

The [`skills/`](skills/) directory contains the source skills. The setup skill's `references/` directory contains baseline snapshots it needs when installed on its own; update those copies when their source files change.

## Skill overrides

Edit skill overrides in [`skills/skill-overrides/`](skills/skill-overrides/) only. Enable the repository hooks once:

```sh
git config core.hooksPath .githooks
```

The pre-commit hook then mirrors staged override changes into the setup skill's `references/skill-overrides/` and stages the copies. Run `npm run sync-skill-overrides` to sync manually, or `npm run check-skill-overrides` to check for drift.

## Tests

Run the Node.js test suite, which checks setup initialization, agent installation, reruns, and failure handling:

```sh
node --test
```

## Releases

The root [`package.json`](package.json) is the release version source. This repository uses Changesets to version the skills collection and prepare GitHub releases. Install the development dependencies with `npm ci`, then add a changeset for each user-facing change:

```sh
npm run changeset
```

The release workflow opens a version pull request after changesets reach `main`. Merging that pull request updates `package.json` and `CHANGELOG.md`, then creates a GitHub tag and release for the skills collection.
