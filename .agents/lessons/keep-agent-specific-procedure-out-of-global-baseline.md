# Keep Agent-Specific Procedure Out Of Global Baseline

## Mistake Pattern

I duplicated a detailed procedure for one subagent inside `AGENTS.md`, making the global baseline more specific than it needed to be.

## Rule

Keep `AGENTS.md` focused on shared orchestration and project-wide rules. Put detailed instructions for a specific subagent in that subagent prompt, and keep only general storage or coordination rules in the baseline.
