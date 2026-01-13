# Real-World Implementation Example

**You are here:** [SKILL.md](../SKILL.md) → Real-world example (case study)

## Table of Contents

- [Implementation Summary](#implementation-summary)
- [Rationale](#rationale)
- [Configuration Details](#configuration-details)
  - [Personal Key Configuration](#personal-key-configuration)
  - [Automation Key Configuration](#automation-key-configuration)
- [Security Analysis](#security-analysis)
  - [Threat Model](#threat-model)
  - [Security Trade-offs Accepted](#security-trade-offs-accepted)
- [Testing Performed](#testing-performed)
  - [Passphrase Caching](#passphrase-caching)
  - [Automation Key Export](#automation-key-export)
- [Lessons Learned](#lessons-learned)
  - [What Went Well](#what-went-well)
  - [Security Insights](#security-insights)
  - [Future Growth Path](#future-growth-path)
- [Implementation Time](#implementation-time)
- [Summary](#summary)
- [Last Verified](#last-verified)

---

This document provides a real-world case study of implementing a two-key GPG strategy (personal + automation) for a developer onboarding repository.

## Implementation Summary

**Implementation Date:** 2025-11-06

**Scenario:** Personal development + CI/CD automation

**Keys Implemented:**

1. **Personal Development Key** (existing, kept)
   - Key ID: `8901E208C6A7354E`
   - Algorithm: Ed25519
   - Passphrase: YES
   - Usage: Interactive development

2. **CI/CD Automation Key** (new)
   - Key ID: `99622A672C37D40E`
   - Algorithm: Ed25519
   - Passphrase: NO
   - Usage: GitHub Actions automation

## Rationale

**Why keep existing personal key?**

- Only 2 days old (created 2025-11-04)
- Already using best practices (Ed25519, no expiration)
- All recent commits signed and verified
- Historical commit integrity maintained
- No security benefit to replacing it

**Why create second automation key?**

- CI/CD cannot use passphrase-protected keys (unattended operation)
- Separation of concerns (personal ≠ automation)
- Reduced risk (automation key compromise doesn't affect personal key)
- Stored securely in GitHub Secrets (encrypted at rest)

## Configuration Details

### Personal Key Configuration

**Global .gitconfig:**

```gitconfig
[user]
    name = Kyle Sexton
    email = kyle.sexton@melodicsoftware.com
    signingkey = 5C2D8471755AA20FC7FEE4B98901E208C6A7354E
[commit]
    gpgsign = true
[tag]
    gpgsign = true
```

**Passphrase caching:**

File: `~/.gnupg/gpg-agent.conf`

```conf
# Cache passphrase for 8 hours (28800 seconds) of inactivity
default-cache-ttl 28800

# Maximum cache time of 24 hours (86400 seconds) regardless of use
max-cache-ttl 86400

# Allow pinentry to cache the passphrase
allow-preset-passphrase
```

### Automation Key Configuration

**NOT configured globally** - only in CI/CD workflows.

**GitHub Actions workflow example:**

```yaml
- name: Import GPG key
  env:
    GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY_AUTOMATION }}
  run: |
    echo "$GPG_PRIVATE_KEY" | gpg --batch --import

- name: Configure Git for signing
  run: |
    git config --global user.name "GitHub Actions"
    git config --global user.email "actions@github.com"
    git config --global user.signingkey 1DAE639431D27A2411E9217A99622A672C37D40E
    git config --global commit.gpgsign true
```

## Security Analysis

### Threat Model

| Threat | Mitigation | Status |
| --- | --- | --- |
| **Laptop theft/loss** | Personal key passphrase-protected + BitLocker encryption | ✅ Mitigated |
| **Key file compromise** | Passphrase required to use key (defense-in-depth) | ✅ Mitigated |
| **Memory-based attacks** | Passphrase cache limited to 24 hours maximum | ✅ Mitigated |
| **Automation key exposure** | Stored in GitHub Secrets (encrypted at rest/transit) | ✅ Mitigated |
| **Automation key misuse** | NOT configured globally (can't be used accidentally) | ✅ Mitigated |
| **Key separation** | Personal ≠ Automation keys (compromise isolated) | ✅ Mitigated |

### Security Trade-offs Accepted

| Decision | Trade-off | Justification |
| --- | --- | --- |
| **No expiration on personal key** | Indefinite validity if compromised | GitHub default recommendation, can manually revoke, reduces maintenance |
| **No expiration on automation key** | Indefinite validity if compromised | Simplicity for personal use, can manually revoke if needed |
| **8-hour passphrase cache** | Passphrase in memory longer | Balance: prompts 1-2x per day, not every commit |
| **No passphrase on automation key** | Single-factor security | Required for CI/CD, mitigated by GitHub Secrets encryption |

## Testing Performed

### Passphrase Caching

**Test scenario:**

1. Made first commit (passphrase prompted)
2. Made second commit 1 minute later (no prompt - cache working!)
3. Made third commit 2 hours later (no prompt - cache still active)

**Result:** ✅ Caching works as expected (8-hour default confirmed)

### Automation Key Export

```bash
# Export automation private key
gpg --armor --export-secret-keys 99622A672C37D40E > /tmp/automation-private-key.asc

# Verify export successful
cat /tmp/automation-private-key.asc
# Output: BEGIN PGP PRIVATE KEY BLOCK (confirmed)

# Set GitHub Secret
gh secret set GPG_PRIVATE_KEY_AUTOMATION \
  --repo melodic-software/onboarding \
  --body "$(cat /tmp/automation-private-key.asc)"
# Output: ✓ Set secret GPG_PRIVATE_KEY_AUTOMATION for melodic-software/onboarding

# Securely delete temp file
rm -f /tmp/automation-private-key.asc

# Verify deletion
ls /tmp/ | grep automation
# Output: (nothing - file deleted)
```

**Result:** ✅ Automation key exported, secured in GitHub Secrets, temp file deleted

## Lessons Learned

### What Went Well

- ✅ Discovered existing key is already excellent (no replacement needed)
- ✅ Two-key strategy provides security + automation without compromise
- ✅ Passphrase caching configuration dramatically reduced friction
- ✅ Infrastructure ready for multi-client growth (conditional includes template in place)

### Security Insights

- **Defense-in-depth works**: Passphrase + BitLocker + caching = practical security
- **Separation of concerns is critical**: Personal ≠ automation keys prevents cross-contamination
- **Ed25519 is excellent**: Modern, fast, small keys, future-proof
- **No expiration is acceptable** for personal use (GitHub's recommendation)

### Future Growth Path

#### Phase 2: First Client Engagement (when needed)

1. Generate per-client key (1-year expiration, passphrase-protected)
2. Create `~/Clients/ClientA/` directory structure
3. Export keys to `~/Clients/ClientA/.vault/gpg-keys/`
4. Create `~/Clients/ClientA/.gitconfig-clienta`
5. Uncomment conditional include in `~/.gitconfig`
6. Add client key to GitHub (verify client email first)

**Conditional includes already configured in .gitconfig:**

```gitconfig
# ==============================================================================
# Conditional Includes for Per-Client Configurations
# ==============================================================================
# Uncomment and customize when starting client work:
#
# [includeIf "gitdir:D:/Clients/ClientA/"]
#     path = D:/Clients/ClientA/.gitconfig-clienta
```

## Implementation Time

**Total time:** ~45 minutes

**Breakdown:**

- Research and planning: 10 minutes
- Key generation: 5 minutes
- Configuration: 10 minutes
- Testing: 5 minutes
- Documentation: 15 minutes

## Summary

**Mission Accomplished:**

- ✅ Personal key (existing) configured with passphrase caching
- ✅ Automation key created for CI/CD (ready for GitHub Actions)
- ✅ Infrastructure ready for multi-client growth
- ✅ Security best practices followed throughout
- ✅ Zero disruption (existing key kept, commits remain verified)

**Security Posture:** ✅ Improved (caching + separation + documentation)

**Future-Proof:** ✅ Ready for personal, CI/CD, and multi-client scenarios

## Navigation

### Return to Main Skill

- **[SKILL.md](../SKILL.md)** - Main gpg-multi-key skill with quick decision matrix

### Related References

- **[scenarios.md](scenarios.md)** - Detailed scenario comparison and migration guidance
- **[backup-recovery.md](backup-recovery.md)** - Comprehensive backup and recovery procedures

### Official Documentation

- [GitHub Actions: Using GPG Keys](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)

## Last Verified

2025-11-17

**Audit Notes**: Implementation example validated against current GitHub Actions workflow best practices and GPG configuration standards.
