# Troubleshooting Push Issues

Comprehensive guide to diagnosing and resolving common push failures and conflicts.

## Common Issues

### Issue 1: Rejected Push (Non-Fast-Forward)

**Symptom:**

```text
error: failed to push some refs to 'origin'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Cause:** Someone else pushed commits to the remote branch since your last fetch.

**Solution:**

```bash
# Option 1: Fetch and merge (creates merge commit)
git fetch origin
git merge origin/main
git push

# Option 2: Fetch and rebase (cleaner history)
git fetch origin
git rebase origin/main
git push

# Option 3: Pull with rebase (fetch + rebase in one step)
git pull --rebase
git push
```

---

### Issue 2: Authentication Failure

**Symptom:**

```text
fatal: Authentication failed for 'https://github.com/username/repo.git'
```

**Solutions:**

```bash
# For HTTPS: Update credentials
# Windows: Use Windows Credential Manager
# macOS: Use Keychain Access
# Linux: Use git-credential-store or gh CLI

# For SSH: Verify SSH key is configured
ssh -T git@github.com
# Should respond: "Hi username! You've successfully authenticated..."

# If SSH fails, add SSH key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Switch from HTTPS to SSH
git remote set-url origin git@github.com:username/repo.git
```

**For comprehensive credential management**, see the **git-config** skill.

---

### Issue 3: Protected Branch

**Symptom:**

```text
remote: error: GH006: Protected branch update failed
```

**Cause:** Attempting to push directly to a protected branch (main/master/develop).

**Solution:**

```bash
# Push to feature branch instead
git switch -c feature-branch
git push -u origin feature-branch

# Create pull request to merge into protected branch
gh pr create --title "Feature: ..." --body "Description..."
```

**For pull request workflows**, see the **git-commit** skill (PR creation section).

---

### Issue 4: Large Files or Repository Size

**Symptom:**

```text
remote: error: File is too large (exceeds 100 MB)
```

**Solution:**

```bash
# Remove large file from commit history
git rm --cached large-file.bin
git commit --amend -m "Remove large file"

# Use Git LFS for large files
git lfs install
git lfs track "*.bin"
git add .gitattributes
git commit -m "Configure Git LFS"
git push
```

**For Git LFS configuration**, see the **line-endings** skill.

---

### Issue 5: Divergent Branches

**Symptom:**

```text
hint: You have divergent branches and need to specify how to reconcile them.
```

**Solution:**

```bash
# Configure pull strategy globally
git config --global pull.rebase true

# Or specify on this pull
git pull --rebase
git push
```

---

## General Troubleshooting Tips

**Before Pushing:**

- Run `git status` to verify working directory state
- Run `git fetch` to see latest remote state
- Run `git log origin/branch..HEAD` to see commits you're about to push
- Verify branch name with `git branch --show-current`

**After Push Failure:**

- Read error message carefully (Git provides helpful hints)
- Check remote status with `git remote show origin`
- Verify credentials and authentication
- Check repository settings for branch protection rules

---

**Related Documentation:**

- [Git Official Docs - Troubleshooting](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)
- git-config skill - Credential management
- git-commit skill - Pull request workflows
- line-endings skill - Git LFS setup
