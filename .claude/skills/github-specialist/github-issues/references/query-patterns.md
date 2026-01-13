# Query Patterns and Filter Syntax

Comprehensive guide to GitHub issue search syntax and filtering options.

## Basic Search Syntax

### Keywords

Search matches title and body text:

```bash
# Single keyword
gh issue list --search "authentication"

# Multiple keywords (AND)
gh issue list --search "authentication error"

# Exact phrase
gh issue list --search '"exact phrase here"'
```

### Search Qualifiers

GitHub supports special qualifiers in search:

```bash
# By state
gh issue list --search "is:open"
gh issue list --search "is:closed"

# By label
gh issue list --search "label:bug"
gh issue list --search "label:\"help wanted\""

# By author
gh issue list --search "author:username"

# By assignee
gh issue list --search "assignee:username"

# By milestone
gh issue list --search "milestone:v1.0"
```

---

## Filter Flags

### State Filter

```bash
# Open only (default)
gh issue list --state open

# Closed only
gh issue list --state closed

# All states
gh issue list --state all
```

### Label Filter

```bash
# Single label
gh issue list --label "bug"

# Multiple labels (AND - must have ALL labels)
gh issue list --label "bug" --label "high-priority"

# Labels with spaces
gh issue list --label "help wanted"
```

### Assignee Filter

```bash
# Specific user
gh issue list --assignee username

# Self
gh issue list --assignee @me

# Unassigned
gh issue list --search "no:assignee"
```

### Author Filter

```bash
# Issues created by user
gh issue list --author username
```

### Milestone Filter

```bash
# Specific milestone
gh issue list --milestone "v1.0"

# No milestone
gh issue list --search "no:milestone"
```

---

## Combining Filters

### CLI Flags

```bash
# Label + state
gh issue list --label "bug" --state open

# Author + label + state
gh issue list --author username --label "bug" --state closed

# Assignee + label
gh issue list --assignee @me --label "high-priority"
```

### Search Qualifiers (More Flexible)

```bash
# Complex queries
gh issue list --search "is:open label:bug author:username"

# Excluding labels
gh issue list --search "is:open -label:wontfix"

# Multiple conditions
gh issue list --search "is:closed label:bug label:confirmed"
```

---

## Date Filters

Search by creation or update date:

```bash
# Created after date
gh issue list --search "created:>2024-01-01"

# Created before date
gh issue list --search "created:<2024-06-01"

# Created in range
gh issue list --search "created:2024-01-01..2024-06-01"

# Updated recently
gh issue list --search "updated:>2024-11-01"

# Closed after date
gh issue list --search "closed:>2024-01-01"
```

---

## Sort and Limit

### Limit Results

```bash
# Limit to 10 results
gh issue list --limit 10

# Limit to 50
gh issue list --limit 50

# Default is 30
```

### Sort Order

Sort is controlled via search qualifiers:

```bash
# Sort by created date (newest first)
gh issue list --search "sort:created-desc"

# Sort by created date (oldest first)
gh issue list --search "sort:created-asc"

# Sort by updated date
gh issue list --search "sort:updated-desc"

# Sort by comments count
gh issue list --search "sort:comments-desc"
```

---

## Common Query Patterns

### Find Bug Reports

```bash
gh issue list --repo owner/repo --label "bug" --state open
```

### Find Feature Requests

```bash
gh issue list --repo owner/repo --label "enhancement" --state open
```

### Find Issues Needing Help

```bash
gh issue list --repo owner/repo --label "help wanted"
```

### Find Recent Activity

```bash
gh issue list --repo owner/repo --search "updated:>2024-11-01" --state all
```

### Find Closed Fixed Bugs

```bash
gh issue list --repo owner/repo --label "bug" --state closed --limit 20
```

### Find Issues with Specific Error

```bash
gh issue list --repo owner/repo --search "ENOENT" --state all
gh issue list --repo owner/repo --search "TypeError" --state all
gh issue list --repo owner/repo --search "path doubling" --state all
```

---

## Output Customization

### JSON Fields

Available fields for `--json`:

```bash
# Common fields
gh issue list --json number,title,state,labels,createdAt

# Full list
gh issue list --json number,title,body,state,labels,assignees,author,comments,createdAt,updatedAt,closedAt,milestone,url
```

### Template Output

```bash
# Custom format
gh issue list --template '{{range .}}#{{.number}} [{{.state}}] {{.title}}{{"\n"}}{{end}}'

# With labels
gh issue list --template '{{range .}}#{{.number}} {{.title}} ({{range .labels}}{{.name}}, {{end}}){{"\n"}}{{end}}'
```

---

## Related Documentation

- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
- [gh issue list Reference](https://cli.github.com/manual/gh_issue_list)
