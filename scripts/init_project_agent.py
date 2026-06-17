#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import stat
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
SHARED_SKILLS_ROOT = REPO_ROOT / "skills"
MANAGED_SKILLS_DIRS = [
    Path(".codex") / "skills",
    Path(".claude") / "skills",
]
MANIFEST_NAME = "skills-installed.json"
LEGACY_MANIFEST_NAMES = [
    "awesome-codex-skills-installed.json",
]
LEGACY_CONFIG_NAME = "awesome-codex-skills-subset.json"
AGENT_CONTEXT_DIRNAME = "agent-context"
AGENT_CONTEXT_README_NAME = "README.md"
PLAYWRIGHT_DIRNAME = ".playwright"
AGENTS_DIRNAME = ".agents"
LESSONS_DIRNAME = "lessons"
LESSONS_INDEX_NAME = "LESSONS.md"
LEGACY_AGENT_CONTEXT_DIRNAME = "anget-context"
LEGACY_CLONE_DIR = Path(LEGACY_AGENT_CONTEXT_DIRNAME) / "awesome-codex-skills"
BASELINE_FILENAMES = ["AGENTS.md", "CLAUDE.md"]
OVERRIDE_FILENAMES = ["AGENTS.override.md", "CLAUDE.override.md"]
PLAYWRIGHT_IGNORE_LINES = [
    ".playwright-cli/",
    ".playwright/output/",
    ".playwright/*.local.json",
]
PLAYWRIGHT_CLI_PACKAGE = "@playwright/cli@latest"
UPSTREAM_SKILL_AGENTS = ["codex", "claude-code"]
UPSTREAM_SKILL_GROUPS = [
    {
        "source": "https://github.com/vercel-labs/skills",
        "skills": ["find-skills"],
    },
    {
        "source": "https://github.com/mattpocock/skills",
        "skills": [
            "grill-me",
            "grill-with-docs",
            "tdd",
            "diagnose",
            "improve-codebase-architecture",
        ],
    },
    {
        "source": "https://github.com/wshobson/agents",
        "skills": ["changelog-automation"],
    },
]
PACKAGE_MANAGER_COMMANDS = {
    "npm": ["npm", "install", "--save-dev", PLAYWRIGHT_CLI_PACKAGE],
    "pnpm": ["pnpm", "add", "--save-dev", PLAYWRIGHT_CLI_PACKAGE],
    "yarn": ["yarn", "add", "--dev", PLAYWRIGHT_CLI_PACKAGE],
    "bun": ["bun", "add", "--dev", PLAYWRIGHT_CLI_PACKAGE],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a project repo with this shared agent baseline, creates "
            "private override files, agent-context, shared lessons, and installs this repo's "
            "shared skills into the target repo's .codex/skills and .claude/skills "
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


def ensure_shared_skills_root(shared_skills_root: Path) -> None:
    if not shared_skills_root.exists():
        raise SystemExit(f"Shared skills directory does not exist: {shared_skills_root}")
    if not shared_skills_root.is_dir():
        raise SystemExit(f"Shared skills path is not a directory: {shared_skills_root}")


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
    managed_lines = [*OVERRIDE_FILENAMES, *PLAYWRIGHT_IGNORE_LINES]
    missing_lines = [line for line in managed_lines if line not in existing_lines]

    if missing_lines:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        addition = "\n".join(missing_lines) + "\n"
        gitignore_path.write_text(existing + prefix + addition, encoding="utf-8")

    return gitignore_path


def copy_playwright_baseline(target_repo: Path, shared_repo_root: Path) -> list[Path]:
    source_dir = shared_repo_root / PLAYWRIGHT_DIRNAME
    target_dir = target_repo / PLAYWRIGHT_DIRNAME
    copied_paths: list[Path] = []

    if not source_dir.exists():
        return copied_paths

    if source_dir.resolve() == target_dir.resolve():
        return copied_paths

    for source_path in sorted(path for path in source_dir.rglob("*") if path.is_file()):
        relative_path = source_path.relative_to(source_dir)
        target_path = target_dir / relative_path
        if target_path.exists():
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        copied_paths.append(target_path)

    return copied_paths


def load_package_json(package_json_path: Path) -> dict:
    try:
        package_json = json.loads(package_json_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Target package.json is not valid JSON: {package_json_path}") from exc

    if not isinstance(package_json, dict):
        raise SystemExit(f"Target package.json must contain a JSON object: {package_json_path}")

    return package_json


def detect_package_manager(target_repo: Path, package_json: dict) -> str:
    package_manager = package_json.get("packageManager")
    if isinstance(package_manager, str):
        manager_name = package_manager.split("@", 1)[0]
        if manager_name in PACKAGE_MANAGER_COMMANDS:
            return manager_name

    lockfile_managers = [
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lock", "bun"),
        ("bun.lockb", "bun"),
        ("package-lock.json", "npm"),
        ("npm-shrinkwrap.json", "npm"),
    ]
    for lockfile_name, manager_name in lockfile_managers:
        if (target_repo / lockfile_name).exists():
            return manager_name

    return "npm"


def executable_name(command_name: str) -> str:
    return f"{command_name}.cmd" if os.name == "nt" else command_name


def install_playwright_cli(target_repo: Path) -> str:
    package_json_path = target_repo / "package.json"
    package_json = load_package_json(package_json_path) if package_json_path.exists() else {}
    manager_name = detect_package_manager(target_repo, package_json)
    command = PACKAGE_MANAGER_COMMANDS[manager_name].copy()
    command[0] = executable_name(command[0])

    try:
        subprocess.run(command, cwd=target_repo, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Could not install {PLAYWRIGHT_CLI_PACKAGE}: {manager_name} is not available on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"Could not install {PLAYWRIGHT_CLI_PACKAGE} with {manager_name} in {target_repo}."
        ) from exc

    return f"installed with {manager_name}"


def upstream_skills_install_command(source: str, skill_names: list[str]) -> list[str]:
    return [
        "npx",
        "skills",
        "add",
        source,
        "--skill",
        *skill_names,
        "--agent",
        *UPSTREAM_SKILL_AGENTS,
        "--copy",
        "-y",
    ]


def mirror_upstream_skill_to_codex(target_repo: Path, skill_name: str) -> None:
    universal_skill_dir = target_repo / AGENTS_DIRNAME / "skills" / skill_name
    codex_skills_root = target_repo / Path(".codex") / "skills"
    codex_skill_dir = codex_skills_root / skill_name

    if not universal_skill_dir.exists():
        raise SystemExit(f"Upstream skill install did not create expected path: {universal_skill_dir}")

    codex_skills_root.mkdir(parents=True, exist_ok=True)
    safe_rmtree(codex_skill_dir, codex_skills_root)
    shutil.copytree(universal_skill_dir, codex_skill_dir)


def install_upstream_skills(target_repo: Path) -> str:
    installed_skill_names: list[str] = []

    for group in UPSTREAM_SKILL_GROUPS:
        source = group["source"]
        skill_names = group["skills"]
        command = upstream_skills_install_command(source, skill_names)
        command[0] = executable_name(command[0])

        try:
            subprocess.run(command, cwd=target_repo, check=True)
        except FileNotFoundError as exc:
            raise SystemExit("Could not install upstream skills: npx is not available on PATH.") from exc
        except subprocess.CalledProcessError as exc:
            raise SystemExit(
                f"Could not install upstream skills from {source} with npx in {target_repo}."
            ) from exc

        installed_skill_names.extend(skill_names)

    for skill_name in installed_skill_names:
        mirror_upstream_skill_to_codex(target_repo, skill_name)

    return "installed from upstream with npx: " + ", ".join(installed_skill_names)


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


def copy_agent_context_baseline(target_repo: Path, shared_repo_root: Path) -> list[Path]:
    source_dir = shared_repo_root / AGENT_CONTEXT_DIRNAME
    target_dir = target_repo / AGENT_CONTEXT_DIRNAME
    copied_paths: list[Path] = []

    if not source_dir.exists():
        return copied_paths

    if source_dir.resolve() == target_dir.resolve():
        return copied_paths

    for source_path in sorted(path for path in source_dir.rglob("*") if path.is_file()):
        if source_path.name == MANIFEST_NAME:
            continue

        relative_path = source_path.relative_to(source_dir)
        target_path = target_dir / relative_path
        if target_path.exists():
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        copied_paths.append(target_path)

    return copied_paths


def ensure_lessons_index(target_repo: Path) -> Path:
    lessons_dir = target_repo / AGENTS_DIRNAME / LESSONS_DIRNAME
    lessons_dir.mkdir(parents=True, exist_ok=True)

    index_path = lessons_dir / LESSONS_INDEX_NAME
    if not index_path.exists():
        content = "\n".join(
            [
                "# Lessons",
                "",
                "Add shared agent lessons here.",
                "",
            ]
        )
        index_path.write_text(content, encoding="utf-8")

    return index_path


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {"skills": []}

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Managed skills manifest is not valid JSON: {manifest_path}") from exc


def discover_shared_skills(shared_skills_root: Path) -> list[dict]:
    installs: list[dict] = []

    for source_dir in sorted(path for path in shared_skills_root.iterdir() if path.is_dir()):
        if not (source_dir / "SKILL.md").exists():
            continue
        installs.append(
            {
                "source": source_dir.name,
                "installed_as": source_dir.name,
            }
        )

    if not installs:
        raise SystemExit(f"No installable skills found in: {shared_skills_root}")

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

    for legacy_name in [LEGACY_CONFIG_NAME, *LEGACY_MANIFEST_NAMES]:
        legacy_path = legacy_agent_context_dir / legacy_name
        if legacy_path.exists():
            legacy_path.unlink()

    if legacy_agent_context_dir.exists() and not any(legacy_agent_context_dir.iterdir()):
        legacy_agent_context_dir.rmdir()


def sync_skills(
    target_repo: Path,
    installs: list[dict],
    manifest_path: Path,
    legacy_manifest_paths: list[Path],
) -> list[Path]:
    skills_roots = [target_repo / relative_dir for relative_dir in MANAGED_SKILLS_DIRS]
    for skills_root in skills_roots:
        skills_root.mkdir(parents=True, exist_ok=True)

    previous_names = load_managed_skill_names([manifest_path, *legacy_manifest_paths])
    current_names = {entry["installed_as"] for entry in installs}

    for removed_name in sorted(previous_names - current_names):
        for skills_root in skills_roots:
            safe_rmtree(skills_root / removed_name, skills_root)

    for install in installs:
        source_dir = SHARED_SKILLS_ROOT / install["source"]
        for skills_root in skills_roots:
            dest_dir = skills_root / install["installed_as"]
            safe_rmtree(dest_dir, skills_root)
            shutil.copytree(
                source_dir,
                dest_dir,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )

    manifest = {
        "source_root": str(SHARED_SKILLS_ROOT),
        "managed_skill_dirs": [str(path) for path in MANAGED_SKILLS_DIRS],
        "skills": installs,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return skills_roots


def main() -> int:
    args = parse_args()
    target_repo = Path(args.target_repo).expanduser().resolve()

    ensure_target_repo(target_repo)
    ensure_shared_skills_root(SHARED_SKILLS_ROOT)

    agent_context_dir = target_repo / AGENT_CONTEXT_DIRNAME
    agent_context_dir.mkdir(parents=True, exist_ok=True)
    copied_context_paths = copy_agent_context_baseline(target_repo, REPO_ROOT)
    copied_playwright_paths = copy_playwright_baseline(target_repo, REPO_ROOT)
    playwright_cli_install = install_playwright_cli(target_repo)
    agent_context_readme_path = ensure_agent_context_readme(agent_context_dir)
    lessons_index_path = ensure_lessons_index(target_repo)
    manifest_path = agent_context_dir / MANIFEST_NAME
    legacy_manifest_paths = [
        agent_context_dir / legacy_name for legacy_name in LEGACY_MANIFEST_NAMES
    ]
    legacy_manifest_paths.extend(
        target_repo / LEGACY_AGENT_CONTEXT_DIRNAME / legacy_name
        for legacy_name in LEGACY_MANIFEST_NAMES
    )

    baseline_paths = copy_baseline_files(target_repo, REPO_ROOT)
    override_paths = ensure_override_files(target_repo)
    gitignore_path = ensure_override_gitignore(target_repo)
    installs = discover_shared_skills(SHARED_SKILLS_ROOT)
    skills_roots = sync_skills(target_repo, installs, manifest_path, legacy_manifest_paths)
    upstream_skills_install = install_upstream_skills(target_repo)
    cleanup_legacy_bootstrap(target_repo)

    print(f"Initialized project repo: {target_repo}")
    print("Copied baseline files:")
    for baseline_path in baseline_paths:
        print(f"- {baseline_path}")
    print("Ensured private override files:")
    for override_path in override_paths:
        print(f"- {override_path}")
    print(f"Ensured project context file: {agent_context_readme_path}")
    if copied_context_paths:
        print("Copied baseline project context files:")
        for context_path in copied_context_paths:
            print(f"- {context_path}")
    if copied_playwright_paths:
        print("Copied Playwright CLI baseline files:")
        for playwright_path in copied_playwright_paths:
            print(f"- {playwright_path}")
    print(f"Playwright CLI dependency: {playwright_cli_install}")
    print(f"Upstream skills: {upstream_skills_install}")
    print(f"Ensured shared lessons index: {lessons_index_path}")
    print(f"Updated ignore rules: {gitignore_path}")
    print(f"Installed {len(installs)} shared skills into:")
    for skills_root in skills_roots:
        print(f"- {skills_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
