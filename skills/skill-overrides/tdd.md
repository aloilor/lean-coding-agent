# tdd override

This override extends the upstream `tdd` skill. When this file conflicts with the skill's default behavior, follow this file.

## Scope

Use `tdd` as the implementation driver for feature work, bug fixes, and any request that mentions test-first, red-green-refactor, regression coverage, or integration tests. This override also carries this repo's test-strategy guidance — test level, repo conventions, fixtures, doubles, reliability, testable design, and final review — so apply it whenever you plan, write, or review tests, including non-TDD review and refactor work where the red-green loop does not run.

## When To Add Or Update Tests

Create or update tests when behavior changes, a bug needs reproduction before its fix, a refactor touches meaningful logic or contracts, or the change affects validation, authorization, persistence, external integrations, or user-visible workflows. Skip new tests only when existing coverage already proves the changed behavior and the risk is low. Start from risk: prioritize behavior that would hurt users, money, data, security, or operations if it broke.

## Before RED

- Read `agent-context/testing.md` first when it exists.
- Inspect the repo to confirm the test framework, runner, focused test command, file layout, naming convention, assertion style, fixtures, builders, factories, and mocking approach.
- Match the existing setup. Do not introduce a new framework, layout, naming pattern, or helper style unless the task explicitly requires it.
- Reuse existing builders, factories, fixtures, and test helpers before creating new ones.
- Pick the smallest useful test for the risk. Prefer lower-level tests when they prove the behavior clearly; use broader integration, contract, E2E, or acceptance tests when the risk lives in wiring, persistence, routing, permissions, browser behavior, external integration, or a user workflow.

## RED

- Write exactly one focused behavior test for the next vertical slice.
- Name the test as a concrete behavior, not an implementation detail.
- Structure the test with Arrange, Act, Assert when the framework style allows it.
- Run the focused test before implementation and confirm it fails for the intended assertion. Compile errors, import errors, missing symbols, setup errors, and typos are broken tests, not a valid RED.
- If the test passes immediately, stop and investigate. The behavior may already exist, the test may assert the wrong thing, or the assertion may be too weak.

## GREEN

- Make the test pass by changing production code, not by weakening the test.
- Never loosen assertions, delete cases, skip tests, mark tests pending, broaden expected values to match the actual result, or swallow failures just to get green.
- Change the test only when the test is genuinely wrong. State why the expectation is wrong before changing it.
- Default to the obvious implementation. Use a fake or hardcoded value only when it is an intentional intermediate step and the next test will force generalization.
- Add no speculative behavior beyond what the current failing test requires.

## Test Quality

- Test observable behavior through public interfaces.
- Do not test private methods, internal call order, or internal collaborators.
- Do not mock code the project owns unless the interaction itself is the public contract.
- Mock at system boundaries only: external APIs, time, randomness, file systems, and sometimes databases. Prefer a test database or a working fake when that gives clearer confidence.
- Know the double you use: dummy (unused argument), stub (canned return), spy (records calls), mock (asserts interactions), fake (working in-memory implementation). Prefer a fake or the real object over a mock when it gives clearer confidence.
- Reuse existing builders, factories, fixtures, and contract tests before writing new ones. Prefer a shared builder over ad-hoc setup, and use contract tests to prove multiple implementations satisfy the same interface.
- Expected values must come from an independent source of truth: a literal example, a worked example, a documented contract, or the spec. Do not recompute the expected value with the same logic as the implementation.

## Make Hard-To-Test Code Testable

Hard-to-test code is a design signal, not a reason to skip the test. When behavior is buried in a side effect or a hidden dependency, create a seam and test through it:

- Inject dependencies (clock, database, HTTP, mailer, randomness) instead of constructing them inside the unit, so tests can pass fakes.
- Return a value instead of only performing an effect.
- Surface the effect through an injected collaborator you can spy on, or an observable result or event.
- Separate decision from action: unit-test the logic as a pure function, keep a thin I/O wrapper for a small integration test.

Prefer building the seam over testing private internals, monkeypatching globals, or scraping logs. If you genuinely cannot make it testable within the task's scope, flag it — do not silently drop the test.

## Reliability

- Isolate mutated state: databases, queues, caches, files, module globals, and shared records.
- Control time with an injected clock. Cover time zones, expiry windows, and clock skew when relevant.
- Control randomness with fixed seeds when randomness affects behavior.
- Wait on observable conditions or events, not fixed sleeps.
- Keep tests parallel-safe by avoiding shared ports, accounts, filenames, and named records.
- Use realistic synthetic data with edge cases, but do not use production personal data.

## Refactor

- Refactor only while tests are green.
- Run the focused test after each meaningful refactor step.
- Extract duplication when the pattern is clear; do not create premature abstractions.
- Keep tests stable across internal refactors. If a test breaks after a behavior-preserving refactor, the test was probably coupled to implementation details.

## Final Checklist

- The failing test was observed red for the intended assertion before implementation.
- The implementation moved in vertical slices: one test, one implementation, repeat.
- The tests match the repo's framework, layout, naming, fixtures, and runner.
- The tests assert observable behavior through public interfaces.
- The test level matches the risk.
- The tests are deterministic, isolated, and parallel-safe.
- Green was reached by fixing production code, not weakening tests.
- Relevant focused and broader verification commands pass.
