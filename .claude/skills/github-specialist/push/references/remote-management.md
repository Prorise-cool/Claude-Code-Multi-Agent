# Remote Management

Complete guide to configuring and managing remote repositories for push/fetch operations.

## Common Remote Commands

```bash
# List all remotes
git remote -v

# Add new remote
git remote add origin https://github.com/username/repo.git
git remote add origin git@github.com:username/repo.git  # SSH

# Change remote URL
git remote set-url origin git@github.com:username/new-repo.git

# Rename remote
git remote rename origin upstream

# Remove remote
git remote remove origin

# Show remote details
git remote show origin
```

## Multiple Remotes (Fork Workflow)

```bash
# Add upstream for forked repos
git remote add upstream git@github.com:original-owner/repo.git

# Verify remotes
git remote -v
# origin      git@github.com:your-username/repo.git (fetch)
# origin      git@github.com:your-username/repo.git (push)
# upstream    git@github.com:original-owner/repo.git (fetch)
# upstream    git@github.com:original-owner/repo.git (push)

# Fetch from upstream
git fetch upstream

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin feature-branch
```

## Remote Verification

```bash
# Test connection to remote
git ls-remote origin

# Show remote tracking branches
git branch -r

# Show all branches (local + remote)
git branch -a
```

## Credential Management

For credential configuration and authentication, see the **git-config** skill (credential management section).

---

**Related Documentation:**

- [Git Official Docs - Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- git-config skill - Credential management section
