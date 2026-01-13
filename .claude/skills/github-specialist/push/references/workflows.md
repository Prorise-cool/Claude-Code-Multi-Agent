# Remote Push Workflows

Complete workflows for common Git push scenarios and development patterns.

## Workflow 1: Feature Branch Development

**Standard feature branch workflow:**

```bash
# 1. Create and switch to feature branch
git switch -c feature/user-auth

# 2. Make changes and commit (see git-commit skill)
git add .
git commit -m "feat(auth): implement user authentication"

# 3. Push feature branch (first time - sets upstream)
git push -u origin feature/user-auth

# 4. Continue development (subsequent pushes)
git commit -m "feat(auth): add password validation"
git push  # No -u needed after first push with -u

# 5. After code review, merge via PR (see git-commit skill for PR creation)
```

---

## Workflow 2: Rebase and Force Push

**When you need to clean up history before merging:**

```bash
# 1. Fetch latest main
git fetch origin

# 2. Rebase feature branch onto main
git rebase origin/main

# 3. Force push (use --force-with-lease for safety)
git push --force-with-lease

# 4. If rebase conflicts occur:
# Resolve conflicts, then:
git rebase --continue
git push --force-with-lease
```

---

## Workflow 3: Hotfix to Production

**Emergency fix workflow:**

```bash
# 1. Create hotfix branch from main
git switch main
git pull
git switch -c hotfix/critical-bug

# 2. Make fix and commit (see git-commit skill)
git commit -m "fix: resolve critical authentication bug"

# 3. Push hotfix
git push -u origin hotfix/critical-bug

# 4. Create PR for fast-track review
gh pr create --title "HOTFIX: Critical auth bug" --body "..."

# 5. After merge, delete hotfix branch
git switch main
git pull
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

---

## Workflow 4: Fork Contribution

**Contributing to open source projects via fork:**

```bash
# 1. Add upstream remote (one-time setup)
git remote add upstream git@github.com:original-owner/repo.git

# 2. Sync fork with upstream
git fetch upstream
git switch main
git merge upstream/main
git push origin main

# 3. Create feature branch
git switch -c feature/awesome-feature

# 4. Make changes and push to fork
git commit -m "feat: add awesome feature"
git push -u origin feature/awesome-feature

# 5. Create PR from fork to upstream
gh pr create --repo original-owner/repo --title "Feature: ..." --body "..."
```

---

## Workflow 5: Release Tagging

**Creating and pushing release tags:**

```bash
# 1. Ensure main branch is up-to-date
git switch main
git pull

# 2. Create annotated tag for release
git tag -a v1.0.0 -m "Release version 1.0.0: Added feature X"

# 3. Push commits and tag together
git push --follow-tags
# Or push tag explicitly:
git push origin v1.0.0

# 4. Verify tag is on remote
git ls-remote --tags origin

# 5. Create GitHub release (if using GitHub)
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes..."
```

---

**Related Documentation:**

- [Git Official Docs - Distributed Workflows](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
- git-commit skill - Commit creation and PR workflows
- git-config skill - Workflow automation and aliases
