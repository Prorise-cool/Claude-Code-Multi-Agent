# Security Best Practices

Comprehensive security guidance for GPG commit signing, covering passphrase protection, key expiration strategies, and backup procedures.

## Table of Contents

- [Passphrase Protection](#passphrase-protection)
- [Key Expiration](#key-expiration)
- [Backup Strategy](#backup-strategy)

## Passphrase Protection

**Recommended:**

- ✅ Use passphrase protection on personal keys (defense-in-depth)
- ✅ Minimum 20 characters, use Diceware or password manager
- ✅ Configure caching to balance security and convenience (4-8 hours)
- ✅ Lock screen when away (Windows + L, Cmd+Ctrl+Q, Ctrl+Alt+L)

## Key Expiration

**With expiration (enterprise best practice):**

- ✅ Time-bound compromise window (limits damage)
- ✅ Forces periodic key review and rotation
- ⚠️ Requires maintenance (extend or rotate before expiry)

**Without expiration (GitHub default):**

- ✅ Set and forget (no maintenance burden)
- ✅ Old commits stay verified indefinitely
- ⚠️ Indefinite validity if compromised (until manually revoked)

**Recommendation:** No expiration for personal projects, 1-year expiration for client/enterprise work.

## Backup Strategy

**What to backup:**

- ✅ Private key (encrypted)
- ✅ Revocation certificate (separate from key)
- ✅ Passphrase (in password manager, not with backup)

**Secure backup locations:**

- ✅ Encrypted vault (VeraCrypt, Cryptomator)
- ✅ Password manager (1Password, Bitwarden) - Secure Documents
- ✅ Hardware encrypted USB drive (in safe)
- ❌ NOT: Unencrypted cloud storage, Git repos, email attachments

**Backup procedure:**

```bash
# Export private key
gpg --armor --export-secret-keys <KEY_ID> > gpg-backup.asc

# Encrypt backup
gpg --symmetric --cipher-algo AES256 gpg-backup.asc

# Result: gpg-backup.asc.gpg (encrypted)
# Store in secure location (NOT in Git repo!)

# Delete unencrypted file
rm gpg-backup.asc
```

**⚠️ Important:** Encrypting your backup with GPG creates a circular dependency - if you lose your GPG key, you can't decrypt the backup. Consider additional backup methods:

- Store unencrypted key in password manager's Secure Documents (1Password, Bitwarden)
- Use hardware encrypted USB drive stored in physical safe
- Print paper backup and store in safe deposit box (for critical keys)

## Last Verified

2025-11-17
