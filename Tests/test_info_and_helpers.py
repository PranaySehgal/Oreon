import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oreon.__init__ import __init__ as initialize_repo
from oreon.commit import commitData
from oreon.createBranch import createNewBranch
from oreon.ignore import ignore
from oreon.info import oreanInfo
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


def test_print_branches_marks_current_branch(repo):
    createNewBranch("feature")

    with patch("oreon.printBranches.console.print") as print_mock:
        printBranches()

    rendered = [call.args[1] if len(call.args) > 1 else call.args[0] for call in print_mock.call_args_list]
    assert "main" in rendered
    assert "feature" in rendered
    assert any(call.args[0] == "*  " for call in print_mock.call_args_list if call.args)


def test_info_command_reports_repository_summary(repo):
    (repo / "file.txt").write_text("value", encoding="utf-8")
    commitData("first")

    with patch("oreon.info.console.print") as info_print:
        oreanInfo()

    output = "\n".join(call.args[0] for call in info_print.call_args_list if call.args)
    assert "OREON REPOSITORY INFORMATION" in output
    assert "Current Branch    : main" in output


def test_ignore_writes_metadata_entries_to_oreonignore(repo):
    metadata = json.loads((repo / ".oreon" / "metadata.json").read_text(encoding="utf-8"))
    metadata["ignore"] = ["ignored.txt", "logs"]
    (repo / ".oreon" / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    ignore()

    assert (repo / ".oreonignore").read_text(encoding="utf-8") == "ignored.txtlogs"


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

    with patch("oreon.show.console.print") as show_print:
        oreonShow("main", 1)

    output = "\n".join(call.args[0] for call in show_print.call_args_list if call.args)
    assert "COMMIT 1" in output
    assert "first" in output
