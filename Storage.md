# Oreon Storage System

This document explains how Oreon stores repository data internally.

---

## Repository Directory

Every Oreon repository contains a hidden `.oreon` folder.

Example:

.oreon/
├── branches.json
├── hashes.json
├── metadata.json
├── commits/
└── latest/

The `.oreon` folder stores repository history, branch metadata, file hashes, and snapshots.

---

## Root Metadata Files

### `metadata.json`

Stores repository configuration.

Fields:
- `cur_branch`: active branch name
- `version`: Oreon version
- `ignore`: paths excluded from tracking

Example:

{
  "cur_branch": "main",
  "version": "2.0.0",
  "ignore": []
}

---

### `branches.json`

Describes all branches and their relationships.

Each branch entry includes:
- `Hierarchy`: ancestry chain for the branch
- `commits`: list of commit numbers on that branch
- `next_commit`: next commit number to use
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

---

### `hashes.json`

Stores SHA-256 hashes for tracked files.

This file is updated whenever Oreon checks the working tree or commits changes.

It is used to detect:
- added files
- modified files
- deleted files

---

## Latest Snapshot

### `.oreon/latest`

The `latest` directory contains a reconstructed snapshot of the current working tree.

This snapshot mirrors the repository state after the most recent commit.

---

## Commit Storage

Commits are stored under `.oreon/commits/<branch>/<commit_number>/changes`.

Each commit contains:
- `metadata.json`: author, message, date, random ID
- `changes.json`: lists of added, updated, and deleted files
- `src/`: actual contents of changed files

Example structure:

.oreon/commits/main/1/changes/
├── metadata.json
├── changes.json
└── src/
    ├── file1.txt
    └── folder/file2.txt

Only files that changed in the commit are stored in `src/`.

---

## Commit Metadata

### `changes/metadata.json`

Contains commit metadata fields:
- `Author`
- `Message`
- `Date_Created`
- `Random_Id`

Example:

{
  "Author": "user",
  "Message": "Initial commit",
  "Date_Created": "2026-07-25 01:14:09.847674",
  "Random_Id": "0a0b246e-8798-11f1-af69-7066557f6ec6"
}

### `changes/changes.json`

Describes commit changes:

{
  "updated": [],
  "added": ["file.txt"],
  "deleted": []
}

---

## Branch Base Snapshot

When a branch is created, Oreon saves a base snapshot under `.oreon/commits/<branch>/base/changes/src`.

The base snapshot contains the full repository state at branch creation time.

It is used to reconstruct branch state independently of parent commit history.

Example:

.oreon/commits/feature/base/changes/src/
├── file1.txt
└── file2.txt

---

## Ignore Behavior

Oreon also uses a `.oreonignore` file in the repository root.

- `editIgnore` reveals `.oreonignore` for editing.
- On the next commit, Oreon reads `.oreonignore` and saves the ignore list to `metadata.json`.
- Ignored files are excluded from tracking and hash comparisons.

---

## Commit Numbering

Each branch manages commit numbering independently.

Example:

main:
1
2
3

feature:
1
2

A commit number is unique only within its branch.

---

## Storage Philosophy

Oreon follows an incremental storage model.

Instead of storing the entire project every time:
- only changed files are stored
- metadata describes each change
- base snapshots provide branch start states
- latest snapshots represent current state

This balances simplicity with storage efficiency.
