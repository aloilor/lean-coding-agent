---
name: maintain-changelog
description: Write, update, or reconcile a curated CHANGELOG.md by inspecting Git commits and diffs, regardless of commit message format. Use whenever the user asks to maintain a changelog, summarize changes into Unreleased, or record shipped changes in a versioned changelog. Follow Keep a Changelog and Semantic Versioning. This is a manually invoked workflow; it does not commit, tag, publish, or change package versions.
compatibility: Requires read access to local Git history and file editing tools. No GitHub integration or Conventional Commits required.
---

# Maintain Changelog

Maintain durable version history for people affected by the software. Curate meaningful changes from evidence; do not turn commit subjects or pull requests into a changelog dump.

## 1. Establish scope

- Read repository guidance, the existing changelog, version sources, and relevant compatibility and migration documentation. Preserve the changelog's language and existing human edits. Default to root `CHANGELOG.md` if no changelog exists; ask which file or component to maintain if multiple candidates are plausible.
- Use the current checkout's committed history through HEAD. Report the branch and HEAD inspected. Leave staged and uncommitted changes out of the changelog and mention their exclusion. Do not fetch, switch branches, or inspect unrelated branches by default.
- Treat changes as **unreleased unless the user explicitly says they have been released**. A tag, version bump, commit date, or planned deployment is not confirmation that changes shipped.
- When the user confirms release, apply that confirmation to the changes under review. Do not require a release endpoint or tag. Ask only if the user's statement leaves a material subset unclear; keep unrelated pending entries in `Unreleased`.
- Modify only the changelog. Do not install automation, commit, tag, publish, change manifests or lockfiles, or create an internal deployment record. Produce separate release notes only if explicitly requested.

## 2. Establish the inclusive date boundary

- Find the newest **released** section and use its release date inclusively, starting at midnight in the project's documented timezone, otherwise the current local timezone. An `Unreleased` section has no release date and does not move the boundary.
- Enumerate commits reachable from HEAD, including merged branch commits. Compare full committer timestamps against the cutoff; author dates can predate integration. Inspect all commits on the cutoff date as well as later commits. Avoid date traversal pruning that can miss commits behind an out-of-order timestamp; enumerate history and filter, or use a supported equivalent such as `--since-as-filter`.
- Release tags and the history of the changelog may help distinguish already documented changes, but do not replace or narrow the requested inclusive date review.
- If no changelog, released section, or usable release date exists, ask for a starting date or commit boundary and the initial/current version. Do not silently inspect all history or fabricate historical releases. A supplied commit boundary is excluded unless the user says otherwise.
- If required history is shallow or unavailable, or release dates conflict, explain what cannot be established and ask for the missing information. Never claim complete coverage without the evidence.

## 3. Inspect every candidate commit

Read each candidate commit's full message and diff, then inspect relevant code, tests, documentation, and related commits where needed to establish the effect. Commit messages may use any format; never depend on Conventional Commit prefixes, labels, or PR metadata.

Maintain a temporary review ledger while working: commit identifier, observed effect, and disposition (new entry, covered already, combined, reverted, or omitted with reason). Include merge commits in the review and check for merge-resolution changes without counting merged changes twice. For large histories, work in explicit batches until every candidate is accounted for; do not sample or silently truncate.

Judge changes by their resulting behavior:

- Include features, fixes, deprecations, removals, security changes, and other meaningful effects on users, integrators, or operators.
- Omit internal refactors, tests, tooling, and dependency churn unless they materially affect those readers. Inspect them before deciding to omit them.
- Combine related implementation commits into one coherent change. Split a commit into multiple entries when it contains distinct reader-facing changes.
- Reconcile against **both released history and existing Unreleased entries**. Re-inspect the full date range on every run, without adding a tracking file. Preserve useful existing prose, improve it only as evidence warrants, and do not duplicate changes already covered.
- Check later fixes and reverts. Remove pending entries for changes fully reverted before release; describe a partial revert's final effect. Preserve historical release entries even when a later release reverts their behavior.
- Investigate uncertain behavior and compatibility. Ask focused questions when evidence is insufficient; do not invent affected audiences, benefits, migration steps, links, or security claims.

