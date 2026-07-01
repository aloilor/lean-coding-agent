# tdd override

This override extends the upstream `tdd` skill. When this file conflicts with the skill's default behavior, follow this file.

## Scope

Use `tdd` as the implementation driver for feature work, bug fixes, and any request that mentions test-first, red-green-refactor, regression coverage, or integration tests. Use `testing-standards` as supporting guidance for test level, repo conventions, fixtures, doubles, reliability, and final review.

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
- Expected values must come from an independent source of truth: a literal example, a worked example, a documented contract, or the spec. Do not recompute the expected value with the same logic as the implementation.

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
