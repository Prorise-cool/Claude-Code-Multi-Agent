# Push Configuration

Configuration options for Git push behavior, upstream tracking, and push strategies.

## Upstream Configuration

Upstream (tracking branch) tells Git where to push by default:

```bash
# Check current branch's upstream
git branch -vv

# Set upstream manually
git branch --set-upstream-to=origin/feature-branch

# Auto-setup upstream on first push (recommended global config)
git config --global push.autoSetupRemote true
# With this set, 'git push' automatically does 'git push -u origin <branch>'
```

## Push Strategies

```bash
# Check current push strategy
git config push.default

# Recommended: 'simple' (default in modern Git)
# Pushes current branch to same-named branch on remote
git config --global push.default simple

# Alternative: 'current'
# Always pushes to same-named branch (even if upstream differs)
git config --global push.default current
```

## Common Push Options

```bash
# Push current branch (upstream must be configured)
git push

# Push current branch and set upstream (first-time push)
git push -u origin feature-branch
# After this, 'git push' will work without arguments

# Push specific branch to remote
git push origin main

# Push all branches to remote (--all and --branches are synonyms)
git push --all origin
git push --branches origin  # Same as --all

# Dry run (show what would be pushed without actually pushing)
git push --dry-run
```

## Advanced Configuration

For detailed Git configuration including credential helpers, performance tuning, and advanced push settings, see the **git-config** skill.

---

**Last Updated:** 2025-11-28
