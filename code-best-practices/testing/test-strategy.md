# Test Strategy

## Start With Risk

- Write tests for behavior that would hurt users, money, data, security, or operations if it broke.
- Cover common paths, boundary values, invalid inputs, permissions, retries, and failure paths.
- Use recent incidents and production bugs to update the test suite where it was blind.

Good targets:

- A payment cannot be captured twice.
- A user cannot read another tenant's data.
- A retry stops after the configured limit and reports the failure.

## Use The Smallest Useful Scope

- Prefer focused unit or component tests when they prove the behavior clearly.
- Use integration tests for contracts between modules, databases, queues, APIs, or services.
- Use end-to-end tests for the small number of user journeys that only full-stack execution can prove.
- Avoid testing the same behavior at every layer unless each layer catches a different class of bug.

Balanced shape:

```text
many focused tests
some integration and contract tests
few full end-to-end tests
```

## Test Behavior, Not Implementation

- Assert observable outputs, state changes, emitted events, or external calls that belong to the contract.
- Avoid assertions against private methods, internal ordering, or incidental helper calls.
- Use mocks mainly at process boundaries such as time, network, filesystem, queues, or third-party services.
- Prefer simple fakes over deep mock setups when they make the test easier to understand.

## Keep Tests Readable

- Name tests after the behavior and condition they verify.
- Structure tests as setup, action, and assertion even if the framework does not enforce that shape.
- Keep fixtures small and local unless shared setup removes real duplication.
- Make one test failure explain one broken behavior.

Example:

```text
returns_validation_error_when_quantity_is_negative
```

## Manage Coverage As A Signal

- Use coverage to find untested risk, not as proof that the system is correct.
- Raise coverage expectations only when the team can keep tests meaningful and maintainable.
- Review new code for missing behavior tests even when the numeric coverage threshold passes.

## Practical Checks

- Does each important behavior have at least one test at the smallest useful scope?
- Would a failing test point to a real behavior problem instead of an internal refactor?
- Are failure paths and invalid inputs covered, not only happy paths?
- Is any end-to-end test proving something that a faster test could prove just as well?
- Did a recent bug reveal a missing test that should now exist?
