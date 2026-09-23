# Design Patterns

Design patterns are names for recurring solutions. Use them as shared vocabulary after the design pressure is real, not as goals to satisfy.

## Decision Rule

Use a pattern only when all are true:

- The problem is recurring or likely to vary in a known way.
- The pattern removes more complexity than it adds.
- The team and surrounding code already understand the shape or can read it easily.
- A direct implementation would be riskier, more duplicated, or harder to change.

If naming the pattern makes the code larger, less local, or harder to verify, use the simpler design.

## Pattern Decision Table

| Pattern | Use When | Do Not Use When | Small Recognition Example |
| --- | --- | --- | --- |
| Factory | Creation has real branching, validation, dependencies, or subtype selection. | Construction is already clear at the call site. | `createPaymentMethod(type, config)` hides provider-specific setup. |
| Builder | Construction has many optional or staged values and invalid combinations are easy. | A normal constructor or options object is readable. | `ReportBuilder.withSections(...).forPeriod(...).build()` protects required order. |
| Adapter | External or legacy interfaces should not leak into domain code. | Both sides can use the same interface directly. | `StripeChargeAdapter` exposes the local `PaymentGateway` contract. |
| Decorator | Behavior wraps an existing operation without changing its core logic. | The wrapped behavior is mandatory and belongs in the object itself. | `CachedRepository` wraps `Repository` without changing callers. |
| Proxy | Access needs lazy loading, remote calls, caching, permissions, or instrumentation. | It only hides a simple direct call. | `AuthorizingClient` checks access before delegating. |
| Composite | Individual items and groups should support the same operation. | Groups have different behavior or simpler collection handling is enough. | `Folder.size()` and `File.size()` share a component interface. |
| Strategy | A policy or algorithm varies by context and callers should not branch on type. | There are only one or two stable branches and a direct conditional is clearer. | `PricingStrategy.calculate(order)` swaps pricing rules. |
| Observer | State changes need decoupled subscribers. | Call order, consistency, or failure handling must be tightly controlled. | `OrderPlaced` notifies email, analytics, and fulfillment listeners. |
| Command | Actions need queuing, undo, retry, logging, or uniform dispatch. | The action is a simple method call with no lifecycle. | `ShipOrderCommand` can be queued and retried. |
| Template Method | An algorithm skeleton is stable but a few steps vary in subclasses. | Composition or callbacks would make variation clearer. | `Importer.run()` fixes parse/validate/save order. |
| Singleton | Exactly one shared instance is required by the domain or platform. | You only want convenient global access. Prefer dependency injection. | A process-wide clock or config object is injected, not fetched globally. |
| Prototype | Cloning a configured object is clearer than rebuilding it. | Construction is cheap and explicit. | Copy a preconfigured document style before changing a few fields. |

## Before Applying A Pattern

- Name the variation or coupling problem the pattern solves.
- Check whether a direct function, object, or dependency injection is enough.
- Keep the public contract smaller than the implementation detail it hides.
- Add or keep tests around the behavior that varies.

## Red Flags

- Pattern names appear in class names before there is variation.
- A new interface has only one implementation and no boundary value.
- The pattern moves simple logic far from where it is used.
- The pattern exists to anticipate an extension that has not arrived.

For smell diagnosis, use [../clean-code/code-smells.md](../clean-code/code-smells.md).
