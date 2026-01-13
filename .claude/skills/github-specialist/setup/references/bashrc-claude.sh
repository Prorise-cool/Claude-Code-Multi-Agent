# =============================================================================
# BASH CONFIGURATION TEMPLATE FOR CLAUDE CODE DEVELOPMENT
# =============================================================================
# CANONICAL LOCATION: plugins/git/skills/setup/references/bashrc-claude.sh
#
# Usage: Source this file from ~/.bashrc (Git Bash on Windows):
#   export CLAUDE_PLUGINS_REPO="/path/to/claude-code-plugins"
#   source "$CLAUDE_PLUGINS_REPO/plugins/git/skills/setup/references/bashrc-claude.sh"
#
# This file provides a complete environment including:
#   - History configuration (cross-terminal sync)
#   - Git aliases with tab completion (g, gco, gb, etc.)
#   - Claude Code CLI completion (claude, ccp, etc.)
#
# Main aliases:
#   ccp          - cd to plugins repo + load local plugins
#   ccp-yolo     - same + skip permission prompts
#   ccp-dev      - load local plugins (when already in repo)
#   claude-yolo  - skip permissions anywhere
#   claude-cont  - continue last conversation
#
# For installation/management, use:
#   /git:bash-aliases - Install/manage git and Claude aliases
# =============================================================================

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# HISTORY CONFIGURATION (fixes Windows Terminal history persistence)
# -----------------------------------------------------------------------------
export HISTFILE=~/.bash_history
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth:erasedups  # Ignore duplicates and space-prefixed

# Enable history appending and cross-session sync
# This pattern enables picking up commands from OTHER terminal tabs:
# - history -a: Append current command to file
# - history -c: Clear in-memory history
# - history -r: Reload from file (picks up commands from other terminals)
shopt -s histappend
PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

# -----------------------------------------------------------------------------
# GIT BASH COMPLETION (Tab completion for git commands and aliases)
# -----------------------------------------------------------------------------
# Canonical alias definitions: plugins/git/skills/setup/references/alias-definitions.sh
# (This file includes them inline for portability - keep in sync with alias-definitions.sh)
#
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
    # -----------------------------------------------------
    # Common bash aliases with git completion
    # -----------------------------------------------------
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

    # NOTE: Auto-generation of g<alias> from .gitconfig was removed due to
    # severe startup performance issues (~2s overhead) caused by command
    # substitution in for loops within interactive mode.
    # Add custom git aliases manually above if needed.
fi

# -----------------------------------------------------------------------------
# CLAUDE CODE COMPLETION (Tab completion for claude CLI and aliases)
# -----------------------------------------------------------------------------
# Based on: https://github.com/cldotdev/claude-bash-completion

