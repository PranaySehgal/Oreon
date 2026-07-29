# Oreon

Oreon is a lightweight command-line version control system for small repositories.
It tracks file changes, manages branches, restores past commits, and merges branch work using a hidden `.oreon` storage layout.

## Features

- 🔧 Initialize repositories with `init`
- 💾 Commit only changed files
- 🌿 Create and switch branches
- 🔄 Merge branches with conflict detection
- ⏪ Restore older commit states
- 📄 View commit history and details
- ⚙️ Edit ignore rules with `editIgnore`

## Getting Started

From the repository root, run:

```powershell
python cli.py <command>
```

Or as a module:

```powershell
python -m Oreon.cli <command>
```

## Common Commands

- `init` — initialize a new Oreon repository
- `commit [-m MESSAGE]` — save changes to the current branch
- `restore [--preview]` — restore a previous commit
- `info` — show repository summary
- `status` — show working tree changes
- `show` — display commit details
- `changeBranch <branch_name>` — switch active branch
- `createBranch <branch_name>` — create a new branch
- `branches` — list available branches
- `renameBranch <old> <new>` — rename a branch
- `merge <parent> <child>` — merge child into parent
- `delete <branchName>` — delete a branch
- `editIgnore` — edit the ignore list

## Example Workflow

1. Initialize a repository:

```powershell
python cli.py init
```

2. Make some file changes and commit them:

```powershell
python cli.py commit -m "Initial project setup"
```

3. Create a branch for a feature:

```powershell
python cli.py createBranch feature-1
```

4. Switch to the new branch:

```powershell
python cli.py changeBranch feature-1
```

5. Commit the feature work:

```powershell
python cli.py commit -m "Add feature 1"
```

6. Switch back to the main branch and merge:

```powershell
python cli.py changeBranch main
python cli.py merge main feature-1
```

## Storage Layout

Oreon stores repository history in `.oreon`:

- `branches.json` — branch definitions and ancestry
- `metadata.json` — current branch, version, and ignore rules
- `hashes.json` — tracked file hashes
- `commits/` — commit data per branch
- `latest/` — reconstructed latest snapshot

## Branch Model

- Each branch has its own independent commit history.
- New branches store a full base snapshot at creation.
- Commits store only changed files.

## Notes

- Oreon is designed for simple version tracking, not as a full git replacement.
- Merge conflicts require manual resolution.
- `.oreonignore` controls ignored files and is updated on commit.

## License

Use and modify Oreon freely for personal or learning projects.
