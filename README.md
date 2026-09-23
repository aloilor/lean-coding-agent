# Lean Coding Agent

Lean Coding Agent is a managed Codex plugin that bundles the complete skill set from this repository. Install the plugin once; Codex keeps the skills together as a versioned package, and releases update the bundle.

## Install

Add the marketplace in Codex:

    codex plugin marketplace add aloir/coding-agent-baseline

Then open Codex's Plugins directory, choose the Lean Coding Agent marketplace, and install **Lean Coding Agent**. This installs all bundled skills together. There is no per-skill setup or project-local copy step.

Ask Codex for help with a task or invoke a skill by name, such as `$engineering-standards`, `$codebase-onboarding`, or `$workflow-feature-development`.

## Updates

The plugin is the subscription unit. When a new release is available, refresh its marketplace source:

    codex plugin marketplace upgrade lean-coding-agent

Each release ships the complete skill bundle under a new plugin version. Do not edit the installed cache; make changes in this repository and ship them with the next release.

## Included skills

Every directory under [`skills/`](skills/) that contains a `SKILL.md` is included in the plugin, along with its references, scripts, and other skill resources. The Codex package contains the skills as a single installable bundle.

## Local development

The repository is the canonical source. `scripts/build_codex_plugin.py` generates `plugins/lean-coding-agent/` from `plugin-src/plugin.json` and the installable skills under `skills/`.

    python scripts/build_codex_plugin.py
    python scripts/build_codex_plugin.py --check
    python -m unittest discover -s tests

For the manual Codex UI smoke scenarios, see [tests/smoke/README.md](tests/smoke/README.md).

To test the plugin from this working tree, add its local marketplace and refresh it after rebuilding:

    codex plugin marketplace add .
    python scripts/build_codex_plugin.py
    codex plugin marketplace upgrade lean-coding-agent

Restart Codex if the updated package is not visible.

Edit canonical skill sources in `skills/` and plugin metadata in `plugin-src/plugin.json`. The build script generates `plugins/lean-coding-agent/`; do not hand-edit generated files.

Submit changes as a pull request against [aloilor/coding-agent-baseline](https://github.com/aloilor/coding-agent-baseline). Public plugin publication and release versioning are separate from local development.

## License

This project is available under the [MIT License](LICENSE).
