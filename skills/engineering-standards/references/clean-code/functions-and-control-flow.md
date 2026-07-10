# Functions And Control Flow

Functions should do one clear job, and control flow should make the main path easy to scan. Prefer simple structure over clever expressions.

## Function And Flow Rules

| Rule | Use | Red Flag |
| --- | --- | --- |
| Keep functions focused | Separate validation, building, persistence, network calls, formatting, and rendering when they are distinct responsibilities. | One function mixes several kinds of work or cannot be described in one sentence. |
| Prefer guard clauses | Return or throw early for terminal cases so the normal path stays visible. | Pyramid-shaped nesting hides the main path. |
| Avoid meaning-changing flags | Split behavior when a boolean or enum changes what the function fundamentally does. | A boolean argument forces callers to remember hidden meaning. |
| Prefer straightforward flow | Split dense expressions when behavior, ordering, or side effects matter. | Side effects hide inside chains that look like data transformation. |

## Checks

- Can the function be described in one sentence?
- Does it mix multiple kinds of work?
- Is the happy path visible without reading several nested blocks?
- Are flags hiding separate workflows or tests?
- Would simpler control flow make review safer?
