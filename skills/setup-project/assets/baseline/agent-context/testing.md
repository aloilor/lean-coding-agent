# Testing Conventions

Automated tests should be easy to scan, clearly categorized, and grouped around the behavior they verify.

## Test Comments

- Add brief comments when a test's intent, setup, or assertion is not immediately obvious.
- Prefer comments that explain why the scenario matters over comments that restate the code.
- Keep comments short and close to the relevant arrange, act, or assert block.

## Service Grouping

- Group tests for a specific service inside a service-specific folder.
- Keep the folder name aligned with the service name used in the application code.
- Avoid mixing unrelated service tests in the same folder just because they share fixtures or helpers.

## Test Type

- Make the test type explicit in the folder path, file name, suite name, or test metadata.
- Use clear categories such as unit, feature, integration, e2e, contract, or smoke tests.
- Choose the narrowest accurate category for the behavior being verified.
