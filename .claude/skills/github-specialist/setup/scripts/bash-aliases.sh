#!/usr/bin/env bash
# =============================================================================
# BASH ALIASES MANAGEMENT SCRIPT
# =============================================================================
# Manages git and Claude Code aliases with bash tab completion.
# Called by /git:bash-aliases slash command.
#
# CANONICAL ALIAS DEFINITIONS: ../references/alias-definitions.sh
# (Keep heredocs below in sync with alias-definitions.sh)
#
# Usage: bash-aliases.sh <operation>
#
# Operations:
#   --install-git-aliases     Add git aliases with tab completion to bashrc
#   --install-claude-aliases  Add Claude Code aliases to bashrc
#   --status                  Show installation status
#   --uninstall               Remove aliases from bashrc
#   --audit                   Comprehensive health check
#
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BASHRC="$HOME/.bashrc"

# Markers for idempotent bashrc modifications
GIT_ALIASES_MARKER="# Git aliases with completion (added by /git:bash-aliases)"
CLAUDE_ALIASES_MARKER="# Claude Code aliases (added by /git:bash-aliases)"

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

print_header() {
    echo ""
    echo "==============================================================="
    echo "  $1"
    echo "==============================================================="
}

print_section() {
    echo ""
    echo "---------------------------------------------------------------"
    echo "  $1"
    echo "---------------------------------------------------------------"
}

print_ok() {
    echo "[OK] $1"
}

print_warn() {
    echo "[WARN] $1"
}

print_fail() {
    echo "[FAIL] $1"
}

print_info() {
    echo "[INFO] $1"
}

contains_marker() {
    local file="$1"
    local marker="$2"
    [[ -f "$file" ]] && grep -qF "$marker" "$file"
}

# -----------------------------------------------------------------------------
# Component Installers
# -----------------------------------------------------------------------------

install_git_aliases() {
    print_header "Installing Git Aliases"

    if contains_marker "$BASHRC" "$GIT_ALIASES_MARKER"; then
        print_ok "Git aliases already configured in $BASHRC"
        return 0
    fi

    echo "Adding git aliases with tab completion to $BASHRC..."

    cat >> "$BASHRC" << 'GITALIASES'

# Git aliases with completion (added by /git:bash-aliases)
# Source git completion script (Git for Windows includes this)
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
    alias g='git'
    __git_complete g __git_main

    alias gs='git status'
    alias gco='git checkout'
    __git_complete gco _git_checkout
    alias gb='git branch'
    __git_complete gb _git_branch
    alias gm='git merge'
    __git_complete gm _git_merge
    alias gp='git pull'
    __git_complete gp _git_pull
    alias gps='git push'
    __git_complete gps _git_push
    alias gd='git diff'
    __git_complete gd _git_diff
    alias gl='git log --oneline --graph --decorate'
    __git_complete gl _git_log
    alias gst='git stash'
    __git_complete gst _git_stash
    alias ga='git add'
    __git_complete ga _git_add
    alias gcm='git commit'
    __git_complete gcm _git_commit
    alias gr='git rebase'
    __git_complete gr _git_rebase
    alias gcp='git cherry-pick'
    __git_complete gcp _git_cherry_pick
fi
GITALIASES

    print_ok "Git aliases added to $BASHRC"
    echo "    Aliases: g, gs, gco, gb, gm, gp, gps, gd, gl, gst, ga, gcm, gr, gcp"
}

install_claude_aliases() {
    print_header "Installing Claude Code Aliases"

    if contains_marker "$BASHRC" "$CLAUDE_ALIASES_MARKER"; then
        print_ok "Claude aliases already configured in $BASHRC"
        return 0
    fi

    echo "Adding Claude Code aliases to $BASHRC..."

    cat >> "$BASHRC" << 'CLAUDEALIASES'

# Claude Code aliases (added by /git:bash-aliases)
alias claude-cont='claude -c'                                         # Continue last conversation
alias claude-cont-yolo='claude -c --dangerously-skip-permissions'     # Continue + skip perms
alias claude-yolo='claude --dangerously-skip-permissions'             # Skip perms anywhere
alias claude-plan='claude --permission-mode plan'                     # Start in plan mode
alias claude-opus='claude --model opus'                               # Use Opus model
alias claude-sonnet='claude --model sonnet'                           # Use Sonnet model
alias claude-opus-yolo='claude --model opus --dangerously-skip-permissions'  # Opus + skip perms
alias claude-headless='claude -p --output-format json'                # Headless JSON output
CLAUDEALIASES

    print_ok "Claude Code aliases added to $BASHRC"
    echo "    Aliases: claude-cont, claude-yolo, claude-plan, claude-opus, claude-sonnet"
}

