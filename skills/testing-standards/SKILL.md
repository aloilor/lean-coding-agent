---
name: testing-standards
description: Use this skill when planning, writing, reviewing, or updating tests; choosing between unit, integration, end-to-end, acceptance, regression, characterization, or contract tests; deciding what behavior needs test coverage; naming tests; structuring tests with Arrange-Act-Assert; diagnosing or preventing flaky, order-dependent, or non-deterministic tests; or adding tests for bugs, risky changes, validation, refactors, and feature work. Applies this repo's shared testing standards for useful, behavior-focused, reliable, maintainable tests.
---

# Testing Standards

Use testing to make behavior cheap to change, safe to refactor, and clear to future maintainers.

Use this skill for test strategy and test shape. When the task calls for a test-first red-green-refactor workflow, follow `references/tdd.md`.

The principles here are language-agnostic. Examples use TypeScript/Jest to illustrate; adapt them to your stack's idioms (naming, framework, assertion style).

## Match The Repo's Existing Test Setup

Before writing any test, discover the project's existing testing setup and mirror it. Do not introduce a new framework, directory layout, or naming convention into a repo that already has one.

1. **Check `agent-context/testing.md` first.** It records this project's test commands, expectations, and fixture conventions. Treat it as the source of truth when present.
2. **Then inspect the repo** to confirm and fill gaps. Identify:
   - The test framework and runner, and the exact command to run tests.
   - Where tests live and how files are named (e.g., `*.test.ts`, `*_test.go`, `tests/`).
   - The assertion style and the mocking/fixture approach already in use.
   - Existing builders, factories, fixtures, and helpers — reuse them instead of inventing new ones.
3. **Match what you find.** Put new tests where the existing ones live, name them the way the repo does, and use the established assertion and double styles.

Only introduce a new framework or convention when the task explicitly calls for it. If the repo has no test setup at all, propose the smallest reasonable one and flag it rather than assuming.

See: `references/RULES.md` (Match The Repo's Existing Test Setup) and `references/testing.md` (Match The Repo's Existing Test Setup).

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

## Make Hard-To-Test Code Testable

Hard-to-test code is a design signal, not a reason to skip the test. When behavior is buried in a side effect or a hidden dependency, create a seam and test through it:

- **Inject dependencies** (clock, database, HTTP, mailer, randomness) instead of constructing them inside the unit, so tests can pass fakes.
- **Return a value** instead of only performing an effect.
- **Surface the effect** through an injected collaborator you can spy on, or an observable result/event.
- **Separate decision from action:** unit-test the logic as a pure function, keep a thin I/O wrapper for a small integration test.

Make it testable rather than asserting on private internals, monkeypatching globals, or scraping logs. If you truly cannot within the task's scope, flag it — don't silently drop the test.

See: `references/RULES.md` (Make Hard-To-Test Code Testable) and `references/testing.md` (Make Hard-To-Test Code Testable).

## Deeper References

Start from the compact rule index, then open detail files only when the task needs examples or deeper guidance:

- `references/RULES.md` — the full rule index covering test strategy, test doubles, reliability, and TDD, each row pointing to its detail file.
- `references/testing.md` for the testing pyramid, test-double taxonomy (dummy/stub/spy/mock/fake), per-layer strategy, contract tests, test builders, and reliability/determinism detail.
- `references/tdd.md` for the red-green-refactor loop, the Three Laws, Rule of Three, triangulation, and simpler-transformation guidance.

## Review Checklist

Before finishing testing work, check:

1. Did you run the test and watch it fail on the assertion (not a compile/import error) before writing the production code?
2. Does the test fail for the bug or missing behavior it is meant to guard?
3. Does the test assert observable behavior instead of implementation details?
4. Is the test level appropriate for the risk?
5. Is the test deterministic and isolated (no shared state, wall-clock time, unseeded randomness, or fixed sleeps)?
6. Is setup clear and minimal?
7. Does the name explain the scenario and expected result?
8. Did you reach green by fixing the code rather than weakening, skipping, or deleting the test?
9. Do relevant test commands pass?
