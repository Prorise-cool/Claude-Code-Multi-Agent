# macOS Installation Guide

Detailed installation instructions for Git GUI tools on macOS.

## GitKraken

```bash
# Homebrew Cask
brew install --cask gitkraken

# Or download from website
# https://www.gitkraken.com/download
```

**Same features and licensing as Windows version**:

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

```bash
# Homebrew Cask
brew install --cask sourcetree

# Or download from website
# https://www.sourcetreeapp.com/
```

**Features:**

- ✅ Free for all uses (private and public repos)
- ✅ Git LFS support
- ✅ Git Flow integration
- ✅ Visual diff/merge tool
- ✅ Atlassian (Bitbucket) integration
- ⚠️ Heavier application, slower startup

**Note**: macOS version has slightly different UI but same functionality.

**Licensing:**

- **Free**: All features, no limitations

---

## GitHub Desktop

```bash
# Homebrew Cask
brew install --cask github

# Or download from website
# https://desktop.github.com/
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

```bash
# Homebrew Cask
brew install --cask fork

# Or download from website
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

```bash
# Download from website
# https://www.git-tower.com/mac
```

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

## Built-in Tools (gitk, Git GUI)

```bash
# These come with Git installation via Homebrew
brew install git

# Run gitk (repository visualizer)
gitk

# Run git-gui (commit GUI)
git gui
```

---

**Last Verified:** 2025-11-25 (macOS installation guides, Homebrew casks, and commands verified)
