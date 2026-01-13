# Best Practices

Detailed best practices for Git line ending management.

## 1. Always Use .gitattributes in Repos You Control

**Minimal .gitattributes:**

```gitattributes
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

## 2. Document Platform-Specific Configs

- Windows: Verify `autocrlf=true` (default)
- macOS: Must set `autocrlf=input` (NOT default)
- Linux: Must set `autocrlf=input` (NOT default)
- WSL: Treat as Linux (`autocrlf=input`)

## 3. Set core.safecrlf=warn for Safety

```bash
git config --global core.safecrlf warn
```

## 4. Test with git ls-files --eol

```bash
# Check files
git ls-files --eol | head -20

# Find mismatches
git ls-files --eol | grep "w/crlf" | grep "eol=lf"
git ls-files --eol | grep "w/mixed"
```

## 5. Normalize When Adding .gitattributes

```bash
vim .gitattributes
git add --renormalize .
git status
git commit -m "Add .gitattributes and normalize"
```

## 6. Review .gitattributes in Code Reviews

Check for:

- New file types without rules
- Binary files not marked `binary`
- Platform-specific files with correct `eol`

## 7. Use Pre-Commit Hooks

```bash
#!/bin/bash
CRLF_SCRIPTS=$(git diff --cached --name-only | grep -E "\.(sh|bash)$" | xargs file | grep CRLF)
if [ -n "$CRLF_SCRIPTS" ]; then
    echo "Error: Shell scripts with CRLF detected"
    exit 1
fi
```

## 8. Educate Team

Key points:

- Why line endings matter
- Platform differences
- Git configuration importance
- When to use .gitattributes

## 9. Add .gitattributes Early

Best time: Before adding any files
Second best: As soon as you realize it's missing

## 10. Monitor for Issues

```bash
# Check for mixed endings
git ls-files --eol | grep "w/mixed"

# Check binary files treated as text
git ls-files --eol | grep -E "\.(png|jpg)" | grep -v "binary"
```
