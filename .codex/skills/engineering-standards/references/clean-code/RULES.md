# Clean Code Rules

Load this file for general code work, complexity checks, smell detection, refactoring, review, or debugging. Open detail files only when the current task needs examples or deeper guidance.

## Rules

| Rule | Summary | Details |
|------|---------|---------|
| Use Names That Explain Intent | Names should reveal purpose instead of forcing readers to infer meaning from implementation. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Prefer Domain Language | Use product and domain terms consistently instead of vague technical filler. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Keep Scope Small | Short names are acceptable only in tiny obvious scopes; public and long-lived names need precision. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Prefer Code That Reads Like A Story | Arrange names and calls so the main flow is understandable at a glance. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Keep Functions Focused | Each function should do one clear job at one level of detail. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Prefer Guard Clauses Over Deep Nesting | End invalid or special paths early when that makes the normal path clearer. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Avoid Flag Arguments When They Change Meaning | Split behavior when a boolean changes what a function fundamentally does. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Prefer Straightforward Flow Over Cleverness | Use simple control flow instead of dense expressions or side-effect chains. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Prefer Self-Explaining Code First | Improve names or structure before adding comments that explain obvious code. | [inline-comments.md](./inline-comments.md) |
| Use Comments For Why, Not Obvious What | Comments should explain intent, constraints, tradeoffs, or surprising local behavior. | [inline-comments.md](./inline-comments.md) |
| Keep Comments Accurate | Update or delete comments when behavior changes or the comment loses its job. | [inline-comments.md](./inline-comments.md) |
| Document The Public Contract First | Public APIs should explain inputs, outputs, errors, effects, and constraints. | [code-documentation.md](./code-documentation.md) |
| Keep Documentation Close To The Code | Put docs where maintainers will update them with behavior changes. | [code-documentation.md](./code-documentation.md) |
| Write For The Reader's Next Question | Add the next useful fact, example, or constraint a caller will need. | [code-documentation.md](./code-documentation.md) |
| Prefer Stable Facts Over Temporary Narration | Document behavior and contracts, not fragile implementation steps. | [code-documentation.md](./code-documentation.md) |
| Explain Edge Cases And Failure Modes | Call out recovery, retry, validation, data-loss, partial-failure, and consistency behavior. | [code-documentation.md](./code-documentation.md) |
| Keep Examples Small And Honest | Examples should be realistic, copy-safe, and as small as possible. | [code-documentation.md](./code-documentation.md) |
| Use Consistent Documentation Structure | Similar public APIs should expose summaries, errors, examples, and effects consistently. | [code-documentation.md](./code-documentation.md) |
| Remove Documentation That Lost Its Job | Delete stale, obvious, or misleading docs instead of preserving noise. | [code-documentation.md](./code-documentation.md) |
| Treat Duplication As A Design Smell | Extract shared behavior only when the repeated code represents the same concept. | [duplication-and-refactoring.md](./duplication-and-refactoring.md) |
| Use Code Smells As Signals | Smells indicate where to inspect design, not mandatory rewrite commands. | [duplication-and-refactoring.md](./duplication-and-refactoring.md) |
| Refactor In Small Safe Steps | Prefer behavior-preserving steps and verify between changes. | [duplication-and-refactoring.md](./duplication-and-refactoring.md) |
| Avoid Premature Abstraction | Wait for a real shared concept before introducing a reusable abstraction. | [duplication-and-refactoring.md](./duplication-and-refactoring.md) |
| One Level Of Indentation Per Method | Use extraction or guard clauses when nesting hides the main path. | [object-calisthenics.md](./object-calisthenics.md) |
| Prefer Guard Clauses When Clearer | Avoid `else` only when early returns make the flow easier to scan. | [object-calisthenics.md](./object-calisthenics.md) |
| Wrap Primitives And Strings When They Have Meaning | Use value objects for domain concepts, units, or validation rules; avoid ceremony for simple values. | [object-calisthenics.md](./object-calisthenics.md) |
| Use First-Class Collections | Wrap collections when collection rules, invariants, or behavior need a home. | [object-calisthenics.md](./object-calisthenics.md) |
| Avoid Deep Object Chains | Ask the object you know for behavior instead of reaching through internals. | [object-calisthenics.md](./object-calisthenics.md) |
| Do Not Abbreviate | Prefer searchable, clear names over cryptic shortening. | [object-calisthenics.md](./object-calisthenics.md) |
| Keep Entities Small | Use size as a warning light for mixed concerns, not as an absolute limit. | [object-calisthenics.md](./object-calisthenics.md) |
| Prefer Few Instance Variables | Group fields that travel together and split classes with unrelated state. | [object-calisthenics.md](./object-calisthenics.md) |
| Avoid Getter And Setter Data Bags | Put domain behavior and invariant protection near the data owner. | [object-calisthenics.md](./object-calisthenics.md) |

