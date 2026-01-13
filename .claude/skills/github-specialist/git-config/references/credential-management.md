# Git Credential Management

Comprehensive guide to Git credential helpers, authentication methods, and credential management workflows.

## Table of Contents

- [Overview: How Git Credentials Work](#overview-how-git-credentials-work)
- [Credential Helper Options](#credential-helper-options)
  - [1. Windows Credential Manager (OS Default)](#1-windows-credential-manager-os-default)
  - [2. GitHub CLI as Credential Helper](#2-github-cli-as-credential-helper)
- [Hybrid Approach (Recommended for GitHub Users)](#hybrid-approach-recommended-for-github-users)
- [Checking Your Current Configuration](#checking-your-current-configuration)
- [Switching Between Credential Helpers](#switching-between-credential-helpers)
  - [Switch to GitHub CLI for GitHub (Hybrid Setup)](#switch-to-github-cli-for-github-hybrid-setup)
  - [Revert to Windows Credential Manager Only (Remove gh CLI)](#revert-to-windows-credential-manager-only-remove-gh-cli)
- [Managing GitHub CLI Credentials](#managing-github-cli-credentials)
  - [View Current Authentication](#view-current-authentication)
  - [Refresh/Add Token Scopes](#refreshadd-token-scopes)
  - [Log Out and Re-authenticate](#log-out-and-re-authenticate)
- [Managing Windows Credential Manager Credentials](#managing-windows-credential-manager-credentials)
  - [View Stored Credentials](#view-stored-credentials)
  - [Delete Cached Credentials](#delete-cached-credentials)
  - [View/Edit via GUI](#viewedit-via-gui)
- [Common Credential Issues](#common-credential-issues)
  - [Issue 1: "refusing to allow an OAuth App to create or update workflow"](#issue-1-refusing-to-allow-an-oauth-app-to-create-or-update-workflow)
  - [Issue 2: Git still uses old/wrong credentials](#issue-2-git-still-uses-oldwrong-credentials)
  - [Issue 3: "fatal: could not read Username"](#issue-3-fatal-could-not-read-username)
  - [Issue 4: SSH vs HTTPS confusion](#issue-4-ssh-vs-https-confusion)
- [Security Best Practices](#security-best-practices)
  - [Token Scope Principle of Least Privilege](#token-scope-principle-of-least-privilege)
  - [Rotate Tokens Periodically](#rotate-tokens-periodically)
  - [Never Commit Credentials](#never-commit-credentials)
- [Quick Reference: Credential Helper Commands](#quick-reference-credential-helper-commands)
- [Recommended Setup for GitHub Users](#recommended-setup-for-github-users)
- [Platform-Specific Notes](#platform-specific-notes)

## Overview: How Git Credentials Work

When you run `git push` or `git clone` with HTTPS URLs, Git needs credentials to authenticate:

1. Git asks the configured **credential helper** for credentials
2. The credential helper returns stored credentials (if available)
3. Git uses those credentials to authenticate with the remote server
4. If authentication succeeds, the credential helper may cache/store them for future use

**Credential helpers are NOT used for SSH URLs** - SSH uses SSH keys managed separately (`~/.ssh/`).

---

## Credential Helper Options

### 1. Windows Credential Manager (OS Default)

**What it is:**

- Built into Windows (no additional software required)
- Stores credentials in Windows Credential Vault (encrypted by Windows)
- Managed via Control Panel → Credential Manager or `cmdkey` command
- Works with all Git hosting providers (GitHub, GitLab, Bitbucket, Azure DevOps, etc.)

**Configuration:**

```bash
# View current credential helper (system default)
git config --get credential.helper
# Output: manager

# Explicitly set Windows Credential Manager as default (usually not needed)
git config --global credential.helper manager
```

**Pros:**

- ✅ OS-native, no dependencies
- ✅ Universal (works with all Git providers)
- ✅ Secure (Windows encrypts credentials)
- ✅ Independent of any CLI tools
- ✅ Familiar to most Windows developers

**Cons:**

- ❌ Manual token management (create PATs in web UI, enter manually)
- ❌ Stale credentials can linger (old tokens remain until explicitly deleted)
- ❌ Harder to update token scopes (must regenerate token and re-enter)
- ❌ No automatic token refresh

**When to use:**

- You work with multiple Git hosting providers (not just GitHub)
- You prefer OS-native tools over CLI dependencies
- You don't need GitHub-specific features (workflow scope, etc.)

---

### 2. GitHub CLI as Credential Helper

**What it is:**

- Uses `gh` CLI to manage GitHub credentials
- `gh` CLI stores OAuth tokens with automatic refresh
- Can be configured as credential helper for GitHub specifically or globally
- Only works for GitHub (not GitLab, Bitbucket, etc.)

**Configuration:**

```bash
# Configure gh CLI as credential helper for GitHub only (recommended)
gh auth setup-git

# This adds to your git config:
# credential.https://github.com.helper=!'C:\Program Files\GitHub CLI\gh.exe' auth git-credential
# credential.https://gist.github.com.helper=!'C:\Program Files\GitHub CLI\gh.exe' auth git-credential
```

**Pros:**

- ✅ Automatic token management (no manual PAT creation)
- ✅ Easy scope updates (`gh auth refresh -s workflow,repo`)
- ✅ Automatic token refresh (OAuth tokens auto-renew)
- ✅ Modern GitHub-recommended approach
- ✅ Integrates with `gh` CLI features

**Cons:**

- ❌ Requires `gh` CLI to be installed
- ❌ Only works for GitHub (not other Git providers)
- ❌ Dependency on external tool (if `gh` breaks, git push breaks)

**When to use:**

- You work primarily/exclusively with GitHub
- You need GitHub Actions workflow scope (for `.github/workflows/` files)
- You prefer automatic token management over manual PATs
- You're already using `gh` CLI for other tasks

---

## Hybrid Approach (Recommended for GitHub Users)

The best approach for GitHub users is a **hybrid setup**:

- GitHub uses `gh` CLI credential helper (automatic token management, workflow scope)
- Everything else uses Windows Credential Manager (universal fallback)

**Setup:**

```bash
# 1. Authenticate with gh CLI (adds workflow scope if needed)
gh auth login --scopes "repo,read:org,admin:public_key,gist,workflow" --git-protocol https

# 2. Configure gh CLI as credential helper for GitHub only
gh auth setup-git

# Result: Hybrid configuration
# - GitHub/Gist → gh CLI (automatic, OAuth, workflow scope)
# - Azure DevOps, GitLab, Bitbucket → Windows Credential Manager
```

**Verify hybrid setup:**

```bash
git config --list | grep -E "credential|helper"

# Expected output:
# credential.helper=manager                                # Global default (Windows)
# credential.https://github.com.helper=!gh auth git-credential    # GitHub-specific (gh CLI)
# credential.https://gist.github.com.helper=!gh auth git-credential  # GitHub Gist (gh CLI)
```

---

## Checking Your Current Configuration

```bash
# View all credential helper configuration
git config --list --show-origin | grep credential

# View just the credential helper
git config --get credential.helper

# View GitHub-specific credential helper
git config --get credential.https://github.com.helper

# Check gh CLI authentication status
gh auth status
```

---

## Switching Between Credential Helpers

### Switch to GitHub CLI for GitHub (Hybrid Setup)

```bash
# Step 1: Authenticate with gh CLI
gh auth login --scopes "repo,read:org,admin:public_key,gist,workflow" --git-protocol https

# Step 2: Configure gh CLI as GitHub credential helper
gh auth setup-git

# Step 3: Verify hybrid setup
git config --list | grep credential
```

### Revert to Windows Credential Manager Only (Remove gh CLI)

```bash
# Remove GitHub-specific credential helpers
git config --global --unset credential.https://github.com.helper
git config --global --unset credential.https://gist.github.com.helper

# Verify Windows Credential Manager is default
git config --get credential.helper
# Output: manager

# Clear cached GitHub credentials from Windows Credential Manager
cmdkey /list | grep github
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

**After reverting:**

- Next `git push` to GitHub will prompt for credentials
- You'll need to create a Personal Access Token at <https://github.com/settings/tokens>
- Select scopes: `repo`, `workflow` (if needed), `read:org`, `gist`
- Enter username and token (NOT password) when prompted
- Windows Credential Manager will cache it

---

## Managing GitHub CLI Credentials

### View Current Authentication

```bash
# Check authentication status
gh auth status

# Output shows:
# - Logged in account
# - Git protocol (ssh or https)
# - Token scopes
```

### Refresh/Add Token Scopes

```bash
# Add workflow scope to existing token
gh auth refresh -h github.com -s repo,workflow

# Re-authenticate with all scopes
gh auth login --scopes "repo,read:org,admin:public_key,gist,workflow" --git-protocol https
```

### Log Out and Re-authenticate

```bash
# Log out of GitHub CLI
gh auth logout

# Re-authenticate (will prompt in browser)
gh auth login --git-protocol https

# Reconfigure as git credential helper
gh auth setup-git
```

---

## Managing Windows Credential Manager Credentials

### View Stored Credentials

```bash
# List all credentials (look for git:https://github.com)
cmdkey /list

# Or using PowerShell (more readable)
cmdkey /list | Select-String -Pattern "github"
```

### Delete Cached Credentials

```bash
# Delete GitHub credentials from Windows Credential Manager
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# Delete specific credential by target name
cmdkey /delete:"git:https://github.com"
```

### View/Edit via GUI

1. Press `Win + R` → type `control /name Microsoft.CredentialManager`
2. Click "Windows Credentials"
3. Find entries starting with `git:https://`
4. Click to view/edit/remove

---

## Common Credential Issues

### Issue 1: "refusing to allow an OAuth App to create or update workflow"

**Cause:** Token lacks `workflow` scope (required for `.github/workflows/` files)

**Solution:**

```bash
# If using gh CLI as credential helper:
gh auth refresh -h github.com -s repo,workflow
gh auth setup-git
git push

# If using Windows Credential Manager:
# 1. Create new PAT with workflow scope: https://github.com/settings/tokens
# 2. Delete old credential: cmdkey /delete:LegacyGeneric:target=git:https://github.com
# 3. Next push will prompt for new token
```

---

### Issue 2: Git still uses old/wrong credentials

**Cause:** Credential cached in Windows Credential Manager even though gh CLI is configured

**Solution:**

```bash
# Clear Windows Credential Manager cache for GitHub
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# Verify gh CLI is configured as GitHub credential helper
git config --get credential.https://github.com.helper

# If not configured, run:
gh auth setup-git

# Try push again
git push
```

---

### Issue 3: "fatal: could not read Username"

**Cause:** No cached credentials, Git needs to prompt but can't (non-interactive)

**Solution:**

```bash
# If using gh CLI: Re-authenticate
gh auth login --git-protocol https
gh auth setup-git

# If using Windows Credential Manager: Manually add credentials
# Next git push will prompt for username/token
# Enter your GitHub username and Personal Access Token (not password)
```

---

### Issue 4: SSH vs HTTPS confusion

**Cause:** Remote URL uses SSH but credential helper is HTTPS-only

**Check remote URL:**

```bash
git remote -v
# SSH format: git@github.com:username/repo.git
# HTTPS format: https://github.com/username/repo.git
```

**Solution:**

```bash
# Switch to HTTPS (if you want to use credential helpers)
git remote set-url origin https://github.com/username/repo.git

# Or switch to SSH (if you have SSH keys configured)
git remote set-url origin git@github.com:username/repo.git
```

---

## Security Best Practices

### Token Scope Principle of Least Privilege

Only grant scopes you actually need:

**Minimal GitHub scopes:**

- `repo` - Access repositories (read/write)
- `read:org` - Read organization membership
- `gist` - Create/edit gists (optional)

**Additional scopes when needed:**

- `workflow` - Required for GitHub Actions (`.github/workflows/`)
- `admin:public_key` - Manage SSH keys via CLI (optional)
- `delete_repo` - Delete repositories (rarely needed)

### Rotate Tokens Periodically

```bash
# GitHub CLI tokens auto-refresh (no manual rotation needed)
gh auth refresh

# Manual PATs: Regenerate every 90 days
# 1. Create new token: https://github.com/settings/tokens
# 2. Delete old credential: cmdkey /delete:LegacyGeneric:target=git:https://github.com
# 3. Next push prompts for new token
```

### Never Commit Credentials

```bash
# Check for accidentally committed secrets
git log -p | grep -E "(password|token|secret|key)"

# If you find exposed credentials:
# 1. Revoke the token immediately (GitHub Settings → Tokens)
# 2. Use git-filter-repo or BFG Repo-Cleaner to remove from history
# 3. Force-push cleaned history (coordinate with team first!)
```

---

## Quick Reference: Credential Helper Commands

```bash
# ===========================
# Checking Configuration
# ===========================

# View all credential configuration
git config --list | grep credential

# View default credential helper
git config --get credential.helper

# View GitHub-specific helper
git config --get credential.https://github.com.helper

# Check gh CLI auth status
gh auth status

# ===========================
# Windows Credential Manager
# ===========================

# List all credentials
cmdkey /list

# Delete GitHub credentials
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# Open Credential Manager GUI
control /name Microsoft.CredentialManager

# ===========================
# GitHub CLI Setup
# ===========================

# Authenticate with gh CLI (includes workflow scope)
gh auth login --scopes "repo,read:org,workflow" --git-protocol https

# Configure gh CLI as credential helper for GitHub
gh auth setup-git

# Refresh/add token scopes
gh auth refresh -h github.com -s repo,workflow

# Log out
gh auth logout

# ===========================
# Reverting to Windows Credential Manager
# ===========================

# Remove gh CLI as GitHub credential helper
git config --global --unset credential.https://github.com.helper
git config --global --unset credential.https://gist.github.com.helper

# Clear cached credentials
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# Next push will prompt for username + PAT
# Create PAT: https://github.com/settings/tokens

# ===========================
# Switching Remote URL Protocol
# ===========================

# View current remote URL
git remote -v

# Switch to HTTPS (for credential helpers)
git remote set-url origin https://github.com/username/repo.git

# Switch to SSH (uses SSH keys, no credential helper)
git remote set-url origin git@github.com:username/repo.git
```

---

## Recommended Setup for GitHub Users

For the best experience with GitHub repositories:

1. **Install and authenticate gh CLI:**

   ```bash
   gh auth login --scopes "repo,read:org,workflow" --git-protocol https
   ```

2. **Configure hybrid credential setup:**

   ```bash
   gh auth setup-git
   ```

3. **Verify configuration:**

   ```bash
   git config --list | grep credential
   # Should show:
   # - credential.helper=manager (default)
   # - credential.https://github.com.helper=!gh auth git-credential (GitHub-specific)
   ```

4. **Test with a push:**

   ```bash
   git push
   # Should work without password prompt (uses gh CLI token)
   ```

**Result:** GitHub uses `gh` CLI (automatic token management, workflow scope), everything else uses Windows Credential Manager.

---

## Platform-Specific Notes

**macOS:**

- Default credential helper: `osxkeychain`
- Storage: macOS Keychain
- GUI access: Keychain Access app
- Same gh CLI setup works for GitHub

**Linux:**

- Default credential helper: `cache` (memory only, temporary)
- Alternative: `libsecret` (persistent storage via GNOME Keyring or KDE Wallet)
- Same gh CLI setup works for GitHub
- May need to install libsecret: `sudo apt install libsecret-1-0 libsecret-1-dev`

---

**Last Updated:** 2025-11-17
