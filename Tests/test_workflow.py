import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oreon.__init__ import __init__ as initialize_repo
from oreon.changeBranch import changeExistingBranch
from oreon.checkHash import checkHash
from oreon.commit import commitData
from oreon.createBranch import createNewBranch
from oreon.info import oreanInfo
from oreon.restore import restoreCommit
from oreon.status import oreanStatus


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))
    return repo_dir


def test_initialize_repo_creates_expected_structure(repo):
    assert (repo / ".oreon").exists()
    assert (repo / ".oreon" / "branches.json").exists()
    assert (repo / ".oreon" / "metadata.json").exists()
    assert (repo / ".oreon" / "hashes.json").exists()

    metadata = json.loads((repo / ".oreon" / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["cur_branch"] == "main"
    assert metadata["ignore"] == []


def test_check_hash_detects_added_and_modified_files(repo):
    (repo / "notes.txt").write_text("first version", encoding="utf-8")

    updated, added, deleted, data = checkHash()
    assert added == ["notes.txt"]
    assert updated == []
    assert deleted == []
    assert data["notes.txt"]

    (repo / "notes.txt").write_text("second version", encoding="utf-8")
    updated, added, deleted, data = checkHash()
    assert updated == ["notes.txt"]
    assert added == []
    assert deleted == []


def test_commit_data_creates_commit_record(repo):
    (repo / "hello.txt").write_text("hello", encoding="utf-8")

    commitData("initial")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert branches["main"]["last_commit"] == 1
    assert branches["main"]["commits"] == [1]

    commit_meta = json.loads(
        (repo / ".oreon" / "commits" / "main" / "1" / "changes" / "metadata.json").read_text(encoding="utf-8")
    )
    assert commit_meta["Message"] == "initial"

    changes = json.loads(
        (repo / ".oreon" / "commits" / "main" / "1" / "changes" / "changes.json").read_text(encoding="utf-8")
    )
    assert "hello.txt" in changes["added"]


def test_create_and_switch_branch(repo):
    (repo / "hello.txt").write_text("hello", encoding="utf-8")
    commitData("initial")

    createNewBranch("feature")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert "feature" in branches
    assert branches["feature"]["commits"] == []

    changeExistingBranch("feature")

    metadata = json.loads((repo / ".oreon" / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["cur_branch"] == "feature"


def test_commit_without_changes_is_noop(repo):
    commitData("empty")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert branches["main"]["commits"] == []


def test_create_branch_rejects_existing_name(repo):
    (repo / "hello.txt").write_text("hello", encoding="utf-8")
    commitData("initial")

    createNewBranch("feature")
    createNewBranch("feature")

    branches = json.loads((repo / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert list(branches.keys()).count("feature") == 1


def test_check_hash_detects_deleted_files(repo):
    (repo / "ghost.txt").write_text("remove me", encoding="utf-8")
    commitData("add file")

    (repo / "ghost.txt").unlink()

    updated, added, deleted, data = checkHash()
    assert deleted == ["ghost.txt"]
    assert added == []
    assert updated == []
    assert data.get("ghost.txt") is None


def test_status_and_info_report_the_active_branch(repo):
    (repo / "hello.txt").write_text("hello", encoding="utf-8")
    commitData("initial")

    createNewBranch("feature")
    changeExistingBranch("feature")

    with patch("oreon.status.console.print") as status_print:
        oreanStatus()
    status_output = "\n".join(call.args[0] for call in status_print.call_args_list if call.args)
    assert "Branch     : feature" in status_output

    with patch("oreon.info.console.print") as info_print:
        oreanInfo()
    info_output = "\n".join(call.args[0] for call in info_print.call_args_list if call.args)
    assert "Current Branch    : feature" in info_output


def test_commit_ignores_files_listed_in_oreonignore(repo):
    (repo / "tracked.txt").write_text("tracked", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored", encoding="utf-8")
    (repo / ".oreonignore").write_text("ignored.txt\n", encoding="utf-8")

    commitData("ignore test")

    ignored_path = repo / ".oreon" / "commits" / "main" / "1" / "changes" / "src" / "ignored.txt"
    tracked_path = repo / ".oreon" / "commits" / "main" / "1" / "changes" / "src" / "tracked.txt"
    assert not ignored_path.exists()
    assert tracked_path.exists()


def test_change_branch_is_blocked_when_worktree_has_changes(repo, capsys):
    (repo / "hello.txt").write_text("hello", encoding="utf-8")
    createNewBranch("feature")

    changeExistingBranch("feature")

    captured = capsys.readouterr()
    assert "Un-Committed Changes" in captured.out

    metadata = json.loads((repo / ".oreon" / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["cur_branch"] == "main"


def test_restore_commit_rebuilds_previous_state(repo):
    (repo / "hello.txt").write_text("one", encoding="utf-8")
    commitData("first")

    (repo / "hello.txt").write_text("two", encoding="utf-8")
    commitData("second")

    restoreCommit(1)

    assert (repo / "hello.txt").read_text(encoding="utf-8") == "one"
