---
"lean-coding-agent": major
---

Add the `plan`, `diagnose`, `implement`, and `code-review` skills. Workflow subagents now load them, and you can run any of them directly without a workflow. Each skill bundles its artifact template, so setup no longer copies templates into `.agents/templates/`.

Upgrading: rerun setup. It installs the four new skills, which the refreshed subagents need. You can delete the old `.agents/templates/` folder, because nothing reads it anymore.
