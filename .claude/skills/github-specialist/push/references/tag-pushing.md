# Tag Pushing

Complete guidance for pushing version tags to remote repositories for releases and milestones.

## Tag Types

- **Annotated tags**: Recommended for releases (includes metadata: tagger, date, message)
- **Lightweight tags**: Simple pointers (just a name pointing to a commit)

## Tag Pushing Commands

```bash
# Create annotated tag (recommended for releases)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create lightweight tag (quick bookmark)
git tag v1.0.0

# Push specific tag to remote
git push origin v1.0.0

# Push all tags to remote
git push --tags

# Push commits + annotated tags pointing to them (recommended)
git push --follow-tags

# Delete tag from remote
git push origin --delete v1.0.0
```

## Tag Pushing Strategies

### Option 1: Manual (Explicit Control) - Recommended

```bash
# Never auto-push tags (default behavior)
# Push tags explicitly when ready
git push origin v1.0.0
```

### Option 2: Follow Tags (Push Relevant Tags)

```bash
# Auto-push annotated tags when they point to commits being pushed
git config --global push.followTags true
# Or use --follow-tags flag:
git push --follow-tags
```

### Option 3: Always Push All Tags (Not Recommended)

```bash
# Pushes ALL local tags on every push (dangerous)
# NOT recommended - can push experimental/draft tags
# Note: This requires combining push.followTags=true with --tags flag
git config --global push.followTags true
# Then use --tags flag when pushing to include all tags
```

## Recommended Workflow

```bash
# 1. Create annotated tag for release
git tag -a v1.0.0 -m "Release version 1.0.0: Added feature X"

# 2. Push commits and tag together
git push --follow-tags
# Or push tag explicitly:
git push origin v1.0.0

# 3. Verify tag is on remote
git ls-remote --tags origin
```

## Tag Aliases

Set up helpful aliases for common tag operations:

```bash
# Set up helpful aliases
git config --global alias.pusht 'push --follow-tags'
git config --global alias.pushtag '!git push origin --tags'

# Usage:
git pusht       # Push commits + relevant annotated tags
git pushtag     # Push all tags explicitly
```

For more alias configuration, see the **git-config** skill.

---

**Last Updated:** 2025-11-28
