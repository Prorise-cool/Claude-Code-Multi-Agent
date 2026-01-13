# Real-World Examples

Detailed examples from actual repositories and scenarios.

## Example 1: This Onboarding Repository

**Setup:**

- Platforms: Windows (primary), macOS, Linux, WSL
- Line ending policy: LF for all documentation

**Configuration:**

```gitattributes
* text=auto
*.md text eol=lf
*.sh text eol=lf
*.ps1 text eol=crlf
*.png binary
```

**Team Config:**

- Windows: `core.autocrlf=true`
- Mac/Linux: `core.autocrlf=input`

**Result:** ✅ Cross-platform, clean diffs, shell scripts work everywhere

## Example 2: External Repository Without .gitattributes

**Your Setup (Windows):**

```bash
git clone https://github.com/external/legacy-project.git
git config --get core.autocrlf  # Shows: true ✅

# Make changes
echo "New feature" >> src/main.c
git commit -m "Add feature"

# Repository gets LF ✅
```

**Key:** Option 1 config prevents issues in external repos

## Example 3: Team Member with Wrong Config

**Problem:**

```bash
# New member (Mac, never configured)
git config --get core.autocrlf  # Empty

# Edits file → Git diff shows every line changed
# Only line endings changed, not content
```

**Fix:**

```bash
git config --global core.autocrlf input
```

**Prevention:** Document Git config in onboarding

## Example 4: Adding .gitattributes to Legacy Repository

**Current State:**

```bash
git ls-files --eol | awk '{print $2}' | sort | uniq -c
#   7,523 w/crlf
#   2,891 w/lf
#      45 w/mixed
```

**Process:**

```bash
# Create .gitattributes
cat > .gitattributes << 'EOF'
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
EOF

# Normalize
git add --renormalize .
git commit -m "Add .gitattributes and normalize (7,568 files)"
```

**Result:** ✅ Clean repository, 7,568 files normalized
