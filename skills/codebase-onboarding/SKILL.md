---
name: codebase-onboarding
description: Analyze a repository and create or update structured agent-context documentation for agent onboarding. Use when filling agent-context/, onboarding agents or engineers to a codebase, refreshing project context docs, or documenting architecture, folder structure, workflows, testing, and domain language from repo evidence.
---

# Codebase Onboarding

Use this skill to fill `agent-context/` with precise, structured, evidence-backed documentation. The output is not a single onboarding guide; it is a set of focused project-context files that future agents can read quickly.

## Core Rule

Document facts from repo evidence. If a fact is inferred, mark it as inferred. If a fact cannot be found, write `Unknown` or add a short `Open Questions` item instead of guessing.

## Required References

Read `references/evidence-checklist.md` before discovery.

Read the reference for each file before creating or updating that file:

- `references/readme.md` for `agent-context/README.md`.
- `references/domain.md` for `agent-context/domain.md`.
- `references/folder-structure.md` for `agent-context/folder-structure.md`.
- `references/architecture.md` for `agent-context/architecture.md`.
- `references/workflows.md` for `agent-context/workflows.md`.
- `references/testing.md` for `agent-context/testing.md`.
- `references/api.md` for optional `agent-context/api.md`.
- `references/data.md` for optional `agent-context/data.md`.
- `references/operations.md` for optional `agent-context/operations.md`.
- `references/security.md` for optional `agent-context/security.md`.

## Workflow

1. Inspect the repo state and existing context.
   - Run `git status --short`.
   - List existing context files with `rg --files agent-context` when the folder exists.
   - Read `AGENTS.md`, `AGENTS.override.md` when present, `agent-context/README.md` when present, and any existing `agent-context/*.md` files relevant to the update.

2. Gather evidence before writing.
   - Use `rg --files` to map source, tests, config, docs, scripts, CI, deployment, and package files.
   - Read the smallest set of files needed to support each documented claim.
   - Prefer existing project docs and config over assumptions from file names.

3. Create or update the standard `agent-context/` files.
   - `README.md`: index and orientation.
   - `domain.md`: project-specific domain language only.
   - `folder-structure.md`: important directories and ownership notes.
   - `architecture.md`: system shape, boundaries, data flow, dependencies, and constraints.
   - `workflows.md`: setup, build, run, review, release, and operational workflows.
   - `testing.md`: test commands, frameworks, fixtures, naming, and verification expectations.

4. Add optional files only when evidence supports them.
   - `api.md` for API contracts and endpoint conventions.
   - `data.md` for schemas, migrations, seed data, or storage conventions.
   - `operations.md` for deployment, monitoring, incidents, jobs, queues, or runbooks.
   - `security.md` for auth, authorization, secrets, privacy, or compliance constraints.

5. Keep edits scoped.
   - Update only `agent-context/` docs unless the user explicitly asks for broader docs.
   - Preserve useful existing content, but reorganize it into the required structure when needed.
   - Add examples that come from the repo, such as actual commands, paths, endpoints, config keys, test names, or module names.

6. Verify.
   - Check that every created file follows its matching file reference in `references/`.
   - Run `rg -n "TBD|TODO|Unknown|Open Questions" agent-context` and ensure unresolved items are intentional.
   - Run `git diff -- agent-context` and confirm the changes are documentation-only and evidence-backed.

## Writing Standards

- Use concise, scannable sections.
- Prefer tables for path inventories, commands, and interfaces.
- Include references as relative links to source files or directories.
- Include short examples when they make a rule actionable.
- Do not document generic programming concepts in `domain.md`.
- Do not describe implementation classes unless they are stable public extension points or central architectural boundaries.
- Do not invent setup, test, or deployment commands.

## Completion Output

When done, report:

- files created or updated in `agent-context/`;
- the main evidence sources consulted;
- unresolved open questions;
- verification performed.
