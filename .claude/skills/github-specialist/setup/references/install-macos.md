# macOS Installation

## Option 1: Xcode Command Line Tools (Built-in)

**Best for**: Quick setup using system Git.

```bash
xcode-select --install
```

**Note**: May not be the latest version of Git, but adequate for most uses.

## Option 2: Homebrew (Recommended for Latest Version)

**Best for**: Getting the latest Git version.

**Prerequisites**: Install Homebrew first: [https://brew.sh](https://brew.sh)

```bash
brew install git
```

## Verify Installation (macOS)

```bash
git --version
# Expected output: git version 2.52.0 (or newer)
```

## macOS-Specific Configuration

**Line ending configuration:**

```bash
git config --global core.autocrlf input
```

**Note**: macOS uses **Zsh** as the default shell (since macOS Catalina 10.15).

## Shell Integration (Optional) - macOS

### Zsh (Default Shell)

Add to `~/.zshrc`:

```bash
# Git-aware prompt (oh-my-zsh has this built-in)
# If using oh-my-zsh, enable the 'git' plugin in ~/.zshrc:
# plugins=(git)

# Optional shell aliases (personal preference)
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
```

Reload: `source ~/.zshrc`

### Bash (Legacy)

If using Bash (not default since macOS Catalina), add to `~/.bash_profile`:

```bash
# Git-aware prompt (requires Homebrew git)
if [ -f /usr/local/etc/bash_completion.d/git-prompt.sh ]; then
  source /usr/local/etc/bash_completion.d/git-prompt.sh
  export PS1='\u@\h:\w$(__git_ps1 " (%s)")\$ '
fi

# Optional shell aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
```

Reload: `source ~/.bash_profile`

## Global Gitignore (Optional) - macOS

Create `~/.config/git/ignore` for patterns to ignore globally:

```bash
mkdir -p ~/.config/git
nano ~/.config/git/ignore
```

Example content:

```text
# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# macOS system files
.DS_Store
.AppleDouble
.LSOverride

# Thumbnails
._*

# Build artifacts
node_modules/
dist/
build/
```
