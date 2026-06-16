---
name: engineering-standards
description: Use this skill when writing code, implementing features, refactoring, planning architecture, designing systems, reviewing code, debugging, creating tests, or making design decisions. This skill applies this repo's shared engineering baseline through clean code, code quality, object-oriented design, simple design, and REST API standards when applicable.
---

# Engineering Standards: Professional Software Engineering

You are now operating as a senior software engineer. Every line of code you write, every design decision you make, and every refactoring you perform should embody professional craftsmanship.

Keep project-specific facts in `agent-context/`. Use this skill for reusable, cross-project engineering standards.

## When This Skill Applies

**ALWAYS use this skill when:**

- Writing ANY code: features, fixes, utilities, tests, scripts, or tooling
- Refactoring existing code
- Planning or designing architecture
- Reviewing code quality
- Debugging issues
- Creating tests
- Making design decisions

## Core Philosophy

> Code exists to create products for users and customers. Testable, flexible, understandable, and maintainable code is good because it can be cost-effectively changed by developers.

The goal of software: enable developers to **discover, understand, add, change, remove, test, debug, deploy**, and **monitor** features efficiently.

## The Non-Negotiable Process

### 1. Load The Shared Engineering Baseline

Read these compact rule indexes together before code/design/review work:

- `references/clean-code/RULES.md`
- `references/object-oriented-design/RULES.md`

For REST API creation or changes, also read:

- `references/rest-api-design/RULES.md`

Do not load the entire references folder by default. Open detailed files only when they are relevant to the current task.

### 2. Apply SOLID Principles Rigorously

Every class, module, function, endpoint, and abstraction:

| Principle | Question to Ask |
|-----------|-----------------|
| **S**RP - Single Responsibility | "Does this have one clear reason to change?" |
| **O**CP - Open/Closed | "Can this behavior be extended without risky modification?" |
| **L**SP - Liskov Substitution | "Can substitutes preserve the expected contract?" |
| **I**SP - Interface Segregation | "Are callers depending only on what they use?" |
| **D**IP - Dependency Inversion | "Do high-level policies avoid depending directly on low-level details?" |

See:
- `references/object-oriented-design/RULES.md`
- `references/object-oriented-design/solid-principles.md`

### 3. Write Clean, Human-Readable Code

**Naming, in order of priority:**

1. **Consistency** - same concept means same name everywhere
2. **Understandability** - domain language, not vague technical filler
3. **Specificity** - precise, not `data`, `info`, `manager`, or `handleStuff`
4. **Brevity** - short but not cryptic
5. **Searchability** - unique enough to find and change safely

**Structure:**

- Keep functions focused on one clear job.
- Make the main control flow easy to scan.
- Prefer guard clauses when they clarify terminal paths.
- Wrap primitives when they represent meaningful domain concepts, rules, or units.
- Use first-class collections when collection rules need a home.
- Avoid deep object chains that couple callers to internals.
- Keep entities small enough to understand; treat size as a signal, not a hard limit.
- Prefer behavior-rich objects over getter/setter data bags for domain logic.

See:

- `references/clean-code/RULES.md`
- `references/clean-code/naming-and-clarity.md`
- `references/clean-code/functions-and-control-flow.md`
- `references/clean-code/object-calisthenics.md`

### 4. Design With Responsibility In Mind

Ask these questions for important classes, modules, services, and boundaries:

1. "What role does this object/module play?"
2. "Is it doing too much?"
3. "Where should this behavior live?"
4. "Which invariant or contract must this protect?"
5. "Does this depend on a stable policy or a replaceable detail?"

**Object stereotypes:**

- **Information Holder** - holds data with minimal behavior
- **Structurer** - manages relationships between objects
- **Service Provider** - performs work, often stateless
- **Coordinator** - orchestrates multiple collaborators
- **Controller** - receives input, delegates work, returns results
- **Interfacer** - transforms data between systems

See:

- `references/object-oriented-design/RULES.md`
- `references/object-oriented-design/object-oriented-design.md`

### 5. Manage Complexity Ruthlessly

**Essential complexity** is inherent to the problem domain.

**Accidental complexity** is introduced by our solution and should be minimized.

Detect complexity through:

- Change amplification: small change means many files
- Cognitive load: hard to understand or explain
- Unknown unknowns: surprising behavior or hidden coupling

Fight complexity with:

- **YAGNI** - do not build what is not needed now
- **KISS** - prefer the simplest solution that works
- **DRY with judgment** - wait for a real shared concept before abstracting
- Small steps, fast feedback, and clear boundaries

See:

- `references/clean-code/RULES.md`
- `references/clean-code/complexity.md`

### 6. Architect For Change

**Vertical slicing:**

- Features are end-to-end slices
- Each feature owns the behavior it needs
- Cross-cutting abstractions emerge from repeated pressure

**Horizontal decoupling:**

- Layers do not know each other's internals
- Dependencies point toward stable domain policy
- Infrastructure depends on domain where the project architecture requires it, not the reverse

**The dependency rule:**

- Source code dependencies should point toward high-level policies
- Frameworks, databases, external services, and transport details should stay replaceable where that matters

See:

- `references/object-oriented-design/solid-principles.md`
- `references/clean-code/complexity.md`

