# Test-Driven Development

## The Core Loop

```
RED → GREEN → REFACTOR → RED → ...
```

### RED Phase
Write a failing test that describes the behavior you want. The test should:
- Use domain language, not technical jargon
- Describe WHAT, not HOW
- Be a concrete example, not an abstract statement

```typescript
// BAD: Abstract
it('can add numbers', () => { ... });

// GOOD: Concrete example
it('when adding 2 + 3, returns 5', () => { ... });
```

**Run the test and watch it fail before writing any production code.** This is not optional — a test you never saw fail proves nothing. Confirm two things from the actual output:

1. **It fails for the right reason.** The failure must be the *assertion* — the expected behavior is missing or wrong (e.g. `expected 5, received undefined`). A compile error, import error, missing symbol, or typo is a broken test, not a RED. Fix that first, then get a real assertion failure.
2. **Only this test's behavior is missing.** If the new test passes immediately, stop — the behavior already exists, the test asserts nothing meaningful, or it's testing the wrong thing. Investigate before moving on.

Writing the test and the implementation together and running once at the end is not TDD. The point of RED is to prove the test can detect the absence of the behavior; you only get that proof by running it red first.

### GREEN Phase
Write the simplest code that makes the test pass. Two strategies:

1. **Obvious Implementation** - When you know the solution, just write it. This is the default.
   ```typescript
   add(a: number, b: number): number {
     return a + b;
   }
   ```

2. **Fake It** - Return a hardcoded value, then let later tests force generalization.
   ```typescript
   add(a: number, b: number): number {
     return 5; // forced general by the next test case
   }
   ```

**Default to Obvious Implementation.** Reach for Fake It only when the real implementation is genuinely unclear and you want a test to pull it into shape. Never leave a faked value in once a test exists that should generalize it — a green suite built on a hardcoded return proves nothing.

**Get to green by changing the production code, never by weakening the test.** When a test won't pass, the failure is the signal — fix the code. Do not loosen the assertion, delete the failing case, mark it `.skip`/`xit`/pending, widen an expected value to match actual output, or wrap it in a try/catch that swallows the failure. Each of these produces a green suite that proves nothing, which is worse than a red one because it hides the gap.

The only legitimate reason to edit a failing test is that the test itself is genuinely wrong — it asserts the wrong behavior, encodes a stale contract, or has a bug. When that's the case, say so explicitly, explain why the expectation is wrong, and correct it deliberately — don't quietly soften it to get past a failure you don't understand. If you can't explain why a test is failing, you are not yet allowed to change it.

### REFACTOR Phase
This is where **design happens**. Look for:
- Duplication (but wait for Rule of Three)
- Long methods to extract
- Poor names to improve
- Complex conditions to simplify

## The Three Laws of TDD

1. **No production code** without a failing test
2. **No more test code** than sufficient to fail (compilation failures count)
3. **No more production code** than sufficient to pass the one failing test

## The Rule of Three

Lean toward extracting duplication only once you've seen it about three times. A wrong abstraction is costlier to unwind than duplication, so let the pattern prove itself first.

```typescript
// Duplication #1 - Leave it
// Duplication #2 - Note it, leave it
// Duplication #3 - NOW extract it
```

This is a heuristic, not a hard rule. Use judgment: extract obvious, identical logic sooner, and never *add* duplication just to satisfy the count.

## Triangulation

Each new test "sculpts" the solution toward a general, robust implementation.

Think of **degrees of freedom** - like a car that needs forward/back, left/right, and rotation. Each test carves out one degree of freedom until the implementation handles all cases.

## Prefer Simpler Transformations

When moving from RED to GREEN, prefer the simplest code change that passes: a constant over a variable, a single branch over a loop, a loop over recursion. Reach for more complex constructs only when a test actually forces them. This keeps each step small and each test meaningful.

## Arrange-Act-Assert And Test Naming

See `SKILL.md` for the Arrange-Act-Assert structure and concrete-behavior naming guidance. In TDD, write the failing test in that shape during the RED phase.

## Classic vs Mockist TDD

**Classic (Detroit/Chicago) TDD:**
- Test with real dependencies
- Higher confidence, slower tests
- Best for: Pure functions, integration tests

**Mockist (London) TDD:**
- Mock external dependencies
- Faster tests, more isolated
- Best for: Classes with infrastructure dependencies

Start with Classic TDD to learn the technique. Add mocks when testing code with databases, APIs, etc.

## Common Mistakes

1. **Writing code before tests** - Violates the fundamental principle
2. **Writing too much test** - Just enough to fail
3. **Writing too much code** - Just enough to pass
4. **Skipping refactor** - This is where design lives
5. **Testing implementation** - Test behavior, not how it's done
6. **Abstract test names** - Use concrete examples
7. **Extracting too early** - Wait for Rule of Three