The ledger supports coverage verification and the final explanation; do not append it to the public changelog or create a durable tracking file.

## 4. Curate the entries

Use [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/):

- Keep one `## [Unreleased]` section at the top, then newest releases first, with headings such as `## [1.4.0] - 2026-11-02`.
- Use the consistent category order `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Omit empty categories and use each category at most once per release. Keep `Unreleased` even when empty.
- Write concise, plain-language bullets describing what changed, who is affected when relevant, and any required action. Include verified help or migration links when useful. Avoid raw identifiers, file lists, and implementation jargon that do not help the reader.
- Put **Breaking:** at the start of incompatible-change bullets in the appropriate category, followed by the required upgrade action and a verified migration link if available. Do not add a second `Changed` heading or invent a migration guide. If required upgrade steps are unknown, ask before presenting the entry as complete.
- Use ISO dates (`YYYY-MM-DD`) and state that the changelog follows Keep a Changelog and Semantic Versioning. Preserve historical release content; ask before reorganizing or correcting published history beyond incidental formatting needed for this update.
- Preserve working version and comparison links. Add or update them only when repository URLs and actual refs are verified; never invent tags for a proposed version. Plain version headings are acceptable when comparison targets are unavailable.

Example body (link definitions require verified targets):

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dealers can now download course completion reports.

## [1.2.1] - 2026-11-02

### Fixed
- Completed courses now remain visible in the training dashboard.
```

## 5. Apply release status and Semantic Versioning

Use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) and the project's declared compatibility contract. For a web application, inspect documented guarantees for APIs, integrations, configuration, imports/exports, and supported workflows. Ask when no adequate contract exists and that prevents a reliable version decision. Ordinary visual changes alone do not imply a major bump.

For stable versions (`1.0.0` and above), choose the highest required bump across the release:

| Change | Required next version |
| --- | --- |
| Incompatible change to the supported public contract | Major; reset minor and patch to zero |
| Compatible public functionality or public API deprecation | Minor; reset patch to zero |
| Only compatible bug fixes | Patch |

For `0.x`, initial `1.0.0`, prereleases, or changes that do not fit these rules, use an established project policy or ask; do not invent a universal policy. Validate supplied versions as SemVer, check ordering, and flag conflicts with the required bump rather than silently accepting or replacing them. Do not infer version impact from commit wording alone.

- **Unreleased:** reconcile entries in `Unreleased` without assigning it a release date or version. Report a proposed next version and rationale when the evidence supports one; label it as a proposal.
- **Released:** use the user's release confirmation and any supplied version/date. If either is missing, propose the version with its rationale and ask for confirmation and the actual release date as needed before creating the released section. Do not use today's date as an invented historical release date.
- Move only confirmed released changes into the new versioned section, including relevant existing Unreleased entries. Keep `Unreleased` above it and retain pending changes there. If the same release is already recorded, reconcile without creating a duplicate section or silently rewriting published history.
- If there are no new notable changes, report that result; do not manufacture entries or a release version. Ask if the user needs an explicitly confirmed release with no notable changes recorded.

## 6. Verify and report

Before finishing, review the diff and confirm:

1. Every candidate commit has a disposition supported by the review ledger; report the count and inclusive boundary.
2. Entries describe verified final behavior, combine related commits, omit noise, and do not duplicate released or pending changes. Running again on unchanged history would produce no further edits.
3. Release status follows the user's input, dates reflect actual supplied release information, and versions follow the applicable compatibility policy.
4. `Unreleased`, release order, category order, unique headings, dates, breaking-change actions, and links are correct. No historical entries or unrelated user edits were lost.
5. Only the intended changelog changed. Do not run application tests solely for a prose update; verify against source evidence and the Markdown diff.

Report the file edited, review boundary and commit count, notable inclusions/exclusions, release status, proposed or recorded version with rationale, and unresolved questions. Distinguish inspected evidence from assumptions and incomplete coverage. Keep operational details and the commit ledger out of the public changelog.
