---
name: codebase-onboarding
description: Analyze an unfamiliar codebase, generate structured agent-context documentation, and activate a provisioned Laravel reviewer-owned quality gate through evidence-backed, user-approved project configuration. Use when joining a new project, filling agent-context/, configuring the provisioned Laravel quality pipeline, or asking to understand, onboard to, or walk through a repo.
---

# Codebase Onboarding

Systematically analyze an unfamiliar codebase and produce structured `agent-context/` documentation. For Laravel repositories with a provisioned reviewer-owned quality gate, also discover, propose, and—after explicit approval—activate project-specific quality-tool configuration. Designed for developers and agents joining a new project or refreshing project context in an existing repo.

Do not create or update `CLAUDE.md` as part of this skill. Put durable shared project context in `agent-context/`.

## When to Use

- First time opening a project.
- Joining a new team or repository.
- User asks "help me understand this codebase".
- User asks to fill or refresh `agent-context/`.
- A provisioned Laravel quality gate needs project-specific activation or a readiness audit.
- User says "onboard me" or "walk me through this repo".

## References

Read `references/evidence-checklist.md` before discovery.

For a Laravel repository containing the provisioned `scripts/quality-gate`, read `references/quality-gate.md` before proposing or changing any quality-tool configuration.

Read the matching reference before creating or updating each file:

- `references/readme.md` for `agent-context/README.md`.
- `references/domain.md` for `agent-context/domain.md`.
- `references/folder-structure.md` for `agent-context/folder-structure.md`.
- `references/architecture.md` for `agent-context/architecture.md`.
- `references/workflows.md` for `agent-context/workflows.md`.
- `references/testing.md` for `agent-context/testing.md`.
- `references/skills.md` for `agent-context/skills.md`.
- `references/api.md` for optional `agent-context/api.md`.
- `references/data.md` for optional `agent-context/data.md`.
- `references/operations.md` for optional `agent-context/operations.md`.
- `references/security.md` for optional `agent-context/security.md`.

## How It Works

### Phase 1: Reconnaissance

Gather raw signals about the project without reading every file. Run these checks in parallel:

```text
1. Package manifest detection
   -> package.json, go.mod, Cargo.toml, pyproject.toml, pom.xml, build.gradle,
      Gemfile, composer.json, mix.exs, pubspec.yaml

2. Framework fingerprinting
   -> next.config.*, nuxt.config.*, angular.json, vite.config.*,
      django settings, flask app factory, fastapi main, rails config

3. Entry point identification
   -> main.*, index.*, app.*, server.*, cmd/, src/main/

4. Directory structure snapshot
   -> Top 2 levels of the directory tree, ignoring node_modules, vendor,
      .git, dist, build, __pycache__, .next

5. Config and tooling detection
   -> .eslintrc*, .prettierrc*, tsconfig.json, Makefile, Dockerfile,
      docker-compose*, .github/workflows/, .env.example, CI configs

6. Test structure detection
   -> tests/, test/, __tests__/, *_test.go, *.spec.ts, *.test.js,
      pytest.ini, jest.config.*, vitest.config.*

7. Project skill inventory
   -> .agents/skills/*/SKILL.md, .claude/skills/*/SKILL.md,
      .codex/skills/*/SKILL.md, skills/*/SKILL.md

8. Reviewer-owned quality-gate readiness
   -> scripts/quality-gate, docs/quality-pipeline.md, composer scripts,
      PHPStan/Pint/test/jscpd/Deptrac/audit configuration and baselines
```

Also inspect existing `agent-context/` docs before writing. Preserve useful content and update it in place.

### Phase 2: Architecture Mapping

From the reconnaissance data, identify:

**Tech Stack**
- Language(s) and version constraints.
- Framework(s) and major libraries.
- Database(s) and ORMs.
- Build tools and bundlers.
- CI/CD platform.

**Architecture Pattern**
- Monolith, monorepo, microservices, or serverless.
- Frontend/backend split or full-stack.
- API style: REST, GraphQL, gRPC, tRPC.

