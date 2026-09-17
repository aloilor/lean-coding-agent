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
    Path(".agents") / "skills",
]
MANIFEST_NAME = "skills-installed.json"
AGENT_CONTEXT_DIRNAME = "agent-context"
AGENT_CONTEXT_README_NAME = "README.md"
DOCS_DIRNAME = "docs"
INCIDENTS_DIRNAME = "incidents"
INCIDENTS_README_NAME = "README.md"
CODEX_AGENTS_DIR = Path(".codex") / "agents"
AGENTS_DIRNAME = ".agents"
LESSONS_DIRNAME = "lessons"
LESSONS_INDEX_NAME = "LESSONS.md"
SKILL_OVERRIDES_DIRNAME = "skill-overrides"
SKILL_OVERRIDES_INDEX_NAME = "INDEX.md"
BASELINE_FILENAMES = ["AGENTS.md", "CLAUDE.md"]
LOCAL_FILENAMES = ["AGENTS.local.md", "CLAUDE.local.md"]
SHARED_AGENT_IGNORE_LINES = [
    ".agents/code-reviews/",
    ".agents/plans/",
    ".agents/implementation-reports/",
    ".agents/tasks/",
    ".codex/tasks/",
]
AGENT_BROWSER_PACKAGE = "agent-browser@latest"
AGENT_BROWSER_COMMAND = "agent-browser"
UPSTREAM_SKILL_AGENTS = ["codex"]
UPSTREAM_SKILL_GROUPS = [
    {
        "source": "https://github.com/vercel-labs/skills",
        "skills": ["find-skills"],
    },
    {
        "source": "https://github.com/vercel-labs/agent-browser",
        "skills": ["agent-browser"],
    },
    {
        "source": "https://github.com/mattpocock/skills",
        "skills": [
            "handoff",
            "tdd",
        ],
    },
    {
        "source": "https://github.com/wshobson/agents",
        "skills": ["changelog-automation"],
    },
    {
        "source": "https://github.com/github/awesome-copilot",
        "skills": [
            "create-readme",
            "create-specification",
            "prd",
            "refactor",
            "sql-code-review",
            "sql-optimization",
        ],
    },
]
DEV_DEPENDENCY_INSTALL_COMMANDS = {
    "npm": ["npm", "install", "--save-dev"],
    "pnpm": ["pnpm", "add", "--save-dev"],
    "yarn": ["yarn", "add", "--dev"],
    "bun": ["bun", "add", "--dev"],
}
AGENT_BROWSER_BROWSER_INSTALL_COMMANDS = {
    "npm": ["npm", "exec", "--", AGENT_BROWSER_COMMAND, "install"],
    "pnpm": ["pnpm", "exec", AGENT_BROWSER_COMMAND, "install"],
    "yarn": ["yarn", "run", AGENT_BROWSER_COMMAND, "install"],
    "bun": ["bun", "run", AGENT_BROWSER_COMMAND, "install"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a project repo with this shared agent baseline, creates "
            "private local files, agent-context, shared lessons, and installs this repo's "
            "shared skills into the target repo's .agents/skills directory for Codex."
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


def baseline_guard_block(filename: str) -> str:
    local_filename = filename.replace(".md", ".local.md")
    return "\n".join(
        [
            "",
            "---",
            "",
            "## Do Not Edit This Baseline File",
            "",
            f"**Under no circumstances edit `{filename}` or the other baseline file in "
            "this project.** These files are the shared agents baseline, copied in from "
            "the upstream agents repo, and any edits here are overwritten on the next "
            "sync.",
            "",
            f"- For project-specific rules that should be shared and committed, use "
            "`agent-context/`.",
            f"- For local, private, machine-specific notes, use `{local_filename}` "
            "(git-ignored).",
            "",
            "Change the baseline itself only in the upstream agents repo, not here.",
            "",
        ]
    )


def copy_baseline_files(target_repo: Path, shared_repo_root: Path) -> list[Path]:
    copied_paths: list[Path] = []

    for filename in BASELINE_FILENAMES:
        source_path = shared_repo_root / filename
        if not source_path.exists():
            raise SystemExit(f"Shared baseline file does not exist: {source_path}")

        target_path = target_repo / filename
        shutil.copy2(source_path, target_path)

        baseline_text = source_path.read_text(encoding="utf-8")
        prefix = "" if baseline_text.endswith("\n") else "\n"
        with target_path.open("a", encoding="utf-8") as target_file:
            target_file.write(prefix + baseline_guard_block(filename))

        copied_paths.append(target_path)

    return copied_paths


def local_file_content(filename: str) -> str:
    return "\n".join(
        [
            f"# {filename}",
            "",
            "Local private notes for this project.",
            "",
            "This file is ignored by git and is safe for machine-specific notes.",
            "",
        ]
    )


def ensure_local_files(target_repo: Path) -> list[Path]:
    local_paths: list[Path] = []

    for filename in LOCAL_FILENAMES:
        local_path = target_repo / filename
        if not local_path.exists():
            local_path.write_text(local_file_content(filename), encoding="utf-8")
        local_paths.append(local_path)

    return local_paths


def ensure_local_gitignore(target_repo: Path) -> Path:
    gitignore_path = target_repo / ".gitignore"
    existing = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    existing_lines = set(existing.splitlines())
    managed_lines = [
        *LOCAL_FILENAMES,
        *SHARED_AGENT_IGNORE_LINES,
    ]
    missing_lines = [line for line in managed_lines if line not in existing_lines]

    if missing_lines:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        addition = "\n".join(missing_lines) + "\n"
        gitignore_path.write_text(existing + prefix + addition, encoding="utf-8")

    return gitignore_path


def install_tool_agents(target_repo: Path, shared_repo_root: Path) -> dict[str, list[Path]]:
    source_dir = shared_repo_root / CODEX_AGENTS_DIR
    installed_paths = {"Codex": []}

    if not source_dir.exists():
        return installed_paths

    codex_target_dir = target_repo / CODEX_AGENTS_DIR

    if source_dir.resolve() != codex_target_dir.resolve():
        for source_path in sorted(path for path in source_dir.rglob("*.toml") if path.is_file()):
            relative_path = source_path.relative_to(source_dir)
            target_path = codex_target_dir / relative_path

            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            installed_paths["Codex"].append(target_path)

    return installed_paths


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
        if manager_name in DEV_DEPENDENCY_INSTALL_COMMANDS:
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


def install_dev_dependency(target_repo: Path, package_name: str) -> str:
    package_json_path = target_repo / "package.json"
    package_json = load_package_json(package_json_path) if package_json_path.exists() else {}
    manager_name = detect_package_manager(target_repo, package_json)
    command = [*DEV_DEPENDENCY_INSTALL_COMMANDS[manager_name], package_name]
    command[0] = executable_name(command[0])

    try:
        subprocess.run(command, cwd=target_repo, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Could not install {package_name}: {manager_name} is not available on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"Could not install {package_name} with {manager_name} in {target_repo}."
        ) from exc

    return manager_name


def install_agent_browser(target_repo: Path) -> str:
    manager_name = install_dev_dependency(target_repo, AGENT_BROWSER_PACKAGE)
    command = AGENT_BROWSER_BROWSER_INSTALL_COMMANDS[manager_name].copy()
    command[0] = executable_name(command[0])

    try:
        subprocess.run(command, cwd=target_repo, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Could not run {AGENT_BROWSER_COMMAND} install: {manager_name} is not available on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"Could not run {AGENT_BROWSER_COMMAND} install with {manager_name} in {target_repo}."
        ) from exc

    return f"package installed and browser installed with {manager_name}"


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
                "Keep private or machine-specific notes in the root local files instead.",
                "",
            ]
        )
        readme_path.write_text(content, encoding="utf-8")

    return readme_path


