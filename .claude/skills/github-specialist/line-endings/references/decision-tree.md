# Git Line Endings Decision Tree

Comprehensive decision tree to determine correct line ending configuration for your environment.

## Question 1: Do You Control All Repositories?

Can you add `.gitattributes` to EVERY repository you use?

**YES** → Consider Option 2 (Modern Explicit), but read caveats carefully
**NO** → Use Option 1 (Traditional)

### Why This Matters

- **Option 2 requires .gitattributes** - Without it, line ending behavior is undefined
- **External repositories** often lack .gitattributes
- **Option 1 works everywhere** - Safe default for mixed environments

## Question 2: What Platform Are You On?

### If Using Option 1 (Traditional)

**Windows:**

```bash
git config --global core.autocrlf true
```

This is the Git for Windows default. Converts CRLF→LF on commit, LF→CRLF on checkout.

**macOS:**

```bash
git config --global core.autocrlf input
```

⚠️ **MUST set explicitly** - NOT the default! Converts CRLF→LF on commit, no conversion on checkout.

**Linux:**

```bash
git config --global core.autocrlf input
```

⚠️ **MUST set explicitly** - NOT the default! Converts CRLF→LF on commit, no conversion on checkout.

**WSL:**

```bash
git config --global core.autocrlf input
```

Treat WSL as Linux. Use `input` to prevent CRLF issues.

### If Using Option 2 (Modern Explicit)

**All platforms:**

```bash
git config --global core.autocrlf false
git config --global core.eol native
```

⚠️ **REQUIRES comprehensive .gitattributes** - Broken without it!

## Question 3: Does Repository Have .gitattributes?

Check for existing `.gitattributes` file:

```bash
ls -la .gitattributes
```

### File Exists and Comprehensive?

**YES** → Both Option 1 and Option 2 work

- `.gitattributes` rules override config settings
- Explicit file-level control

**NO** → Option 1 works, Option 2 BROKEN

- Recommendation: Add `.gitattributes` (see gitattributes-guide.md)
- Option 1 provides fallback behavior

## Question 4: What Type of Files Are You Working With?

### Shell Scripts (.sh, .bash)

**MUST use LF** - Unix shells require LF line endings

```gitattributes
*.sh text eol=lf
*.bash text eol=lf
```

⚠️ **Critical**: CRLF in shell scripts causes `^M: bad interpreter` errors

### PowerShell Scripts (.ps1, .cmd, .bat)

**Should use CRLF** - Windows standard

```gitattributes
*.ps1 text eol=crlf
*.cmd text eol=crlf
*.bat text eol=crlf
```

### Documentation (.md, .txt)

**Recommend LF** - Cross-platform standard

```gitattributes
*.md text eol=lf
*.txt text eol=lf
```

### Configuration Files (.json, .yml, .yaml)

**Recommend LF** - Cross-platform standard

```gitattributes
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
```

### Binary Files (.png, .jpg, .pdf, .exe)

**NEVER convert** - Mark as binary

```gitattributes
*.png binary
*.jpg binary
*.pdf binary
*.exe binary
*.zip binary
```

## Common Scenarios

### Scenario: New Developer Joining Cross-Platform Team

**Recommendation**: Option 1 (Traditional)

**Windows developer:**

```bash
git config --global core.autocrlf true
git config --global core.safecrlf warn
```

**macOS/Linux developer:**

```bash
git config --global core.autocrlf input
git config --global core.safecrlf warn
```

**Team adds `.gitattributes`** to repositories over time for explicit control.

### Scenario: Controlled Corporate Environment

**Recommendation**: Option 2 (Modern Explicit)

**All developers:**

```bash
git config --global core.autocrlf false
git config --global core.eol native
git config --global core.safecrlf warn
```

**Repository has comprehensive `.gitattributes`**:

```gitattributes
# Default behavior
* text=auto

# Shell scripts - LF
*.sh text eol=lf

# PowerShell - CRLF
*.ps1 text eol=crlf

# Documentation - LF
*.md text eol=lf

# Binary files
*.png binary
```

### Scenario: Contributing to External Open Source Projects

**Recommendation**: Option 1 (Traditional)

