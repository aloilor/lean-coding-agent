# Determinism-in-the-Loop Pipeline

> **Deferred TODO:** The full-repository quality-gate integration described below is not
> active in current agent workflows. The implementation and design notes remain in the
> repository for later evaluation.

A stack-agnostic model for keeping AI-written code out of the "code slop" trap: rising duplication and falling refactoring as generated code accumulates. The core idea: LLMs catch their own slop poorly but fix it well **once something points at it**, so pair the model with deterministic, mechanical checks that do the pointing.

## Three layers

Each layer catches what the one below it cannot. They are complementary, not substitutes.

- **Lint = tidiness.** Syntactic, per-file, fast: formatting, unused symbols, simple anti-patterns.
- **Static analysis = structural floor (ratcheted).** Semantic and often whole-program: complexity, cross-module duplication, dependency direction, dead code, type flow, taint. This is the layer that actually *measures* slop.
- **Agent review = semantic judgment.** The wrong abstraction, a misnamed concept, subtly-wrong logic, a leaky interface — the things no tool can see.

Determinism raises the floor cheaply and objectively; it never reaches the ceiling. The review layer is where the expensive judgment is spent — and it should be spent on the ceiling, not on re-deriving what a linter already said.

## Two tiers

Placement follows a single property: **is the check meaningful on one file, or does it need the whole graph?**

- **Proposed review tier (deferred).** A future reviewer integration may run one local full-repository gate containing style, static analysis and complexity, tests, duplication, architecture, and dependency audit. Current workflows do not run this gate.
- **CI-class analyses (whole-repo, ratcheted).** Duplication, architecture / dependency direction, dead code, and security need the whole graph. They remain CI-class analyses if a future local gate executes them against the exact worktree under review; scoping them to touched files destroys what they measure.

### The ratchet

You cannot hard-fail a check against an existing messy repo — every file trips it on day one. The ratchet fixes this: record the current metric as a baseline, grandfather existing debt, and block only **regressions**. New code may not make duplication / complexity / type errors worse; existing debt can only trend down. Whole-repo static analysis is only deployable in ratcheted form.

The ratcheted complexity policy and reviewer integration remain future design work.

## Deferred placement proposal

Static-analysis findings are deterministic and already-true; they do not need to be rediscovered through semantic judgment. If this TODO is resumed, the proposed ownership is one fresh, explicit gate execution for the exact worktree under review:

```
implementer ── implement + run behavior verification ──► handoff
      ▼
reviewer ── inventory diff, then run full deterministic gate ──► fresh manifest + reports
      • AUDIT baseline, threshold, ruleset, ignore, and dependency-policy diffs
        — were findings SUPPRESSED instead of fixed?
        (gaming the ratchet is the highest-signal thing a reviewer can catch)
      • CORRELATE static hotspots with the smells it spots
      • does NOT re-list mechanical findings as its own discoveries
      • spends its budget on SEMANTIC review
      • returns blocking gate findings to the implementer for the next pass
```

In the deferred design, the deterministic gate is the reviewer's **instrument panel**, not its **assignment**. None of these responsibilities apply to current workflows.

**Inspection breadth is not fix scope.** Whole-project analysis and semantic review may inspect untouched callers, dependencies, and neighboring code to determine whether the implementation caused a regression. That broader inspection does not authorize cleanup. The reviewer returns change-caused findings in touched files, plus unresolved explicitly in-scope target findings named by the task, specification, bug investigation, refactor brief, or implementation plan, for the implementer to fix. New findings that ripple into *untouched* files are flagged as review findings but not assigned as implementation scope without approval. Pre-existing unrelated findings are the baseline's job, not the change's.

The main risk is an extra review round-trip when the reviewer is the first explicit consumer of a mechanical finding. In exchange, there is one authoritative run and no handoff ambiguity about artifact freshness. Auditing the baseline diff still catches an implementer suppressing a finding instead of fixing it.

## Cross-tool enforcement

Enforcement can sit at three layers. The distinction that matters: a hook in one agent's config covers that agent only — never humans or a different tool — while a git hook covers everything that commits.

| Layer | Mechanism | Covers | Role |
|-------|-----------|--------|------|
| Agent workflow (deferred) | future reviewer integration | reviewers | would run the gate once per review pass and use fresh findings |
| Commit gate | git `pre-commit` running the gate | Claude Code + Codex + **humans** | a hard, human-covering stop |
| Hosted CI | CI service running the same project scripts for each pushed commit | every pushed worktree | independent remote enforcement |

No current workflow calls `scripts/quality-gate`. A future reviewer integration or git `pre-commit` could call the same script, but neither is provisioned by this baseline.

**A future reviewer-only vs. hard-gate choice must be deliberate.** The PHP/Laravel reference assets ship without active workflow integration, PostToolUse hooks, or git hooks. Adding reviewer execution or a git `pre-commit` would activate a new ownership and enforcement model.

## The honest ceiling

This pipeline catches **structural** slop — too complex, duplicated, tangled, dead, unsafe, mistyped. It does **not** catch **semantic** slop. That stays with the reviewer and with `engineering-standards`. The full stack is the floor and the ceiling working together, not the floor pretending to be both.

## Concrete implementation

See `templates/php-laravel/` in the coding-agent baseline and its `docs/quality-pipeline.md` for the retained experimental PHP/Laravel implementation: Pint, PHPStan/Larastan with cognitive complexity, tests, jscpd, Deptrac, and Composer audit with committed ratchets where needed.
