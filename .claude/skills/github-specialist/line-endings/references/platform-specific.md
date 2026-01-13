# Platform-Specific Configuration

Detailed setup guides for Windows, macOS, Linux, and WSL.

## Table of Contents

- [Windows Configuration](#windows-configuration)
- [macOS Configuration](#macos-configuration)
- [Linux Configuration](#linux-configuration)
- [WSL (Windows Subsystem for Linux) Configuration](#wsl-windows-subsystem-for-linux-configuration)
  - [Special Consideration: Two Git Installations](#special-consideration-two-git-installations)
- [Team Onboarding Checklist](#team-onboarding-checklist)

## Windows Configuration

**Recommended Setup (Option 1):**

```bash
# Check current config (should be default from Git for Windows)
git config --global --get core.autocrlf
# Expected: true (Git for Windows default)

# If not set, configure explicitly
git config --global core.autocrlf true
git config --global core.safecrlf warn
```

**What You Get:**

- Files in working directory: CRLF (Windows standard)
- Files in repository: LF (cross-platform standard)
- Automatic conversion on checkout and commit
- Works with and without .gitattributes

**Verification:**

```bash
# Check effective configuration
git config --get core.autocrlf
# Should show: true

git config --get core.safecrlf
# Should show: warn

# Test in a repository
git ls-files --eol | head -5
# Should show: i/lf w/crlf (index has LF, working has CRLF)
```

**Behavior in Different Scenarios:**

| Repository Type | Working Directory | Repository | Behavior |
| --- | --- | --- | --- |
| No .gitattributes | CRLF | LF | Auto-normalized ✅ |
| `.gitattributes * text=auto` | CRLF | LF | Auto-normalized ✅ |
| `.gitattributes *.md eol=lf` | **LF** | LF | Honors attribute ✅ |
| `.gitattributes *.bat eol=crlf` | CRLF | CRLF | Honors attribute ✅ |

**Special Considerations:**

- Git for Windows defaults to `autocrlf=true` during installation
- System-level config in `C:/Program Files/Git/etc/gitconfig`
- User-level config overrides system-level
- Modern editors (VS Code, Visual Studio, IntelliJ) handle both CRLF and LF seamlessly

## macOS Configuration

**Recommended Setup (Option 1):**

```bash
# Set configuration (NOT the macOS Git default!)
git config --global core.autocrlf input
git config --global core.safecrlf warn
```

**What You Get:**

- Files in working directory: LF (Unix standard)
- Files in repository: LF (cross-platform standard)
- Convert CRLF → LF on commit (if Windows files are added)
- No conversion on checkout (LF stays LF)

**Verification:**

```bash
# Check configuration
git config --get core.autocrlf
# Should show: input

git config --get core.safecrlf
# Should show: warn

# Test in a repository
git ls-files --eol | head -5
# Should show: i/lf w/lf (both index and working have LF)
```

**Special Considerations:**

- macOS Git default is `autocrlf=false` - **you must change it to `input`**
- Prevents CRLF from being committed to repos without .gitattributes
- Compatible with Xcode, TextEdit, and all Unix tools
- macOS uses LF natively (Unix-based OS)

## Linux Configuration

**Recommended Setup (Option 1):**

```bash
# Set configuration (NOT the Linux Git default!)
git config --global core.autocrlf input
git config --global core.safecrlf warn
```

**What You Get:**

- Files in working directory: LF (Linux standard)
- Files in repository: LF (cross-platform standard)
- Convert CRLF → LF on commit (if Windows files are added)
- No conversion on checkout (LF stays LF)

**Verification:**

```bash
# Check configuration
git config --get core.autocrlf
# Should show: input

git config --get core.safecrlf
# Should show: warn

# Test in a repository
git ls-files --eol | head -5
# Should show: i/lf w/lf (both index and working have LF)
```

**Special Considerations:**

- Linux Git default is `autocrlf=false` - **you must change it to `input`**
- Critical for shell scripts, Makefiles, and Linux development tools
- Works with vim, nano, emacs, and all Unix editors
- Prevents accidental CRLF commits that break scripts

## WSL (Windows Subsystem for Linux) Configuration

### Special Consideration: Two Git Installations

When using WSL, you typically have TWO separate Git installations:

1. **Windows Git** - `git.exe` (native Windows)
2. **WSL Git** - `git` (Linux within WSL)

Each has its own configuration!

**Recommended Setup:**

```bash
# INSIDE WSL (Linux Git)
git config --global core.autocrlf input
git config --global core.safecrlf warn

# WINDOWS (Windows Git) - if using native Windows Git
git config --global core.autocrlf true
git config --global core.safecrlf warn
```

**What You Get:**

- WSL Git behaves like Linux Git (LF everywhere)
- Windows Git behaves like Windows Git (CRLF in working dir)
- Files are normalized consistently in repository
- Choose which Git to use per repository

**Verification:**

```bash
# Inside WSL
git config --get core.autocrlf
# Should show: input

# In Windows PowerShell/CMD
git config --get core.autocrlf
# Should show: true
```

**File System Considerations:**

```bash
# WSL can access Windows files
cd /mnt/c/Users/YourName/Projects/repo
# Uses WSL Git config (autocrlf=input)

# Windows can access WSL files (Windows 10 1903+)
cd \wsl$\Ubuntu\home\yourname\repo
# Uses Windows Git config (autocrlf=true)
```

**Best Practices:**

- **Repos in `/home/` (WSL filesystem)**: Use WSL Git exclusively
- **Repos in `/mnt/c/` (Windows filesystem)**: Use Windows Git exclusively
- **Avoid mixing**: Don't switch between WSL Git and Windows Git in same repo
- **Performance**: WSL Git is faster when working in WSL filesystem

**VS Code Remote-WSL:**

When using VS Code Remote-WSL extension:

- VS Code uses WSL Git (not Windows Git)
- Respects WSL Git config (`autocrlf=input`)
- Files stay consistent with Linux line endings

## Team Onboarding Checklist

**All team members run:**

```bash
git config --list --show-origin | grep -E "autocrlf|eol|safecrlf"

# Windows expected output:
# file:C:/Program Files/Git/etc/gitconfig    core.autocrlf=true
# file:C:/Users/You/.gitconfig               core.safecrlf=warn

# Mac/Linux expected output:
# file:/home/you/.gitconfig    core.autocrlf=input
# file:/home/you/.gitconfig    core.safecrlf=warn
```
