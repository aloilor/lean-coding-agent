# Lean Coding Agent

A minimal, opt-in baseline for Codex with clear-code standards, TDD, and repeatable workflows.

Lean Coding Agent provides a selectable collection of project-local skills, including a self-contained <code>setup-project</code> installer for applying the broader project baseline.

## Install

### Install Lean Coding Agent skills (recommended)

From the project where you want the skills, run:

    npx skills@latest add aloir/coding-agent-baseline

The Skills CLI prompts you to choose skills and the coding agents to install them for. Choose <code>setup-project</code> and Codex to install the baseline setup assistant, then invoke <code>$setup-project</code> in the target project. You can also select other skills to install directly. To update installed skills later, run <code>npx skills update</code>, then invoke <code>$setup-project</code> again in each initialized project to sync its baseline files.

## Set up a project

In the target project, invoke <code>$setup-project</code>. The skill asks for the project path, presents skills with recommendation labels and reasons, and asks which skills to install. Recommendations are not preselected.

- <code>engineering-standards</code> is recommended for most coding projects.
- <code>codebase-onboarding</code> is recommended for new or unfamiliar projects.
- Upstream <code>tdd</code> is recommended when the project has a test suite and is included only when community skills are selected.
- <code>grill-with-docs</code> and <code>workflow-*</code> are recommended for teams choosing structured workflows.
- REST, Git, SQL, browser, and other specialized skills are contextual options.

The setup flow separately asks whether to install upstream community skills and browser tooling. Both are optional and default to no. Automated tests mock all package-manager and network commands.

You can choose model IDs independently for the implementer, reviewer, and diagnostician agents. Each defaults to <code>gpt-6-luna</code>; the agents keep their existing <code>xhigh</code> reasoning effort.

## Safe synchronization

The setup skill previews managed-file changes and Git status before applying them. It shows diffs for existing files that would be replaced and requires your explicit approval. Declining the preview leaves the project untouched.

Sync reuses saved skill, add-on, and model choices from <code>agent-context/skills-installed.json</code>. It preserves project context, local-private files, unrelated and untracked content, and skills installed outside this baseline. A previously selected baseline skill is not removed just because a later sync omits it; removal requires an explicit choice.

New manifests identify <code>lean-coding-agent</code> and its selection schema without recording a machine-specific repository path. The first approved sync can migrate a legacy initializer manifest when its structure and baseline file signatures match, even if its old source directory no longer exists. Ambiguous or foreign manifests are rejected.

## Local development

The repository remains the canonical source. <code>scripts/build_codex_plugin.py</code> generates the Codex plugin under <code>plugins/lean-coding-agent/</code> and the self-contained Skills CLI installer under <code>skills/setup-project/</code> from the baseline files, agent TOMLs, skills, overrides, setup engine, and upstream install metadata.

    python scripts/build_codex_plugin.py
    python scripts/build_codex_plugin.py --check
    python -m unittest discover -s tests

The automated suite is organized into <code>tests/unit/</code>, <code>tests/integration/</code>, <code>tests/contract/</code>, and <code>tests/smoke/</code>. <code>--check</code> fails if generated package files are missing, changed, or unexpected.

For the Codex UI smoke scenarios, see [tests/smoke/README.md](tests/smoke/README.md). These manual checks use temporary projects and cover clean setup, selected options, add-on opt-ins, conflict approval and decline, and sync persistence.

To smoke-test the optional Codex plugin package from this working tree, add its local marketplace:

    codex plugin marketplace add "C:\Users\Craas\Desktop\personal-projects\coding-agent-baseline"
    codex plugin marketplace list

Restart Codex if the marketplace is not visible. Codex runs the installed package from its cache. Rebuild, refresh or reinstall the local plugin, and restart the app after changing package files.

## Contributing

Edit canonical files in <code>skills/</code>, <code>agent-context/</code>, <code>.agents/lessons/</code>, <code>.codex/agents/</code>, or the setup sources under <code>plugin-src/</code> and <code>scripts/</code>. The build script generates <code>skills/setup-project/</code> and <code>plugins/lean-coding-agent/</code>; do not hand-edit either output. Rebuild and verify with <code>--check</code>.

Submit changes as a pull request against <code>aloilor/coding-agent-baseline</code>. Public release, publishing, and submission to the universal Plugins Directory are separate from local development.

## License

This project is available under the [MIT License](LICENSE).
