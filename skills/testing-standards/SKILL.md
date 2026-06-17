---
name: testing-standards
description: Use this skill when planning, writing, reviewing, or updating tests; choosing between unit, integration, end-to-end, acceptance, regression, characterization, or contract tests; deciding what behavior needs test coverage; naming tests; structuring tests with Arrange-Act-Assert; diagnosing or preventing flaky, order-dependent, or non-deterministic tests; or adding tests for bugs, risky changes, validation, refactors, and feature work. Applies this repo's shared testing standards for useful, behavior-focused, reliable, maintainable tests.
---

# Testing Standards

Use testing to make behavior cheap to change, safe to refactor, and clear to future maintainers.

Use this skill for test strategy and test shape. When the task calls for a test-first red-green-refactor workflow, follow `references/tdd.md`.

The principles here are language-agnostic. Examples use TypeScript/Jest to illustrate; adapt them to your stack's idioms (naming, framework, assertion style).

## Choose The Right Test

Start from risk: prioritize behavior that would hurt users, money, data, security, or operations if it broke. Then pick the smallest test that gives useful confidence:

1. **Unit tests** - single class/function, fast, isolated.
2. **Integration tests** - multiple components together.
3. **E2E/acceptance tests** - full system, user perspective.

Prefer lower-level tests when they prove the behavior clearly. Use broader tests when the risk is in integration, wiring, framework behavior, permissions, routing, browser behavior, or the user workflow.

See: `references/RULES.md` (Test Strategy Rules) and `references/testing.md` (testing pyramid, test types, per-layer strategy).

## When To Add Or Update Tests

Create or update tests when:

- Behavior changes.
- A bug needs reproduction before the fix.
- A refactor touches meaningful logic or contracts.
- The change affects validation, authorization, persistence, external integrations, or user-visible workflows.
- The risk is meaningful enough that manual inspection is a poor safety net.

Skip new tests when existing coverage already proves the changed behavior and the risk is low.

See: `references/RULES.md` (Start From Risk, Test Strategy Rules).

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

This Arrange-Act-Assert structure is the canonical reference for the detail files; `references/testing.md` and `references/tdd.md` build on it.

## Name Tests With Concrete Behavior

Use concrete examples, not abstract statements.

```typescript
// Avoid: "can add numbers"
// Prefer: "when adding 2 + 3, returns 5"
```

Name the scenario, action, and expected result when the framework style allows it. In xUnit-style frameworks that prefer identifiers, a snake_case or camelCase name carries the same intent: `returns_validation_error_when_quantity_is_negative`.

See: `references/RULES.md` (Write A Concrete Failing Test First) and `references/tdd.md` (RED phase).

## Keep Tests Reliable

A test that fails intermittently is worse than no test: it trains people to ignore failures. Make every test deterministic and isolated.

- **Isolate state.** Reset databases, queues, caches, and files between tests that mutate shared state. Prefer unique IDs, transactions, or disposable resources over shared named records. No test should depend on another test having run first.
- **Control time.** Inject a clock instead of reading the system time deep inside logic. Test time zones, expiry windows, and clock skew when they affect behavior.
- **Control randomness.** Fix seeds when randomness is part of the behavior under test.
- **Don't sleep.** In async and end-to-end tests, wait on a condition or event, never an arbitrary timeout. Fixed sleeps are the most common source of flake.
- **Run in parallel safely.** Avoid shared ports, accounts, filenames, or records so the suite can parallelize.
- **Use safe data.** Fixtures should resemble real input (shapes, limits, encodings, edge cases) without using production personal data.

See: `references/RULES.md` (Reliability Rules) and `references/testing.md` (Reliability and Determinism — isolation, fakes, and test data).

## Deeper References

Start from the compact rule index, then open detail files only when the task needs examples or deeper guidance:

- `references/RULES.md` — the full rule index covering test strategy, test doubles, reliability, and TDD, each row pointing to its detail file.
- `references/testing.md` for the testing pyramid, test-double taxonomy (dummy/stub/spy/mock/fake), per-layer strategy, contract tests, test builders, and reliability/determinism detail.
- `references/tdd.md` for the red-green-refactor loop, the Three Laws, Rule of Three, triangulation, and simpler-transformation guidance.

## Review Checklist

Before finishing testing work, check:

1. Does the test fail for the bug or missing behavior it is meant to guard?
2. Does the test assert observable behavior instead of implementation details?
3. Is the test level appropriate for the risk?
4. Is the test deterministic and isolated (no shared state, wall-clock time, unseeded randomness, or fixed sleeps)?
5. Is setup clear and minimal?
6. Does the name explain the scenario and expected result?
7. Do relevant test commands pass?
