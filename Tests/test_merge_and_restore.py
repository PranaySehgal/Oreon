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
from oreon.restore import restoreCommit


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))
    return repo_dir


def test_restore_commit_rehydrates_previous_state(repo):
    (repo / "file.txt").write_text("v1", encoding="utf-8")
    commitData("first")

    (repo / "file.txt").write_text("v2", encoding="utf-8")
    commitData("second")

    restoreCommit(1)

    assert (repo / "file.txt").read_text(encoding="utf-8") == "v1"


def test_restore_commit_preview_uses_temp_directory(repo, monkeypatch):
    (repo / "file.txt").write_text("v1", encoding="utf-8")
    commitData("first")

    monkeypatch.setattr("builtins.input", lambda *_args, **_kwargs: "0")
    restoreCommit(1, preview=True)

    assert (repo / "file.txt").read_text(encoding="utf-8") == "v1"
    assert (repo / ".oreon" / "main" / "Recovery").exists() is False