**Reason**: You cannot control whether external repos have `.gitattributes`

**Your config:**

```bash
# Platform-appropriate autocrlf
git config --global core.autocrlf input  # macOS/Linux
# or
git config --global core.autocrlf true   # Windows

git config --global core.safecrlf warn
```

**External repo's `.gitattributes`** (if present) will override your config.

### Scenario: Mixed Environment (Internal + External Repos)

**Recommendation**: Option 1 (Traditional)

**Reason**: Works safely in both controlled and uncontrolled repositories

**Your config**: Platform-specific autocrlf (see above)

**Your internal repos**: Add `.gitattributes` for explicit control

**External repos**: Your autocrlf provides safe fallback

## Verification Steps

After configuration, verify behavior:

### Check Current Config

```bash
git config --list --show-origin | grep -E "autocrlf|eol|safecrlf"
```

Expected output (Option 1, Windows):

```text
file:C:/Users/[User]/.gitconfig    core.autocrlf=true
file:C:/Users/[User]/.gitconfig    core.safecrlf=warn
```

Expected output (Option 1, macOS/Linux):

```text
file:/home/[user]/.gitconfig    core.autocrlf=input
file:/home/[user]/.gitconfig    core.safecrlf=warn
```

### Check File Line Endings

```bash
git ls-files --eol README.md
```

Expected output format:

```text
i/lf    w/crlf  attr/text=auto  README.md
```

- `i/lf`: Index (repository) uses LF
- `w/crlf`: Working directory uses CRLF (Windows) or LF (macOS/Linux)
- `attr/text=auto`: Attribute from `.gitattributes`

### Test Normalization

```bash
# Check for mixed line endings
git ls-files --eol | grep "w/crlf" | grep "eol=lf"

# Should return empty if configuration is correct
```

## Troubleshooting Decision Points

### Problem: Shell Scripts Won't Execute

**Symptom**: `/bin/bash^M: bad interpreter`

**Root Cause**: Shell script has CRLF line endings

**Solution Path**:

1. **Immediate fix**: Convert to LF

   ```bash
   dos2unix script.sh
   # or
   sed -i 's/\r$//' script.sh
   ```

2. **Permanent fix**: Add to `.gitattributes`

   ```gitattributes
   *.sh text eol=lf
   ```

3. **Normalize in repo**:

   ```bash
   git add --renormalize script.sh
   git commit -m "fix: normalize shell script line endings"
   ```

### Problem: Git Shows Every Line Changed

**Symptom**: `git diff` shows all lines modified, but content is identical

**Root Cause**: Line endings changed (CRLF ↔ LF)

**Solution Path**:

1. **Check current line endings**:

   ```bash
   git ls-files --eol file.txt
   ```

2. **Normalize to repository standard**:

   ```bash
   git add --renormalize file.txt
   git commit -m "fix: normalize line endings"
   ```

3. **Prevent recurrence**: Add to `.gitattributes`

   ```gitattributes
   *.txt text eol=lf
   ```

### Problem: Mixed Line Endings in Same File

**Symptom**: Some lines CRLF, some lines LF

**Root Cause**: Inconsistent editor settings or manual editing

**Solution Path**:

1. **Detect mixed endings**:

   ```bash
   git ls-files --eol file.txt
   ```

2. **Fix file**:

   ```bash
   # Convert all to LF
   dos2unix file.txt

   # Or normalize via Git
   git add --renormalize file.txt
   ```

3. **Prevent recurrence**:

   ```bash
   git config --global core.safecrlf warn
   ```

## Summary: Quick Decision Guide

**Use Option 1 (Traditional) if:**

- You work in multiple repositories (internal + external)
- You contribute to open source
- You want safe defaults that work everywhere
- You're setting up Git for first time

**Use Option 2 (Modern Explicit) if:**

- You control ALL repositories you work in
- You can ensure comprehensive `.gitattributes` everywhere
- You want team-wide consistency
- You understand the trade-offs

**Always set core.safecrlf=warn** for early warning of line ending issues.

**Always add .gitattributes** to repositories you control for explicit, self-documenting line ending rules.

---

**Last Updated:** 2025-11-28
