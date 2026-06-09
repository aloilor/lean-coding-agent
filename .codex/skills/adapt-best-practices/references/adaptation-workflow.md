# Adaptation Workflow

Use this file as the detailed playbook after the skill triggers.

## 1. Read The Source Completely

- Read the source folder `README.md` first.
- Read every markdown guide in the folder before deciding how to adapt it.
- Note repeated themes, because repeated themes often need one shared target-specific pattern.

## 2. Decide The Output Shape

- Mirror the source directory tree by default.
- Keep the same guide filenames unless the source naming is actively misleading for the target stack.
- Keep README indexes short and clickable.

If you need an initial mirrored tree, run:

```bash
python scripts/scaffold_adapted_guides.py --source "<source-folder>" --output "<output-folder>" --language "<language>" --framework "<framework>"
```

The scaffold is only a starting point. Rewrite the files before delivery.

## 3. Research Before Rewriting

Use this source order:

1. Official language documentation and style guides
2. Official framework documentation
3. Standards, PEPs, RFCs, or maintainer-authored references
4. High-signal ecosystem docs for common tooling only when needed

Do not rely on memory alone for framework behavior that may have changed.

## 4. Classify Each Rule

For each source rule, decide which bucket it belongs in:

- `apply-directly`: the rule is still correct without meaningful changes
- `apply-with-adaptation`: the rule stays valid but the idiomatic expression changes
- `not-applicable`: the rule does not fit the target stack
- `replace`: the source rule points to a better stack-specific practice

This classification is for your reasoning. The final output does not need these literal labels unless they help readability.

## 5. Rewrite For Native Use

- Write as if the guide was originally authored for the target stack.
- Replace generic examples with idiomatic code.
- Prefer realistic examples over toy snippets when the framework benefits from context.
- Keep examples short enough to scan in a review.

Good example patterns:

- Thin route/controller, heavier service/helper
- Target-specific validation and error handling
- Clear naming that matches the language style guide
- Common project structure for that framework

## 6. Extend The Guidance Carefully

Extend the source only when the target stack clearly needs additional context, such as:

- Common pitfalls the generic guide misses
- Framework-specific tradeoffs
- Language conventions that materially affect readability
- A standard pattern that replaces a generic abstraction

Do not pad the output with unrelated framework tips.

## 7. Finish Cleanly

- Remove copied source wording that no longer fits.
- Remove scaffold comments.
- Check that every README link still works.
- Confirm the output reads like finished documentation, not notes.
