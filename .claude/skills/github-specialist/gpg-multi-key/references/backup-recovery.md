# GPG Multi-Key Backup and Recovery

**You are here:** [SKILL.md](../SKILL.md) → Backup and Recovery (detailed procedures)

## Table of Contents

- [Why Backup is Critical](#why-backup-is-critical)
- [What to Backup](#what-to-backup)
  - [Essential (MUST Backup)](#essential-must-backup)
  - [Optional (Recommended)](#optional-recommended)
- [Backup Strategies](#backup-strategies)
  - [Strategy 1: Full Keyring Backup (Recommended for Personal)](#strategy-1-full-keyring-backup-recommended-for-personal)
  - [Strategy 2: Per-Key Backup (Recommended for Consultants)](#strategy-2-per-key-backup-recommended-for-consultants)
  - [Strategy 3: Per-Client Vault (Recommended for Multi-Client)](#strategy-3-per-client-vault-recommended-for-multi-client)
  - [Strategy 4: Hardware Security Keys (Enterprise)](#strategy-4-hardware-security-keys-enterprise)
- [Secure Storage Locations](#secure-storage-locations)
  - [Recommended](#recommended)
  - [NOT Recommended](#not-recommended)
  - [Detailed Storage Recommendations](#detailed-storage-recommendations)
- [Backup Frequency](#backup-frequency)
- [Recovery Procedures](#recovery-procedures)
  - [Full Keyring Recovery](#full-keyring-recovery)
  - [Single Key Recovery](#single-key-recovery)
  - [Revocation Certificate Recovery](#revocation-certificate-recovery)
- [Verification and Testing](#verification-and-testing)
  - [Backup Verification (Do This Immediately After Backup)](#backup-verification-do-this-immediately-after-backup)
  - [Recovery Testing (Do This Annually)](#recovery-testing-do-this-annually)
- [Disaster Recovery Scenarios](#disaster-recovery-scenarios)
  - [Scenario 1: Laptop Lost/Stolen](#scenario-1-laptop-loststolen)
  - [Scenario 2: Accidental Deletion](#scenario-2-accidental-deletion)
  - [Scenario 3: Hardware Failure](#scenario-3-hardware-failure)
  - [Scenario 4: Forgotten Passphrase](#scenario-4-forgotten-passphrase)
  - [Scenario 5: Key Expiration](#scenario-5-key-expiration)
- [Multi-Machine Synchronization](#multi-machine-synchronization)
  - [Strategy 1: Manual Export/Import](#strategy-1-manual-exportimport)
  - [Strategy 2: Shared GPG Home (Advanced)](#strategy-2-shared-gpg-home-advanced)
  - [Strategy 3: Per-Machine Keys (Most Secure)](#strategy-3-per-machine-keys-most-secure)
- [Security Checklist](#security-checklist)
- [Navigation](#navigation)

---

Comprehensive backup and recovery procedures for managing multiple GPG keys across different contexts (personal, automation, per-client, enterprise).

## Why Backup is Critical

**Without backups:**

- Lost keys = lost ability to sign commits with verified identity
- Historical commits may become unverifiable
- Client work may be inaccessible if encryption keys are lost
- Re-establishing trust requires generating new keys and re-adding to all services

**With proper backups:**

- Recover from laptop loss/failure
- Migrate keys to new development machines
- Restore after accidental deletion
- Audit trail for security incidents

## What to Backup

### Essential (MUST Backup)

1. **Private Keys** (all contexts)
   - Personal development key
   - CI/CD automation key (if used)
   - Per-client keys (all clients)
   - Enterprise keys (following company policy)

2. **Revocation Certificates**
   - Generated automatically in `~/.gnupg/openpgp-revocs.d/`
   - One per key (named by key fingerprint)
   - Required to revoke compromised keys

3. **Passphrases**
   - Store separately in password manager
   - **NEVER** store with key backups
   - Use unique passphrases per key (client isolation)

### Optional (Recommended)

1. **Git Configuration Files**
   - `~/.gitconfig` (global configuration)
   - Per-client configs (e.g., `.gitconfig-clienta`)
   - Conditional include patterns

2. **GPG Configuration**
   - `~/.gnupg/gpg.conf` (GPG settings)
   - `~/.gnupg/gpg-agent.conf` (passphrase caching settings)

## Backup Strategies

### Strategy 1: Full Keyring Backup (Recommended for Personal)

**Pros:** Simple, backs up all keys at once
**Cons:** Single backup file contains all keys (higher risk if compromised)

```bash
# Export all private keys
gpg --armor --export-secret-keys > gpg-all-keys-backup.asc

# Encrypt backup (symmetric encryption with strong passphrase)
gpg --symmetric --cipher-algo AES256 gpg-all-keys-backup.asc

# Result: gpg-all-keys-backup.asc.gpg (encrypted)

# Delete unencrypted file
shred -u gpg-all-keys-backup.asc  # Linux (secure overwrite + delete)
rm -f gpg-all-keys-backup.asc     # macOS/Windows (Note: standard deletion, consider secure erase tools)
# macOS note: rm -P is deprecated. Use 'rm -f' or install 'srm' for secure deletion
# Windows note: Use 'cipher /w' or SDelete for secure deletion if needed
```

### Strategy 2: Per-Key Backup (Recommended for Consultants)

**Pros:** Key isolation, can store client keys separately
**Cons:** More management overhead (multiple backup files)

```bash
# Export specific key
gpg --armor --export-secret-keys <KEY_ID> > personal-key-backup.asc

# Encrypt
gpg --symmetric --cipher-algo AES256 personal-key-backup.asc

# Delete unencrypted file (use platform-appropriate method)
shred -u personal-key-backup.asc  # Linux
# rm -f personal-key-backup.asc  # macOS/Windows (less secure)

# Repeat for each key (personal, automation, per-client)
```

### Strategy 3: Per-Client Vault (Recommended for Multi-Client)

**Integrated with consultant workflow** (see Scenario 3 in SKILL.md):

```bash
# Client keys already exported to per-client vaults
~/Clients/ClientA/.vault/gpg-keys/clienta-private.asc
~/Clients/ClientA/.vault/gpg-keys/clienta-public.asc

# Encrypt per-client vault directories
# (Use VeraCrypt, Cryptomator, or similar)

# Backup encrypted vaults to secure storage
```

### Strategy 4: Hardware Security Keys (Enterprise)

**YubiKey/Nitrokey considerations:**

- Private key **cannot be extracted** from hardware device
- Backup means having **multiple YubiKeys** with same key
- Follow enterprise policy for hardware key backup procedures

```bash
# Generate key on YubiKey (immutable)
gpg --card-edit
gpg/card> admin
gpg/card> generate

# IMPORTANT: Key cannot be backed up traditionally
# Enterprise solution: Generate on one YubiKey, clone to backup YubiKey (if policy allows)
# OR: Generate off-device, import to YubiKey, then backup before import
```

## Secure Storage Locations

### Recommended

| Storage Type | Use Case | Security Level | Pros | Cons |
| --- | --- | --- | --- | --- |
| **Password Manager** | Personal keys | High | Encrypted, versioned, synced | Requires subscription |
| **Encrypted Vault** | Per-client keys | High | Full control, offline capable | Manual sync required |
| **Hardware USB** | Cold backup | Very High | Air-gapped, physical security | Can be lost/damaged |
| **Enterprise Storage** | Enterprise keys | Varies | Policy-compliant, IT support | Requires approval |

### NOT Recommended

| Storage Type | Why NOT | Risk |
| --- | --- | --- |
| **Unencrypted Cloud** | No encryption at rest | Key exposure |
| **Git Repositories** | Version history = permanent exposure | Cannot be removed |
| **Email** | Transit/storage not secure | Interception risk |
| **Shared Drives** | Access control issues | Unauthorized access |
| **Chat Apps** | Not designed for secrets | Logging, backups, leaks |

### Detailed Storage Recommendations

#### Password Managers (Recommended)

**1Password / Bitwarden / Dashlane:**

```bash
# Export encrypted backup
gpg --symmetric --cipher-algo AES256 gpg-all-keys-backup.asc

# Upload gpg-all-keys-backup.asc.gpg to password manager "Secure Documents"
# Store decryption passphrase in separate password manager entry
```

**Pros:**

- Encrypted at rest and in transit
- Version history (recover old keys)
- Access from any device (after authentication)
- Password manager already protects other secrets

**Cons:**

- Requires cloud service trust
- Subscription cost
- Internet required for access

#### Encrypted Vaults (Recommended)

**VeraCrypt / Cryptomator:**

```bash
# Create encrypted vault
veracrypt --create ~/gpg-backup-vault.tc

# Mount vault
veracrypt ~/gpg-backup-vault.tc /mnt/gpg-vault

# Copy backups into vault
cp gpg-all-keys-backup.asc.gpg /mnt/gpg-vault/

# Unmount
veracrypt --dismount /mnt/gpg-vault
```

**Pros:**

- Full control (no third party)
- Offline capable
- Can store on external drive

**Cons:**

- Manual sync across devices
- Risk of forgetting vault passphrase

#### Hardware USB (Cold Backup)

**Hardware-encrypted USB drive (e.g., Apricorn Aegis, Kingston IronKey):**

```bash
# Copy encrypted backups to hardware USB
cp gpg-all-keys-backup.asc.gpg /media/encrypted-usb/

# Store USB in physical safe
# Separate from computer (fire/theft protection)
```

**Pros:**

- Air-gapped (not connected to internet)
- Physical security (safe, lockbox)
- Hardware encryption (secure even if stolen)

**Cons:**

- Can be lost or damaged
- Requires physical access to recover
- Cost of hardware-encrypted USB ($50-150)

## Backup Frequency

| Key Type | Backup Frequency | Rationale |
| --- | --- | --- |
| **Personal** | After generation + annually | Infrequent changes |
| **Automation** | After generation + after rotation | Stored in CI/CD, low change frequency |
| **Per-Client** | After generation + after each change | Client work = higher risk, backup after key changes |
| **Enterprise** | Per company policy | Typically quarterly or after policy changes |

**Trigger events for immediate backup:**

- New key generation
- Key expiration extension
- Revocation certificate generation
- Subkey addition
- Passphrase change (encryption strength change)

## Recovery Procedures

### Full Keyring Recovery

```bash
# Decrypt backup
gpg --decrypt gpg-all-keys-backup.asc.gpg > gpg-all-keys-backup.asc

# Import private keys
gpg --import gpg-all-keys-backup.asc

# Verify keys imported successfully
gpg --list-secret-keys --keyid-format=long

# Trust imported keys
gpg --edit-key <KEY_ID>
gpg> trust
gpg> 5 (ultimate trust)
gpg> quit

# Clean up decrypted file (IMPORTANT)
shred -u gpg-all-keys-backup.asc
```

### Single Key Recovery

```bash
# Decrypt specific key backup
gpg --decrypt personal-key-backup.asc.gpg > personal-key-backup.asc

# Import key
gpg --import personal-key-backup.asc

# Verify import
gpg --list-secret-keys --keyid-format=long | grep <KEY_ID>

# Clean up
shred -u personal-key-backup.asc
```

### Revocation Certificate Recovery

**Scenario:** Key compromised, need to revoke immediately

```bash
# Import revocation certificate from backup
gpg --import ~/backup/openpgp-revocs.d/<KEY_FINGERPRINT>.rev

# Verify key is revoked
gpg --list-keys <KEY_ID>
# Should show: [revoked: YYYY-MM-DD]

# Distribute revoked key to keyservers
gpg --keyserver keys.openpgp.org --send-keys <KEY_ID>

# Remove from GitHub (Settings → GPG keys → Delete)
# Inform team/clients of compromise
```

## Verification and Testing

### Backup Verification (Do This Immediately After Backup)

```bash
# 1. Verify encrypted backup exists
ls -lh gpg-all-keys-backup.asc.gpg

# 2. Verify decryption works (without importing)
gpg --decrypt gpg-all-keys-backup.asc.gpg > /tmp/test-decrypt.asc

# 3. Check decrypted content is valid
gpg --show-keys /tmp/test-decrypt.asc

# 4. Clean up test files
shred -u /tmp/test-decrypt.asc

# 5. Document backup date and location
echo "Backup verified: $(date)" >> gpg-backup-log.txt
```

### Recovery Testing (Do This Annually)

**Test in isolated environment:**

```bash
# 1. Create test GPG home directory
export GNUPGHOME=/tmp/gpg-test-recovery
mkdir -p $GNUPGHOME
chmod 700 $GNUPGHOME

# 2. Attempt recovery from backup
gpg --decrypt /path/to/backup.asc.gpg | gpg --import

# 3. Verify keys recovered
gpg --list-secret-keys --keyid-format=long

# 4. Test signing with recovered key
echo "test" | gpg --sign --default-key <KEY_ID> | gpg --verify

# 5. Clean up test environment
unset GNUPGHOME
rm -rf /tmp/gpg-test-recovery
```

## Disaster Recovery Scenarios

### Scenario 1: Laptop Lost/Stolen

**Impact:** All keys potentially compromised

**Response:**

1. Assume keys compromised (laptop may not have full-disk encryption)
2. Immediately revoke all keys:

   ```bash
   # Import revocation certificates from backup
   gpg --import ~/backup/openpgp-revocs.d/*.rev

   # Distribute to keyservers
   gpg --keyserver keys.openpgp.org --send-keys <KEY_ID>
   ```

3. Remove keys from GitHub/GitLab
4. Generate new keys following same multi-key strategy
5. Notify clients/team of key rotation

### Scenario 2: Accidental Deletion

**Impact:** Keys deleted, but not compromised

**Response:**

1. Restore from backup (see Recovery Procedures above)
2. No revocation needed (keys not compromised)
3. Verify keys work with test commit
4. Update backup if changes were made since last backup

### Scenario 3: Hardware Failure

**Impact:** Cannot access keys (disk failure, corruption)

**Response:**

1. Restore from backup to new machine
2. Verify passphrase caching configuration
3. Test signing with each key
4. Update Git configuration (if paths changed)

### Scenario 4: Forgotten Passphrase

**Impact:** Cannot use key (passphrase required for signing)

**Response:**

1. Check password manager for passphrase
2. If not found: Passphrase cannot be recovered
3. Generate new key and revoke old key
4. Lesson: Always store passphrases in password manager

### Scenario 5: Key Expiration

**Impact:** Key expired, commits show "Expired"

**Response:**

1. Extend key expiration:

   ```bash
   gpg --edit-key <KEY_ID>
   gpg> expire
   # Set new expiration (1y recommended)
   gpg> save
   ```

2. Re-export public key
3. Update on GitHub/GitLab
4. Update backup with extended key

## Multi-Machine Synchronization

### Strategy 1: Manual Export/Import

**For consultants with multiple laptops:**

```bash
# On Machine A (export)
gpg --armor --export-secret-keys > keys-for-machine-b.asc
# Encrypt and transfer securely

# On Machine B (import)
gpg --import keys-for-machine-b.asc
gpg --edit-key <KEY_ID>
gpg> trust
gpg> 5 (ultimate trust)
gpg> quit
```

### Strategy 2: Shared GPG Home (Advanced)

**Using encrypted network storage:**

```bash
# Symlink GPG home to encrypted network storage
# NOT RECOMMENDED for per-client keys (security risk)
mv ~/.gnupg ~/Backup/gnupg-sync/
ln -s ~/Backup/gnupg-sync/ ~/.gnupg
```

**Risks:**

- Network latency affects GPG operations
- Concurrent access issues (multiple machines)
- Increased attack surface (network exposure)

### Strategy 3: Per-Machine Keys (Most Secure)

**Generate separate keys per machine:**

- Machine A: `<KEY_ID_A>` (add "Machine A" comment)
- Machine B: `<KEY_ID_B>` (add "Machine B" comment)
- Both keys registered on GitHub (both verify commits)

**Pros:**

- Machine compromise isolated
- No sync complexity
- Clear audit trail (which machine signed commit)

**Cons:**

- More keys to manage
- Must update GitHub with multiple keys

## Security Checklist

After backup creation:

- [ ] Backup is encrypted with strong passphrase
- [ ] Decryption passphrase stored separately in password manager
- [ ] Backup stored in secure location (password manager, encrypted vault, or hardware USB)
- [ ] Backup is NOT stored in Git, email, or unencrypted cloud
- [ ] Unencrypted backup file securely deleted (shred/rm -P)
- [ ] Backup verification completed (decrypt test)
- [ ] Backup location documented (where can I find this in 1 year?)
- [ ] Revocation certificates backed up alongside keys
- [ ] Git configuration files backed up (optional but recommended)

## Navigation

### Return to Main Skill

- **[SKILL.md](../SKILL.md)** - Main gpg-multi-key skill with quick decision matrix

### Related References

- **[scenarios.md](scenarios.md)** - Detailed scenario comparison and migration guidance
- **[implementation-example.md](implementation-example.md)** - Real-world case study

### Official Documentation

- [GnuPG Manual: Backup](https://www.gnupg.org/documentation/)
- [GitHub: Backup and Recovery Best Practices](https://docs.github.com/en/authentication/managing-commit-signature-verification)

**Last Updated:** 2025-11-17

**Audit Notes**: Validated secure deletion commands against current platform capabilities. Updated macOS `rm -P` (deprecated) to `rm -f` with notes about secure deletion alternatives.
