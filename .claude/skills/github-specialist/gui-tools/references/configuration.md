# Configuration After Installation

Post-installation configuration steps for Git GUI tools.

## 1. Configure Git Identity (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Most GUI tools will prompt for this on first launch.

---

## 2. Add SSH Keys (for SSH cloning)

GUI tools typically integrate with your system SSH keys (`~/.ssh/id_ed25519`, `~/.ssh/id_rsa`).

If you don't have SSH keys yet, see the **setup** skill for SSH key generation.

---

## 3. Authenticate with Git Hosting Provider

Most GUI tools will prompt you to authenticate with GitHub, GitLab, Bitbucket, etc. on first use.

**GitHub**: Uses OAuth (browser authentication)
**GitLab/Bitbucket**: Uses OAuth or Personal Access Tokens
**Self-hosted**: Uses username/password or tokens

---

## 4. Configure Diff/Merge Tool (Optional)

Some GUI tools set themselves as the default diff/merge tool in Git config. You can verify or change this:

```bash
# View current diff tool
git config --get diff.tool

# View current merge tool
git config --get merge.tool

# Set a different diff tool (if needed)
git config --global diff.tool <tool-name>

# Set a different merge tool (if needed)
git config --global merge.tool <tool-name>
```

---

**Last Updated:** 2025-11-28
