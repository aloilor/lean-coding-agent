---
name: engineering-standards
description: Apply this skill to every task that writes, generates, changes, refactors, debugs, or reviews code, including production code, tests, scripts, migrations, examples, and executable configuration. Use it for every code-level design decision to enforce clear contracts, cohesive responsibilities, controlled coupling and complexity, appropriate object design, naming, documentation, and maintainability.
---

# Engineering Standards

Reusable, cross-project baseline for code and code-level design. Apply it to every code change, proportionate to the change's scope and risk; even a trivial edit must satisfy the relevant rules. Use this skill for engineering judgment about the code.

## Always Apply

- Make behavior and contracts clear through names, types, structure, and focused tests.
- Keep functions, modules, classes, APIs, and tests cohesive around one responsibility or invariant.
- Minimize unnecessary concepts, branches, state, dependencies, and hidden coupling.
- Introduce abstractions and extension points only for a concrete shared concept, boundary, or variation.
- Remove duplication only when it represents the same stable concept or business rule.
- Document public contracts, constraints, side effects, edge cases, and failure modes; avoid comments that narrate obvious code.
- When objects are involved, keep responsibilities cohesive, encapsulate state and behavior, protect invariants, and prefer composition over inheritance.

## Apply The Skill

1. **Identify the code decision.** Name the behavior or contract involved, the unit that should own it, and any invariant, side effect, or failure mode that constrains the design.
2. **Name the concrete design pressure.** Look for unclear intent, independent reasons to change, hidden side effects, repeated business knowledge, excessive branching or state, reach-through coupling, or dependence on volatile details. Do not restructure code because of size, personal preference, or a smell label alone.
3. **Load only relevant guidance.** Use the routing table below, then open a detail file only when the decision remains unclear.
4. **Choose the smallest justified code shape.** Prefer a direct implementation while the behavior is local and stable. Extract a function, object, interface, or pattern only when it gives a shared concept, invariant, boundary, or recurring variation a clear owner.
5. **Evaluate the resulting code before completion.** Re-read the changed code or diff. Confirm that names expose intent, responsibilities remain cohesive, dependencies and side effects are visible, repeated business rules have one owner, and the change did not introduce unused flexibility or indirection. Run applicable deterministic checks; use this review for semantic design concerns those checks cannot judge.
6. **Handle red flags explicitly.** Remove each in-scope red flag or justify it with a current requirement, invariant, external boundary, or demonstrated variation. If it cannot be justified concretely, simplify the design.

For implementation and refactoring, use these steps to guide code-shape decisions while following the applicable workflow for scope and verification. For review, report a standards issue only when you can cite the concrete code, the maintenance or correctness risk, and the smallest responsible correction; do not report taste as a defect.

## References

| Current Decision | Read |
| --- | --- |
| Naming, functions, control flow, comments, documentation, duplication, smells, or complexity | `references/clean-code/RULES.md` |
| Object responsibilities, invariants, collaboration, inheritance, polymorphism, SOLID, patterns, or domain modeling | `references/object-oriented-design/RULES.md` |
| No concrete design pressure beyond the core rules | Do not load a detail reference. |

Open detail files only when their examples or deeper questions are directly useful. Do not load the whole `references/` folder by default.

## Red Flags

- A new abstraction exists before a stable shared concept exists.
- A change adds flexibility for a hypothetical future.
- Code reaches through another object's internals instead of asking for behavior.

Treat these as decisions that require correction or concrete justification, not as automatic rewrite commands. Prefer a little local duplication over the wrong abstraction. Let structure earn its place.
