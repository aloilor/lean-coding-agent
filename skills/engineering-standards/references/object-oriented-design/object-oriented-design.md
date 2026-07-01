# Object-Oriented Design

Object-oriented design is useful when behavior, state, identity, collaboration, or invariants need clear homes. Do not force objects or patterns where simple functions or data are clearer.

## Responsibility Checklist

For each unit, ask:

- What does it know?
- What does it do?
- What does it decide?
- What invariant or contract does it protect?
- What should callers not need to know about its internals?

Use stereotypes such as entity, value object, coordinator, service provider, or gateway only as optional vocabulary after responsibilities are clear.

## Tell, Do Not Ask

Prefer asking an object for an outcome over pulling out its data and making the decision elsewhere.

Good pressure:

- A caller reaches through several properties.
- The same decision appears near the same data in multiple places.
- Callers must know internal state combinations to use an object safely.

Do not hide data blindly. Serialization, persistence mapping, UI display, and framework boundaries may legitimately expose data shapes.

## Encapsulation

Encapsulation means protecting useful invariants behind a clear contract.

- Keep state private when direct mutation would break rules.
- Expose operations that preserve valid transitions.
- Keep validation near the concept it protects.
- Avoid getter/setter objects that force callers to own domain behavior.

## Composition And Inheritance

Prefer composition when behavior varies independently or can be assembled from collaborators.

Use inheritance only when:

- The subtype is truly substitutable for the base type.
- The base contract is stable and tested.
- Shared behavior is real, not just shared fields.

If a subtype needs to disable parent behavior or surprise callers, use composition instead.

## Law Of Demeter

Talk to immediate collaborators rather than reaching through object graphs.

Risky:

```text
order.customer.account.billingAddress.country
```

Prefer a named operation near the owner of the knowledge:

```text
order.billingCountry()
```

Use this to reduce coupling, not to add layers of pass-through methods.

## Polymorphism

Use polymorphism when behavior genuinely varies by type and branches are growing, volatile, or repeated.

Prefer a simple conditional when:

- There are only one or two stable cases.
- The branch is local and easy to test.
- A new hierarchy would hide more than it clarifies.

## Domain Modeling

Use richer domain models when they protect rules or clarify behavior:

| Concept | Use When | Avoid When |
| --- | --- | --- |
| Value object | Equality is value-based and validation, units, or formatting matter. | A primitive is clear and has no rules. |
| Entity | Identity and lifecycle matter more than attributes. | The data is transient or has no behavior. |
| Aggregate | A cluster of objects must stay consistent through one root. | Simple persistence or flat data is enough. |

Keep domain-driven design terms optional. They should clarify real domain complexity, not add ceremony to ordinary code.

## Pattern Question

Ask "Is a known pattern already present or clearly simplifying this?" only after a real design pressure appears. For pattern selection, use [design-patterns.md](./design-patterns.md).
