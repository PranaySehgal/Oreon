# Oreon Function Reference

This is how Oreon works in version 2.0.0.

Oreon is built around a CLI entry point and modular command files.

## Module responsibilities

### `cli.py`
- Entry point for parsing and dispatching commands.
- Defines subcommands such as `init`, `commit`, `restore`, `info`, `status`, `show`, `changeBranch`, `createBranch`, `branches`, `renameBranch`, `merge`, `delete`, and `editIgnore`.
- Validates repository existence before executing commands.

### `__init__.py`
- Initializes a new Oreon repository.
- Creates `.oreon` directories and files: `latest`, `commits`, `hashes.json`, `metadata.json`, `branches.json`, and `.oreonignore`.
- Hides the `.oreon` folder on Windows.

### `changeBranch.py`
- Switches the active branch by restoring the branch’s latest commit state.
- Updates `metadata.json` with the new `cur_branch`.
- Prevents branch switching when uncommitted changes exist.

### `checkHash.py`
- Scans repository files and computes SHA-256 hashes.
- Compares current file hashes with `.oreon/hashes.json`.
- Detects added, updated, and deleted files.
- Updates `hashes.json` and maintains the ignore list in `metadata.json`.

### `commit.py`
- Commits current changes for the active branch.
- Stores changed files under `.oreon/commits/<branch>/<commit_number>/changes/src/`.
- Writes `metadata.json` and `changes.json` for the commit.
- Rebuilds `.oreon/latest` as the current repository snapshot.

### `createBranch.py`
- Creates a new branch from the current branch.
- Requires a clean working tree before creating a branch.
- Adds branch metadata and initializes the branch directory.
- Saves a full base snapshot for the new branch.

### `deleteBranch.py`
- Deletes a branch only when it has no child branches.
- Removes the branch directory from `.oreon/commits`.
- Updates `branches.json`.
- Prevents deletion of the default branch if required.

### `info.py`
- Prints repository summary information.
- Reports branch list, current branch, total commit storage size, and working tree status.

### `merge.py`
- Merges one branch into another using reconstructed snapshots.
- Requires a clean working tree before merge.
- Applies non-conflicting changes automatically.
- Detects file conflicts and prompts the user to resolve them.
- Commits merged changes to the destination branch.

### `printBranches.py`
- Displays all existing branches.
- Highlights the active current branch.

### `renameBranch.py`
- Renames a branch in `branches.json`.
- Updates descendant branch hierarchy references.
- Renames the branch directory under `.oreon/commits`.
- Updates `metadata.json` to set the renamed branch as current.

### `restore.py`
- Reconstructs repository state for a branch at a selected commit.
- Uses the branch base snapshot and commit deltas.
- Supports preview mode to temporarily restore and then revert.
- Updates `.oreon/latest` and `.oreon/hashes.json` after restoration.

### `show.py`
- Displays commit details.
- Shows added, modified, and deleted files for the chosen commit.

### `showCommits.py`
- Lists commits for the current branch in a tabular format.
- Allows selecting commit UUIDs for viewing or restoration.
- Returns the commit index for restore actions.

### `status.py`
- Shows working tree status.
- Reports added, modified, and deleted files compared to `.oreon/hashes.json`.
- Indicates whether the working tree is clean or dirty.

### `ignore.py`
- Reveals `.oreonignore` for editing.
- Writes the ignore list from metadata into `.oreonignore`.
- Explains that `.oreonignore` is hidden again on the next commit.

