import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import setup_project


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
                    project = Path(temp_dir)
                    for lockfile in lockfiles:
                        (project / lockfile).touch()
                    self.assertEqual(
                        expected,
                        setup_project.detect_package_manager(project, package_json),
                    )

    def test_generates_browser_install_commands_for_selected_manager(self) -> None:
        with mock.patch.object(setup_project.os, "name", "nt"):
            commands = setup_project.browser_tooling_commands("pnpm")

        self.assertEqual(
            [
                ["pnpm.cmd", "add", "--save-dev", "agent-browser@latest"],
                ["pnpm.cmd", "exec", "agent-browser", "install"],
            ],
            commands,
        )

    def test_reports_missing_or_failed_external_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            with mock.patch.object(
                setup_project.subprocess,
                "run",
                side_effect=subprocess.CalledProcessError(2, ["npx", "skills"]),
            ):
                failure = setup_project.run_external_command(["npx", "skills"], project)

            self.assertEqual(
                "Command failed with exit code 2: npx skills",
                failure,
            )

            with mock.patch.object(
                setup_project.subprocess,
                "run",
                side_effect=FileNotFoundError("npx"),
            ):
                missing = setup_project.run_external_command(["npx", "skills"], project)
            self.assertIn("Command unavailable (npx)", missing)


if __name__ == "__main__":
    unittest.main()
