#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import stat
import shutil
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
GLOBAL_SKILLS_ROOT = REPO_ROOT / "global-skills"
MANAGED_SKILLS_DIRS = [
    Path(".codex") / "skills",
    Path(".claude") / "skills",
]
MANIFEST_NAME = "global-skills-installed.json"
LEGACY_MANIFEST_NAME = "awesome-codex-skills-installed.json"
LEGACY_CONFIG_NAME = "awesome-codex-skills-subset.json"
AGENT_CONTEXT_DIRNAME = "agent-context"
AGENT_CONTEXT_README_NAME = "README.md"
LEGACY_AGENT_CONTEXT_DIRNAME = "anget-context"
LEGACY_CLONE_DIR = Path(LEGACY_AGENT_CONTEXT_DIRNAME) / "awesome-codex-skills"
BASELINE_FILENAMES = ["AGENTS.md", "CLAUDE.md"]
OVERRIDE_FILENAMES = ["AGENTS.override.md", "CLAUDE.override.md"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a project repo with this shared agent baseline, creates "
            "private override files and agent-context, and installs this repo's "
            "global skills into the target repo's .codex/skills and .claude/skills "
            "directories."
        )
    )
    parser.add_argument(
        "target_repo",
        help="Path to the project repo that should receive the agent bootstrap files.",
    )
    return parser.parse_args()


def ensure_target_repo(target_repo: Path) -> None:
    if not target_repo.exists():
        raise SystemExit(f"Target repo does not exist: {target_repo}")
    if not target_repo.is_dir():
        raise SystemExit(f"Target repo is not a directory: {target_repo}")


def ensure_global_skills_root(global_skills_root: Path) -> None:
    if not global_skills_root.exists():
        raise SystemExit(f"Global skills directory does not exist: {global_skills_root}")
    if not global_skills_root.is_dir():
        raise SystemExit(f"Global skills path is not a directory: {global_skills_root}")


def copy_baseline_files(target_repo: Path, shared_repo_root: Path) -> list[Path]:
    copied_paths: list[Path] = []

    for filename in BASELINE_FILENAMES:
        source_path = shared_repo_root / filename
        if not source_path.exists():
            raise SystemExit(f"Shared baseline file does not exist: {source_path}")

        target_path = target_repo / filename
        shutil.copy2(source_path, target_path)
        copied_paths.append(target_path)

    return copied_paths


def override_file_content(filename: str) -> str:
    return "\n".join(
        [
            f"# {filename}",
            "",
            "Local private overrides for this project.",
            "",
            "This file is ignored by git and is safe for machine-specific notes.",
            "",
        ]
    )


def ensure_override_files(target_repo: Path) -> list[Path]:
    override_paths: list[Path] = []

    for filename in OVERRIDE_FILENAMES:
        override_path = target_repo / filename
        if not override_path.exists():
            override_path.write_text(override_file_content(filename), encoding="utf-8")
        override_paths.append(override_path)

    return override_paths


def ensure_override_gitignore(target_repo: Path) -> Path:
    gitignore_path = target_repo / ".gitignore"
    existing = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    existing_lines = set(existing.splitlines())
    missing_lines = [filename for filename in OVERRIDE_FILENAMES if filename not in existing_lines]

    if missing_lines:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        addition = "\n".join(missing_lines) + "\n"
        gitignore_path.write_text(existing + prefix + addition, encoding="utf-8")

    return gitignore_path


def ensure_agent_context_readme(agent_context_dir: Path) -> Path:
    readme_path = agent_context_dir / AGENT_CONTEXT_README_NAME
    if not readme_path.exists():
        content = "\n".join(
            [
                "# Project Agent Context",
                "",
                "Add shared project-specific context here.",
                "",
                "Good starting points:",
                "",
                "- folder structure",
                "- tech stack",
                "- architecture conventions",
                "- testing expectations",
                "- project-specific workflows",
                "",
                "Keep private or machine-specific notes in the root override files instead.",
                "",
            ]
        )
        readme_path.write_text(content, encoding="utf-8")

    return readme_path


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {"skills": []}

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Managed skills manifest is not valid JSON: {manifest_path}") from exc


def discover_global_skills(global_skills_root: Path) -> list[dict]:
    installs: list[dict] = []

    for source_dir in sorted(path for path in global_skills_root.iterdir() if path.is_dir()):
        if not (source_dir / "SKILL.md").exists():
            continue
        installs.append(
            {
                "source": source_dir.name,
                "installed_as": source_dir.name,
            }
        )

    if not installs:
        raise SystemExit(f"No installable skills found in: {global_skills_root}")

    return installs


