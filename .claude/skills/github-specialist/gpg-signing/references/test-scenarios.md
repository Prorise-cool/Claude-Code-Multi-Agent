# Git GPG Signing - Test Scenarios

Test scenarios for validating skill activation and coverage.

## Scenario 1: Initial GPG setup on Windows

- **Query:** "Set up GPG commit signing on Windows"
- **Expected:** Skill activates, provides installation and configuration guidance

## Scenario 2: Troubleshooting "inappropriate ioctl" error

- **Query:** "Getting inappropriate ioctl error with GPG signing"
- **Expected:** Skill loads troubleshooting.md, provides GPG_TTY solution

## Scenario 3: Passphrase caching configuration

- **Query:** "How do I stop GPG from asking for my passphrase every time?"
- **Expected:** Skill loads passphrase-caching.md with gpg-agent configuration

## Scenario 4: Windows dual-GPG confusion

- **Query:** "GPG signing not working on Windows, multiple GPG installations"
- **Expected:** Skill loads windows-setup.md with PATH troubleshooting

## Scenario 5: GitHub unverified commits

- **Query:** "My commits show as unverified on GitHub"
- **Expected:** Skill provides public key export and GitHub upload steps

## Scenario 6: keyboxd daemon race condition on Windows

- **Query:** "Getting 'gpg failed to sign the data' error on Windows after reboot"
- **Expected:** Skill loads troubleshooting.md with keyboxd daemon startup diagnosis and T7777/T7829 bug references

## Scenario 7: SSH signing alternative

- **Query:** "Should I use SSH or GPG for commit signing?"
- **Expected:** Skill provides comparison table and SSH setup instructions

## Scenario 8: Key generation guidance

- **Query:** "What algorithm should I use for my GPG key?"
- **Expected:** Skill recommends Ed25519/Curve25519 with rationale
