# Determinism-in-the-Loop Pipeline

A stack-agnostic model for keeping AI-written code out of the "code slop" trap: rising duplication and falling refactoring as generated code accumulates. The core idea: LLMs catch their own slop poorly but fix it well **once something points at it**, so pair the model with deterministic, mechanical checks that do the pointing.

## Three layers

Each layer catches what the one below it cannot. They are complementary, not substitutes.

- **Lint = tidiness.** Syntactic, per-file, fast: formatting, unused symbols, simple anti-patterns.
- **Static analysis = structural floor (ratcheted).** Semantic and often whole-program: complexity, cross-module duplication, dependency direction, dead code, type flow, taint. This is the layer that actually *measures* slop.
- **Agent review = semantic judgment.** The wrong abstraction, a misnamed concept, subtly-wrong logic, a leaky interface — the things no tool can see.

Determinism raises the floor cheaply and objectively; it never reaches the ceiling. The review layer is where the expensive judgment is spent — and it should be spent on the ceiling, not on re-deriving what a linter already said.

## Two tiers

Placement follows a single property: **is the check meaningful on one file, or does it need the whole graph?**

- **Review tier.** Style, complexity, and per-file type checks run once after the reviewer inventories the diff. Findings become inputs to semantic review and blocking findings return through the review-fix loop.
- **Commit / CI tier (whole-repo, ratcheted).** Duplication, architecture / dependency direction, dead code, security. These are *relationships between* files — scoping them to touched files destroys what they measure, so they stay whole-repo.

### The ratchet

You cannot hard-fail a check against an existing messy repo — every file trips it on day one. The ratchet fixes this: record the current metric as a baseline, grandfather existing debt, and block only **regressions**. New code may not make duplication / complexity / type errors worse; existing debt can only trend down. Whole-repo static analysis is only deployable in ratcheted form.

The shared `code-reviewer` instruction owns the exact ratcheted complexity acceptance policy and applies it to the fresh gate artifact during review.

## Placement: reviewer runs, implementer fixes returned findings

Static-analysis findings are deterministic and already-true; they do not need to be rediscovered through semantic judgment. The reviewer owns one fresh, explicit gate execution for the exact worktree under review:

```
implementer ── implement + run behavior verification ──► handoff
      ▼
reviewer ── inventory diff, then run deterministic gate ──► fresh findings
      • AUDIT the baseline diff — were findings SUPPRESSED instead of fixed?
        (gaming the ratchet is the highest-signal thing a reviewer can catch)
      • CORRELATE static hotspots with the smells it spots
      • does NOT re-list mechanical findings as its own discoveries
      • spends its budget on SEMANTIC review
      • returns blocking gate findings to the implementer for the next pass
```

Static analysis is the reviewer's **instrument panel**, not its **assignment**. Running the gate after inventorying the diff makes that instrument panel independent and current. Blocking findings return through the normal review-fix loop.

**Fix scope.** When analysis is whole-project, the artifact holds findings beyond the change. The reviewer returns change-caused findings in touched files, plus unresolved explicitly in-scope target findings named by the task, specification, bug investigation, refactor brief, or implementation plan, for the implementer to fix. New findings that ripple into *untouched* files are flagged as review findings but not assigned as implementation scope without approval. Pre-existing unrelated findings are the baseline's job, not the change's.

The main risk is an extra review round-trip when the reviewer is the first explicit consumer of a mechanical finding. In exchange, there is one authoritative run and no handoff ambiguity about artifact freshness. Auditing the baseline diff still catches an implementer suppressing a finding instead of fixing it.

## Cross-tool enforcement

Enforcement can sit at three layers. The distinction that matters: a hook in one agent's config covers that agent only — never humans or a different tool — while a git hook covers everything that commits.

| Layer | Mechanism | Covers | Role |
|-------|-----------|--------|------|
| Agent workflow | shared `code-reviewer` instruction, installed to both `.claude/agents/` and `.codex/agents/` | reviewers | runs the gate once per review pass and uses fresh findings |
| Commit gate | git `pre-commit` running the gate | Claude Code + Codex + **humans** | a hard, human-covering stop |

The reviewer calls `scripts/quality-gate` directly. A git `pre-commit` can call the same script when hard enforcement for humans and other tools is wanted, but it is not provisioned by this baseline.

**Reviewer-only vs. hard gate is a deliberate choice.** The PHP/Laravel reference implementation ships with reviewer-only execution and no PostToolUse or git hooks. Adding a git `pre-commit` changes that ownership model by upgrading the script to a hard, human-covering gate.

## The honest ceiling

This pipeline catches **structural** slop — too complex, duplicated, tangled, dead, unsafe, mistyped. It does **not** catch **semantic** slop. That stays with the reviewer and with `engineering-standards`. The full stack is the floor and the ceiling working together, not the floor pretending to be both.

## Concrete implementation

See `templates/php-laravel/` in the coding-agent baseline and its `docs/quality-pipeline.md` for a worked PHP/Laravel instance (Laravel Pint + PHPStan/Larastan + cognitive-complexity rule, ratcheted via `phpstan-baseline.neon`, run explicitly by the code reviewer).
