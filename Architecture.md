# Oreon Architecture

## Overview

Oreon is a lightweight command-line version control system that tracks file changes, manages branches, restores previous states, and merges development paths.

It uses a hybrid snapshot/incremental model: only changed files are stored per commit, while branch creation also preserves a full base snapshot and the latest working-state snapshot.

---

## System Design

Oreon is organized into a CLI front end and several command modules.

- `cli.py` parses user input and routes commands to internal modules.
- Individual modules implement commit, branch management, merge, restore, status, and other operations.
- All repository data is stored under a hidden `.oreon` directory.

### Command flow

User command → `cli.py` → operation module → `.oreon` storage update

---

## Repository Structure

Every Oreon repository contains a hidden `.oreon` folder.

Example:

.oreon/
├── branches.json
├── hashes.json
├── metadata.json
├── commits/
└── latest/

The `.oreon` directory stores repository metadata, branch information, hash data, commit metadata, and a reconstructed latest snapshot.

---

## Key Metadata Files

### `metadata.json`

Stores repository-level configuration.

Fields include:
- `cur_branch`: current active branch
- `version`: Oreon version
- `ignore`: list of ignored paths

Example:

{
  "cur_branch": "main",
  "version": "2.0.0",
  "ignore": []
}

### `branches.json`

Stores branch definitions and relationships.

Each branch entry contains:
- `Hierarchy`: branch ancestry path
- `commits`: list of commit numbers for the branch
- `next_commit`: next commit number to assign
- `last_commit`: most recent commit number

Example:

{
  "main": {
    "Hierarchy": "",
    "commits": [],
    "next_commit": 1,
    "last_commit": null
  }
}

### `hashes.json`

Stores SHA-256 hashes for tracked files.

It is used to detect added, modified, and deleted files when running `status`, `commit`, or `merge`.

---

## Commit Model

Commits are stored under `.oreon/commits/<branch>/<commit_number>/changes`.

Each commit directory contains:
- `metadata.json`: commit author, message, date, random ID
- `changes.json`: lists of added, updated, and deleted files
- `src/`: actual file contents for changed files

Only files that changed in that commit are stored under `src/`.

Commit numbering is independent per branch.

Example:

main/
├── 1/
└── 2/

feature/
├── 1/
└── 2/

---

## Branch Model

A branch can be created from the current branch using `createBranch`.

When a new branch is created:
- A branch entry is added to `branches.json`
- A new branch directory is created under `.oreon/commits`
- A `base` snapshot is stored for that branch with all current files

The base snapshot preserves the repository state at branch creation time and enables branch reconstruction independent of parent commits.

---

## Merge Model

Merging compares reconstructed branch snapshots to apply changes.

The merge process:
1. Validate both branch names and ensure the working tree is clean
2. Restore the target branch state in a temporary area
3. Compare changed files between source and destination
4. Copy non-conflicting changes into the working tree
5. If a conflict occurs, create temporary conflict directories and prompt the user to choose a resolution
6. Commit the merged result to the target branch

Merges are based on final file state rather than replaying every commit.

---

## Restore Model

The restore operation rebuilds a branch state from its base snapshot and commit history.

`restoreCommit` can run in preview mode, temporarily restoring a commit and then optionally returning the repository to its original state.

---

## CLI Commands

Oreon supports these commands:

- `init`
- `commit [-m MESSAGE]`
- `restore [--preview]`
- `info`
- `status`
- `show`
- `changeBranch <branch_name>`
- `createBranch <branch_name>`
- `branches`
- `renameBranch <old> <new>`
- `merge <parent> <child>`
- `delete <branchName>`
- `editIgnore`

---

## Supported Commands

| Command | Purpose |
|---|---|
| `init` | Initialize an Oreon repository |
| `commit` | Create a new commit |
| `restore` | Restore a previous state |
| `changeBranch` | Switch active branch |
| `createBranch` | Create a new branch |
| `renameBranch` | Rename an existing branch |
| `info` | Display repository information |
| `branches` | Display available branches |
| `status` | Check repository changes |
| `show` | Display commit changes |
| `merge` | Merge branches |
| `delete` | Delete a branch |
| `editIgnore` | Reveal and edit ignore rules |

---

## Design Philosophy

Oreon focuses on:

- simple internal architecture
- human-readable storage
- incremental commit storage
- branch independence
- transparent repository management

