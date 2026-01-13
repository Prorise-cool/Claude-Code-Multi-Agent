# GPG Passphrase Caching Configuration

Comprehensive guide to configuring GPG agent passphrase caching for better workflow while maintaining security.

## Table of Contents

- [Overview](#overview)
- [Configuration File](#configuration-file)
  - [Windows: Determining Correct Config File Location](#windows-determining-correct-config-file-location)
- [Basic Configuration](#basic-configuration)
  - [Recommended Configuration (8-Hour Workday)](#recommended-configuration-8-hour-workday)
  - [How It Works](#how-it-works)
- [Recommended Settings by Scenario](#recommended-settings-by-scenario)
  - [Scenario 1: High Security (Shared Machines, Client Work)](#scenario-1-high-security-shared-machines-client-work)
  - [Scenario 2: Balanced Security (Normal Development)](#scenario-2-balanced-security-normal-development)
  - [Scenario 3: Convenience (Recommended for Most Users)](#scenario-3-convenience-recommended-for-most-users)
- [Applying Configuration](#applying-configuration)
  - [Create or Edit Configuration File](#create-or-edit-configuration-file)
  - [Restart GPG Agent](#restart-gpg-agent)
  - [Verify Configuration Loaded](#verify-configuration-loaded)
- [Testing Passphrase Caching](#testing-passphrase-caching)
  - [Test Cache Behavior](#test-cache-behavior)
  - [Test Cache Expiration](#test-cache-expiration)
- [Clearing Cache Manually](#clearing-cache-manually)
  - [Clear All Cached Passphrases](#clear-all-cached-passphrases)
- [Security Considerations](#security-considerations)
  - [Longer Cache Times (More Convenient)](#longer-cache-times-more-convenient)
  - [Shorter Cache Times (More Secure)](#shorter-cache-times-more-secure)
  - [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)
  - [Different Cache Times for Different Keys](#different-cache-times-for-different-keys)
  - [Disable Caching for Specific Operations](#disable-caching-for-specific-operations)
  - [Preload Cache (Expert Use Only)](#preload-cache-expert-use-only)
- [Troubleshooting](#troubleshooting)
  - [Cache Not Working (Prompts Every Time)](#cache-not-working-prompts-every-time)
  - [Cache Persisting Too Long](#cache-persisting-too-long)
  - [Cache Cleared on Screen Lock](#cache-cleared-on-screen-lock)
- [Platform-Specific Notes](#platform-specific-notes)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [References](#references)
- [Last Verified](#last-verified)

## Overview

GPG agent caches passphrases in memory to reduce how often you need to enter them. Proper configuration balances security (shorter cache) with convenience (longer cache).

## Configuration File

**Location:** `~/.gnupg/gpg-agent.conf`

**Platform paths:**

- **Linux/macOS:** `/home/<username>/.gnupg/gpg-agent.conf`
- **Windows (Gpg4win):** `%APPDATA%\gnupg\gpg-agent.conf` (typically `C:\Users\<Username>\AppData\Roaming\gnupg\gpg-agent.conf`)
- **Windows (Git Bash GPG):** `C:\Users\<Username>\.gnupg\gpg-agent.conf`
- **WSL:** `/home/<username>/.gnupg/gpg-agent.conf`

### Windows: Determining Correct Config File Location

**Windows has two GPG installations with different config locations:**

1. **Gpg4win** (recommended) - Installed at `C:\Program Files (x86)\GnuPG\`
   - Config location: `%APPDATA%\gnupg\gpg-agent.conf`
   - Resolves to: `C:\Users\<Username>\AppData\Roaming\gnupg\gpg-agent.conf`

2. **Git Bash GPG** (bundled with Git for Windows) - Located at `/usr/bin/gpg` in Git Bash
   - Config location: `C:\Users\<Username>\.gnupg\gpg-agent.conf`
   - Same as `~/.gnupg/gpg-agent.conf` in Git Bash

**CRITICAL:** The config file location must match which GPG Git is configured to use. If you configure the wrong location, your cache settings will be silently ignored.

**Verify which GPG Git is using:**

```bash
# Check which GPG Git is configured to use
git config --global gpg.program

# Expected outputs:
# Gpg4win: "C:/Program Files (x86)/GnuPG/bin/gpg.exe"
# Git Bash: "/usr/bin/gpg" or blank (uses default)
```

**Verify correct config directory:**

```bash
# For Gpg4win (if Git uses C:/Program Files (x86)/GnuPG/bin/gpg.exe)
ls "$APPDATA/gnupg/gpg-agent.conf"

# For Git Bash GPG (if Git uses /usr/bin/gpg or default)
ls ~/.gnupg/gpg-agent.conf

# Or check GPG's config directory directly
gpgconf --list-dirs homedir
```

**Recommendation:** Use Gpg4win and configure `%APPDATA%\gnupg\gpg-agent.conf`. This is the standard Windows GPG installation and is what Git for Windows recommends.

## Basic Configuration

### Recommended Configuration (8-Hour Workday)

**Linux/macOS/WSL:**

```conf
# GPG Agent Configuration
# This caches your passphrase to reduce how often you need to enter it

# Cache passphrase for 8 hours (28800 seconds) of inactivity
default-cache-ttl 28800

# Maximum cache time of 24 hours (86400 seconds) regardless of use
max-cache-ttl 86400

# Allow pinentry to cache the passphrase
allow-preset-passphrase
```

**Windows (Gpg4win) - Location: `%APPDATA%\gnupg\gpg-agent.conf`:**

```conf
# GPG Agent Configuration for Windows (Gpg4win)
# This caches your passphrase to reduce how often you need to enter it

# Cache passphrase for 8 hours (28800 seconds) of inactivity
default-cache-ttl 28800

# Maximum cache time of 24 hours (86400 seconds) regardless of use
max-cache-ttl 86400

# Allow pinentry to cache the passphrase
allow-preset-passphrase

# REQUIRED for Windows: Specify pinentry program for reliable caching
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
```

**Note for Windows users:** The `pinentry-program` line is **required** for reliable passphrase caching on Windows. Without it, caching may not work properly. Adjust the path if Gpg4win is installed in a different location.

### How It Works

**default-cache-ttl:**

- Passphrase cached for specified seconds after last use
- Each time you sign a commit, timer resets
- After period of inactivity, cache expires

**Example (28800 seconds = 8 hours):**

- Enter passphrase at 9:00 AM
- Make commits throughout the day (no prompts)
- No commits for 8 hours → cache expires at 5:00 PM
- Make commit at 11:00 AM → cache expires at 7:00 PM (8 hours from last use)

**max-cache-ttl:**

- Absolute maximum cache duration
- Even with continuous use, passphrase expires after this time
- Forces re-authentication at least once per period

**Example (86400 seconds = 24 hours):**

- Enter passphrase at 9:00 AM
- Even with continuous commits, cache expires at 9:00 AM next day
- Ensures daily passphrase entry minimum

**allow-preset-passphrase:**

- Enables GPG agent to cache passphrases in memory
- Required for cache TTL settings to work
- Passphrase stored in protected agent process memory

## Recommended Settings by Scenario

| Scenario | default-cache-ttl | max-cache-ttl | Rationale |
| --- | --- | --- | --- |
| **High Security** | 900 (15 min) | 3600 (1 hour) | Prompt frequently, minimal cache window |
| **Balanced Security** | 3600 (1 hour) | 28800 (8 hours) | Prompt every ~hour, expires by end of day |
| **Convenience (Recommended)** | 28800 (8 hours) | 86400 (24 hours) | Prompt once per workday, expires overnight |
| **Low Security** | 43200 (12 hours) | 604800 (1 week) | Rarely prompt (NOT recommended) |

### Scenario 1: High Security (Shared Machines, Client Work)

```conf
# High security: Prompt frequently
default-cache-ttl 900       # 15 minutes
max-cache-ttl 3600          # 1 hour maximum
allow-preset-passphrase
```

**When to use:**

- Working on shared machines
- Handling sensitive client data
- Public workspaces (coffee shops, co-working)
- Compliance requirements

**Trade-offs:**

- ✅ Minimal window for memory-based attacks
- ✅ Expires quickly if you forget to lock screen
- ⚠️ Frequent passphrase prompts (workflow interruption)

### Scenario 2: Balanced Security (Normal Development)

```conf
# Balanced: Prompt every ~hour
default-cache-ttl 3600      # 1 hour
max-cache-ttl 28800         # 8 hours maximum
allow-preset-passphrase
```

**When to use:**

- Normal development workflow
- Private office or home
- Moderate security requirements

**Trade-offs:**

- ✅ Reasonable security (1-hour exposure window)
- ✅ Not too many prompts (1-2 times per work session)
- ⚠️ May interrupt flow state occasionally

### Scenario 3: Convenience (Recommended for Most Users)

```conf
# Convenience: Prompt once per workday
default-cache-ttl 28800     # 8 hours
max-cache-ttl 86400         # 24 hours maximum
allow-preset-passphrase
```

**When to use:**

- Personal development
- Trusted private machine
- BitLocker/FileVault disk encryption enabled
- Lock screen when away habit

**Trade-offs:**

- ✅ Minimal friction (enter passphrase once in morning)
- ✅ Expires overnight (24-hour max)
- ⚠️ Longer window for memory attacks (if machine compromised)

**Recommended if:**

- You practice locking screen when away (Windows + L, Cmd+Ctrl+Q)
- Your drive is encrypted (BitLocker, FileVault, LUKS)
- You work on a private, physically secure machine

## Applying Configuration

### Create or Edit Configuration File

```bash
# Create/edit gpg-agent.conf
nano ~/.gnupg/gpg-agent.conf

# Or use echo to append settings
cat >> ~/.gnupg/gpg-agent.conf <<'EOF'
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase
EOF
```

### Restart GPG Agent

```bash
# Kill existing agent
gpgconf --kill gpg-agent

# Launch new agent (loads new config)
gpgconf --launch gpg-agent

# Verify agent is running
gpgconf --list-components | grep gpg-agent
```

### Verify Configuration Loaded

```bash
# Check cache TTL settings
gpgconf --list-options gpg-agent | grep cache-ttl

# Expected output:
# default-cache-ttl:24:0:28800
# max-cache-ttl:24:0:86400
```

## Testing Passphrase Caching

### Test Cache Behavior

```bash
# 1. Make first commit (will prompt for passphrase)
git commit --allow-empty -m "Test caching - first commit"
# → Passphrase prompt appears

# 2. Wait 1 minute

# 3. Make second commit (should NOT prompt if cache working)
git commit --allow-empty -m "Test caching - second commit"
# → No passphrase prompt (cache hit!)

# 4. Verify both commits are signed
git log --show-signature -2
```

### Test Cache Expiration

```bash
# 1. Make commit (enter passphrase)
git commit --allow-empty -m "Test expiration"

# 2. Wait for default-cache-ttl to expire
# (e.g., wait 16 minutes if default-cache-ttl is 900 seconds / 15 min)

# 3. Make another commit (should prompt again)
git commit --allow-empty -m "After cache expired"
# → Passphrase prompt appears (cache expired)
```

## Clearing Cache Manually

### Clear All Cached Passphrases

```bash
# Method 1: Reload agent (clears cache)
gpgconf --reload gpg-agent

# Method 2: Kill and restart agent (more thorough)
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**When to clear cache manually:**

- Before stepping away from machine
- After handling sensitive operations
- When testing cache configuration
- Before shutting down

## Security Considerations

### Longer Cache Times (More Convenient)

**Pros:**

- ✅ Fewer passphrase prompts (smoother workflow)
- ✅ Reduces chance of typos (fewer entries)
- ✅ Better user experience

**Cons:**

- ⚠️ Passphrase remains in memory longer (larger attack window)
- ⚠️ Unlocked session vulnerable if you walk away
- ⚠️ Memory dump attacks have longer window

**Mitigations:**

- Always lock screen when away (Windows + L, Cmd+Ctrl+Q, Ctrl+Alt+L)
- Enable disk encryption (BitLocker, FileVault, LUKS)
- Use physical security (locked office, home workspace)
- Set max-cache-ttl to force daily re-entry

### Shorter Cache Times (More Secure)

**Pros:**

- ✅ Reduced window for memory-based attacks
- ✅ Expires quickly if you forget to lock screen
- ✅ Better for shared/public machines

**Cons:**

- ⚠️ Frequent passphrase prompts (workflow interruption)
- ⚠️ May lead to simpler passphrases (user frustration)
- ⚠️ Interrupts flow state during active development

### Best Practices

**Always:**

- ✅ Lock screen when stepping away
- ✅ Use disk encryption (protects keys at rest)
- ✅ Use strong passphrase (20+ characters)
- ✅ Set max-cache-ttl (forces periodic re-entry)

**Consider:**

- ✅ Shorter cache on shared machines (15-60 min)
- ✅ Longer cache on private machines (4-8 hours)
- ✅ Test cache behavior to verify configuration
- ✅ Clear cache manually before shutdown

**Avoid:**

- ❌ Infinite cache (no max-cache-ttl)
- ❌ Extremely long cache times (>1 week)
- ❌ Disabling passphrase entirely (except for automation keys)
- ❌ Relying solely on cache (always test expiration)

## Advanced Configuration

### Different Cache Times for Different Keys

**Not directly supported** - GPG agent caches all keys with same TTL.

**Workaround:** Use separate GPG agents for different security contexts (complex, rarely needed).

### Disable Caching for Specific Operations

```bash
# Force passphrase prompt (bypass cache)
echo "no-allow-external-cache" >> ~/.gnupg/gpg-agent.conf
```

**Not recommended** for commit signing (defeats the purpose of caching).

### Preload Cache (Expert Use Only)

```bash
# Preload passphrase into cache without signing
gpg-preset-passphrase --preset <KEYGRIP>
```

**Keygrip:** Unique identifier for key (different from KEY_ID).

**Get keygrip:**

```bash
gpg --list-secret-keys --with-keygrip
```

## Troubleshooting

### Cache Not Working (Prompts Every Time)

**Possible causes:**

1. **Configuration not loaded:**

   ```bash
   # Verify config file exists
   cat ~/.gnupg/gpg-agent.conf

   # Restart agent
   gpgconf --kill gpg-agent
   gpgconf --launch gpg-agent
   ```

2. **Multiple agents running:**

   ```bash
   # Kill all agents
   pkill gpg-agent

   # Start single agent
   gpgconf --launch gpg-agent
   ```

3. **Syntax error in config file:**

   ```bash
   # Check for errors (should return nothing)
   gpgconf --check-options gpg-agent
   ```

### Cache Persisting Too Long

**Verify current settings:**

```bash
gpgconf --list-options gpg-agent | grep cache-ttl
```

**Update and restart:**

```bash
# Edit config
nano ~/.gnupg/gpg-agent.conf

# Restart agent
gpgconf --kill gpg-agent
```

### Cache Cleared on Screen Lock

**Some desktop environments clear GPG cache on screen lock.**

**Check desktop environment behavior:**

- GNOME Keyring may manage GPG agent
- KDE Wallet may manage GPG agent
- macOS Keychain may integrate with GPG

**Disable desktop environment GPG management if needed** (consult desktop docs).

## Platform-Specific Notes

### Windows

#### Dual GPG Installation Issue (CRITICAL)

**Windows typically has TWO separate GPG installations:**

1. **Gpg4win** (standalone installation)
   - Location: `C:\Program Files (x86)\GnuPG\`
   - Config: `%APPDATA%\gnupg\gpg-agent.conf`
   - Resolves to: `C:\Users\<Username>\AppData\Roaming\gnupg\gpg-agent.conf`
   - **Recommended** for Windows users

2. **Git Bash GPG** (bundled with Git for Windows)
   - Location: `/usr/bin/gpg` (in Git Bash environment)
   - Config: `~/.gnupg/gpg-agent.conf` (Git Bash home)
   - Resolves to: `C:\Users\<Username>\.gnupg\gpg-agent.conf`
   - Separate keyring from Gpg4win

**Common Problem:** Users configure `~/.gnupg/gpg-agent.conf` (Git Bash GPG location), but Git is configured to use Gpg4win, which reads `%APPDATA%\gnupg\gpg-agent.conf`. Result: **configuration silently ignored, caching doesn't work**.

**How to verify which GPG Git is using:**

```bash
# Check Git's GPG configuration
git config --global gpg.program

# If output is "C:/Program Files (x86)/GnuPG/bin/gpg.exe" or similar:
# → You're using Gpg4win → Configure %APPDATA%\gnupg\gpg-agent.conf

# If output is "/usr/bin/gpg" or blank:
# → You're using Git Bash GPG → Configure ~/.gnupg/gpg-agent.conf

# Verify GPG's config directory
gpgconf --list-dirs homedir
# This shows which config directory the active GPG uses
```

**Verify your configuration is in the correct location:**

```bash
# For Gpg4win users (most Windows users)
ls "$APPDATA/gnupg/gpg-agent.conf"

# For Git Bash GPG users (rare)
ls ~/.gnupg/gpg-agent.conf

# Check which config location GPG is reading
gpgconf --list-dirs homedir
```

**Solution if caching not working:**

1. Verify which GPG Git uses: `git config --global gpg.program`
2. Create config in the correct location based on step 1
3. Restart GPG agent: `gpgconf --kill gpg-agent`
4. Test: Sign a commit and verify caching works

#### Windows Configuration Requirements

**pinentry-program is REQUIRED** for reliable passphrase caching on Windows:

```conf
# Add this to your gpg-agent.conf (adjust path if needed)
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
```

Without the `pinentry-program` line, caching may not work properly on Windows.

**Available pinentry options:**

- `pinentry-basic.exe` - Simple text-based dialog (default, recommended)
- `pinentry-qt.exe` - Qt-based GUI dialog (if Qt installed)
- `pinentry-w32.exe` - Windows native dialog

**Default pinentry:** `pinentry-basic.exe` (GUI dialog)

**Cache persistence:** Until logout, agent restart, or max-cache-ttl expires

**Agent autostart:** Managed by Gpg4win installation (launches automatically)

#### Windows Troubleshooting

##### Problem: Configured caching but still prompted every commit

**Diagnostic steps:**

```bash
# 1. Verify which GPG Git is using
git config --global gpg.program

# 2. Check if config file exists at correct location
# For Gpg4win:
ls "$APPDATA/gnupg/gpg-agent.conf"
# For Git Bash GPG:
ls ~/.gnupg/gpg-agent.conf

# 3. Verify config is loaded
"C:/Program Files (x86)/GnuPG/bin/gpgconf.exe" --list-options gpg-agent | grep cache-ttl
# Expected: default-cache-ttl shows your configured value (e.g., 28800)

# 4. Restart GPG agent
"C:/Program Files (x86)/GnuPG/bin/gpgconf.exe" --kill gpg-agent
"C:/Program Files (x86)/GnuPG/bin/gpgconf.exe" --launch gpg-agent

# 5. Test caching
git commit --allow-empty -m "Test cache"
# Enter passphrase
git commit --allow-empty -m "Test cache again"
# Should NOT prompt if caching working
```

**Common cause:** Config file created at wrong location (Git Bash path when using Gpg4win, or vice versa).

**Solution:** Create config at correct location based on `git config --global gpg.program` output.

### macOS

**gpg-agent may conflict with macOS Keychain.**

**Ensure GPG agent is used:**

```bash
# Add to ~/.zshrc or ~/.bash_profile
export GPG_TTY=$(tty)
```

### Linux

**Agent may be managed by systemd.**

**Check systemd service:**

```bash
systemctl --user status gpg-agent
```

**Enable systemd socket:**

```bash
systemctl --user enable --now gpg-agent.socket
```

## References

- [GnuPG Agent Documentation](https://www.gnupg.org/documentation/manuals/gnupg/Invoking-GPG_002dAGENT.html)
- [GPG Agent Configuration Options](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html)

## Last Verified

2025-11-17
