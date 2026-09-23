---
name: engineering-standards
description: Apply this skill to every task that writes, generates, changes, fixes, refactors, debugs, or reviews code, including production code, tests, scripts, migrations, examples, and executable configuration. Use it for every code-level design decision to enforce a language-neutral baseline for correctness, safety, compatibility, clear contracts, controlled complexity, and maintainability.
---

# Engineering Standards

Apply this semantic quality baseline to every code change, proportionate to scope and risk. Use it with the applicable workflow and repository checks; never substitute prose review for deterministic evidence.

## Precedence And Scope

- Preserve approved requirements, correctness, security, data integrity, and public compatibility before optimizing code shape.
- Follow explicit project rules and repository-enforced tooling, then language and framework contracts. Apply this baseline over inconsistent nearby style or precedent.
- Read project context before changing architecture, domain rules, persistence, integrations, or operational behavior.
- Do not hand-edit generated or vendored code unless the task explicitly requires it and the source of truth cannot be changed.

## Non-Negotiable Gate

- Preserve existing behavior and public contracts unless an approved requirement changes them; make migrations and compatibility consequences explicit.
- Validate untrusted input at trust boundaries. Make failure behavior, side effects, state transitions, resource ownership, and transactional boundaries visible where they matter.
- Express intent through names, types, contracts, and cohesive units with one clear reason to change.
- Choose the smallest justified design. Avoid unnecessary concepts, branches, state, dependencies, indirection, configurability, and extension points.
- Give each stable rule, invariant, or policy one authoritative owner. Allow repeated boundary validation when it independently protects a boundary.
- Document caller-relevant constraints, side effects, and failure modes that names and types cannot express; do not narrate obvious code.
- Encapsulate state when mutation could break an invariant. Prefer composition unless inheritance is required by a stable subtype or framework contract.

## Apply The Gate

1. **Understand.** Read the complete changed unit, relevant callers, tests, and contracts. Name the required behavior, trust boundaries, invariants, side effects, failure modes, and compatibility constraints.
2. **Route And Design.** For every code decision, find every matching row in the References table and open each linked file before finalizing the design. Apply that guidance with the core gate; if no row matches, use the core gate alone. Then choose the smallest project-compatible shape that gives each current responsibility, rule, effect, or external boundary a clear owner. Do not load unrelated references or add an abstraction or dependency unless it removes more risk or complexity than it adds.
3. **Verify.** Re-read the complete changed units and diff, inspect affected callers and documentation, run the repository's applicable deterministic checks, and record exact results or explicit limitations.

## Completion Gate

- Require both semantic review and deterministic evidence; neither replaces the other.
- Do not complete work with an unresolved in-scope correctness, security, data-integrity, compatibility, contract, or required verification failure.
- For review findings, cite the concrete code, trigger, risk, and smallest responsible correction. Do not report taste, raw size, or a smell label as a defect.

## Companion Skills

| Decision | Also Use |
| --- | --- |
| Behavioral implementation, regression fixes, test design, or verification | `$tdd` |
| Behavior-preserving restructuring | `$refactor` |
| HTTP resource and API contract changes | `$rest-api-design` |
| Database correctness, access control, or material query performance | `$sql-code-review` and, when performance matters, `$sql-optimization` |

## References

Use this table during **Route And Design**. Open and apply every matched detail file before finalizing the decision.

| Decision | Read |
| --- | --- |
| Naming and intent | [Naming And Clarity](references/clean-code/naming-and-clarity.md) |
| Functions and control flow | [Functions And Control Flow](references/clean-code/functions-and-control-flow.md) |
| Inline comments | [Inline Comments](references/clean-code/inline-comments.md) |
| Caller-facing documentation | [Code Documentation](references/clean-code/code-documentation.md) |
| Duplication and safe refactoring | [Duplication And Refactoring](references/clean-code/duplication-and-refactoring.md) |
| Complexity and technical debt | [Managing Complexity](references/clean-code/complexity.md) |
| Smell diagnosis | [Code Smells](references/clean-code/code-smells.md) |
| Object responsibilities, invariants, collaboration, inheritance, polymorphism, or domain modeling | [Object-Oriented Design](references/object-oriented-design/object-oriented-design.md) |
| SOLID contract questions | [SOLID Principles](references/object-oriented-design/solid-principles.md) |
| Pattern selection after demonstrated design pressure | [Design Patterns](references/object-oriented-design/design-patterns.md) |
