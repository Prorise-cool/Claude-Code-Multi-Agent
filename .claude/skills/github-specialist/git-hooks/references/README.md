# Git Hooks References

This directory contains detailed reference documentation for the hooks skill, following a progressive disclosure pattern for optimal token efficiency.

## Progressive Disclosure Architecture

The hooks skill uses a layered approach:

**Layer 1 (Always Loaded):**

- SKILL.md - Main skill file with overview, quick start, and core capabilities

**Layer 2 (Conditional - Load as Needed):**

- Reference files in this directory - Detailed guides loaded when user needs depth

**Layer 3 (External):**

- Official documentation via MCP servers (microsoft-learn, context7, perplexity, etc.)

## Reference Files

### Framework-Specific Guides

**Status: Placeholder** - Can be created as needed based on demand

- `husky-net-guide.md` - Comprehensive Husky.Net guide for .NET developers
- `lefthook-guide.md` - Comprehensive lefthook guide with advanced patterns
- `husky-guide.md` - Comprehensive Husky (JavaScript) guide
- `pre-commit-guide.md` - Comprehensive pre-commit framework guide for Python

### Topic-Specific Guides

**Created:**

- `framework-comparison.md` - Detailed framework comparison and selection guidance
- `performance-optimization.md` - Comprehensive performance optimization strategies

**Planned (create as needed):**

- `conventional-commits.md` - Conventional Commits specification and tooling details
- `secret-scanning.md` - Secret scanning deep dive (gitleaks vs TruffleHog vs detect-secrets)
- `testing-strategies.md` - Testing and validation patterns for git hooks
- `ci-cd-integration.md` - CI/CD enforcement patterns and GitHub Actions examples
- `team-collaboration.md` - Team adoption strategies and policies

## When to Create New References

Create a new reference file when:

1. **Topic requires >500 tokens** of detail beyond what's in SKILL.md
2. **User frequently requests** specific deep-dive information
3. **Official documentation is scattered** and needs consolidation
4. **Complex examples** require extended explanation

## Token Budget Guidelines

- **SKILL.md target:** ~10-15k tokens (comprehensive but scannable)
- **Reference files target:** ~2-5k tokens each (focused deep dives)
- **Total skill budget:** ~30-50k tokens (including all references)

Current allocation:

- SKILL.md: ~12,500 tokens
- framework-comparison.md: ~4,000 tokens
- performance-optimization.md: ~3,500 tokens
- examples/: ~1,500 tokens
- **Total:** ~21,500 tokens

## Usage Pattern

When a user needs detailed information:

1. **SKILL.md provides overview** and quick start
2. **User identifies they need more detail** on specific topic
3. **Reference file is loaded** providing comprehensive guidance
4. **MCP servers provide official docs** for latest information

This approach balances comprehensiveness with token efficiency.

## Contributing New References

When creating new reference files:

1. **Focus on one topic** - Don't try to cover everything
2. **Link to official docs** - Use MCP servers for latest information
3. **Include examples** - Practical, copy-paste ready configurations
4. **Follow template structure:**
   - Overview
   - When to use this reference
   - Detailed content (organized logically)
   - Examples
   - Troubleshooting (if applicable)
   - Related references
   - Last verified date

## Maintenance

Reference files should be updated when:

- Official framework documentation changes significantly
- New major versions are released with breaking changes
- User feedback indicates outdated or unclear information
- Better patterns or tools emerge

**Last Updated:** 2025-11-25
