import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oreon.__init__ import __init__ as initialize_repo
from oreon.commit import commitData
from oreon.createBranch import createNewBranch
from oreon.info import oreanInfo
from oreon.ignore import ignore
from oreon.printBranches import printBranches
from oreon.renameBranch import renameBranch
from oreon.show import oreonShow


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))
    return repo_dir


def test_print_branches_shows_current_branch(repo):
    createNewBranch("feature")
    printBranches()

    assert (repo / ".oreon" / "branches.json").exists()


def test_info_command_runs_without_error(repo):
    (repo / "file.txt").write_text("value", encoding="utf-8")
    commitData("first")
    oreanInfo()


def test_ignore_writes_oreonignore(repo):
    (repo / ".oreonignore").write_text("ignored.txt", encoding="utf-8")
    ignore()

    assert (repo / ".oreonignore").exists()


def test_rename_branch_updates_metadata_and_folder(repo):
    createNewBranch("feature")
    renameBranch("feature", "feature2")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    metadata = json.loads((repo / ".oreon" / "metadata.json").read_text(encoding="utf-8"))

    assert "feature2" in branches
    assert "feature" not in branches
    assert metadata["cur_branch"] == "feature2"
    assert (repo / ".oreon" / "commits" / "feature2").exists()


def test_show_commit_output_works(repo):
    (repo / "file.txt").write_text("value", encoding="utf-8")
    commitData("first")
    oreonShow("main", 1)
