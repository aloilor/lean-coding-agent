# Laravel Quality-Gate Activation (Deferred TODO)

This reference is retained for future work. Current onboarding and development workflows
must not activate, run, configure, or consume the quality gate unless a user explicitly
asks to resume this TODO.

Preserved future purpose: turn the provisioned Laravel gate into project-specific,
executable verification without inventing architecture or silently accepting debt.

Use this reference only when both conditions hold:

- the repository is a Laravel project, confirmed by `artisan` and `laravel/framework` in `composer.json`; and
- `scripts/quality-gate` exists.

For other repositories, record that this activation is not applicable and do not add PHP/Laravel tooling.

## Safety And Approval Boundary

Discovery and dry-run measurement with already-installed tools are read-only. Before installing dependencies or changing `composer.json`, `package.json`, PHPStan settings, `.jscpd.json`, `deptrac.yaml`, baselines, or audit policy:

1. Inventory installed tools, detected package managers, existing equivalent scripts, files to create or update, and proposed source/test paths.
2. When the tools already exist, include dry-run measurements, proposed thresholds, architecture layers and rules, and expected baseline files in one consolidated activation proposal.
3. When tools are missing, first propose dependency installation and script wiring, explain that package manifests and lockfiles will change, and obtain explicit setup approval. After installation, collect dry-run measurements and present a second policy proposal for thresholds, architecture rules, baselines, or audit policy.
4. Obtain explicit approval for every mutation stage; approval for tool setup is not approval to accept measured debt or architecture policy.

Architecture rules, ratchet thresholds, baselines, and security ignores are policy. Never invent, loosen, regenerate, or accept them silently. If the user approves dependency/script setup but not a proposed policy, configure the independent checks and record the policy-dependent check as pending instead of guessing.

Preserve project-owned commands and configuration. When an existing command already satisfies a gate contract, wire the stable `quality:*` name to that command rather than replacing it.

## Phase A: Inventory And Proposal

Read:

- `composer.json`, `composer.lock`, `package.json`, and the detected lockfile;
- `phpstan.neon*`, `phpstan-baseline.neon`, `pint.json`, `phpunit.xml*`, and Pest configuration when present;
- `.jscpd.json`, `deptrac.yaml`, `deptrac.baseline.yaml`, audit policy or ignore configuration;
- `agent-context/architecture.md`, `agent-context/testing.md`, and their source evidence; and
- `docs/quality-pipeline.md` provisioned with the gate.

Inventory each stable contract:

| Contract | Purpose | Default candidate when no equivalent exists |
| --- | --- | --- |
| `quality:style` | non-mutating style check | `pint --test` |
| `quality:static` | PHPStan/Larastan and cognitive complexity | `phpstan analyse --error-format=json --no-progress` |
| `quality:test` | full project test suite | detected authoritative test command, run through Sail (`sail artisan test`) |
| `quality:duplication` | whole-project clone detection | detected package-manager invocation of project-local `jscpd` |
| `quality:architecture` | project-approved dependency boundaries | `deptrac analyse --formatter=json` after rules are approved |
| `quality:audit` | locked Composer dependency advisories | `composer audit --locked --format=json` |

Do not assume `php artisan test` is authoritative merely because the repository is Laravel. Prefer the existing full-suite command when project scripts or testing documentation establish one. Whichever command is authoritative, run it through Laravel Sail (for example `sail artisan test`, or `sail` prefixed onto the project's Pest/PHPUnit invocation) so the suite executes inside the application container rather than on the host.

## Phase B: Configure After The Applicable Approval

### Dependencies And Script Wiring

- Install missing PHP development dependencies using the Composer command printed by the initializer.
- Install `jscpd` as a project-local development dependency with the detected Node package manager.
- Add only missing `quality:*` Composer scripts. Preserve unrelated scripts, their order where practical, and existing project-specific verification commands.
- Do not redirect structured output in Composer scripts; `scripts/quality-gate` owns stdout and stderr capture.

### Pint

Pint requires no configuration by default. Preserve an existing `pint.json`. Create one only when repository evidence establishes a non-default preset, rules, or exclusions; do not invent style policy during onboarding.

### PHPStan, Larastan, And Complexity

- Confirm `phpstan.neon.dist` analyses the actual application source roots and excludes generated or vendor code through project configuration.
- Preserve the configured analysis level and cognitive-complexity thresholds unless the activation proposal explicitly changes them.
- Run PHPStan before generating a baseline and summarize the finding count and affected paths.
- For an existing repository, generate or update `phpstan-baseline.neon` only after the user approves grandfathering the reported existing findings. A new clean repository keeps an empty baseline.

### Duplication

- Build `.jscpd.json` from detected PHP source roots and evidence-backed exclusions such as generated code, dependencies, caches, or fixtures. Do not exclude ordinary application or test code merely to lower the metric.
- Measure duplication once with no threshold and record the reported percentage.
- Propose that measured value as the initial repository ratchet. Write the threshold only after approval; never round it upward or increase an existing threshold automatically.
- Keep a reviewer-readable reporter configured so clone locations remain available in `.quality-reports/duplication.txt`.

### Architecture

- Derive proposed Deptrac paths, layers, collectors, and allowed dependencies from confirmed boundaries in `agent-context/architecture.md` and code evidence.
- Present the proposed layer map and ruleset before writing `deptrac.yaml`. Architecture inference is a proposal, not authority.
- After approval, run Deptrac without a baseline and summarize every existing violation.
- Generate and import `deptrac.baseline.yaml` only after explicit approval to grandfather those violations. Keep the rules in `deptrac.yaml` and accepted debt in the separate imported baseline.

### Dependency Audit

- Use the locked Composer dependency graph as the source of truth.
- Run the audit before adding any ignore policy.
- Never add advisory ignores or abandoned-package policy during onboarding without explicit approval and a recorded reason. Findings remain visible when policy is undecided.

## Phase C: Operational Verification

Run `sh scripts/quality-gate` after configuration, then parse `.quality-reports/manifest.json` rather than relying only on the process exit code.

For each of the six checks, record:

- `operational-pass`, `operational-fail`, `skipped`, or `pending-approval`;
- the command and configuration evidence;
- the report path;
- any accepted baseline or threshold; and
- the exact reason for a skip, failure, or pending decision.

A skipped check is not operational. A failed check is evidence, not permission to fix unrelated product code during onboarding. Apply the normal scope rule: inspect broadly, but do not turn pre-existing findings into cleanup work.

Update:

- `agent-context/workflows.md` with the gate command, configuration files, operational-status table, reviewer ownership, and approval-dependent policies;
- `agent-context/testing.md` with the authoritative test command and which gate checks cover each verification layer; and
- `agent-context/architecture.md` only with architecture boundaries confirmed during onboarding, never with unapproved Deptrac proposals.

## Completion Report

In the onboarding closeout, distinguish:

- configured and passing checks;
- configured checks currently failing on known evidence;
- skipped checks caused by missing setup;
- policy decisions awaiting approval; and
- files, manifests, lockfiles, thresholds, baselines, or rules changed with approval.

Do not describe the gate as active or green unless all required checks are configured, the manifest contains no skips, and executed checks pass.
