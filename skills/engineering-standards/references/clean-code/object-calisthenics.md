# Object Calisthenics

Object calisthenics are practice constraints for noticing design pressure. Treat them as prompts, not production laws. Apply them only when they make the current code clearer, safer, or easier to change.

## Prompt Table

| Prompt | Useful Pressure | Overuse Risk | Read Instead |
| --- | --- | --- | --- |
| One level of indentation per method | Reveals nested responsibilities and hidden exceptional paths. | Extracting tiny methods that obscure a simple flow. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Prefer guard clauses | Keeps the normal path easy to scan. | Early returns that scatter required cleanup or ordering. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Wrap meaningful primitives | Protects units, validation, formatting, and domain invariants. | Creating value objects for values with no rules. | [../object-oriented-design/object-oriented-design.md](../object-oriented-design/object-oriented-design.md) |
| Use first-class collections | Gives collection rules and invariants a home. | Wrapping a list that has no behavior. | [../object-oriented-design/object-oriented-design.md](../object-oriented-design/object-oriented-design.md) |
| Avoid deep object chains | Reduces knowledge of another object's internals. | Adding pass-through methods that hide useful structure. | [../object-oriented-design/object-oriented-design.md](../object-oriented-design/object-oriented-design.md) |
| Do not abbreviate | Keeps names searchable and obvious. | Overly long names in tiny local scopes. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Keep entities small | Reveals mixed responsibilities. | Splitting cohesive behavior across too many files. | [code-smells.md](./code-smells.md) |
| Prefer few instance variables | Exposes unrelated state and data clumps. | Fragmenting state that changes together. | [code-smells.md](./code-smells.md) |
| Avoid getter/setter data bags | Keeps behavior near the data and invariants. | Hiding data needed for legitimate serialization or framework boundaries. | [../object-oriented-design/object-oriented-design.md](../object-oriented-design/object-oriented-design.md) |

## How To Use

- Pick one prompt that matches a real pain in the code.
- Check whether the proposed change preserves behavior and stays in scope.
- Prefer improving names and boundaries before adding abstractions.
- Verify after each meaningful refactor.

## Quick Checks

- Is the main path visible without reading every branch?
- Does a domain value have rules that a raw primitive cannot protect?
- Is a caller reaching through another object to make a decision?
- Would splitting this unit reduce reasons to change, or just scatter cohesive behavior?