## Complexity Rules

| Rule | Summary | Details |
|------|---------|---------|
| Separate Essential From Accidental Complexity | Preserve real domain complexity; remove complexity introduced by the solution. | [complexity.md](./complexity.md) |
| Watch Change Amplification | If a small behavior change touches many files, inspect boundaries and coupling. | [complexity.md](./complexity.md) |
| Reduce Cognitive Load | Code should be easy to hold in working memory and explain to another developer. | [complexity.md](./complexity.md) |
| Expose Unknown Unknowns | Surprising behavior and hidden coupling are signs of unmanaged complexity. | [complexity.md](./complexity.md) |
| Communicate Clearly | Names, structure, tests, and docs should make the design understandable. | [complexity.md](./complexity.md) |
| Keep It Simple | Start with the obvious solution and add structure only when it earns its keep. | [complexity.md](./complexity.md) |
| Create Fast Feedback | Use tests, CI, code review, and small changes to catch complexity early. | [complexity.md](./complexity.md) |
| Show Courage | Remove or simplify code when evidence shows it is no longer needed. | [complexity.md](./complexity.md) |
| Respect Future Maintainers | Optimize for the people who will read, change, debug, and operate the system. | [complexity.md](./complexity.md) |
| Apply KISS | Prefer fewer moving parts, fewer concepts, and direct control flow. | [complexity.md](./complexity.md) |
| Apply YAGNI | Do not build extension points, options, or features before there is a real need. | [complexity.md](./complexity.md) |
| Apply DRY With The Rule Of Three | Avoid repeated business rules, but wait for a clear shared concept before abstracting. | [complexity.md](./complexity.md) |
| Separate Concerns | Split validation, business rules, persistence, presentation, and integration when they change independently. | [complexity.md](./complexity.md) |
| Manage Technical Debt Deliberately | Track, isolate, and pay down debt when it slows change or increases risk. | [complexity.md](./complexity.md) |
| Use The Boy Scout Rule Carefully | Leave touched code cleaner when it is related to the task and low risk. | [complexity.md](./complexity.md) |
| Know When Not To Refactor | Avoid refactoring without tests, during urgent fixes, or when the benefit is unclear. | [complexity.md](./complexity.md) |
| Apply Simple Design In Order | Make it work, express intent, remove meaningful duplication, then minimize. | [complexity.md](./complexity.md) |

## Code Smell Rules

| Rule | Summary | Details |
|------|---------|---------|
| Bloaters | Large methods, classes, parameter lists, data clumps, and primitive obsession often hide missing concepts. | [code-smells.md](./code-smells.md) |
| Object-Orientation Abusers | Switches, refused bequests, and temporary fields can signal misplaced polymorphism or inheritance. | [code-smells.md](./code-smells.md) |
| Change Preventers | Divergent change, shotgun surgery, and parallel inheritance mean change boundaries are wrong. | [code-smells.md](./code-smells.md) |
| Dispensables | Dead code, lazy classes, duplicate code, comments, and speculative generality add noise. | [code-smells.md](./code-smells.md) |
| Couplers | Feature envy, inappropriate intimacy, message chains, and middle men reveal unhealthy dependencies. | [code-smells.md](./code-smells.md) |
| Long Method | Extract named steps when a method hides multiple responsibilities or levels of detail. | [code-smells.md](./code-smells.md) |
| Large Class | Split classes that have too many responsibilities or reasons to change. | [code-smells.md](./code-smells.md) |
| Feature Envy | Move behavior toward the object whose data it uses most. | [code-smells.md](./code-smells.md) |
| Primitive Obsession | Wrap domain concepts when primitives carry rules, units, or validation. | [code-smells.md](./code-smells.md) |
| Switch Statements | Consider polymorphism, strategy, or a dispatch table when behavior varies by type. | [code-smells.md](./code-smells.md) |
| Inappropriate Intimacy | Reduce classes knowing too much about each other's internals. | [code-smells.md](./code-smells.md) |
| Speculative Generality | Delete unused abstractions, hooks, and configuration added just in case. | [code-smells.md](./code-smells.md) |
| Prevent Smells Early | Use clear names, focused responsibilities, tests, and small refactors before smells harden. | [code-smells.md](./code-smells.md) |
| Respond To Smells Safely | Identify the smell, understand why it exists, refactor incrementally, and verify behavior. | [code-smells.md](./code-smells.md) |
