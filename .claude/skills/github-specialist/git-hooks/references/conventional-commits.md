# Conventional Commits & Semantic Versioning

## commitlint Setup

### Step 1: Install commitlint

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

### Step 2: Create commitlint.config.js

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation changes
        'style',    // Code style changes (formatting)
        'refactor', // Code refactoring
        'perf',     // Performance improvements
        'test',     // Adding or updating tests
        'build',    // Build system changes
        'ci',       // CI/CD changes
        'chore',    // Other changes
        'revert'    // Revert previous commit
      ]
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'always', 'sentence-case'],
    'header-max-length': [2, 'always', 100]
  }
};
```

### Step 3: Add commit-msg Hook

#### Husky

```bash
npx husky add .husky/commit-msg "npx --no -- commitlint --edit \$1"
```

#### Husky.Net

```json
{
  "name": "commitlint",
  "group": "commit-msg",
  "command": "npx",
  "args": ["--no", "--", "commitlint", "--edit", "${args}"]
}
```

#### lefthook

```yaml
commit-msg:
  commands:
    commitlint:
      run: npx --no -- commitlint --edit $1
```

## commitizen (Interactive Commits)

### Installation

```bash
npm install --save-dev commitizen cz-conventional-changelog
npx commitizen init cz-conventional-changelog --save-dev --save-exact
```

### Usage

```bash
# Instead of git commit, use:
npx cz
```

This provides an interactive prompt for creating Conventional Commits.

## semantic-release (Automated Versioning)

### Installation and Configuration

```bash
npm install --save-dev semantic-release
```

### Add to package.json

```json
{
  "release": {
    "branches": ["main", "master"]
  }
}
```

### GitHub Actions Workflow

```yaml
name: Release
on:
  push:
    branches: [main, master]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### How it works

- Analyzes commits since last release
- Determines next version based on Conventional Commits
- Generates changelog
- Creates git tag and GitHub release
- Publishes package (if configured)

---

**Last Updated:** 2025-11-19
