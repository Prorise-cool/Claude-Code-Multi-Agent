# Git Line Endings - Formal Evaluations

Structured evaluations for testing skill activation and behavior across different scenarios.

## Evaluation Overview

- **Total Evaluations**: 4
- **Passed**: 4
- **Failed**: 0
- **Pass Rate**: 100%
- **Models Tested**: Claude Sonnet 4 (2025-11-17), Claude Opus 4.5 (2025-11-25 audit verification)
- **Last Evaluation**: 2025-11-25

## Evaluation 1: First-Time Configuration (Windows)

**Scenario:** New developer setting up Git on Windows for the first time.

**Input:** "I just installed Git on Windows. How should I configure line endings?"

**Expected Behavior:**

- Skill identifies platform (Windows)
- Recommends Option 1 (Traditional) approach
- Provides `core.autocrlf=true` command
- Explains why this is the default and safe choice
- Mentions `.gitattributes` as optional enhancement

**Actual Behavior (Sonnet 4.5):** ✅ PASS - All expected behaviors demonstrated

**Pass Criteria:**

- ✅ Correct platform-specific recommendation
- ✅ Provides working commands
- ✅ Explains rationale
- ✅ Mentions alternatives appropriately

**Notes:**

- Skill successfully navigated to Windows-specific configuration
- Clear explanation of autocrlf=true behavior (CRLF in working dir, LF in repo)
- Appropriate mention of .gitattributes without overwhelming new user

---

## Evaluation 2: Shell Script Execution Error

**Scenario:** Developer encountering `^M: bad interpreter` error when trying to run shell script.

**Input:** "My shell script won't run. I get an error about /bin/bash^M. What's wrong?"

**Expected Behavior:**

- Identifies root cause (CRLF line endings)
- Provides immediate fix (dos2unix or sed)
- Provides permanent fix (.gitattributes rule)
- Explains normalization process
- Includes verification steps

**Actual Behavior (Sonnet 4.5):** ✅ PASS - Comprehensive troubleshooting provided

**Pass Criteria:**

- ✅ Correctly diagnoses line ending issue
- ✅ Provides both immediate and permanent fixes
- ✅ Includes working commands
- ✅ Explains why issue occurred

**Notes:**

- Skill correctly identified `^M` as CRLF indicator
- Provided both dos2unix and sed alternatives
- Explained that Unix shells require LF
- Included .gitattributes prevention strategy

---

## Evaluation 3: Team .gitattributes Setup

**Scenario:** Team lead creating `.gitattributes` for new repository with mixed file types.

**Input:** "I need to set up .gitattributes for a new project with shell scripts, PowerShell scripts, and documentation."

**Expected Behavior:**

- Loads .gitattributes guide reference
- Provides comprehensive .gitattributes template
- Includes patterns for shell scripts (eol=lf)
- Includes patterns for PowerShell (eol=crlf)
- Includes patterns for documentation
- Explains normalization after adding file

**Actual Behavior (Sonnet 4.5):** ✅ PASS - Complete template with explanations

**Pass Criteria:**

- ✅ Comprehensive .gitattributes example
- ✅ Platform-appropriate line ending rules
- ✅ Binary file exclusions
- ✅ Normalization guidance

**Notes:**

- Skill provided comprehensive template with clear comments
- Correctly assigned eol=lf for shell scripts (Unix requirement)
- Correctly assigned eol=crlf for PowerShell (Windows standard)
- Included `* text=auto` default behavior
- Explained `git add --renormalize .` for applying changes

---

## Evaluation 4: Mixed Environment Strategy

**Scenario:** Developer working in both internal repos (with .gitattributes) and external repos (without).

**Input:** "I work on our company repos and also contribute to open source. What's the best line ending strategy?"

**Expected Behavior:**

- Recommends Option 1 (Traditional) for mixed environments
- Explains why Option 2 requires control of all repos
- Provides platform-specific config commands
- Explains how .gitattributes overrides config when present
- Mentions both approaches work together

**Actual Behavior (Sonnet 4.5):** ✅ PASS - Nuanced guidance for mixed environments

**Pass Criteria:**

- ✅ Recommends appropriate strategy
- ✅ Explains trade-offs clearly
- ✅ Platform-specific guidance
- ✅ Clarifies interaction between config and .gitattributes

**Notes:**

