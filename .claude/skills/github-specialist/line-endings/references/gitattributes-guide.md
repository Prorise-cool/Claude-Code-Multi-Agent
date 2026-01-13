# .gitattributes Guide

Comprehensive guide to .gitattributes configuration for line ending management.

## What is .gitattributes?

`.gitattributes` is a repository-level configuration file that explicitly declares how Git should handle specific files. It is checked into version control and applies to all developers, ensuring consistent behavior across the team.

## Common Patterns

**Minimal:**

```gitattributes
* text=auto
```

**Comprehensive:**

```gitattributes
# Default behavior
* text=auto

# Documentation - LF
*.md text eol=lf
*.txt text eol=lf

# Shell scripts - MUST be LF (Unix requirement)
*.sh text eol=lf
*.bash text eol=lf

# PowerShell scripts - CRLF (Windows standard)
*.ps1 text eol=crlf
*.cmd text eol=crlf
*.bat text eol=crlf

# Configuration files - LF
*.json text eol=lf
*.yml text eol=lf
.gitignore text eol=lf

# Binary files
*.png binary
*.jpg binary
*.pdf binary
*.exe binary
```

## Attribute Reference

- `text=auto` - Auto-detect text files and normalize
- `text eol=lf` - Use LF in working directory
- `text eol=crlf` - Use CRLF in working directory
- `binary` - Never convert line endings

## When to Add .gitattributes

Always add to:

- New repositories you create
- Team repositories you control
- Projects with cross-platform contributors
- Projects with shell scripts or platform-specific files

## Adding to Existing Repository

```bash
# Create .gitattributes
vim .gitattributes

# Normalize existing files
git add --renormalize .

# Review and commit
git status
git commit -m "Add .gitattributes and normalize line endings"
```
