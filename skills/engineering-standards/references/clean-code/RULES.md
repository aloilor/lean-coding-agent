# Clean Code

## Overview

Clean code is code that is easy to read, change, review, and refactor. Prefer names, structure, and small steps that make intent obvious before adding comments or abstractions.

## Core Rules

- Name things by intent, not by vague implementation details.
- Keep functions focused on one job.
- Make the main control flow easy to scan.
- Use inline comments for local context, tradeoffs, and constraints.
- Document public contracts, failure modes, and edge cases.
- Treat duplication and code smells as signals, not automatic rewrite orders.
- Refactor in small behavior-preserving steps.

## Contents

- [Naming And Clarity](./naming-and-clarity.md)
- [Functions And Control Flow](./functions-and-control-flow.md)
- [Inline Comments](./inline-comments.md)
- [Code Documentation](./code-documentation.md)
- [Duplication And Refactoring](./duplication-and-refactoring.md)
- [Object Calisthenics](./object-calisthenics.md)

## Quick Reference

| Area | One-Liner | Red Flag |
|------|-----------|----------|
| Naming | Say what the code means | `data`, `tmp`, `handleStuff()` |
| Functions | One clear job | Validation, persistence, formatting, and IO mixed together |
| Control Flow | Show the main path | Deep nesting or clever chained side effects |
| Inline Comments | Explain why | Comments repeating obvious code |
| Documentation | Help callers use code safely | Missing errors, side effects, or edge cases |
| Refactoring | Improve in small safe steps | Broad rewrites mixed with behavior changes |
| Object Calisthenics | Optional practice constraints for small focused objects | Enforcing exercise rules at all times |