def safe_rmtree(path: Path, root: Path) -> None:
    def handle_remove_readonly(func, child_path, exc_info) -> None:
        _ = func
        _ = exc_info
        os.chmod(child_path, stat.S_IWRITE)
        if os.path.isdir(child_path):
            shutil.rmtree(child_path, onexc=handle_remove_readonly)
        else:
            os.unlink(child_path)

    path = path.resolve()
    root = root.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"Refusing to remove path outside managed root: {path}") from exc

    if path.exists():
        shutil.rmtree(path, onexc=handle_remove_readonly)


def load_managed_skill_names(manifest_paths: list[Path]) -> set[str]:
    managed_names: set[str] = set()

    for manifest_path in manifest_paths:
        manifest = load_manifest(manifest_path)
        for entry in manifest.get("skills", []):
            if isinstance(entry, dict) and isinstance(entry.get("installed_as"), str):
                managed_names.add(entry["installed_as"])

    return managed_names


def cleanup_legacy_bootstrap(target_repo: Path) -> None:
    legacy_agent_context_dir = target_repo / LEGACY_AGENT_CONTEXT_DIRNAME
    legacy_agent_context_dir.mkdir(parents=True, exist_ok=True)

    legacy_clone_dir = target_repo / LEGACY_CLONE_DIR
    if legacy_clone_dir.exists():
        safe_rmtree(legacy_clone_dir, legacy_agent_context_dir)

    for legacy_name in [LEGACY_CONFIG_NAME, LEGACY_MANIFEST_NAME]:
        legacy_path = legacy_agent_context_dir / legacy_name
        if legacy_path.exists():
            legacy_path.unlink()

    if legacy_agent_context_dir.exists() and not any(legacy_agent_context_dir.iterdir()):
        legacy_agent_context_dir.rmdir()


def sync_skills(
    target_repo: Path,
    installs: list[dict],
    manifest_path: Path,
    legacy_manifest_path: Path,
) -> list[Path]:
    skills_roots = [target_repo / relative_dir for relative_dir in MANAGED_SKILLS_DIRS]
    for skills_root in skills_roots:
        skills_root.mkdir(parents=True, exist_ok=True)

    previous_names = load_managed_skill_names([manifest_path, legacy_manifest_path])
    current_names = {entry["installed_as"] for entry in installs}

    for removed_name in sorted(previous_names - current_names):
        for skills_root in skills_roots:
            safe_rmtree(skills_root / removed_name, skills_root)

    for install in installs:
        source_dir = GLOBAL_SKILLS_ROOT / install["source"]
        for skills_root in skills_roots:
            dest_dir = skills_root / install["installed_as"]
            safe_rmtree(dest_dir, skills_root)
            shutil.copytree(
                source_dir,
                dest_dir,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )

    manifest = {
        "source_root": str(GLOBAL_SKILLS_ROOT),
        "managed_skill_dirs": [str(path) for path in MANAGED_SKILLS_DIRS],
        "skills": installs,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return skills_roots


def main() -> int:
    args = parse_args()
    target_repo = Path(args.target_repo).expanduser().resolve()

    ensure_target_repo(target_repo)
    ensure_global_skills_root(GLOBAL_SKILLS_ROOT)

    agent_context_dir = target_repo / AGENT_CONTEXT_DIRNAME
    agent_context_dir.mkdir(parents=True, exist_ok=True)
    agent_context_readme_path = ensure_agent_context_readme(agent_context_dir)
    manifest_path = agent_context_dir / MANIFEST_NAME
    legacy_manifest_path = target_repo / LEGACY_AGENT_CONTEXT_DIRNAME / LEGACY_MANIFEST_NAME

    baseline_paths = copy_baseline_files(target_repo, REPO_ROOT)
    override_paths = ensure_override_files(target_repo)
    gitignore_path = ensure_override_gitignore(target_repo)
    installs = discover_global_skills(GLOBAL_SKILLS_ROOT)
    skills_roots = sync_skills(target_repo, installs, manifest_path, legacy_manifest_path)
    cleanup_legacy_bootstrap(target_repo)

    print(f"Initialized project repo: {target_repo}")
    print("Copied baseline files:")
    for baseline_path in baseline_paths:
        print(f"- {baseline_path}")
    print("Ensured private override files:")
    for override_path in override_paths:
        print(f"- {override_path}")
    print(f"Ensured project context file: {agent_context_readme_path}")
    print(f"Updated ignore rules: {gitignore_path}")
    print(f"Installed {len(installs)} global skills into:")
    for skills_root in skills_roots:
        print(f"- {skills_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
