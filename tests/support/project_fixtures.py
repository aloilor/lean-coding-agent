from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).parents[2]


def temporary_project(test_case: Any) -> Path:
    temporary_directory = tempfile.TemporaryDirectory()
    test_case.addCleanup(temporary_directory.cleanup)
    project = Path(temporary_directory.name) / "project"
    project.mkdir()
    return project


def temporary_plugin(test_case: Any) -> Path:
    temporary_directory = tempfile.TemporaryDirectory()
    test_case.addCleanup(temporary_directory.cleanup)
    plugin = Path(temporary_directory.name) / "installed-plugin-copy"
    subprocess.run(
        [
            "node",
            str(REPO_ROOT / "scripts" / "build_codex_plugin.mjs"),
            "--output",
            str(plugin),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return plugin


def file_contents(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    }