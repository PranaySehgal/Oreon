# 🚀 Oreon

### A lightweight version control system written entirely in Python.

_Track changes. Create commits. Restore history. Understand version control._

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-v1.0.0-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## ✨ Overview

**Oreon** is a lightweight command-line version control system built completely from scratch in Python.

It allows you to initialize repositories, create commits, detect project changes, and restore previous versions—all without relying on Git's internal implementation.

The project was created to explore the fundamentals of version control while keeping the implementation simple, readable, and educational.

---

## 🌟 Features

- 📦 Initialize repositories
- 💾 Create commits with optional commit messages
- 🔍 Detect added, modified, and deleted files
- ♻️ Restore any previous project state
- 📁 Preserve directory structure
- ⚡ Efficient incremental storage of changes
- 💻 Simple and intuitive command-line interface

---

## 📥 Installation

```bash
pip install oreon
```

---

## 🚀 Quick Start

### Initialize a repository

```bash
oreon init
```

### Create a commit

```bash
oreon commit
```

### Create a commit with a message

```bash
oreon commit -m "Initial project setup"
```

### Restore a previous commit

```bash
oreon restore
```

---

## 📖 Example Workflow

```bash
# Initialize the repository
oreon init

# First commit
oreon commit -m "Initial commit"

# Modify files...

# Save changes
oreon commit -m "Added authentication"

# Restore a previous version
oreon restore
```

---

## ⚙️ How Oreon Works

Oreon stores repository metadata inside a hidden **`.oreon`** directory.

Instead of copying the entire project for every commit, Oreon tracks changes between commits while maintaining the latest committed state separately. This enables efficient restoration without replicating Git's architecture.

The internal design is original to Oreon and was built from first principles as an educational implementation of a version control system.

---

## 🎯 Why Oreon?

Most developers use Git every day but rarely explore how a version control system actually works.

Oreon was built to bridge that gap by implementing core concepts such as:

- Repository initialization
- Commit history
- Change detection
- File restoration
- Snapshot management

—all in pure Python.

---

## 🛣️ Roadmap

- [ ] `.oreonignore` support
- [ ] Branching
- [ ] Merge support
- [ ] Commit diff viewer
- [ ] Compression
- [ ] Performance optimizations

---

## 📄 License

Released under the **MIT License**.

---

**⭐ If you find Oreon interesting, consider starring the repository!**
