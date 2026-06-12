# Testing

This folder collects reusable testing best practices for useful coverage, reliable feedback, and release confidence.

## Sources

- Martin Fowler, [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- Google SRE, [Testing for Reliability](https://sre.google/sre-book/testing-reliability/)

## Contents

- [Test Strategy](./test-strategy.md): how to choose useful test scopes, cover risk, and avoid brittle implementation tests.
- [Test Data And Environments](./test-data-and-environments.md): how to keep test data realistic, isolated, repeatable, and safe.

## Core Rules

- Test the riskiest behavior first, using the smallest test scope that gives real confidence.
- Make test failures deterministic and actionable before adding more tests.
- Keep test data safe, realistic, and isolated so tests can run repeatedly and in parallel.
- Use broader integration and end-to-end tests only when a smaller test cannot prove the behavior.
