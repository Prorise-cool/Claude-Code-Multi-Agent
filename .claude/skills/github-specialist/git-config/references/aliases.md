# Git Aliases and Clone Shortcuts - Complete Reference

Comprehensive reference for Git aliases and clone shortcuts. Aliases provide shortcuts for common Git operations.

For essential quick-start configuration, see the main [config](../SKILL.md) skill.

## Table of Contents

- [Git Aliases](#git-aliases)
  - [Information & Inspection](#information--inspection)
  - [Navigation & Utilities](#navigation--utilities)
  - [Branch Operations](#branch-operations)
  - [Staging & Unstaging](#staging--unstaging)
  - [Committing](#committing)
  - [History Editing (DANGER!)](#history-editing-danger)
  - [Remote Operations](#remote-operations)
- [Tag Pushing Workflow](#tag-pushing-workflow)
- [Clone Shortcuts](#clone-shortcuts)
  - [Universal GitHub Shorthand](#universal-github-shorthand)
  - [Organization/Personal Shortcuts](#organizationpersonal-shortcuts)
  - [Adding Your Own Shortcuts](#adding-your-own-shortcuts)
  - [Managing Clone Shortcuts](#managing-clone-shortcuts)
- [Alias Management](#alias-management)
- [Advanced Alias Patterns](#advanced-alias-patterns)
- [Recommended Alias Sets](#recommended-alias-sets)

---

## Git Aliases

Aliases provide shortcuts for common Git operations. Copy/paste these commands to set them up globally.

### Information & Inspection

```bash
git config --global alias.st "status -sb"
git config --global alias.sta "status -sb --ahead-behind"
git config --global alias.br "branch -vv"
git config --global alias.last "log -1 --stat"
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.lg1 "log --graph --decorate --date=relative --format='%C(auto)%h %d %s %C(green)(%cr) %C(bold blue)<%an>'"

# Alternative git log alias (gl) - similar to lg/lg1 but different formatting
# Uncomment if you prefer this style over lg/lg1
#git config --global alias.gl "log --all --graph --pretty=format:'%C(magenta)%h %C(white)%an %ar%C(auto) %D%n%s%n'"
```

**What these do:**

- `st`: Short status (`status -sb`) - compact status output
- `sta`: Short status with ahead/behind counts
- `br`: Branch list with verbose info (`branch -vv`)
- `last`: Show last commit with stats
- `lg`, `lg1`: Pretty graph log with colors and formatting
- `gl`: Alternative graph log format (commented out - uncomment if preferred)

**Usage examples:**

```bash
git st              # Shows compact status
git sta             # Shows status with ahead/behind
git br              # Lists branches with tracking info
git last            # Shows last commit details
git lg              # Shows pretty commit graph
git lg1             # Alternative pretty graph format
```

---

### Navigation & Utilities

```bash
git config --global alias.root "rev-parse --show-toplevel" # Find repo root from any subdirectory
```

**What this does:**

- `root`: Shows repository root directory (useful when deep in subdirectories)

**Usage example:**

```bash
cd src/components/deeply/nested/path
git root
# Output: /path/to/repo
```

---

### Branch Operations

```bash
git config --global alias.co "switch"
git config --global alias.cob "switch -c" # Create and switch (idempotent)
```

**What these do:**

- `co`: Switch to existing branch (`switch`)
- `cob`: Create and switch to new branch (`switch -c`)

**Usage examples:**

```bash
git co main                # Switch to main branch
git cob feature/new-thing  # Create and switch to new branch
```

**Note:** These use modern `git switch` instead of legacy `git checkout` for clarity.

---

### Staging & Unstaging

```bash
git config --global alias.rs "restore"
git config --global alias.unstage "restore --staged --"
```

**What these do:**

- `rs`: Restore file to working tree state (`restore`)
- `unstage`: Remove file from staging area (`restore --staged`)

**Usage examples:**

```bash
git unstage file.txt       # Remove file.txt from staging
git rs file.txt            # Restore file.txt to last committed version
```

---

### Committing

```bash
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.fixup 'commit --fixup'
git config --global alias.squash 'commit --squash'
```

**What these do:**

- `amend`: Add changes to last commit without editing message
- `fixup`: Create fixup commit (for later squashing with interactive rebase)
- `squash`: Create squash commit (combines with previous commit in interactive rebase)

**Usage examples:**

```bash
git amend                       # Add staged changes to last commit
git fixup abc123                # Create fixup commit for abc123
git squash abc123               # Create squash commit for abc123
git rebase -i --autosquash main # Apply fixups/squashes automatically
```

---

### History Editing (DANGER!)

**WARNING**: These rewrite history - ONLY use on unpushed local commits!
Using these on pushed commits will cause problems for collaborators.

```bash
git config --global alias.uncommit "reset --soft HEAD~1"  # Undo last commit, keep changes staged
git config --global alias.recommit "commit --amend --no-edit"  # Add changes to last commit (same as 'amend')
git config --global alias.editcommit "commit --amend"  # Amend last commit and edit message
```

**What these do:**

- `uncommit`: Undo last commit but keep changes staged (safe undo)
- `recommit`: Add staged changes to last commit (alias for `amend`)
- `editcommit`: Amend last commit and edit the commit message

**Usage examples:**

```bash
git uncommit        # Undo last commit, changes stay staged
git recommit        # Add more changes to last commit
git editcommit      # Amend last commit and change message
```

**Safety guidelines:**

- ✅ **Safe**: Using on local commits not yet pushed
- ❌ **Dangerous**: Using on commits already pushed to shared branches
- ⚠️ **Use with caution**: If you must rewrite pushed commits, use `git push --force-with-lease`

---

### Remote Operations

```bash
git config --global alias.f "fetch --prune --prune-tags --tags"
git config --global alias.pfwl "push --force-with-lease"

# Explicit tag pushing (safe alternative to push.followTags=true)
git config --global alias.pusht 'push --follow-tags'
git config --global alias.pushtag '!git push origin --tags'
```

**What these do:**

- `f`: Fetch with pruning (removes deleted remote branches/tags)
- `pfwl`: Push with force-with-lease (safer force push)
- `pusht`: Push commits AND annotated tags that point to them
- `pushtag`: Push all tags to origin

**Usage examples:**

```bash
git f                           # Fetch and prune deleted branches/tags
git pfwl                        # Force push safely (only if no one else pushed)
git pusht                       # Push commits with their annotated tags
git pushtag                     # Push all tags
git push origin v1.0.0          # Push specific tag
```

---

## Tag Pushing Workflow

**Default behavior (without `push.followTags=true`):**

- `git push` - Normal push (no tags)
- `git pusht` - Push commits + annotated tags that point to them
- `git pushtag` - Push all tags explicitly
- `git push origin v1.0.0` - Push specific tag

**Why explicit tag pushing is safer:**

- Prevents accidental tag pushes
- Allows selective tag publishing
- Clearer intent when pushing tags
- No surprises with automated tag pushing

**Recommended workflow:**

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push commits (tags NOT included by default)
git push

# Explicitly push tags when ready
git pusht                    # Push commits + their tags
# OR
git pushtag                  # Push all tags
# OR
git push origin v1.0.0       # Push specific tag
```

---

## Clone Shortcuts

Git's `url.insteadOf` feature creates shorthand prefixes for clone URLs, saving typing and reducing errors.

### Universal GitHub Shorthand

```bash
# Universal GitHub shorthand (useful for everyone)
git config --global url."git@github.com:".insteadOf "gh:"
# Usage: git clone gh:username/repo
```

**What this does:**

Expands `gh:username/repo` to `git@github.com:username/repo` automatically.

**Usage example:**

```bash
# Instead of: git clone git@github.com:microsoft/vscode.git
git clone gh:microsoft/vscode
```

---

### Organization/Personal Shortcuts

**Note:** These are example shortcuts - customize for your own organizations and accounts.

```bash
# Melodic Software organization shorthand (example)
git config --global url."git@github.com:melodic-software/".insteadOf "melodic:"
# Usage: git clone melodic:onboarding

# Personal account shorthand example (kyle-sexton)
git config --global url."git@github.com:kyle-sexton/".insteadOf "ks:"
# Usage: git clone ks:rpg-maker
```

**Usage examples:**

```bash
# Instead of: git clone git@github.com:melodic-software/onboarding.git
git clone melodic:onboarding

# Instead of: git clone git@github.com:kyle-sexton/rpg-maker.git
git clone ks:rpg-maker

# Instead of: git clone git@github.com:microsoft/vscode.git
git clone gh:microsoft/vscode
```

---

### Adding Your Own Shortcuts

**Template for corporate Git servers (self-hosted GitLab, GitHub Enterprise, etc.):**

```bash
# Example for self-hosted GitLab
git config --global url."ssh://git@git.company.com:2202/team/".insteadOf "work:"
# Usage: git clone work:project-name
```

**Template for other personal namespaces:**

```bash
# Example for personal GitHub namespace
git config --global url."git@github.com:YourUsername/".insteadOf "me:"
# Usage: git clone me:my-repo
```

**Usage examples:**

```bash
# Corporate repository
git clone work:api-gateway

# Personal repository
git clone me:dotfiles
```

---

### Managing Clone Shortcuts

**View configured shortcuts:**

```bash
# List all url.insteadOf settings
git config --global --get-regexp url

# Output example:
# url.git@github.com:.insteadof gh:
# url.git@github.com:melodic-software/.insteadof melodic:
# url.git@github.com:kyle-sexton/.insteadof ks:
```

**Remove a shortcut:**

```bash
# Remove specific shortcut
git config --global --unset url."git@github.com:melodic-software/".insteadOf
```

**Edit all shortcuts:**

```bash
# Open global config in editor
git config --global --edit
```

---

## Alias Management

### View All Aliases

```bash
# List all configured aliases
git config --global --get-regexp alias

# View specific alias
git config --global alias.st
```

### Remove an Alias

```bash
# Remove specific alias
git config --global --unset alias.st
```

### Edit All Aliases

```bash
# Open global config in editor
git config --global --edit
```

---

## Advanced Alias Patterns

### Shell Aliases (using `!`)

Git aliases can execute shell commands by prefixing with `!`:

```bash
# Example: Complex shell alias
git config --global alias.recent '!git for-each-ref --sort=-committerdate --format="%(committerdate:short) %(refname:short)" refs/heads/ | head -n 10'

# Example: Alias that uses shell pipeline
git config --global alias.branches '!git branch -a | grep -v "HEAD" | sort'
```

**Usage:**

```bash
git recent     # Shows 10 most recently committed branches
git branches   # Shows sorted branch list
```

**When to use shell aliases:**

- Complex operations requiring multiple commands
- Filtering or transforming output with grep/awk/sed
- Conditional logic or loops

---

## Recommended Alias Sets

### Minimal Set (Essential Only)

If you prefer fewer aliases, start with these essentials:

```bash
git config --global alias.st "status -sb"
git config --global alias.co "switch"
git config --global alias.br "branch -vv"
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.pfwl "push --force-with-lease"
```

### Full Set (All Aliases)

See the complete list in the sections above for full productivity enhancement.

---

## Official Documentation

- [Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)
- [Git URL Rewriting](https://git-scm.com/docs/git-config#Documentation/git-config.txt-urlltbasegtinsteadOf)
- [Git Config](https://git-scm.com/docs/git-config)

**Last Verified:** 2025-11-17