def ensure_incidents_readme(target_repo: Path, shared_repo_root: Path) -> Path:
    incidents_dir = target_repo / DOCS_DIRNAME / INCIDENTS_DIRNAME
    incidents_dir.mkdir(parents=True, exist_ok=True)

    readme_path = incidents_dir / INCIDENTS_README_NAME
    if not readme_path.exists():
        source_path = shared_repo_root / DOCS_DIRNAME / INCIDENTS_DIRNAME / INCIDENTS_README_NAME
        content = source_path.read_text(encoding="utf-8")
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


def ensure_skill_overrides_index(target_repo: Path) -> Path:
    overrides_dir = target_repo / AGENTS_DIRNAME / SKILL_OVERRIDES_DIRNAME
    overrides_dir.mkdir(parents=True, exist_ok=True)

    index_path = overrides_dir / SKILL_OVERRIDES_INDEX_NAME
    if not index_path.exists():
        content = "\n".join(
            [
                "# Skill Overrides",
                "",
                "Project-specific overrides that adjust the default behavior of installed "
                "skills without editing the skills themselves. Installed and marketplace "
                "skills are overwritten when they update, so overrides live here instead. "
                "These files are shared (committed), unlike the private `*.local.md` files.",
                "",
                "Before running a skill, check this index. If the skill is listed below, read "
                "`.agents/skill-overrides/<skill-name>.md` and apply it — those overrides take "
                "precedence over that skill's default behavior.",
                "",
                "One file per overridden skill, named `<skill-name>.md` to match the skill's "
                "name. Add a matching clickable entry here whenever you add an override.",
                "",
                "- _No skill overrides yet._",
                "",
            ]
        )
        index_path.write_text(content, encoding="utf-8")

    return index_path


def index_entry_for_skill(index_text: str, skill_name: str) -> str | None:
    prefix = f"- [{skill_name}]("
    for line in index_text.splitlines():
        if line.startswith(prefix):
            return line
    return None


