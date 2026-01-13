# Windows Installation Guide

Detailed installation instructions for Git GUI tools on Windows.

## GitKraken

**Website:** [https://www.gitkraken.com/download](https://www.gitkraken.com/download)

**Installation:**

```powershell
# Option 1: winget (recommended)
winget install --id Axosoft.GitKraken -e --source winget

# Option 2: Download installer from website
# https://www.gitkraken.com/download
```

**Features:**

- ✅ Modern, intuitive UI
- ✅ Built-in merge conflict editor
- ✅ Visual commit graph
- ✅ GitHub/GitLab/Bitbucket/Azure DevOps integrations
- ✅ GPG commit signing support
- ⚠️ Requires Pro license for private repositories

**Licensing:**

- **Community (Free)**: Public repositories only
- **Pro**: $96/user/year ($8/month) - Up to 2 seats, private repos
- **Advanced**: $144/user/year ($12/month) - Up to 10 seats, enhanced features
- **Business**: $192/user/year ($16/month) - Up to 100 seats, enterprise features

> **⚠️ Pricing Note:** Prices paid annually. Promotional pricing may be available. **These prices were accurate as of November 2025 but may change.** Always check the [official GitKraken pricing page](https://www.gitkraken.com/pricing) for current rates.

---

## Sourcetree

**Website:** [https://www.sourcetreeapp.com/](https://www.sourcetreeapp.com/)

**Installation:**

```powershell
# Option 1: winget (recommended)
winget install --id Atlassian.Sourcetree -e --source winget

# Option 2: Download installer from website
# https://www.sourcetreeapp.com/
```

**Features:**

- ✅ Free for all uses (private and public repos)
- ✅ Git LFS support
- ✅ Git Flow integration
- ✅ Visual diff/merge tool
- ✅ Atlassian (Bitbucket) integration
- ⚠️ Heavier application, slower startup

**Licensing:**

- **Free**: All features, no limitations

### Sourcetree Configuration Notes

#### Issue 1: Empty config values

Sourcetree may add empty config values during installation. These won't hurt anything, but you can clean them up:

```powershell
git config --global --unset difftool.sourcetree.cmd
git config --global --unset mergetool.sourcetree.cmd
git config --global --unset mergetool.sourcetree.trustexitcode
git config --global --unset mergetool.sourcetree.keepbackup
```

#### Issue 2: Global gitignore location

If you install Sourcetree and have it add a global gitignore, it may create files in `C:\Users\[YourUsername]\Documents` folder with `.txt` extensions:

- `.gitignore_global.txt` (Git)
- `.hgignore_global.txt` (Mercurial)

#### Option 1: Move and configure properly

1. Move files to `C:\Users\[YourUsername]\` (user profile root)
2. Remove `.txt` extensions
3. Ensure filenames start with `.`
4. Update Git config:

   ```powershell
   git config --global core.excludesfile "C:\Users\[YourUsername]\.gitignore_global"

   # Verify
   git config --global --get core.excludesfile
   ```

5. Update paths in Sourcetree settings

#### Option 2: Remove and unset (simpler)

```powershell
# Delete the files
Remove-Item "C:\Users\[YourUsername]\Documents\.gitignore_global.txt" -ErrorAction SilentlyContinue
Remove-Item "C:\Users\[YourUsername]\Documents\.hgignore_global.txt" -ErrorAction SilentlyContinue

# Unset Git config
git config --global --unset core.excludesfile
```

**Mercurial config (if needed):**

1. Open (or create) `C:\Users\[YourUsername]\Mercurial.ini` in a text editor
2. Add (or update) these lines:

   ```ini
   [ui]
   ignore = C:\Users\[YourUsername]\.hgignore_global
   ```

3. Verify:

   ```cmd
   hg config ui.ignore
   ```

---

## GitHub Desktop

**Website:** [https://desktop.github.com/download/](https://desktop.github.com/download/)

**Installation:**

```powershell
# Option 1: winget (recommended)
winget install --id GitHub.GitHubDesktop -e --source winget

# Option 2: Download installer from website
# https://desktop.github.com/download/
```

**Features:**

- ✅ Free, open source
- ✅ Simple, opinionated workflow
- ✅ GitHub integration (obviously)
- ✅ Automatic updates
- ⚠️ Limited advanced features (no rebasing, cherry-picking in GUI)
- ⚠️ Best for GitHub workflows

**Licensing:**

- **Free**: All features, open source

---

## Fork

**Website:** [https://git-fork.com/](https://git-fork.com/)

**Installation:**

```powershell
# Option 1: winget (recommended)
winget install --id Fork.Fork -e --source winget

# Option 2: Download installer from website
# https://git-fork.com/
```

**Features:**

- ✅ Currently free (evaluation model)
- ✅ Fast, lightweight
- ✅ Clean, modern UI
- ✅ Git LFS support
- ✅ Interactive rebase
- ⚠️ Future licensing model unclear

**Licensing:**

- **Free**: Currently in "evaluation" mode (free indefinitely)

---

## Tower

**Website:** [https://www.git-tower.com/windows](https://www.git-tower.com/windows)

**Installation:**

Download installer from website (30-day trial, then purchase).

**Features:**

- ✅ Premium UX and features
- ✅ Advanced Git operations (interactive rebase, cherry-pick, etc.)
- ✅ Conflict resolution wizard
- ✅ Multi-account support
- ⚠️ Paid software (€59-79/year depending on plan)

**Licensing:**

- **Trial**: 30 days free
- **Basic**: ~$65/user/year (€59) - Personal use
- **Pro**: ~$85/user/year (€79) - Enhanced features
- **Enterprise**: Contact for custom quote

> **⚠️ Pricing Note:** Tower uses Euro (€) pricing; USD amounts are approximate conversions. **These prices were accurate as of November 2025 but may change.** Educational institutions and students can apply for free licenses. Check the [official Tower pricing page](https://www.git-tower.com/pricing) for current rates.

---

**Last Verified:** 2025-11-25 (Windows installation links, pricing, and winget packages verified)
