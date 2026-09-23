# Naming And Clarity

Names should reveal intent, domain meaning, and scope. A reader should not need to reverse-engineer implementation to understand what a value, function, class, or module means.

## Naming Rules

| Rule | Use | Red Flag |
| --- | --- | --- |
| Explain intent | Name the role or decision in the current context. | `data`, `result`, `tmp`, `handle`, or `process` outside tiny scopes. |
| Prefer domain language | Use product and business terms for business behavior. | Storage, transport, or framework words leaking into domain code. |
| Match name to scope | Short names are fine in tiny obvious scopes; public and long-lived names need precision. | A vague name travels across functions, modules, or API boundaries. |
| Make flow read like a story | Use names and small helpers so the main path is a sequence of intentions. | Readers must parse low-level mechanics before understanding the workflow. |

## Checks

- Would a new teammate understand the name without reading the implementation?
- Would a better name remove a nearby explanatory comment?
- Does domain code use domain words?
- Is the name precise enough for how far it travels?
- Can the main flow be understood by reading names alone?
