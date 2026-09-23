# Codex UI Smoke Tests

These manual checks complement the automated, network-mocked tests. Use temporary project directories.

1. In a temporary project, run <code>npx skills@latest add aloir/coding-agent-baseline</code>. Select <code>setup-project</code> and Codex, then start a Codex task in that project.
2. Invoke <code>$setup-project</code>, select no skills or add-ons, and confirm that no optional skills are copied and no package or network command runs.
3. In a second temporary project, select multiple recommended skills, choose a different model for each agent, and confirm only the selected first-party skills are copied and each custom-agent TOML uses its model.
4. In an isolated project, opt into upstream community skills and browser tooling. Confirm the expected commands run and the selected files appear.
5. Modify <code>AGENTS.md</code> in an initialized temporary project. Preview sync, decline, and confirm the file is unchanged. Preview again, approve the exact changes, and confirm the update is applied while unrelated and untracked files remain.
6. Sync again without changing choices. Confirm the saved skills, add-ons, and agent models remain in effect.
7. If you also tested the optional plugin marketplace, remove it when finished:

       codex plugin marketplace remove lean-coding-agent

Codex installs a cache copy of a local plugin. After rebuilding the package, refresh or reinstall the plugin and restart Codex before repeating a smoke check.
