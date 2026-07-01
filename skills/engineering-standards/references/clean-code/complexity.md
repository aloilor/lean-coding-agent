# Managing Complexity

Preserve essential domain complexity. Remove accidental complexity introduced by unclear structure, hidden coupling, speculative design, or missing feedback.

## Diagnose First

| Signal | Question | Safer Response |
| --- | --- | --- |
| Change amplification | Does a small behavior change require many edits? | Move the rule to one owner or clarify the boundary. |
| Cognitive load | Is too much state, branching, or indirection needed to understand the code? | Name concepts, split mixed responsibilities, and simplify control flow. |
| Unknown unknowns | Are effects hidden, surprising, or weakly tested? | Make contracts explicit and add focused verification. |
| Coupling | Does one unit know another unit's internals? | Narrow the contract or move behavior to the owner. |
| Speculation | Does code support a future that has not arrived? | Inline, delete, or defer flexibility until there is evidence. |

## Core Heuristics

| Heuristic | Apply It As | Avoid |
| --- | --- | --- |
| KISS | Prefer fewer concepts, branches, states, dependencies, and moving parts. | Clever compression that hides intent. |
| YAGNI | Build only what the current requirement or clear near-term extension needs. | Hooks, options, and error handling for hypothetical scenarios. |
| DRY | Keep repeated business knowledge, invariants, and policies in one place. | Extracting similar-looking code before the shared concept is stable. |
| Separation of concerns | Split validation, domain rules, persistence, presentation, and integration when they change independently. | Splitting cohesive behavior just to satisfy a pattern. |
| Simple design | First make it correct, then expressive, then remove meaningful duplication, then minimize. | Minimizing before behavior and intent are clear. |

## Duplication Judgment

Repeated syntax is not always duplication. Repeated business knowledge usually is.

Extract when:

- The repeated code represents the same policy, invariant, calculation, or contract.
- A bug fix would need to be made in multiple places.
- The shared name would make the domain clearer.

Tolerate local similarity when:

- The branches are likely to change for different reasons.
- The abstraction name would be vague.
- The extraction would make callers understand more indirection than behavior.

## Refactoring Boundary

Refactor only when it is in scope, behavior-preserving, adequately verified, and materially reduces change risk or maintenance cost.

Good reasons:

- The requested change is hard because responsibilities are tangled.
- A small extraction makes the behavior easier to verify.
- A duplicated business rule would make the requested change fragile.

Bad reasons:

- The code merely looks imperfect.
- The cleanup is unrelated to the task.
- Verification is weak and the refactor is not necessary for the requested change.

## Technical Debt

Treat technical debt as a tradeoff, not a mood.

- Name the debt and the cost it creates.
- Isolate it when removal is out of scope.
- Pay it down when it slows current change, increases risk, or blocks verification.
- Mention meaningful out-of-scope debt instead of quietly expanding the patch.
