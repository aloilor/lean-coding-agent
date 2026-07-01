# Determinism-in-the-Loop Pipeline

A stack-agnostic model for keeping AI-written code out of the "code slop" trap:
rising duplication and falling refactoring as generated code accumulates. The
core idea: LLMs catch their own slop poorly but fix it well **once something
points at it**, so pair the model with deterministic, mechanical checks that do
the pointing.

## Three layers

Each layer catches what the one below it cannot. They are complementary, not
substitutes.

- **Lint = tidiness.** Syntactic, per-file, fast: formatting, unused symbols,
  simple anti-patterns.
- **Static analysis = structural floor (ratcheted).** Semantic and often
  whole-program: complexity, cross-module duplication, dependency direction,
  dead code, type flow, taint. This is the layer that actually *measures* slop.
- **Agent review = semantic judgment.** The wrong abstraction, a misnamed
  concept, subtly-wrong logic, a leaky interface — the things no tool can see.

Determinism raises the floor cheaply and objectively; it never reaches the
ceiling. The review layer is where the expensive judgment is spent — and it
should be spent on the ceiling, not on re-deriving what a linter already said.

## Two tiers

Placement follows a single property: **is the check meaningful on one file, or
does it need the whole graph?**

- **Edit tier (fast, scoped to touched files).** Style, complexity, and
  per-file type checks. Runs in the implementer's inner loop. Findings should
  reach review *already fixed*, not freshly reported.
- **Commit / CI tier (whole-repo, ratcheted).** Duplication, architecture /
  dependency direction, dead code, security. These are *relationships between*
  files — scoping them to touched files destroys what they measure, so they
  stay whole-repo.

### The ratchet

You cannot hard-fail a check against an existing messy repo — every file trips
it on day one. The ratchet fixes this: record the current metric as a baseline,
grandfather existing debt, and block only **regressions**. New code may not make
duplication / complexity / type errors worse; existing debt can only trend down.
Whole-repo static analysis is only deployable in ratcheted form.

## Placement: implementer fixes, reviewer audits

Static-analysis findings are deterministic and already-true; they do not need
the reviewer's *judgment*. So the **implementer** is the first consumer, not the
reviewer:

```
implementer ── run deterministic gate (fast, scoped) ──► fix, or baseline
      │
      │  emits: ONE artifact with all static-analysis findings + the baseline diff
      ▼
reviewer ── receives the report as READ-ONLY context ──►
      • AUDIT the baseline diff — were findings SUPPRESSED instead of fixed?
        (gaming the ratchet is the highest-signal thing a reviewer can catch)
      • CORRELATE static hotspots with the smells it spots
      • does NOT re-list mechanical findings as its own discoveries
      • spends its budget on SEMANTIC review
```

Static analysis is the reviewer's **instrument panel**, not its **assignment**.

**Fix scope.** When analysis is whole-project, the artifact holds findings beyond
the change. The implementer fixes only findings **its change caused in the files
it touched**. New findings the change ripples into *untouched* files (a caller it
did not open) are **flagged for the reviewer, not fixed** — this keeps edits
scoped without silently shipping a regression. Pre-existing unrelated findings
are the baseline's job, not the change's.

Two failure modes this ordering avoids:

1. **Reviewer-as-slow-linter** — spending a full review round-trip to surface a
   complexity violation the gate could have bounced back in seconds.
2. **Baseline gaming** — an implementer making the gate green by *suppressing* a
   finding into the baseline instead of fixing it. If the reviewer only sees
   "gate passed," this is invisible; auditing the baseline diff catches it.

## Cross-tool enforcement

Enforcement can sit at three layers. The distinction that matters: a hook in one
agent's config covers that agent only — never humans or a different tool — while
a git hook covers everything that commits.

| Layer | Mechanism | Covers | Role |
|-------|-----------|--------|------|
| Edit-tier hook | PostToolUse on `Edit`/`Write` — Claude Code `.claude/settings.json` **and** Codex `.codex/hooks.json` (same `{"hooks":{"PostToolUse":[…]}}` shape, both act on exit 2) | Claude Code + Codex | fast advisory feedback per edit |
| Agent workflow | shared `implementer` / `code-reviewer` instructions, installed to both `.claude/agents/` and `.codex/agents/` | agents | puts findings in the loop before handoff |
| Commit gate | git `pre-commit` running the gate | Claude Code + Codex + **humans** | a hard, human-covering stop |

The edit-tier hooks and the commit gate call the **same** gate script
(`scripts/quality-gate`), so the check is defined once. The severity differs by
trigger: a PostToolUse hook fires *after* the edit landed, so its exit 2 informs
the model rather than undoing anything (advisory); a git `pre-commit` turns the
same failure into a hard stop and is the only layer that also covers humans and
other tools.

**Agent-only vs. hard gate is a deliberate choice.** The two edit-tier hooks give
cross-*agent* enforcement without touching anyone's git workflow. Adding the git
`pre-commit` upgrades that to a hard, human-covering gate. The PHP/Laravel
reference implementation ships **agent-only** (PostToolUse hooks, no git hook);
the commit gate is documented as the next layer to add when a hard stop is wanted.

## The honest ceiling

This pipeline catches **structural** slop — too complex, duplicated, tangled,
dead, unsafe, mistyped. It does **not** catch **semantic** slop. That stays with
the reviewer and with `engineering-standards`. The full stack is the floor and
the ceiling working together, not the floor pretending to be both.

## Concrete implementation

See `templates/php-laravel/` in the coding-agent baseline and its
`QUALITY-PIPELINE.md` for a worked PHP/Laravel instance (Laravel Pint +
PHPStan/Larastan + cognitive-complexity rule, ratcheted via
`phpstan-baseline.neon`, enforced agent-only through Claude Code and Codex
PostToolUse hooks).
