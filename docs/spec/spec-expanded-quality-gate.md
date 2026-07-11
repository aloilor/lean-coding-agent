# Expanded Reviewer-Owned Quality Gate

## Status

Approved for implementation on 2026-07-11.

## Summary

Expand the PHP/Laravel template's reviewer-owned `scripts/quality-gate` from style and PHPStan only into one full-repository review gate. The code reviewer runs it once per review pass after inventorying the diff. The gate executes every configured check, even after a failure, and produces a fresh manifest that points the reviewer to each check's evidence.

The expanded gate covers:

- formatting;
- static analysis and cognitive complexity;
- the project test suite;
- whole-repository duplication;
- project-defined architecture boundaries; and
- Composer dependency/security audit findings.

This is still a local reviewer workflow step. It does not add a hosted CI workflow, git hook, or automatic human-facing commit gate.

## Context and Problem

The current PHP/Laravel gate runs `quality:style` and `quality:report`, persists only `static-report.json`, and accumulates a single exit status. Duplication, architecture, tests, and dependency audit are described as separate CI-tier concerns and are not available to the reviewer during semantic review.

The reviewer needs one authoritative execution against the exact worktree under review, plus enough structured evidence to distinguish failed, passed, and unavailable checks. Mechanical findings must inform the review without silently expanding the implementer's scope to unrelated repository debt.

## Assumptions

- Target repositories use Composer and define the documented `quality:*` scripts after initialization.
- `jscpd` is installed as a project-local Node development dependency for duplication analysis.
- Deptrac is installed as a Composer development dependency, but each project owns its layer and ruleset configuration. The baseline must not impose a generic Laravel architecture that may contradict the project's design.
- Existing whole-repository duplication and architecture debt is ratcheted in committed tool configuration or baseline files. New suppressions and threshold increases are reviewable changes.
- A skipped check preserves the current non-wedging bootstrap behavior, but the reviewer treats it as missing verification rather than a clean pass.

## Approach

Use the existing POSIX shell gate as a small orchestrator over named Composer scripts. This is the simplest responsible option because Composer remains the project-specific command boundary, while one script owns execution order, freshness, aggregation, and the evidence contract.

The heavier alternative is a new PHP or Python gate runner with a formal report schema library. It would make JSON generation and future extensions easier, but adds a runtime and abstraction that six fixed checks do not yet justify.

The tradeoff is that POSIX shell JSON generation must remain deliberately simple: fixed check names, fixed relative report paths, and controlled status values only.

## Functional Requirements

### FR-1: One reviewer-owned command

`sh scripts/quality-gate` remains the sole workflow command the code reviewer runs. The code reviewer runs it after diff inventory and before semantic review on every review pass.

### FR-2: Fixed check set and order

The gate attempts the following Composer scripts in this order:

1. `quality:style`
2. `quality:static`
3. `quality:test`
4. `quality:duplication`
5. `quality:architecture`
6. `quality:audit`

The documentation supplies concrete PHP/Laravel examples:

- Pint for `quality:style`;
- PHPStan/Larastan plus cognitive-complexity for `quality:static`;
- the Laravel test runner via Sail (`sail artisan test`) for `quality:test`;
- `jscpd` for `quality:duplication`;
- Deptrac for `quality:architecture`; and
- `composer audit --locked --format=json` for `quality:audit`.

Projects may change the implementation behind a script while preserving its name and gate contract.

### FR-3: Continue after failures

A failed check must not prevent later checks from running. The gate exits only after all six checks have been attempted and the manifest has been written.

### FR-4: Fresh evidence directory

At the beginning of every run, the gate recreates `.quality-reports/`. Evidence from a previous run must not survive as apparent current evidence.

Each check receives a stable primary report path and a stable stderr log path under that directory. The gate captures command stdout as the primary report and stderr separately so JSON-producing commands remain machine-readable.

Stable primary paths are:

| Check | Primary report |
| --- | --- |
| style | `.quality-reports/style.txt` |
| static | `.quality-reports/static-analysis.json` |
| tests | `.quality-reports/tests.txt` |
| duplication | `.quality-reports/duplication.txt` |
| architecture | `.quality-reports/architecture.json` |
| audit | `.quality-reports/dependency-audit.json` |

The documentation must require `.quality-reports/` to be ignored. Existing committed baselines and tool configuration remain tracked.

### FR-5: Structured manifest

The gate writes `.quality-reports/manifest.json` on every run, including partially provisioned runs. The manifest contains:

- a schema version;
- generation time in UTC;
- one entry for every fixed check;
- each check's `pass`, `fail`, or `skipped` status;
- its primary report path;
- its stderr log path; and
- its numeric exit code when executed, otherwise `null`.

The manifest contains only gate-controlled values so it is valid JSON without interpolating untrusted tool output.

### FR-6: Missing setup

