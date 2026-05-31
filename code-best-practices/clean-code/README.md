# Clean Code

This folder collects reusable clean-code best practices for writing code that is easy to read, change, review, and refactor.

## Sources

- Martin Fowler, [Code Smell](https://martinfowler.com/bliki/CodeSmell.html)
- Martin Fowler, [Rename Variable](https://refactoring.com/catalog/renameVariable.html)
- Martin Fowler, [Extract Function](https://refactoring.com/catalog/extractFunction.html)
- Martin Fowler, [Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html)
- Martin Fowler, [Flag Argument](https://martinfowler.com/bliki/FlagArgument.html)
- Martin Fowler, [Encapsulate Collection](https://refactoring.com/catalog/encapsulateCollection.html)
- Google, [Documentation Best Practices](https://google.github.io/styleguide/docguide/best_practices.html)
- Google, [C++ Style Guide - Comments](https://google.github.io/styleguide/cppguide.html#Comments)

## Contents

- [Naming And Clarity](./naming-and-clarity.md): how to make code readable through names, small scopes, and explicit intent.
- [Functions And Control Flow](./functions-and-control-flow.md): how to keep functions focused and control flow easy to scan.
- [Comments And Documentation](./comments-and-documentation.md): when comments help, when they hurt, and how to keep them accurate.
- [Duplication And Refactoring](./duplication-and-refactoring.md): how to spot duplication, use code smells well, and refactor in small safe steps.

## Core Rules

- Prefer code that explains itself through names and structure.
- Keep functions focused on one small job.
- Use control flow that is easy to scan, not clever to write.
- Write comments for intent and context, not for obvious code.
- Treat duplication and code smells as signals to refactor, not as reasons to panic.
