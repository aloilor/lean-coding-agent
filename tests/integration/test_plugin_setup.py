import contextlib
import io
import json
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from scripts import init_project_agent
from tests.support.project_fixtures import (
    file_contents,
    load_packaged_engine,
    temporary_plugin,
    temporary_project,
)


class PluginSetupIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = unittest.TestCase()
        cls.plugin_root = temporary_plugin(fixture)
        cls.addClassCleanup(fixture.doCleanups)
        cls.engine = load_packaged_engine(cls.plugin_root)

    def setUp(self) -> None:
        self.project = temporary_project(self)

    def invoke(self, command: str, *options: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(self.engine, "git_status", return_value="Working tree is clean."),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            status = self.engine.main([command, "--target", str(self.project), *options])
        return status, stdout.getvalue(), stderr.getvalue()

    def read_manifest(self) -> dict[str, object]:
        return json.loads(
            (self.project / "agent-context" / "skills-installed.json").read_text(
                encoding="utf-8"
            )
        )

    def test_installs_from_plugin_copy_with_no_default_skills_or_external_side_effects(self) -> None:
        self.assertFalse(self.plugin_root.is_relative_to(Path(__file__).parents[2]))
        with mock.patch.object(self.engine, "run_external_command") as run_external:
            status, output, _ = self.invoke("apply")

        self.assertEqual(0, status)
        self.assertIn("Project state: new", output)
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertFalse((self.project / ".agents" / "skills").exists())
        self.assertEqual([], self.read_manifest()["skills"])
        self.assertEqual(
            {"community_skills": False, "browser_tooling": False},
            self.read_manifest()["addons"],
        )
        self.assertEqual([], run_external.call_args_list)

    def test_default_project_files_match_initializer_outputs_except_portable_manifest(
        self,
    ) -> None:
        initializer_target = temporary_project(self)
        init_project_agent.copy_agent_context_baseline(
            initializer_target,
            init_project_agent.REPO_ROOT,
        )
        init_project_agent.ensure_agent_context_readme(initializer_target / "agent-context")
        init_project_agent.ensure_incidents_readme(
            initializer_target,
            init_project_agent.REPO_ROOT,
        )
        init_project_agent.ensure_lessons_index(initializer_target)
        init_project_agent.sync_baseline_skill_overrides(
            initializer_target,
            init_project_agent.REPO_ROOT,
        )
        init_project_agent.install_tool_agents(initializer_target, init_project_agent.REPO_ROOT)
        init_project_agent.copy_baseline_files(initializer_target, init_project_agent.REPO_ROOT)
        init_project_agent.ensure_local_files(initializer_target)
        init_project_agent.ensure_local_gitignore(initializer_target)

        with mock.patch.object(self.engine, "run_external_command"):
            status, _, error = self.invoke("apply")

        self.assertEqual(0, status, error)
        expected_files = file_contents(initializer_target)
        actual_files = file_contents(self.project)
        portable_manifest = Path("agent-context") / "skills-installed.json"
        expected_files.pop(portable_manifest, None)
        actual_files.pop(portable_manifest, None)
        self.assertEqual(
            {
                path: content.replace(b"\r\n", b"\n")
                for path, content in expected_files.items()
            },
            {
                path: content.replace(b"\r\n", b"\n")
                for path, content in actual_files.items()
            },
        )

    def test_apply_rejects_baseline_assets_missing_the_initializer_guard(self) -> None:
        baseline_agents = self.plugin_root / "assets" / "baseline" / "AGENTS.md"
        original_content = baseline_agents.read_bytes()
        self.addCleanup(baseline_agents.write_bytes, original_content)
        baseline_text = original_content.decode("utf-8")
        self.assertIn(self.engine.BASELINE_GUARD_MARKER, baseline_text)
        baseline_agents.write_text(
            baseline_text.replace(self.engine.BASELINE_GUARD_MARKER, "", 1),
            encoding="utf-8",
        )

        status, _, error = self.invoke("apply")

        self.assertEqual(2, status)
        self.assertIn("initializer guard", error)
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_installs_only_selected_skills_and_applies_independent_models(self) -> None:
        context_file = self.project / "agent-context" / "testing.md"
        context_file.parent.mkdir()
        context_file.write_text("project-owned context\n", encoding="utf-8")
        untracked_file = self.project / "local-notes.txt"
        untracked_file.write_text("keep this file\n", encoding="utf-8")

        status, _, _ = self.invoke(
            "apply",
            "--skill",
            "engineering-standards",
            "--skill",
            "workflow-feature-development",
            "--implementer-model",
            "model-for-implementation",
            "--reviewer-model",
            "model-for-review",
            "--diagnostician-model",
            "model-for-diagnosis",
        )

        self.assertEqual(0, status)
        installed_skills = {
            path.name
            for path in (self.project / ".agents" / "skills").iterdir()
            if path.is_dir()
        }
        self.assertEqual(
            {"engineering-standards", "workflow-feature-development"},
            installed_skills,
        )
        self.assertEqual("project-owned context\n", context_file.read_text(encoding="utf-8"))
        self.assertEqual("keep this file\n", untracked_file.read_text(encoding="utf-8"))
        self.assertEqual(
            [
                "engineering-standards",
                "workflow-feature-development",
            ],
            self.read_manifest()["skills"],
        )
        self.assertEqual(
            {
                "implementer": "model-for-implementation",
                "reviewer": "model-for-review",
                "diagnostician": "model-for-diagnosis",
            },
            self.read_manifest()["models"],
        )
        for role, agent_name in self.engine.MODEL_ROLES.items():
            config = tomllib.loads(
                (
                    self.project
                    / ".codex"
                    / "agents"
                    / f"{agent_name}.toml"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(self.read_manifest()["models"][role], config["model"])
            self.assertEqual("xhigh", config["model_reasoning_effort"])

    def test_preview_decline_leaves_conflicting_files_untouched_then_token_approves_exact_diff(self) -> None:
        self.assertEqual(0, self.invoke("apply")[0])
        agents_file = self.project / "AGENTS.md"
        agents_file.write_text("project edit to baseline\n", encoding="utf-8")

        preview_status, preview, _ = self.invoke("preview")
        self.assertEqual(0, preview_status)
        self.assertIn("--- AGENTS.md ---", preview)
        self.assertIn("-project edit to baseline", preview)
        token = preview.split("Approval token: ", 1)[1].splitlines()[0]

        declined_status, _, declined_error = self.invoke("apply")
        self.assertEqual(2, declined_status)
        self.assertIn("require explicit approval", declined_error)
        self.assertEqual("project edit to baseline\n", agents_file.read_text(encoding="utf-8"))

        approved_status, _, _ = self.invoke("apply", "--approve-conflicts", token)
        self.assertEqual(0, approved_status)
        self.assertNotIn("project edit to baseline", agents_file.read_text(encoding="utf-8"))

    def test_approval_token_cannot_apply_after_a_conflicting_file_changes(self) -> None:
        self.assertEqual(0, self.invoke("apply")[0])
        agents_file = self.project / "AGENTS.md"
        agents_file.write_text("first project edit\n", encoding="utf-8")
        _, preview, _ = self.invoke("preview")
        token = preview.split("Approval token: ", 1)[1].splitlines()[0]
        agents_file.write_text("second project edit\n", encoding="utf-8")

        status, _, error = self.invoke("apply", "--approve-conflicts", token)

        self.assertEqual(2, status)
        self.assertIn("require explicit approval", error)
        self.assertEqual("second project edit\n", agents_file.read_text(encoding="utf-8"))

    def test_sync_reapplies_saved_choices_and_does_not_remove_omitted_skills(self) -> None:
        self.assertEqual(
            0,
            self.invoke(
                "apply",
                "--skill",
                "engineering-standards",
                "--skill",
                "workflow-feature-development",
                "--implementer-model",
                "saved-implementer",
                "--reviewer-model",
                "saved-reviewer",
                "--diagnostician-model",
                "saved-diagnostician",
            )[0],
        )
        untracked_file = self.project / "untracked.txt"
        untracked_file.write_text("leave me\n", encoding="utf-8")

        status, _, _ = self.invoke("apply")

        self.assertEqual(0, status)
        self.assertTrue(
            (self.project / ".agents" / "skills" / "engineering-standards" / "SKILL.md").is_file()
        )
        self.assertTrue(
            (
                self.project
                / ".agents"
                / "skills"
                / "workflow-feature-development"
                / "SKILL.md"
            ).is_file()
        )
        self.assertEqual("leave me\n", untracked_file.read_text(encoding="utf-8"))
        self.assertEqual(
            {
                "implementer": "saved-implementer",
                "reviewer": "saved-reviewer",
                "diagnostician": "saved-diagnostician",
            },
            self.read_manifest()["models"],
        )

    def test_skill_removal_requires_preview_approval_and_an_explicit_choice(self) -> None:
        self.assertEqual(0, self.invoke("apply", "--skill", "engineering-standards")[0])
        skill_file = (
            self.project
            / ".agents"
            / "skills"
            / "engineering-standards"
            / "SKILL.md"
        )
        self.assertTrue(skill_file.is_file())

        _, preview, _ = self.invoke("preview", "--remove-skill", "engineering-standards")
        self.assertIn(".agents/skills/engineering-standards/SKILL.md", preview)
        token = preview.split("Approval token: ", 1)[1].splitlines()[0]
        declined_status, _, _ = self.invoke("apply", "--remove-skill", "engineering-standards")
        self.assertEqual(2, declined_status)
        self.assertTrue(skill_file.is_file())

        approved_status, _, _ = self.invoke(
            "apply",
            "--remove-skill",
            "engineering-standards",
            "--approve-conflicts",
            token,
        )

        self.assertEqual(0, approved_status)
        self.assertFalse(skill_file.exists())
        self.assertEqual([], self.read_manifest()["skills"])

    def test_legacy_manifest_migrates_without_source_path_or_rerunning_addons(self) -> None:
        agents_source = self.plugin_root / "assets" / "baseline" / "AGENTS.md"
        claude_source = self.plugin_root / "assets" / "baseline" / "CLAUDE.md"
        (self.project / "AGENTS.md").write_bytes(agents_source.read_bytes())
        (self.project / "CLAUDE.md").write_bytes(claude_source.read_bytes())
        for role, agent_name in self.engine.MODEL_ROLES.items():
            source = self.plugin_root / "assets" / "baseline" / ".codex" / "agents" / f"{agent_name}.toml"
            path = self.project / ".codex" / "agents" / f"{agent_name}.toml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                self.engine.apply_models_to_toml(
                    source.read_text(encoding="utf-8"),
                    f"legacy-{role}",
                ),
                encoding="utf-8",
            )
        manifest_path = self.project / "agent-context" / "skills-installed.json"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "source_root": "C:\\retired\\coding-agent-baseline\\skills",
                    "managed_skill_dirs": [str(self.engine.MANAGED_SKILLS_DIR)],
                    "skills": [
                        {
                            "source": "engineering-standards",
                            "installed_as": "engineering-standards",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        self.assertTrue(self.engine.legacy_baseline_signature(self.project))
        state = self.engine.load_project_state(self.project)
        self.assertEqual("legacy", state["kind"])
        self.assertEqual(["engineering-standards"], state["skills"])
        self.assertTrue(state["skip_external_installs"])
        with mock.patch.object(self.engine, "run_external_command") as run_external:
            status, output, _ = self.invoke("apply", "--approve-conflicts", "wrong-token")
            if status == 2 and "Approval token: " in output:
                token = output.split("Approval token: ", 1)[1].splitlines()[0]
                status, _, error = self.invoke("apply", "--approve-conflicts", token)
            else:
                error = ""

        self.assertEqual(0, status, error)
        run_external.assert_not_called()
        migrated = self.read_manifest()
        self.assertEqual("lean-coding-agent", migrated["baseline"])
        self.assertNotIn("source_root", migrated)
        self.assertEqual(["engineering-standards"], migrated["skills"])
        self.assertEqual(
            {"community_skills": True, "browser_tooling": True},
            migrated["addons"],
        )
        self.assertEqual(
            {
                "implementer": "legacy-implementer",
                "reviewer": "legacy-reviewer",
                "diagnostician": "legacy-diagnostician",
            },
            migrated["models"],
        )

    def test_foreign_manifest_is_rejected_without_target_changes(self) -> None:
        manifest_path = self.project / "agent-context" / "skills-installed.json"
        manifest_path.parent.mkdir()
        manifest_path.write_text(
            json.dumps(
                {
                    "source_root": "C:\\other-project\\skills",
                    "managed_skill_dirs": [".agents/skills"],
                    "skills": [],
                }
            ),
            encoding="utf-8",
        )
        before = manifest_path.read_bytes()

        status, _, error = self.invoke("apply")

        self.assertEqual(2, status)
        self.assertIn("ambiguous or foreign", error)
        self.assertEqual(before, manifest_path.read_bytes())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_optional_addons_run_only_after_selection_and_failures_keep_local_files(self) -> None:
        package_file = self.project / "package.json"
        package_file.write_text(json.dumps({"packageManager": "pnpm@10.0.0"}), encoding="utf-8")
        with mock.patch.object(
            self.engine,
            "run_external_command",
            side_effect=["community install failed"] + [None] * 6,
        ) as run_external:
            status, _, error = self.invoke(
                "apply",
                "--community-skills",
                "--browser-tooling",
            )

        self.assertEqual(1, status)
        self.assertIn("community install failed", error)
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertEqual(7, run_external.call_count)
        commands = [call.args[0] for call in run_external.call_args_list]
        self.assertTrue(all(command[0] == "npx.cmd" for command in commands[:5]))
        self.assertEqual(
            ["pnpm.cmd", "add", "--save-dev", "agent-browser@latest"],
            commands[5],
        )
        self.assertEqual(
            ["pnpm.cmd", "exec", "agent-browser", "install"],
            commands[6],
        )


if __name__ == "__main__":
    unittest.main()
