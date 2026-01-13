# Web Fallback Strategies

When the GitHub CLI (gh) is unavailable, these fallback methods provide access to GitHub issues.

## Fallback Priority

1. **WebSearch tool** - Fast, works across public repos
2. **firecrawl MCP** - Better parsing of results
3. **Direct URL construction** - Manual but reliable
4. **GitHub API** - Programmatic but rate-limited

---

## Method 1: WebSearch Tool

Use Claude Code's WebSearch tool with site-specific queries:

```text
Query: site:github.com/owner/repo/issues keyword
```

### Examples

```text
# Search Claude Code issues for hooks
site:github.com/anthropics/claude-code/issues hooks

# Search for specific error
site:github.com/anthropics/claude-code/issues "path doubling"

# Include pull requests
site:github.com/anthropics/claude-code keyword
```

### Parsing Results

WebSearch returns search result snippets. Look for:

- Issue number in URL (e.g., `/issues/11984`)
- Title and description snippets
- State indicators (open, closed) if visible

---

## Method 2: firecrawl MCP

Use the firecrawl MCP server to scrape GitHub issue pages:

```text
URL: https://github.com/owner/repo/issues?q=keyword
```

### Example Usage

```javascript
// Scrape issue list page
mcp__firecrawl__firecrawl_scrape({
  url: "https://github.com/anthropics/claude-code/issues?q=hooks",
  formats: ["markdown"]
})
```

### Advantages

- Better structured output than WebSearch
- Can extract issue details more reliably
- Handles pagination

---

## Method 3: Direct URL Construction

Construct GitHub search URLs manually:

### Search URLs

```text
# Basic search
https://github.com/owner/repo/issues?q=keyword

# Filter by state
https://github.com/owner/repo/issues?q=keyword+is:open
https://github.com/owner/repo/issues?q=keyword+is:closed

# Filter by label
https://github.com/owner/repo/issues?q=keyword+label:bug

# Combined filters
https://github.com/owner/repo/issues?q=keyword+is:open+label:bug
```

### View Specific Issue

```text
https://github.com/owner/repo/issues/11984
```

Use WebFetch to retrieve content:

```text
WebFetch: https://github.com/anthropics/claude-code/issues/11984
Prompt: Extract issue title, state, labels, and description
```

---

## Method 4: GitHub API (Unauthenticated)

Direct API access with rate limits (60 requests/hour unauthenticated):

### API Endpoints

```text
# List issues
GET https://api.github.com/repos/owner/repo/issues

# Search issues
GET https://api.github.com/search/issues?q=keyword+repo:owner/repo

# Get specific issue
GET https://api.github.com/repos/owner/repo/issues/11984
```

### Using with WebFetch

```text
WebFetch: https://api.github.com/repos/anthropics/claude-code/issues?state=all&per_page=10
Prompt: Parse the JSON and list issues with number, title, and state
```

### Rate Limit Considerations

- Unauthenticated: 60 requests/hour
- Check limit: `curl -I https://api.github.com/rate_limit`
- Headers include remaining quota

---

## Fallback Detection Logic

```bash
# Check gh availability
check_gh_available() {
    if command -v gh &> /dev/null; then
        # Check if authenticated (optional)
        if gh auth status &> /dev/null; then
            echo "gh_authenticated"
        else
            echo "gh_unauthenticated"
        fi
    else
        echo "gh_unavailable"
    fi
}

# Use result to choose method
status=$(check_gh_available)
case $status in
    gh_authenticated)
        # Full gh CLI access
        gh issue list --repo owner/repo --search "keyword"
        ;;
    gh_unauthenticated)
        # gh works for public repos
        gh issue list --repo owner/repo --search "keyword"
        ;;
    gh_unavailable)
        # Fall back to web methods
        echo "Falling back to WebSearch..."
        ;;
esac
```

---

## Comparison of Methods

| Method | Speed | Auth Required | Rate Limit | Parsing Quality |
| --- | --- | --- | --- | --- |
| gh CLI | Fast | Recommended | 5000/hr | Excellent |
| WebSearch | Fast | No | N/A | Moderate |
| firecrawl | Medium | No | Varies | Good |
| Direct URL + WebFetch | Slow | No | N/A | Variable |
| GitHub API | Fast | Optional | 60/hr (unauth) | Excellent |

---

## Best Practices

1. **Always try gh first** - It's the most reliable method
2. **Cache results** - Avoid repeated requests for same query
3. **Handle failures gracefully** - Have multiple fallback layers
4. **Inform user** - Let them know which method is being used
5. **Rate limit awareness** - Don't exhaust limits with repeated queries

---

## Example Fallback Workflow

```text
1. Check: Is gh installed?
   - Yes: Use gh issue list
   - No: Continue to step 2

2. Try: WebSearch with site:github.com query
   - Success: Parse and return results
   - Failure: Continue to step 3

3. Try: WebFetch on search URL
   - Success: Parse HTML and return results
   - Failure: Report inability to search

4. Report: Method used and any limitations
```

---

## Related Documentation

- [GitHub API Documentation](https://docs.github.com/en/rest/issues)
- [GitHub Search Documentation](https://docs.github.com/en/search-github)
