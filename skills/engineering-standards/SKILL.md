---
name: engineering-standards
description: Apply this repo's shared engineering baseline when writing code, implementing features, fixing bugs, refactoring, debugging, reviewing code, designing REST APIs, planning architecture, or making object/system design decisions. Use it to load only the relevant coding-style, clean-code, object-oriented design, complexity, code-smell, and REST API references from the bundled references folder.
---

# Engineering Standards

Use this skill as the enforcement layer for reusable engineering rules. Keep project-specific facts in `agent-context/`; use this skill for cross-project coding, design, API, refactoring, debugging, and review guidance.

## Loading Rule

Read only what the current task needs:

- General code work: start with `references/coding-style/RULES.md` and `references/clean-code/RULES.md`.
- Naming, functions, comments, docs, duplication, or object calisthenics: open the matching file inside `references/clean-code/`.
- Object responsibilities, SOLID, inheritance, polymorphism, or design patterns: start with `references/object-oriented-design/RULES.md`, then open the specific object-design reference.
- Complexity or refactoring risk: start with `references/code-quality/RULES.md`, then open complexity or code-smell details as needed.
- REST API work: start with `references/rest-api-design/RULES.md`, then open only the relevant REST API topic file.

Do not load the entire references folder by default.

## Core Behavior

- Prefer local project conventions over this shared baseline.
- Treat detailed references as review prompts, not hard lint rules.
- Prefer the simplest correct implementation that satisfies the current requirement.
- Keep changes focused; avoid speculative abstractions and unrelated cleanup.
- Use examples from references only when they clarify the current decision.
- Relax a guideline when enforcing it would make the code less idiomatic, more ceremonial, or harder to maintain.

## Before Coding

Check:

- What behavior needs to change?
- What is the smallest safe implementation?
- What tests, checks, or review steps will verify it?
- Which local project rule, stack convention, or shared reference applies?

## While Coding

Check:

- Are names clear and domain-specific?
- Is the main control flow easy to scan?
- Is duplication real behavior duplication, not merely similar syntax?
- Are edge cases and failure modes handled where callers need to recover, retry, validate, or avoid data loss?
- Are abstractions solving current complexity instead of hypothetical future needs?

## For Reviews

Prioritize issues that can cause bugs, regressions, maintainability risk, unclear contracts, poor testability, or avoidable complexity. Cite the relevant reference only when it makes the review more actionable.

## Reference Map

- `references/coding-style/RULES.md`: top-level coding-style routing.
- `references/clean-code/RULES.md`: clean-code checklist and focused clean-code links.
- `references/clean-code/naming-and-clarity.md`
- `references/clean-code/functions-and-control-flow.md`
- `references/clean-code/inline-comments.md`
- `references/clean-code/code-documentation.md`
- `references/clean-code/duplication-and-refactoring.md`
- `references/clean-code/object-calisthenics.md`
- `references/object-oriented-design/RULES.md`: object-design routing.
- `references/object-oriented-design/object-oriented-design.md`
- `references/object-oriented-design/solid-principles.md`
- `references/object-oriented-design/design-patterns.md`
- `references/code-quality/RULES.md`: complexity and code-smell routing.
- `references/code-quality/complexity.md`
- `references/code-quality/code-smells.md`
- `references/rest-api-design/RULES.md`: REST API routing.
- `references/rest-api-design/resource-modeling.md`
- `references/rest-api-design/http-semantics.md`
- `references/rest-api-design/validation-and-errors.md`
- `references/rest-api-design/querying-and-responses.md`
- `references/rest-api-design/versioning-and-security.md`
- `references/rest-api-design/documentation-and-operations.md`
