# Git Setup - Configuration Details

Comprehensive guide to Git configuration file locations, hierarchy, and management.

## Configuration File Locations

Understanding where Git stores configuration at different levels.

### System Level

**Location:**

- **Windows**: `<git-install-dir>/etc/gitconfig` (typically `C:/Program Files/Git/etc/gitconfig`)
- **macOS**: `/etc/gitconfig` or `/usr/local/etc/gitconfig`
- **Linux**: `/etc/gitconfig`

**Scope**: All users on the system

**Command**: `git config --system`

**Note**: Requires administrator/sudo privileges to modify

**Use Cases:**

- Enterprise-wide Git settings
- Default configurations for all users
- Organizational standards

**Example:**

```bash
# View system config (requires sudo on macOS/Linux)
sudo git config --system --list

# Set system-wide default branch
sudo git config --system init.defaultBranch main
```

### Global/User Level

#### Traditional Location

**Path:**

- **Windows**: `<user-home>/.gitconfig`
  - Quick access in Explorer: `%USERPROFILE%/.gitconfig`
- **macOS/Linux**: `~/.gitconfig`

**Scope**: Current user, all repositories

**Command**: `git config --global`

**Precedence**: Used if XDG location doesn't exist

#### XDG Base Directory Location

**Path (All Platforms):** `~/.config/git/config`

**Scope**: Current user, all repositories

**Command**: `git config --global`

**Precedence**: If this file exists, Git uses it instead of `~/.gitconfig`

**Why XDG?**

- Follows XDG Base Directory Specification
- Keeps configuration organized in `~/.config/`
- Better separation of concerns
- Modern standard for cross-platform tools

**Migration:**

```bash
# If you have ~/.gitconfig, you can move it to XDG location
mkdir -p ~/.config/git
mv ~/.gitconfig ~/.config/git/config
```

**Note**: Git automatically uses `~/.config/git/config` if it exists, otherwise falls back to `~/.gitconfig`. Both work identically.

### Local/Repository Level

**Location**: `.git/config` (inside repository)

**Scope**: Single repository only

**Command**:

- `git config --local` (explicit)
- `git config` (when inside a repo, defaults to local)

**Use Cases:**

- Repository-specific user identity (work vs personal email)
- Project-specific settings (tabs vs spaces, line endings)
- Temporary overrides for testing

**Example:**

```bash
# Inside a repository, set project-specific email
git config user.email "work@company.com"

# View local config only
git config --local --list
```

## Configuration Hierarchy

**Priority (Highest to Lowest):**

1. **Local** (`.git/config` in repository)
2. **Global** (`~/.config/git/config` or `~/.gitconfig`)
3. **System** (`/etc/gitconfig`)

**Behavior**: Settings at higher priority levels override lower levels.

**Example Scenario:**

```bash
# System: user.name = "System User"
# Global: user.name = "John Doe"
# Local: user.name = "Work John"

# Inside repo with local config:
git config user.name
# Output: Work John (local overrides)

# In repo without local config:
git config user.name
# Output: John Doe (global used)
```

## Viewing Configuration

### View All Configuration

```bash
# Show all config with source files
git config --list --show-origin

# Example output shows file paths for each setting
```

### View Specific Level

```bash
# System config only
git config --system --list

# Global config only
git config --global --list

# Local config only (inside repo)
git config --local --list
```

### View Specific Value

```bash
# Get value (searches all levels, returns highest priority)
git config user.name

# Get value from specific level
git config --global user.name
git config --local user.email
```

## Setting Configuration

### Basic Syntax

```bash
git config [--system|--global|--local] section.key "value"
```

### Common Settings

**User Identity** (Required):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Default Branch**:

```bash
git config --global init.defaultBranch main
```

**Editor**:

```bash
# VS Code
git config --global core.editor "code --wait"

# Vim
git config --global core.editor "vim"

# Nano
git config --global core.editor "nano"

# Notepad (Windows)
git config --global core.editor "notepad"
```

**Line Endings** (see line-endings skill for details):

```bash
# Windows
git config --global core.autocrlf true

# macOS/Linux
git config --global core.autocrlf input
```

