# Testing & Validation Strategies

## Unit Testing Hook Scripts

### Example: Testing a pre-commit hook script

```bash
#!/usr/bin/env bash
# test-pre-commit.sh

# Test successful execution
run_pre_commit_with_valid_code() {
  # Setup
  echo "valid code" > test-file.py
  git add test-file.py

  # Execute
  .git/hooks/pre-commit
  result=$?

  # Assert
  [ "$result" -eq 0 ] || exit 1
  echo "✅ PASS: Pre-commit succeeds with valid code"
}

# Test failure on invalid code
run_pre_commit_with_invalid_code() {
  # Setup
  echo "invalid syntax (" > test-file.py
  git add test-file.py

  # Execute
  .git/hooks/pre-commit
  result=$?

  # Assert
  [ "$result" -ne 0 ] || exit 1
  echo "✅ PASS: Pre-commit fails with invalid code"
}

# Run tests
run_pre_commit_with_valid_code
run_pre_commit_with_invalid_code
```

## Integration Testing

### Test complete workflow

```bash
#!/usr/bin/env bash
# integration-test.sh

# Create test repository
test_hook_integration() {
  # Setup
  mkdir test-repo && cd test-repo
  git init

  # Install hooks
  dotnet husky install

  # Create test file
  echo "using System;" > Test.cs
  git add Test.cs

  # Attempt commit
  git commit -m "test: integration test"
  result=$?

  # Assert hook executed successfully
  [ "$result" -eq 0 ] || exit 1
  echo "✅ PASS: Integration test successful"

  # Cleanup
  cd .. && rm -rf test-repo
}

test_hook_integration
```

## CI/CD Validation

Run same checks in CI as locally.

### GitHub Actions (.NET)

```yaml
name: Code Quality
on: [push, pull_request]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0.x'

      - name: Restore dependencies
        run: dotnet restore

      - name: Format check
        run: dotnet format --verify-no-changes --verbosity diagnostic

      - name: Build
        run: dotnet build --no-restore /warnaserror

      - name: Test
        run: dotnet test --no-build --verbosity normal
```

### GitHub Actions (JavaScript/TypeScript)

```yaml
name: Code Quality
on: [push, pull_request]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Format check
        run: npx prettier --check .

      - name: Test
        run: npm test
```

## Team Collaboration & Enforcement

### Automatic Hook Installation

#### Husky.Net (MSBuild Target)

```bash
# Attach to project file
dotnet husky attach YourProject.csproj
```

This adds a target that runs `dotnet husky install` before package restore.

#### Husky (JavaScript - package.json)

```json
{
  "scripts": {
    "prepare": "husky install"
  }
}
```

Runs automatically after `npm install`.

#### lefthook (package.json or CI script)

```json
{
  "scripts": {
    "postinstall": "lefthook install"
  }
}
```

#### pre-commit (CI enforcement)

```yaml
# GitHub Actions
- name: Install pre-commit hooks
  run: pre-commit install

- name: Run pre-commit
  run: pre-commit run --all-files
```

### CI/CD Enforcement (Defense in Depth)

**Strategy:** Run same checks locally (pre-commit) AND remotely (CI/CD).

**Why?**

- Developers can bypass local hooks (`--no-verify`)
- CI/CD provides final validation
- Prevents bad code from merging

### GitHub Branch Protection

1. Require status checks to pass
2. Require branches to be up to date
3. Require signed commits (optional)

### Azure DevOps Branch Policies

1. Require build validation
2. Require minimum number of reviewers
3. Check for linked work items

### Bypass Policies

#### When to allow `--no-verify`

- Emergency hotfixes (with post-hoc review)
- Revert commits
- CI/CD automated commits

#### When to disallow

- Regular development work
- Pull request merges
- Production deployments

#### Audit bypasses

```bash
# Log bypass attempts
git log --all --grep="--no-verify" --oneline
```

#### Organizational policy example

> Developers may use `--no-verify` only for emergency hotfixes. All bypassed commits must be reviewed in next team standup.

---

**Last Updated:** 2025-11-19