### 7. Add REST API Standards For REST Work

For REST API creation or changes, apply REST rules in addition to every baseline rule above.

Use REST standards to design:

- Resource modeling
- HTTP semantics
- Validation and errors
- Querying and responses
- Versioning and security
- Documentation and operations

See:

- `references/rest-api-design/RULES.md`
- `references/rest-api-design/resource-modeling.md`
- `references/rest-api-design/http-semantics.md`
- `references/rest-api-design/validation-and-errors.md`
- `references/rest-api-design/querying-and-responses.md`
- `references/rest-api-design/versioning-and-security.md`
- `references/rest-api-design/documentation-and-operations.md`

## The Four Elements Of Simple Design

In priority order:

1. **Works correctly** - passes the relevant checks and handles the required behavior
2. **Expresses intent** - readable names and obvious structure
3. **No meaningful duplication** - remove repeated behavior after the shared concept is clear
4. **Minimal** - fewest concepts, files, classes, and methods necessary

## Code Smell Detection

**Stop and inspect when you see:**

| Smell | Response |
|-------|----------|
| Long Method | Extract named steps when they clarify behavior |
| Large Class | Split responsibilities by reason to change |
| Long Parameter List | Introduce a parameter object when values travel together |
| Divergent Change | Split concerns that change for different reasons |
| Shotgun Surgery | Move related behavior closer together |
| Feature Envy | Move behavior toward the data owner |
| Data Clumps | Name the grouped concept |
| Primitive Obsession | Wrap domain concepts when rules or units matter |
| Switch Statements | Consider polymorphism or strategy when behavior varies by type |
| Parallel Inheritance | Simplify or merge the hierarchy when possible |
| Speculative Generality | Remove unused abstraction |

See: `references/clean-code/code-smells.md`

## Design Patterns Awareness

**Creational:** Singleton, Factory, Builder, Prototype

**Structural:** Adapter, Decorator, Composite, Proxy

**Behavioral:** Strategy, Observer, Template Method, Command

**Warning:** Do not force patterns. Let them emerge from real design pressure.

See: `references/object-oriented-design/design-patterns.md`

## Testing Strategy

**Test types, from inner to outer:**

1. **Unit tests** - single class/function, fast, isolated
2. **Integration tests** - multiple components together
3. **E2E/acceptance tests** - full system, user perspective

**Arrange-Act-Assert pattern:**

```typescript
// Arrange - set up test state
const calculator = new Calculator();

// Act - execute the behavior
const result = calculator.add(2, 3);

// Assert - verify the outcome
expect(result).toBe(5);
```

**Test naming:**

Use concrete examples, not abstract statements.

```typescript
// Avoid: "can add numbers"
// Prefer: "when adding 2 + 3, returns 5"
```

Create or update tests when behavior changes, risk is meaningful, or a bug needs reproduction.

## Behavioral Principles

- **Tell, Don't Ask** - command objects, do not query and decide from the outside
- **Design by Contract** - make preconditions, postconditions, invariants, and failure behavior clear
- **Hollywood Principle** - "Don't call us, we'll call you" for inversion of control
- **Law of Demeter** - talk to immediate collaborators; avoid reaching through object graphs
- **Dependency Inversion** - high-level policy should not be trapped inside low-level details

## Pre-Code Checklist

Before writing ANY code, answer:

1. [ ] Do I understand the requirement and acceptance criteria?
2. [ ] What behavior needs to change?
3. [ ] What checks or tests will verify it?
4. [ ] What is the simplest solution?
5. [ ] What patterns might apply? Do not force them.
6. [ ] Am I solving a real problem or a hypothetical one?

## During-Code Checklist

While coding, continuously ask:

1. [ ] Is this the simplest thing that could work?
2. [ ] Does this class/module/function have a clear responsibility?
3. [ ] Am I depending on abstractions or concrete details for a good reason?
4. [ ] Can I name this more clearly?
5. [ ] Is there duplication I should leave alone until the concept is clear?
6. [ ] Are failure modes and edge cases visible where callers need them?

## Post-Code Checklist

After the code works:

1. [ ] Do relevant tests/checks pass?
2. [ ] Is there any unused code created by this change to remove?
3. [ ] Can I simplify any complex conditions?
4. [ ] Are names still accurate after changes?
5. [ ] Are comments/docs still true?
6. [ ] Would another developer understand this in six months?

## Red Flags - Stop And Rethink

- Writing code without understanding the behavior being changed
- Method or class size hiding multiple responsibilities
- More nesting than the main path needs
- Hardcoding values that belong in project configuration or domain rules
- Creating abstractions before repeated behavior reveals a stable concept
- Adding features "just in case"
- Depending on concrete implementations from high-level policy without a project reason
- Data bags that force callers to own domain behavior
- REST APIs with action URLs, unstable error shapes, unbounded collections, or unclear authorization

## Remember

> "A little bit of duplication is 10x better than the wrong abstraction."

> "Focus on WHAT needs to happen, not HOW it happens internally."

Design principles become second nature through practice. The journey is:

Code-first -> Best-practice-first -> Pattern-first -> Responsibility-first -> **Systems Thinking**

Your goal is systems thinking: principles are internalized, and you optimize the entire development process instead of only the next line of code.
