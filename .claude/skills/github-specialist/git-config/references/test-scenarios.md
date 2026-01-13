# Git Configuration Skill - Test Scenarios

This document contains test scenarios for validating the git-config skill's activation and response quality.

## Table of Contents

- [Scenario 1: Alias Setup](#scenario-1-alias-setup)
- [Scenario 2: Credential Management](#scenario-2-credential-management)
- [Scenario 3: Performance Optimization](#scenario-3-performance-optimization)
- [Scenario 4: Line Ending Configuration](#scenario-4-line-ending-configuration)
- [Scenario 5: Background Maintenance](#scenario-5-background-maintenance)
- [Scenario 6: Repository-Level Configuration](#scenario-6-repository-level-configuration-overrides)
- [Scenario 7: Troubleshooting Credentials](#scenario-7-troubleshooting-credential-issues)
- [Scenario 8: Rerere Configuration](#scenario-8-rerere-configuration-and-management)
- [Scenario 9: Clone Shortcuts](#scenario-9-clone-shortcuts-setup)
- [Evaluation Summary](#evaluation-driven-development)
- [Multi-Model Testing](#multi-model-testing)
- [Common Real-World Scenarios](#common-real-world-usage-scenarios)

---

## Scenario 1: Alias Setup

- **Query**: "How do I set up Git aliases for common operations?"
- **Expected**: Skill activates, provides alias setup commands from the Aliases section
- **Reference**: [aliases.md](aliases.md)

## Scenario 2: Credential Management

- **Query**: "Configure Git to use GitHub CLI for authentication"
- **Expected**: Skill activates, guides to credential-management.md reference
- **Reference**: [credential-management.md](credential-management.md)

## Scenario 3: Performance Optimization

- **Query**: "My Git is slow on large repos"
- **Expected**: Skill activates, provides performance optimization settings from Quick Start and Performance Settings sections
- **Reference**: [global-configuration.md#performance-settings](global-configuration.md#performance-settings)

## Scenario 4: Line Ending Configuration

- **Query**: "Set up .gitattributes for cross-platform development"
- **Expected**: Skill activates, provides .gitattributes template and normalization guidance
- **Reference**: See line-endings skill for comprehensive guidance

## Scenario 5: Background Maintenance

- **Query**: "Enable Git background maintenance"
- **Expected**: Skill activates, provides maintenance setup commands from Maintenance section
- **Reference**: [global-configuration.md#maintenance](global-configuration.md#maintenance)

## Scenario 6: Repository-Level Configuration Overrides

- **Query**: "How do I override global Git configuration for a specific repository?"
- **Expected**: Skill activates, explains local vs global config priority, provides examples of repo-specific overrides
- **Reference**: SKILL.md Repository-Level Configuration section

## Scenario 7: Troubleshooting Credential Issues

- **Query**: "Git keeps asking for credentials or my stored credentials aren't working"
- **Expected**: Skill activates, guides through credential-management.md reference, helps diagnose credential helper setup
- **Reference**: [credential-management.md](credential-management.md), [troubleshooting.md#credential-issues](troubleshooting.md#credential-issues)

## Scenario 8: Rerere Configuration and Management

- **Query**: "How do I enable Git to remember how I resolved merge conflicts?"
- **Expected**: Skill activates, explains rerere setup and usage from configuration-basics.md reference
- **Reference**: [configuration-basics.md#managing-rerere-reuse-recorded-resolution](configuration-basics.md#managing-rerere-reuse-recorded-resolution)

## Scenario 9: Clone Shortcuts Setup

- **Query**: "Set up shortcuts for cloning repositories (like 'git clone gh:username/repo')"
- **Expected**: Skill activates, provides url.insteadOf configuration from aliases.md reference
- **Reference**: [aliases.md#clone-shortcuts](aliases.md#clone-shortcuts)

---

## Evaluation-Driven Development

**Baseline:** Without the skill, Claude provides general Git configuration guidance but lacks structured organization, platform-specific examples, and comprehensive troubleshooting.

**With Skill:** Progressive disclosure (quick answers in SKILL.md, detailed guidance in references), structured navigation, platform-specific guidance for Windows/macOS/Linux, and copy-paste ready commands.

**Test Coverage:** 9 scenarios covering:

- Basic use (aliases, performance, maintenance)
- Advanced use (credentials, line endings, repo config)
- Troubleshooting (credential issues, rerere)
- Shortcuts (clone shortcuts, url.insteadOf)

---

## Multi-Model Testing

| Model | Status | Notes |
| --- | --- | --- |
| Sonnet | Verified | Optimal performance, efficient reference navigation |
| Haiku | Test | Quick lookups and quick reference preference |
| Opus | Test | Complex troubleshooting scenarios |

---

## Common Real-World Usage Scenarios

This skill has been used to solve real-world configuration challenges. See [troubleshooting.md#common-real-world-scenarios](troubleshooting.md#common-real-world-scenarios) for detailed examples:

1. **Corporate Proxy Fetch Timeouts** - Reducing `fetch.parallel` for restrictive corporate networks
2. **WSL Filesystem Performance** - Using correct Git binary for filesystem location
3. **Rerere Not Applying** - Understanding when rerere works and when it doesn't
4. **Aliases Breaking After Upgrade** - Troubleshooting syntax changes
5. **Persistent Line Ending Warnings** - Ensuring `.gitattributes` is committed and respected

---

**Last Updated:** 2025-11-25
