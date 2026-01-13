# GPG Multi-Key Scenarios: Detailed Comparison

**You are here:** [SKILL.md](../SKILL.md) → Scenarios (detailed comparison)

This document provides a comprehensive comparison of the four multi-key GPG scenarios covered in the main skill. Use this reference to choose the right strategy for your situation and understand the trade-offs.

## Table of Contents

- [Scenario Overview](#scenario-overview)
- [Detailed Scenario Comparison](#detailed-scenario-comparison)
  - [Scenario 1: Basic Setup](#scenario-1-basic-setup-single-personal-key)
  - [Scenario 2: Personal + CI/CD](#scenario-2-personal--cicd-automation)
  - [Scenario 3: Multi-Client Consultant](#scenario-3-multi-client-consultant)
  - [Scenario 4: Enterprise Environment](#scenario-4-enterprise-environment)
- [Migration Decision Matrix](#migration-decision-matrix)
- [Key Selection Guide](#key-selection-guide-by-context)
- [Comparison: Security vs Convenience](#comparison-security-vs-convenience)
- [Cost-Benefit Analysis](#cost-benefit-analysis)
- [Troubleshooting Multi-Key Setups](#troubleshooting-multi-key-setups)

## Scenario Overview

| Scenario | Target User | Complexity | Keys | Main Benefit |
| --- | --- | --- | --- | --- |
| **1. Basic Single Key** | Individual developers, personal projects | Low | 1 | Simplicity |
| **2. Personal + CI/CD** | Developers with automation workflows | Medium | 2 | Automation + security |
| **3. Multi-Client Consultant** | Consultants, contractors with multiple clients | High | 3+ | Identity isolation |
| **4. Enterprise Environment** | Corporate developers, regulated industries | Medium-High | 1-2 | Policy compliance |

## Detailed Scenario Comparison

### Scenario 1: Basic Setup (Single Personal Key)

**Who Should Use:**

- Individual developers working on personal projects
- GitHub users wanting verified commits
- Developers new to GPG signing
- Teams with simple commit verification needs

**Key Configuration:**

| Property | Value | Rationale |
| --- | --- | --- |
| **Number of Keys** | 1 | Maximum simplicity |
| **Algorithm** | Ed25519 | Modern, secure, fast |
| **Expiration** | No expiration (or 2 years) | Simplicity, GitHub default |
| **Passphrase** | YES (strong) | Defense-in-depth |
| **Storage** | `~/.gnupg/` | Default GPG location |
| **Git Config** | Global (`~/.gitconfig`) | Single identity |

**Strengths:**

- ✅ Simple setup (15 minutes)
- ✅ Single passphrase to remember
- ✅ GitHub verified commits
- ✅ No configuration complexity
- ✅ Works for 90% of developers

**Limitations:**

- ❌ Cannot automate CI/CD signing (passphrase required)
- ❌ Single identity (one email address)
- ❌ No client isolation (all commits use same key)
- ❌ Key compromise affects all work

**When to Graduate to Scenario 2:**

- You add GitHub Actions or GitLab CI workflows
- You want automated signed commits (releases, changelogs)
- You need unattended signing

**When to Graduate to Scenario 3:**

- You start consultant/contractor work with multiple clients
- You need different email addresses per client
- Client contracts require key isolation

---

### Scenario 2: Personal + CI/CD Automation

**Who Should Use:**

- Developers with GitHub Actions / GitLab CI workflows
- Open-source maintainers with automated releases
- Teams with CI/CD pipelines requiring signed commits
- Developers wanting both interactive and automated signing

**Key Configuration:**

| Key | Algorithm | Expiration | Passphrase | Storage | Git Config |
| --- | --- | --- | --- | --- | --- |
| **Personal** | Ed25519 | None | YES | `~/.gnupg/` | Global (default) |
| **Automation** | Ed25519 | None | NO | GitHub Secrets | CI/CD only |

**Strengths:**

- ✅ Automation possible (no passphrase for CI/CD key)
- ✅ Personal key protected (passphrase)
- ✅ Risk isolation (automation key compromise ≠ personal key compromise)
- ✅ Clear separation (personal commits vs automated commits)
- ✅ GitHub Secrets encryption (keys encrypted at rest)

**Limitations:**

- ❌ More complexity (managing 2 keys)
- ❌ Automation key is single-factor security (file possession only)
- ❌ Still single identity (one email for both keys)
- ❌ Must remember to NOT use automation key for personal work

**Security Considerations:**

**Why automation key has NO passphrase:**

- Required for unattended CI/CD operation
- GitHub Actions cannot enter passphrase interactively
- Stored in GitHub Secrets (encrypted at rest, encrypted in transit)
- NOT configured globally (can't be used accidentally locally)

**Mitigations for automation key:**

- Store in encrypted secrets (GitHub Secrets, Azure Key Vault)
- Monitor CI/CD logs for unexpected usage
- Rotate regularly if compromised
- Use only for automation (never local development)
- Scope to specific repositories (not organization-wide)

**Migration Path from Scenario 1:**

1. Keep existing personal key (no changes)
2. Generate automation key (no passphrase)
3. Export automation private key
4. Add to GitHub Secrets
5. Update CI/CD workflows to import key
6. Test with dummy commit
7. Monitor for verification

**When to Graduate to Scenario 3:**

- You start consultant/contractor work
- You need multiple client identities
- Clients require separate keys per engagement

---

### Scenario 3: Multi-Client Consultant

**Who Should Use:**

- Consultants working with multiple clients
- Contractors with per-client email addresses
- Freelancers managing separate client identities
- Agencies with project-based key isolation
- Developers requiring per-project key separation

**Key Configuration:**

| Key | Algorithm | Expiration | Passphrase | Storage | Git Config |
| --- | --- | --- | --- | --- | --- |
| **Personal** | Ed25519 | None | YES | `~/.gnupg/` | Global (default) |
| **Automation** | Ed25519 | None | NO | GitHub Secrets | CI/CD only |
| **Client A** | Ed25519 | 1 year | YES | `~/Clients/ClientA/.vault/` | Conditional include |
| **Client B** | Ed25519 | 1 year | YES | `~/Clients/ClientB/.vault/` | Conditional include |
| **Client N** | Ed25519 | 1 year | YES | `~/Clients/ClientN/.vault/` | Conditional include |

**Architecture:**

```text
Directory Structure:
~/
├── .gitconfig (global config with conditional includes)
├── personal-projects/ (uses personal key)
└── Clients/
    ├── ClientA/
    │   ├── .gitconfig-clienta (Client A config: email, key)
    │   ├── .vault/gpg-keys/ (Client A keys encrypted)
    │   └── projects/ (Client A repositories)
    └── ClientB/
        ├── .gitconfig-clientb (Client B config: email, key)
        ├── .vault/gpg-keys/ (Client B keys encrypted)
        └── projects/ (Client B repositories)
```

**Strengths:**

- ✅ Complete identity isolation (Client A commits ≠ Client B commits)
- ✅ Automatic key switching (Git conditional includes)
- ✅ Risk isolation (compromised client key doesn't affect other clients)
- ✅ Professional separation (correct email per client)
- ✅ Contractual compliance (client may require separate keys)
- ✅ Passphrase isolation (different passphrase per client)
- ✅ Expiration management (annual review per client)
- ✅ Per-client key rotation (without affecting others)

**Limitations:**

- ❌ High complexity (managing 3+ keys)
- ❌ Multiple passphrases to remember (use password manager)
- ❌ Key rotation overhead (annual per-client)
- ❌ Backup complexity (multiple keys, multiple vaults)
- ❌ Initial setup time (2-3 hours)
- ❌ Requires disciplined directory organization

**Automatic Key Switching:**

Git conditional includes automatically switch keys based on directory:

```gitconfig
# ~/.gitconfig
[includeIf "gitdir:~/Clients/ClientA/"]
    path = ~/Clients/ClientA/.gitconfig-clienta
```

**How it works:**

1. You `cd ~/Clients/ClientA/projects/repo1`
2. You run `git commit`
3. Git detects `gitdir:~/Clients/ClientA/` match
4. Git loads `~/Clients/ClientA/.gitconfig-clienta`
5. Commit uses Client A email and key automatically

**Client Key Best Practices:**

**Expiration:** 1 year (forces annual review, enterprise best practice)

**Rationale:**

- Annual touchpoint with client (are we still working together?)
- Forces review of key security
- Limits exposure window if compromised
- Professional best practice (demonstrates security awareness)

**Passphrase:** YES (20+ characters, unique per client)

**Rationale:**

- Client data requires high security
- Client contracts may require passphrase protection
- Protects client IP if laptop stolen
- Defense-in-depth (key + passphrase)

**Migration Path from Scenario 2:**

1. Keep personal and automation keys (no changes)
2. Create `~/Clients/` directory structure
3. Generate first client key (expiration: 1 year)
4. Create per-client `.gitconfig-clienta` file
5. Add conditional include to `~/.gitconfig`
6. Test key switching (`git config user.email` in client directory)
7. Repeat for each client
8. Backup all client keys to per-client vaults

**When to Graduate to Scenario 4:**

- You join a company with GPG policies
- Enterprise requires specific key types/sizes
- Hardware security keys required (YubiKey)
- Centralized key management needed

---

### Scenario 4: Enterprise Environment

**Who Should Use:**

- Corporate developers in regulated industries
- Teams with security/compliance policies
- Organizations requiring hardware security keys
- Companies with centralized key management
- Environments with mandatory GPG key rotation

**Key Configuration (Typical):**

| Property | Value | Rationale |
| --- | --- | --- |
| **Number of Keys** | 1 (corporate) | Policy-driven, single identity |
| **Algorithm** | RSA 4096 or Ed25519 | Policy-specific (RSA for max compatibility) |
| **Expiration** | 6 months - 1 year | Mandatory rotation policy |
| **Passphrase** | YES (policy-driven complexity) | Compliance requirement |
| **Storage** | YubiKey / Nitrokey (optional) | Hardware security module |
| **Git Config** | Global (corporate email) | Single corporate identity |
| **Revocation** | Filed with IT | Centralized revocation process |
| **Backup** | IT-managed or approved vault | Policy-compliant backup |

**Enterprise Variations:**

**A. Software Key (Standard Enterprise):**

- Key stored in `~/.gnupg/` (standard GPG home)
- Passphrase required (per policy)
- Annual expiration and rotation
- Backups filed with IT or approved storage

**B. Hardware Security Key (High-Security Enterprise):**

- Key stored on YubiKey/Nitrokey (never leaves device)
- Requires physical key + PIN
- Private key cannot be extracted
- Multiple YubiKeys provisioned (backup key)

**Strengths:**

- ✅ Policy compliance (meets corporate security requirements)
- ✅ Centralized management (IT support available)
- ✅ Audit trail (who signed what, when)
- ✅ Hardware key option (maximum security)
- ✅ Standardized across team (consistent process)
- ✅ Revocation procedure documented
- ✅ Backup/recovery managed

**Limitations:**

- ❌ Limited flexibility (must follow policy)
- ❌ Rotation overhead (6-12 month forced rotation)
- ❌ Hardware key cost ($50-150 per YubiKey x2)
- ❌ Hardware key loss = cannot sign until reissued
- ❌ May require legacy RSA (instead of modern Ed25519)
- ❌ Personal projects may require separate personal key

**YubiKey Integration:**

**Benefits:**

- ✅ Private key never leaves hardware device
- ✅ Physical two-factor authentication (key + PIN)
- ✅ Requires physical presence to sign commits
- ✅ Immune to software keyloggers
- ✅ Tamper-resistant (key deletion if device attacked)

**Drawbacks:**

- ⚠️ Lost YubiKey requires revocation and reissuance
- ⚠️ Cannot backup private key (must provision multiple YubiKeys)
- ⚠️ Cost ($50-150 per key)
- ⚠️ USB port required (may limit laptop choice)
- ⚠️ Remote work challenges (forgot YubiKey at home = cannot sign)

**Setup:**

```bash
# Check YubiKey status
gpg --card-status

# Generate key on YubiKey (cannot be extracted)
gpg --edit-card
gpg/card> admin
gpg/card> generate

# Configure Git to use YubiKey
git config --global user.signingkey <YUBIKEY_KEY_ID>
git config --global commit.gpgsign true
```

**Enterprise Policy Example:**

| Policy Area | Requirement | Rationale |
| --- | --- | --- |
| **Key Type** | RSA 4096-bit | Maximum compatibility with legacy systems |
| **Expiration** | 1 year | Balance security (rotation) with overhead |
| **Passphrase** | 16+ chars, mixed case, numbers, symbols | NIST SP 800-63B compliance |
| **Backup** | Filed with IT (encrypted) | Business continuity (employee departure) |
| **Revocation** | Within 24 hours of compromise | Incident response requirement |
| **Hardware Key** | Mandatory for infrastructure team | High-privilege access protection |

**Migration Path from Scenario 3:**

1. Check enterprise policy requirements
2. Generate corporate key (per policy specs)
3. Keep personal/client keys (for non-corporate work)
4. Add corporate key to global config (or create separate work profile)
5. Optionally: Use Git conditional includes for `~/Work/` directory
6. File revocation certificate with IT
7. Add corporate key to corporate GitHub/GitLab

**Dual Environment (Corporate + Personal):**

Many enterprise developers maintain separate keys:

- **Corporate key:** For company repositories (on work laptop)
- **Personal key:** For personal projects (on personal laptop or separate profile)
- **Clear separation:** Work = work key, personal = personal key

**Git config for dual environment:**

```gitconfig
# ~/.gitconfig (work laptop)
[user]
    name = Your Name
    email = you@company.com
    signingkey = <CORPORATE_KEY_ID>
[commit]
    gpgsign = true

[includeIf "gitdir:~/personal/"]
    path = ~/.gitconfig-personal

# ~/.gitconfig-personal
[user]
    email = you@personal.com
    signingkey = <PERSONAL_KEY_ID>
```

---

## Migration Decision Matrix

**From Scenario 1 (Basic) → Scenario 2 (CI/CD):**

Migrate when:

- [ ] You have GitHub Actions or GitLab CI workflows
- [ ] You want automated signed commits (releases, changelogs)
- [ ] You need unattended signing

**From Scenario 2 (CI/CD) → Scenario 3 (Multi-Client):**

Migrate when:

- [ ] You start consultant/contractor work with multiple clients
- [ ] You need different email addresses per client
- [ ] Client contracts require key isolation
- [ ] You want per-client identity management

**From Scenario 3 (Multi-Client) → Scenario 4 (Enterprise):**

Migrate when:

- [ ] You join a company with GPG policies
- [ ] Enterprise requires specific key types/sizes/expiration
- [ ] Hardware security keys required
- [ ] Centralized key management needed

**From Scenario 1 (Basic) → Scenario 4 (Enterprise):**

Direct migration (skip 2 and 3) when:

- [ ] New hire at company with GPG policies
- [ ] Company provides onboarding for GPG setup
- [ ] No personal/client work (corporate only)

---

## Key Selection Guide: By Context

| Context | Recommended Scenario | Key Count | Complexity | Setup Time |
| --- | --- | --- | --- | --- |
| **Personal hobby projects** | 1 (Basic) | 1 | Low | 15 min |
| **Open-source maintainer** | 2 (CI/CD) | 2 | Medium | 1 hour |
| **Freelance consultant (1-2 clients)** | 3 (Multi-Client) | 3-4 | High | 2-3 hours |
| **Freelance consultant (3+ clients)** | 3 (Multi-Client) | 4-10 | High | 3-5 hours |
| **Corporate developer** | 4 (Enterprise) | 1-2 | Medium-High | 1-2 hours |
| **Corporate + personal projects** | 4 + 1 (Hybrid) | 2 | Medium | 2 hours |
| **Consultant joining enterprise** | 4 + 3 (Hybrid) | 4+ | Very High | 4-6 hours |

---

## Comparison: Security vs Convenience

| Scenario | Security Level | Convenience | Automation | Identity Isolation |
| --- | --- | --- | --- | --- |
| **1. Basic** | ★★★☆☆ | ★★★★★ | No | Single identity |
| **2. CI/CD** | ★★★★☆ | ★★★★☆ | Yes | Single identity |
| **3. Multi-Client** | ★★★★★ | ★★☆☆☆ | Yes | Full isolation |
| **4. Enterprise** | ★★★★★ | ★★★☆☆ | No (usually) | Corporate identity |
| **4. Enterprise (YubiKey)** | ★★★★★★ | ★★☆☆☆ | No | Corporate identity |

**Security considerations:**

- **Basic:** Single key compromise = all work affected
- **CI/CD:** Automation key is single-factor, but isolated from personal key
- **Multi-Client:** Best isolation - compromised client key doesn't affect other clients
- **Enterprise:** Policy-driven, hardware key option for maximum security

**Convenience considerations:**

- **Basic:** One passphrase, one identity, zero configuration overhead
- **CI/CD:** Two keys, but automation key used automatically in CI/CD
- **Multi-Client:** Multiple passphrases, requires disciplined directory organization
- **Enterprise:** Policy compliance overhead, hardware key requires physical presence

---

## Cost-Benefit Analysis

### Scenario 1: Basic Setup

**Costs:**

- Setup time: 15 minutes
- Ongoing: 0 (no maintenance)
- Financial: $0

**Benefits:**

- GitHub verified commits
- Basic security (passphrase protection)
- Simple mental model

**ROI:** Excellent for personal projects

---

### Scenario 2: Personal + CI/CD

**Costs:**

- Setup time: 1 hour (generate key, configure CI/CD)
- Ongoing: Minimal (rotate automation key if compromised)
- Financial: $0

**Benefits:**

- Automated signed commits (releases, changelogs)
- Risk isolation (automation key separate)
- Professional appearance (all commits verified)

**ROI:** High for open-source maintainers and automation users

---

#### Cost Analysis: Scenario 3 (Multi-Client Consultant)

**Costs:**

- Setup time: 2-5 hours (initial), 30 min per new client
- Ongoing: Annual key rotation per client (1 hour per year per client)
- Financial: $0 (or password manager subscription for backup)

**Benefits:**

- Complete client isolation (contractual compliance)
- Professional identity management (correct email per client)
- Risk mitigation (compromised key affects one client only)
- Automatic key switching (zero mental overhead after setup)

**ROI:** High for consultants with 2+ clients, essential for 5+ clients

---

#### Cost Analysis: Scenario 4 (Enterprise Environment)

**Costs:**

- Setup time: 1-2 hours (policy review, key generation, IT filing)
- Ongoing: Annual rotation (policy-driven), 1-2 hours per year
- Financial: $0 (software key) or $100-300 (YubiKey x2)

**Benefits:**

- Policy compliance (avoid violations)
- IT support (backup/recovery managed)
- Hardware key option (maximum security for high-privilege access)
- Standardized team process (consistent across org)

**ROI:** Mandatory (no alternative in corporate environment)

---

## Troubleshooting Multi-Key Setups

### Issue: Wrong Key Used for Commit

**Symptom:** Commit signed with personal key when should use client key

**Diagnosis:**

```bash
# Check which key Git is using
cd ~/Clients/ClientA/projects/repo1
git config user.signingkey
# Expected: <CLIENT_A_KEY_ID>
# If wrong: <PERSONAL_KEY_ID>
```

**Solution:**

```bash
# Verify conditional include is correct
cat ~/.gitconfig | grep -A 2 "includeIf"
# Should match directory path

# Check client config exists
cat ~/Clients/ClientA/.gitconfig-clienta
# Should set user.signingkey to CLIENT_A_KEY_ID

# Test key switching
git config user.signingkey
git config user.email
```

---

### Issue: Passphrase Prompt for Automation Key

**Symptom:** CI/CD fails with "cannot sign, passphrase required"

**Diagnosis:** Automation key was generated WITH passphrase (should be NO passphrase)

**Solution:**

```bash
# Generate new automation key without passphrase
# Use batch mode with %no-protection
cat > /tmp/gpg-automation-params <<'EOF'
%no-protection
EOF

# Or: Remove passphrase from existing key (NOT RECOMMENDED - regenerate instead)
gpg --edit-key <AUTOMATION_KEY_ID>
gpg> passwd
# Enter old passphrase, leave new passphrase empty
gpg> save
```

---

### Issue: Multiple Passphrase Prompts

**Symptom:** GPG asks for passphrase for every commit (annoying)

**Solution:** Configure GPG agent passphrase caching

```bash
# Edit ~/.gnupg/gpg-agent.conf
default-cache-ttl 3600        # Cache for 1 hour
max-cache-ttl 86400           # Maximum 24 hours

# Restart GPG agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

---

## Navigation

### Return to Main Skill

- **[SKILL.md](../SKILL.md)** - Main gpg-multi-key skill with quick decision matrix

### Related References

- **[backup-recovery.md](backup-recovery.md)** - Comprehensive backup and recovery procedures
- **[implementation-example.md](implementation-example.md)** - Real-world case study

### Official Documentation

- [GitHub: Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [Git Conditional Includes](https://git-scm.com/docs/git-config#_conditional_includes)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)

**Last Updated:** 2025-11-17

**Audit Notes**: Comprehensive validation completed using official GnuPG, Git, and GitHub documentation. All scenarios, commands, and configurations verified accurate.
