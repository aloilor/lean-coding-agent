#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR = REPO_ROOT / "plugins" / "lean-coding-agent"
DEFAULT_SETUP_SKILL_DIR = REPO_ROOT / "skills" / "setup-project"
GENERATED_INDEX = ".generated-files.json"


class BuildError(Exception):
    pass


def initializer_templates() -> ModuleType:
    if __package__:
        from . import init_project_agent
    else:
        import init_project_agent
    return init_project_agent


def add_file(files: dict[Path, bytes], source: Path, destination: Path) -> None:
    resolved_source = source.resolve()
    try:
        resolved_source.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise BuildError(f"Build source escapes the repository: {source}") from exc
    if not resolved_source.is_file():
        raise BuildError(f"Required build source is missing: {source}")
    files[destination] = resolved_source.read_bytes()


def add_tree(
    files: dict[Path, bytes],
    source: Path,
    destination: Path,
    *,
    excluded_roots: set[str] | None = None,
) -> None:
    if not source.is_dir():
        return
    for source_path in sorted(path for path in source.rglob("*") if path.is_file()):
        if ".git" in source_path.parts or "__pycache__" in source_path.parts:
            continue
        relative_path = source_path.relative_to(source)
        if excluded_roots and relative_path.parts[0] in excluded_roots:
            continue
        add_file(files, source_path, destination / relative_path)


def generated_files() -> dict[Path, bytes]:
    initializer = initializer_templates()
    files: dict[Path, bytes] = {}
    add_file(files, REPO_ROOT / "plugin-src" / "plugin.json", Path("plugin.json"))
    add_file(
        files,
        REPO_ROOT / "plugin-src" / "skills" / "setup-project" / "SKILL.md",
        Path("skills") / "setup-project" / "SKILL.md",
    )
    add_file(
        files,
        REPO_ROOT / "scripts" / "setup_project.py",
        Path("skills") / "setup-project" / "scripts" / "setup_project.py",
    )
    add_file(
        files,
        REPO_ROOT / "plugin-src" / "upstream-skills.json",
        Path("assets") / "upstream-skills.json",
    )
    baseline = Path("assets") / "baseline"
    for filename in ("AGENTS.md", "CLAUDE.md"):
        source = REPO_ROOT / filename
        files[baseline / filename] = initializer.guarded_baseline_content(
            filename,
            source.read_text(encoding="utf-8"),
        ).encode("utf-8")
    add_tree(files, REPO_ROOT / "agent-context", baseline / "agent-context")
    files[baseline / ".agents" / "lessons" / "LESSONS.md"] = (
        initializer.lessons_index_content().encode("utf-8")
    )
    add_tree(files, REPO_ROOT / ".codex" / "agents", baseline / ".codex" / "agents")
    add_tree(
        files,
        REPO_ROOT / "skills",
        baseline / "skills",
        excluded_roots={"setup-project"},
    )
    add_file(
        files,
        REPO_ROOT / "docs" / "incidents" / "README.md",
        baseline / "docs" / "incidents" / "README.md",
    )
    files[Path(GENERATED_INDEX)] = (
        json.dumps(sorted(path.as_posix() for path in files), indent=2) + "\n"
    ).encode("utf-8")
    return files


def current_files(destination: Path) -> dict[Path, bytes]:
    if not destination.exists():
        return {}
    if destination.is_symlink() or not destination.is_dir():
        raise BuildError(f"Generated output must be a regular directory: {destination}")
    return {
        path.relative_to(destination): path.read_bytes()
        for path in destination.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def check_generated_tree(destination: Path, expected: dict[Path, bytes]) -> list[str]:
    actual = current_files(destination)
    problems = []
    for relative_path in sorted(set(expected) | set(actual)):
        if relative_path not in actual:
            problems.append(f"missing generated file: {relative_path.as_posix()}")
        elif relative_path not in expected:
            problems.append(f"unexpected package file: {relative_path.as_posix()}")
        elif actual[relative_path] != expected[relative_path]:
            problems.append(f"stale generated file: {relative_path.as_posix()}")
    return problems


def setup_skill_files(plugin_files: dict[Path, bytes]) -> dict[Path, bytes]:
    """Create the self-contained setup skill distributed by the Skills CLI."""
    setup_skill = Path("skills") / "setup-project"
    files = {
        Path("SKILL.md"): plugin_files[setup_skill / "SKILL.md"],
        Path("scripts") / "setup_project.py": plugin_files[
            setup_skill / "scripts" / "setup_project.py"
        ],
    }
    for relative_path, content in plugin_files.items():
        if relative_path.parts[0] == "assets":
            files[relative_path] = content
    files[Path(GENERATED_INDEX)] = (
        json.dumps(sorted(path.as_posix() for path in files), indent=2) + "\n"
    ).encode("utf-8")
    return files


def build_generated_tree(
    destination: Path,
    expected: dict[Path, bytes],
    *,
    check: bool = False,
) -> list[str]:
    destination = destination.expanduser().resolve()
    if check:
        return check_generated_tree(destination, expected)

    current_files(destination)
    previous_generated: set[Path] = set()
    index_path = destination / GENERATED_INDEX
    if index_path.is_file():
        try:
            previous = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(previous, list) and all(isinstance(item, str) for item in previous):
                previous_generated = {Path(item) for item in previous}
        except (OSError, json.JSONDecodeError):
            previous_generated = set()
    for relative_path in previous_generated - set(expected):
        stale_path = destination / relative_path
        try:
            stale_path.resolve().relative_to(destination)
        except ValueError as exc:
            raise BuildError(f"Generated index contains an unsafe path: {relative_path}") from exc
        if stale_path.is_file():
            stale_path.unlink()
    for relative_path, content in expected.items():
        output_path = destination / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
    for directory in sorted(
        (path for path in destination.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        try:
            directory.rmdir()
        except OSError:
            pass
    return check_generated_tree(destination, expected)


def build_plugin(destination: Path = DEFAULT_PLUGIN_DIR, *, check: bool = False) -> list[str]:
    return build_generated_tree(destination, generated_files(), check=check)


def build_setup_skill(
    destination: Path = DEFAULT_SETUP_SKILL_DIR,
    *,
    check: bool = False,
) -> list[str]:
    return build_generated_tree(
        destination,
        setup_skill_files(generated_files()),
        check=check,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build or check the Lean Coding Agent plugin and Skills CLI installer."
    )
    parser.add_argument("--check", action="store_true", help="Fail when generated output is stale.")
    parser.add_argument("--output", type=Path, default=DEFAULT_PLUGIN_DIR)
    args = parser.parse_args(argv)
    try:
        plugin_problems = build_plugin(args.output, check=args.check)
        skill_problems = build_setup_skill(check=args.check)
    except BuildError as exc:
        print(f"Plugin build failed: {exc}", file=sys.stderr)
        return 2
    problems = plugin_problems + [
        f"Skills CLI installer: {problem}" for problem in skill_problems
    ]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        if args.check:
            print("Run python scripts/build_codex_plugin.py to refresh generated package files.")
        return 1
    print(f"Plugin package is {'current' if args.check else 'built'}: {args.output.resolve()}")
    print(
        f"Skills CLI installer is {'current' if args.check else 'built'}: "
        f"{DEFAULT_SETUP_SKILL_DIR.resolve()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
