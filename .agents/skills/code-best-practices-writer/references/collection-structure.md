# Code Best Practices Collection Structure

Use this file as the local source of truth before writing or reorganizing content in `code-best-practices`.

## Current Top-Level Layout

- `code-best-practices/README.md`: root index of all guide categories
- `code-best-practices/clean-code/`: naming, functions, comments, duplication, refactoring
- `code-best-practices/design-patterns/`: creational, structural, behavioral patterns, pattern misuse
- `code-best-practices/object-oriented-programming/`: SOLID, composition, encapsulation
- `code-best-practices/rest-api-design/`: resource modeling, HTTP semantics, validation, querying, operations

## Observed Conventions

- Root and category README files act as clickable indexes.
- Category README files use short intros and compact descriptions.
- Existing category READMEs usually include `## Sources`, `## Contents`, and `## Core Rules`.
- Guide files usually use one topic per file, several `##` sections, and a final `## Practical Checks`.
- The tone is practical and direct, with short examples instead of long theory.

## Writing Style To Match

- Write in English.
- Prefer plain wording and concrete advice.
- Keep guidance reusable across projects.
- Use examples only when they clarify the rule.
- Keep lists flat and easy to scan.

## Change Rules

- Prefer extending the existing structure over inventing a new one.
- Add a new file only when the topic is too large or too different for an existing file.
- Add a new category only when no current category is a natural fit.
- Keep README descriptions short enough to work as an index.