**Key Directories**
Map the top-level directories to their purpose:

```text
src/components/  -> React UI components
src/api/         -> API route handlers
src/lib/         -> Shared utilities
src/db/          -> Database models and migrations
tests/           -> Test suites
scripts/         -> Build and deployment scripts
```

**Data Flow**
Trace one request from entry to response:
- Where does a request enter? router, handler, controller.
- How is it validated? middleware, schemas, guards.
- Where is business logic? services, models, use cases.
- How does it reach the database? ORM, raw queries, repositories.

### Phase 3: Convention Detection

Identify patterns the codebase already follows:

**Naming Conventions**
- File naming: kebab-case, camelCase, PascalCase, snake_case.
- Component/class naming patterns.
- Test file naming: `*.test.ts`, `*.spec.ts`, `*_test.go`.

**Code Patterns**
- Error handling style: try/catch, Result types, error codes.
- Dependency injection or direct imports.
- State management approach.
- Async patterns: callbacks, promises, async/await, channels.

**Git Conventions**
- Branch naming from recent branches.
- Commit message style from recent commits.
- PR workflow: squash, merge, rebase.
- If the repo has no commits yet or only a shallow history, skip this section and note "Git history unavailable or too shallow to detect conventions".

**Skill Usage Guidance**
- Inventory project-local skills and shared skill sources.
- Deduplicate mirrored copies of the same skill by name.
- Capture each skill's trigger guidance from its frontmatter `description` and any concise "when to use" instructions.
- Note related project workflows from `AGENTS.md`, `CLAUDE.md`, or equivalent repo guidance when they determine which skill to use.
- If no project-local skills exist, still create `agent-context/skills.md` and state that no project-local skills were found.

### Phase 4: Activate The Laravel Quality Gate When Applicable

When the repository is confirmed as Laravel and contains `scripts/quality-gate`, follow `references/quality-gate.md` after architecture and testing discovery. Inventory the six stable `quality:*` contracts and measure current debt without accepting it when the tools already exist. Present one consolidated proposal when measurement is already possible; otherwise obtain setup approval before installing missing tools, then measure and obtain separate policy approval before writing rules, thresholds, baselines, or security policy.

After approval, configure the independent checks, run the full gate, parse its fresh manifest, and record each check as operational-pass, operational-fail, skipped, or pending-approval. Do not claim that the gate is active or green when any required check is skipped. Do not fix unrelated findings discovered during activation.

### Phase 5: Generate Agent Context Artifacts

Create or update structured docs inside `agent-context/`. Use the per-file references above for the exact structure.

| Source insight | Agent-context target |
| --- | --- |
| Overview and where to start | `agent-context/README.md` |
| Project-specific terms and ambiguity | `agent-context/domain.md` |
| Key directories and where to look | `agent-context/folder-structure.md` |
| Tech stack, architecture pattern, entry points, data flow | `agent-context/architecture.md` |
| Common tasks, build/run commands, git and review conventions | `agent-context/workflows.md` |
| Test stack, test locations, naming, verification commands | `agent-context/testing.md` |
| Project-local skills and when agents should use them | `agent-context/skills.md` |
| API style, endpoints, contracts | `agent-context/api.md` when evidence exists |
| Databases, schemas, migrations, seed data | `agent-context/data.md` when evidence exists |
| Deployment, runtime config, jobs, monitoring | `agent-context/operations.md` when evidence exists |
| Auth, secrets, sensitive data, compliance | `agent-context/security.md` when evidence exists |

The resulting docs should collectively cover the same information as the onboarding guide:

