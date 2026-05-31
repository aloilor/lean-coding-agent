# Design Patterns

This folder collects reusable design-pattern best practices for choosing patterns for the right reasons, keeping them simple, and avoiding pattern-driven overengineering.

## Sources

- Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*
- Martin Fowler, [Code Smell](https://martinfowler.com/bliki/CodeSmell.html)
- Martin Fowler, [Flag Argument](https://martinfowler.com/bliki/FlagArgument.html)
- Martin Fowler, [Replace Conditional with Polymorphism](https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html)

## Contents

- [Creational Patterns](./creational-patterns.md): how to create objects cleanly without spreading construction complexity everywhere.
- [Structural Patterns](./structural-patterns.md): how to compose and wrap objects without tight coupling.
- [Behavioral Patterns](./behavioral-patterns.md): how to organize responsibilities and collaboration between objects.
- [Pattern Selection And Misuse](./pattern-selection-and-misuse.md): how to know when a pattern helps and when it is just noise.

## Core Rules

- Use a pattern to solve a real recurring design problem, not to make code look sophisticated.
- Prefer the simplest pattern that removes concrete pain.
- Keep the intent of the pattern obvious from the code.
- If a pattern adds more moving parts than value, do not use it.
- Patterns should reduce coupling and clarify responsibilities, not hide simple code behind ceremony.
