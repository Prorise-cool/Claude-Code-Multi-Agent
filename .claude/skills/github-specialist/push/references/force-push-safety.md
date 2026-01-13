# Force Push Safety Protocols

Comprehensive guidance for safe force pushing operations, including safety rules, force-with-lease mechanics, and recovery procedures.

## Critical Safety Rules

- ✅ **ONLY force push on feature branches** (your personal work)
- ✅ **ALWAYS use `--force-with-lease`** (not `--force`)
- ❌ **NEVER force push to main/master/develop** (shared branches)
- ❌ **NEVER force push if others are working on the same branch**
- ⚠️ **ALWAYS communicate** before force pushing shared feature branches

## Why `--force-with-lease` is Safer

```bash
# ❌ DANGEROUS: Overwrites remote regardless of changes
git push --force

# ✅ SAFE: Only overwrites if no one else pushed since your last fetch
git push --force-with-lease

# ✅ SAFEST: Force-with-lease for specific branch
git push --force-with-lease origin feature-branch
```

## How `--force-with-lease` Works

1. Checks if remote branch matches your last known state (from `git fetch`)
2. If someone else pushed since your last fetch → REJECTS push (prevents data loss)
3. If remote matches your expectation → Allows force push

⚠️ **Important Caveat**: `--force-with-lease` can be defeated by background processes that run `git fetch` automatically (e.g., IDE background sync, cron jobs). If your editor or system runs `git fetch` in the background, it updates your local remote-tracking branch, making `--force-with-lease` think you've seen the latest changes when you haven't. To mitigate this:

- Be aware of tools that auto-fetch (IDEs, Git GUI clients)
- Use `--force-if-includes` for additional safety (see below)

## When Force Push is Necessary

```bash
# Scenario 1: After amending last commit
git commit --amend -m "Updated commit message"
git push --force-with-lease

# Scenario 2: After interactive rebase (squashing commits)
git rebase -i HEAD~3
git push --force-with-lease

# Scenario 3: After rebasing onto main
git rebase main
git push --force-with-lease

# Scenario 4: After resetting to previous commit
git reset --hard HEAD~1
git push --force-with-lease
```

## Advanced Safety: `--force-if-includes`

For maximum safety, especially when background processes might auto-fetch, use `--force-if-includes` alongside `--force-with-lease`:

```bash
# Safest force push - verifies remote changes are integrated locally
git push --force-with-lease --force-if-includes

# Or configure globally
git config --global push.useForceIfIncludes true
```

**How `--force-if-includes` works**: It verifies that the tip of the remote-tracking ref is reachable from one of the reflog entries of your local branch. This ensures you've actually integrated (merged/rebased) any remote changes locally before force pushing.

## Pre-Force-Push Safety Checklist

1. ✅ Is this a feature branch (not main/master/develop)?
2. ✅ Am I the only person working on this branch?
3. ✅ Have I communicated with team if it's shared?
4. ✅ Did I run `git fetch` recently to see latest remote state?
5. ✅ Am I using `--force-with-lease` (not `--force`)?
6. ✅ Consider using `--force-if-includes` for maximum safety

## Recovery from Accidental Force Push

If you accidentally force push and lose commits:

```bash
# Find lost commits in reflog
git reflog

# Reset to previous state
git reset --hard <commit-hash>

# Force push again (carefully!)
git push --force-with-lease
```

## Branch Protection

Branch protection is typically configured at the repository level (GitHub, GitLab, Bitbucket settings). Common protections include:

- Requiring pull requests before merging
- Requiring status checks to pass
- Requiring review approvals (1+ reviewers)
- Restricting who can push to protected branches
- Preventing force pushes to protected branches

Configure branch protection rules in your repository settings to prevent accidental force pushes to shared branches.

---

**Last Updated:** 2025-11-28
