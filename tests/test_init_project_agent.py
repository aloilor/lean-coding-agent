import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "init_project_agent.py"
SPEC = importlib.util.spec_from_file_location("init_project_agent", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
INIT_PROJECT_AGENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INIT_PROJECT_AGENT)


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
