# Change Process Grill Guide

Find out how a change gets from an idea to a release. Git history shows what happened, including every shortcut anyone took, so ask what is supposed to happen.

Examples below show the shape of a useful line. Never copy them into a project.

## Branching

- **Ask about:** the strategy (trunk-based, GitFlow, release branches), branch naming, what may go straight to the main branch, how long branches should live.
- **Look at:** remote branch names, merge commits in `git log`, CI branch filters.
- Useful: "Small docs fixes go straight to `main`; everything else uses `<type>/<description>` from an up-to-date `main`."
- Obvious: "Create a branch for your work."

## Commits

- **Ask about:** message format, whether commits get squashed, what a commit must contain alongside the code.
- **Look at:** recent commit messages, commitlint config, changeset config.
- Useful: "Add a changeset for every change that reaches users; skip it for CI and test-only changes."

## Pull Requests And Reviews

- **Ask about:** what a PR must contain, how big one can be, who approves, what reviewers reject in practice, merge method, whether failed checks block merging.
- **Look at:** PR templates, `CODEOWNERS`, branch protection hints in CI.
- Useful: "Reviewers reject PRs that mix refactors with behavior changes."
- Useful: "Branch protection is unavailable here, so check CI is green before merging."

## Releases

- **Ask about:** versioning scheme and what counts as breaking, changelog ownership, who cuts a release and how, tags, release cadence, support for older versions.
- **Look at:** release workflows, tags, `CHANGELOG`, version fields.
- Useful: "Never bump the version by hand; merging the generated version PR creates the tag and release."

## Docs That Change With Code

- **Ask about:** changes that must update a specific doc in the same PR.
- **Look at:** `git log --name-only` for docs that repeatedly change alongside certain paths.
- Useful: "Adding, renaming, or removing a skill also updates the skill list in the README."

## What Agents May Do Alone

- **Ask about:** committing, pushing, opening PRs, merging, tagging, publishing.
- Useful: "Agents open PRs but merge only when asked."
