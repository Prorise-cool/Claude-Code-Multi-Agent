# Git Global Configuration - Detailed Reference

Comprehensive configuration settings for Git global (`--global`) and repository-level (`--local`) configuration. This reference provides detailed explanations and advanced configuration options.

For essential quick-start configuration, see the main [config](../SKILL.md) skill.

## Table of Contents

- [Pull & Rebase Strategy](#pull--rebase-strategy)
- [Fetch Strategy](#fetch-strategy)
- [Push Strategy](#push-strategy)
- [Checkout/Switch Strategy](#checkoutswitch-strategy)
- [Commit Settings](#commit-settings)
- [Status Settings](#status-settings)
- [Diff Settings](#diff-settings)
- [Merge Settings](#merge-settings)
- [Managing rerere (Reuse Recorded Resolution)](#managing-rerere-reuse-recorded-resolution)
- [Color Settings](#color-settings)
- [Sorting](#sorting)
- [Log Settings](#log-settings)
- [Performance Settings](#performance-settings)
- [Submodule Strategy](#submodule-strategy)
- [Miscellaneous](#miscellaneous)
- [Repository-Level Configuration](#repository-level-configuration)
- [Maintenance](#maintenance)
  - [Enable Background Maintenance](#enable-background-maintenance)
  - [Recommended Setup](#recommended-setup)
- [Git Attributes](#git-attributes)
  - [Example `.gitattributes` File](#example-gitattributes-file)
  - [Normalizing Existing Repos](#normalizing-existing-repos)
- [Official Documentation](#official-documentation)

---

## Pull & Rebase Strategy

```bash
# Use rebase instead of merge when pulling (cleaner history)
git config --global pull.rebase true

# Make pulls safer/smoother with rebase
git config --global rebase.autoStash true      # Auto-stash uncommitted changes
git config --global rebase.updateRefs true     # Keep branch stack clean
git config --global rebase.missingCommitsCheck warn  # Catch potential issues
git config --global rebase.rescheduleFailedExec true # Reschedule --exec steps on conflict

# Preserve merge topology when rebasing (optional - advanced)
# Only if you want to preserve complex merge structure
#git config --global rebase.merges rebase-cousins
```

**What these do:**

- `pull.rebase true`: Uses rebase instead of merge when pulling, creating cleaner linear history
- `rebase.autoStash true`: Automatically stashes uncommitted changes before rebase, re-applies after
- `rebase.updateRefs true`: Updates branch references during rebase to maintain clean stack
- `rebase.missingCommitsCheck warn`: Warns if commits appear to be missing during interactive rebase
- `rebase.rescheduleFailedExec true`: If --exec command fails, reschedule it after resolving conflicts

---

## Fetch Strategy

```bash
# Automatically prune deleted remote branches when fetching
git config --global fetch.prune true

# Automatically prune deleted tags when fetching
git config --global fetch.pruneTags true

# Helps keep large histories snappy
git config --global fetch.writeCommitGraph true

# Show when a fetch forced updates (helpful signal)
git config --global fetch.showForcedUpdates true

# Faster negotiation on large remotes (improves fetch performance)
git config --global fetch.negotiationAlgorithm skipping

# Faster fetch on large repos (8 concurrent connections)
# Optimal for GitHub/GitLab/Bitbucket cloud
# Reduce to 4 for corporate/self-hosted servers if you see timeouts
git config --global fetch.parallel 8

# Keep modules in step when fetching/checking out (if using submodules)
git config --global fetch.recurseSubmodules on-demand
```

**What these do:**

- `fetch.prune true`: Automatically removes local references to remote branches that have been deleted
- `fetch.pruneTags true`: Automatically removes local tags that have been deleted on remote
- `fetch.writeCommitGraph true`: Maintains commit-graph file during fetch for better performance
- `fetch.showForcedUpdates true`: Shows when fetches involve force-updated branches (security signal)
- `fetch.negotiationAlgorithm skipping`: Uses faster negotiation algorithm for large repositories
- `fetch.parallel 8`: Fetches from 8 submodules/refs concurrently (adjust based on network/server)
- `fetch.recurseSubmodules on-demand`: Fetches submodule changes when parent repo references them

---

## Push Strategy

```bash
# Set default push behavior to current branch
# "simple" refuses to push if upstream name differs (safer)
# Alternative: "current" always pushes to same-named branch
git config --global push.default simple

# Auto-setup remote tracking on first push (eliminates "no upstream branch" errors)
git config --global push.autoSetupRemote true

# OPTIONAL: Automatically push annotated tags when pushing commits
# This is COMMENTED OUT because explicit tag pushing is safer
# If you prefer automatic tag pushing: git config --global push.followTags true
# Otherwise use aliases: git pusht (push with tags) or git pushtag (tags only)
```

**What these do:**

- `push.default simple`: Only push current branch to upstream if names match (prevents accidental pushes)
- `push.autoSetupRemote true`: Automatically sets up remote tracking on first push to avoid errors
- `push.followTags true` (commented): Would automatically push annotated tags with commits (use with caution)

---

## Checkout/Switch Strategy

```bash
# Set the default remote branch to origin
git config --global checkout.defaultRemote origin

# Parallelize checkout/switch/restore operations
git config --global checkout.workers 8

# Only parallelize when there are enough files to matter
git config --global checkout.thresholdForParallelism 100
```

**What these do:**

- `checkout.defaultRemote origin`: When switching to branch that exists on multiple remotes, prefer origin
- `checkout.workers 8`: Use 8 parallel workers for checkout operations (faster on large repos)
- `checkout.thresholdForParallelism 100`: Only parallelize when >100 files need updating

---

## Commit Settings

```bash
# Include a diff in commit messages you compose (great during reviews)
git config --global commit.verbose true
```

**What this does:**

- `commit.verbose true`: Shows diff below commit message template (helps write better messages)

---

## Status Settings

```bash
# Show ahead/behind counts in git status (how many commits ahead/behind remote)
# Provides useful visibility into sync status with remote branches
# Can disable in massive repos for performance: git config status.aheadBehind false
git config --global status.aheadBehind true

# Show branch and tracking information in git status
# Default in modern Git, but explicit doesn't hurt
git config --global status.branch true

# Show stash count in git status output
# Reminds you if you have stashed changes
git config --global status.showStash true

# Show all untracked files recursively
# Default is "normal" (shows untracked files/dirs), "all" shows every file
git config --global status.showUntrackedFiles all
```

**What these do:**

- `status.aheadBehind true`: Shows how many commits ahead/behind remote branch
- `status.branch true`: Shows current branch and tracking info
- `status.showStash true`: Shows stash count in status output
- `status.showUntrackedFiles all`: Shows all untracked files (not just directories)

---

## Diff Settings

```bash
# Better diff algorithm (more accurate, slower but worth it)
git config --global diff.algorithm histogram

# Better diffs for common files (great for detecting refactored code)
git config --global diff.colorMoved zebra

# Show more context in diffs
# Some prefer less context (3 lines) for cleaner diffs
git config --global diff.context 5

# Show context between change hunks (helps understand the bigger picture)
# Shows up to 10 lines of unchanged code between separate change hunks if they're close
git config --global diff.interHunkContext 10

# Nicer rename detection in diffs
# Alternative: "copies" also detects copied files (stricter)
git config --global diff.renames true

# Detects moved code even when indentation changes (complements colormoved=zebra)
git config --global diff.colorMovedWS allow-indentation-change

# Smarter diff UI
git config --global diff.mnemonicPrefix true
git config --global diff.wsErrorHighlight all
```

**What these do:**

- `diff.algorithm histogram`: More accurate diff algorithm (better change detection)
- `diff.colorMoved zebra`: Highlights moved code blocks with alternating colors
- `diff.context 5`: Shows 5 lines of context around changes (default is 3)
- `diff.interHunkContext 10`: Shows up to 10 lines between separate hunks if close together
- `diff.renames true`: Detects and shows file renames in diffs
- `diff.colorMovedWS allow-indentation-change`: Detects moves even when indentation changes
- `diff.mnemonicPrefix true`: Uses mnemonic prefixes (i/ for index, w/ for working tree, etc.)
- `diff.wsErrorHighlight all`: Highlights whitespace errors in all diff contexts

---

## Merge Settings

```bash
# Show original state in merge conflicts (zdiff3 is best)
# Shows the merge base, making conflicts much easier to resolve
git config --global merge.conflictstyle zdiff3

# This is an optional Git feature that remembers how you resolved merge conflicts
git config --global rerere.enabled true
git config --global rerere.autoUpdate true
```

**What these do:**

- `merge.conflictstyle zdiff3`: Shows 3-way diff with merge base (easier conflict resolution)
- `rerere.enabled true`: Enables "reuse recorded resolution" - remembers conflict resolutions
- `rerere.autoUpdate true`: Automatically stages files when rerere resolves conflicts

---

## Managing rerere (Reuse Recorded Resolution)

**How rerere works (safety info):**

- Records conflict state when you encounter merge conflicts
- Records resolution when you COMPLETE the merge/rebase
- **Aborted merges do NOT record** (git merge --abort, git rebase --abort)
- Only applies to IDENTICAL conflicts (same file, same chunk, same context)

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

- Working on long-lived feature branches with frequent rebases
- Repeatedly resolving same conflicts across multiple branches
- Team working on overlapping code sections

**When NOT to use:**

- Short-lived branches that merge quickly
- Conflicts that need case-by-case resolution
- When you're uncertain about conflict resolution patterns

---

## Color Settings

```bash
# Enable color output
git config --global color.ui auto
```

---

## Sorting

```bash
# Sort branch by newest first
git config --global branch.sort -committerdate

# Sort tags by newest first
git config --global tag.sort -taggerdate
```

**What these do:**

- `branch.sort -committerdate`: Shows most recently committed branches first in `git branch`
- `tag.sort -taggerdate`: Shows newest tags first in `git tag`

---

## Log Settings

```bash
# Abbreviate commit hashes in git log output
git config --global log.abbrevCommit true

# Default to off (can be noisy)
# Flip to true if you want GPG signatures shown inline
git config --global log.showSignature false

# Optional: Customize git log graph colors (personal preference)
# Default colors are fine for most users
#git config --global log.graphColors "blue,yellow,cyan,magenta,green,red"
```

**What these do:**

- `log.abbrevCommit true`: Shows short commit hashes instead of full SHA-1
- `log.showSignature false`: Doesn't show GPG signatures in log (less noise)
- `log.graphColors`: Customizes colors for `git log --graph` (optional)

---

## Performance Settings

```bash
# Modern Git for Windows/macOS/Linux supports built-in FSMonitor (Git ≥ 2.37)
# Monitors filesystem for changes, speeds up git status
git config --global core.fsmonitor true

# Adds performance boost for git status on large repos (works with fsmonitor)
git config --global core.untrackedCache true

# Helps keep large histories snappy
git config --global index.skipHash true
git config --global feature.manyFiles true

# Helps keep large histories snappy
git config --global gc.writeCommitGraph true
```

**What these do:**

- `core.fsmonitor true`: Uses filesystem monitor to speed up `git status` (requires Git 2.37+)
- `core.untrackedCache true`: Caches untracked files for faster `git status`
- `index.skipHash true`: Skips index file hash checks (faster writes)
- `feature.manyFiles true`: Optimizes for repositories with many files
- `gc.writeCommitGraph true`: Writes commit-graph during garbage collection (faster queries)

---

## Submodule Strategy

```bash
# Default to false (predictable behavior, opt-in per-repo)
git config --global submodule.recurse false

# Show submodule changes in status
git config --global status.submoduleSummary 1
```

**What these do:**

- `submodule.recurse false`: Doesn't automatically recurse into submodules (opt-in per operation)
- `status.submoduleSummary 1`: Shows summary of submodule changes in `git status`

---

## Miscellaneous

```bash
# Prompts you instead of auto-executing on typos (safer than the old autoCorrect=1)
git config --global help.autoCorrect prompt # Git 2.16+

# Optional: If you ever *don't* rebase, forbid merge commits on pull
# This is ignored (but harmless) when pull.rebase=true
git config --global pull.ff only # seatbelt if rebase gets toggled off

# Optional HTTP/2 (only if your host supports it)
# If you hit flaky corporate proxies, drop back to 1.1
git config --global http.version HTTP/2

# Unicode paths display nicely (recommended for all platforms)
git config --global core.quotepath false

# Usually default, but explicit doesn't hurt
git config --global protocol.version 2
```

**What these do:**

- `help.autoCorrect prompt`: Prompts before executing typo corrections
- `pull.ff only`: Only allows fast-forward merges when not rebasing
- `http.version HTTP/2`: Uses HTTP/2 protocol (faster, if supported)
- `core.quotepath false`: Displays Unicode characters in paths correctly
- `protocol.version 2`: Uses Git protocol version 2 (more efficient)

---

## Repository-Level Configuration

**These settings are context-specific** - use them in individual repos when needed, NOT as global defaults.

**When to use repo-level config:**

- Repo-specific requirements (submodules, performance, size)
- Overriding global settings for specific workflows
- Team-specific conventions for that repository

**Examples:**

```bash
# Enable submodule recursion in a specific repo
git config submodule.recurse true

# Disable ahead/behind in a massive repo (performance)
git config status.aheadBehind false

# Override line ending strategy (with .gitattributes)
git config core.autocrlf false
```

**How to use:**

```bash
# Navigate to repository
cd /path/to/repo

# Set local (repository-level) config
git config --local setting.name value

# View local config
git config --local --list

# Remove local setting
git config --local --unset setting.name
```

---

## Maintenance

Git can perform background maintenance to keep repositories fast.

### Enable Background Maintenance

```bash
# Enable background maintenance (commit-graph, repack)
git maintenance start

# Disable background maintenance (remove scheduled tasks)
git maintenance stop

# In each repo you want maintained
git maintenance register

# Opt a repo out (keep background jobs, but exclude the current repo)
git maintenance unregister

# Run the tasks appropriate for the 'hourly' tier right now
git maintenance run --schedule=hourly

# Or run a specific task once
git maintenance run --task=commit-graph
git maintenance run --task=incremental-repack
git maintenance run --task=loose-objects
git maintenance run --task=pack-refs

# See which repos are registered
git config --global --get-all maintenance.repo

# See which tasks are enabled (global / repo)
git config --global --list | grep maintenance.
git config --list | grep maintenance. # run inside a repo for its effective settings

# Let Git maintain all recently-used repos automatically
git config --global maintenance.auto true

# Enable/disable specific tasks globally
#git config --global maintenance.commit-graph.enabled true
#git config --global maintenance.incremental-repack.enabled true
#git config --global maintenance.loose-objects.enabled true
#git config --global maintenance.pack-refs.enabled true

# (Optional) disable full gc if you prefer only incremental maintenance
git config --global maintenance.gc.enabled false

# Helps keep large histories snappy
git config --global gc.writeCommitGraph true

# You can also scope by schedule (e.g., only run a task hourly/daily/weekly)
git config --global maintenance.commit-graph.schedule hourly
git config --global maintenance.incremental-repack.schedule weekly
```

### Recommended Setup

Run `git maintenance start` once for your account. In each active repo run `git maintenance register`, and keep these enabled globally:

```bash
git config --global maintenance.commit-graph.enabled true
git config --global maintenance.incremental-repack.enabled true
git config --global maintenance.loose-objects.enabled true
git config --global maintenance.pack-refs.enabled true
git config --global maintenance.gc.enabled false # optional, if you want to avoid full gc
```

**What background maintenance does:**

- **commit-graph**: Maintains commit-graph file for faster queries
- **incremental-repack**: Periodically repacks objects for better compression
- **loose-objects**: Cleans up loose objects that aren't packed
- **pack-refs**: Packs references (branches, tags) for faster access
- **gc**: Full garbage collection (usually disable in favor of incremental tasks)

**Maintenance schedules:**

- **hourly**: Runs every hour (commit-graph)
- **daily**: Runs once per day (loose-objects)
- **weekly**: Runs once per week (incremental-repack)

---

## Git Attributes

`.gitattributes` provides explicit control over line endings per file type. This is the recommended approach for cross-platform teams.

**Best practice:** control endings in `.gitattributes` and turn `autocrlf` off (or use platform-appropriate settings with `safecrlf=warn`).

**NOTE:** If you do this, you must have a `.gitattributes` file in each repo.

### Example `.gitattributes` File

```gitattributes
# Let Git detect text files and normalize line endings in the repo
* text=auto

# Scripts/config that should always be LF (shell and CI tools can be picky)
*.sh      text eol=lf
*.bash    text eol=lf
*.yml     text eol=lf
*.yaml    text eol=lf
*.json    text eol=lf
*.editorconfig text eol=lf
*.gitattributes text eol=lf
Dockerfile text eol=lf

# Windows-oriented files that are fine as CRLF in working tree
*.ps1     text eol=crlf
# Note: Git patterns are case-sensitive on Linux, case-insensitive on Windows
# Use lowercase extensions (Windows matches any case, Linux uses lowercase by convention)
*.cmd     text eol=crlf
*.bat     text eol=crlf
*.sln     text eol=crlf

# Calendar files - CRLF (Windows standard for .ics files)
*.ics     text eol=crlf

# .NET project files (XML) are text; line ending can be CRLF or LF
# If your team prefers CRLF in the editor:
*.csproj  text eol=crlf
*.props   text eol=crlf
*.targets text eol=crlf

# Treat images and other binaries correctly
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.pdf binary
*.zip binary
*.7z  binary
*.exe binary
*.dll binary

# ===========================
# Git Large File System (LFS)
# ===========================
#
# Git LFS stores binary files separately to prevent repository bloat.
# For repositories with large binaries (>1MB images, videos, datasets, large PDFs):
# Install Git LFS: https://git-lfs.github.com/
# Then replace "binary" with LFS pattern for large files.
#
# Git LFS pattern syntax:
# *.extension filter=lfs diff=lfs merge=lfs -text
#
# Example (if using LFS):
# *.png filter=lfs diff=lfs merge=lfs -text
# *.jpg filter=lfs diff=lfs merge=lfs -text
# *.pdf filter=lfs diff=lfs merge=lfs -text
# *.zip filter=lfs diff=lfs merge=lfs -text
# *.exe filter=lfs diff=lfs merge=lfs -text
#
# For detailed Git LFS guidance, see the line-endings skill
```

### Normalizing Existing Repos

If any repo already has mixed endings, normalize them:

```bash
git add --renormalize .
git commit -m "Normalize line endings"
```

---

## Official Documentation

- [Git Configuration Documentation](https://git-scm.com/docs/git-config)
- [Git Attributes Documentation](https://git-scm.com/docs/gitattributes)
- [Git Maintenance](https://git-scm.com/docs/git-maintenance)
- [Git Rerere](https://git-scm.com/docs/git-rerere)

**Last Verified:** 2025-11-17
