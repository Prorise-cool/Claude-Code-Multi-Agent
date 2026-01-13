# Troubleshooting

Common Git line ending issues and solutions.

## Issue: "warning: CRLF will be replaced by LF"

**What It Means:** Git is normalizing correctly (informational, not error).

**Fix:** This is expected behavior. To suppress warnings (not recommended):

```bash
git config --global core.safecrlf false
```

## Issue: Files Show Wrong Line Endings

**Symptom:**

```bash
git ls-files --eol README.md
# Shows: i/lf w/crlf attr/text eol=lf
```

**Fix:**

```bash
git add --renormalize .
git commit -m "Normalize line endings"
```

## Issue: Shell Scripts Won't Execute

**Error:** `bash: /bin/bash^M: bad interpreter`

**Fix:**

```bash
# Immediate
dos2unix script.sh

# Permanent
echo "*.sh text eol=lf" >> .gitattributes
git add --renormalize script.sh
git commit -m "Fix shell script line endings"
```

## Issue: Git Shows Every Line Changed

**Cause:** Line endings changed (CRLF ↔ LF).

**Fix:**

```bash
git add --renormalize file.txt
git commit -m "Normalize line endings"
```

## Issue: Binary Files Corrupted

**Fix:**

```bash
# Restore
git checkout HEAD -- file.png

# Prevent
echo "*.png binary" >> .gitattributes
git commit -m "Mark binary files"
```
