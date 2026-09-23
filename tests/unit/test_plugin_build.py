from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support.project_fixtures import REPO_ROOT


class PluginBuildTest(unittest.TestCase):
    def test_setup_plugin_does_not_bundle_starter_context_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plugin-copy"
            build = self.run_builder(output)
            self.assertEqual(0, build.returncode, build.stderr)
            self.assertFalse(
                (
                    output
                    / "skills"
                    / "setup-lean-coding-agent"
                    / "references"
                    / "agent-context"
                ).exists()
            )

    def test_every_installable_skill_is_bundled_from_its_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plugin-copy"
            self.assertEqual(0, self.run_builder(output).returncode)
            self.assertEqual(0, self.run_builder(output, check=True).returncode)

            skill_dirs = [
                path
                for path in (REPO_ROOT / "skills").iterdir()
                if path.is_dir() and (path / "SKILL.md").is_file()
            ]
            for skill_dir in skill_dirs:
                packaged_skill = Path("skills") / skill_dir.name
                self.assertEqual(
                    (skill_dir / "SKILL.md").read_bytes(),
                    (output / packaged_skill / "SKILL.md").read_bytes(),
                )

    def test_generated_plugin_is_current_and_check_detects_stale_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plugin-copy"
            self.assertEqual(0, self.run_builder(output).returncode)
            self.assertEqual(0, self.run_builder(output, check=True).returncode)

            stale_skill = output / "skills" / "engineering-standards" / "SKILL.md"
            stale_skill.write_text("changed generated output\n", encoding="utf-8")
            stale_check = self.run_builder(output, check=True)
            self.assertEqual(1, stale_check.returncode)
            self.assertIn("stale generated file: skills/engineering-standards/SKILL.md", stale_check.stderr)

            self.assertEqual(0, self.run_builder(output).returncode)
            self.assertEqual(0, self.run_builder(output, check=True).returncode)

    def run_builder(self, output: Path, check: bool = False) -> subprocess.CompletedProcess[str]:
        command = [
            "node",
            str(REPO_ROOT / "scripts" / "build_codex_plugin.mjs"),
            "--output",
            str(output),
        ]
        if check:
            command.append("--check")
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
