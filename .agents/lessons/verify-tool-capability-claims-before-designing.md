# Verify Tool Capability Claims Before Designing Around Them

## Mistake Pattern

I asserted from memory that a tool lacked a capability — "Codex has no per-tool-call hook like Claude Code's PostToolUse" — and built a design decision on it (framing the edit-tier hook as Claude-only). The claim was wrong; Codex does support PostToolUse hooks, and the user had to correct me.

## Rule

Before designing around a "tool X can't do Y" claim, verify it against the tool's current documentation. Agent and LLM tooling changes faster than the knowledge cutoff, so a remembered capability limit is often stale. State such limits as something to check, then confirm, instead of asserting them as fact. A wrong negative is expensive: it produces an architecture built on a constraint that does not exist.
