---
name: engineering-standards
description: Use this skill when writing, changing, refactoring, or reviewing production or test code, and when making code-level design decisions. Apply this repo's shared baseline for clear contracts, cohesive responsibilities, controlled coupling and complexity, appropriate object design, naming, documentation, and maintainability.
---

# Engineering Standards

Reusable, cross-project baseline for code and code-level design. Follow `AGENTS.md` and the applicable workflow skills for task scope, execution process, and verification requirements; use this skill for engineering judgment about the code itself. Keep project-specific facts in `agent-context/`.

## Always Apply

- Make behavior and contracts clear through names, types, structure, and focused tests.
- Keep functions, modules, classes, APIs, and tests cohesive around one responsibility or invariant.
- Minimize unnecessary concepts, branches, state, dependencies, and hidden coupling.
- Introduce abstractions and extension points only for a concrete shared concept, boundary, or variation.
- Remove duplication only when it represents the same stable concept or business rule.
- Document public contracts, constraints, side effects, edge cases, and failure modes; avoid comments that narrate obvious code.
- When objects are involved, keep responsibilities cohesive, encapsulate state and behavior, protect invariants, and prefer composition over inheritance.

## Optional References

Read only the references needed for the current task:

- `references/clean-code/RULES.md` - routing map for naming, functions, comments, documentation, duplication, smells, and complexity.
- `references/object-oriented-design/RULES.md` - routing map for object responsibilities, SOLID, inheritance, polymorphism, patterns, and domain modeling.

Open detail files only when their examples or deeper questions are directly useful. Do not load the whole `references/` folder by default.

## Red Flags

- A new abstraction exists before a stable shared concept exists.
- A change adds flexibility for a hypothetical future.
- Code reaches through another object's internals instead of asking for behavior.

Prefer a little local duplication over the wrong abstraction. Let structure earn its place.
