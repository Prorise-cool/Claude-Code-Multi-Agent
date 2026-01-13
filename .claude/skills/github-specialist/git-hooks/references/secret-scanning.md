# Security & Secret Scanning

## gitleaks Integration

### Installation

```bash
# macOS
brew install gitleaks

# Windows
scoop install gitleaks

# Docker
docker pull zricethezav/gitleaks
```

### Framework Integration

#### Husky.Net

```json
{
  "name": "gitleaks",
  "group": "pre-commit",
  "command": "gitleaks",
  "args": ["protect", "--staged", "--verbose"]
}
```

#### lefthook

```yaml
pre-commit:
  commands:
    gitleaks:
      run: gitleaks protect --staged --verbose
```

#### Husky (JavaScript)

```bash
npx husky add .husky/pre-commit "gitleaks protect --staged --verbose"
```

#### pre-commit (Python)

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
```

## TruffleHog Integration (Comprehensive Secret Scanning)

**TruffleHog** validates secrets against SaaS APIs (detects 800+ secret types).

### Installation and Usage

```bash
# Install
brew install trufflesecurity/trufflehog/trufflehog

# Run in pre-commit
trufflehog git file://. --since-commit HEAD --only-verified
```

### lefthook Integration

```yaml
pre-commit:
  commands:
    trufflehog:
      run: trufflehog git file://. --since-commit HEAD --only-verified
```

### Why TruffleHog?

- Validates secrets against APIs (eliminates false positives)
- Detects 800+ secret types
- Scans beyond code (Docker images, S3 buckets, documents)
- Enterprise-grade accuracy

## CI/CD Secret Scanning (Defense in Depth)

### GitHub Actions (gitleaks)

```yaml
name: Secret Scanning
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
```

### Best Practice

Scan locally (pre-commit) AND in CI/CD (pull requests).

## Handling False Positives

### Using .gitleaksignore

```text
# .gitleaksignore
test-fixtures/fake-secret.txt
docs/examples/api-key-example.md
```

### Using .gitleaks.toml

```toml
[allowlist]
paths = [
  "test-fixtures/",
  "docs/examples/"
]
```

---

**Last Updated:** 2025-11-19
