# WORKFLOWS.md Guide

Answers: how to set up the project, which commands differ from stack defaults, which files are generated, how changes are committed and reviewed, and what CI and release need. Verification commands live in `TESTING.md`; do not repeat them here.

Example values below illustrate shape and specificity. Never copy them into a project.

## Setup

- **Look at:** README and `CONTRIBUTING.md` setup steps, `.tool-versions`, `.nvmrc`, `.python-version`, `rust-toolchain.toml`, `engines` fields, bootstrap scripts, devcontainer config, one-time git config.
- **Belongs:** required tool versions and non-default steps, in order. Copy them even when the README has them.
- Write `Stack defaults apply.` when cloning and installing dependencies is all it takes.
- Good: "Run `git config core.hooksPath .githooks` once; the pre-commit hook mirrors override changes."

## Commands

- **Look at:** scripts in `package.json`, `Makefile`, `justfile`, `Taskfile.yml`, `scripts/`, and commands mentioned in docs.
- **Belongs:** commands an agent needs that it would not guess, with when to run them.
- **Drop:** stack defaults that work as-is (`npm install`, `cargo build`), and verification commands already in `TESTING.md`.

## Generated Files

- **Look at:** `DO NOT EDIT` or `@generated` headers, `linguist-generated` in `.gitattributes`, codegen scripts and configs, synced or mirrored copies, lockfiles with special rules.
- **Belongs:** one row per generated path with its source and regenerate command.
- Good: `` | `CHANGELOG.md` | changesets | `npm run version` (release workflow only) | ``

## Change Process

- **Look at:** `CONTRIBUTING.md`, PR and issue templates, commitlint or changeset config, `CODEOWNERS`, branch protection hints in CI, recent merged commit messages (`git log --oneline -n 30`).
- **Belongs:** branch, commit, changelog or changeset, and review requirements not already stated in `AGENTS.md`. Also docs that must change together with code, found where commits touching one path also touch a doc (`git log --name-only`), or where a doc restates behavior it does not own.
- Good: "Add a changeset (`npm run changeset`) for every user-facing change."
- Good: "Adding, renaming, or removing a skill → update the README skill reference in the same change."

## CI And Release

- **Look at:** CI and release workflow files, deploy scripts, environment files, release docs.
- **Belongs:** CI jobs that do more than the Definition Of Done, how releases are cut, deploy constraints, which operations only CI performs.
- Good: "Never bump `package.json` by hand; the release workflow opens a version PR from changesets."

## Traps

- **Look at:** fix commits that follow setup, build, or CI failures, issue templates, failures from running commands while gathering evidence.
- **Belongs:** `symptom → cause → what to do instead`.

## Template

Write this structure exactly. Keep every heading; write `None.` under a heading with no facts.

```md
# Workflows

## Setup
<Stack defaults apply.> or:
1. <step>

## Commands
| Task | Command | When |
| --- | --- | --- |
| <task> | `<command>` | <when> |

## Generated Files
| Generated | Source | Regenerate with |
| --- | --- | --- |
| `<path>` | `<source>` | `<command>` |

## Change Process
- <rule>

## CI And Release
- <rule>

## Traps
- <symptom> → <cause> → <what to do instead>
```
