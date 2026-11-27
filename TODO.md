# TODO

Open items only, one line each. Delete an item when it's done; git history and [CHANGELOG.md](CHANGELOG.md) keep the record. Put longer designs in `.agents/plans/`. Track each item here or in a GitHub issue, never both.

## Now

## Next

- Replace mandatory implementation reports with a short Implementation Results section in the approved plan covering verification, test-first evidence or exemptions, approved deviations, risks, and omissions; keep separate reports optional for large or multi-implementer work.
- Update the workflows to spawn multiple implementers and reviewers so work runs in parallel.
- Use fresh agents for every implement-review loop pass: spawn a new implementer to address review findings and a new reviewer to check the resulting changes, passing context through durable artifacts instead of resuming previous agents.
- Add adversarial plan review: given a plan, spawn an agent from a different coding system to challenge its assumptions, identify gaps and risks, and suggest improvements (for example, Claude Code reviews a plan drafted by Codex).
- Make workflows modular: extract role skills (plan, orchestrate, implement, code review) that subagents invoke, and that a main agent can also invoke directly to run a whole workflow in one session without subagents.

## Later
