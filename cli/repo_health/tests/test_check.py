import tempfile
from pathlib import Path

from repo_health.check import check_repo


def make_repo(tmp_path: Path, **files: bool) -> Path:
    (tmp_path / ".git").mkdir()
    if files.get("readme", False):
        (tmp_path / "README.md").write_text("# Test")
    if files.get("license", False):
        (tmp_path / "LICENSE").write_text("MIT")
    if files.get("gitignore", False):
        (tmp_path / ".gitignore").write_text("*.pyc")
    if files.get("ci", False):
        workflows = tmp_path / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "ci.yml").write_text("on: push")
    return tmp_path


def test_missing_everything() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = make_repo(Path(tmp))
        issues = check_repo(path)
        assert len(issues) == 4


def test_complete_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = make_repo(Path(tmp), readme=True, license=True, gitignore=True, ci=True)
        issues = check_repo(path)
        assert issues == []
