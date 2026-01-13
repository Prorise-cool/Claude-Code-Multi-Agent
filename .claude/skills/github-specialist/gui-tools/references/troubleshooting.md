# Troubleshooting Git GUI Tools

Common issues and solutions when working with Git GUI tools.

## GUI Tool Not Detecting Repositories

**Cause**: Tool not looking in the correct directory

**Solution**:

1. Open the tool's settings/preferences
2. Navigate to "Repositories" or "General" section
3. Add the directory where your repositories live
4. Restart the tool

---

## Authentication Failures

**Cause**: Git credential helper conflict or stale credentials

**Solution**:

```bash
# Check current credential helper
git config --get credential.helper

# For GitHub users with gh CLI:
gh auth status
gh auth refresh

# For Windows Credential Manager users:
cmdkey /list | Select-String -Pattern "git"
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

See the **git-config** skill for comprehensive credential management guidance.

---

## Merge Conflicts Not Resolving

**Cause**: GUI tool merge conflict editor not configured properly

**Solution**:

1. Ensure the GUI tool is set as the merge tool in Git config
2. Or use command-line conflict resolution:

```bash
# View conflicted files
git status

# Manually edit conflicted files
# Remove conflict markers (<<<<<<<, =======, >>>>>>>)

# Mark as resolved
git add <file>
git commit
```

---

## Slow Performance

**Cause**: Large repository or many files

**Solution**:

1. Enable Git performance features (see **git-config** skill):

   ```bash
   git config --global core.fsmonitor true
   git config --global core.untrackedCache true
   git config --global feature.manyFiles true
   ```

2. Consider using command-line Git for very large repos
3. Use Git LFS for large binary files (see **line-endings** skill)

---

**Last Updated:** 2025-11-28
