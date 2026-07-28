# Oreon Architecture

## Overview

Oreon is a lightweight command-line version control system designed to track changes, manage branches, restore previous states, and merge independent development paths.

Unlike traditional version control systems that primarily operate by storing commit objects and reconstructing history through patches, Oreon follows a snapshot-based approach combined with incremental storage.

Oreon stores only the files that have changed in each commit while maintaining branch snapshots to efficiently reconstruct repository states.

---

# System Design

Oreon is divided into multiple independent modules. The command-line interface acts as the central controller that connects user commands with internal functionality.

The general execution flow is:

User Command
|
v
cli.py
|
+----------------+
| |
v v
Commit System Branch System
|
v
Storage Layer


`cli.py` acts as the entry point of Oreon. It:

- Parses user commands.
- Validates provided arguments.
- Calls the appropriate internal modules.
- Provides a unified interface for repository operations.

---

# Repository Structure

Every Oreon repository contains a hidden `.oreon` directory.

Example:

.oreon/
│
├── branches.json
├── changes.json
├── hashes.json
├── metadata.json
│
├── commits/
│
└── latest/


The `.oreon` directory stores all information required to maintain version history.

---

# Metadata Management

Oreon maintains repository information using metadata files.

## metadata.json

Stores repository-level information.

Includes:

- Current branch
- Oreon version

## Example: 

### {
####   "cur_branch":"main",
####   "version":"2.0.0"
### }

---

## branches.json

Maintains branch information and hierarchy.

It stores:

- Existing branches
- Branch relationships
- Parent-child structure

This allows Oreon to understand branch dependencies and apply branch restrictions.

---

# Hash Based Change Detection

Oreon uses file hashing to detect changes between the current working directory and the previous repository state.

The process:

1. Calculate hashes of current files.
2. Compare them with stored hashes.
3. Identify:
   - Added files
   - Modified files
   - Deleted files

The detected differences are then used by commands like:

- `status`
- `commit`
- `merge`

---

# Commit System

A commit in Oreon does not duplicate the entire project.

Instead, it stores only the files affected by that commit.

Example:
Commit 1:
src/a.txt
src/b.txt

Commit 2:
src/c.txt


Commit 2 does not store unchanged files from Commit 1.

Each branch maintains its own commit numbering.

Example:
main

1
2
3

master

1
2


Commit numbers are independent between branches.

---

# Branch System

Oreon supports hierarchical branching.

A branch contains:

- Its own commit history.
- Its own numbering system.
- A reference to its parent branch.

When a branch is created:

1. A branch entry is added.
2. A branch directory is created.
3. The current project snapshot is copied as the branch base.

The base snapshot allows Oreon to reconstruct branch states without depending entirely on parent history.

---

# Merge System

Oreon performs merges by comparing reconstructed snapshots.

The merge process:

1. Generate the latest state of both branches.
2. Compare files between the two snapshots.
3. Detect conflicting modifications.
4. Apply non-conflicting changes automatically.
5. Ask the user to resolve conflicts when necessary.

Oreon compares final states instead of replaying individual commits.

---

# Restore System

The restore operation reconstructs the repository state of a selected commit.

The process:

1. Identify the requested commit.
2. Load the required snapshot information.
3. Apply stored changes.
4. Replace the current working directory state.

---

# Supported Commands

| Command | Purpose |
|---|---|
| init | Initialize an Oreon repository |
| commit | Create a new commit |
| restore | Restore a previous state |
| changeBranch | Switch active branch |
| createBranch | Create a new branch |
| renameBranch | Rename an existing branch |
| info | Display repository information |
| branches | Display available branches |
| status | Check repository changes |
| show | Display commit changes |
| merge | Merge branches |
| delete | Delete a branch |

---

# Design Philosophy

Oreon focuses on:

- Simple internal architecture.
- Human-readable storage.
- Incremental commit storage.
- Branch independence.
- Transparent repository management.