# -----------------------------------------------------------------------------
# Direct Operations
# -----------------------------------------------------------------------------

cmd_status() {
    print_header "Bash Aliases Status"

    echo ""
    echo "Git Aliases:"
    if contains_marker "$BASHRC" "$GIT_ALIASES_MARKER"; then
        print_ok "Configured in $BASHRC"
        echo "    Aliases: g, gs, gco, gb, gm, gp, gps, gd, gl, gst, ga, gcm, gr, gcp"
    else
        print_info "Not configured"
    fi

    echo ""
    echo "Claude Code Aliases:"
    if contains_marker "$BASHRC" "$CLAUDE_ALIASES_MARKER"; then
        print_ok "Configured in $BASHRC"
        echo "    Aliases: claude-cont, claude-yolo, claude-plan, claude-opus, claude-sonnet"
    else
        print_info "Not configured"
    fi
}

cmd_uninstall() {
    print_header "Uninstalling Bash Aliases"

    local modified=false

    # Note: We can't easily remove the exact blocks from bashrc
    # Instead, provide manual instructions
    echo ""
    echo "To remove aliases, edit ~/.bashrc and remove these sections:"
    echo ""

    if contains_marker "$BASHRC" "$GIT_ALIASES_MARKER"; then
        echo "  - Git aliases section (search for: '$GIT_ALIASES_MARKER')"
        modified=true
    fi

    if contains_marker "$BASHRC" "$CLAUDE_ALIASES_MARKER"; then
        echo "  - Claude aliases section (search for: '$CLAUDE_ALIASES_MARKER')"
        modified=true
    fi

    if ! $modified; then
        print_info "No aliases found in $BASHRC"
    else
        echo ""
        echo "Then run: source ~/.bashrc"
    fi
}

cmd_audit() {
    print_header "Bash Aliases Audit Report"

    local warnings=0

    echo ""

    # Git aliases check
    if contains_marker "$BASHRC" "$GIT_ALIASES_MARKER"; then
        print_ok "Git aliases: PASS - Configured"

        # Check if git-completion.bash is available
        if [[ -f /usr/share/git/completion/git-completion.bash ]] || \
           [[ -f /etc/bash_completion.d/git ]] || \
           [[ -f "$PROGRAMFILES/Git/etc/bash_completion.d/git-completion.bash" ]]; then
            print_ok "git-completion.bash: PASS - Found"
        else
            print_warn "git-completion.bash: WARN - Not found (tab completion may not work)"
            ((warnings++))
        fi
    else
        print_info "Git aliases: Not installed (optional)"
    fi

    echo ""

    # Claude aliases check
    if contains_marker "$BASHRC" "$CLAUDE_ALIASES_MARKER"; then
        print_ok "Claude aliases: PASS - Configured"

        # Check if claude is available
        if command -v claude &>/dev/null; then
            print_ok "claude CLI: PASS - Found"
        else
            print_warn "claude CLI: WARN - Not found in PATH"
            ((warnings++))
        fi
    else
        print_info "Claude aliases: Not installed (optional)"
    fi

    # Summary
    echo ""
    echo "==============================================================="
    if ((warnings > 0)); then
        echo "  Overall: PASS ($warnings warning(s))"
    else
        echo "  Overall: PASS"
    fi
    echo "==============================================================="
}

# -----------------------------------------------------------------------------
# Usage
# -----------------------------------------------------------------------------

usage() {
    echo "Usage: bash-aliases.sh <operation>"
    echo ""
    echo "Component Installation:"
    echo "  --install-git-aliases     Add git aliases with tab completion"
    echo "  --install-claude-aliases  Add Claude Code aliases"
    echo ""
    echo "Direct Operations:"
    echo "  --status                  Show installation status"
    echo "  --uninstall               Show uninstall instructions"
    echo "  --audit                   Comprehensive health check"
    echo ""
    echo "Git Aliases:"
    echo "  g, gs, gco, gb, gm, gp, gps, gd, gl, gst, ga, gcm, gr, gcp"
    echo ""
    echo "Claude Code Aliases:"
    echo "  claude-cont, claude-yolo, claude-plan, claude-opus, claude-sonnet"
}

# -----------------------------------------------------------------------------
# Main Dispatch
# -----------------------------------------------------------------------------

case "${1:-}" in
    --install-git-aliases)
        install_git_aliases
        ;;
    --install-claude-aliases)
        install_claude_aliases
        ;;
    --status)
        cmd_status
        ;;
    --uninstall)
        cmd_uninstall
        ;;
    --audit)
        cmd_audit
        ;;
    --help|-h)
        usage
        ;;
    *)
        echo "Error: Unknown operation '${1:-}'"
        echo ""
        usage
        exit 1
        ;;
esac
