---
"lean-coding-agent": minor
---

Let the Skills CLI own baseline skill installation, updates, and removal. Setup preserves the selected skills instead of copying sibling folders or pruning retired skills, removes obsolete installation manifests on rerun, and no longer bundles release metadata. Existing projects should rerun `npx skills add aloilor/lean-coding-agent` to register the desired skills with the CLI.
