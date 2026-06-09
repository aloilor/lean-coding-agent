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
DEFAULT_SKILLS_DIR = Path(".codex") / "skills"
MANIFEST_NAME = "global-skills-installed.json"
LEGACY_MANIFEST_NAME = "awesome-codex-skills-installed.json"
LEGACY_CONFIG_NAME = "awesome-codex-skills-subset.json"
AGENT_CONTEXT_DIRNAME = "agent-context"
LEGACY_AGENT_CONTEXT_DIRNAME = "anget-context"
LEGACY_CLONE_DIR = Path(LEGACY_AGENT_CONTEXT_DIRNAME) / "awesome-codex-skills"
AGENTS_MARKER_START = "<!-- shared-agents-reference:start -->"
AGENTS_MARKER_END = "<!-- shared-agents-reference:end -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a project repo so it uses this shared agents repo, creates "
            "agent-context, and installs this repo's global skills into the target "
            "repo's .codex/skills directory."
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


def shared_agents_block(target_repo: Path, shared_agents_path: Path) -> str:
    link_path = Path(os.path.relpath(shared_agents_path, target_repo)).as_posix()
    lines = [
        AGENTS_MARKER_START,
        "## Shared Baseline",
        "",
        f"Follow the shared baseline in [{link_path}]({link_path}).",
        "",
        "Keep project-specific rules below this block.",
        AGENTS_MARKER_END,
    ]
    return "\n".join(lines)


def ensure_agents_file(target_repo: Path, shared_repo_root: Path) -> Path:
    agents_path = target_repo / "AGENTS.md"
    shared_agents_path = shared_repo_root / "AGENTS.md"
    block = shared_agents_block(target_repo, shared_agents_path)

    if not agents_path.exists():
        content = "\n".join(
            [
                "# AGENTS.md",
                "",
                block,
                "",
                "## Project-Specific Rules",
                "",
                "- Add project-specific instructions here.",
                "",
            ]
        )
        agents_path.write_text(content, encoding="utf-8")
        return agents_path

    original = agents_path.read_text(encoding="utf-8")
    if AGENTS_MARKER_START in original and AGENTS_MARKER_END in original:
        start = original.index(AGENTS_MARKER_START)
        end = original.index(AGENTS_MARKER_END) + len(AGENTS_MARKER_END)
        updated = original[:start] + block + original[end:]
    elif block in original:
        updated = original
    else:
        updated = original.rstrip() + "\n\n" + block + "\n"

    if updated != original:
        agents_path.write_text(updated, encoding="utf-8")

    return agents_path


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
) -> Path:
    skills_root = target_repo / DEFAULT_SKILLS_DIR
    skills_root.mkdir(parents=True, exist_ok=True)

    previous_names = load_managed_skill_names([manifest_path, legacy_manifest_path])
    current_names = {entry["installed_as"] for entry in installs}

    for removed_name in sorted(previous_names - current_names):
        safe_rmtree(skills_root / removed_name, skills_root)

    for install in installs:
        source_dir = GLOBAL_SKILLS_ROOT / install["source"]
        dest_dir = skills_root / install["installed_as"]
        safe_rmtree(dest_dir, skills_root)
        shutil.copytree(
            source_dir,
            dest_dir,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )

    manifest = {
        "source_root": str(GLOBAL_SKILLS_ROOT),
        "skills": installs,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return skills_root


def main() -> int:
    args = parse_args()
    target_repo = Path(args.target_repo).expanduser().resolve()

    ensure_target_repo(target_repo)
    ensure_global_skills_root(GLOBAL_SKILLS_ROOT)

    agent_context_dir = target_repo / AGENT_CONTEXT_DIRNAME
    agent_context_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = agent_context_dir / MANIFEST_NAME
    legacy_manifest_path = target_repo / LEGACY_AGENT_CONTEXT_DIRNAME / LEGACY_MANIFEST_NAME

    agents_path = ensure_agents_file(target_repo, REPO_ROOT)
    installs = discover_global_skills(GLOBAL_SKILLS_ROOT)
    skills_root = sync_skills(target_repo, installs, manifest_path, legacy_manifest_path)
    cleanup_legacy_bootstrap(target_repo)

    print(f"Initialized project repo: {target_repo}")
    print(f"Updated AGENTS file: {agents_path}")
    print(f"Installed {len(installs)} global skills into: {skills_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