If Composer is unavailable, all checks are `skipped`, the manifest is still produced, and the gate exits successfully to avoid wedging an initialized but not-yet-provisioned repository.

If an individual Composer script is absent, only that check is `skipped`; remaining configured checks still run. A skipped status is explicitly documented as missing verification that the reviewer must surface.

### FR-7: Exit semantics

- Exit `0` when every executed check passes, including when one or more checks are skipped.
- Exit `2` when at least one executed check fails.
- Evidence generation failure is itself a gate failure and must not be reported as a clean result.

Reviewer approval depends on the manifest, not only the process exit code; therefore skipped required checks cannot be interpreted as green.

### FR-8: Ratchet ownership

- PHPStan continues to use the committed `phpstan-baseline.neon`.
- Duplication uses a committed `.jscpd.json` threshold seeded from the repository's current measured duplication.
- Architecture uses a project-authored `deptrac.yaml` and, when needed for existing debt, committed `deptrac.baseline.yaml` imported by that configuration.
- Dependency audit ignore/policy changes are treated as suppression changes.
- The reviewer audits changes to all baseline, threshold, ruleset, ignore, and dependency-policy files before consuming findings.

The baseline template documents how to seed these ratchets but does not generate project-specific architecture rules or silently update baselines during a gate run.

### FR-9: Reviewer use and fix scope

The shared code-reviewer instructions require the reviewer to:

- read the fresh manifest and the reports for every failed check;
- record skipped checks or missing reports as missing verification;
- use deterministic findings as evidence, without relabeling them as semantic discoveries;
- inspect surrounding or untouched code when needed to establish the implementation's impact without treating that inspection as authorization to expand repair scope;
- block on test failures and unresolved in-scope or change-caused deterministic findings;
- return change-caused findings in touched files to the implementer;
- surface new ripple findings in untouched files without assigning extra fix scope absent approval; and
- leave unrelated pre-existing whole-repository findings to their committed ratchet rather than requesting opportunistic cleanup.

Security advisories affecting the locked dependency set are reviewed under the existing security severity/evidence policy. Abandoned-package notices may be reported without automatically being treated as exploitable vulnerabilities.

### FR-10: Initialization guidance

Laravel initialization continues to copy the template without overwriting existing target files. Its setup output and documentation must name both toolchain installation steps:

- Composer development tools, including Deptrac; and
- project-local `jscpd` installation with the detected/supported Node package manager guidance.

The initializer is not required to modify a target project's `composer.json`, `package.json`, Deptrac rules, or ratchet values automatically.

## Acceptance Criteria

1. Given all six Composer scripts are available and succeed, one gate run executes all six in order, writes a valid manifest with six `pass` entries and stable report paths, and exits `0`.
2. Given an early check fails, all later checks still execute, the failed check is recorded as `fail`, passing checks are recorded as `pass`, and the gate exits `2`.
3. Given one or more scripts are missing, those checks are `skipped`, configured checks still execute, the manifest is valid, and the gate does not claim skipped checks passed.
4. Given Composer is unavailable, the gate writes a six-entry all-skipped manifest and exits `0`.
5. Given stale files exist in `.quality-reports/`, a new run removes them before producing current evidence.
6. Tool stderr cannot corrupt a JSON primary report because it is stored in the check's separate stderr log.
7. The reviewer instructions consume `.quality-reports/manifest.json`, audit all relevant suppression/ratchet changes, and state the blocking and scope rules for tests, touched-file findings, untouched ripple findings, and unrelated baseline debt.
8. The PHP/Laravel documentation provides install commands, Composer script examples, artifact meanings, ignore rules, ratchet setup, reviewer flow, and the distinction between this local full-repository gate and hosted CI.
9. Laravel template provisioning tests still pass and verify the expanded template assets/setup guidance remain provisioned without reinstalling legacy hooks.
10. Automated gate tests cover success, continue-on-failure, partial setup, Composer absence, and stale-evidence cleanup.

## Out of Scope

- Creating GitHub Actions or another hosted CI workflow.
- Installing a git pre-commit or agent edit hook.
- Automatically editing target-project package manifests.
- Inventing or generating a universal Deptrac layer model for all Laravel projects.
- Automatically accepting, regenerating, or increasing any ratchet baseline.
- Scanning non-Composer ecosystems for dependency vulnerabilities.

## Verification

- Run the focused quality-gate orchestration tests with fake Composer commands and parse the generated manifest as JSON.
- Run `python -m unittest tests.test_init_project_agent` to protect Laravel provisioning behavior.
- Run the repository's broader Python test suite.
- Inspect the changed shell script with a POSIX shell syntax check where available.
- Review the final diff for accidental hosted-CI/hook provisioning and for consistency among the gate, template documentation, deterministic-pipeline context, initializer output, and code-reviewer instructions.
