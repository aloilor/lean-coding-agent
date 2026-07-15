# Lessons

- [Write All Project Output In English](write-all-project-output-in-english.md) - Write all project output, including stored content and assistant responses, in English unless the project rule is explicitly changed.
- [Make README Indexes Clickable](make-readme-indexes-clickable.md) - When a README serves as an index, link the referenced files so the document is directly navigable.
- [Sync Updated Shared Skills To Local And Sibling Repos](sync-updated-shared-skills-to-local-and-sibling-repos.md) - Whenever a skill in `skills/` is updated, sync that skill into every maintained matching `.agents/skills/<skill>` copy in this repo and sibling repos under `../`.
- [Honor Bootstrap Installation Scope](honor-bootstrap-installation-scope.md) - When asked to install tooling in initialized projects, make the bootstrap create the required project files instead of only documenting manual commands.
- [Prefer Engineering Standards Over Local Style](prefer-engineering-standards-over-local-style.md) - Follow the `engineering-standards` skill for style guidance instead of preserving inconsistent nearby code style.
- [Update Bootstrap Managed Ignore Rules](update-bootstrap-managed-ignore-rules.md) - When ignore rules must apply to initialized repos, update the bootstrap-managed list instead of only editing this repo's root `.gitignore`.
- [Test Initialization Structure Changes](test-initialization-structure-changes.md) - Every structural change to project initialization must include a regression test for the new structure and a rerun of the initialization checks.
- [Do Not Clean Up Removals In The Initializer](do-not-clean-up-removals-in-initializer.md) - When baseline content is removed, stop generating it without adding initializer deletion or migration logic.
