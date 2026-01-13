# Troubleshooting Git Hooks

## Hooks Not Running

### Diagnosis

```bash
# Check hook files exist
ls -la .git/hooks/

# Check hook is executable (Unix/Mac)
chmod +x .git/hooks/pre-commit

# Check core.hooksPath
git config core.hooksPath
```

### Solutions

- **Husky.Net:** Run `dotnet husky install`
- **Husky (JS):** Run `npx husky install`
- **lefthook:** Run `lefthook install`
- **pre-commit:** Run `pre-commit install`

## Hooks Too Slow

### Diagnosing Performance Issues

```bash
# Time hook execution
time git commit -m "test"
```

### Performance Solutions

1. **Use incremental processing** (lint-staged, ${staged}, {staged_files})
2. **Use parallel execution** (lefthook with `parallel: true`)
3. **Switch to faster tools** (Ruff instead of Flake8/pylint)
4. **Cache results** (ESLint --cache, dotnet --no-build)
5. **Defer slow checks to CI/CD** (full test suite in CI, quick tests in pre-push)

## Windows Path Issues

### Problem

Paths with spaces or backslashes fail.

### Solution

```yaml
# Use quotes and forward slashes
run: dotnet format --include "${staged_files}"
```

**Husky.Net:**

```json
{
  "args": ["format", "--include", "${staged}"]
}
```

## Migration & Adoption

### Gradual Rollout Strategy

#### Phase 1: Start with formatting (low risk)

- Add dotnet format / Prettier / Black
- Warning mode (don't block commits)
- Team feedback and adjustment

#### Phase 2: Add linting

- Add ESLint / Ruff / StyleCop
- Error mode (block commits)
- Fix existing violations

#### Phase 3: Add commit message validation

- Add commitlint
- Educate team on Conventional Commits
- Provide commitizen for assistance

#### Phase 4: Add testing and security

- Add dotnet test in pre-push
- Add gitleaks in pre-commit
- CI/CD enforcement

### Migration from Manual Scripts

**From:** `.git/hooks/pre-commit` shell script

**To:** Framework-managed hooks

**Strategy:**

1. **Preserve existing logic** - Copy scripts to framework configuration
2. **Test in parallel** - Run old script AND new framework temporarily
3. **Validate behavior** - Ensure new framework matches old behavior
4. **Deprecate old scripts** - Remove manual scripts once validated

### Team Education

**Key topics:**

1. **What are git hooks?** - Automated scripts that run on git events
2. **Why do we use them?** - Enforce quality, prevent mistakes, automate checks
3. **How to bypass (when appropriate)?** - `--no-verify` for emergencies
4. **What happens if hook fails?** - Commit/push blocked, fix issues
5. **Where to get help?** - Link to this skill, team documentation

---

**Last Updated:** 2025-11-19
