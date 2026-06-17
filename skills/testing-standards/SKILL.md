---
name: testing-standards
description: Use this skill when planning, writing, reviewing, or updating tests; choosing between unit, integration, end-to-end, acceptance, regression, characterization, or contract tests; deciding what behavior needs test coverage; naming tests; structuring tests with Arrange-Act-Assert; or adding tests for bugs, risky changes, validation, refactors, and feature work. Applies this repo's shared testing standards for useful, behavior-focused, maintainable tests.
---

# Testing Standards

Use testing to make behavior cheap to change, safe to refactor, and clear to future maintainers.

Use this skill for test strategy and test shape. When the task calls for a test-first red-green-refactor workflow, follow `references/tdd.md`.

## Choose The Right Test

Pick the smallest test that gives useful confidence:

1. **Unit tests** - single class/function, fast, isolated.
2. **Integration tests** - multiple components together.
3. **E2E/acceptance tests** - full system, user perspective.

Prefer lower-level tests when they prove the behavior clearly. Use broader tests when the risk is in integration, wiring, framework behavior, permissions, routing, browser behavior, or the user workflow.

## When To Add Or Update Tests

Create or update tests when:

- Behavior changes.
- A bug needs reproduction before the fix.
- A refactor touches meaningful logic or contracts.
- The change affects validation, authorization, persistence, external integrations, or user-visible workflows.
- The risk is meaningful enough that manual inspection is a poor safety net.

Skip new tests when existing coverage already proves the changed behavior and the risk is low.

## Structure Tests Clearly

Use Arrange-Act-Assert:

```typescript
// Arrange - set up test state
const calculator = new Calculator();

// Act - execute the behavior
const result = calculator.add(2, 3);

// Assert - verify the outcome
expect(result).toBe(5);
```

Keep tests readable as examples of behavior. Avoid hiding important setup behind vague helpers.

## Name Tests With Concrete Behavior

Use concrete examples, not abstract statements.

```typescript
// Avoid: "can add numbers"
// Prefer: "when adding 2 + 3, returns 5"
```

Name the scenario, action, and expected result when the framework style allows it.

## Deeper References

Open these only when the task needs more detail than the guidance above:

- `references/testing.md` for the testing pyramid, test-double taxonomy (dummy/stub/spy/mock/fake), per-layer strategy, contract tests, and test builders.
- `references/tdd.md` for the red-green-refactor loop, the Three Laws, Rule of Three, triangulation, and the transformation priority premise.

## Review Checklist

Before finishing testing work, check:

1. Does the test fail for the bug or missing behavior it is meant to guard?
2. Does the test assert observable behavior instead of implementation details?
3. Is the test level appropriate for the risk?
4. Is setup clear and minimal?
5. Does the name explain the scenario and expected result?
6. Do relevant test commands pass?