```markdown
# Onboarding Guide: [Project Name]

## Overview
[2-3 sentences: what this project does and who it serves]

## Tech Stack
| Layer | Technology | Version |
| --- | --- | --- |
| Language | TypeScript | 5.x |
| Framework | Next.js | 14.x |
| Database | PostgreSQL | 16 |
| ORM | Prisma | 5.x |
| Testing | Jest + Playwright | - |

## Architecture
[Diagram or description of how components connect]

## Key Entry Points
- **API routes**: `src/app/api/` - Next.js route handlers
- **UI pages**: `src/app/(dashboard)/` - authenticated pages
- **Database**: `prisma/schema.prisma` - data model source of truth
- **Config**: `next.config.ts` - build and runtime config

## Directory Map
[Top-level directory -> purpose mapping]

## Request Lifecycle
[Trace one API request from entry to response]

## Conventions
- [File naming pattern]
- [Error handling approach]
- [Testing patterns]
- [Git workflow]

## Common Tasks
- **Run dev server**: `npm run dev`
- **Run tests**: `npm test`
- **Run linter**: `npm run lint`
- **Database migrations**: `npx prisma migrate dev`
- **Build for production**: `npm run build`

## Skills Index
| Skill | Use when | Source |
| --- | --- | --- |
| `git-conventional-commit` | Creating or proposing Conventional Commit messages | `.agents/skills/git-conventional-commit/SKILL.md` |

## Where to Look
| I want to... | Look at... |
| --- | --- |
| Add an API endpoint | `src/app/api/` |
| Add a UI page | `src/app/(dashboard)/` |
| Add a database table | `prisma/schema.prisma` |
| Add a test | `tests/` matching the source path |
| Change build config | `next.config.ts` |
```

Do not print a standalone onboarding guide unless the user explicitly asks for one. Persist the durable version in `agent-context/`.

For an activated Laravel quality gate, `agent-context/workflows.md` must include its operational-status table, configuration and baseline paths, reviewer-owned command, and pending approvals. `agent-context/testing.md` must identify the authoritative test command used by `quality:test`.

## Best Practices

1. **Don't read everything** - reconnaissance should use `rg --files`, `rg`, and targeted file reads, not reading every file. Read selectively only for ambiguous signals.
2. **Verify, don't guess** - if a framework is detected from config but the actual code uses something different, trust the code.
3. **Respect existing `agent-context/` docs** - enhance them rather than replacing useful project-specific content. Call out major reorganizations in the final summary.
4. **Stay concise** - each context doc should be scannable. Details belong in code and references, not duplicated in prose.
5. **Flag unknowns** - if a convention cannot be confidently detected, say so rather than guessing. "Could not determine test runner" is better than a wrong answer.
6. **Separate discovery from policy** - measurements and proposals may be produced during onboarding, but architecture rules, thresholds, baselines, and security ignores require explicit approval before they become repository policy.

## Anti-Patterns to Avoid

- Updating `CLAUDE.md` from this skill.
- Listing every dependency - highlight only the ones that shape how agents should work.
- Describing obvious directory names - `src/` does not need an explanation unless this repo gives it a specific role.
- Copying the README - `agent-context/` docs add structural insight the README lacks.
- Writing one giant onboarding document when the information belongs in separate `agent-context/` files.
- Treating a skipped quality-gate check as operational or silently baselining existing findings to make the gate green.

## Examples

### Example 1: First time in a new repo
**User**: "Onboard me to this codebase"
**Action**: Run the full 5-phase workflow, activate an applicable provisioned Laravel gate after approval, then create or update the standard `agent-context/` docs.
**Output**: `agent-context/README.md`, `domain.md`, `folder-structure.md`, `architecture.md`, `workflows.md`, `testing.md`, and `skills.md`, plus optional docs when evidence exists.

### Example 2: Fill agent-context for an existing project
**User**: "Fill agent-context for this project"
**Action**: Run Phases 1-3, activate an applicable provisioned Laravel gate through Phase 4 after approval, read existing `agent-context/` docs, then update each file using its matching reference.
**Output**: Updated `agent-context/` docs with detected conventions, skill usage guidance, quality-gate operational status when applicable, and open questions.

### Example 3: Refresh project conventions
**User**: "Update the project context with current conventions"
**Action**: Run convention detection, update `folder-structure.md`, `workflows.md`, and `testing.md`; update other docs only when evidence changed.
**Output**: Focused `agent-context/` updates, with unchanged docs left alone.
