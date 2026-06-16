# Object-Oriented Design Rules

Load this file for object responsibilities, boundaries, SOLID, inheritance, polymorphism, patterns, and architecture decisions. Open details only when a rule applies.

## Object Design Rules

| Rule | Summary | Details |
|------|---------|---------|
| Use Responsibility-Driven Design | Find objects by candidates, stereotypes, and responsibilities rather than by data alone. | [object-oriented-design.md](./object-oriented-design.md) |
| Find Objects Deliberately | Look for nouns, external actors, domain concepts, and system events that need behavior. | [object-oriented-design.md](./object-oriented-design.md) |
| Find Responsibilities | Each object should know what it owns and what it can do. | [object-oriented-design.md](./object-oriented-design.md) |
| Use Object Stereotypes | Distinguish information holders, structurers, service providers, coordinators, controllers, and interfacers. | [object-oriented-design.md](./object-oriented-design.md) |
| Ask The Two Questions | Ask what each object knows and what it does. | [object-oriented-design.md](./object-oriented-design.md) |
| Tell, Don't Ask | Command objects to perform behavior instead of pulling data out and deciding externally. | [object-oriented-design.md](./object-oriented-design.md) |
| Design By Contract | Make preconditions, postconditions, and invariants explicit where callers rely on them. | [object-oriented-design.md](./object-oriented-design.md) |
| Prefer Composition Over Inheritance | Use inheritance only for stable is-a relationships; prefer composition for flexible behavior. | [object-oriented-design.md](./object-oriented-design.md) |
| Follow The Law Of Demeter | Talk to immediate collaborators instead of reaching through object graphs. | [object-oriented-design.md](./object-oriented-design.md) |
| Encapsulate Behavior And State | Hide internals and expose operations that protect invariants. | [object-oriented-design.md](./object-oriented-design.md) |
| Use Polymorphism For Type Behavior | Replace type checks with polymorphism when behavior genuinely varies by subtype. | [object-oriented-design.md](./object-oriented-design.md) |
| Model Value Objects | Use immutable value-based objects for concepts like money, email, ranges, and units. | [object-oriented-design.md](./object-oriented-design.md) |
| Model Entities | Use identity-based objects when lifecycle and identity matter more than attributes. | [object-oriented-design.md](./object-oriented-design.md) |
| Use Aggregates To Protect Invariants | Keep clusters of related entities consistent through an aggregate root. | [object-oriented-design.md](./object-oriented-design.md) |

## SOLID Rules

| Rule | Summary | Details |
|------|---------|---------|
| Single Responsibility Principle | A class or module should have one clear reason to change. | [solid-principles.md](./solid-principles.md) |
| Open/Closed Principle | Add new behavior through extension when that lowers risk. | [solid-principles.md](./solid-principles.md) |
| Liskov Substitution Principle | Subtypes must honor the base contract without surprising callers. | [solid-principles.md](./solid-principles.md) |
| Interface Segregation Principle | Clients should depend only on methods they actually use. | [solid-principles.md](./solid-principles.md) |
| Dependency Inversion Principle | High-level policy should depend on abstractions, not concrete details. | [solid-principles.md](./solid-principles.md) |
| Dependency Rule | Source dependencies should point inward toward stable domain policy where architecture requires it. | [solid-principles.md](./solid-principles.md) |
| Apply SOLID At Architecture Level | Use SOLID to shape bounded contexts, modules, services, and infrastructure boundaries. | [solid-principles.md](./solid-principles.md) |

## Pattern Rules

| Rule | Summary | Details |
|------|---------|---------|
| Don't Force Patterns | Patterns should solve real problems, not anticipated ones. | [design-patterns.md](./design-patterns.md) |
| Use Patterns When They Fit | Use a pattern when the problem is recognized, the fit is natural, it simplifies, and the team understands it. | [design-patterns.md](./design-patterns.md) |
| Singleton | Use only when one shared instance is truly needed; prefer dependency injection otherwise. | [design-patterns.md](./design-patterns.md) |
| Factory | Use when creation logic is complex or varies by type. | [design-patterns.md](./design-patterns.md) |
| Builder | Use when constructing objects with many optional or staged parameters. | [design-patterns.md](./design-patterns.md) |
| Prototype | Use when cloning configured objects is clearer than reconstructing them. | [design-patterns.md](./design-patterns.md) |
| Adapter | Translate one interface into another without leaking external shapes. | [design-patterns.md](./design-patterns.md) |
| Decorator | Add behavior around an object without changing its core implementation. | [design-patterns.md](./design-patterns.md) |
| Proxy | Control access, caching, lazy loading, or remote calls through a stand-in object. | [design-patterns.md](./design-patterns.md) |
| Composite | Treat individual objects and groups uniformly when they share behavior. | [design-patterns.md](./design-patterns.md) |
| Strategy | Swap algorithms or policies behind a stable interface. | [design-patterns.md](./design-patterns.md) |
| Observer | Notify subscribers when state changes without tight coupling. | [design-patterns.md](./design-patterns.md) |
| Template Method | Keep an algorithm skeleton stable while subclasses fill specific steps. | [design-patterns.md](./design-patterns.md) |
| Command | Represent an action as an object for queuing, undo, logging, or dispatch. | [design-patterns.md](./design-patterns.md) |
| Use Pattern Awareness | Consider intent, participants, collaboration, and consequences before naming a pattern. | [design-patterns.md](./design-patterns.md) |
| Avoid Pattern Anti-Patterns | Watch for God Object, Spaghetti Code, Golden Hammer, premature optimization, and copy-paste programming. | [design-patterns.md](./design-patterns.md) |
