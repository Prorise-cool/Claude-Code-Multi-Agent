# Git Push Best Practices

Comprehensive best practices for safe, effective Git push operations.

## Push Safety

**Force Push Safety:**

- ✅ Always use `--force-with-lease` instead of `--force`
- ✅ Communicate before force pushing shared branches
- ✅ Run `git fetch` before force pushing (keeps lease up-to-date)
- ✅ Verify branch name before force pushing (`git branch` to check)
- ✅ Consider using `--force-if-includes` for maximum safety
- ❌ Never force push to main/master/develop
- ❌ Never use `--force` unless absolutely necessary (extremely rare)

**Pre-Push Verification:**

- ✅ Run tests before pushing (ensure code works)
- ✅ Review changes with `git diff origin/branch..HEAD`
- ✅ Verify no sensitive data (credentials, API keys, secrets)
- ✅ Check commit messages are descriptive
- ✅ Ensure working directory is clean (`git status`)

---

## Push Frequency

**Recommended Cadence:**

- ✅ Push feature branches daily (backup and collaboration)
- ✅ Push after completing logical units of work
- ✅ Push before leaving for the day (backup)
- ✅ Push after significant progress (don't lose work)
- ❌ Don't push broken code (run tests first)
- ❌ Don't push sensitive data (use .gitignore, git-secrets)

**Branch Hygiene:**

- ✅ Delete merged feature branches promptly
- ✅ Clean up stale remote branches (`git push origin --delete old-branch`)
- ✅ Keep remote tracking branches current (`git fetch --prune`)
- ✅ Verify branch is up-to-date before pushing

---

## Tag Management

**Tag Creation:**

- ✅ Use annotated tags for releases (`git tag -a`)
- ✅ Follow semantic versioning (v1.0.0, v1.1.0, v2.0.0)
- ✅ Include meaningful tag messages (what changed)
- ✅ Tag stable commits (not work-in-progress)
- ❌ Don't use lightweight tags for releases (less metadata)

**Tag Pushing:**

- ✅ Push tags explicitly (`git push origin v1.0.0`)
- ✅ Or use `--follow-tags` to push relevant tags
- ✅ Verify tag is on remote (`git ls-remote --tags origin`)
- ❌ Don't use `--tags` regularly (can push experimental tags)
- ❌ Don't delete tags from remote unless absolutely necessary

---

## Remote Hygiene

**Remote Configuration:**

- ✅ Use descriptive remote names (origin, upstream, fork)
- ✅ Verify remote URLs before pushing (`git remote -v`)
- ✅ Use SSH for authentication when possible (more secure)
- ✅ Keep credential helpers configured (avoid repeated prompts)

**Remote Maintenance:**

- ✅ Clean up old branches after merging
- ✅ Keep remote tracking branches up-to-date (`git fetch --prune`)
- ✅ Verify remote connection periodically (`git ls-remote origin`)
- ✅ Update remote URLs if repositories move

---

## Security Best Practices

**Credential Management:**

- ✅ Use SSH keys for authentication (more secure than passwords)
- ✅ Use credential helpers (avoid storing passwords in plain text)
- ✅ Rotate credentials periodically
- ✅ Use personal access tokens (not passwords) for HTTPS
- ❌ Never commit credentials to repository
- ❌ Never share SSH private keys

**Data Protection:**

- ✅ Use `.gitignore` to prevent committing sensitive files
- ✅ Use `git-secrets` or similar tools to scan for secrets
- ✅ Review diffs before pushing (`git diff origin/branch..HEAD`)
- ✅ Use Git LFS for large binary files (don't bloat repository)
- ❌ Never commit API keys, passwords, tokens, certificates
- ❌ Never commit environment files (.env) with real credentials

---

## Collaboration Best Practices

**Team Communication:**

- ✅ Communicate before force pushing shared branches
- ✅ Follow team's branching strategy (Git Flow, GitHub Flow, etc.)
- ✅ Use descriptive branch names (feature/user-auth, fix/login-bug)
- ✅ Create pull requests for code review (don't push directly to main)
- ✅ Respond to PR feedback promptly

**Branch Protection:**

- ✅ Configure branch protection rules for main/master/develop
- ✅ Require pull requests before merging
- ✅ Require status checks to pass (tests, linting)
- ✅ Require review approvals (1+ reviewers)
- ✅ Prevent force pushes to protected branches

---

## Automation and Configuration

**Global Configuration:**

```bash
# Auto-setup upstream on first push
git config --global push.autoSetupRemote true

# Push annotated tags automatically
git config --global push.followTags true

# Use force-if-includes for maximum safety
git config --global push.useForceIfIncludes true

# Default push strategy (simple is default in modern Git)
git config --global push.default simple
```

**Helpful Aliases:**

```bash
# Safe force push
git config --global alias.fpush 'push --force-with-lease --force-if-includes'

# Push with tags
git config --global alias.pusht 'push --follow-tags'

# Push all tags
git config --global alias.pushtag '!git push origin --tags'
```

**For comprehensive configuration**, see the **git-config** skill.

---

**Related Documentation:**

- [Git Official Docs - Git Workflows](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
- git-config skill - Configuration and aliases
- git-commit skill - Commit best practices
