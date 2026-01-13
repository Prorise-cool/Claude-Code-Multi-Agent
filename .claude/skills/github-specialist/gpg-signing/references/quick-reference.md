# GPG Signing Quick Reference

Quick lookup for common GPG and Git signing commands.

## Table of Contents

- [Key Generation](#key-generation)
- [Key Management](#key-management)
- [Git Configuration](#git-configuration)
- [Testing and Verification](#testing-and-verification)
- [Agent Management](#agent-management)

## Key Generation

```bash
# Generate key interactively
gpg --full-generate-key

# Generate key non-interactively (batch mode)
# See GnuPG docs for batch-key-generation protocol
```

## Key Management

```bash
# List secret keys
gpg --list-secret-keys --keyid-format=long

# List public keys
gpg --list-keys --keyid-format=long

# Export public key (for GitHub/GitLab/etc)
gpg --armor --export <KEY_ID>

# Export private key (for backup - KEEP SECURE!)
gpg --armor --export-secret-keys <KEY_ID>
```

## Git Configuration

```bash
# Configure signing key globally
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgSign true

# Configure signing key for specific repository
cd /path/to/repo
git config user.signingkey <KEY_ID>
git config commit.gpgsign true

# Verify Git configuration
git config --global user.signingkey
```

## Testing and Verification

```bash
# Test GPG signing directly
echo "test" | gpg --clearsign

# Create test commit with signature
git commit --allow-empty -m "Test GPG signing"

# Verify commit signature
git log --show-signature -1

# Show signature for all commits
git log --show-signature --oneline
```

## Agent Management

```bash
# Restart GPG agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent

# Check agent status
gpgconf --list-components

# List configured directories
gpgconf --list-dirs

# Check cache TTL settings
gpgconf --list-options gpg-agent | grep cache-ttl
```

## Related References

- [Passphrase Caching Configuration](passphrase-caching.md) - Cache strategies and security
- [Windows Setup Guide](windows-setup.md) - Gpg4win specifics
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Security Best Practices](security-best-practices.md) - Key expiration, backups, etc.

**Last Verified**: 2025-11-19
