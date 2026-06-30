---
name: engineering-standards
description: Use this skill when writing code, implementing features, refactoring, planning architecture, designing systems, reviewing code, debugging, or making design decisions. This skill applies this repo's shared engineering baseline through clean code, code quality, object-oriented design, simple design, and maintainability guidance.
---

# Engineering Standards

Reusable, cross-project engineering baseline: clean code, object-oriented design, simple design, and maintainability. Keep project-specific facts in `agent-context/`; use this skill for standards that apply everywhere.

## When This Skill Applies

Use it for any code work: writing features, fixes, utilities, tests, scripts, or tooling; refactoring; planning or designing architecture; reviewing code; debugging; and making design decisions.

## Core Philosophy

> Code exists so developers can cost-effectively discover, understand, add, change, remove, test, debug, deploy, and monitor behavior. Optimize for the people who will read and change it next.

## Load The Shared Baseline First

Before code, design, or review work, read these compact rule indexes:

- `references/clean-code/RULES.md`
- `references/object-oriented-design/RULES.md`

Each index summarizes every rule and links to a detail file. Open a detail file only when the current task needs its examples or depth — do not load the whole `references/` folder by default.

## Apply The Core Lenses

**SOLID** — for each class, module, function, or boundary:

| Principle | Question |
|-----------|----------|
| SRP | Does this have one clear reason to change? |
| OCP | Can behavior extend without risky modification? |
| LSP | Can substitutes preserve the expected contract? |
| ISP | Do callers depend only on what they use? |
| DIP | Do high-level policies avoid depending on low-level details? |

Detail: `references/object-oriented-design/solid-principles.md`.

**Simple design, in priority order:** (1) works correctly, (2) expresses intent through clear names and obvious structure, (3) no meaningful duplication, (4) minimal — the fewest concepts necessary. Detail: `references/clean-code/complexity.md`.

**Complexity** — separate essential (domain) complexity from accidental (solution) complexity, and fight the accidental kind with KISS, YAGNI, and DRY-with-judgment. Watch for change amplification, high cognitive load, and surprising coupling. Detail: `references/clean-code/complexity.md`.

**Code smells** are signals to inspect design, not mandatory rewrites: long method, large class, long parameter list, feature envy, data clumps, primitive obsession, divergent change, shotgun surgery, speculative generality. Detail: `references/clean-code/code-smells.md`.

**Design patterns** should emerge from real design pressure — do not force them. Detail: `references/object-oriented-design/design-patterns.md`.

## Working Checklist

- **Before:** Do I understand the required behavior and how I'll verify it? What is the simplest solution? Am I solving a real problem or a hypothetical one?
- **While coding:** Is this the simplest thing that works? Does each unit have one clear responsibility? Am I depending on abstractions for a good reason? Can I name this more clearly? Am I leaving incidental duplication alone until the shared concept is clear?
- **After it works:** Do the relevant checks pass? Any unused code my change created to remove? Are names and comments still accurate? Would another developer understand this in six months?

## Red Flags — Stop And Rethink

- Writing code without understanding the behavior being changed.
- A method or class size that hides multiple responsibilities.
- More nesting than the main path needs.
- Hardcoding values that belong in configuration or domain rules.
- Creating an abstraction before repeated behavior reveals a stable concept.
- Adding features, flexibility, or error handling "just in case."
- Data bags that force callers to own domain behavior.

## Remember

> "A little bit of duplication is far better than the wrong abstraction."

Prefer the simplest responsible design, and let structure earn its place.
