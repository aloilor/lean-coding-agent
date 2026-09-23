import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

from tests.support.project_fixtures import REPO_ROOT, temporary_plugin


class PluginPackageContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = unittest.TestCase()
        cls.plugin_root = temporary_plugin(fixture)
        cls.addClassCleanup(fixture.doCleanups)

    def test_portable_manifest_and_single_setup_skill_match_plugin_contract(self) -> None:
        manifest = json.loads((self.plugin_root / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual("lean-coding-agent", manifest["name"])
        self.assertEqual("0.1.0", manifest["version"])
        self.assertEqual("MIT", manifest["license"])
        self.assertTrue(manifest["author"]["name"])
        self.assertIn("extensions", manifest)
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertEqual("Lean Coding Agent", interface["displayName"])
        self.assertTrue(interface["defaultPrompt"])
        self.assertEqual(["Interactive", "Write"], interface["capabilities"])
        skill_dirs = [
            path.name
            for path in (self.plugin_root / "skills").iterdir()
            if path.is_dir()
        ]
        self.assertEqual(["setup-project"], skill_dirs)
        self.assertTrue((self.plugin_root / "skills" / "setup-project" / "SKILL.md").is_file())

    def test_marketplace_source_and_presentation_resolve_to_the_plugin_package(self) -> None:
        marketplace_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        entry = marketplace["plugins"][0]
        source_path = entry["source"]["path"]

        self.assertEqual("lean-coding-agent", marketplace["name"])
        self.assertEqual("Lean Coding Agent", marketplace["interface"]["displayName"])
        self.assertEqual("lean-coding-agent", entry["name"])
        self.assertEqual("./plugins/lean-coding-agent", source_path)
        self.assertTrue((REPO_ROOT / source_path.removeprefix("./")).is_dir())

    def test_packaged_skill_links_resolve_inside_the_plugin_copy(self) -> None:
        skill_roots = [
            self.plugin_root / "skills",
            self.plugin_root / "assets" / "baseline" / "skills",
        ]
        markdown_files = [
            path
            for skill_root in skill_roots
            for path in skill_root.rglob("SKILL.md")
        ]
        self.assertTrue(markdown_files)
        unresolved = []
        external_schemes = {"http", "https", "mailto", "tel"}
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for markdown_file in markdown_files:
            for link in link_pattern.findall(markdown_file.read_text(encoding="utf-8")):
                destination = link.strip().split()[0].strip("<>")
                parsed = urlsplit(destination)
                if parsed.scheme.lower() in external_schemes or destination.startswith("#"):
                    continue
                if parsed.scheme or parsed.netloc:
                    continue
                relative_target = Path(unquote(parsed.path))
                if not parsed.path:
                    continue
                resolved = (markdown_file.parent / relative_target).resolve()
                try:
                    resolved.relative_to(self.plugin_root.resolve())
                except ValueError:
                    unresolved.append(f"{markdown_file.relative_to(self.plugin_root)} -> {link}")
                    continue
                if not resolved.exists():
                    unresolved.append(f"{markdown_file.relative_to(self.plugin_root)} -> {link}")

        self.assertEqual([], unresolved)

    def test_bundled_engine_and_assets_do_not_depend_on_the_source_checkout(self) -> None:
        engine_path = (
            self.plugin_root
            / "skills"
            / "setup-project"
            / "scripts"
            / "setup_project.py"
        )
        self.assertTrue(engine_path.is_file())
        self.assertTrue((self.plugin_root / "assets" / "baseline" / "AGENTS.md").is_file())
        self.assertTrue((self.plugin_root / "assets" / "baseline" / ".codex" / "agents").is_dir())
        self.assertTrue((self.plugin_root / "assets" / "upstream-skills.json").is_file())
        self.assertNotIn(str(REPO_ROOT), engine_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