_claude_completion() {
    local cur prev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Slash commands (built-in)
    local slash_commands="/add-dir /agents /bashes /bug /clear /compact /config /context /cost /doctor /exit /export /help /hooks /ide /init /install-github-app /login /logout /mcp /memory /model /output-style /permissions /plugin /pr-comments /privacy-settings /release-notes /resume /review /rewind /sandbox /security-review /stats /status /statusline /terminal-setup /todos /usage /vim"

    # CLI options
    local cli_options="-p --print -c --continue -r --resume -v --version -h --help -d --debug --verbose --model --agent --permission-mode --dangerously-skip-permissions --output-format --system-prompt --append-system-prompt --add-dir --plugin-dir --mcp-config --allowed-tools --disallowed-tools --ide --chrome"

    # Model names
    local models="opus sonnet haiku claude-opus-4-5-20250929 claude-sonnet-4-5-20250929"

    # Permission modes
    local permission_modes="default plan acceptEdits bypassPermissions delegate dontAsk"

    # Output formats
    local output_formats="text json stream-json"

    # Complete based on previous word
    case "$prev" in
        --model)
            COMPREPLY=( $(compgen -W "$models" -- "$cur") )
            return 0
            ;;
        --permission-mode)
            COMPREPLY=( $(compgen -W "$permission_modes" -- "$cur") )
            return 0
            ;;
        --output-format)
            COMPREPLY=( $(compgen -W "$output_formats" -- "$cur") )
            return 0
            ;;
        --plugin-dir|--add-dir|--mcp-config)
            # Complete directories/files
            COMPREPLY=( $(compgen -d -- "$cur") )
            return 0
            ;;
    esac

    # Slash command completion
    if [[ "$cur" == /* ]]; then
        # Add custom commands from ~/.claude/commands/
        local custom_commands=""
        local commands_dir="$HOME/.claude/commands"
        if [[ -d "$commands_dir" ]]; then
            custom_commands=$(find -L "$commands_dir" -type f -name "*.md" 2>/dev/null | \
                sed "s|^$commands_dir/||" | \
                sed 's/\.md$//' | \
                sed 's|/|:|g' | \
                sed 's/^/\//')
        fi
        COMPREPLY=( $(compgen -W "$slash_commands $custom_commands" -- "$cur") )
        return 0
    fi

    # CLI option completion
    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "$cli_options" -- "$cur") )
        return 0
    fi
}

# Register completion for claude and all aliases
complete -F _claude_completion claude
complete -F _claude_completion claude-yolo
complete -F _claude_completion claude-cont
complete -F _claude_completion claude-cont-yolo
complete -F _claude_completion claude-plan
complete -F _claude_completion claude-opus
complete -F _claude_completion claude-sonnet
complete -F _claude_completion claude-opus-yolo
complete -F _claude_completion claude-headless

# Completion for ccp/ccp-dev functions (same options as claude)
complete -F _claude_completion ccp
complete -F _claude_completion ccp-dev
complete -F _claude_completion ccp-yolo

# -----------------------------------------------------------------------------
# PLUGIN DEVELOPMENT (claude-code-plugins repo)
# -----------------------------------------------------------------------------
# Set CLAUDE_PLUGINS_REPO to your local plugin repo path:
#   export CLAUDE_PLUGINS_REPO="/path/to/claude-code-plugins"

# Load all local plugins from dev repo (use when already in plugins repo)
# Usage: ccp-dev [additional-args]
ccp-dev() {
  local repo_dir="${CLAUDE_PLUGINS_REPO:-}"
  if [[ -z "$repo_dir" ]]; then
    echo "Error: CLAUDE_PLUGINS_REPO not set. Add to ~/.bashrc:"
    echo "  export CLAUDE_PLUGINS_REPO=\"/path/to/claude-code-plugins\""
    return 1
  fi
  local plugin_dir="$repo_dir/plugins"
  local plugins=""
  for dir in "$plugin_dir"/*/; do
    if [[ -f "${dir}.claude-plugin/plugin.json" ]]; then
      plugins="$plugins --plugin-dir $dir"
    fi
  done
  claude $plugins "$@"
}

# Full workflow: cd to repo + load local plugins
# Usage: ccp [additional-args]
ccp() {
  local repo_dir="${CLAUDE_PLUGINS_REPO:-}"
  if [[ -z "$repo_dir" ]]; then
    echo "Error: CLAUDE_PLUGINS_REPO not set"
    return 1
  fi
  cd "$repo_dir" && ccp-dev "$@"
}

# Combined: cd to plugins repo + local plugins + skip permissions
# Usage: ccp-yolo [additional-args]
ccp-yolo() {
  ccp --dangerously-skip-permissions "$@"
}

# -----------------------------------------------------------------------------
# SESSION MANAGEMENT
# -----------------------------------------------------------------------------
alias claude-cont='claude -c'                                         # Continue last conversation
alias claude-cont-yolo='claude -c --dangerously-skip-permissions'     # Continue + skip perms

# -----------------------------------------------------------------------------
# PERMISSION MODES
# -----------------------------------------------------------------------------
alias claude-yolo='claude --dangerously-skip-permissions'             # Skip perms anywhere
alias claude-plan='claude --permission-mode plan'                     # Start in plan mode

# -----------------------------------------------------------------------------
# MODEL SELECTION
# -----------------------------------------------------------------------------
alias claude-opus='claude --model opus'                               # Use Opus model
alias claude-sonnet='claude --model sonnet'                           # Use Sonnet model
alias claude-opus-yolo='claude --model opus --dangerously-skip-permissions'  # Opus + skip perms

# -----------------------------------------------------------------------------
# SCRIPTING/AUTOMATION
# -----------------------------------------------------------------------------
alias claude-headless='claude -p --output-format json'                # Headless JSON output

# -----------------------------------------------------------------------------
