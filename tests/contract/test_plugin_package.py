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

    def test_portable_manifest_and_complete_skill_bundle_match_plugin_contract(self) -> None:
        manifest = json.loads((self.plugin_root / "plugin.json").read_text(encoding="utf-8"))
        package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))

        self.assertEqual("lean-coding-agent", manifest["name"])
        self.assertEqual(package["version"], manifest["version"])
        self.assertEqual("MIT", manifest["license"])
        self.assertTrue(manifest["author"]["name"])
        self.assertIn("extensions", manifest)
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertEqual("Lean Coding Agent", interface["displayName"])
        self.assertTrue(interface["defaultPrompt"])
        self.assertEqual(["Interactive", "Write"], interface["capabilities"])
        expected_skill_dirs = sorted(
            path.name
            for path in (REPO_ROOT / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        skill_dirs = sorted(
            path.name
            for path in (self.plugin_root / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        self.assertEqual(expected_skill_dirs, skill_dirs)
        self.assertNotIn("setup-project", skill_dirs)

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
        markdown_files = list((self.plugin_root / "skills").rglob("SKILL.md"))
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

    def test_plugin_package_has_no_project_installer_or_project_baseline_copy(self) -> None:
        self.assertFalse((self.plugin_root / "skills" / "setup-project").exists())
        self.assertFalse((self.plugin_root / "assets" / "baseline").exists())


if __name__ == "__main__":
    unittest.main()
