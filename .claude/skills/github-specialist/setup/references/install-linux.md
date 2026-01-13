# Linux Installation

## Ubuntu/Debian

```bash
sudo apt update
sudo apt install git
```

## Fedora/RHEL

```bash
sudo dnf install git
```

## Arch Linux

```bash
sudo pacman -S git
```

## Verify Installation (Linux)

```bash
git --version
# Expected output: git version 2.52.0 (or newer)
```

## Linux-Specific Configuration

**Line ending configuration:**

```bash
git config --global core.autocrlf input
```

## Shell Integration (Optional) - Linux

### Bash

Add to `~/.bashrc`:

```bash
# Git-aware prompt (optional - requires git-prompt.sh)
# Ubuntu/Debian: usually at /usr/lib/git-core/git-sh-prompt
# Fedora/RHEL: usually at /usr/share/git-core/contrib/completion/git-prompt.sh
if [ -f /usr/lib/git-core/git-sh-prompt ]; then
  source /usr/lib/git-core/git-sh-prompt
  export PS1='\u@\h:\w$(__git_ps1 " (%s)")\$ '
fi

# Optional shell aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
```

Reload: `source ~/.bashrc`

### Zsh

Add to `~/.zshrc`:

```bash
# Git-aware prompt (oh-my-zsh has this built-in)
# If using oh-my-zsh, enable the 'git' plugin in ~/.zshrc:
# plugins=(git)

# Optional shell aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
```

Reload: `source ~/.zshrc`

## Global Gitignore (Optional) - Linux

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

# OS files
.DS_Store
Thumbs.db

# Build artifacts
node_modules/
dist/
build/
```
