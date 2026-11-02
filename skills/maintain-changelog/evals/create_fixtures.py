"""Create disposable Git repositories for the prompts in evals.json.

Usage: python3 create_fixtures.py /absolute/path/to/empty-fixtures-directory
Each run should receive its own freshly generated fixtures.
"""

import json
import os
from pathlib import Path
import subprocess
import sys


def git(repo, *args, date=None):
    env = dict(os.environ)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], env=env, text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def write(repo, path, content):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def commit(repo, message, date):
    git(repo, "add", ".")
    git(repo, "commit", "-qm", message, date=date)


def base(root, name, changelog=True):
    repo = root / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Fixture Author")
    git(repo, "config", "user.email", "fixture@example.invalid")
    write(repo, "package.json", json.dumps({"name": "training", "version": "1.4.0"}) + "\n")
    write(repo, "docs/compatibility.md", "Public contract: documented API fields and supported dealer workflows. Compatible features require minor; incompatible API changes require major. Release dates use UTC.\n")
    write(repo, "app.json", json.dumps({"reports": False, "completed_visible": False, "reminders": False, "status_old": True}) + "\n")
    if changelog:
        write(repo, "CHANGELOG.md", "# Changelog\n\nBased on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n## [Unreleased]\n\n## [1.4.0] - 2026-11-01\n\n### Added\n- Dealers can view their training dashboard.\n")
    commit(repo, "First working copy", "2026-11-01T08:00:00+00:00")
    return repo


def change(repo, field, value, message, date):
    app = json.loads((repo / "app.json").read_text())
    app[field] = value
    write(repo, "app.json", json.dumps(app) + "\n")
    commit(repo, message, date)


def main():
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=False)
    repo = base(root, "unreleased")
    change(repo, "reports", True, "Dealer downloads are ready", "2026-11-01T18:00:00+00:00")
    write(repo, "docs/reports.md", "Dealers can download course completion reports from the training dashboard.\n")
    changelog = (repo / "CHANGELOG.md").read_text().replace("## [Unreleased]\n", "## [Unreleased]\n\n### Added\n- Dealers can download course completion reports.\n")
    write(repo, "CHANGELOG.md", changelog)
    commit(repo, "Write it down", "2026-11-02T08:00:00+00:00")
    change(repo, "completed_visible", True, "That annoying dashboard thing", "2026-11-02T09:00:00+00:00")
    change(repo, "reminders", True, "Trying reminders", "2026-11-02T10:00:00+00:00")
    change(repo, "reminders", False, "Back that out", "2026-11-02T11:00:00+00:00")
    write(repo, "tests/notes.txt", "Rename test fixtures only; no product behavior changes.\n")
    commit(repo, "Tidy fixtures", "2026-11-02T12:00:00+00:00")

    repo = base(root, "released")
    app = json.loads((repo / "app.json").read_text())
    del app["status_old"]
    app["status"] = "complete"
    write(repo, "app.json", json.dumps(app) + "\n")
    write(repo, "docs/migrate-status.md", "API clients must replace status_old with status. The old field has been removed.\n")
    commit(repo, "Use the new response shape", "2026-11-02T09:00:00+00:00")
    change(repo, "completed_visible", True, "Dashboard correction", "2026-11-02T10:00:00+00:00")

    repo = base(root, "bootstrap", changelog=False)
    write(repo, "package.json", '{"name":"training","version":"0.2.0"}\n')
    change(repo, "reports", True, "New report page", "2026-11-02T10:00:00+00:00")
    print(root)


if __name__ == "__main__":
    main()
