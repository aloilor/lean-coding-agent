# Require Bug Diagnosis Approval Before Implementation

## Mistake Pattern

I let a diagnosis report flow directly into implementation, even though the user wanted to approve the bug fix after diagnosis and before code changes started.

## Rule

When a bug diagnostician produces a diagnosis report, show the diagnosis, proposed fix direction, verification plan, and incident draft to the user. Do not invoke the implementer or begin coding until the user explicitly approves the diagnosis and fix direction.
