---
name: adapt-best-practices
description: Adapt a folder of general coding best-practice guides into language-specific or language-and-framework-specific guidance. Use when Codex is asked to convert reusable markdown best-practice folders into output tailored to a target stack, preserve or mirror the source structure, research which rules still apply, replace non-idiomatic advice, and add concrete examples in the target language or framework.
---

# Adapt Best Practices

Turn generic guidance into stack-specific guidance without changing more structure than necessary.

## Workflow

1. Read [references/adaptation-workflow.md](./references/adaptation-workflow.md) first.
2. Inspect the source folder's `README.md` and every guide file before writing anything.
3. Identify the target precisely:
   - Language only
   - Language plus framework
   - Framework plus conventions that imply specific tooling
4. Choose the output location:
   - If the repo keeps agent-facing reusable context together, prefer `agent-context/best-practices/<language>-<framework>/<source-folder-name>/`.
   - Otherwise create a sibling folder whose name makes the target stack obvious and still leaves room for future agent context.
5. If the output folder does not exist yet, scaffold it with `scripts/scaffold_adapted_guides.py`.
6. Research the target stack before rewriting guidance:
   - Prefer official language docs, official framework docs, PEPs, standards, and maintainer documentation.
   - Use broader articles only to fill gaps after checking primary sources.
7. Rewrite the output so it reads like native guidance for the target stack, not like annotated source material.
8. Re-read the full output and remove any leftover scaffold comments or generic placeholders.

## Adaptation Rules

- Preserve the source folder shape unless there is a strong reason to split or merge files.
- Keep filenames stable when mirroring an existing guide set.
- Treat every source rule as one of four cases:
  - Apply directly
  - Apply with adaptation
  - Do not apply
  - Replace with a target-specific equivalent
- Explain target-specific tradeoffs when a generic rule becomes conditional in the target stack.
- Replace generic examples with short, idiomatic examples in the target language and framework.
- Prefer examples that look realistic in the target ecosystem: routing, validation, modules, errors, tests, or common extension points.
- Keep the writing practical and direct. Do not turn the output into a theory document.

## Output Requirements

- Keep the output in English unless the user requests another language.
- Keep README files as clickable indexes.
- Add or refresh a `## Sources` section when the output makes framework-specific claims.
- Make it obvious when a source rule was replaced rather than copied.
- Deliver finished guides, not a checklist for a future writer.

## Stack References

- Read [references/python-flask-example.md](./references/python-flask-example.md) when the target is Python and Flask, or when you want a concrete model for the expected level of specificity.

## Completion Checklist

- Did you inspect the full source folder before rewriting it?
- Did you use primary sources for stack-specific behavior?
- Did you preserve the source structure unless a change was justified?
- Did you replace generic examples with target-specific ones?
- Did you remove scaffold comments and unfinished placeholders?
