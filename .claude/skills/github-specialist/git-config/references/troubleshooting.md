# Git Configuration Troubleshooting

## Table of Contents

- [Line Ending Errors](#line-ending-errors)
- [Credential Issues](#credential-issues)
- [Performance Problems](#performance-problems)
- [Common Real-World Scenarios](#common-real-world-scenarios)

---

## Line Ending Errors

### Error: "LF would be replaced by CRLF" or "CRLF would be replaced by LF"

**What This Means:**

**With `safecrlf=warn` (recommended):** You'll see a **warning** (informational) - the file WILL be staged successfully. This is normal when `.gitattributes` converts line endings.

**With `safecrlf=true` (too strict):** You'll see **"fatal: ..."** error - the file will be **blocked** from staging. This causes constant errors with `.gitattributes`.

**Why This Happens:**

- File in working directory has different line endings than `.gitattributes` specifies
- Example: You edit `.md` file on Windows (gets CRLF), `.gitattributes` says `*.md eol=lf`, Git converts
- This is **correct behavior** with `.gitattributes` - not a problem!
- Only a problem if file has MIXED endings (some LF AND CRLF in same file)

**Solution (Recommended - One-Time Fix for Entire Repo):**

1. **Create `.gitattributes`** in your repository root (see Git Attributes section in SKILL.md)

2. **Normalize all files:**

   ```bash
   git add --renormalize .
   ```

3. **Commit the changes:**

   ```bash
   git commit -m "Normalize line endings with .gitattributes"
   ```

**Solution (Quick Fix for Single File):**

```bash
# Normalize just one file
git add --renormalize path/to/file.md
git commit -m "Normalize line endings in file.md"
```

**Understanding the Safety Check:**

Your configuration uses a **defense-in-depth** strategy:

- `core.autocrlf` (system/global) - Converts line endings automatically
- `core.safecrlf=warn` (global) - **Warns** about conversions that could cause problems
- `.gitattributes` (per-repo) - Explicit control, best practice

**The warning is protecting you!** It's preventing:

- Mixed line endings in your repository
- Files that would break on other platforms
- Phantom diffs (files appearing changed when only line endings differ)

**Why `.gitattributes` is Best:**

- ✅ Explicit control over every file type
- ✅ Works consistently across Windows/WSL/Linux/macOS
- ✅ Team members get the same behavior
- ✅ No surprises or errors

**If You're in a Hurry (Not Recommended):**

```bash
# Temporarily disable the safety check (bypasses protection)
git -c core.safecrlf=false add path/to/file
git commit -m "Your message"
```

⚠️ **Warning:** This bypasses your safety net and can cause problems later.

---

## Credential Issues

### Error: "refusing to allow OAuth App to create or update workflow"

**Cause:** GitHub CLI (gh) credential helper lacks the `workflow` scope needed to modify GitHub Actions workflows.

**Solution:**

```bash
# Re-authenticate with workflow scope
gh auth login --scopes "repo,read:org,workflow" --git-protocol https

# Verify scopes
gh auth status
```

### Git Uses Old/Wrong Credentials

**Cause:** Cached credentials in OS credential manager are stale or incorrect.

**Solution (Windows):**

```bash
# Clear Windows Credential Manager
git credential-manager erase <<< url=https://github.com

# Or manually: Control Panel → Credential Manager → Windows Credentials → Remove git:https://github.com
```

**Solution (macOS):**

```bash
# Clear macOS Keychain
git credential-osxkeychain erase <<< host=github.com

# Or manually: Keychain Access → Search "github" → Delete entries
```

**Solution (Linux):**

```bash
# Clear libsecret cache
git credential-libsecret erase <<< url=https://github.com

# Or clear memory cache (cache helper)
git credential-cache exit
```

### SSH vs HTTPS Confusion

**Issue:** Git push fails because remote URL doesn't match credential setup.

**Check remote URL:**

```bash
git remote -v
# If HTTPS: https://github.com/username/repo.git
# If SSH: git@github.com:username/repo.git
```

**Fix mismatch:**

```bash
# Switch to HTTPS (if using credential helpers)
git remote set-url origin https://github.com/username/repo.git

# Switch to SSH (if using SSH keys)
git remote set-url origin git@github.com:username/repo.git
```

---

## Performance Problems

### Slow `git status` on Large Repos

**Symptom:** `git status` takes 5+ seconds on repos with many files.

**Solution:**

```bash
# Enable filesystem monitoring
git config --global core.fsmonitor true
git config --global core.untrackedCache true

# Verify settings applied
git config --list | grep -E "fsmonitor|untrackedCache"
```

**Note:** On WSL, use Git inside WSL (not Windows Git accessing WSL files) for fsmonitor to work correctly.

### Slow Fetch/Clone Operations

**Symptom:** Fetch or clone operations timeout or take excessive time.

**Solution:**

```bash
# For cloud Git hosts (GitHub/GitLab/Bitbucket)
git config --global fetch.parallel 8

# For corporate/self-hosted servers (may have connection limits)
git config --global fetch.parallel 4

# Verify setting
git config fetch.parallel
```

### Repository Growth / Disk Space Issues

**Symptom:** `.git` directory grows large, takes up excessive disk space.

**Solution:**

```bash
# Run garbage collection
git gc --aggressive --prune=now

# Enable background maintenance (long-term solution)
git maintenance start
git maintenance register  # run in each repo you want maintained
```

---

## Common Real-World Scenarios

### Corporate Proxy Causing Fetch Timeouts

**Symptom:** `fetch.parallel=8` causes timeouts or connection resets in corporate network.

**Solution:**

```bash
# Reduce parallelism for corporate proxies
git config --global fetch.parallel 4

# Or disable entirely if proxy is very restrictive
git config --global fetch.parallel 1

# Verify setting
git config fetch.parallel
```

**Why:** Corporate proxies often limit concurrent connections. High parallelism overwhelms the proxy.

---

### WSL Filesystem Performance Issues

**Symptom:** `core.fsmonitor=true` doesn't improve performance in WSL, `git status` still slow.

**Cause:** Using Windows Git to access files in WSL filesystem (`\\wsl$\...`) or vice versa.

**Solution:**

- **Use Git inside WSL** for files in WSL (`/home/...`)
- **Use Windows Git** for files in Windows (`/mnt/c/...`)
- **Never cross-access** (Windows Git → WSL files or WSL Git → Windows files)

**Verification:**

```bash
# In WSL, check which Git you're using
which git
# Should show: /usr/bin/git (WSL Git)
# NOT: /mnt/c/Program Files/Git/... (Windows Git)

# Check if repo is in WSL or Windows filesystem
pwd
# WSL: /home/username/... (good)
# Windows: /mnt/c/Users/... (use Windows Git for this repo)
```

---

### Rerere Not Applying Remembered Resolutions

**Symptom:** `rerere.enabled=true` but conflicts aren't being resolved automatically.

**Cause:** Conflict context has changed (different surrounding lines) or resolution was never recorded.

**Solution:**

```bash
# Check if rerere has recorded resolutions
ls .git/rr-cache/
# Should show directories with conflict hashes

# View what rerere would apply
git rerere diff

# If no output, rerere has no recorded resolutions for current conflicts
# Resolve manually, rerere will record for next time

# If rerere applies wrong resolution, forget it
git rerere forget path/to/file
```

**Remember:** Rerere only works for IDENTICAL conflicts (same file, same chunk, same surrounding context).

---

### Aliases Not Working After Upgrade

**Symptom:** Custom Git aliases stop working after Git upgrade.

**Cause:** Alias syntax changed or underlying command changed.

**Solution:**

```bash
# View all aliases
git config --global --get-regexp alias

# Test individual alias
git config --global alias.st
# Output: status -sb

# Test alias execution manually
git status -sb  # Does this work?

# If broken, re-add alias with updated syntax
git config --global alias.st "status -sb"
```

---

### Line Endings Normalized But Still See Warnings

**Symptom:** After running `git add --renormalize .`, still see line ending warnings on subsequent commits.

**Cause:** New files being created with wrong line endings, or `.gitattributes` not being respected.

**Solution:**

1. **Verify `.gitattributes` is committed:**

   ```bash
   git ls-files | grep .gitattributes
   # Should show: .gitattributes
   ```

2. **Check your global `core.autocrlf` setting:**

   ```bash
   git config --global core.autocrlf
   # Windows: should be "true" or "false" (if using .gitattributes)
   # macOS/Linux: should be "input"
   ```

3. **Verify editor isn't overriding line endings:**

   - VS Code: Check `.editorconfig` or workspace settings
   - Other editors: Check line ending settings

4. **Re-normalize and commit `.gitattributes` together:**

   ```bash
   git add .gitattributes
   git add --renormalize .
   git commit -m "Normalize line endings with .gitattributes"
   ```

---

## Additional Resources

For more troubleshooting help:

- **Credential Management:** See [credential-management.md](credential-management.md)
- **Line Endings:** See line-endings skill
- **Performance:** See [global-configuration.md](global-configuration.md) Performance Settings section
- **Git Official Troubleshooting:** <https://git-scm.com/docs/git-help>
