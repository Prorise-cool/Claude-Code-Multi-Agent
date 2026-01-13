# Git Configuration Basics

## Table of Contents

- [Configuration File Locations](#configuration-file-locations)
  - [1. System Level](#1-system-level)
  - [2. Global/User Level](#2-globaluser-level)
  - [3. Local/Repository Level](#3-localrepository-level)
  - [Configuration Hierarchy](#configuration-hierarchy)
  - [View Configuration](#view-configuration)
- [Managing rerere (Reuse Recorded Resolution)](#managing-rerere-reuse-recorded-resolution)

---

## Configuration File Locations

Git uses a hierarchical configuration system with three levels.

### 1. System Level

**Location:**

- **Windows**: `<git-install-dir>/etc/gitconfig` (typically `C:/Program Files/Git/etc/gitconfig`)
- **macOS**: `/etc/gitconfig` or `/usr/local/etc/gitconfig`
- **Linux**: `/etc/gitconfig`

**Scope**: All users on the system
**Command**: `git config --system`
**Note**: Requires administrator/sudo privileges to modify

### 2. Global/User Level

**Location (Traditional):**

- **Windows**: `~/.gitconfig` (equivalent to `%USERPROFILE%\.gitconfig` in Windows)
- **macOS/Linux**: `~/.gitconfig`

**Location (XDG):**

- **All platforms**: `~/.config/git/config`

**Scope**: Current user, all repositories
**Command**: `git config --global`

Git will use `~/.config/git/config` if it exists, otherwise `~/.gitconfig`.

### 3. Local/Repository Level

**Location**: `.git/config` (inside repository)
**Scope**: Single repository only
**Command**: `git config --local` (or `git config` when inside a repo)

### Configuration Hierarchy

```text
~
├── .config/
│   └── git/
│       ├── config        # Global config (XDG location)
│       ├── ignore        # Global .gitignore patterns
│       └── template/     # Commit message templates
└── .gitconfig            # Global config (traditional location)
```

**Priority**: Local > Global > System (local overrides global overrides system)

### View Configuration

```bash
# View all configuration with source files
git config --list --show-origin

# View global (user) configuration only
git config --list --global

# View specific value
git config user.name
git config user.email
```

---

## Managing rerere (Reuse Recorded Resolution)

**How rerere works (safety info):**

- Records conflict state when you encounter merge conflicts
- Records resolution when you COMPLETE the merge/rebase
- **Aborted merges do NOT record** (git merge --abort, git rebase --abort)
- Only applies to IDENTICAL conflicts (same file, same chunk, same context)

**Enable rerere:**

```bash
git config --global rerere.enabled true
git config --global rerere.autoUpdate true
```

**Managing rerere:**

```bash
# View what rerere would apply
git rerere diff

# Clear all recorded resolutions
git rerere clear

# Forget resolution for specific file
git rerere forget path/to/file

# Disable for one operation
git -c rerere.enabled=false merge feature-branch
```

**When to use:**

- Long-lived feature branches with frequent rebases
- Multiple team members working on same files
- Repeated merge conflicts during complex rebases

**When NOT to use:**

- Short-lived feature branches (overhead not worth it)
- Solo projects with simple workflows
- When conflicts vary significantly each time
