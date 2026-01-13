# Built-in Git GUI Tools

Git ships with two built-in GUI tools that are available on all platforms without additional installation.

## gitk - Repository Browser

**Purpose**: Visualize repository history

```bash
# View current branch history
gitk

# View all branches
gitk --all

# View specific file history
gitk path/to/file

# View commits by specific author
gitk --author="John Doe"
```

**Features:**

- ✅ Ships with Git (no installation needed)
- ✅ Fast, lightweight
- ✅ Good for quick history browsing
- ⚠️ Dated UI
- ⚠️ Read-only (visualization only)

---

## Git GUI - Commit Tool

**Purpose**: Stage changes and create commits

```bash
# Open Git GUI in current repository
git gui

# Open Git GUI for specific repository
git gui --repo /path/to/repo
```

**Features:**

- ✅ Ships with Git (no installation needed)
- ✅ Lightweight
- ✅ Good for staging/committing
- ⚠️ Dated UI
- ⚠️ Limited features (no branch management, merging, etc.)

---

**Last Updated:** 2025-11-28
