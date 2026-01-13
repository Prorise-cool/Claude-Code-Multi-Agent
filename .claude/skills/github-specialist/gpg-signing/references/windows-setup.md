# Windows GPG Setup Guide

Comprehensive Windows-specific GPG setup guidance for commit signing.

## Table of Contents

- [Gpg4win Installation](#gpg4win-installation)
  - [Option 1: Official Installer (Recommended for Control)](#option-1-official-installer-recommended-for-control)
  - [Option 2: winget (Quick Install)](#option-2-winget-quick-install)
  - [Verify Installation](#verify-installation)
  - [Configure Git to Use Gpg4win](#configure-git-to-use-gpg4win)
- [Understanding Dual GPG Installations on Windows](#understanding-dual-gpg-installations-on-windows)
  - [Two GPG Installations](#two-gpg-installations)
  - [Why This Matters](#why-this-matters)
  - [Verify Which GPG Git Is Using](#verify-which-gpg-git-is-using)
  - [Recommendation: Use Gpg4win](#recommendation-use-gpg4win)
  - [Verification Commands](#verification-commands)
  - [Switching Between GPG Installations](#switching-between-gpg-installations)
  - [Dynamic GPG Detection for Troubleshooting](#dynamic-gpg-detection-for-troubleshooting)
- [Understanding Git Bash Paths on Windows](#understanding-git-bash-paths-on-windows)
  - [Common Path Mappings](#common-path-mappings)
  - [Important Security Considerations](#important-security-considerations)
  - [Path Conversion Utility: cygpath](#path-conversion-utility-cygpath)
- [GPG Key Generation on Windows](#gpg-key-generation-on-windows)
  - [Using Command Line (Recommended)](#using-command-line-recommended)
  - [Using Kleopatra (GUI)](#using-kleopatra-gui)
- [Windows-Specific Configuration](#windows-specific-configuration)
  - [GPG Home Directory Permissions](#gpg-home-directory-permissions)
  - [Pinentry Configuration (REQUIRED for Reliable Caching)](#pinentry-configuration-required-for-reliable-caching)
  - [Environment Variables](#environment-variables)
  - [GPG Agent Startup on Windows: Official Design vs. Practical Reality](#gpg-agent-startup-on-windows-official-design-vs-practical-reality)
- [Common Windows Issues](#common-windows-issues)
  - [gpg: cannot open tty 'no tty': No such file or directory](#gpg-cannot-open-tty-no-tty-no-such-file-or-directory)
  - [gpg: signing failed: Screen or window too small](#gpg-signing-failed-screen-or-window-too-small)
  - [Passphrase Caching Not Working (Prompted Every Commit)](#passphrase-caching-not-working-prompted-every-commit)
  - [Windows Firewall Blocking GPG Agent](#windows-firewall-blocking-gpg-agent)
  - [GPG Keys Not Persisting After Reboot](#gpg-keys-not-persisting-after-reboot)
- [Windows-Specific Security Considerations](#windows-specific-security-considerations)
  - [BitLocker Disk Encryption](#bitlocker-disk-encryption)
  - [Windows Defender Antivirus](#windows-defender-antivirus)
  - [Temporary File Cleanup](#temporary-file-cleanup)
- [Integration with Git GUI Tools](#integration-with-git-gui-tools)
  - [GitKraken](#gitkraken)
  - [GitHub Desktop](#github-desktop)
  - [VS Code](#vs-code)
- [Verification and Testing](#verification-and-testing)
  - [Test GPG Installation](#test-gpg-installation)
  - [Verify Paths](#verify-paths)
- [Official Documentation](#official-documentation)
- [Last Verified](#last-verified)

## Gpg4win Installation

### Option 1: Official Installer (Recommended for Control)

Download the official [Gpg4win](https://gpg4win.org/thanks-for-download.html) installer.

The installer provides:

- Gpg4win components (GnuPG, Kleopatra certificate manager)
- GUI key management tools
- Documentation and guides
- Integration with Windows shell

### Option 2: winget (Quick Install)

```powershell
winget install --id GnuPG.Gpg4win -e --source winget
```

**Note:** winget uses default settings (no wizard).

### Verify Installation

```powershell
# Check GPG installation
where.exe gpg
# Expected: C:\Program Files (x86)\GnuPG\bin\gpg.exe

# Check version
gpg --version
```

### Configure Git to Use Gpg4win

```powershell
# Set GPG program path in Git configuration
git config --global gpg.program "C:/Program Files (x86)/GnuPG/bin/gpg.exe"

# Verify configuration
git config --global gpg.program
```

## Understanding Dual GPG Installations on Windows

**CRITICAL:** Windows systems typically have **two separate GPG installations**, each with its own keyring and configuration file location. Understanding this is essential for successful GPG setup.

### Two GPG Installations

#### 1. Gpg4win (Recommended)

- **Location:** `C:\Program Files (x86)\GnuPG\`
- **Keyring directory:** `%APPDATA%\gnupg\` (typically `C:\Users\<Username>\AppData\Roaming\gnupg\`)
- **Config file:** `%APPDATA%\gnupg\gpg-agent.conf`
- **Purpose:** Standalone Windows GPG installation with GUI tools (Kleopatra)
- **Recommended for:** Windows users, official Windows GPG distribution

#### 2. Git Bash GPG (Bundled with Git for Windows)

- **Location:** `/usr/bin/gpg` (in Git Bash), typically `C:\Program Files\Git\usr\bin\gpg.exe`
- **Keyring directory:** `~/.gnupg/` (Git Bash home), resolves to `C:\Users\<Username>\.gnupg\`
- **Config file:** `~/.gnupg/gpg-agent.conf` → `C:\Users\<Username>\.gnupg\gpg-agent.conf`
- **Purpose:** Bundled GPG for Git Bash Unix-like environment
- **Not recommended for:** Git commit signing (use Gpg4win instead)

### Why This Matters

**Each GPG installation maintains:**

- ✅ **Separate keyring** - Keys generated in one are NOT available in the other
- ✅ **Separate config directory** - Configuration files must be in the correct location
- ✅ **Independent GPG agent** - Each runs its own passphrase cache

**Common Problem:**

Users generate keys and configure passphrase caching in **Git Bash GPG** (`~/.gnupg/`), but Git is configured to use **Gpg4win** (`%APPDATA%\gnupg\`). Result:

- ❌ Keys "not found" when signing commits
- ❌ Passphrase caching configuration ignored
- ❌ Confusion about which GPG is being used

### Verify Which GPG Git Is Using

```bash
# Check Git's GPG configuration
git config --global gpg.program

# Possible outputs:

# 1. Gpg4win (recommended, explicit path):
# "C:/Program Files (x86)/GnuPG/bin/gpg.exe"
# → Keys in: %APPDATA%\gnupg\
# → Config in: %APPDATA%\gnupg\gpg-agent.conf

# 2. Git Bash GPG (blank or /usr/bin/gpg):
# Blank output or "/usr/bin/gpg"
# → Keys in: C:\Users\<Username>\.gnupg\
# → Config in: C:\Users\<Username>\.gnupg\gpg-agent.conf

# 3. Verify config directory location
gpgconf --list-dirs homedir
# This shows which directory the active GPG is using
```

### Recommendation: Use Gpg4win

**We recommend configuring Git to use Gpg4win explicitly:**

```bash
# Set GPG program to Gpg4win
git config --global gpg.program "C:/Program Files (x86)/GnuPG/bin/gpg.exe"
```

**Why Gpg4win is recommended:**

- ✅ Official Windows GPG distribution
- ✅ Includes GUI key management (Kleopatra)
- ✅ Standard Windows installation location (`%APPDATA%`)
- ✅ Better Windows integration (pinentry, agent autostart)
- ✅ Separate from Git Bash environment (cleaner separation)

**When you might use Git Bash GPG:**

- You want Unix-style GPG environment
- You use Git Bash exclusively for development
- You need keys isolated from Windows system

### Verification Commands

```bash
# Verify which GPG is in PATH
where.exe gpg
# Shows ALL GPG installations on system

# List keys in active GPG
gpg --list-secret-keys --keyid-format=long
# Shows keys available to the active GPG

# Check config directory
gpgconf --list-dirs homedir
# Shows where the active GPG looks for config/keys

# Verify Git's GPG setting
git config --global gpg.program
# Shows which GPG Git will use for signing
```

### Switching Between GPG Installations

**If you need to switch from Git Bash GPG to Gpg4win:**

```bash
# 1. Export keys from Git Bash GPG
gpg --list-secret-keys --keyid-format=long
# Note your KEY_ID

gpg --armor --export-secret-keys <KEY_ID> > /tmp/my-key.asc

# 2. Configure Git to use Gpg4win
git config --global gpg.program "C:/Program Files (x86)/GnuPG/bin/gpg.exe"

# 3. Import keys into Gpg4win
"C:/Program Files (x86)/GnuPG/bin/gpg.exe" --import /tmp/my-key.asc

# 4. Verify keys imported
"C:/Program Files (x86)/GnuPG/bin/gpg.exe" --list-secret-keys --keyid-format=long

# 5. Delete temporary key file (SECURITY)
rm -f /tmp/my-key.asc
```

**If you generated keys in the wrong GPG and want to start fresh:**

```bash
# Generate new key in Gpg4win
"C:/Program Files (x86)/GnuPG/bin/gpg.exe" --full-generate-key

# Configure Git
git config --global user.signingkey <NEW_KEY_ID>
git config --global commit.gpgsign true

# Add new key to GitHub
"C:/Program Files (x86)/GnuPG/bin/gpg.exe" --armor --export <NEW_KEY_ID>
```

### Dynamic GPG Detection for Troubleshooting

**Problem Statement:**

When troubleshooting GPG signing issues (especially daemon startup problems), a common mistake is launching GPG agents or checking keys from the WRONG GPG installation. This leads to:

- Launching keyboxd from Git Bash GPG when Git uses Gpg4win
- Checking keys in one installation when Git uses the other
- Configuration changes in the wrong GPG's config directory

#### Solution: Always Detect Git's GPG Configuration First

**Step-by-Step Dynamic Detection Workflow:**

##### Step 1: Determine which GPG Git is using

```bash
# Check Git's configured GPG
git config --get gpg.program

# Possible outputs:
# <gpg4win-path>/bin/gpg.exe  → Git uses Gpg4win
# /usr/bin/gpg                 → Git uses Git Bash GPG
# (no output)                  → Git uses system PATH
```

##### Step 2: Extract the GPG binary path and directory

```bash
# If output was a full path (Gpg4win example):
GPG_PATH=$(git config --get gpg.program)

# If no output (using PATH):
GPG_PATH=$(where.exe gpg | head -1)

# Extract directory path
GPG_DIR=$(dirname "$GPG_PATH")
```

##### Step 3: Use that EXACT GPG for all operations

```bash
# Launch keyboxd from the CORRECT installation
"${GPG_DIR}/gpgconf.exe" --launch keyboxd

# List keys from the CORRECT installation
"${GPG_DIR}/gpg.exe" --list-secret-keys --keyid-format=long

# Check config directory for CORRECT installation
"${GPG_DIR}/gpgconf.exe" --list-dirs homedir
```

#### Concrete Example (Git uses Gpg4win)

```bash
# 1. Check Git's GPG configuration
$ git config --get gpg.program
<gpg4win-path>/bin/gpg.exe

# 2. Set variable for reuse
$ GPG_PATH=$(git config --get gpg.program)
$ GPG_DIR=$(dirname "$GPG_PATH")

# 3. Launch keyboxd from THAT GPG
$ "${GPG_DIR}/gpgconf.exe" --launch keyboxd

# 4. Verify agent started
$ "${GPG_DIR}/gpgconf.exe" --list-components | grep keyboxd
keyboxd:GnuPG Key Storage:<gpg-dir>/keyboxd.exe

# 5. List keys from THAT GPG
$ "${GPG_DIR}/gpg.exe" --list-secret-keys --keyid-format=long
sec   ed25519/ABC123... 2025-01-01 [SC]
      Fingerprint...
uid           [ultimate] Your Name <your.email@example.com>
ssb   cv25519/DEF456... 2025-01-01 [E]

# 6. Check config directory for THAT GPG
$ "${GPG_DIR}/gpgconf.exe" --list-dirs homedir
<user-appdata>/gnupg
```

#### Common Mistakes to Avoid

1. ❌ **Running commands without checking Git's config first**
   - Assuming Git uses the GPG in PATH
   - Using Gpg4win commands when Git uses Git Bash GPG (or vice versa)

2. ❌ **Hardcoding GPG paths in troubleshooting scripts**
   - Brittle: `gpgconf --launch keyboxd` (uses PATH, may be wrong)
   - Robust: Check `git config --get gpg.program` first, then use that GPG

3. ❌ **Mixing GPG installations in single troubleshooting session**
   - Launching keyboxd from Gpg4win, then checking keys in Git Bash GPG
   - Configuration changes in one installation won't affect the other

#### Quick Reference Commands

**For Scripting (Recommended):**

```bash
# Detect and use Git's configured GPG
GPG_PATH=$(git config --get gpg.program)
if [ -z "$GPG_PATH" ]; then
    # Fall back to PATH if no explicit config
    GPG_PATH=$(where.exe gpg | head -1)
fi
GPG_DIR=$(dirname "$GPG_PATH")

# Now use ${GPG_DIR} for all operations
"${GPG_DIR}/gpgconf.exe" --launch keyboxd
"${GPG_DIR}/gpg.exe" --list-secret-keys
"${GPG_DIR}/gpgconf.exe" --list-dirs homedir
```

**For Manual Troubleshooting:**

```bash
# 1. Identify Git's GPG
git config --get gpg.program

# 2. If Gpg4win (example output: <gpg4win-path>/bin/gpg.exe):
#    Use full paths to Gpg4win's gpgconf/gpg executables

# 3. If Git Bash GPG (example output: /usr/bin/gpg or no output):
#    Use system PATH (gpgconf, gpg commands directly)
```

## Understanding Git Bash Paths on Windows

Git Bash provides a Unix-like environment on Windows with Unix-style path conventions. Understanding path mappings is essential when working with temporary files, scripts, and GPG keys.

### Common Path Mappings

| Git Bash Path | Windows Path | Description |
| --- | --- | --- |
| `/tmp/` | `C:\Users\YourUsername\AppData\Local\Temp\` | Temporary files directory |
| `/c/` | `C:\` | C: drive root |
| `/d/` | `D:\` | D: drive root |
| `~` | `C:\Users\YourUsername\` | User home directory |
| `/usr/bin/` | `C:\Program Files\Git\usr\bin\` | Git Bash binaries |
| `~/.gnupg/` | `C:\Users\YourUsername\.gnupg\` | GPG configuration and keyring |

### Important Security Considerations

**Temporary Files in `/tmp/`:**

- ✅ **Safe to clean:** Windows Disk Cleanup can safely remove these files
- ⚠️ **Not truly temporary:** Files persist until manually deleted or cleaned by Windows
- 🔒 **Security risk:** Sensitive files (like private keys) should be deleted explicitly

**Best practices for temporary GPG files:**

```bash
# After securing key elsewhere (GitHub Secrets, encrypted vault)
rm -f /tmp/private-key.asc

# Verify deletion
ls -lah /tmp/ | grep private-key
# Should return nothing
```

### Path Conversion Utility: `cygpath`

Git Bash includes `cygpath` for converting between Unix and Windows paths:

```bash
# Convert Unix path to Windows path
cygpath -w /tmp/
# Output: C:\Users\YourUsername\AppData\Local\Temp

# Convert Windows path to Unix path
cygpath -u "C:\Program Files\Git"
# Output: /c/Program Files/Git

# Get absolute Windows path of current directory
cygpath -wa .
```

**Common use cases:**

1. **Finding where temp files are stored:**

   ```bash
   # List files in Unix format
   ls /tmp/

   # Get Windows location for Explorer
   cygpath -w /tmp/
   ```

2. **Passing paths to Windows applications:**

   ```bash
   # Correct - Convert to Windows path first
   notepad.exe $(cygpath -w ~/file.txt)

   # Wrong - Windows app won't understand Unix paths
   notepad.exe ~/file.txt
   ```

3. **Debugging script output locations:**

   ```bash
   echo "File created at: $(cygpath -w $OUTPUT_FILE)"
   ```

## GPG Key Generation on Windows

### Using Command Line (Recommended)

```bash
# Generate key interactively
gpg --full-generate-key

# Follow prompts:
# 1. Key type: (9) ECC (sign and encrypt) *default*
# 2. Curve: (1) Curve 25519 *default*
# 3. Expiration: 0 = no expiration
# 4. Real name: Your Name
# 5. Email: your.verified@email.com
# 6. Passphrase: Strong 20+ characters

# List keys to get KEY_ID
gpg --list-secret-keys --keyid-format=long
```

### Using Kleopatra (GUI)

Kleopatra is installed with Gpg4win and provides a graphical interface:

1. Open Kleopatra from Start Menu
2. File → New OpenPGP Key Pair
3. Enter Name and Email
4. Advanced Settings:
   - Key Material: Ed25519 (Curve 25519)
   - Expiration: No expiration (or set date)
   - Passphrase: Required
5. Create
6. Export public key → Add to GitHub

## Windows-Specific Configuration

### GPG Home Directory Permissions

**Location:** `C:\Users\<Username>\.gnupg\`

**Security warning:** If you see "unsafe permissions on homedir":

1. Right-click `.gnupg` folder → Properties → Security
2. Click "Advanced" → "Disable inheritance"
3. Remove all users except your account
4. Ensure your account has "Full Control"
5. Apply changes

### Pinentry Configuration (REQUIRED for Reliable Caching)

Pinentry is the tool that prompts for your GPG passphrase. On Windows, explicitly configuring the pinentry program is **REQUIRED** for reliable passphrase caching.

**Why this is required:**

- Without explicit `pinentry-program` configuration, GPG may fail to cache passphrases properly
- Leads to passphrase prompts on every commit, even with correct cache TTL settings
- Windows GPG agent needs explicit pinentry path for reliable operation

**Recommended configuration:**

```bash
# For Gpg4win users (most Windows users)
# Add to %APPDATA%\gnupg\gpg-agent.conf
cat >> "$APPDATA/gnupg/gpg-agent.conf" << 'EOF'
# REQUIRED for Windows: Specify pinentry program for reliable caching
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
EOF

# Restart agent to apply changes
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**For Git Bash GPG users (rare):**

```bash
# Add to ~/.gnupg/gpg-agent.conf
cat >> ~/.gnupg/gpg-agent.conf << 'EOF'
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
EOF

# Restart agent
gpgconf --kill gpg-agent
```

**Available pinentry programs:**

- `pinentry-basic.exe` - Simple GUI dialog (recommended, default)
- `pinentry-w32.exe` - Windows native dialog
- `pinentry-qt.exe` - Qt-based GUI (if Qt installed)
- `pinentry.exe` - Automatic selection (may cause issues)

**Verify configuration loaded:**

```bash
# Check if pinentry-program is configured
gpgconf --list-options gpg-agent | grep pinentry

# Test passphrase caching
git commit --allow-empty -m "Test 1"  # Will prompt
git commit --allow-empty -m "Test 2"  # Should NOT prompt if caching works
```

### Environment Variables

**GPG_TTY (for Git Bash/WSL):**

```bash
# Add to ~/.bashrc
export GPG_TTY=$(tty)

# Or set for current session
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
source ~/.bashrc
```

### GPG Agent Startup on Windows: Official Design vs. Practical Reality

**Understanding the Gap Between Design and Reality:**

GnuPG agents (gpg-agent and keyboxd) are officially designed for automatic on-demand startup, but Windows 11 frequently exhibits startup failures due to race conditions and daemon initialization issues.

#### Official Design (What SHOULD Happen)

**Automatic On-Demand Startup:**

- GnuPG agents designed to start automatically when needed
- Official GnuPG documentation states: "no reason to start manually"
- Agents launch when GPG tools (like Git) attempt to use them
- Should work transparently without user intervention

**Why This Design Makes Sense:**

- Reduces system resource usage (agents only run when needed)
- Simplifies user experience (no manual configuration)
- Works well on Linux and macOS systems
- Provides clean integration with desktop environments

#### Windows Reality (What ACTUALLY Happens)

**Known Issues:**

1. **Cold Boot Connection Failures:**
   - **Bug T7777**: "Gpg4win fails to connect to keyboxd on a cold boot"
   - Affects GPG4win 4.4.1 and 5.0 beta
   - First operation after Windows reboot fails with 30-60 second hang
   - Subsequent attempts usually succeed

2. **Root Cause:**
   - **Bug T7829**: "w32: daemon startup and connection race when socket file already exists"
   - Race condition during daemon startup on Windows
   - **Status**: FIXED in master branch (commit rGae431b04370f)
   - Will be included in upcoming GPG4win stable releases

3. **Symptoms:**
   - `error: gpg failed to sign the data`
   - `can't connect to keyboxd` errors
   - 30-60 second timeout on first commit after reboot
   - Intermittent failures requiring retries

#### Recommended Approach

##### Primary Strategy: Rely on Official Design

Trust the automatic on-demand startup (official design) as the first line of defense:

```bash
# Let GPG handle agent startup automatically
git commit -m "message"

# If failure occurs, retry immediately
git commit -m "message"  # Second attempt usually succeeds
```

**Why This Works:**

- Aligns with official GnuPG design
- Avoids workarounds that may cause conflicts
- Future GPG4win releases will improve reliability (T7829 fix)
- Simplest approach with minimal configuration

**If Cold Boot Issues Persist:**

When automatic startup fails consistently, use these lightweight workarounds:

1. **Option A: Open Kleopatra before first commit**
   - Launches Kleopatra GUI (Start menu → Kleopatra)
   - Triggers agent startup as side effect
   - No configuration changes needed
   - Works reliably, GUI-friendly

2. **Option B: Manual agent launch (command-line)**
   - Detect Git's GPG: `git config --get gpg.program`
   - Launch keyboxd from that GPG's directory
   - Example: `"<gpg-dir>/gpgconf.exe" --launch keyboxd`
   - See [Dynamic GPG Detection](#dynamic-gpg-detection-for-troubleshooting) for details

3. **Option C: Retry on failure**
   - If first commit fails with agent error, retry immediately
   - Second attempt usually succeeds (agent is now running)
   - No configuration needed
   - Good for occasional failures

#### Cache Duration Configuration

**Improve user experience** by reducing how often passphrase prompts occur:

**Via Kleopatra GUI (Recommended for Windows Users):**

1. Open Kleopatra (Start menu → Kleopatra)
2. Settings → Configure Kleopatra → GnuPG System → Private Keys
3. Set cache timeouts:
   - **Default cache TTL**: 28800 seconds (8 hours)
   - **Maximum cache TTL**: 86400 seconds (24 hours)
4. Click OK, restart GPG agent

**Via gpg-agent.conf (Advanced Users):**

Edit `<user-appdata>/gnupg/gpg-agent.conf`:

```conf
# Cache passphrase for 8 hours of inactivity
default-cache-ttl 28800

# Maximum cache time of 24 hours regardless of use
max-cache-ttl 86400
```

Restart agent to apply:

```bash
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**CRITICAL:** Ensure you're editing the config file for the CORRECT GPG installation. See [Dual GPG Installations](#understanding-dual-gpg-installations-on-windows) for details.

#### Task Scheduler Startup (Last Resort Only)

**NOT Officially Recommended** - Use only for severe persistent problems:

**Why NOT Recommended:**

- Conflicts with official automatic startup design
- May cause permission issues or race conditions
- Bypasses official daemon management
- Creates maintenance burden (scripts to manage)
- Future GPG4win releases may break this approach

**When to Consider:**

- Cold boot issues occur on EVERY reboot
- Options A/B/C above do not resolve the problem
- You need guaranteed agent availability at login
- Willing to accept maintenance overhead

**Implementation (If Absolutely Necessary):**

Create Task Scheduler task to launch keyboxd at login:

1. Open Task Scheduler (Start → Task Scheduler)
2. Create Basic Task → Name: "GPG Agent Startup"
3. Trigger: "When I log on"
4. Action: "Start a program"
5. Program: `<gpg-dir>/gpgconf.exe`
6. Arguments: `--launch keyboxd`
7. Finish, test by rebooting

**IMPORTANT:** Replace `<gpg-dir>` with actual GPG installation path detected from `git config --get gpg.program`.

#### Future Outlook

**Good News:**

- T7829 fix merged to GnuPG master branch (commit rGae431b04370f)
- Will be included in upcoming GPG4win stable releases
- Should significantly improve Windows reliability
- Official automatic startup will work more reliably

**What This Means:**

- Current workarounds are temporary
- Future releases may not need manual intervention
- Aligning with official design (automatic startup) is forward-compatible
- Task Scheduler scripts may become unnecessary

## Common Windows Issues

### "gpg: cannot open tty 'no tty': No such file or directory"

**Cause:** GPG can't find terminal for passphrase prompt.

**Solution:**

```bash
# Set GPG_TTY
export GPG_TTY=$(tty)

# Or use GUI pinentry
echo "pinentry-program \"C:\\Program Files (x86)\\GnuPG\\bin\\pinentry-w32.exe\"" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

### "gpg: signing failed: Screen or window too small"

**Cause:** Terminal window too small for pinentry curses interface.

**Solution:**

Use GUI pinentry instead:

```bash
echo "pinentry-program \"C:\\Program Files (x86)\\GnuPG\\bin\\pinentry-w32.exe\"" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

### Passphrase Caching Not Working (Prompted Every Commit)

**Symptom:** You configured `gpg-agent.conf` with cache settings but are still prompted for your passphrase on every commit.

**Root Cause:** This is almost always caused by configuring the **wrong config file location** due to Windows' dual GPG installation issue.

**Diagnosis:**

```bash
# 1. Verify which GPG Git is using
git config --global gpg.program

# 2. Check GPG's actual config directory
gpgconf --list-dirs homedir

# 3. Check if config file exists at correct location
# For Gpg4win (if Git uses C:/Program Files (x86)/GnuPG/bin/gpg.exe):
ls "$APPDATA/gnupg/gpg-agent.conf"

# For Git Bash GPG (if Git uses /usr/bin/gpg or blank):
ls ~/.gnupg/gpg-agent.conf

# 4. Verify cache settings are loaded
gpgconf --list-options gpg-agent | grep cache-ttl
# Should show your configured values (e.g., 28800 for 8 hours)
```

#### Solution 1: Create Config in Correct Location (Most Common)

If `git config --global gpg.program` shows `C:/Program Files (x86)/GnuPG/bin/gpg.exe` (Gpg4win):

```bash
# Create/edit config at Gpg4win location
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
# Should show: default-cache-ttl:24:0:... 28800

# Test caching
git commit --allow-empty -m "Test 1"  # Will prompt
git commit --allow-empty -m "Test 2"  # Should NOT prompt
```

#### Solution 2: Missing pinentry-program Line

Even with correct config location, caching may fail without `pinentry-program`:

```bash
# Add pinentry-program to your config
echo "pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe" >> "$APPDATA/gnupg/gpg-agent.conf"

# Restart agent
gpgconf --kill gpg-agent
```

#### Solution 3: Multiple GPG Agents Running

```bash
# Kill all GPG agents
taskkill /F /IM gpg-agent.exe

# Launch single agent
gpgconf --launch gpg-agent
```

**Verification:**

After applying solution, verify caching works:

```bash
# First commit will prompt for passphrase
git commit --allow-empty -m "Cache test 1"

# Second commit should NOT prompt (uses cached passphrase)
git commit --allow-empty -m "Cache test 2"

# If still prompting, check config is loaded
gpgconf --list-options gpg-agent | grep -E "(cache-ttl|pinentry)"
```

**See also:** [Passphrase Caching Reference](passphrase-caching.md) for detailed cache configuration guidance.

### Windows Firewall Blocking GPG Agent

**Symptoms:** GPG agent won't start or can't communicate.

**Solution:**

1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Add: `C:\Program Files (x86)\GnuPG\bin\gpg-agent.exe`
4. Allow on Private and Public networks

### GPG Keys Not Persisting After Reboot

**Cause:** Keys stored on temp drive or incorrect keyring location.

**Verify keyring location:**

```bash
# Should be in user home directory
gpgconf --list-dirs homedir
# Expected: C:\Users\<Username>\AppData\Roaming\gnupg
```

**If incorrect, set GNUPGHOME:**

```bash
# Add to environment variables
setx GNUPGHOME "C:\Users\<Username>\.gnupg"
```

## Windows-Specific Security Considerations

### BitLocker Disk Encryption

**Recommended:** Enable BitLocker on drive containing `.gnupg` directory.

- GPG keys at rest are protected by drive encryption
- Passphrase-protected keys add second layer (defense-in-depth)
- Important if laptop is lost or stolen

**Check BitLocker status:**

```powershell
manage-bde -status C:
```

**Enable BitLocker:**

1. Settings → System → Storage → Advanced storage settings
2. Manage BitLocker → Turn on BitLocker
3. Save recovery key securely (NOT with GPG backup)

### Windows Defender Antivirus

**Exclusions for performance:**

Add GPG directories to exclusions:

1. Windows Security → Virus & threat protection → Manage settings
2. Exclusions → Add or remove exclusions
3. Add folder: `C:\Users\<Username>\.gnupg`
4. Add folder: `C:\Program Files (x86)\GnuPG`

**Note:** Only do this if you trust your GPG installation source.

### Temporary File Cleanup

**After exporting sensitive GPG data:**

```bash
# Verify file is secured elsewhere first!

# Delete from /tmp/
rm -f /tmp/private-key.asc

# Verify deletion
ls -lah /tmp/ | grep private-key
# Should return nothing

# Optionally run Disk Cleanup
cleanmgr.exe
```

## Integration with Git GUI Tools

### GitKraken

GitKraken can manage GPG keys automatically:

1. File → Preferences → GPG Preferences
2. Select "Use GPG Signing" → Enable
3. Signing Key → Create or Import
4. GitKraken will handle key generation and Git configuration

**Resources:**

- [GitKraken GPG Signing Guide](https://help.gitkraken.com/gitkraken-desktop/commit-signing-with-gpg/)

### GitHub Desktop

GitHub Desktop does not natively support GPG signing. Use command line or GitKraken instead.

### VS Code

VS Code uses Git's configuration automatically:

- If Git is configured for GPG signing, VS Code will prompt for passphrase
- Ensure GPG agent is running and configured

## Verification and Testing

### Test GPG Installation

```bash
# Test GPG works
echo "test" | gpg --clearsign

# Test key signing
git commit --allow-empty -m "Test GPG signing"

# Verify signature
git log --show-signature -1
```

### Verify Paths

```bash
# Check Git's GPG program path
git config --global gpg.program

# Check GPG keyring location
gpgconf --list-dirs homedir

# Check agent is running
gpgconf --list-components | grep gpg-agent
```

## Official Documentation

- [Gpg4win Official Documentation](https://www.gpg4win.org/documentation.html)
- [GnuPG Windows Install Guide](https://www.gnupg.org/download/index.html#binary)
- [GitHub: Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)

## Last Verified

2025-11-22
