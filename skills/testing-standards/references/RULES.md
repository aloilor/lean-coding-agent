# Testing Rules

Load this file when planning, writing, reviewing, or updating tests. Open the detail files only when the current task needs examples or deeper guidance.

## Test Strategy Rules

| Rule | Summary | Details |
|------|---------|---------|
| Match The Repo's Existing Test Setup | Before writing tests, discover the framework, run command, file layout, naming, and fixtures (check `agent-context/testing.md` first, then the repo) and mirror them. | [testing.md](./testing.md) |
| Choose The Smallest Useful Test | Prefer lower-level tests; use broader tests only when the risk lives in integration, wiring, framework behavior, or user workflows. | [testing.md](./testing.md) |
| Follow The Testing Pyramid | Many fast unit tests, some integration and contract tests, few brittle end-to-end tests. | [testing.md](./testing.md) |
| Start From Risk | Prioritize behavior that would hurt users, money, data, security, or operations if it broke. | [testing.md](./testing.md) |
| Write Isolated Unit Tests | Test one class or function with no real external dependencies, and keep them fast. | [testing.md](./testing.md) |
| Use Integration Tests At Boundaries | Test multiple components together where systems meet, with real dependencies when that is the risk. | [testing.md](./testing.md) |
| Reserve E2E Tests For Critical Paths | Exercise the full system from the user's perspective only for the few journeys that need it. | [testing.md](./testing.md) |
| Match Test Strategy To The Layer | Domain: unit tests, no mocks. Application: orchestration with fakes. Infrastructure: real dependencies. | [testing.md](./testing.md) |
| Focus Integration Tests On High Value | Cover boundaries, critical paths such as money and security, and complex queries. | [testing.md](./testing.md) |
| Use Contract Tests Across Implementations | Run one shared test suite against every implementation of an interface. | [testing.md](./testing.md) |
| Build Test Objects With Builders | Use builders to construct test data clearly without exposing irrelevant setup. | [testing.md](./testing.md) |
| Make Hard-To-Test Code Testable | Treat hard-to-test behavior as a design signal: inject dependencies, return values, surface effects, and separate decision from action instead of skipping the test. | [testing.md](./testing.md) |
| Avoid Common Testing Mistakes | Do not test implementation, over-mock, share state, skip assertions, or test trivia. | [testing.md](./testing.md) |

## Test Double Rules

| Rule | Summary | Details |
|------|---------|---------|
| Use A Dummy For Unused Arguments | Pass a placeholder object only to satisfy a signature. | [testing.md](./testing.md) |
| Use A Stub For Canned Answers | Return predefined values to drive the code under test. | [testing.md](./testing.md) |
| Use A Spy To Record Calls | Capture how a collaborator was called, then assert on it afterward. | [testing.md](./testing.md) |
| Use A Mock To Verify Interactions | Assert the expected calls happened when the interaction itself is the contract. | [testing.md](./testing.md) |
| Prefer Fakes Over Deep Mocks | Use a working in-memory implementation when it makes the test clearer than mock setups. | [testing.md](./testing.md) |

## Reliability Rules

| Rule | Summary | Details |
|------|---------|---------|
| Isolate Test State | Reset shared databases, queues, caches, and files; never depend on test ordering. | [testing.md](./testing.md) |
| Control Time | Inject a clock instead of reading wall-clock time inside business logic. | [testing.md](./testing.md) |
| Control Randomness | Fix the seed when randomness is part of the behavior under test. | [testing.md](./testing.md) |
| Wait On Conditions, Not Sleeps | Replace fixed sleeps with waits on the expected state or event. | [testing.md](./testing.md) |
| Keep Tests Parallel-Safe | Avoid shared ports, accounts, filenames, or named records. | [testing.md](./testing.md) |
| Use Safe, Realistic Data | Match production shapes and edge cases without using real personal data. | [testing.md](./testing.md) |

## TDD Rules

| Rule | Summary | Details |
|------|---------|---------|
| Follow Red-Green-Refactor | Write a failing test, make it pass simply, then improve the design. | [tdd.md](./tdd.md) |
| Write A Concrete Failing Test First | In RED, describe the wanted behavior with a concrete example in domain language. | [tdd.md](./tdd.md) |
| Run It Red Before Implementing | In RED, run the test and confirm it fails on the assertion (not a compile/import error) before writing any production code. | [tdd.md](./tdd.md) |
| Make It Pass Simply | In GREEN, default to the obvious implementation; use Fake It only when the solution is unclear. | [tdd.md](./tdd.md) |
| Never Weaken A Test To Get To Green | Get to green by fixing the code, never by loosening, skipping, or deleting the test; only change a test when it is genuinely wrong, and say why. | [tdd.md](./tdd.md) |
| Refactor While Tests Stay Green | In REFACTOR, remove meaningful duplication and improve names without changing behavior. | [tdd.md](./tdd.md) |
| Obey The Three Laws Of TDD | No production code, no extra test code, and no extra production code beyond what the failing test needs. | [tdd.md](./tdd.md) |
| Apply The Rule Of Three As A Heuristic | Lean toward extracting duplication near the third occurrence; use judgment and never add duplication to comply. | [tdd.md](./tdd.md) |
| Triangulate Toward Generality | Add tests that each remove one degree of freedom until the implementation generalizes. | [tdd.md](./tdd.md) |
| Prefer Simpler Transformations | Move RED to GREEN with the simplest code change, adding complexity only when a test forces it. | [tdd.md](./tdd.md) |
| Choose Classic Or Mockist Deliberately | Default to real dependencies (Classic); add mocks (Mockist) for infrastructure-bound code. | [tdd.md](./tdd.md) |
