# Git

This folder collects reusable Git best practices for day-to-day branching, commits, history management, releases, and safe collaboration.

## Sources

- Conventional Branch, [Conventional Branch 1.0.0](https://conventionalbranch.org/)
- Conventional Commits, [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- Git, [git-branch](https://git-scm.com/docs/git-branch)
- Git, [git-rebase](https://git-scm.com/docs/git-rebase)
- Git, [git-tag](https://git-scm.com/docs/git-tag)
- Git, [git-reflog](https://git-scm.com/docs/git-reflog)

## Contents

- [Branching Conventions](./branching-conventions.md): how to name branches consistently using Conventional Branch prefixes and machine-friendly descriptions.
- [Commit Conventions](./commit-conventions.md): how to write Conventional Commit messages with clear types, scopes, and breaking-change markers.
- [Branching Tagging And History](./branching-tagging-and-history.md): how to keep Git branches short-lived, history reviewable, releases tagged clearly, and recovery steps safe.

## Core Rules

- Use a small, documented set of branch prefixes with clear lowercase descriptions.
- Keep branches short-lived and focused on one change.
- Prefer small commits with conventional messages that explain intent.
- Update your branch from the remote before opening or refreshing a review.
- Rewrite only your own unpublished or private branch history.
- Use annotated tags for releases and `reflog` for recovery.