- Skill correctly identified Option 1 as safer for mixed environments
- Explained that Option 2 requires comprehensive .gitattributes everywhere
- Clarified that .gitattributes (when present) overrides config
- Recommended adding .gitattributes to internal repos while keeping safe autocrlf config

---

## Multi-Model Testing Notes

### Tested Models

**Claude Sonnet** (Sonnet 4):

- ✅ VERIFIED - Excellent performance on all scenarios
- Successfully handles all complexity levels (configuration, troubleshooting, workflows)
- Navigates progressive disclosure architecture effectively
- Correctly identifies when to load references vs stay in hub

**Claude Opus** (Opus 4.5):

- ✅ VERIFIED - Comprehensive audit completed successfully
- Provides thorough analysis for complex multi-option scenarios (Option 1 vs Option 2)
- Excellent at explaining trade-offs and rationale
- Strong at detailed troubleshooting scenarios

**Claude Haiku**:

- 🔄 PENDING TESTING
- Expected to perform well for common scenarios (platform-specific config, simple troubleshooting)
- Hub file complexity (~2,100 tokens) suitable for Haiku
- May benefit from more explicit references to decision tree for complex scenarios

### Progressive Disclosure Architecture

**Performance Observations**:

- Hub file (~2,100 tokens) provides clear entry points
- Decision tree reference works well for complex scenarios
- Troubleshooting scenarios benefit from immediate fixes in hub
- References load appropriately based on complexity

**Optimization for All Models**:

- Quick Start provides fast path for common cases (Haiku-friendly)
- Decision tree provides structured guidance for complex scenarios (Sonnet/Opus benefit)
- Troubleshooting section in hub handles common issues without loading references
- Comprehensive references available for deep dives

### Recommended Additional Testing

1. **Test with Claude Haiku**:
   - Verify activation on platform keywords (Windows, macOS, Linux)
   - Test common troubleshooting scenarios (shell script errors)
   - Confirm Quick Start guidance is clear enough for fast execution

2. **Test Complex Scenarios**:
   - Mixed staging state (some files CRLF, some LF)
   - Legacy repository normalization (large codebases)
   - Team onboarding with mixed platforms

3. **Test Reference Loading**:
   - Verify decision-tree.md loads for complex configuration decisions
   - Confirm platform-specific.md loads for detailed platform guidance
   - Test configuration-approaches.md for Option 1 vs Option 2 comparisons

---

## Test Scenarios

### Scenario 1: New User Configuring Git Line Endings (Windows, macOS, Linux)

**User Context**: Developer setting up Git for first time

**Expected Outcome**: Platform-specific autocrlf configuration provided

**Test Platforms**:

- Windows: autocrlf=true (Git for Windows default)
- macOS: autocrlf=input (MUST set explicitly)
- Linux: autocrlf=input (MUST set explicitly)

### Scenario 2: Developer Troubleshooting Shell Script Execution Errors

**User Context**: Shell script won't run, shows `^M` errors

**Expected Outcome**: Immediate fix (dos2unix) + permanent fix (.gitattributes)

**Validation**: Commands provided work correctly, issue explained clearly

### Scenario 3: Team Lead Setting Up .gitattributes for New Repository

**User Context**: Creating .gitattributes for project with mixed file types

**Expected Outcome**: Comprehensive template with shell scripts (LF), PowerShell (CRLF), docs (LF), binaries

**Validation**: Template is complete, rules are correct for each file type

### Scenario 4: Developer Working in Mixed Environment (Internal + External Repos)

**User Context**: Works in both controlled and uncontrolled repositories

**Expected Outcome**: Recommends Option 1 (Traditional) for safety

**Validation**: Clear explanation of trade-offs, platform-specific config, .gitattributes override behavior

---

## Validation Criteria

All reference files must:

- ✅ Load correctly when referenced from hub
- ✅ Provide complete information for their topic
- ✅ Include working commands and examples
- ✅ Maintain consistent terminology with hub
- ✅ Reference official Git documentation where applicable

Common paths should:

- ✅ Require minimal reference loading (hub provides quick answers)
- ✅ Progressive disclosure works (hub → references for complexity)
- ✅ Navigation is intuitive (clear links from hub to references)

---

**Last Updated:** 2025-11-28
**Verified Against:** Git 2.51.2+ (commands and behavior validated via MCP servers)
