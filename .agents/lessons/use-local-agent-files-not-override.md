# Use Local Agent Files Not Override

## Mistake Pattern

I named private per-project agent files `AGENTS.override.md` and `CLAUDE.override.md`, which does not match the repo's preferred naming.

## Rule

Use `AGENTS.local.md` and `CLAUDE.local.md` for private, gitignored per-project notes. Do not call these files overrides in bootstrap scripts, documentation, or baseline instructions.
