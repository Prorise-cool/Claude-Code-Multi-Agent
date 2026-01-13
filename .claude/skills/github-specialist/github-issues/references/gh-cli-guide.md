# GitHub CLI (gh) Guide

Complete guide to installing, authenticating, and using the GitHub CLI for issue management.

## Installation

### macOS

```bash
# Homebrew (recommended)
brew install gh

# MacPorts
sudo port install gh
```

### Windows

```powershell
# winget (recommended)
winget install --id GitHub.cli

# Chocolatey
choco install gh

# Scoop
scoop install gh
```

### Linux

```bash
# Debian/Ubuntu
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y

# Fedora/RHEL/CentOS
sudo dnf install gh

# Arch Linux
sudo pacman -S github-cli
```

### Verify Installation

```bash
gh --version
# gh version 2.x.x (2024-xx-xx)
```

---

## Authentication

### Interactive Login (Recommended)

```bash
gh auth login
```

Follow the prompts to:

1. Choose GitHub.com or GitHub Enterprise
2. Choose authentication method (browser or token)
3. Complete authentication

### Token-Based Login

```bash
# Using environment variable
export GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
gh auth status

# Or pass token directly
gh auth login --with-token < token.txt
```

### Verify Authentication

```bash
gh auth status
# github.com
#   Logged in to github.com account username (keyring)
#   Token: ghp_************************************
#   Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

### Authentication for Private Repos

For private repositories, ensure your token has:

- `repo` scope (full control of private repositories)

---

## Issue Commands Reference

### List Issues

```bash
# Basic list (open issues in current repo)
gh issue list

# All states
gh issue list --state all

# With search
gh issue list --search "keyword"

# Specific repo
gh issue list --repo owner/repo

# Filter by label
gh issue list --label "bug"

# Filter by assignee
gh issue list --assignee @me

# Limit results
gh issue list --limit 50

# JSON output
gh issue list --json number,title,state,labels
```

### View Issue

```bash
# View in terminal
gh issue view 123

# With comments
gh issue view 123 --comments

# JSON output
gh issue view 123 --json title,body,comments,labels,state

# Open in browser
gh issue view 123 --web
```

### Search Issues

```bash
# Basic search
gh issue list --search "error message"

# Search with qualifiers
gh issue list --search "is:open label:bug"

# Author search
gh issue list --search "author:username"

# Combined
gh issue list --search "is:closed label:bug milestone:v1.0"
```

---

## Advanced Usage

### Output Formatting

```bash
# JSON output
gh issue list --json number,title,state

# Custom template
gh issue list --template '{{range .}}#{{.number}} {{.title}}{{"\n"}}{{end}}'

# Pipe to jq for processing
gh issue list --json number,title | jq '.[].title'
```

### Combining with Other Tools

```bash
# Filter with grep
gh issue list --json title | grep -i "error"

# Count issues
gh issue list --json number | jq 'length'

# Export to file
gh issue list --json number,title,state > issues.json
```

### Rate Limits

- **Authenticated:** 5,000 requests/hour
- **Unauthenticated:** 60 requests/hour

Check current status:

```bash
gh api rate_limit
```

---

## Troubleshooting

### "gh: command not found"

GitHub CLI not installed. Follow installation steps above.

### "authentication required"

Run `gh auth login` to authenticate.

### "repository not found"

- Check repository path (owner/repo)
- Verify you have access to private repositories
- Ensure correct authentication scopes

### Rate limit exceeded

Wait for rate limit reset or authenticate for higher limits:

```bash
gh api rate_limit --jq '.rate.reset | strftime("%Y-%m-%d %H:%M:%S")'
```

---

## Related Documentation

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub CLI Issue Commands](https://cli.github.com/manual/gh_issue)
