#!/usr/bin/env python3
"""
Purpose: Check a Git repository for basic health files.
Inputs:
  path   Repository path (default: current working directory)
Outputs: Report of missing README, LICENSE, .gitignore, or CI workflow.
Risks: None; this is a read-only check.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CI_CANDIDATES = [
    ".github/workflows",
    ".gitlab-ci.yml",
    ".circleci/config.yml",
    "azure-pipelines.yml",
    "Jenkinsfile",
    "bitbucket-pipelines.yml",
]

README_NAMES = ["README.md", "README"]


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def has_file(path: Path, names: list[str]) -> bool:
    for name in names:
        if (path / name).exists():
            return True
    return False


def has_ci_workflow(path: Path) -> bool:
    for candidate in CI_CANDIDATES:
        target = path / candidate
        if target.is_dir():
            if any(f.suffix in {".yml", ".yaml"} for f in target.iterdir()):
                return True
        elif target.is_file():
            return True
    return False


def check_repo(path: Path) -> list[str]:
    issues: list[str] = []
    if not is_git_repo(path):
        issues.append("Not a Git repository (missing .git directory)")
        return issues

    if not has_file(path, README_NAMES):
        issues.append("Missing README or README.md")

    if not has_file(path, ["LICENSE"]):
        issues.append("Missing LICENSE")

    if not has_file(path, [".gitignore"]):
        issues.append("Missing .gitignore")

    if not has_ci_workflow(path):
        issues.append("Missing CI workflow (checked .github/workflows, .gitlab-ci.yml, etc.)")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check repository health.")
    parser.add_argument("path", nargs="?", default=".", help="Path to repository")
    args = parser.parse_args()

    repo_path = Path(args.path).expanduser().resolve()
    if not repo_path.is_dir():
        print(f"ERROR: {repo_path} is not a directory", file=sys.stderr)
        return 1

    issues = check_repo(repo_path)

    print(f"Checking repository: {repo_path}")
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
