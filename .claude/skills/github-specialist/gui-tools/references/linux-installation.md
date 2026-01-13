# Linux Installation Guide

Detailed installation instructions for Git GUI tools on Linux.

## GitKraken

**Download**: [https://www.gitkraken.com/download](https://www.gitkraken.com/download)

**Installation:**

```bash
# Debian/Ubuntu (.deb package)
wget https://release.gitkraken.com/linux/gitkraken-amd64.deb
sudo dpkg -i gitkraken-amd64.deb
sudo apt-get install -f  # Fix dependencies if needed

# Fedora/RHEL (.rpm package)
wget https://release.gitkraken.com/linux/gitkraken-amd64.rpm
sudo rpm -i gitkraken-amd64.rpm

# Snap (universal)
sudo snap install gitkraken --classic

# Flatpak
flatpak install flathub com.axosoft.GitKraken
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

## GitHub Desktop (Community Fork)

**Download**: [https://github.com/shiftkey/desktop](https://github.com/shiftkey/desktop)

**Installation:**

> **Note**: Visit the [releases page](https://github.com/shiftkey/desktop/releases) for the latest version. Replace version numbers below with current release.

```bash
# Debian/Ubuntu (.deb package)
wget https://github.com/shiftkey/desktop/releases/download/release-3.3.6-linux1/GitHubDesktop-linux-amd64-3.3.6-linux1.deb
sudo dpkg -i GitHubDesktop-linux-amd64-3.3.6-linux1.deb

# RPM-based distros
wget https://github.com/shiftkey/desktop/releases/download/release-3.3.6-linux1/GitHubDesktop-linux-x86_64-3.3.6-linux1.rpm
sudo rpm -i GitHubDesktop-linux-x86_64-3.3.6-linux1.rpm

# AppImage (portable)
wget https://github.com/shiftkey/desktop/releases/download/release-3.3.6-linux1/GitHubDesktop-linux-x86_64-3.3.6-linux1.AppImage
chmod +x GitHubDesktop-linux-x86_64-3.3.6-linux1.AppImage
./GitHubDesktop-linux-x86_64-3.3.6-linux1.AppImage
```

**Note**: This is a community-maintained fork of GitHub Desktop for Linux, not officially supported by GitHub.

---

## GitAhead

**Download**: [https://github.com/gitahead/gitahead/releases](https://github.com/gitahead/gitahead/releases)

**Note**: GitAhead development has slowed. Consider Gittyup (an active fork of GitAhead) as an alternative.

**Installation:**

```bash
# GitAhead (original) - Download AppImage from GitHub releases
# https://github.com/gitahead/gitahead/releases

# Gittyup (active fork) - Flatpak (recommended)
flatpak install flathub com.github.Murmele.Gittyup
```

**Features:**

- ✅ Free, open source (MIT license)
- ✅ Lightweight, fast
- ✅ Cross-platform
- ✅ Good for simple workflows
- ⚠️ Fewer features than commercial tools
- ⚠️ GitAhead: Development has slowed; Gittyup: Actively maintained fork

---

## SmartGit

**Download**: [https://www.syntevo.com/smartgit/download/](https://www.syntevo.com/smartgit/download/)

**Installation:**

> **Note**: Visit the [download page](https://www.syntevo.com/smartgit/download/) for the latest version. Replace version numbers below with current release.

```bash
# Debian/Ubuntu (.deb package)
wget https://www.syntevo.com/downloads/smartgit/smartgit-23_1_1.deb
sudo dpkg -i smartgit-23_1_1.deb

# Generic (tar.gz)
wget https://www.syntevo.com/downloads/smartgit/smartgit-linux-23_1_1.tar.gz
tar -xzf smartgit-linux-23_1_1.tar.gz
cd smartgit/bin
./smartgit.sh
```

**Features:**

- ✅ Cross-platform consistency
- ✅ Powerful features
- ✅ Free for non-commercial use
- ⚠️ Java-based (requires JRE)
- ⚠️ Commercial license required for business use

**Licensing:**

- **Free**: Non-commercial use (open-source developers, educational institutions, charities)
- **Subscription**: $89/user/year (commercial use)
- **Perpetual**: $139/user (commercial use, includes 1 year updates)

> **⚠️ Pricing Note:** **These prices were accurate as of November 2025 but may change.** Check the [official SmartGit purchase page](https://www.smartgit.dev/purchase/) for current rates and to apply for free non-commercial licenses.

---

## Built-in Tools (gitk, Git GUI)

```bash
# Install Git (includes gitk and git-gui)
# Debian/Ubuntu
sudo apt install git git-gui gitk

# Fedora/RHEL
sudo dnf install git git-gui gitk

# Arch
sudo pacman -S git tk

# Run gitk (repository visualizer)
gitk

# Run git-gui (commit GUI)
git gui
```

---

**Last Verified:** 2025-11-25 (Linux installation guides, package manager commands, and tool availability verified)
