import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oreon.__init__ import __init__ as initialize_repo
from oreon.cli import main
from oreon.createBranch import createNewBranch
from oreon.deleteBranch import deleteBranch


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))
    return repo_dir


def test_create_branch_creates_branch_metadata_and_base_snapshot(repo):
    createNewBranch("feature")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert "feature" in branches
    assert branches["feature"]["commits"] == []
    assert branches["feature"]["Hierarchy"].startswith("main+feature")
    assert (repo / ".oreon" / "commits" / "feature" / "base" / "changes" / "metadata.json").exists()


def test_delete_branch_rejects_branch_with_children(repo):
    createNewBranch("feature")
    createNewBranch("feature2")

    data = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    data["feature2"]["Hierarchy"] = "main+feature+feature2"
    (repo / ".oreon" / "branches.json").write_text(json.dumps(data), encoding="utf-8")

    deleteBranch("feature")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert "feature" in branches


def test_delete_branch_removes_leaf_branch(repo):
    createNewBranch("feature")
    deleteBranch("feature")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert "feature" not in branches
    assert "main" in branches


def test_cli_init_command_creates_repo(monkeypatch, tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)

    monkeypatch.setattr("sys.argv", ["oreon", "init"])
    main()

    assert (repo_dir / ".oreon").exists()
