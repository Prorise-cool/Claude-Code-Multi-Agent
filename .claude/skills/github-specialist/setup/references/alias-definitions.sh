# =============================================================================
# CENTRALIZED ALIAS DEFINITIONS
# =============================================================================
# CANONICAL LOCATION: plugins/git/skills/setup/references/alias-definitions.sh
#
# This file is the single source of truth for bash alias definitions.
# Changes here propagate to:
#   - /git:bash-aliases command (installer script)
#   - bashrc-claude.sh (template)
#
# To use directly (advanced): source this file from ~/.bashrc AFTER
# sourcing git-completion.bash.
# =============================================================================

# -----------------------------------------------------------------------------
# GIT ALIASES WITH TAB COMPLETION
# -----------------------------------------------------------------------------
# Requires git-completion.bash to be sourced first.

# Source git completion if available
if [ -f /usr/share/git/completion/git-completion.bash ]; then
    source /usr/share/git/completion/git-completion.bash
elif [ -f /etc/bash_completion.d/git ]; then
    source /etc/bash_completion.d/git
elif [ -f "$PROGRAMFILES/Git/etc/bash_completion.d/git-completion.bash" ]; then
    source "$PROGRAMFILES/Git/etc/bash_completion.d/git-completion.bash"
fi

# Helper to check if function exists
_function_exists() {
    declare -f -F "$1" > /dev/null
    return $?
}

# Add completion to git aliases (requires git-completion.bash loaded above)
if type __git_complete &>/dev/null; then
    # Core git alias
    alias g='git'
    __git_complete g __git_main

    # Status
    alias gs='git status'

    # Checkout
    alias gco='git checkout'
    __git_complete gco _git_checkout

    # Branch
    alias gb='git branch'
    __git_complete gb _git_branch

    # Merge
    alias gm='git merge'
    __git_complete gm _git_merge

    # Pull
    alias gp='git pull'
    __git_complete gp _git_pull

    # Push
    alias gps='git push'
    __git_complete gps _git_push

    # Diff
    alias gd='git diff'
    __git_complete gd _git_diff

    # Log (pretty format)
    alias gl='git log --oneline --graph --decorate'
    __git_complete gl _git_log

    # Stash
    alias gst='git stash'
    __git_complete gst _git_stash

    # Add
    alias ga='git add'
    __git_complete ga _git_add

    # Commit
    alias gcm='git commit'
    __git_complete gcm _git_commit

    # Rebase
    alias gr='git rebase'
    __git_complete gr _git_rebase

    # Cherry-pick
    alias gcp='git cherry-pick'
    __git_complete gcp _git_cherry_pick
fi

# -----------------------------------------------------------------------------
# CLAUDE CODE ALIASES
# -----------------------------------------------------------------------------

# Session management
alias claude-cont='claude -c'                                         # Continue last conversation
alias claude-cont-yolo='claude -c --dangerously-skip-permissions'     # Continue + skip perms

# Permission modes
alias claude-yolo='claude --dangerously-skip-permissions'             # Skip perms anywhere
alias claude-plan='claude --permission-mode plan'                     # Start in plan mode

# Model selection
alias claude-opus='claude --model opus'                               # Use Opus model
alias claude-sonnet='claude --model sonnet'                           # Use Sonnet model
alias claude-opus-yolo='claude --model opus --dangerously-skip-permissions'  # Opus + skip perms

# Scripting/automation
alias claude-headless='claude -p --output-format json'                # Headless JSON output
