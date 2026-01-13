# Git Large File System (LFS)

Git LFS is a Git extension that stores large binary files separately to prevent repository bloat.

## Installation

**Windows:**

```bash
winget install Git.LFS
git lfs install
```

**macOS:**

```bash
brew install git-lfs
git lfs install
```

**Linux:**

```bash
sudo apt-get install git-lfs  # Ubuntu/Debian
git lfs install
```

## When to Use Git LFS

Use for:

- ✅ Large binaries (>1MB): images, videos, datasets
- ✅ Frequently updated binaries: design files (PSD, Sketch)
- ✅ Build artifacts: compiled binaries

Don't use for:

- ❌ Small binaries (<100KB)
- ❌ Text files (source code, documentation)
- ❌ Rarely changing files

## Configuration

```gitattributes
# Images
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text

# Archives
*.zip filter=lfs diff=lfs merge=lfs -text

# Documents
*.pdf filter=lfs diff=lfs merge=lfs -text
```

## Basic Commands

```bash
# Track file type
git lfs track "*.psd"

# View tracked patterns
git lfs track

# List LFS files
git lfs ls-files

# Migrate existing files (rewrites history!)
git lfs migrate import --include="*.png,*.jpg"
```

## GitHub LFS Storage and Bandwidth Limits

**Current limits per GitHub plan (as of 2025-11-17):**

| Plan | Storage | Bandwidth (per month) |
| --- | --- | --- |
| GitHub Free (personal) | 10 GiB | 10 GiB |
| GitHub Pro | 10 GiB | 10 GiB |
| GitHub Free (organizations) | 10 GiB | 10 GiB |
| GitHub Team | 250 GiB | 250 GiB |
| GitHub Enterprise Cloud | 250 GiB | 250 GiB |

**Additional usage:**

- Bandwidth and storage beyond included amounts are billed per GiB
- Use the [GitHub pricing calculator](https://github.com/pricing/calculator?feature=lfs) to estimate costs
- Storage is billed hourly, bandwidth is billed per GiB downloaded

**Important notes:**

- Bandwidth resets every month, storage usage does not reset
- Repository owner's quota is used (not the person pushing/downloading)
- Anyone with write access can push to LFS without using their own quota

**Reference:** [GitHub LFS Billing Documentation](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)
