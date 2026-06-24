# Update Bootstrap Managed Ignore Rules

## Mistake Pattern

Updating this repo's root `.gitignore` can leave initialized project repos unchanged when their ignore rules are managed by a bootstrap script.

## Rule

When a gitignore rule should apply to initialized repos, update the bootstrap-managed ignore list and relevant workflow documentation, then verify the initializer writes the expected entries to a target repo. Do not assume the shared repo's root `.gitignore` is copied into targets.
