# Configuration Approaches

Detailed comparison of Option 1 (Traditional) vs Option 2 (Modern Explicit) configuration strategies.

## Table of Contents

- [Option 1: Traditional (autocrlf=true/input)](#option-1-traditional-autocrlftrueinput)
- [Option 2: Modern Explicit (autocrlf=false + eol=native)](#option-2-modern-explicit-autocrlffalse--eolnative)
- [Why Option 1 is Recommended](#why-option-1-is-recommended)
  - [The Critical Constraint: External Repositories](#the-critical-constraint-external-repositories)
  - [What Happens Without .gitattributes](#what-happens-without-gitattributes)
  - [Evidence from Testing](#evidence-from-testing)
  - [With .gitattributes: Both Options Work](#with-gitattributes-both-options-work)
- [Decision Matrix](#decision-matrix)
- [Recommendation](#recommendation)

## Option 1: Traditional (autocrlf=true/input)

**Configuration:**

```bash
# Windows
git config --global core.autocrlf true
git config --global core.safecrlf warn

# Mac/Linux
git config --global core.autocrlf input
git config --global core.safecrlf warn
```

**How It Works:**

- Git automatically converts line endings based on platform
- Windows: CRLF in working directory, LF in repository
- Mac/Linux: LF everywhere
- Normalization happens implicitly

**Behavior:**

| Scenario | Repository | Windows Working Dir | Mac/Linux Working Dir |
| --- | --- | --- | --- |
| No .gitattributes | LF | CRLF | LF |
| .gitattributes `* text=auto` | LF | CRLF | LF |
| .gitattributes `eol=lf` | LF | **LF** | LF |
| .gitattributes `eol=crlf` | CRLF | CRLF | CRLF |

**Critical Feature:** Works **WITHOUT .gitattributes** - normalizes automatically.

**Pros:**

✅ **Zero config on Windows** - Git for Windows default
✅ **Works without .gitattributes** - Safe for external/legacy repos
✅ **Automatic normalization** - Prevents mixed line endings in repository
✅ **Industry standard** - Traditional Git workflow
✅ **Honors .gitattributes** - Explicit `eol` attributes take precedence

**Cons:**

⚠️ **Platform-specific configs** - Windows devs use different settings than Mac/Linux
⚠️ **Implicit conversions** - Harder to understand what's happening
⚠️ **Debugging complexity** - When issues occur, harder to diagnose
⚠️ **Requires team coordination** - Each platform needs correct config

## Option 2: Modern Explicit (autocrlf=false + eol=native)

**Configuration:**

```bash
# All platforms (Windows, Mac, Linux, WSL)
git config --global core.autocrlf false
git config --global core.eol native
git config --global core.safecrlf warn
```

**How It Works:**

- Git does NOT automatically convert line endings
- `.gitattributes` controls all normalization behavior
- `eol=native` provides platform defaults when attributes don't specify
- Behavior is explicit and predictable

**Behavior:**

<!-- markdownlint-disable MD060 - emoji width differs from character count -->

| Scenario | Repository | Windows Working Dir | Mac/Linux Working Dir |
| --- | --- | --- | --- |
| No .gitattributes | **MIXED** ❌ | CRLF (native) | LF (native) |
| .gitattributes `* text=auto` | LF | CRLF (native) | LF (native) |
| .gitattributes `eol=lf` | LF | LF | LF |
| .gitattributes `eol=crlf` | CRLF | CRLF | CRLF |

<!-- markdownlint-enable MD060 -->

**Critical Limitation:** **REQUIRES .gitattributes** to work safely - without it, repository gets mixed line endings.

**Pros:**

✅ **Same config everywhere** - No platform-specific setup
✅ **Explicit and predictable** - Easy to understand and debug
✅ **Modern best practice** - Industry trend as of 2024-2025
✅ **Forces .gitattributes** - Encourages explicit line ending rules
✅ **Team consistency** - Everyone has identical configuration

**Cons:**

⚠️ **Requires config change** - Must override Git for Windows default
⚠️ **Requires .gitattributes** - Repos without it get corrupted
⚠️ **Not safe for external repos** - Can't add .gitattributes to repos you don't control
⚠️ **One-time migration** - Team needs to update configs

## Why Option 1 is Recommended

### The Critical Constraint: External Repositories

**You will work in repositories you don't control:**

- Open source projects
- Client repositories
- Legacy codebases
- Vendor repositories
- Forked projects

**These repositories may not have `.gitattributes`.**

### What Happens Without .gitattributes

**Option 1 (autocrlf=true/input):**

```bash
# Windows developer (autocrlf=true)
echo "Hello World" > file.txt   # Creates with CRLF
git add file.txt                # Commits as LF ✅
git commit -m "Add file"

# Mac developer (autocrlf=input)
echo "Hello World" > file.txt   # Creates with LF
git add file.txt                # Commits as LF ✅
git commit -m "Add file"

# Repository: Consistent LF everywhere ✅
```

**Option 2 (autocrlf=false + eol=native):**

```bash
# Windows developer (autocrlf=false, eol=native)
echo "Hello World" > file.txt   # Creates with CRLF
git add file.txt                # Commits as CRLF ❌
git commit -m "Add file"

# Mac developer (autocrlf=false, eol=native)
echo "Hello World" > file.txt   # Creates with LF
git add file.txt                # Commits as LF ❌
git commit -m "Add file"

# Repository: MIXED line endings ❌
# Result: Line ending chaos, huge diffs, merge conflicts
```

### Evidence from Testing

**Test Results:**

We tested both configurations in a repository WITHOUT .gitattributes:

<!-- markdownlint-disable MD060 - emoji width differs from character count -->

| Configuration | File Created On | Working Dir | Committed To Repo | Result |
| --- | --- | --- | --- | --- |
| `autocrlf=true` | Windows | CRLF | LF | ✅ Normalized |
| `autocrlf=input` | Mac/Linux | LF | LF | ✅ Normalized |
| `autocrlf=false eol=native` | Windows | CRLF | **CRLF** | ❌ Not normalized |
| `autocrlf=false eol=native` | Mac/Linux | LF | LF | ❌ Not normalized |

<!-- markdownlint-enable MD060 -->

**Conclusion:** Only Option 1 provides safe defaults that work in repositories without .gitattributes.

### With .gitattributes: Both Options Work

**When `.gitattributes` is present and comprehensive:**

- Both Option 1 and Option 2 behave identically
- `.gitattributes` `eol` attribute overrides `core.autocrlf`
- Explicit rules take precedence
- Behavior is predictable and consistent

**Example:**

```gitattributes
* text=auto
*.md text eol=lf
*.sh text eol=lf
*.ps1 text eol=crlf
```

With this `.gitattributes`:

- Option 1: `.md` and `.sh` files have LF, `.ps1` files have CRLF ✅
- Option 2: `.md` and `.sh` files have LF, `.ps1` files have CRLF ✅
- Both work correctly ✅

## Decision Matrix

<!-- markdownlint-disable MD060 - emoji width differs from character count -->

| Scenario | Option 1 | Option 2 |
| --- | --- | --- |
| Repository WITH comprehensive .gitattributes | ✅ Works | ✅ Works |
| Repository WITHOUT .gitattributes | ✅ Works (normalizes automatically) | ❌ Broken (mixed line endings) |
| External/legacy repo you can't modify | ✅ Works | ❌ Broken |
| Team repos you control | ✅ Works | ✅ Works (if you add .gitattributes) |

<!-- markdownlint-enable MD060 -->

## Recommendation

**Use Option 1 (autocrlf=true/input) if:**

- ✅ You work in repos you don't control (external, open source, client, vendor)
- ✅ Some repos lack .gitattributes
- ✅ You need safe defaults that "just work"
- ✅ You want to match Git for Windows defaults

**Use Option 2 (autocrlf=false + eol=native) if:**

- ✅ You control ALL repositories you work in
- ✅ You can ensure ALL repos have comprehensive .gitattributes
- ✅ You want explicit, debuggable configuration
- ✅ You're building a greenfield project with modern practices

**For most developers working in mixed environments: Use Option 1.**
