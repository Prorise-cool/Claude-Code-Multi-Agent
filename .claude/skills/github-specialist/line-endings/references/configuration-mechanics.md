# Configuration Mechanics

Detailed explanation of Git line ending configuration mechanics.

## Table of Contents

- [core.autocrlf](#coreautocrlf)
- [core.eol](#coreeol)
- [core.safecrlf](#coresafecrlf)
- [Precedence Hierarchy](#precedence-hierarchy)
- [Configuration Levels](#configuration-levels)

## core.autocrlf

Controls automatic line ending conversion.

**Values:**

| Value | Behavior on Checkout | Behavior on Commit | Use Case |
| --- | --- | --- | --- |
| `true` | LF → CRLF | CRLF → LF | Windows developers (Git for Windows default) |
| `input` | No conversion | CRLF → LF | Mac/Linux developers |
| `false` | No conversion | No conversion | Manual control via .gitattributes |

**How `autocrlf=true` Works (Windows):**

```text
Repository (LF)
     ↓ git checkout
  Convert LF → CRLF
     ↓
Working Directory (CRLF)
     ↓ git add/commit
  Convert CRLF → LF
     ↓
Repository (LF)
```

**How `autocrlf=input` Works (Mac/Linux):**

```text
Repository (LF)
     ↓ git checkout
  No conversion
     ↓
Working Directory (LF)
     ↓ git add/commit
  Convert CRLF → LF (if present)
     ↓
Repository (LF)
```

## core.eol

Fallback line ending style for working directory when `.gitattributes` doesn't specify and `autocrlf` doesn't apply.

**Values:**

- `native` - Use platform default (CRLF on Windows, LF on Unix) **[Recommended with autocrlf=false]**
- `lf` - Always use LF
- `crlf` - Always use CRLF

**When It Applies:**

- Only used when `core.autocrlf=false`
- Only applies to files with `text` attribute but no explicit `eol` attribute
- Overridden by `.gitattributes` `eol` attribute

## core.safecrlf

Safety check to prevent irreversible line ending conversions.

**Values:**

- `true` - Reject commits that would lose data (strict)
- `warn` - Warn about potential data loss but allow commit **[Recommended]**
- `false` - No safety checks (dangerous)

**Example Warning:**

```bash
$ git add file.txt
warning: in the working copy of 'file.txt', CRLF will be replaced by LF the next time Git touches it
```

This is informational - Git is normalizing the file per your configuration.

## Precedence Hierarchy

**Order of priority (highest to lowest):**

1. **`.gitattributes` `eol` attribute** - Explicit per-file rule (highest priority)
2. **`.gitattributes` `text` attribute** - Enables normalization
3. **`core.autocrlf`** - Automatic conversion (only if `eol` not specified)
4. **`core.eol`** - Fallback default (only if `autocrlf=false` and no attributes)

**Critical Finding:** `.gitattributes` `eol` attribute **ALWAYS overrides** `core.autocrlf`.

**Example:**

```bash
# Config: core.autocrlf=true
# .gitattributes: *.md text eol=lf

# Result: Markdown files will have LF in working directory
# The .gitattributes eol=lf takes precedence over autocrlf=true
```

## Configuration Levels

Git config can be set at three levels:

```bash
# System-wide (all users, all repos)
git config --system core.autocrlf true
# File: C:/Program Files/Git/etc/gitconfig (Windows)
# File: /etc/gitconfig (Unix)

# User/Global (current user, all repos)
git config --global core.autocrlf true
# File: ~/.gitconfig or ~/.config/git/config

# Repository/Local (current repo only)
git config --local core.autocrlf true
# File: .git/config (in repository root)
```

**Priority:** Local > Global > System (local settings override global/system)

**Best Practice:** Set line ending config at **global level** for consistency across your repos, use **local level** only for exceptions.
