---
name: project-conventions
description: Capture the non-obvious project conventions agents would otherwise get wrong in docs/conventions/ (CODING-STANDARDS.md, TESTING.md, WORKFLOWS.md), from repo evidence plus a short interview. Use when setting up a project, joining one, or creating, filling, or refreshing docs/conventions/.
---

# Project Conventions

Capture what an agent would otherwise get wrong in three files under `docs/conventions/`. Do not create or update `AGENTS.md` or `CLAUDE.md` as part of this skill.

## Why

Studies of repository context files found that generated codebase overviews do not help agents find the right files, that generated files mostly repeat existing docs, and that every extra instruction raises cost by around 20% without reliably improving task success. What helps is short, non-obvious knowledge, and the most valuable of it is not in the repo at all, so this skill asks. Full rationale and citations: [docs/project-conventions.md](https://github.com/aloilor/lean-coding-agent/blob/main/docs/project-conventions.md).

## Files

| File | Holds | Template |
| --- | --- | --- |
| `docs/conventions/CODING-STANDARDS.md` | Conventions tooling does not enforce, boundaries and invariants, "never do X" rules, including API, data, and security rules. | `references/CODING-STANDARDS.md` |
| `docs/conventions/TESTING.md` | Exact verification commands, what to run per change type, test traps. | `references/TESTING.md` |
| `docs/conventions/WORKFLOWS.md` | Non-default commands, setup and CI traps, generated files, review and release rules. | `references/WORKFLOWS.md` |

Project terms belong in `docs/conventions/GLOSSARY.md` and decisions in `docs/conventions/adr/`, both owned by `lean-grill-with-docs`. Do not duplicate them here.

## The Inclusion Test

Write a fact only when all three hold:

1. **Not cheaply discoverable.** `rg`, a directory listing, a manifest, linter config, existing code, or the README would not answer it in under a minute.
2. **Costly if wrong.** A wrong command or flag, a broken invariant, a forbidden path, an unsafe operation, a rejected review.
3. **Confirmed.** Backed by code, config, CI, docs, or git history, or stated by the user. Mark indirect conclusions `Inferred from ...`.

Leave out directory maps, tech-stack and dependency tables, architecture overviews, endpoint or schema inventories, rules the linter or formatter already enforces, and anything copied from the README or `docs/`. Link to an existing doc instead of restating it.

## Process

1. **Read what exists.** Read `docs/conventions/`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the README, and `docs/` (including `docs/conventions/GLOSSARY.md` and `docs/conventions/adr/`). If a legacy `agent-context/` folder exists, treat its content as candidates and tell the user it can be deleted once migrated.
2. **Collect candidates from evidence.** Use `rg --files`, `rg`, and targeted reads. Do not read every file. Look for:
   - Commands that differ from the stack default or need flags, env vars, services, or a specific order (manifests, Makefiles, CI).
   - CI checks that local defaults skip.
   - Generated files that must not be hand-edited and the command that regenerates them.
   - Boundaries enforced only by convention, and comments explaining workarounds (`HACK`, `NOTE`, `do not`).
   - Recurring fixes in git history (`git log --oneline --grep fix -n 50`) and review feedback in `.github/` templates.
3. **Interview.** Ask the user up to five short questions in one message, about what the evidence cannot show: rules reviewers enforce, things agents or new contributors get wrong, forbidden operations, flaky tests, deploy constraints. Offer concrete candidates from step 2 to confirm or reject. If the user declines, write only evidence-backed facts.
4. **Filter.** Apply the inclusion test to every candidate. Drop failures rather than rewording them.
5. **Write.** Create or update the three files in place. Preserve confirmed existing content, remove content that fails the test, and keep a file even when it only says that stack defaults apply. Use bullets, not prose.
6. **Report.** Summarize what was added, removed, and left as open questions.

When the user asks to understand or be walked through the repo, explain it in chat. Persist only facts that pass the inclusion test.

## Rules

- **Verify, don't guess.** If config and code disagree, trust the code. Write `Unknown` rather than a plausible guess.
- **Document, don't legislate.** Record existing practice and what the user states; do not invent new rules, thresholds, or architecture.
- **Keep secrets out.** Name config keys, never values.
- **Prefer pointers to copies.** `See docs/deploy.md` beats restating the deploy guide.
