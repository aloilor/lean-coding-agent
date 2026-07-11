import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).parents[1]
GATE_SOURCE = REPO_ROOT / "templates" / "php-laravel" / "scripts" / "quality-gate"
CHECKS = ["style", "static", "tests", "duplication", "architecture", "audit"]
SCRIPT_NAMES = [
    "quality:style",
    "quality:static",
    "quality:test",
    "quality:duplication",
    "quality:architecture",
    "quality:audit",
]


def find_posix_shell() -> str | None:
    shell = shutil.which("sh")
    if shell:
        return shell

    for candidate in (
        Path(r"C:\Program Files\Git\bin\sh.exe"),
        Path(r"C:\Program Files\Git\usr\bin\sh.exe"),
    ):
        if candidate.is_file():
            return str(candidate)
    return None


def find_posix_command(command_name: str) -> str | None:
    executable = shutil.which(command_name)
    if executable:
        return executable

    shell = find_posix_shell()
    if shell is None:
        return None
    shell_path = Path(shell)
    for directory in (shell_path.parent, shell_path.parent.parent / "usr" / "bin"):
        for filename in (command_name, f"{command_name}.exe"):
            candidate = directory / filename
            if candidate.is_file():
                return str(candidate)
    return None


@unittest.skipUnless(find_posix_shell(), "a POSIX shell is required")
class QualityGateIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.bin_dir = self.repo / "fake-bin"
        self.bin_dir.mkdir()
        self.gate_path = self.repo / "scripts" / "quality-gate"
        self.gate_path.parent.mkdir()
        shutil.copy2(GATE_SOURCE, self.gate_path)
        subprocess.run(["git", "init", "--quiet", str(self.repo)], check=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def install_fake_composer(self) -> None:
        composer = self.bin_dir / "composer"
        composer.write_text(
            """#!/usr/bin/env sh
if [ "$1" = "run-script" ] && [ "$2" = "--list" ]; then
    for script in $AVAILABLE_SCRIPTS; do
        printf '  %s fixture script\\n' "$script"
    done
    exit 0
fi

if [ "$1" = "--quiet" ]; then
    shift
else
    printf '> %s\\n' "$1"
fi
script=$1
printf '%s\\n' "$script" >> "$EXECUTION_LOG"
printf '{\"script\":\"%s\"}\\n' "$script"
printf 'stderr for %s\\n' "$script" >&2

for failing_script in $FAIL_SCRIPTS; do
    if [ "$script" = "$failing_script" ]; then
        exit 7
    fi
done
exit 0
""",
            encoding="utf-8",
        )
        composer.chmod(0o755)

    def install_required_command_wrappers(self) -> None:
        for command_name in ("rm", "mkdir", "date", "cat", "mv"):
            executable = find_posix_command(command_name)
            if executable is None:
                self.skipTest(f"{command_name} is required by the POSIX gate")
            executable_path = Path(executable).as_posix().replace("'", "'\\''")
            wrapper = self.bin_dir / command_name
            wrapper.write_text(
                f"#!/bin/sh\nexec '{executable_path}' \"$@\"\n",
                encoding="utf-8",
            )
            wrapper.chmod(0o755)

    def run_gate(
        self,
        *,
        available_scripts: list[str] | None = None,
        failing_scripts: list[str] | None = None,
        composer_absent: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if composer_absent:
            self.install_required_command_wrappers()
            environment["PATH"] = str(self.bin_dir)
        else:
            environment["PATH"] = os.pathsep.join([str(self.bin_dir), environment["PATH"]])
        environment["AVAILABLE_SCRIPTS"] = " ".join(available_scripts or [])
        environment["FAIL_SCRIPTS"] = " ".join(failing_scripts or [])
        environment["EXECUTION_LOG"] = str(self.repo / "execution.log")
        return subprocess.run(
            [find_posix_shell(), str(self.gate_path)],
            cwd=self.repo,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def read_manifest(self) -> dict:
        return json.loads(
            (self.repo / ".quality-reports" / "manifest.json").read_text(encoding="utf-8")
        )

    def test_all_checks_pass_in_order_with_stable_evidence_paths(self) -> None:
        self.install_fake_composer()

        result = self.run_gate(available_scripts=SCRIPT_NAMES)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            SCRIPT_NAMES,
            (self.repo / "execution.log").read_text(encoding="utf-8").splitlines(),
        )
        manifest = self.read_manifest()
        self.assertEqual(1, manifest["schema_version"])
        self.assertRegex(manifest["generated_at"], r"^\d{4}-\d{2}-\d{2}T.*Z$")
        self.assertEqual(CHECKS, [check["name"] for check in manifest["checks"]])
        self.assertEqual(["pass"] * 6, [check["status"] for check in manifest["checks"]])
        self.assertEqual([0] * 6, [check["exit_code"] for check in manifest["checks"]])
        self.assertEqual(
            [
                ".quality-reports/style.txt",
                ".quality-reports/static-analysis.json",
                ".quality-reports/tests.txt",
                ".quality-reports/duplication.txt",
                ".quality-reports/architecture.json",
                ".quality-reports/dependency-audit.json",
            ],
            [check["report"] for check in manifest["checks"]],
        )
        self.assertEqual(
            [f".quality-reports/{name}.stderr.log" for name in CHECKS],
            [check["stderr"] for check in manifest["checks"]],
        )

    def test_failure_does_not_prevent_later_checks_and_exits_two(self) -> None:
        self.install_fake_composer()

        result = self.run_gate(
            available_scripts=SCRIPT_NAMES,
            failing_scripts=["quality:style"],
        )

        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual(
            SCRIPT_NAMES,
            (self.repo / "execution.log").read_text(encoding="utf-8").splitlines(),
        )
        checks = self.read_manifest()["checks"]
        self.assertEqual("fail", checks[0]["status"])
        self.assertEqual(7, checks[0]["exit_code"])
        self.assertEqual(["pass"] * 5, [check["status"] for check in checks[1:]])

    def test_missing_script_is_skipped_while_configured_checks_run(self) -> None:
        self.install_fake_composer()

        result = self.run_gate(available_scripts=["quality:style", "quality:test"])

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["quality:style", "quality:test"],
            (self.repo / "execution.log").read_text(encoding="utf-8").splitlines(),
        )
        checks = self.read_manifest()["checks"]
        self.assertEqual(
            ["pass", "skipped", "pass", "skipped", "skipped", "skipped"],
            [check["status"] for check in checks],
        )
        self.assertEqual([0, None, 0, None, None, None], [check["exit_code"] for check in checks])

    def test_composer_absence_writes_all_skipped_manifest(self) -> None:
        result = self.run_gate(composer_absent=True)

        self.assertEqual(0, result.returncode, result.stderr)
        checks = self.read_manifest()["checks"]
        self.assertEqual(["skipped"] * 6, [check["status"] for check in checks])
        self.assertEqual([None] * 6, [check["exit_code"] for check in checks])

    def test_each_run_removes_stale_evidence_and_keeps_stderr_separate(self) -> None:
        self.install_fake_composer()
        reports = self.repo / ".quality-reports"
        reports.mkdir()
        stale_report = reports / "stale.txt"
        stale_report.write_text("old evidence", encoding="utf-8")

        result = self.run_gate(available_scripts=SCRIPT_NAMES)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(stale_report.exists())
        static_report = (reports / "static-analysis.json").read_text(encoding="utf-8")
        self.assertEqual('{"script":"quality:static"}\n', static_report)
        self.assertNotIn("stderr", static_report)
        self.assertEqual(
            "stderr for quality:static\n",
            (reports / "static.stderr.log").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
