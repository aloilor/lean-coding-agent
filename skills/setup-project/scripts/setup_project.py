#!/usr/bin/env python3
"""Set up or synchronize a project from a portable Lean Coding Agent package."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


PLUGIN_ID = "lean-coding-agent"
SCHEMA_VERSION = 1
MANIFEST_RELATIVE_PATH = Path("agent-context") / "skills-installed.json"
MANAGED_SKILLS_DIR = Path(".agents") / "skills"
DEFAULT_MODEL = "gpt-6-luna"
MODEL_ROLES = {
    "implementer": "implementer",
    "reviewer": "code-reviewer",
    "diagnostician": "bug-diagnostician",
}
AGENT_BROWSER_PACKAGE = "agent-browser@latest"
AGENT_BROWSER_COMMAND = "agent-browser"
DEV_DEPENDENCY_INSTALL_COMMANDS = {
    "npm": ["npm", "install", "--save-dev"],
    "pnpm": ["pnpm", "add", "--save-dev"],
    "yarn": ["yarn", "add", "--dev"],
    "bun": ["bun", "add", "--dev"],
}
AGENT_BROWSER_INSTALL_COMMANDS = {
    "npm": ["npm", "exec", "--", AGENT_BROWSER_COMMAND, "install"],
    "pnpm": ["pnpm", "exec", AGENT_BROWSER_COMMAND, "install"],
    "yarn": ["yarn", "run", AGENT_BROWSER_COMMAND, "install"],
    "bun": ["bun", "run", AGENT_BROWSER_COMMAND, "install"],
}
BASELINE_GUARD_MARKER = "## Do Not Edit This Baseline File"


class SetupError(Exception):
    """An expected setup refusal or validation error."""


def default_assets_root() -> Path:
    """Find assets bundled with this skill or its containing plugin."""
    script_path = Path(__file__).resolve()
    skill_assets = script_path.parents[1] / "assets"
    if (skill_assets / "baseline").is_dir():
        return skill_assets
    for parent in script_path.parents:
        assets = parent / "assets"
        if (parent / "plugin.json").is_file() and (assets / "baseline").is_dir():
            return assets
    return skill_assets


def skill_recommendation(skill_name: str) -> dict[str, str]:
    recommendations = {
        "engineering-standards": ("recommended", "Useful for most coding projects."),
        "codebase-onboarding": ("recommended", "Useful for new or unfamiliar projects."),
        "tdd": ("recommended", "Useful when the project has a test suite."),
        "grill-with-docs": (
            "recommended",
            "Useful for teams choosing the structured workflow process.",
        ),
    }
    if skill_name in recommendations:
        label, reason = recommendations[skill_name]
        return {"label": label, "reason": reason}
    if skill_name.startswith("workflow-"):
        return {
            "label": "recommended",
            "reason": "Useful for teams choosing the structured workflow process.",
        }
    contextual_reasons = {
        "rest-api-design": "Choose it when the project needs HTTP API design guidance.",
        "git-commit-and-push": "Choose it when the project wants guided Git publishing.",
        "git-conventional-commit": "Choose it when the project uses Conventional Commits.",
        "sql-code-review": "Choose it when the project needs SQL review guidance.",
        "sql-optimization": "Choose it when the project needs database query tuning.",
        "agent-browser": "Choose it when the project needs browser automation guidance.",
    }
    return {
        "label": "contextual option",
        "reason": contextual_reasons.get(
            skill_name, "Choose it when its specialized guidance fits the project."
        ),
    }


def skill_catalog(skills_root: Path) -> list[dict[str, Any]]:
    """Return installable skills with reasons and no implicit selections."""
    if not skills_root.is_dir():
        raise SetupError(f"Packaged skills directory does not exist: {skills_root}")
    return [
        {
            "name": skill_dir.name,
            "recommendation": skill_recommendation(skill_dir.name),
            "selected": False,
        }
        for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir())
        if (skill_dir / "SKILL.md").is_file()
    ]


def valid_skill_name(skill_name: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name))


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SetupError(f"Could not read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SetupError(f"Expected a JSON object in {path}.")
    return value


def current_models(target_repo: Path) -> dict[str, str]:
    models = {role: DEFAULT_MODEL for role in MODEL_ROLES}
    for role, agent_name in MODEL_ROLES.items():
        agent_path = target_repo / ".codex" / "agents" / f"{agent_name}.toml"
        if not agent_path.is_file():
            continue
        try:
            content = agent_path.read_text(encoding="utf-8")
        except OSError:
            continue
        match = re.search(r'''(?m)^model\s*=\s*("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*(?:#.*)?$''', content)
        if not match:
            continue
        encoded_model = match.group(1)
        try:
            model = json.loads(encoded_model) if encoded_model.startswith('"') else encoded_model[1:-1]
        except json.JSONDecodeError:
            continue
        if isinstance(model, str) and model.strip():
            models[role] = model.strip()
    return models


def legacy_baseline_signature(target_repo: Path) -> bool:
    for filename in ("AGENTS.md", "CLAUDE.md"):
        path = target_repo / filename
        if not path.is_file():
            return False
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            return False
        if BASELINE_GUARD_MARKER not in content:
            return False
        if "copied in from the upstream agents repo" not in content:
            return False
    return True


def parse_skill_names(value: Any, *, legacy: bool) -> list[str]:
    if not isinstance(value, list):
        raise SetupError("The saved skill selection is not a list.")
    names: list[str] = []
    for item in value:
        if isinstance(item, str):
            name = item
        elif legacy and isinstance(item, dict):
            source, installed_as = item.get("source"), item.get("installed_as")
            if not isinstance(source, str) or not isinstance(installed_as, str):
                raise SetupError("The legacy skill manifest has an invalid skill entry.")
            if source != installed_as:
                raise SetupError("The legacy skill manifest has a non-baseline skill mapping.")
            name = source
        else:
            raise SetupError("The saved skill selection has an invalid entry.")
        if not valid_skill_name(name) or name in names:
            raise SetupError("The saved skill selection has an invalid or duplicate name.")
        names.append(name)
    return names


def load_portable_manifest(manifest: dict[str, Any], path: Path) -> dict[str, Any]:
    if manifest.get("baseline") != PLUGIN_ID:
        raise SetupError(f"Refusing foreign setup manifest: {path}")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise SetupError(f"Unsupported {PLUGIN_ID} manifest schema in {path}.")
    skills = parse_skill_names(manifest.get("skills"), legacy=False)
    addons, models = manifest.get("addons", {}), manifest.get("models", {})
    if not isinstance(addons, dict) or not isinstance(models, dict):
        raise SetupError(f"The setup manifest has invalid add-on or model selections: {path}")
    normalized_addons = {}
    for name in ("community_skills", "browser_tooling"):
        enabled = addons.get(name, False)
        if not isinstance(enabled, bool):
            raise SetupError(f"The setup manifest has an invalid {name} selection: {path}")
        normalized_addons[name] = enabled
    normalized_models = {}
    for role in MODEL_ROLES:
        model = models.get(role, DEFAULT_MODEL)
        if not isinstance(model, str) or not model.strip():
            raise SetupError(f"The setup manifest has an invalid {role} model: {path}")
        normalized_models[role] = model.strip()
    return {
        "kind": "initialized",
        "skills": skills,
        "addons": normalized_addons,
        "models": normalized_models,
        "skip_external_installs": {"community_skills": False, "browser_tooling": False},
    }


def is_legacy_manifest(manifest: dict[str, Any]) -> bool:
    source_root, managed_dirs = manifest.get("source_root"), manifest.get("managed_skill_dirs")
    if not isinstance(source_root, str) or not isinstance(managed_dirs, list):
        return False
    source_name = source_root.replace("\\", "/").rstrip("/").split("/")[-1]
    absolute_source = Path(source_root).is_absolute() or PureWindowsPath(source_root).is_absolute()
    normalized_dirs = [
        item.replace("\\", "/").rstrip("/") if isinstance(item, str) else item
        for item in managed_dirs
    ]
    return (
        absolute_source
        and source_name == "skills"
        and normalized_dirs == [".agents/skills"]
    )


def load_legacy_manifest(
    manifest: dict[str, Any], target_repo: Path, path: Path
) -> dict[str, Any]:
    if not is_legacy_manifest(manifest) or not legacy_baseline_signature(target_repo):
        raise SetupError(f"Refusing ambiguous or foreign setup manifest: {path}")
    return {
        "kind": "legacy",
        "skills": parse_skill_names(manifest.get("skills"), legacy=True),
        # Older initializer versions always attempted both optional installations.
        "addons": {"community_skills": True, "browser_tooling": True},
        "models": current_models(target_repo),
        "skip_external_installs": {"community_skills": True, "browser_tooling": True},
    }


def load_project_state(target_repo: Path) -> dict[str, Any]:
    """Classify a target and validate any existing selection record."""
    manifest_path = target_repo / MANIFEST_RELATIVE_PATH
    if not manifest_path.exists():
        if legacy_baseline_signature(target_repo):
            raise SetupError(
                "Baseline files exist without a recognizable selection manifest; "
                "refusing ambiguous project state."
            )
        return {
            "kind": "new",
            "skills": [],
            "addons": {"community_skills": False, "browser_tooling": False},
            "models": {role: DEFAULT_MODEL for role in MODEL_ROLES},
            "skip_external_installs": {"community_skills": False, "browser_tooling": False},
        }
    manifest = read_json_object(manifest_path)
    if manifest.get("baseline") == PLUGIN_ID:
        return load_portable_manifest(manifest, manifest_path)
    return load_legacy_manifest(manifest, target_repo, manifest_path)


def detect_package_manager(target_repo: Path, package_json: dict[str, Any] | None = None) -> str:
    package_json_path = target_repo / "package.json"
    if package_json is None:
        package_json = read_json_object(package_json_path) if package_json_path.is_file() else {}
    declared = package_json.get("packageManager")
    if isinstance(declared, str):
        manager = declared.split("@", 1)[0]
        if manager in DEV_DEPENDENCY_INSTALL_COMMANDS:
            return manager
    for filename, manager in (
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lock", "bun"),
        ("bun.lockb", "bun"),
        ("package-lock.json", "npm"),
        ("npm-shrinkwrap.json", "npm"),
    ):
        if (target_repo / filename).exists():
            return manager
    return "npm"


def executable_name(command: str) -> str:
    return f"{command}.cmd" if os.name == "nt" else command


def browser_tooling_commands(manager: str) -> list[list[str]]:
    if manager not in DEV_DEPENDENCY_INSTALL_COMMANDS:
        raise SetupError(f"Unsupported package manager: {manager}")
    dependency = [*DEV_DEPENDENCY_INSTALL_COMMANDS[manager], AGENT_BROWSER_PACKAGE]
    browser = AGENT_BROWSER_INSTALL_COMMANDS[manager].copy()
    dependency[0], browser[0] = executable_name(dependency[0]), executable_name(browser[0])
    return [dependency, browser]


def upstream_skill_commands(asset_root: Path) -> list[list[str]]:
    metadata = read_json_object(asset_root / "upstream-skills.json")
    groups = metadata.get("groups")
    if not isinstance(groups, list):
        raise SetupError("Packaged upstream skill metadata has no groups list.")
    commands = []
    for group in groups:
        if not isinstance(group, dict):
            raise SetupError("Packaged upstream skill metadata contains an invalid group.")
        source, skills = group.get("source"), group.get("skills")
        if not isinstance(source, str) or not isinstance(skills, list) or not skills:
            raise SetupError("Packaged upstream skill metadata contains an invalid group.")
        if not all(isinstance(skill, str) and skill for skill in skills):
            raise SetupError("Packaged upstream skill metadata contains an invalid skill name.")
        commands.append(
            [
                executable_name("npx"),
                "skills",
                "add",
                source,
                "--skill",
                *skills,
                "--agent",
                "codex",
                "--copy",
                "-y",
            ]
        )
    return commands


def apply_models_to_toml(content: str, model: str) -> str:
    if not model.strip() or "\n" in model or "\r" in model:
        raise SetupError("Model IDs must be non-empty single-line values.")
    encoded = json.dumps(model, ensure_ascii=False)
    pattern = re.compile(r'(?m)^model\s*=\s*"(?:[^"\\]|\\.)*"\s*$')
    if pattern.search(content):
        return pattern.sub(f"model = {encoded}", content, count=1)
    return f"model = {encoded}\n" + content


def packaged_baseline_content(source_path: Path, filename: str) -> bytes:
    content = source_path.read_bytes()
    if BASELINE_GUARD_MARKER.encode("utf-8") not in content:
        raise SetupError(
            f"Packaged baseline file {filename} is missing the initializer guard."
        )
    return content


def local_file_content(filename: str) -> bytes:
    return "\n".join(
        [
            f"# {filename}",
            "",
            "Local private notes for this project.",
            "",
            "This file is ignored by git and is safe for machine-specific notes.",
            "",
        ]
    ).encode("utf-8")


def merge_override_index(existing: str | None, baseline_index: str) -> str:
    if existing is None:
        return baseline_index
    target_lines = [
        line for line in existing.splitlines() if line.strip() != "- _No skill overrides yet._"
    ]
    target_text = "\n".join(target_lines).rstrip() + "\n"
    missing = []
    for source_line in baseline_index.splitlines():
        if not source_line.startswith("- ["):
            continue
        skill_name = source_line[3:].split("](", 1)[0]
        if not any(line.startswith(f"- [{skill_name}](") for line in target_lines):
            missing.append(source_line)
    if not missing:
        return target_text
    if "## Baseline Overrides" not in target_text:
        target_text = target_text.rstrip() + "\n\n## Baseline Overrides\n\n"
    elif not target_text.endswith("\n"):
        target_text += "\n"
    return target_text + "\n".join(missing) + "\n"


def collect_asset_files(source_dir: Path) -> list[Path]:
    if not source_dir.is_dir():
        return []
    return sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )


def plan_file_changes(
    target_repo: Path,
    asset_root: Path,
    selected_skills: list[str],
    removed_skills: list[str],
    addons: dict[str, bool],
    models: dict[str, str],
) -> dict[Path, bytes | None]:
    """Build the complete managed-file plan without touching the target."""
    baseline_root = asset_root / "baseline"
    if not (baseline_root / "AGENTS.md").is_file() or not (baseline_root / "skills").is_dir():
        raise SetupError(f"The plugin asset bundle is incomplete: {asset_root}")
    changes: dict[Path, bytes | None] = {}
    for filename in ("AGENTS.md", "CLAUDE.md"):
        changes[Path(filename)] = packaged_baseline_content(
            baseline_root / filename, filename
        )

    # Context starter files are project-owned after creation, so copy only missing files.
    context_source = baseline_root / "agent-context"
    for source_path in collect_asset_files(context_source):
        if source_path.name == "skills-installed.json":
            continue
        relative = Path("agent-context") / source_path.relative_to(context_source)
        if not (target_repo / relative).exists():
            changes[relative] = source_path.read_bytes()

    for relative in (
        Path(".agents") / "lessons" / "LESSONS.md",
        Path("docs") / "incidents" / "README.md",
    ):
        source_path = baseline_root / relative
        if source_path.is_file() and not (target_repo / relative).exists():
            changes[relative] = source_path.read_bytes()

    local_names = ("AGENTS.local.md", "CLAUDE.local.md")
    for filename in local_names:
        relative = Path(filename)
        if not (target_repo / relative).exists():
            changes[relative] = local_file_content(filename)

    gitignore_path = target_repo / ".gitignore"
    current_gitignore = (
        gitignore_path.read_text(encoding="utf-8") if gitignore_path.is_file() else ""
    )
    ignore_lines = [
        *local_names,
        ".agents/code-reviews/",
        ".agents/plans/",
        ".agents/implementation-reports/",
        ".agents/tasks/",
        ".codex/tasks/",
    ]
    existing_lines = set(current_gitignore.splitlines())
    missing_lines = [line for line in ignore_lines if line not in existing_lines]
    if missing_lines:
        prefix = "" if not current_gitignore or current_gitignore.endswith("\n") else "\n"
        changes[Path(".gitignore")] = (
            current_gitignore + prefix + "\n".join(missing_lines) + "\n"
        ).encode("utf-8")

    # Baseline override files are managed; the index retains project-owned entries.
    override_source = baseline_root / "skills" / "skill-overrides"
    override_target = Path(".agents") / "skill-overrides"
    for source_path in collect_asset_files(override_source):
        if source_path.suffix == ".md" and source_path.name != "INDEX.md":
            changes[override_target / source_path.name] = source_path.read_bytes()
    source_index = override_source / "INDEX.md"
    if source_index.is_file():
        target_index = target_repo / override_target / "INDEX.md"
        existing_index = target_index.read_text(encoding="utf-8") if target_index.is_file() else None
        changes[override_target / "INDEX.md"] = merge_override_index(
            existing_index, source_index.read_text(encoding="utf-8")
        ).encode("utf-8")

    for role, agent_name in MODEL_ROLES.items():
        source_path = baseline_root / ".codex" / "agents" / f"{agent_name}.toml"
        if source_path.is_file():
            content = apply_models_to_toml(
                source_path.read_text(encoding="utf-8"), models[role]
            )
            relative = Path(".codex") / "agents" / source_path.name
            changes[relative] = content.encode("utf-8")

    skill_root = baseline_root / "skills"
    available = {item["name"] for item in skill_catalog(skill_root)}
    for skill_name in selected_skills:
        if skill_name not in available:
            # Retired skills stay in the manifest and on disk until explicitly removed.
            continue
        source_dir = skill_root / skill_name
        for source_path in collect_asset_files(source_dir):
            relative = MANAGED_SKILLS_DIR / skill_name / source_path.relative_to(source_dir)
            changes[relative] = source_path.read_bytes()

    for skill_name in removed_skills:
        skill_dir = target_repo / MANAGED_SKILLS_DIR / skill_name
        if skill_dir.is_dir():
            for existing_path in collect_asset_files(skill_dir):
                changes[existing_path.relative_to(target_repo)] = None

    manifest = {
        "baseline": PLUGIN_ID,
        "schema_version": SCHEMA_VERSION,
        "managed_skill_dirs": [MANAGED_SKILLS_DIR.as_posix()],
        "skills": [name for name in selected_skills if name not in removed_skills],
        "addons": addons,
        "models": models,
    }
    changes[MANIFEST_RELATIVE_PATH] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    return changes


def resolve_selections(
    state: dict[str, Any],
    available_skills: set[str],
    requested_skills: list[str] | None,
    removed_skills: list[str] | None,
    community_skills: bool | None,
    browser_tooling: bool | None,
    requested_models: dict[str, str | None],
) -> tuple[list[str], list[str], dict[str, bool], dict[str, str]]:
    requested = requested_skills or []
    invalid = [name for name in requested if name not in available_skills]
    if invalid:
        raise SetupError("Unknown skill selection: " + ", ".join(invalid))
    previous_skills = list(state["skills"])
    removed = removed_skills or []
    invalid_removals = [name for name in removed if name not in previous_skills]
    if invalid_removals:
        raise SetupError("Can remove only previously selected skills: " + ", ".join(invalid_removals))
    if set(requested) & set(removed):
        raise SetupError("A skill cannot be selected and removed in the same operation.")
    selected = list(dict.fromkeys([*previous_skills, *requested]))
    selected = [name for name in selected if name not in removed]
    addons = dict(state["addons"])
    if community_skills is not None:
        addons["community_skills"] = community_skills
    if browser_tooling is not None:
        addons["browser_tooling"] = browser_tooling
    models = dict(state["models"])
    for role, requested_model in requested_models.items():
        if requested_model is None:
            continue
        model = requested_model.strip()
        if not model or "\n" in model or "\r" in model:
            raise SetupError(f"The {role} model must be a non-empty single-line ID.")
        models[role] = model
    return selected, removed, addons, models


def ensure_target_repo(target_repo: Path) -> None:
    if not target_repo.is_dir():
        raise SetupError(f"Target project directory does not exist: {target_repo}")


def validate_target_paths(target_repo: Path, changes: dict[Path, bytes | None]) -> None:
    for relative_path in changes:
        safe_path = PurePosixPath(relative_path.as_posix())
        if safe_path.is_absolute() or ".." in safe_path.parts:
            raise SetupError(f"Refusing an unsafe managed path: {relative_path}")
        current = target_repo
        for index, part in enumerate(relative_path.parts):
            current = current / part
            if current.is_symlink():
                raise SetupError(f"Refusing to write through a symbolic link: {current}")
            if current.exists() and index < len(relative_path.parts) - 1 and not current.is_dir():
                raise SetupError(f"A managed path is blocked by a file: {current}")
        if current.exists() and current.is_dir() and changes[relative_path] is not None:
            raise SetupError(f"A managed file path is occupied by a directory: {current}")


def find_conflicts(
    target_repo: Path, changes: dict[Path, bytes | None]
) -> dict[Path, tuple[bytes | None, bytes | None]]:
    conflicts: dict[Path, tuple[bytes | None, bytes | None]] = {}
    for relative_path, proposed in changes.items():
        current_path = target_repo / relative_path
        if not current_path.is_file():
            continue
        current = current_path.read_bytes()
        if current != proposed:
            conflicts[relative_path] = (current, proposed)
    return conflicts


def approval_token(conflicts: dict[Path, tuple[bytes | None, bytes | None]]) -> str:
    payload = []
    for path, (current, proposed) in sorted(conflicts.items(), key=lambda item: item[0].as_posix()):
        payload.append(
            {
                "path": path.as_posix(),
                "current": current.hex() if current is not None else None,
                "proposed": proposed.hex() if proposed is not None else None,
            }
        )
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def git_status(target_repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=target_repo,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return "Git executable unavailable; file-level conflicts are still checked."
    if result.returncode != 0:
        return "Target is not a Git working tree."
    return result.stdout.rstrip() or "Working tree is clean."


def unified_change(relative_path: Path, current: bytes | None, proposed: bytes | None) -> str:
    before = current.decode("utf-8", errors="replace").splitlines(keepends=True) if current else []
    after = proposed.decode("utf-8", errors="replace").splitlines(keepends=True) if proposed else []
    return "".join(
        difflib.unified_diff(
            before,
            after,
            fromfile=f"a/{relative_path.as_posix()}",
            tofile=f"b/{relative_path.as_posix()}",
        )
    )


def render_preview(
    target_repo: Path,
    state: dict[str, Any],
    changes: dict[Path, bytes | None],
    conflicts: dict[Path, tuple[bytes | None, bytes | None]],
) -> str:
    output = [
        f"Target: {target_repo}",
        f"Project state: {state['kind']}",
        "Git status:",
        git_status(target_repo),
        f"Managed changes: {len(changes)} planned, {len(conflicts)} conflict(s).",
    ]
    if not conflicts:
        output.append("No existing managed file needs replacement approval.")
        return "\n".join(output)
    output.append("Existing managed-file changes:")
    for relative_path, (current, proposed) in sorted(
        conflicts.items(), key=lambda item: item[0].as_posix()
    ):
        output.append(f"\n--- {relative_path.as_posix()} ---")
        output.append(unified_change(relative_path, current, proposed) or "(binary content differs)")
    output.append(f"Approval token: {approval_token(conflicts)}")
    output.append("Ask the user to approve these exact replacements before applying them.")
    return "\n".join(output)


def make_plan(
    target_repo: Path,
    asset_root: Path,
    requested_skills: list[str] | None,
    removed_skills: list[str] | None,
    community_skills: bool | None,
    browser_tooling: bool | None,
    requested_models: dict[str, str | None],
) -> tuple[dict[str, Any], dict[Path, bytes | None], dict[Path, tuple[bytes | None, bytes | None]]]:
    ensure_target_repo(target_repo)
    state = load_project_state(target_repo)
    state["skip_external_installs"] = {
        addon: state["skip_external_installs"][addon] and requested is None
        for addon, requested in (
            ("community_skills", community_skills),
            ("browser_tooling", browser_tooling),
        )
    }
    available_skills = {
        item["name"] for item in skill_catalog(asset_root / "baseline" / "skills")
    }
    selected, removed, addons, models = resolve_selections(
        state,
        available_skills,
        requested_skills,
        removed_skills,
        community_skills,
        browser_tooling,
        requested_models,
    )
    changes = plan_file_changes(
        target_repo, asset_root, selected, removed, addons, models
    )
    validate_target_paths(target_repo, changes)
    conflicts = find_conflicts(target_repo, changes)
    return state, changes, conflicts


def apply_changes(
    target_repo: Path,
    changes: dict[Path, bytes | None],
    conflicts: dict[Path, tuple[bytes | None, bytes | None]],
    approved_token: str | None,
) -> None:
    if conflicts and approved_token != approval_token(conflicts):
        token = approval_token(conflicts)
        raise SetupError(
            "Conflicting managed files require explicit approval. Review the preview and "
            f"pass --approve-conflicts {token} only after approval."
        )
    validate_target_paths(target_repo, changes)
    for relative_path, proposed in changes.items():
        destination = target_repo / relative_path
        current = destination.read_bytes() if destination.is_file() else None
        if current == proposed:
            continue
        if proposed is None:
            if destination.is_file():
                destination.unlink()
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(proposed)
    for relative_path in changes:
        if relative_path.parts[: len(MANAGED_SKILLS_DIR.parts)] != MANAGED_SKILLS_DIR.parts:
            continue
        parent = (target_repo / relative_path).parent
        skill_root = target_repo / MANAGED_SKILLS_DIR
        while parent != skill_root and parent.is_relative_to(skill_root):
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def run_external_command(command: list[str], target_repo: Path) -> str | None:
    try:
        subprocess.run(command, cwd=target_repo, check=True)
    except FileNotFoundError as exc:
        return f"Command unavailable ({command[0]}): {exc}"
    except subprocess.CalledProcessError as exc:
        return f"Command failed with exit code {exc.returncode}: {' '.join(command)}"
    return None


def install_selected_addons(
    target_repo: Path,
    asset_root: Path,
    addons: dict[str, bool],
    skip_external_installs: dict[str, bool],
) -> list[str]:
    errors = []
    if addons["community_skills"] and not skip_external_installs["community_skills"]:
        for command in upstream_skill_commands(asset_root):
            error = run_external_command(command, target_repo)
            if error:
                errors.append(error)
    if addons["browser_tooling"] and not skip_external_installs["browser_tooling"]:
        package_json_path = target_repo / "package.json"
        package_json = read_json_object(package_json_path) if package_json_path.is_file() else {}
        manager = detect_package_manager(target_repo, package_json)
        for command in browser_tooling_commands(manager):
            error = run_external_command(command, target_repo)
            if error:
                errors.append(error)
                break
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safely set up or synchronize a project using a Lean Coding Agent package."
    )
    parser.add_argument("--asset-root", type=Path, default=default_assets_root())
    subparsers = parser.add_subparsers(dest="command", required=True)
    catalog_parser = subparsers.add_parser("catalog", help="List skills and recommendations.")
    catalog_parser.add_argument("--json", action="store_true", help="Print the catalog as JSON.")
    for command_name in ("preview", "apply"):
        command_parser = subparsers.add_parser(command_name)
        command_parser.add_argument("--target", required=True, type=Path)
        command_parser.add_argument("--skill", action="append", dest="skills")
        command_parser.add_argument("--remove-skill", action="append", dest="removed_skills")
        command_parser.add_argument(
            "--community-skills", dest="community_skills", action="store_true"
        )
        command_parser.add_argument(
            "--no-community-skills", dest="community_skills", action="store_false"
        )
        command_parser.add_argument(
            "--browser-tooling", dest="browser_tooling", action="store_true"
        )
        command_parser.add_argument(
            "--no-browser-tooling", dest="browser_tooling", action="store_false"
        )
        command_parser.set_defaults(community_skills=None, browser_tooling=None)
        for role in MODEL_ROLES:
            command_parser.add_argument(f"--{role}-model", dest=f"{role}_model")
    subparsers.choices["apply"].add_argument("--approve-conflicts", metavar="TOKEN")
    return parser


def configure_console_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="backslashreplace")


def main(argv: list[str] | None = None) -> int:
    configure_console_output()
    args = build_parser().parse_args(argv)
    try:
        asset_root = args.asset_root.expanduser().resolve()
        if args.command == "catalog":
            catalog = skill_catalog(asset_root / "baseline" / "skills")
            if args.json:
                print(json.dumps(catalog, indent=2, ensure_ascii=False))
            else:
                for skill in catalog:
                    recommendation = skill["recommendation"]
                    print(
                        f"{skill['name']} — {recommendation['label']}: "
                        f"{recommendation['reason']}"
                    )
            return 0

        requested_models = {role: getattr(args, f"{role}_model") for role in MODEL_ROLES}
        target_repo = args.target.expanduser().resolve()
        state, changes, conflicts = make_plan(
            target_repo,
            asset_root,
            args.skills,
            args.removed_skills,
            args.community_skills,
            args.browser_tooling,
            requested_models,
        )
        print(render_preview(target_repo, state, changes, conflicts))
        if args.command == "preview":
            return 0

        apply_changes(target_repo, changes, conflicts, args.approve_conflicts)
        print("Managed project files applied.")
        # Optional install errors leave the successfully applied project files in place.
        selected_addons = json.loads(
            changes[MANIFEST_RELATIVE_PATH].decode("utf-8")
        )["addons"]
        addon_errors = install_selected_addons(
            target_repo, asset_root, selected_addons, state["skip_external_installs"]
        )
        for error in addon_errors:
            print(f"Add-on installation error: {error}", file=sys.stderr)
        return 1 if addon_errors else 0
    except (OSError, SetupError) as exc:
        print(f"Setup failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
