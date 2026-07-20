# Quality Pipeline (PHP / Laravel)

> **Deferred TODO:** The quality-gate assets are retained for future evaluation, but current
> agent workflows do not run, configure, or consume them. The material below documents the
> preserved experimental design and must not be treated as an active review requirement.

This template includes an experimental full-repository quality gate. It remains a local utility and does not install a git hook or a hosted CI workflow.

The gate attempts these Composer scripts in order and continues after failures:

1. `quality:style`
2. `quality:static`
3. `quality:test`
4. `quality:duplication`
5. `quality:architecture`
6. `quality:audit`

Projects may replace the command behind a name, but must preserve these names and the gate's evidence contract.

## Install the tools

Install the PHP development tools, including Deptrac:

```sh
composer require --dev \
    larastan/larastan:^3.0 \
    tomasvotruba/cognitive-complexity \
    phpstan/extension-installer \
    laravel/pint \
    deptrac/deptrac

composer config --no-plugins allow-plugins.phpstan/extension-installer true
```

Install `jscpd` as a project-local Node development dependency. Use the package manager declared by the project or identified by its lockfile:

```sh
npm install --save-dev jscpd
# pnpm add --save-dev jscpd
# yarn add --dev jscpd
# bun add --dev jscpd
```

The initializer prints the matching installation command. It does not modify `composer.json`, `package.json`, architecture rules, or ratchet values. The follow-up `codebase-onboarding` pass inventories the existing project configuration and uses staged approval when missing tools must be installed before current debt can be measured. It installs dependencies or writes scripts, thresholds, architecture rules, baselines, or audit policy only after the applicable explicit approval; setup approval never implies acceptance of measured debt or architecture policy.

## Define the Composer scripts

This npm-based example keeps tool output on stdout so the gate can capture it. For another Node package manager, replace only the `quality:duplication` command with that manager's project-local execution form.

```json
{
  "scripts": {
    "quality:style": "pint --test",
    "quality:static": "phpstan analyse --error-format=json --no-progress",
    "quality:test": "sail artisan test",
    "quality:duplication": "npx --no-install jscpd --config .jscpd.json .",
    "quality:architecture": "deptrac analyse --formatter=json",
    "quality:audit": "composer audit --locked --format=json",
    "quality:baseline": "phpstan analyse --generate-baseline"
  }
}
```

Composer makes its `vendor/bin` directory available to scripts, so `pint`, `phpstan`, `deptrac`, and `sail` resolve to the committed Composer development dependencies. `quality:test` runs the suite through Laravel Sail so it executes inside the application container against the same PHP version, extensions, and services (database, cache, queue) the app uses; never wire `quality:test` to a bare `php artisan test` or `phpunit`/`pest` invocation that runs on the host. The gate captures stdout as the primary report and stderr in a separate log. Do not redirect output inside these Composer scripts: redirecting structured output would leave the gate's JSON report empty.

## Configure the ratchets

PHPStan uses the committed `phpstan-baseline.neon` imported by `phpstan.neon.dist`. To seed an existing repository, run `composer quality:baseline`, inspect the generated suppressions, and commit the accepted baseline. The gate never updates it.

Duplication is a repository-level percentage ratchet. First run `jscpd` without a threshold, record the current duplicated-lines percentage, and then commit a `.jscpd.json` using that measured value:

```json
{
  "format": ["php"],
  "reporters": ["console"],
  "threshold": 3.25
}
```

The number above is illustrative; do not copy it as a universal threshold. A percentage ratchet prevents the total from increasing but does not grandfather individual clones, so reviewers must still correlate new clone findings with the diff. Lower the committed threshold when debt is removed; never increase it automatically.

Each project authors its own `deptrac.yaml` layers and rules. A generic Laravel layer model is intentionally not supplied because project dependency direction is an architectural decision. If an existing project has accepted violations, generate and inspect a baseline:

```sh
vendor/bin/deptrac analyse --formatter=baseline
```

Then import the committed result from the project-authored configuration:

```yaml
imports:
  - deptrac.baseline.yaml
```

Changes to `phpstan-baseline.neon`, `.jscpd.json`, `deptrac.yaml`, `deptrac.baseline.yaml`, Composer audit ignores, or dependency policy are suppression or ratchet changes and receive review before their findings are consumed.

## Evidence contract

Every run removes and recreates `.quality-reports/`. Add this directory to `.gitignore`; the initializer also manages that ignore rule. Keep ratchet and tool configuration files tracked.

| Check | Primary report | Stderr log |
| --- | --- | --- |
| style | `.quality-reports/style.txt` | `.quality-reports/style.stderr.log` |
| static | `.quality-reports/static-analysis.json` | `.quality-reports/static.stderr.log` |
| tests | `.quality-reports/tests.txt` | `.quality-reports/tests.stderr.log` |
| duplication | `.quality-reports/duplication.txt` | `.quality-reports/duplication.stderr.log` |
| architecture | `.quality-reports/architecture.json` | `.quality-reports/architecture.stderr.log` |
| audit | `.quality-reports/dependency-audit.json` | `.quality-reports/audit.stderr.log` |

`.quality-reports/manifest.json` contains schema version `1`, a UTC generation time, and one entry per check with its `pass`, `fail`, or `skipped` status, report paths, and numeric exit code (`null` when skipped). PHPStan, Deptrac, and Composer audit produce structured JSON primary reports; style, tests, and duplication use reviewer-readable text. Tool stderr never shares a structured report.

The gate exits `2` if any executed check fails and `0` otherwise. If Composer is unavailable, or an individual script is absent, affected checks are `skipped` and the manifest is still written. Exit `0` therefore does not by itself mean the worktree is verified: a future consumer must treat every skip or missing report as missing verification. An evidence-generation failure exits `2` and is never reported as clean.

## Planned reviewer flow and scope (TODO)

The flow in this section is a future integration proposal. It is not part of the current
reviewer or development workflows.

The full-repository gate deliberately sees more code than the implementer changed. That gives the reviewer enough context to detect regressions in callers, dependencies, and architecture relationships, but it does not broaden the approved repair scope. Only change-caused findings and findings explicitly targeted by the request, approved plan, or bug investigation are actionable.

The reviewer:

1. Inventories the diff, then runs `sh scripts/quality-gate` once for that review pass.
2. Audits changed ratchet, baseline, ruleset, ignore, and dependency-policy files.
3. Reads the fresh manifest and every failed report; skipped checks and missing reports are missing verification.
4. Uses deterministic results as evidence without presenting them as independently discovered semantic findings.
5. Blocks on test failures and unresolved in-scope or change-caused findings.
6. Returns change-caused findings in touched files to the implementer. New ripple findings in untouched files are surfaced without assigning them for repair unless scope is approved. Unrelated pre-existing whole-repository debt remains governed by its committed ratchet and must not become opportunistic cleanup.
7. Reviews locked-dependency advisories using the shared security severity and reachability policy. Abandoned-package notices may be reported without automatically being treated as exploitable vulnerabilities.

Duplication, architecture, and dependency audit remain CI-class analyses because they need whole-repository context. This gate runs them locally against the exact reviewed worktree so their findings inform semantic review. A hosted CI service should call the same scripts independently for every pushed commit, but hosted CI provisioning is outside this template.

No PostToolUse or git pre-commit hook is installed. When upgrading a repository created by an earlier baseline, the initializer removes only legacy PostToolUse commands that invoke `scripts/quality-gate` and preserves unrelated hook configuration.