## Unsetting Configuration

Remove configuration values entirely.

### Unset Specific Value

```bash
# Unset system config (requires admin/sudo)
git config --system --unset section.key

# Unset global config
git config --global --unset section.key

# Unset local config (inside repo)
git config --unset section.key
```

### Examples

```bash
# Remove global editor setting (revert to default)
git config --global --unset core.editor

# Remove local email override
git config --unset user.email

# Remove system-level default branch
sudo git config --system --unset init.defaultBranch
```

### Unset All Values in Section

```bash
# Remove entire section
git config --remove-section section.name

# Example: Remove all aliases
git config --global --remove-section alias
```

## Editing Configuration Files Directly

You can edit configuration files directly in a text editor.

### Edit with Git Command

```bash
# Edit global config in default editor
git config --global --edit

# Edit local config in default editor (inside repo)
git config --edit
```

### Manual Editing

Configuration files use INI format:

```ini
[user]
    name = John Doe
    email = john@example.com
[core]
    editor = code --wait
    autocrlf = input
[init]
    defaultBranch = main
[alias]
    st = status
    co = checkout
```

**Best Practice**: Use `git config` commands rather than manual editing to avoid syntax errors.

## Configuration Portability

### Backup Global Configuration

```bash
# Copy global config to backup
cp ~/.gitconfig ~/.gitconfig.backup

# Or XDG location
cp ~/.config/git/config ~/.config/git/config.backup
```

### Restore Configuration

```bash
# Restore from backup
cp ~/.gitconfig.backup ~/.gitconfig
```

### Share Configuration Across Machines

**Option 1: Version control** (recommended)

Create a dotfiles repository to sync configuration across machines.

**Option 2: Cloud sync** (Dropbox, OneDrive, etc.)

Use symbolic links to sync gitconfig via cloud storage.

## Conditional Includes

Include different configurations based on conditions (advanced).

### By Directory

```bash
# In ~/.gitconfig or ~/.config/git/config
[includeIf "gitdir:<work-repos-dir>/"]
    path = <work-config-file>
[includeIf "gitdir:<personal-repos-dir>/"]
    path = <personal-config-file>
```

**Use Case**: Automatic work email for work repositories, personal email for personal repositories.

**Example Pattern**:

Main config has default user name. Conditional includes override email based on directory.

Work repos automatically use work email. Personal repos use personal email.

## Troubleshooting Configuration

### Issue: Config Not Taking Effect

**Symptoms**: Setting a config value but Git still uses old value

**Solutions**:

1. **Check configuration hierarchy**:

   ```bash
   git config --list --show-origin | grep setting.name
   ```

   Look for higher-priority config overriding your setting.

2. **Verify you're at correct level**:

   ```bash
   # If you set --local but meant --global:
   git config --global setting.name value
   ```

3. **Check for typos**:

   ```bash
   # Incorrect:
   git config --global core.autcrlf true  # typo

   # Correct:
   git config --global core.autocrlf true
   ```

### Issue: Config File Permissions

**Symptoms**: Permission denied when setting system config

**Solution**: Use sudo (macOS/Linux) or run terminal as Administrator (Windows)

```bash
# macOS/Linux
sudo git config --system init.defaultBranch main

# Windows PowerShell (run as Administrator)
git config --system init.defaultBranch main
```

### Issue: Finding Config File Location

**Solution**: Use `--show-origin` flag

```bash
git config --list --show-origin
```

Shows exact file path for each setting.

## Best Practices

1. **Use Global for Personal Defaults**: Set user identity, editor, line endings globally
2. **Use Local for Project Overrides**: Override email, line endings for specific projects
3. **Avoid System-Level Changes**: Unless managing enterprise environment
4. **Back Up Configuration**: Before major changes, backup `~/.gitconfig`
5. **Use Conditional Includes**: For work/personal repo separation
6. **Document Custom Settings**: Comment your `.gitconfig` for future reference
7. **Test Before Committing**: Verify configuration changes work as expected

---

**Last Updated:** 2025-11-28
