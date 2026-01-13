# Workflows & Scenarios

Common workflows and real-world scenarios for Git line ending configuration.

## Scenario A: New Repository (You Control)

```bash
# 1. Initialize repository
mkdir my-project && cd my-project && git init

# 2. Add .gitattributes FIRST
cat > .gitattributes << 'EOF'
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
EOF

git add .gitattributes && git commit -m "Add .gitattributes"

# 3. Configure Git if not already
# Windows: git config --global core.autocrlf true
# Mac/Linux: git config --global core.autocrlf input

# 4. Add project files
git add . && git commit -m "Initial commit"
```

## Scenario B: Existing Repository with .gitattributes

**Fresh Clone:**

```bash
git clone https://github.com/user/repo.git
# Files checked out with correct line endings automatically
```

**After .gitattributes update:**

```bash
git pull
git add --renormalize .
git status && git commit -m "Normalize line endings"
```

## Scenario C: External Repository Without .gitattributes

With Option 1 config (safe): Files normalized automatically ✅
With Option 2 config (broken): Mixed line endings ❌

## Scenario D: Fixing Mixed Line Endings

```bash
# 1. Detect
git ls-files --eol | awk '{print $2}' | sort | uniq -c

# 2. Fix
cat > .gitattributes << 'EOF'
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
EOF

# 3. Normalize
git add --renormalize .
git commit -m "Add .gitattributes and normalize line endings"
```
