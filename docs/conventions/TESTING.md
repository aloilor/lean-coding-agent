# Testing

## Commands

| Purpose | Command | Source |
| --- | --- | --- |
| Run all tests | `node --test tests/*.test.mjs` | `tests/` |

## Traps

- There is no `npm test` script, and `node --test tests/` fails because it treats the directory as a test file. Pass the file glob.
- Keep automated test files in `tests/`.