def upsert_baseline_override_index_entries(
    target_index_path: Path,
    source_index_path: Path,
    override_names: list[str],
) -> None:
    if not source_index_path.exists():
        target_index_path.parent.mkdir(parents=True, exist_ok=True)
        if not target_index_path.exists():
            target_index_path.write_text("# Skill Overrides\n\n", encoding="utf-8")
        return

    source_text = source_index_path.read_text(encoding="utf-8")
    if not target_index_path.exists():
        target_index_path.write_text(source_text, encoding="utf-8")
        return

    target_text = target_index_path.read_text(encoding="utf-8")
    target_lines = [
        line for line in target_text.splitlines() if line.strip() != "- _No skill overrides yet._"
    ]
    target_text = "\n".join(target_lines).rstrip() + "\n"

    missing_entries: list[str] = []
    for override_name in override_names:
        if index_entry_for_skill(target_text, override_name):
            continue
        source_entry = index_entry_for_skill(source_text, override_name)
        if source_entry:
            missing_entries.append(source_entry)

    if not missing_entries:
        target_index_path.write_text(target_text, encoding="utf-8")
        return

    if "## Baseline Overrides" not in target_text:
        target_text = target_text.rstrip() + "\n\n## Baseline Overrides\n\n"
    elif not target_text.endswith("\n"):
        target_text += "\n"

    target_text += "\n".join(missing_entries) + "\n"
    target_index_path.write_text(target_text, encoding="utf-8")


def sync_baseline_skill_overrides(target_repo: Path, shared_repo_root: Path) -> list[Path]:
    source_dir = shared_repo_root / "skills" / SKILL_OVERRIDES_DIRNAME
    target_dir = target_repo / AGENTS_DIRNAME / SKILL_OVERRIDES_DIRNAME
    target_dir.mkdir(parents=True, exist_ok=True)

    if not source_dir.exists():
        return [ensure_skill_overrides_index(target_repo)]

    copied_paths: list[Path] = []
    source_override_paths = sorted(
        path
        for path in source_dir.glob("*.md")
        if path.name != SKILL_OVERRIDES_INDEX_NAME
    )
    override_names = [path.stem for path in source_override_paths]

    for source_path in source_override_paths:
        target_path = target_dir / source_path.name
        shutil.copy2(source_path, target_path)
        copied_paths.append(target_path)

    target_index_path = target_dir / SKILL_OVERRIDES_INDEX_NAME
    upsert_baseline_override_index_entries(
        target_index_path,
        source_dir / SKILL_OVERRIDES_INDEX_NAME,
        override_names,
    )
    copied_paths.append(target_index_path)
    return copied_paths


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


def sync_skills(
    target_repo: Path,
    installs: list[dict],
    manifest_path: Path,
) -> list[Path]:
    skills_roots = [target_repo / relative_dir for relative_dir in MANAGED_SKILLS_DIRS]
    for skills_root in skills_roots:
        skills_root.mkdir(parents=True, exist_ok=True)

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
    installed_tool_agent_paths = install_tool_agents(target_repo, REPO_ROOT)
    agent_browser_install = install_agent_browser(target_repo)
    agent_context_readme_path = ensure_agent_context_readme(agent_context_dir)
    incidents_readme_path = ensure_incidents_readme(target_repo, REPO_ROOT)
    lessons_index_path = ensure_lessons_index(target_repo)
    skill_override_paths = sync_baseline_skill_overrides(target_repo, REPO_ROOT)
    skill_overrides_index_path = target_repo / AGENTS_DIRNAME / SKILL_OVERRIDES_DIRNAME / SKILL_OVERRIDES_INDEX_NAME
    manifest_path = agent_context_dir / MANIFEST_NAME
    baseline_paths = copy_baseline_files(target_repo, REPO_ROOT)
    local_paths = ensure_local_files(target_repo)
    gitignore_path = ensure_local_gitignore(target_repo)
    installs = discover_shared_skills(SHARED_SKILLS_ROOT)
    skills_roots = sync_skills(target_repo, installs, manifest_path)
    upstream_skills_install = install_upstream_skills(target_repo)

    print(f"Initialized project repo: {target_repo}")
    print("Copied baseline files:")
    for baseline_path in baseline_paths:
        print(f"- {baseline_path}")
    print("Ensured private local files:")
    for local_path in local_paths:
        print(f"- {local_path}")
    print(f"Ensured project context file: {agent_context_readme_path}")
    if copied_context_paths:
        print("Copied baseline project context files:")
        for context_path in copied_context_paths:
            print(f"- {context_path}")
    for tool_name, agent_paths in installed_tool_agent_paths.items():
        if not agent_paths:
            continue
        print(f"Installed {tool_name} agent files:")
        for agent_path in agent_paths:
            print(f"- {agent_path}")
    print(f"Agent Browser dependency: {agent_browser_install}")
    print(f"Ensured incident reports file: {incidents_readme_path}")
    print(f"Upstream skills: {upstream_skills_install}")
    print(f"Ensured shared lessons index: {lessons_index_path}")
    print(f"Ensured skill overrides index: {skill_overrides_index_path}")
    if skill_override_paths:
        print("Installed baseline skill override files:")
        for skill_override_path in skill_override_paths:
            print(f"- {skill_override_path}")
    print(f"Updated ignore rules: {gitignore_path}")
    print(f"Installed {len(installs)} shared skills into:")
    for skills_root in skills_roots:
        print(f"- {skills_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
