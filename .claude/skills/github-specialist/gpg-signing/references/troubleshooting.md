# GPG Signing Troubleshooting Guide

Comprehensive troubleshooting guide for common GPG commit signing issues across all platforms.

## Table of Contents

- [Common Errors](#common-errors)
  - [gpg: signing failed: No secret key](#gpg-signing-failed-no-secret-key)
  - [gpg: signing failed: Inappropriate ioctl for device](#gpg-signing-failed-inappropriate-ioctl-for-device)
  - [gpg: signing failed: Screen or window too small](#gpg-signing-failed-screen-or-window-too-small)
  - [error: gpg failed to sign the data (Generic)](#error-gpg-failed-to-sign-the-data-generic)
  - [Commits Show "Unverified" on GitHub](#commits-show-unverified-on-github)
  - [Passphrase Prompt Every Commit (Cache Not Working)](#passphrase-prompt-every-commit-cache-not-working)
  - [gpg: WARNING: unsafe permissions on homedir](#gpg-warning-unsafe-permissions-on-homedir)
  - [gpg: can't connect to the agent: IPC connect call failed](#gpg-cant-connect-to-the-agent-ipc-connect-call-failed)
  - [error: gpg failed to sign the data - keyboxd Daemon Not Running (Windows)](#error-gpg-failed-to-sign-the-data---keyboxd-daemon-not-running-windows)
  - [gpg: no default secret key: No secret key](#gpg-no-default-secret-key-no-secret-key)
  - [gpg: skipped KEY_ID: No secret key](#gpg-skipped-key_id-no-secret-key)
- [Platform-Specific Issues](#platform-specific-issues)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
  - [WSL](#wsl)
- [Diagnostic Commands](#diagnostic-commands)
  - [Check GPG Installation](#check-gpg-installation)
  - [Check Keys](#check-keys)
  - [Check GPG Agent](#check-gpg-agent)
  - [Check Git Configuration](#check-git-configuration)
  - [Test Signing](#test-signing)
- [Getting Help](#getting-help)
- [Last Verified](#last-verified)

## Common Errors

### "gpg: signing failed: No secret key"

**Error message:**

```text
error: gpg failed to sign the data
fatal: failed to write commit object
```

**Cause:** Git is configured to use a key ID that doesn't exist in your GPG keyring.

**Diagnosis:**

```bash
# List all secret keys in your keyring
gpg --list-secret-keys --keyid-format=long

# Check which key Git is configured to use
git config --global user.signingkey
```

**Solution:**

```bash
# If key doesn't exist, generate new key
gpg --full-generate-key

# Get the new KEY_ID
gpg --list-secret-keys --keyid-format=long
# Look for "sec   ed25519/<KEY_ID>"

# Update Git config with correct KEY_ID
git config --global user.signingkey <KEY_ID>

# Verify configuration
git config --global user.signingkey
```

---

### "gpg: signing failed: Inappropriate ioctl for device"

**Error message:**

```text
error: gpg failed to sign the data
gpg: signing failed: Inappropriate ioctl for device
```

**Cause:** GPG agent cannot prompt for passphrase because it can't access the terminal.

**Solution 1 (Linux/macOS/WSL):**

```bash
# Set GPG_TTY environment variable
export GPG_TTY=$(tty)

# Make permanent - add to shell profile
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc  # or ~/.zshrc for Zsh
source ~/.bashrc
```

**Solution 2 (Windows with Gpg4win):**

```bash
# Use GUI pinentry instead of terminal
echo "pinentry-program \"C:\\Program Files (x86)\\GnuPG\\bin\\pinentry-basic.exe\"" >> ~/.gnupg/gpg-agent.conf

# Restart agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**Solution 3 (macOS):**

```bash
# Use macOS pinentry
echo "pinentry-program /usr/local/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf

# If pinentry-mac not installed
brew install pinentry-mac

# Restart agent
gpgconf --kill gpg-agent
```

---

### "gpg: signing failed: Screen or window too small"

**Cause:** Terminal window is too small for ncurses-based pinentry prompt.

**Solution:**

Use GUI pinentry instead of terminal-based:

**Windows:**

```bash
echo "pinentry-program \"C:\\Program Files (x86)\\GnuPG\\bin\\pinentry-w32.exe\"" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

**macOS:**

```bash
echo "pinentry-program /usr/local/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

**Linux:**

```bash
# Try different pinentry programs
echo "pinentry-program /usr/bin/pinentry-gtk-2" >> ~/.gnupg/gpg-agent.conf
# Or: pinentry-qt, pinentry-gnome3, pinentry-x11

gpgconf --kill gpg-agent
```

---

### "error: gpg failed to sign the data" (Generic)

**Possible causes:** Multiple issues (wrong passphrase, expired key, agent not running, etc.)

**Debug steps:**

1. **Test GPG signing directly:**

   ```bash
   echo "test" | gpg --clearsign
   ```

   - If this fails → GPG issue (not Git issue)
   - If this succeeds → Git configuration issue

2. **Check GPG agent status:**

   ```bash
   gpgconf --list-components
   ```

   Expected output should include `gpg-agent:...running`

3. **Check key expiration:**

   ```bash
   gpg --list-keys --keyid-format=long <KEY_ID>
   ```

   Look for `expired:` in output

4. **Restart GPG agent:**

   ```bash
   gpgconf --kill gpg-agent
   gpgconf --launch gpg-agent
   ```

5. **Verify Git configuration:**

   ```bash
   # Check GPG program path
   git config --global gpg.program

   # Check signing key
   git config --global user.signingkey

   # Check auto-signing enabled
   git config --global commit.gpgsign
   ```

6. **Try commit again:**

   ```bash
   git commit --allow-empty -m "Test GPG signing"
   ```

---

### Commits Show "Unverified" on GitHub

**Possible causes:**

#### 1. Public Key Not Added to GitHub

**Diagnosis:**

- Go to: [https://github.com/settings/keys](https://github.com/settings/keys)
- Check if your GPG key is listed

**Solution:**

```bash
# Export public key
gpg --armor --export <KEY_ID>

# Add to GitHub:
# 1. Go to https://github.com/settings/keys
# 2. Click "New GPG key"
# 3. Paste the exported key
# 4. Click "Add GPG key"
```

#### 2. Email Mismatch

**Diagnosis:**

```bash
# Check Git email
git config --global user.email

# Check GPG key email
gpg --list-keys <KEY_ID>

# Check GitHub verified emails
# Go to: https://github.com/settings/emails
```

**Solution:**

All three must match:

- Git commit email
- GPG key email
- GitHub verified email

**Fix mismatched Git email:**

```bash
git config --global user.email "your.verified@email.com"
```

**Fix mismatched GPG key email:**

```bash
# Add new email to existing key
gpg --edit-key <KEY_ID>
gpg> adduid
# Enter name and new email
gpg> save

# Re-export public key and update on GitHub
gpg --armor --export <KEY_ID>
```

**Verify email on GitHub:**

1. Go to: [https://github.com/settings/emails](https://github.com/settings/emails)
2. Click "Resend verification email" if needed
3. Click link in email to verify

#### 3. Key Expired

**Diagnosis:**

```bash
gpg --list-keys <KEY_ID>
# Look for "expired: YYYY-MM-DD"
```

**Solution:**

```bash
# Extend expiration
gpg --edit-key <KEY_ID>
gpg> expire
# Select new expiration (0 = never, 2y = 2 years, etc.)
gpg> save

# Re-export and update on GitHub
gpg --armor --export <KEY_ID>
```

#### 4. Key Revoked

**Diagnosis:**

```bash
gpg --list-keys <KEY_ID>
# Look for "revoked"
```

**Solution:**

Cannot un-revoke a key. Must generate new key:

```bash
# Generate new key
gpg --full-generate-key

# Configure Git with new key
git config --global user.signingkey <NEW_KEY_ID>

# Export and add to GitHub
gpg --armor --export <NEW_KEY_ID>
```

---

### Passphrase Prompt Every Commit (Cache Not Working)

**Cause:** GPG agent not caching passphrases properly.

**Windows users:** See [Windows-specific caching troubleshooting](#passphrase-caching-not-working-dual-installation-issue) below for dual GPG installation issues.

**Solution 1: Verify correct config file location (CRITICAL for Windows):**

```bash
# Check which GPG Git is using
git config --global gpg.program

# Check GPG's config directory
gpgconf --list-dirs homedir

# Verify config file exists at correct location
# Linux/macOS/WSL:
ls ~/.gnupg/gpg-agent.conf

# Windows (Gpg4win):
ls "$APPDATA/gnupg/gpg-agent.conf"

# Windows (Git Bash GPG):
ls ~/.gnupg/gpg-agent.conf
```

**Solution 2: Configure caching in correct location:**

```bash
# Linux/macOS/WSL:
cat >> ~/.gnupg/gpg-agent.conf <<'EOF'
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase
EOF

# Windows (Gpg4win) - if Git uses C:/Program Files (x86)/GnuPG/bin/gpg.exe:
cat >> "$APPDATA/gnupg/gpg-agent.conf" <<'EOF'
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase
# REQUIRED for Windows:
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
EOF

# Restart agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**Solution 3: Verify configuration loaded:**

```bash
gpgconf --list-options gpg-agent | grep cache-ttl
# Should show your configured values (e.g., 28800 for 8 hours)
```

**Solution 4: Kill multiple agents:**

```bash
# Linux/macOS/WSL:
pkill gpg-agent

# Windows:
taskkill /F /IM gpg-agent.exe

# Start single agent
gpgconf --launch gpg-agent
```

**Solution 5: Check for config syntax errors:**

```bash
# Verify config file syntax
cat ~/.gnupg/gpg-agent.conf  # Or $APPDATA/gnupg/gpg-agent.conf on Windows

# Check for errors
gpgconf --check-options gpg-agent
```

---

### "gpg: WARNING: unsafe permissions on homedir"

**Cause:** GPG home directory permissions are too permissive (world-readable).

**Solution (Linux/macOS):**

```bash
# Fix directory permissions
chmod 700 ~/.gnupg

# Fix file permissions
chmod 600 ~/.gnupg/*
```

**Solution (Windows):**

1. Right-click `C:\Users\<Username>\.gnupg` → Properties → Security
2. Click "Advanced" → "Disable inheritance"
3. Remove all users except your account
4. Ensure your account has "Full Control"
5. Apply changes

---

### "gpg: can't connect to the agent: IPC connect call failed"

**Cause:** GPG agent is not running or socket is invalid.

**Solution:**

```bash
# Kill any existing agents
gpgconf --kill gpg-agent

# Launch agent
gpgconf --launch gpg-agent

# Verify agent started
gpgconf --list-components | grep gpg-agent
```

**Alternative (systemd on Linux):**

```bash
# Check agent service
systemctl --user status gpg-agent

# Restart service
systemctl --user restart gpg-agent

# Enable socket
systemctl --user enable --now gpg-agent.socket
```

---

### "error: gpg failed to sign the data" - keyboxd Daemon Not Running (Windows)

**Symptoms:**

- `error: gpg failed to sign the data` when attempting to commit
- `fatal: failed to write commit object`
- First operation after Windows reboot fails, subsequent attempts may succeed
- 30-60 second hang before error on cold boot

**Root Cause:**

Windows daemon startup race condition where keyboxd daemon is not running or fails to start properly. This is a known issue in GPG4win with multiple bug tracker entries:

- **T7777**: "Gpg4win fails to connect to keyboxd on a cold boot" (affects GPG4win 4.4.1 and 5.0 beta)
- **T7829**: "w32: daemon startup and connection race when socket file already exists" (root cause, FIXED in master branch commit rGae431b04370f)
- Related: T7658, T7720, T6623

**Official Design vs. Windows Reality:**

- **Official design**: GnuPG agents (including keyboxd) are designed for on-demand automatic startup. Official documentation states "no reason to start manually."
- **Windows reality**: Windows 11 frequently exhibits startup failures due to race conditions. First operation after reboot often fails with connection timeout.

**Solution Workflow:**

#### Step 1: Detect which GPG installation Git is using

```bash
# Check Git's GPG configuration
git config --get gpg.program

# Example outputs:
# C:/Program Files (x86)/GnuPG/bin/gpg.exe  → Gpg4win
# /usr/bin/gpg                               → Git Bash GPG
# (no output)                                → Using system PATH
```

#### Step 2: Launch keyboxd from the CORRECT GPG installation

**CRITICAL**: You must launch keyboxd from the SAME GPG installation that Git is configured to use. Launching from the wrong installation will not fix the issue.

```bash
# If Git uses Gpg4win (C:/Program Files (x86)/GnuPG/bin/gpg.exe):
"C:/Program Files (x86)/GnuPG/bin/gpgconf.exe" --launch keyboxd

# If Git uses Git Bash GPG (/usr/bin/gpg):
gpgconf --launch keyboxd

# If Git uses system PATH (no explicit gpg.program):
# First determine which GPG is in PATH:
where gpg
# Then use gpgconf from the same location
```

#### Step 3: Verify keyboxd started correctly

```bash
# Check agent status (use same GPG as Git)
gpgconf --list-components | grep keyboxd

# Should show:
# keyboxd:GnuPG Key Storage:/path/to/keyboxd
```

#### Step 4: Test signing capability

```bash
# Test GPG signing directly
echo "test" | gpg --clearsign

# If successful, try Git commit
git commit --allow-empty -m "Test commit after keyboxd fix"
```

**Workarounds for Persistent Issues:**

If cold boot issues occur frequently:

1. **Primary approach**: Rely on automatic on-demand startup (official design)
   - Most operations will succeed after brief delay
   - Second attempt usually works if first fails

2. **If cold boot issues persist**:
   - Open Kleopatra before first commit (triggers agent startup)
   - Or manually run: `gpgconf --launch keyboxd` (from correct GPG path)
   - Or retry commit (second attempt usually succeeds)

3. **Last resort only**: Task Scheduler startup script
   - **NOT officially recommended** (community workaround)
   - May cause conflicts or permission issues
   - Use only for severe persistent problems
   - See [Windows Setup - Automatic Agent Startup](windows-setup.md#automatic-agent-startup-on-windows) for details

**Future Outlook:**

- T7829 fix merged to master branch (commit rGae431b04370f)
- Will be included in upcoming GPG4win stable releases
- Should significantly improve Windows reliability

**Common Mistakes to Avoid:**

1. ❌ Launching keyboxd from wrong GPG installation (Gpg4win vs Git Bash GPG)
2. ❌ Assuming automatic startup works reliably on Windows (it should, but often doesn't)
3. ❌ Using Windows Services for gpg-agent/keyboxd (not supported, causes issues)
4. ❌ Not retrying after first failure (second attempt often succeeds)

**Bug Tracker References:**

- [T7777: Gpg4win fails to connect to keyboxd on a cold boot](https://dev.gnupg.org/T7777)
- [T7829: w32: daemon startup and connection race when socket file already exists](https://dev.gnupg.org/T7829)
- [T7658: Connection race conditions](https://dev.gnupg.org/T7658)
- [T7720: Related startup issues](https://dev.gnupg.org/T7720)
- [T6623: Windows startup robustness](https://dev.gnupg.org/T6623)

---

### "gpg: no default secret key: No secret key"

**Cause:** No key is set as default, or Git config doesn't specify which key to use.

**Solution:**

```bash
# List all secret keys
gpg --list-secret-keys --keyid-format=long

# Set key in Git config
git config --global user.signingkey <KEY_ID>

# Verify
git config --global user.signingkey
```

---

### "gpg: skipped <KEY_ID>: No secret key"

**Cause:** Public key exists in keyring but private key is missing.

**Diagnosis:**

```bash
# List public keys
gpg --list-keys <KEY_ID>

# List secret keys
gpg --list-secret-keys <KEY_ID>
```

**Solution:**

If private key is missing, you must either:

1. **Import private key from backup:**

   ```bash
   gpg --import /path/to/private-key-backup.asc
   ```

2. **Generate new key:**

   ```bash
   gpg --full-generate-key
   git config --global user.signingkey <NEW_KEY_ID>
   ```

---

## Platform-Specific Issues

### Windows

#### Git Bash Can't Find GPG

**Cause:** Git not configured to use Gpg4win.

**Solution:**

```bash
# Set GPG program path
git config --global gpg.program "C:/Program Files (x86)/GnuPG/bin/gpg.exe"

# Verify
where.exe gpg
```

#### Pinentry Dialog Doesn't Appear

**Cause:** Pinentry configuration missing or incorrect.

**Solution:**

```bash
echo "pinentry-program \"C:\\Program Files (x86)\\GnuPG\\bin\\pinentry-w32.exe\"" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

#### Passphrase Caching Not Working (Dual Installation Issue)

**Symptom:** Configured passphrase caching (cache TTL settings) but still prompted for passphrase on every commit.

**Root Cause:** Windows has TWO separate GPG installations:

1. **Gpg4win** - Config at `%APPDATA%\gnupg\gpg-agent.conf`
2. **Git Bash GPG** - Config at `~/.gnupg/gpg-agent.conf` (resolves to `C:\Users\<Username>\.gnupg\gpg-agent.conf`)

**Common mistake:** Configuring Git Bash GPG location (`~/.gnupg/`) when Git is configured to use Gpg4win (`%APPDATA%\gnupg/`). Result: **configuration silently ignored**.

**Diagnosis:**

```bash
# Step 1: Verify which GPG Git is using
git config --global gpg.program

# If output is "C:/Program Files (x86)/GnuPG/bin/gpg.exe":
# → You're using Gpg4win
# → Config must be at: %APPDATA%\gnupg\gpg-agent.conf

# If output is "/usr/bin/gpg" or blank:
# → You're using Git Bash GPG
# → Config must be at: ~/.gnupg/gpg-agent.conf

# Step 2: Verify GPG's config directory
gpgconf --list-dirs homedir
# This shows which directory the active GPG is reading

# Step 3: Check if config exists at correct location
# For Gpg4win:
ls "$APPDATA/gnupg/gpg-agent.conf"
# For Git Bash GPG:
ls ~/.gnupg/gpg-agent.conf

# Step 4: Verify cache settings are loaded
gpgconf --list-options gpg-agent | grep cache-ttl
# Should show your configured values (e.g., 28800 for 8 hours)
# If shows defaults (600), config not loaded from correct location
```

##### Solution: Create config in correct location

**For Gpg4win users (most Windows users):**

```bash
# Create config at Gpg4win location
cat > "$APPDATA/gnupg/gpg-agent.conf" << 'EOF'
# Cache passphrase for 8 hours
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase

# REQUIRED for Windows: pinentry program
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
EOF

# Restart GPG agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent

# Verify settings loaded
gpgconf --list-options gpg-agent | grep cache-ttl
# Expected: default-cache-ttl ... 28800

# Test caching works
git commit --allow-empty -m "Test 1"  # Will prompt
git commit --allow-empty -m "Test 2"  # Should NOT prompt
```

**For Git Bash GPG users (rare):**

```bash
# Create config at Git Bash GPG location
cat > ~/.gnupg/gpg-agent.conf << 'EOF'
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
EOF

# Restart agent
gpgconf --kill gpg-agent
```

**Why pinentry-program is required on Windows:**

Without the `pinentry-program` line, passphrase caching may fail on Windows even with correct cache TTL settings. This is a Windows-specific requirement.

**Verification:**

```bash
# After applying fix, test caching
git commit --allow-empty -m "Cache test 1"
# → Will prompt for passphrase

git commit --allow-empty -m "Cache test 2"
# → Should NOT prompt (uses cached passphrase)

# If still prompting:
# 1. Verify config loaded:
gpgconf --list-options gpg-agent | grep -E "(cache-ttl|pinentry)"

# 2. Check multiple agents not running:
taskkill /F /IM gpg-agent.exe
gpgconf --launch gpg-agent

# 3. Try again
```

**See also:**

- [Windows Setup Guide](windows-setup.md#understanding-dual-gpg-installations-on-windows) - Detailed explanation of dual installations
- [Passphrase Caching Reference](passphrase-caching.md#windows-determining-correct-config-file-location) - Complete caching configuration guide

### macOS

#### GPG Agent Conflicts with macOS Keychain

**Cause:** macOS keychain trying to manage GPG.

**Solution:**

```bash
# Ensure GPG_TTY is set
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.zshrc

# Use GPG pinentry (not macOS Keychain)
echo "pinentry-program /usr/local/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf
brew install pinentry-mac
gpgconf --kill gpg-agent
```

### Linux

#### Systemd Not Starting GPG Agent

**Cause:** GPG agent socket not enabled.

**Solution:**

```bash
# Enable and start socket
systemctl --user enable --now gpg-agent.socket

# Verify
systemctl --user status gpg-agent
```

#### GNOME Keyring Interfering

**Cause:** GNOME Keyring managing GPG agent.

**Solution:**

Disable GNOME Keyring GPG integration:

1. Edit `/etc/xdg/autostart/gnome-keyring-gpg.desktop`
2. Add line: `Hidden=true`
3. Logout and login

### WSL

#### GPG Agent Not Starting in WSL

**Cause:** WSL environment variables not set.

**Solution:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export GPG_TTY=$(tty)

# Restart shell
source ~/.bashrc
```

---

## Diagnostic Commands

### Check GPG Installation

```bash
# GPG version
gpg --version

# GPG executable location
which gpg

# Git GPG program configuration
git config --global gpg.program
```

### Check Keys

```bash
# List all public keys
gpg --list-keys --keyid-format=long

# List all secret (private) keys
gpg --list-secret-keys --keyid-format=long

# Check specific key details
gpg --list-keys --keyid-format=long --with-subkey-fingerprints <KEY_ID>
```

### Check GPG Agent

```bash
# Agent status
gpgconf --list-components | grep gpg-agent

# Agent version
gpg-agent --version

# Cache TTL settings
gpgconf --list-options gpg-agent | grep cache-ttl
```

### Check Git Configuration

```bash
# Show all Git GPG-related settings
git config --global --get-regexp gpg

# Show signing key
git config --global user.signingkey

# Show auto-sign setting
git config --global commit.gpgsign

# Show GPG program path
git config --global gpg.program
```

### Test Signing

```bash
# Test GPG signing directly
echo "test" | gpg --clearsign

# Test Git commit signing
git commit --allow-empty -m "Test"

# Verify commit signature
git log --show-signature -1
```

---

## Getting Help

If you've tried all troubleshooting steps and still have issues:

1. **Check GPG logs:**

   ```bash
   # Enable GPG debug logging
   echo "log-file /tmp/gpg-agent.log" >> ~/.gnupg/gpg-agent.conf
   echo "debug-level basic" >> ~/.gnupg/gpg-agent.conf
   gpgconf --kill gpg-agent

   # Reproduce issue, then check log
   cat /tmp/gpg-agent.log
   ```

2. **Run Git with trace:**

   ```bash
   GIT_TRACE=1 git commit -m "test"
   ```

3. **Check official documentation:**
   - [GnuPG Documentation](https://www.gnupg.org/documentation/)
   - [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
   - [GitHub GPG Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification)

4. **Ask for help:**
   - [Git Mailing List](https://git-scm.com/community)
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/gpg+git)
   - [GnuPG Users Mailing List](https://lists.gnupg.org/mailman/listinfo/gnupg-users)

---

## Last Verified

2025-11-22
