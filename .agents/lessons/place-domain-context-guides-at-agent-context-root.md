# Place Domain Context Guides At Agent Context Root

## Mistake Pattern

I placed a guide about API design under `agent-context/coding-style/` even though it describes broader project or domain context rather than code formatting or implementation style.

## Rule

Put broad domain, architecture, API, operational, and project-context guides directly under `agent-context/` as their own topic folders. Reserve `agent-context/coding-style/` for guidance about how code should be written at the implementation level.
