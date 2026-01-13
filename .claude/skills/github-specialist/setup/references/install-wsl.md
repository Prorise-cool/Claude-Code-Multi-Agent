# WSL (Windows Subsystem for Linux)

**Important**: WSL runs Linux (Ubuntu by default), so Git installation is identical to native Linux.

## Table of Contents

- [WSL Version Check](#wsl-version-check)
- [Installation](#installation)
- [Verify Installation](#verify-installation-wsl)
- [WSL-Specific Configuration](#wsl-specific-configuration)
- [WSL2 vs WSL1 Performance](#wsl2-vs-wsl1-performance)
- [Filesystem Performance Guidelines](#filesystem-performance-guidelines)
- [Windows Integration](#windows-integration)
- [Credential Sharing](#credential-sharing-with-windows)
- [Troubleshooting](#troubleshooting)

---

## WSL Version Check

Before installing Git, verify you're running WSL2 (recommended for Git operations):

```bash
# Check WSL version
wsl --list --verbose
```

**Expected output:**

```text
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

**If VERSION shows 1**, upgrade to WSL2:

```powershell
# In PowerShell (as Administrator)
wsl --set-version Ubuntu 2
```

**Why WSL2 matters for Git:**

- WSL2 uses a real Linux kernel (WSL1 uses translation layer)
- 2-5x faster Git operations on Linux filesystem
- Better compatibility with Git hooks and scripts
- Native inotify support (important for file watchers)

---

## Installation

```bash
# WSL uses same commands as Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git
```

For other distributions in WSL:

```bash
# Fedora (if using Fedora WSL)
sudo dnf install git

# openSUSE
sudo zypper install git
```

---

## Verify Installation (WSL)

```bash
git --version
# Expected output: git version 2.52.0 (or newer)
```

---

## WSL-Specific Configuration

**Line ending configuration:**

```bash
git config --global core.autocrlf input
```

**Note**: WSL uses Linux line ending strategy (LF only). The `input` setting ensures:

- Files committed with LF endings (Unix-style)
- Files checked out unchanged (no CRLF conversion)
- Consistent with native Linux behavior

**Default branch:**

```bash
git config --global init.defaultBranch main
```

**User identity:**

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## WSL2 vs WSL1 Performance

| Operation | WSL1 | WSL2 | Improvement |
| --- | --- | --- | --- |
| `git status` (large repo) | ~2-5s | ~0.3-0.8s | 3-6x faster |
| `git clone` | Moderate | Fast | 2-3x faster |
| `git checkout` | Slow | Fast | 3-5x faster |
| File system operations | Translation overhead | Native speed | Significant |

**WSL2 Advantages:**

- Real Linux kernel with full syscall compatibility
- Native ext4 filesystem performance
- Better memory management
- Full Docker integration
- Native inotify for file watching (important for build tools)

**WSL1 Advantages:**

- Faster Windows filesystem access (via mount points)
- Lower memory footprint
- No virtualization overhead
- Better for cross-OS file workflows

**Recommendation**: Use WSL2 for Git repositories stored in the Linux filesystem (`~/`).

---

## Filesystem Performance Guidelines

**Critical performance rule:**

> Keep Git repositories in the WSL/Linux filesystem (`~/repos/`), NOT the Windows filesystem (mounted drives).

**Performance comparison:**

| Location | Read Speed | Write Speed | Git Performance |
| --- | --- | --- | --- |
| `~/repos/` (Linux FS) | Native | Native | Optimal |
| Mounted Windows drives | 5-10x slower | 10-20x slower | Poor |

**Why mounted Windows drives are slow:**

- 9P protocol translation between Linux and Windows
- File permission translation overhead
- Metadata synchronization costs
- No native filesystem caching

**Best practice directory structure:**

```bash
# Create repos directory in Linux filesystem
mkdir -p ~/repos
cd ~/repos

# Clone repositories here
git clone https://github.com/user/repo.git
```

**Accessing WSL files from Windows:**

In File Explorer, type `\\wsl$` in the address bar, then navigate to your distribution (e.g., Ubuntu) and home directory.

---

## Windows Integration

WSL can run Windows applications directly:

```bash
# Open VS Code in current directory
code .

# Open File Explorer in current directory
explorer.exe .

# Run Windows Git (if needed for specific tools)
git.exe status
```

**Note**: Use Linux `git` (not `git.exe`) for repositories in the Linux filesystem for optimal performance.

---

## Credential Sharing with Windows

Share Git credentials between Windows and WSL to avoid entering credentials twice.

### Option 1: Git Credential Manager (Recommended)

**If Git for Windows is installed:** GCM typically auto-configures for WSL. Test first before manual setup:

```bash
# Test if GCM is already working
git ls-remote https://github.com/your-username/private-repo.git
# If this prompts for credentials via Windows GUI, GCM is working
```

**Manual configuration (if auto-config didn't work):**

```bash
# Configure WSL Git to use Windows Git Credential Manager
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

**Verify configuration:**

```bash
# Check the credential helper setting
git config --global credential.helper
# Expected: /mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe
```

### Option 2: SSH Keys (Alternative)

Use the same SSH key in both environments:

**From WSL, copy Windows SSH key:**

```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Copy Windows SSH key to WSL (adjust username)
# Use wslpath or navigate to your Windows user profile
cp "$(wslpath "$USERPROFILE")/.ssh/id_ed25519" ~/.ssh/
cp "$(wslpath "$USERPROFILE")/.ssh/id_ed25519.pub" ~/.ssh/

# Set correct permissions
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

**Or generate a new key pair in WSL:**

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Then add the public key to your GitHub/GitLab account.

---

## Troubleshooting

### Slow Git Operations

**Symptom**: `git status` or other commands are very slow.

**Diagnosis:**

```bash
# Check where your repo is located
pwd

# If it shows a mounted Windows path - that's the problem
```

**Solution**: Move repository to Linux filesystem:

```bash
# Create destination
mkdir -p ~/repos

# Re-clone to Linux filesystem
cd ~/repos
git clone https://github.com/user/myproject.git
```

### Permission Denied Errors

**Symptom**: `Permission denied` when running Git commands.

**Solution**: Check file ownership:

```bash
# Files should be owned by your WSL user
ls -la

# If owned by root, fix ownership
sudo chown -R $(whoami):$(whoami) .
```

### Line Ending Issues

**Symptom**: Files show as modified immediately after checkout.

**Solution**: Configure line endings correctly:

```bash
# In WSL, use input (not true)
git config --global core.autocrlf input

# Refresh the repository
git rm --cached -r .
git reset --hard
```

### WSL Not Recognizing Git

**Symptom**: `git: command not found` after installation.

**Solution**: Restart WSL or refresh shell:

```bash
# Close and reopen WSL terminal
# Or run:
exec bash
```

### Credential Manager Not Working

**Symptom**: Git keeps asking for credentials.

**Solution**: Verify Git for Windows is installed and credential helper is configured:

```bash
# Check current setting
git config --global credential.helper

# Verify Git for Windows GCM exists
ls /mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe

# Configure credential helper if not set
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

---

## Related Skills

For advanced Git configuration in WSL:

- **config** - Comprehensive Git configuration (aliases, performance tuning)
- **line-endings** - Cross-platform line ending management
- **gpg-signing** - GPG commit signing setup

---

**Last Verified:** 2025-11-25 (WSL2 on Windows 11, Ubuntu 22.04/24.04, Git 2.52.0+)
