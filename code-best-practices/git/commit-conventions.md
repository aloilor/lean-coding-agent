# Commit Conventions

## Use The Conventional Commit Shape

- Follow the Conventional Commits structure: `<type>[optional scope]: <description>`.
- Add an optional body when the short summary is not enough.
- Add optional footers for metadata such as references or reviewers.

Examples:

```text
feat: add CSV export for invoices
fix(auth): handle null email during signup
docs: correct API setup example
```

## Choose Types By Intent

- Use `feat` when the commit adds a new feature.
- Use `fix` when the commit patches a bug.
- Use other types such as `docs`, `refactor`, `test`, `chore`, or `ci` when they describe the change more honestly.
- If one change really contains multiple intents, split it into multiple commits when possible.

## Use Scope Only When It Adds Clarity

- Add a scope when it helps readers understand which part of the codebase changed.
- Keep scopes short and noun-based, such as `auth`, `parser`, or `api`.
- Skip the scope when the repository is small or the type and description are already clear enough.

Examples:

```text
feat(api): add invoice export endpoint
fix(parser): handle trailing commas in arrays
```

## Write Short Descriptions That Explain Behavior

- Write the description as a compact summary of the change, not a copy of the file edits.
- Prefer descriptions that explain user-visible behavior, system behavior, or the intent of the refactor.
- Keep the first line scannable in logs, pull requests, and changelogs.

Better examples:

- `fix: prevent duplicate invoice emails`
- `refactor: split payment retry logic by provider`
- `test: cover invalid token refresh flow`

Weaker examples:

- `fix: stuff`
- `chore: updates`
- `refactor: changes`

## Use Breaking Change Markers Explicitly

- Mark breaking changes with `!` before the colon, with a `BREAKING CHANGE:` footer, or both.
- Use a footer when the compatibility impact needs explanation beyond the summary line.
- Do not hide breaking behavior inside a normal `feat` or `fix` commit.

Examples:

```text
feat!: drop support for Node 18

BREAKING CHANGE: the CLI now requires Node 20 or newer
```

```text
feat(api)!: remove legacy invoice endpoint
```

## Use Bodies And Footers When They Add Real Context

- Add a body when reviewers or future maintainers need the reason behind the change.
- Separate the body from the summary with one blank line.
- Use footers for structured metadata such as `Refs: #123` or `Reviewed-by: A`.

Example:

```text
fix: prevent racing of requests

Track the latest request id and ignore older responses so stale results
do not overwrite the current UI state.

Refs: #123
```

## Keep Conventional Commits Honest

- Do not choose `feat` or `fix` only because they look nicer in history.
- Do not treat the convention as a substitute for small, reviewable commits.
- Be consistent across the repository so tooling and humans can rely on the history.

## Practical Checks

- Does the first line match `<type>[optional scope]: <description>`?
- Did I choose `feat` or `fix` only when the change truly fits those meanings?
- Would a scope help readers, or is it unnecessary noise?
- If the change is breaking, did I mark it clearly with `!` or `BREAKING CHANGE:`?
- If the summary is not enough, did I add a useful body or footer instead of packing too much into the title?
