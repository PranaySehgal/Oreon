import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oreon.__init__ import __init__ as initialize_repo
from oreon.cli import main
from oreon.commit import commitData
from oreon.createBranch import createNewBranch
from oreon.merge import mergeBranches


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))
    return repo_dir


def test_merge_requires_clean_worktree(repo):
    (repo / "stable.txt").write_text("base", encoding="utf-8")
    commitData("base")
    createNewBranch("feature")

    (repo / "file.txt").write_text("dirty", encoding="utf-8")
    with patch("oreon.merge.console.print") as merge_print:
        mergeBranches("main", "feature")

    output = "\n".join(call.args[0] for call in merge_print.call_args_list if call.args)
    assert "Aborting" in output or "Un-committed" in output


def test_cli_accepts_commit_message_argument(monkeypatch, tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    initialize_repo(str(repo_dir))

    (repo_dir / "file.txt").write_text("hello", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["oreon", "commit", "-m", "hello-message"])
    main()

    branches = json.loads((repo_dir / ".oreon" / "branches.json").read_text(encoding="utf-8"))
    assert branches["main"]["last_commit"] == 1


def test_cli_rejects_uninitialized_repo(monkeypatch, tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    monkeypatch.chdir(repo_dir)
    monkeypatch.setattr("sys.argv", ["oreon", "status"])

    main()

    assert (repo_dir / ".oreon").exists() is False
