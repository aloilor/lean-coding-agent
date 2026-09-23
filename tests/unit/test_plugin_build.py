import tempfile
import unittest
from pathlib import Path

from scripts.build_codex_plugin import build_plugin, generated_files


class PluginBuildTest(unittest.TestCase):
    def test_every_installable_skill_is_bundled_from_its_canonical_source(self) -> None:
        generated = generated_files()
        skill_dirs = [
            path
            for path in (Path(__file__).parents[2] / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        ]
        for skill_dir in skill_dirs:
            packaged_skill = Path("skills") / skill_dir.name
            self.assertEqual(
                (skill_dir / "SKILL.md").read_bytes(),
                generated[packaged_skill / "SKILL.md"],
            )

    def test_generated_plugin_is_current_and_check_detects_stale_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plugin-copy"
            self.assertEqual([], build_plugin(output))
            self.assertEqual([], build_plugin(output, check=True))

            stale_skill = output / "skills" / "engineering-standards" / "SKILL.md"
            stale_skill.write_text("changed generated output\n", encoding="utf-8")
            problems = build_plugin(output, check=True)
            self.assertEqual(
                ["stale generated file: skills/engineering-standards/SKILL.md"],
                problems,
            )

            self.assertEqual([], build_plugin(output))
            self.assertEqual([], build_plugin(output, check=True))


if __name__ == "__main__":
    unittest.main()
