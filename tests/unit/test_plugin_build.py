import tempfile
import unittest
from pathlib import Path

from scripts import init_project_agent
from scripts.build_codex_plugin import build_plugin, generated_files


class PluginBuildTest(unittest.TestCase):
    def test_baseline_assets_match_initializer_outputs_without_repository_lessons(
        self,
    ) -> None:
        generated = generated_files()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            init_project_agent.copy_baseline_files(target, init_project_agent.REPO_ROOT)
            init_project_agent.ensure_lessons_index(target)

            generated_paths = (
                Path("AGENTS.md"),
                Path("CLAUDE.md"),
                Path(".agents/lessons/LESSONS.md"),
            )
            for relative in generated_paths:
                asset_path = Path("assets") / "baseline" / relative
                self.assertEqual(
                    (target / relative).read_text(encoding="utf-8"),
                    generated[asset_path].decode("utf-8"),
                )

        bundled_lessons = {
            path.relative_to(Path("assets") / "baseline")
            for path in generated
            if path.parts[:4] == ("assets", "baseline", ".agents", "lessons")
        }
        self.assertEqual(
            {Path(".agents") / "lessons" / "LESSONS.md"},
            bundled_lessons,
        )

    def test_generated_assets_are_current_and_check_detects_stale_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plugin-copy"
            self.assertEqual([], build_plugin(output))
            self.assertEqual([], build_plugin(output, check=True))

            stale_skill = output / "skills" / "setup-project" / "SKILL.md"
            stale_skill.write_text("changed generated output\n", encoding="utf-8")
            problems = build_plugin(output, check=True)
            self.assertEqual(
                ["stale generated file: skills/setup-project/SKILL.md"],
                problems,
            )

            self.assertEqual([], build_plugin(output))
            self.assertEqual([], build_plugin(output, check=True))


if __name__ == "__main__":
    unittest.main()
