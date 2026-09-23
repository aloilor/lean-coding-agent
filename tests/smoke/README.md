# Codex UI Smoke Checks

1. Add the repository marketplace with <code>codex plugin marketplace add .</code>.
2. In Codex's Plugins directory, install **Lean Coding Agent** from the marketplace.
3. Start a new Codex task and confirm the plugin exposes every skill under the repository's <code>skills/</code> directory that contains a <code>SKILL.md</code>.
4. Confirm installation does not create project-local skill copies or ask which skills to install.
5. Rebuild the plugin, run <code>codex plugin marketplace upgrade lean-coding-agent</code>, and confirm the installed bundle refreshes as one versioned package.
6. Remove the local marketplace when finished with <code>codex plugin marketplace remove lean-coding-agent</code>.
