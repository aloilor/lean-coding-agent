---
name: code-best-practices-writer
description: Create or update best-practice guides inside this repository's `code-best-practices` folder. Use when asked to add a new best-practice topic, expand an existing guide, create a new category, refresh README indexes, or keep the collection's structure and writing style consistent.
---

# Code Best Practices Writer

Use this skill to extend the repository's reusable best-practice library without breaking its structure or tone.

## Workflow

1. Read [references/collection-structure.md](./references/collection-structure.md) first.
2. Inspect `code-best-practices/README.md`, then inspect the closest matching category README and at least one related guide file before editing.
3. Choose the smallest change that fits the request:
   - Add a section to an existing guide if the new topic naturally belongs there.
   - Add a new guide file inside an existing category if the topic deserves its own focused document.
   - Create a new category only if the topic does not fit the existing categories and the scope is broad enough to justify a category README plus one or more guide files.
4. Update every affected README index immediately after adding or renaming content.
5. Re-read the changed markdown for consistency before finishing.

## Writing Rules

- Write all repository content in English.
- Prefer plain explanations over academic wording.
- Keep examples short and practical when they make the rule easier to apply.
- Prefer concise bullet points and short sections over long essays.
- Use Title Case headings, matching the current collection.
- Keep filenames lowercase with hyphens.
- End guide files with a `## Practical Checks` section when the file is instructional.
- Touch only the files required by the requested topic.

## Category Selection

Prefer the existing categories whenever possible:

- `clean-code`
- `design-patterns`
- `object-oriented-programming`
- `rest-api-design`

When a topic could fit more than one category, choose the category where a reader would most naturally look first. Prefer one clear home over duplicating guidance across folders.

## File Patterns

### Category README

Keep category `README.md` files aligned with the existing pattern:

1. `# Category Name`
2. One short introductory paragraph
3. Optional `## Sources`
4. `## Contents` with clickable links and one-line descriptions
5. `## Core Rules` with compact bullets

Update `code-best-practices/README.md` when adding or renaming a category.

### Guide File

Keep guide files focused and easy to scan:

1. `# Guide Title`
2. Several `##` sections for distinct subtopics
3. Short bullets or compact examples under each section
4. A final `## Practical Checks` section with review questions

Use code blocks only when they clarify the rule better than prose.

## Content Standards

- Prefer durable guidance over framework-specific trivia unless the user explicitly asks for that specificity.
- Explain why a rule matters, not just what to do.
- Avoid filler, marketing language, and generic "always/never" claims that are not defendable.
- Keep advice actionable enough that an engineer could use it during a review or implementation.
- Mention tradeoffs when a rule is situational.

## Completion Checklist

- Did you place the content in the best existing category?
- Did you update every affected `README.md` index?
- Does the new content match the collection's heading style, tone, and brevity?
- Did you include practical examples where they add clarity?
- Did you avoid unrelated cleanup or restructuring?
