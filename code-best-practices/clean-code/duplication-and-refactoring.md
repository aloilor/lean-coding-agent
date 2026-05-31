# Duplication And Refactoring

## Treat Duplication As A Design Smell

- Duplicate code often means one idea is being maintained in multiple places.
- The risk is not only extra lines; the real risk is inconsistent future changes.
- Not every repeated line needs an abstraction, but repeated behavior should make you stop and look.

Good examples of duplication worth refactoring:

- The same validation rule in several handlers
- The same pricing calculation in multiple services
- The same decision tree copied into different endpoints

## Use Code Smells As Signals

- A code smell is a clue, not an automatic verdict.
- Long functions, vague names, flag arguments, and data-heavy classes often point to deeper design problems.
- Smells are useful because they are easy to notice early.

## Refactor In Small Safe Steps

- Prefer small mechanical refactorings over giant rewrites.
- Rename before you redesign.
- Extract a function before extracting a class.
- Keep behavior stable while improving readability.

Useful moves:

- Rename a variable or function when the name is weak.
- Extract a function when a block has one clear purpose.
- Replace nested conditionals with guard clauses when the main path is hidden.
- Encapsulate a collection when callers are mutating internal lists directly.

## Avoid Premature Abstraction

- Do not abstract just because two blocks look similar once.
- Wait until the duplication reflects a shared concept, not only shared syntax.
- Bad abstractions can be harder to clean up than a little temporary repetition.

## Practical Checks

- If this rule changes, how many places must I edit?
- Is this code smell pointing at a naming problem, a function-size problem, or a boundary problem?
- Can I improve this with one small refactoring instead of a broad rewrite?
