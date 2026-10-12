# Update Setup Managed Ignore Rules

## Mistake Pattern

Updating this repo's root `.gitignore` can leave set-up project repos unchanged when their ignore rules are managed by the setup script.

## Rule

When a gitignore rule should apply to set-up repos, update the setup-managed ignore list and relevant workflow documentation, then verify the setup script writes the expected entries to a target repo. Do not assume the shared repo's root `.gitignore` is copied into targets.
