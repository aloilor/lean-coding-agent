#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
SHARED_SKILLS_ROOT = REPO_ROOT / "skills"
SIBLINGS_ROOT = REPO_ROOT.parent
MANAGED_SKILLS_DIRS = [
    Path(".agents") / "skills",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync shared skills from this repo's skills folder into matching "
            ".agents/skills directories in this repo and sibling repos under ../."
        )
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Optional skill names to sync. Defaults to all installable shared skills.",
    )
    return parser.parse_args()


def discover_shared_skills(requested: list[str]) -> list[Path]:
    if requested:
        sources = [SHARED_SKILLS_ROOT / name for name in requested]
    else:
        sources = sorted(path for path in SHARED_SKILLS_ROOT.iterdir() if path.is_dir())

    installable: list[Path] = []
    missing: list[Path] = []
    for source in sources:
        if (source / "SKILL.md").exists():
            installable.append(source)
        else:
            missing.append(source)

    if missing:
        missing_names = ", ".join(path.name for path in missing)
        raise SystemExit(f"These shared skills are missing or not installable: {missing_names}")

    if not installable:
        raise SystemExit(f"No installable shared skills found in {SHARED_SKILLS_ROOT}")

    return installable


def iter_target_repos() -> list[Path]:
    repos = [REPO_ROOT]

    for sibling in sorted(path for path in SIBLINGS_ROOT.iterdir() if path.is_dir()):
        if sibling == REPO_ROOT:
            continue
        if not (sibling / ".git").exists():
            continue
        repos.append(sibling)

    return repos


def sync_skill(source_dir: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(
        source_dir,
        target_dir,
        ignore=shutil.ignore_patterns(".git", "__pycache__"),
    )


def main() -> int:
    args = parse_args()
    source_dirs = discover_shared_skills(args.skills)
    repos = iter_target_repos()

    updated: list[str] = []
    skipped: list[str] = []

    for repo in repos:
        for relative_dir in MANAGED_SKILLS_DIRS:
            skills_root = repo / relative_dir
            if not skills_root.exists():
                skipped.append(f"{repo}: missing {relative_dir.as_posix()}")
                continue

            for source_dir in source_dirs:
                target_dir = skills_root / source_dir.name
                if not target_dir.exists():
                    skipped.append(
                        f"{repo}: {relative_dir.as_posix()}/{source_dir.name} not maintained locally"
                    )
                    continue
                sync_skill(source_dir, target_dir)
                updated.append(f"{repo}: {relative_dir.as_posix()}/{source_dir.name}")

    if updated:
        print("Updated skill copies:")
        for entry in updated:
            print(f"- {entry}")
    else:
        print("No matching maintained skill copies were updated.")

    if skipped:
        print("Skipped:")
        for entry in skipped:
            print(f"- {entry}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
