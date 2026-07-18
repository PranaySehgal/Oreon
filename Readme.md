# Oreon

**A lightweight Version Control System (VCS) written in Python.**

Oreon is a command-line version control system inspired by Git. It allows you to track changes to your project, create commits, restore previous versions, and work with multiple branches—all through a simple and intuitive CLI.

> **Current Version:** 1.0.0

---

## Features

- Initialize repositories
- Track file additions, modifications, and deletions
- Create commits with custom messages
- Restore any previous commit
- View repository status
- Display commit history
- Create and switch between branches
- Prevent branch switching when uncommitted changes exist
- Repository information command
- SHA-256 based change detection
- Incremental storage for efficient versioning

---

## Installation

### From PyPI

```bash
pip install oreon
```

### Verify Installation

```bash
oreon --version
```

---

## Getting Started

### Initialize a Repository

```bash
oreon init
```

---

### Check Repository Status

```bash
oreon status
```

---

### Create a Commit

```bash
oreon commit -m "Initial project setup"
```

---

### View Commit History

```bash
oreon show
```

---

### Restore a Previous Commit

```bash
oreon restore
```

---

### View Repository Information

```bash
oreon info
```

---

## Branching

### Create a Branch

```bash
oreon createBranch feature
```

### Switch Branches

```bash
oreon changeBranch feature
```

If uncommitted changes are detected, Oreon prevents switching branches to avoid accidental data loss.

---

## Repository Structure

```text
project/
│
├── .oreon/
│   ├── commits/
│   ├── latest/
│   ├── hashes.json
│   └── ...
│
├── source files...
```

---

## Design

Unlike Git, Oreon uses an incremental storage approach.

The latest repository state is maintained inside `.oreon/latest`, while each commit stores only the changes introduced in that commit. During restoration, Oreon reconstructs the requested state by starting from the latest snapshot and reversing the required commits.

This approach keeps commits compact while allowing efficient restoration of previous versions.

---

## Notes

- Oreon tracks **files**, not empty directories.
- Empty folders are not versioned, similar to Git's behavior.
- Directories are recreated automatically whenever tracked files require them.

---

## Example Workflow

```bash
oreon init

oreon commit -m "Initial commit"

# edit files

oreon status

oreon commit -m "Implemented feature"

oreon show

oreon restore

oreon createBranch experimental

oreon changeBranch experimental
```

---

## Current Limitations

The following features are planned for future releases:

- File diff support
- Merge functionality
- Branch deletion
- Ignore file support (`.oreonignore`)
- Remote repositories
- Tags

---

## Why Oreon?

Oreon was built as a learning project to explore how version control systems work internally. Rather than wrapping Git, it implements its own repository format, commit storage, restoration logic, and branching mechanism from the ground up.

---

## Contributing

Contributions, suggestions, bug reports, and feature requests are welcome. Feel free to open an issue or submit a pull request.

---

## License

MIT License.

---

## Author

**Pranay Sehgal**

GitHub: https://github.com/PranaySehgal
