# Branching Conventions

## Use A Predictable Branch Shape

- Follow the Conventional Branch structure: `<type>/<description>`.
- Reserve trunk branches such as `main`, `master`, or `develop` as special long-lived branches without a prefix.
- Keep the description short enough to scan in pull requests, CI logs, and deployment tooling.

Examples:

```text
feature/add-login-page
fix/header-bug
release/v1.2.0
```

## Use Standard Branch Types First

- Use `feature/` or `feat/` for new work that adds behavior.
- Use `bugfix/` or `fix/` for bug fixes.
- Use `hotfix/` for urgent production-facing fixes.
- Use `release/` for release preparation branches.
- Use `chore/` for non-feature work such as dependency or documentation updates.
- Prefer a small shared set of types over a long taxonomy that people will forget.
- If your team adds custom types, document them clearly and keep them rare.

## Keep Names Machine-Friendly

- Use lowercase letters, numbers, and hyphens in normal branch descriptions.
- Do not use spaces, underscores, or uppercase letters.
- For release branches, dots are acceptable inside version numbers such as `release/v1.2.0`.
- Avoid consecutive, leading, or trailing hyphens or dots.

Good examples:

- `feature/issue-123-new-login`
- `chore/update-dependencies`
- `hotfix/security-patch`

Avoid:

- `Feature/Add-Login`
- `fix/header bug`
- `fix/header_bug`
- `feature/new--login`

## Make Purpose Obvious

- Write the description so another engineer can understand the branch intent without opening the diff.
- Include a ticket number when it helps connect the branch to planning or issue tracking.
- Prefer the smallest meaningful description, not a sentence.

Better examples:

- `feature/issue-123-new-login`
- `fix/cache-invalidation`
- `release/v2.1.0`

Weaker examples:

- `feature/stuff`
- `fix/many-things`
- `chore/updates`

## Use Branch Names To Support Workflow

- Keep branch names stable enough that CI rules and release automation can rely on them.
- Do not overload branch prefixes with commit-level detail. Branches are temporary and should stay simpler than commits.
- Use the branch type to signal workflow intent, then use commit messages to describe the specific changes inside the branch.

## Practical Checks

- Does the branch follow `<type>/<description>` or an approved trunk branch name?
- Is the type one the team recognizes immediately?
- Is the description lowercase, concise, and free of spaces, underscores, and noisy punctuation?
- Would someone understand the branch purpose from the name alone?
- If the team uses custom types, are they documented and worth the extra complexity?
