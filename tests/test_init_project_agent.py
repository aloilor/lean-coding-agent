import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "init_project_agent.py"
SPEC = importlib.util.spec_from_file_location("init_project_agent", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
INIT_PROJECT_AGENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INIT_PROJECT_AGENT)
REPO_ROOT = SCRIPT_PATH.parents[1]


def file_contents(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    }


class InitializationIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name) / "target"
        self.repo.mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_initializer(self) -> list[object]:
        output = io.StringIO()
        with (
            mock.patch.object(sys, "argv", [str(SCRIPT_PATH), str(self.repo)]),
            mock.patch.object(INIT_PROJECT_AGENT.subprocess, "run") as run,
            redirect_stdout(output),
        ):
            self.assertEqual(0, INIT_PROJECT_AGENT.main())

        self.assertIn(f"Initialized project repo: {self.repo}", output.getvalue())
        return run.call_args_list

    def expected_baseline(self, filename: str) -> str:
        source_text = (REPO_ROOT / filename).read_text(encoding="utf-8")
        separator = "" if source_text.endswith("\n") else "\n"
        return source_text + separator + INIT_PROJECT_AGENT.baseline_guard_block(filename)

    def seed_project_owned_and_legacy_files(self) -> None:
        (self.repo / ".gitignore").write_text("existing/\nAGENTS.local.md\n", encoding="utf-8")
        (self.repo / "AGENTS.local.md").write_text("private agents notes\n", encoding="utf-8")

        (self.repo / "agent-context").mkdir()
        (self.repo / "agent-context" / "README.md").write_text(
            "# Existing project context\n",
            encoding="utf-8",
        )
        (self.repo / "agent-context" / INIT_PROJECT_AGENT.MANIFEST_NAME).write_text(
            json.dumps({"skills": [{"installed_as": "removed-skill"}]}),
            encoding="utf-8",
        )

        for skills_dir in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS:
            removed_skill = self.repo / skills_dir / "removed-skill"
            removed_skill.mkdir(parents=True)
            (removed_skill / "stale.txt").write_text("stale", encoding="utf-8")
            unmanaged_skill = self.repo / skills_dir / "project-skill"
            unmanaged_skill.mkdir()
            (unmanaged_skill / "keep.txt").write_text("keep", encoding="utf-8")

        lessons_index = self.repo / ".agents" / "lessons" / "LESSONS.md"
        lessons_index.parent.mkdir(parents=True)
        lessons_index.write_text("# Project lessons\n", encoding="utf-8")

        overrides_dir = self.repo / ".agents" / "skill-overrides"
        overrides_dir.mkdir()
        (overrides_dir / "INDEX.md").write_text(
            "# Skill Overrides\n\n- [project-skill](project-skill.md) - keep me.\n",
            encoding="utf-8",
        )
        (overrides_dir / "project-skill.md").write_text("project override\n", encoding="utf-8")

        incidents_readme = self.repo / "docs" / "incidents" / "README.md"
        incidents_readme.parent.mkdir(parents=True)
        incidents_readme.write_text("# Project incidents\n", encoding="utf-8")

        legacy_dir = self.repo / INIT_PROJECT_AGENT.LEGACY_AGENT_CONTEXT_DIRNAME
        legacy_clone = legacy_dir / "awesome-codex-skills"
        legacy_clone.mkdir(parents=True)
        (legacy_clone / "old.txt").write_text("old", encoding="utf-8")
        (legacy_dir / INIT_PROJECT_AGENT.LEGACY_CONFIG_NAME).write_text("{}", encoding="utf-8")

    def assert_external_install_commands(self, calls: list[object]) -> None:
        expected_commands = [
            [
                INIT_PROJECT_AGENT.executable_name("npm"),
                "install",
                "--save-dev",
                INIT_PROJECT_AGENT.AGENT_BROWSER_PACKAGE,
            ],
            [
                INIT_PROJECT_AGENT.executable_name("npm"),
                "exec",
                "--",
                INIT_PROJECT_AGENT.AGENT_BROWSER_COMMAND,
                "install",
            ],
        ]
        expected_commands.extend(
            [
                INIT_PROJECT_AGENT.executable_name("npx"),
                *INIT_PROJECT_AGENT.upstream_skills_install_command(
                    group["source"], group["skills"]
                )[1:],
            ]
            for group in INIT_PROJECT_AGENT.UPSTREAM_SKILL_GROUPS
        )

        self.assertEqual(len(expected_commands), len(calls))
        for call, expected_command in zip(calls, expected_commands, strict=True):
            self.assertEqual(mock.call(expected_command, cwd=self.repo, check=True), call)

    def test_initializes_the_complete_managed_project_structure(self) -> None:
        self.seed_project_owned_and_legacy_files()

        calls = self.run_initializer()

        for filename in INIT_PROJECT_AGENT.BASELINE_FILENAMES:
            self.assertEqual(
                self.expected_baseline(filename),
                (self.repo / filename).read_text(encoding="utf-8"),
            )
        self.assertEqual(
            "private agents notes\n",
            (self.repo / "AGENTS.local.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            INIT_PROJECT_AGENT.local_file_content("CLAUDE.local.md"),
            (self.repo / "CLAUDE.local.md").read_text(encoding="utf-8"),
        )

        gitignore_lines = (self.repo / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertEqual("existing/", gitignore_lines[0])
        expected_ignore_lines = [
            "AGENTS.local.md",
            "CLAUDE.local.md",
            ".agents/code-reviews/",
            ".agents/refactor-briefs/",
            ".agents/implementation-plans/",
            ".agents/implementation-reports/",
            ".agents/tasks/",
            ".codex/tasks/",
            ".claude/tasks/",
        ]
        for expected_line in expected_ignore_lines:
            self.assertEqual(1, gitignore_lines.count(expected_line), expected_line)

        self.assertEqual(
            "# Existing project context\n",
            (self.repo / "agent-context" / "README.md").read_text(encoding="utf-8"),
        )
        for source_path in (REPO_ROOT / "agent-context").rglob("*"):
            if not source_path.is_file() or source_path.name == INIT_PROJECT_AGENT.MANIFEST_NAME:
                continue
            target_path = self.repo / "agent-context" / source_path.relative_to(
                REPO_ROOT / "agent-context"
            )
            if source_path.name != "README.md":
                self.assertEqual(source_path.read_bytes(), target_path.read_bytes())

        installs = INIT_PROJECT_AGENT.discover_shared_skills(REPO_ROOT / "skills")
        manifest = json.loads(
            (self.repo / "agent-context" / INIT_PROJECT_AGENT.MANIFEST_NAME).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(str(REPO_ROOT / "skills"), manifest["source_root"])
        self.assertEqual(
            [str(path) for path in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS],
            manifest["managed_skill_dirs"],
        )
        self.assertEqual(installs, manifest["skills"])

        self.assertEqual(
            "# Project lessons\n",
            (self.repo / ".agents" / "lessons" / "LESSONS.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            "# Project incidents\n",
            (self.repo / "docs" / "incidents" / "README.md").read_text(encoding="utf-8"),
        )

        source_overrides = REPO_ROOT / "skills" / "skill-overrides"
        target_overrides = self.repo / ".agents" / "skill-overrides"
        for source_path in source_overrides.glob("*.md"):
            if source_path.name != "INDEX.md":
                self.assertEqual(
                    source_path.read_bytes(),
                    (target_overrides / source_path.name).read_bytes(),
                )
        target_override_index = (target_overrides / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("[project-skill](project-skill.md)", target_override_index)
        for override_name in [path.stem for path in source_overrides.glob("*.md")]:
            if override_name != "INDEX":
                self.assertIn(f"[{override_name}]({override_name}.md)", target_override_index)
        self.assertEqual(
            "project override\n",
            (target_overrides / "project-skill.md").read_text(encoding="utf-8"),
        )

        for source_agent in (REPO_ROOT / "agents").glob("*.md"):
            self.assertEqual(
                source_agent.read_bytes(),
                (self.repo / ".claude" / "agents" / source_agent.name).read_bytes(),
            )
            codex_agent_path = self.repo / ".codex" / "agents" / source_agent.with_suffix(
                ".toml"
            ).name
            self.assertEqual(
                INIT_PROJECT_AGENT.codex_agent_content(source_agent),
                codex_agent_path.read_text(encoding="utf-8"),
            )
            codex_agent = tomllib.loads(codex_agent_path.read_text(encoding="utf-8"))
            self.assertIn("developer_instructions", codex_agent)

        for install in installs:
            source_skill = REPO_ROOT / "skills" / install["source"]
            for skills_dir in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS:
                target_skill = self.repo / skills_dir / install["installed_as"]
                self.assertEqual(file_contents(source_skill), file_contents(target_skill))

        for skills_dir in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS:
            self.assertFalse((self.repo / skills_dir / "removed-skill").exists())
            self.assertEqual(
                "keep",
                (self.repo / skills_dir / "project-skill" / "keep.txt").read_text(
                    encoding="utf-8"
                ),
            )
        self.assertFalse(
            (self.repo / INIT_PROJECT_AGENT.LEGACY_AGENT_CONTEXT_DIRNAME).exists()
        )
        self.assertFalse((self.repo / INIT_PROJECT_AGENT.QUALITY_GATE_SCRIPT_SUBPATH).exists())
        self.assert_external_install_commands(calls)

    def test_rerun_refreshes_managed_files_and_preserves_project_owned_files(self) -> None:
        self.run_initializer()
        source_agent = next((REPO_ROOT / "agents").glob("*.md"))
        install = INIT_PROJECT_AGENT.discover_shared_skills(REPO_ROOT / "skills")[0]
        source_skill = REPO_ROOT / "skills" / install["source"]
        source_skill_file = next(path for path in source_skill.rglob("*") if path.is_file())

        managed_files = [
            self.repo / "AGENTS.md",
            self.repo / ".claude" / "agents" / source_agent.name,
            self.repo / ".codex" / "agents" / source_agent.with_suffix(".toml").name,
        ]
        for skills_dir in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS:
            managed_files.append(
                self.repo
                / skills_dir
                / install["installed_as"]
                / source_skill_file.relative_to(source_skill)
            )
        for managed_file in managed_files:
            managed_file.write_text("drifted\n", encoding="utf-8")

        preserved_contents = {
            self.repo / "AGENTS.local.md": "private local change\n",
            self.repo / "agent-context" / "testing.md": "project testing context\n",
            self.repo / ".agents" / "lessons" / "LESSONS.md": "# Project lessons\n",
            self.repo / "docs" / "incidents" / "README.md": "# Project incidents\n",
        }
        for path, content in preserved_contents.items():
            path.write_text(content, encoding="utf-8")

        calls = self.run_initializer()

        self.assertEqual(
            self.expected_baseline("AGENTS.md"),
            (self.repo / "AGENTS.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            source_agent.read_bytes(),
            (self.repo / ".claude" / "agents" / source_agent.name).read_bytes(),
        )
        self.assertEqual(
            INIT_PROJECT_AGENT.codex_agent_content(source_agent),
            (self.repo / ".codex" / "agents" / source_agent.with_suffix(".toml").name).read_text(
                encoding="utf-8"
            ),
        )
        for skills_dir in INIT_PROJECT_AGENT.MANAGED_SKILLS_DIRS:
            target_skill = self.repo / skills_dir / install["installed_as"]
            self.assertEqual(file_contents(source_skill), file_contents(target_skill))
        for path, content in preserved_contents.items():
            self.assertEqual(content, path.read_text(encoding="utf-8"))

        gitignore_lines = (self.repo / ".gitignore").read_text(encoding="utf-8").splitlines()
        for managed_line in [
            *INIT_PROJECT_AGENT.LOCAL_FILENAMES,
            *INIT_PROJECT_AGENT.SHARED_AGENT_IGNORE_LINES,
        ]:
            self.assertEqual(1, gitignore_lines.count(managed_line), managed_line)
        self.assert_external_install_commands(calls)


class PackageManagerDetectionTest(unittest.TestCase):
    def test_prefers_package_manager_declaration_then_known_lockfiles(self) -> None:
        cases = [
            ({"packageManager": "pnpm@10.0.0"}, [], "pnpm"),
            ({"packageManager": "unknown@1.0.0"}, ["yarn.lock"], "yarn"),
            ({}, ["bun.lockb"], "bun"),
            ({}, ["package-lock.json"], "npm"),
            ({}, [], "npm"),
        ]

        for package_json, lockfiles, expected in cases:
            with self.subTest(package_json=package_json, lockfiles=lockfiles):
                with tempfile.TemporaryDirectory() as temp_dir:
                    repo = Path(temp_dir)
                    for lockfile in lockfiles:
                        (repo / lockfile).touch()
                    self.assertEqual(
                        expected,
                        INIT_PROJECT_AGENT.detect_package_manager(repo, package_json),
                    )

    def test_agent_browser_uses_the_selected_package_manager_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            (repo / "package.json").write_text(
                json.dumps({"packageManager": "pnpm@10.0.0"}),
                encoding="utf-8",
            )

            with mock.patch.object(INIT_PROJECT_AGENT.subprocess, "run") as run:
                result = INIT_PROJECT_AGENT.install_agent_browser(repo)

            self.assertEqual("package installed and browser installed with pnpm", result)
            self.assertEqual(
                [
                    mock.call(
                        [
                            INIT_PROJECT_AGENT.executable_name("pnpm"),
                            "add",
                            "--save-dev",
                            INIT_PROJECT_AGENT.AGENT_BROWSER_PACKAGE,
                        ],
                        cwd=repo,
                        check=True,
                    ),
                    mock.call(
                        [
                            INIT_PROJECT_AGENT.executable_name("pnpm"),
                            "exec",
                            INIT_PROJECT_AGENT.AGENT_BROWSER_COMMAND,
                            "install",
                        ],
                        cwd=repo,
                        check=True,
                    ),
                ],
                run.call_args_list,
            )

    def test_install_failure_reports_the_selected_package_manager(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            with mock.patch.object(
                INIT_PROJECT_AGENT.subprocess,
                "run",
                side_effect=subprocess.CalledProcessError(1, "npm"),
            ):
                with self.assertRaisesRegex(
                    SystemExit,
                    "Could not install agent-browser@latest with npm",
                ):
                    INIT_PROJECT_AGENT.install_agent_browser(repo)


class LaravelDetectionTest(unittest.TestCase):
    def test_detects_artisan_or_laravel_framework_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.assertFalse(INIT_PROJECT_AGENT.detect_php_laravel(repo))

            (repo / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )
            self.assertTrue(INIT_PROJECT_AGENT.detect_php_laravel(repo))

            (repo / "composer.json").write_text("{invalid", encoding="utf-8")
            self.assertFalse(INIT_PROJECT_AGENT.detect_php_laravel(repo))

            (repo / "artisan").touch()
            self.assertTrue(INIT_PROJECT_AGENT.detect_php_laravel(repo))


class RemoveLegacyQualityGateHooksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_config(self, relative_path: str, config: object) -> Path:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(config), encoding="utf-8")
        return path

    def test_removes_config_containing_only_legacy_hook(self) -> None:
        path = self.write_config(
            ".claude/settings.json",
            {
                "hooks": {
                    "PostToolUse": [
                        {
                            "matcher": "Edit|Write",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": 'sh "$(git rev-parse --show-toplevel)/scripts/quality-gate"',
                                }
                            ],
                        }
                    ]
                }
            },
        )

        updated = INIT_PROJECT_AGENT.remove_legacy_quality_gate_hooks(self.repo)

        self.assertEqual([path], updated)
        self.assertFalse(path.exists())

    def test_preserves_unrelated_hooks_and_configuration(self) -> None:
        path = self.write_config(
            ".codex/hooks.json",
            {
                "theme": "dark",
                "hooks": {
                    "PostToolUse": [
                        {
                            "matcher": "Edit|Write|apply_patch",
                            "hooks": [
                                {"type": "command", "command": "scripts/quality-gate"},
                                {"type": "command", "command": "scripts/other-check"},
                            ],
                        }
                    ],
                    "SessionStart": [{"type": "command", "command": "scripts/setup"}],
                },
            },
        )

        updated = INIT_PROJECT_AGENT.remove_legacy_quality_gate_hooks(self.repo)

        self.assertEqual([path], updated)
        config = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("dark", config["theme"])
        self.assertEqual(
            [{"type": "command", "command": "scripts/other-check"}],
            config["hooks"]["PostToolUse"][0]["hooks"],
        )
        self.assertEqual(
            [{"type": "command", "command": "scripts/setup"}],
            config["hooks"]["SessionStart"],
        )

    def test_leaves_unrelated_config_unchanged(self) -> None:
        path = self.write_config(
            ".claude/settings.json",
            {
                "hooks": {
                    "PostToolUse": [
                        {
                            "matcher": "Edit",
                            "hooks": [{"type": "command", "command": "scripts/other-check"}],
                        }
                    ]
                }
            },
        )
        original = path.read_text(encoding="utf-8")

        updated = INIT_PROJECT_AGENT.remove_legacy_quality_gate_hooks(self.repo)

        self.assertEqual([], updated)
        self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_leaves_invalid_json_unchanged(self) -> None:
        path = self.repo / ".codex" / "hooks.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{invalid", encoding="utf-8")

        updated = INIT_PROJECT_AGENT.remove_legacy_quality_gate_hooks(self.repo)

        self.assertEqual([], updated)
        self.assertEqual("{invalid", path.read_text(encoding="utf-8"))

    def test_laravel_provisioning_removes_hook_without_reinstalling_it(self) -> None:
        (self.repo / "artisan").touch()
        hook_path = self.write_config(
            ".codex/hooks.json",
            {
                "hooks": {
                    "PostToolUse": [
                        {
                            "matcher": "apply_patch",
                            "hooks": [
                                {"type": "command", "command": "scripts/quality-gate"}
                            ],
                        }
                    ]
                }
            },
        )

        result = INIT_PROJECT_AGENT.provision_laravel_quality_gate(
            self.repo,
            SCRIPT_PATH.parents[1],
        )

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual([hook_path], result["removed_hook_paths"])
        self.assertFalse(hook_path.exists())
        self.assertTrue((self.repo / "scripts" / "quality-gate").exists())
        self.assertFalse((self.repo / ".claude" / "settings.json").exists())


if __name__ == "__main__":
    unittest.main()
