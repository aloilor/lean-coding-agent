# Changelog Examples

Read this when writing or rewording entries. Each example shows a pattern and why it works for someone deciding whether and how to upgrade. The project, versions, and dates are illustrative; real entries come only from verified evidence.

## Contents

1. [A complete changelog](#1-a-complete-changelog)
2. [From commits to entries](#2-from-commits-to-entries)
3. [Rewriting weak bullets](#3-rewriting-weak-bullets)
4. [Breaking changes](#4-breaking-changes)
5. [Deprecation, then removal](#5-deprecation-then-removal)
6. [Security fixes](#6-security-fixes)
7. [Preparing a release](#7-preparing-a-release)

## 1. A complete changelog

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dealers can now download course completion reports as CSV from the training dashboard.

## [2.0.0] - 2026-11-02

### Removed
- **Breaking:** The `status_old` API field, deprecated in 1.4.0. API clients must read `status`; see the [status migration guide](docs/migrate-status.md).

### Fixed
- Completed courses now remain visible in the training dashboard.

## [1.4.0] - 2026-10-15

### Added
- Admins can enrol many dealers in a course at once.
- API responses include course progress in a new `status` field.

### Deprecated
- The `status_old` API field. Use `status` instead; `status_old` will be removed in 2.0.0.

## [1.3.1] - 2026-10-01

### Security
- Course certificates can no longer be downloaded by dealers from other dealerships.
```

Why it works:

- `Unreleased` stays at the top, so pending work has an obvious home.
- Releases run newest first with ISO dates, and each category appears once per release, in the standard order.
- Every bullet names what changed for the reader, not how it was built.
- 1.4.0 added the replacement and deprecated the old field, so the removal in 2.0.0 was announced a release ahead, and the breaking entry says exactly what to do.

## 2. From commits to entries

Commits in the review range:

```text
a1b2c3d  wip reports
d4e5f6a  reports: add csv writer
b7c8d9e  fix tests
e0f1a2b  That annoying dashboard thing
c3d4e5f  Trying reminders
f6a7b8c  Back that out
9d0e1f2  bump eslint
```

A commit dump, which does not help readers:

```markdown
### Changed
- wip reports
- reports: add csv writer
- fix tests
- That annoying dashboard thing
- Trying reminders
- Back that out
- bump eslint
```

Curated from the diffs:

```markdown
### Added
- Dealers can now download course completion reports as CSV.

### Fixed
- Completed courses now remain visible in the training dashboard.
```

What happened to each commit:

- `a1b2c3d` and `d4e5f6a` are one feature, so they become one entry.
- `e0f1a2b` has a vague subject; the diff shows it fixes dashboard visibility.
- `c3d4e5f` and `f6a7b8c` cancel out before release, so nothing is recorded.
- `b7c8d9e` and `9d0e1f2` change tests and tooling only, so readers are unaffected.

## 3. Rewriting weak bullets

| Weak | Clear | What changed |
| --- | --- | --- |
| Fixed bug in dashboard. | Completed courses now remain visible in the training dashboard. | Says which behavior is now correct. |
| Refactored `ReportService` to use streams. | Large course reports now download without timing out. | States the effect, or omit the entry if readers see none. |
| Updated API. | **Breaking:** `GET /courses` now returns `status` instead of `status_old`. Read `status` in API clients. | Names the change and the required action. |
| Added `export_csv` flag (#482, a1b2c3d). | Dealers can now export their course list as CSV. | Drops identifiers that do not help the reader. |
| Various improvements and fixes. | *(Split into specific entries, or omit.)* | A catch-all tells readers nothing. |

## 4. Breaking changes

```markdown
### Changed
- **Breaking:** Course progress moved from `status_old` to `status` in API responses. Update API clients to read `status`; see the [status migration guide](docs/migrate-status.md).

### Removed
- **Breaking:** The legacy `/v1/reports` endpoint. Use `/v2/reports`, which returns the same data with pagination.
```

- A replaced interface goes under `Changed`; a removal with no replacement in the same release goes under `Removed`.
- The bullet starts with **Breaking:**, states the action, and links a migration guide only if one exists.
- If the upgrade steps are unknown, ask instead of writing a vague "update your integration".

## 5. Deprecation, then removal

```markdown
## [2.0.0] - 2026-11-02

### Removed
- **Breaking:** The `status_old` API field, deprecated in 1.4.0. Read `status` instead.

## [1.4.0] - 2026-10-15

### Deprecated
- The `status_old` API field. Use `status` instead; `status_old` will be removed in 2.0.0.
```

The deprecation gives readers a release of warning and a replacement. The removal refers back to it, so someone skipping versions can follow the trail.

## 6. Security fixes

```markdown
### Security
- Course certificates can no longer be downloaded by dealers from other dealerships. Upgrade as soon as possible if dealers share an installation.
```

- Describe the impact and who should act, at the level of detail the maintainers have made public.
- Leave out exploit details, and never invent severity, CVE identifiers, or affected versions.

## 7. Preparing a release

Before, with pending entries:

```markdown
## [Unreleased]

### Added
- Dealers can now download course completion reports as CSV.

### Fixed
- Completed courses now remain visible in the training dashboard.

## [1.4.0] - 2026-10-15
```

After the user asks to prepare 1.5.0 for release on 2026-11-03:

```markdown
## [Unreleased]

## [1.5.0] - 2026-11-03

### Added
- Dealers can now download course completion reports as CSV.

### Fixed
- Completed courses now remain visible in the training dashboard.

## [1.4.0] - 2026-10-15
```

`Unreleased` stays, empty, above the new section. The version is a minor bump because the changes add compatible functionality and fix a bug, with nothing breaking.
