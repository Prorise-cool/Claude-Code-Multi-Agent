# Git Hooks Examples

This directory contains ready-to-use configuration examples for various git hook frameworks across different ecosystems.

## Files

### .NET/C# Examples

- **husky-net-dotnet-format.json** - Complete Husky.Net configuration for .NET projects
  - dotnet format on pre-commit (staged files only)
  - gitleaks secret scanning on pre-commit
  - dotnet build with warnings as errors on pre-push
  - dotnet test on pre-push
  - commitlint for commit message validation

- **lefthook-dotnet.yml** - lefthook configuration optimized for .NET projects
  - Parallel execution for maximum performance
  - dotnet format with staged files
  - gitleaks integration
  - commitlint support
  - Pre-push build and test validation

### JavaScript/TypeScript Examples

- **husky-javascript-package.json** - Complete package.json with Husky + lint-staged + commitlint
  - Automatic hook installation via prepare script
  - lint-staged configuration for incremental processing
  - ESLint and Prettier integration
  - Dependencies included

### Python Examples

- **pre-commit-python.yaml** - Comprehensive pre-commit configuration for Python projects
  - Ruff for fast linting and formatting (10-100x faster than Flake8/Black)
  - mypy for type checking
  - Standard file checks (YAML, JSON, TOML, trailing whitespace)
  - gitleaks for secret scanning
  - commitlint for commit message validation

### Polyglot Examples

- **lefthook-polyglot.yml** - Multi-language repository configuration
  - .NET/C# (dotnet format, dotnet test)
  - JavaScript/TypeScript (ESLint, Prettier)
  - Python (Ruff)
  - Parallel execution across all languages
  - Unified secret scanning and commit message validation

### Commit Message Validation

- **commitlint.config.js** - Conventional Commits configuration
  - Standard commit types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert)
  - Scope and subject validation rules
  - Header and body length limits
  - Proper formatting enforcement

## Usage

### Husky.Net

```bash
# 1. Install Husky.Net
dotnet tool install Husky

# 2. Initialize
dotnet husky install

# 3. Copy example configuration
cp examples/husky-net-dotnet-format.json .husky/task-runner.json

# 4. Attach to project (optional, for team auto-install)
dotnet husky attach YourProject.csproj
```

### lefthook

```bash
# 1. Install lefthook
npm install lefthook --save-dev  # or brew install lefthook

# 2. Copy example configuration
cp examples/lefthook-dotnet.yml lefthook.yml  # or lefthook-polyglot.yml

# 3. Initialize
lefthook install
```

### Husky (JavaScript)

```bash
# 1. Copy package.json configuration
# Merge the "scripts", "devDependencies", and "lint-staged" sections
# from examples/husky-javascript-package.json into your package.json

# 2. Install dependencies
npm install

# 3. Initialize Husky
npx husky init

# 4. Add hooks
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg "npx --no -- commitlint --edit \$1"
```

### pre-commit (Python)

```bash
# 1. Install pre-commit
pip install pre-commit

# 2. Copy example configuration
cp examples/pre-commit-python.yaml .pre-commit-config.yaml

# 3. Install hooks
pre-commit install

# 4. Run on all files (first time)
pre-commit run --all-files
```

### commitlint

```bash
# 1. Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# 2. Copy example configuration
cp examples/commitlint.config.js commitlint.config.js
```

## Customization

### Adjusting for Your Project

All examples are designed as starting points. Customize them based on your needs:

1. **Add/remove hooks** - Comment out or delete tasks you don't need
2. **Adjust file patterns** - Modify `glob`, `include`, or `lint-staged` patterns
3. **Change validation rules** - Customize commitlint rules, linter configurations
4. **Add custom scripts** - Include project-specific validation scripts

### Performance Tuning

- **Use parallel execution** where supported (lefthook, concurrent lint-staged tasks)
- **Process only staged files** using `${staged}`, `{staged_files}`, or lint-staged
- **Defer slow checks to CI/CD** - Keep local hooks fast, run comprehensive checks in pipelines

### Security Best Practices

- **Always include secret scanning** (gitleaks or TruffleHog) in pre-commit
- **Validate in CI/CD** - Don't rely solely on local hooks (developers can bypass with `--no-verify`)
- **Use commitlint** to enforce Conventional Commits for automated versioning and changelogs

## See Also

- [Main skill documentation](../SKILL.md) - Complete git hooks guide
- [Official documentation links](../SKILL.md#references) - Framework-specific official docs
