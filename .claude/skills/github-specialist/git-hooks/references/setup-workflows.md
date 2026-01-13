# Setup Workflows by Ecosystem

## .NET/C# Workflows

### Husky.Net Setup Workflow

#### Step 1: Install Husky.Net

```bash
# Navigate to project root
cd <project-root>

# Create tool manifest if not exists
dotnet new tool-manifest

# Install Husky.Net
dotnet tool install Husky

# Initialize Husky
dotnet husky install
```

#### Step 2: Attach to Project (Automatic Installation)

```bash
# Attach Husky to .csproj file (auto-installs for team members)
dotnet husky attach <path-to-csproj>
```

This adds an MSBuild target to your .csproj file ensuring automatic installation when team members restore packages.

#### Step 3: Create task-runner.json Configuration

Create `.husky/task-runner.json`:

```json
{
  "$schema": "https://alirezanet.github.io/Husky.Net/schema.json",
  "tasks": [
    {
      "name": "dotnet-format",
      "group": "pre-commit",
      "command": "dotnet",
      "args": ["format", "--include", "${staged}"],
      "include": ["**/*.cs"]
    },
    {
      "name": "dotnet-test",
      "group": "pre-push",
      "command": "dotnet",
      "args": ["test", "--no-build"],
      "include": ["**/*.cs"]
    },
    {
      "name": "commit-message-linter",
      "group": "commit-msg",
      "command": "dotnet",
      "args": ["husky", "exec", ".husky/csx/commit-lint.csx", "--args", "${args}"]
    }
  ]
}
```

#### Step 4: Verify Installation

```bash
# Test pre-commit hook
git add .
git commit -m "test: verify hooks work"
```

**See example:** [examples/husky-net-dotnet-format.json](../examples/husky-net-dotnet-format.json)

### lefthook Setup Workflow (.NET/C#)

#### Step 1: Install lefthook

```bash
# Windows (Scoop)
scoop install lefthook

# macOS (Homebrew)
brew install lefthook

# npm (cross-platform)
npm install lefthook --save-dev

# Initialize
lefthook install
```

#### Step 2: Create lefthook.yml Configuration

Create `lefthook.yml` in project root:

```yaml
pre-commit:
  parallel: true
  commands:
    dotnet-format:
      glob: "*.cs"
      run: dotnet format --include {staged_files}

pre-push:
  parallel: true
  commands:
    dotnet-test:
      run: dotnet test --no-build
    dotnet-build:
      run: dotnet build /warnaserror

commit-msg:
  commands:
    commitlint:
      run: npx --no -- commitlint --edit $1
```

#### Step 3: Verify Installation

```bash
# Test configuration
lefthook run pre-commit

# Commit to trigger hooks
git add .
git commit -m "test: verify lefthook works"
```

**See example:** [examples/lefthook-dotnet.yml](../examples/lefthook-dotnet.yml)

### .NET-Specific Patterns

**dotnet format Integration:**

```json
{
  "name": "dotnet-format-staged",
  "command": "dotnet",
  "args": ["format", "--include", "${staged}", "--verify-no-changes"],
  "include": ["**/*.cs", "**/*.vb"]
}
```

**dotnet test with Build Warnings as Errors:**

```json
{
  "name": "dotnet-test-strict",
  "group": "pre-push",
  "command": "dotnet",
  "args": ["test", "/warnaserror", "--no-build"]
}
```

**NuGet Package Validation:**

```yaml
pre-commit:
  commands:
    nuget-validate:
      glob: "*.csproj"
      run: dotnet pack --no-build --configuration Release
```

**ReSharper/Rider CLI Integration:**

```json
{
  "name": "jb-cleanup-code",
  "command": "dotnet",
  "args": ["jb", "cleanupcode", "YourSolution.sln", "--profile=Team: Full Cleanup", "--include=${staged}"]
}
```

## JavaScript/TypeScript Workflows

### Husky + lint-staged + commitlint Setup

#### Step 1: Install Dependencies

```bash
npm install --save-dev husky lint-staged @commitlint/cli @commitlint/config-conventional eslint prettier
```

#### Step 2: Initialize Husky

```bash
npx husky init
npm pkg set scripts.prepare="husky install"
npm run prepare
```

#### Step 3: Configure lint-staged

Add to `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

Or create `.lintstagedrc.json`:

```json
{
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "*.{json,md,yml,yaml}": [
    "prettier --write"
  ]
}
```

#### Step 4: Add Hooks

```bash
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg "npx --no -- commitlint --edit \$1"
```

#### Step 5: Configure commitlint

Create `commitlint.config.js`:

```javascript
export default { extends: ['@commitlint/config-conventional'] };
```

#### Step 6: Verify Installation

```bash
# Test hooks
git add .
git commit -m "feat: add new feature"
```

**See example:** [examples/husky-javascript-package.json](../examples/husky-javascript-package.json)

### Monorepo Patterns (Nx, Turborepo, Lerna)

**For monorepos**, run tools from root and use workspace-relative paths:

```json
{
  "lint-staged": {
    "packages/**/*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

**Nx-specific example:**

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "nx affected:lint --fix --files",
      "nx affected:test --files"
    ]
  }
}
```

## Python Workflows

### pre-commit Framework Setup

#### Step 1: Install pre-commit

```bash
pip install pre-commit
```

#### Step 2: Create .pre-commit-config.yaml

Create `.pre-commit-config.yaml` in project root:

```yaml
repos:
  # Ruff replaces Black, Flake8, isort - 10-100x faster
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

#### Step 3: Install Hooks

```bash
pre-commit install
```

#### Step 4: Run on All Files (First Time)

```bash
pre-commit run --all-files
```

#### Step 5: Verify Installation

```bash
# Test hooks
git add .
git commit -m "feat: add new feature"
```

**See example:** [examples/pre-commit-python.yaml](../examples/pre-commit-python.yaml)

### Fast Python Linters (Ruff vs Flake8/pylint)

**Ruff** is 10-100x faster than traditional Python linters:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.5
    hooks:
      - id: ruff
        args: [--fix, --select, "E,F,W,I,N"]
      - id: ruff-format  # Replaces Black for even faster formatting
```

**Why Ruff?**

- 10-100x faster than Flake8/pylint
- Compatible with Flake8/pylint/isort rule sets
- Single tool replaces multiple linters
- Written in Rust (native performance)

## Polyglot Workflows

For repositories with multiple languages, use **lefthook** or **pre-commit** (language-agnostic).

### lefthook for Polyglot Repositories

```yaml
pre-commit:
  parallel: true
  commands:
    # .NET/C#
    dotnet-format:
      glob: "*.cs"
      run: dotnet format --include {staged_files}

    # JavaScript/TypeScript
    eslint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}

    prettier:
      glob: "*.{js,ts,jsx,tsx,json,md}"
      run: npx prettier --write {staged_files}

    # Python
    ruff:
      glob: "*.py"
      run: ruff check --fix {staged_files}

    black:
      glob: "*.py"
      run: black {staged_files}
```

**See example:** [examples/lefthook-polyglot.yml](../examples/lefthook-polyglot.yml)

---

**Last Updated:** 2025-11-25
