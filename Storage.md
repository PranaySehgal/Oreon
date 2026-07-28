# Oreon Storage System

This document explains how Oreon stores repository data internally.

---

# Repository Directory

Every Oreon repository contains a hidden `.oreon` folder.

Example:
.oreon/

├── branches.json
├── changes.json
├── hashes.json
├── metadata.json

├── commits/

└── latest/


---

# Root Metadata Files

## metadata.json

Stores repository information.

Contains:

- Current branch.
- Repository version.

## Example: 

### {
####   "cur_branch":"main",
####   "version":"2.0.0"
### }


---

## branches.json

Stores branch information.

Responsible for:

- Tracking existing branches.
- Maintaining branch hierarchy.

---

## hashes.json

Stores file hashes used for change detection.

It allows Oreon to quickly identify file modifications.

---

## changes.json

Stores information about repository changes.

## Example: 

### "Relative File Source":"%HASH%"


---

# Latest Snapshot

The `latest` directory stores the current repository state.

Example:

latest/

abc.txt
def.txt
efg.txt


It represents the latest reconstructed version of the project.

---

# Commit Storage

Commits are stored inside:

.oreon/commits/


Each branch maintains its own commits.

Example:

commits/

main/
├──1/
└──2/

master/
├──1/
└──base/


---

# Commit Structure

A commit stores only changed files.

Example:
1/

changes/

├── changes.json
├── metadata.json
└── src/
└── def.txt


---

## changes/

Contains:

### metadata.json

Stores commit information.

Includes:

- Commit author.
- Commit date.
- Branch information.
- Commit message.
## Example:

### {
####  "Author": "USER",
####  "Message": "Message",
####  "Date_Created": "2026-07-25 01:14:09.847674",
####  "Random_Id": "0a0b246e-8798-11f1-af69-7066557f6ec6"
### }


---

### changes.json

Stores which files changed during the commit.

## Example:

### {
####  "updated": [],
####  "added": ["efg.txt"],
####  "deleted": []
### }


---

### Changed Files

Only files affected by the commit are stored.

Unchanged files are not duplicated.

---

# Branch Base Snapshot

When a branch is created, Oreon stores a base snapshot.

Example:

master/

base/

abc.txt
def.txt


The base snapshot represents the state of the project when the branch was created.

It allows:

- Faster restoration.
- Independent branch reconstruction.
- Easier merge operations.

---

# Commit Numbering

Each branch manages commit numbering independently.

Example:

main:

1
2
3

master:

1
2


A commit number is unique only inside its branch.

---

# Storage Philosophy

Oreon follows an incremental storage model.

Instead of storing the entire project every time:

- Only changed files are stored.
- Metadata describes each change.
- Base snapshots provide branch starting points.
- Latest snapshots represent current state.

This provides a balance between simplicity and storage efficiency.