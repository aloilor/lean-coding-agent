---
name: engineering-standards
description: Use this skill when writing code, implementing features, refactoring, planning architecture, designing systems, reviewing code, debugging, or making design decisions. Always apply this repo's shared engineering baseline for clean code, object-oriented design, SOLID, DRY, YAGNI, KISS, naming, documentation, simple design, and maintainability.
---

# Engineering Standards

Reusable, cross-project engineering baseline for code that is simple, maintainable, well named, verified, and documented where callers need it. Keep project-specific facts in `agent-context/`.

## Always Apply

- Prefer the simplest responsible design that satisfies the request.
- Use names, structure, and tests that make behavior easy to understand and change.
- Keep functions, modules, classes, APIs, and tests focused on one clear responsibility.
- Avoid speculative features, extension points, abstractions, and just-in-case error handling.
- Remove duplication only when it represents the same stable concept or business rule.
- Document public contracts, constraints, side effects, edge cases, and failure modes; avoid comments that narrate obvious code.
- When objects are involved, keep responsibilities cohesive, encapsulate state and behavior, protect invariants, and prefer composition over inheritance.

## Decision Checklist

- **Before:** What behavior is changing, and how will I verify it?
- **During:** Is this still the simplest thing that works without creating an obvious future trap?
- **After:** Do relevant checks pass, did my change create unused code, and would another developer understand this later?

## Optional References

Read only the references needed for the current task:

- `references/clean-code/RULES.md` - routing map for naming, functions, comments, documentation, duplication, smells, and complexity.
- `references/object-oriented-design/RULES.md` - routing map for object responsibilities, SOLID, inheritance, polymorphism, patterns, and domain modeling.

Open detail files only when their examples or deeper questions are directly useful. Do not load the whole `references/` folder by default.

## Red Flags

- The behavior or verification plan is unclear.
- A new abstraction exists before a stable shared concept exists.
- A change adds flexibility for a hypothetical future.
- Code reaches through another object's internals instead of asking for behavior.
- A cleanup is unrelated to the requested change or lacks verification.

Prefer a little local duplication over the wrong abstraction. Let structure earn its place.
