# Git Setup - Testing and Evaluations

Test scenarios, multi-model testing notes, and formal evaluations for the setup skill.

## Test Scenarios

Document typical activation scenarios for testing.

### Scenario 1: Platform-Specific Activation

**Query**: "I need to install Git on my Windows machine"

**Expected Behavior**: Skill activates and provides Windows-specific installation guidance

**Success Criteria**:

- Skill identifies Windows platform
- Provides winget and Git for Windows installer options
- Includes Windows-specific configuration (long paths)
- Shows verification steps
- References config skill for advanced setup

### Scenario 2: Troubleshooting Scenario

**Query**: "Git Bash command history isn't working in Windows Terminal"

**Expected Behavior**: Skill loads git-bash-history-troubleshooting.md reference

**Success Criteria**:

- Skill recognizes troubleshooting context
- Provides immediate solution in main SKILL.md
- References detailed troubleshooting guide
- Explains root cause (missing .bash_history)
- Provides clear resolution steps

### Scenario 3: Configuration Guidance

**Query**: "How do I set up my Git identity after installing?"

**Expected Behavior**: Skill provides user.name and user.email configuration commands

**Success Criteria**:

- Shows basic configuration commands
- Explains why user identity is required
- Includes verification steps
- Mentions optional settings (editor, default branch)
- References config for advanced configuration

## Formal Evaluations

Structured evaluations for testing skill activation and behavior.

### Evaluation 1: New Developer on Windows Needs Git Installed

**User Context**: New developer on Windows 11, no Git installed, needs to set up Git for first time

**User Query**: "I need to install Git on my Windows laptop and configure it"

**Expected Behavior**:

1. Skill activates autonomously based on "install Git" and "Windows" triggers
2. Provides two installation options (Git for Windows installer vs winget)
3. Guides through basic configuration (user identity, default branch, editor)
4. Includes verification steps to confirm installation success
5. References config skill for advanced configuration

**Success Criteria**:

- ✅ Skill activates without explicit invocation
- ✅ Platform-specific guidance provided (Windows)
- ✅ Quick Start section provides fastest path
- ✅ Configuration hierarchy clearly explained

**Testing Status**: Verified with Claude Sonnet 4.5

### Evaluation 2: Developer Encounters Git Bash History Issue on Windows Terminal

**User Context**: Windows developer using Windows Terminal with Git Bash profile, up arrow key not working for command history

**User Query**: "My Git Bash terminal isn't saving command history. The up arrow doesn't work."

**Expected Behavior**:

1. Skill activates based on "Git Bash" and "command history" troubleshooting triggers
2. Provides immediate solution in Windows-Specific Troubleshooting section
3. References git-bash-history-troubleshooting.md for detailed explanation
4. Explains root cause (missing .bash_history file)
5. Provides clear resolution steps

**Success Criteria**:

- ✅ Skill activates for troubleshooting scenario
- ✅ Progressive disclosure works (main solution in SKILL.md, details in reference)
- ✅ Solution is actionable and specific
- ✅ Reference file loads when needed

**Testing Status**: Verified with Claude Sonnet 4.5

### Evaluation 3: macOS Developer Needs to Choose Between Xcode Tools and Homebrew

**User Context**: macOS developer setting up new machine, unfamiliar with Git installation options on macOS

**User Query**: "What's the best way to install Git on macOS? I see multiple options."

**Expected Behavior**:

1. Skill activates based on "install Git" and "macOS" triggers
2. Presents both options (Xcode Command Line Tools vs Homebrew)
3. Explains trade-offs clearly ("Built-in" vs "Latest version")
4. Provides recommendation (Homebrew for latest version)
5. Includes macOS-specific configuration (autocrlf=input, Zsh integration)

**Success Criteria**:

- ✅ Skill provides clear comparison without overwhelming
- ✅ Recommendation is clear and justified
- ✅ Platform-specific details addressed (Zsh as default shell since Catalina)
- ✅ Quick Start provides fast path for common case

**Testing Status**: Verified with Claude Sonnet 4.5

## Multi-Model Testing Notes

### Tested Models

**Claude Sonnet 4.5**:

- ✅ Optimal performance
- ✅ Navigates platform-specific sections effectively
- ✅ Correctly identifies Quick Start paths
- ✅ Handles progressive disclosure well

**Claude Sonnet 3.5**:

- ✅ Excellent performance
- ✅ Strong activation on platform keywords
- ✅ Navigates reference files appropriately

**Claude Haiku**:

- 🔄 Expected to perform well due to progressive disclosure architecture
- 🔄 May need more explicit platform guidance in queries for consistent activation

### Observations

**Platform Detection Section**: Helps all models identify correct platform workflows

**Quick Start Sections**: Provide clear entry points for faster models

**Progressive Disclosure Pattern**: SKILL.md → references/ works well across model tiers

**Strong Activation Triggers**: Description ensures autonomous skill invocation

**Multiple Test Scenarios**: Cover diverse activation patterns (installation, troubleshooting, configuration)

### Recommended Additional Testing

1. **Test with Claude Haiku**:
   - Verify activation reliability with smaller model
   - Test cross-platform scenarios (user switching from Windows to macOS)
   - Test escalation patterns (basic setup → advanced configuration → config skill)

2. **Test Edge Cases**:
   - User with existing Git installation (upgrade vs reconfigure)
   - User with corrupted Git installation (repair guidance)
   - User needing both Windows and WSL Git setups

3. **Test Reference Loading**:
   - Verify install-windows.md loads for Windows installation
   - Confirm install-macos.md loads for macOS installation
   - Test git-bash-history-troubleshooting.md for Windows Terminal issue

## Development Methodology

This skill was developed following evaluation-first principles.

### Development Process

1. Identified gaps in Git installation guidance across platforms (Windows, macOS, Linux, WSL)
2. Created test scenarios for common installation and troubleshooting patterns
3. Built minimal Quick Start sections for each platform to address fastest path
4. Iterated based on real usage feedback and common troubleshooting issues
5. Separated Git Bash history troubleshooting into reference file for progressive disclosure

### Design Decisions

**Multi-Platform Coverage**: Single skill for all platforms (high cohesion - Git setup changes together)

**Quick Start Sections**: At top for fast path (time-to-value optimization)

**Platform Detection Section**: Guides model's workflow selection

**Optional Shell Integration**: Degrees of freedom for user preferences

**System-Level Config**: Marked as optional and admin-only (prevents permission errors)

### Iterative Improvements

- v1.0.0 (2025-01-06): Initial release based on Windows, macOS, Linux, WSL setup patterns
- v1.1.0 (2025-01-11): Added git-bash-history-troubleshooting.md reference after identifying common Windows Terminal issue
- v1.2.0 (2025-11-25): Comprehensive audit - enhanced WSL reference, updated Git versions, added Ubuntu 24.04 support
- v1.3.0 (2025-11-28): Token optimization - extracted configuration details and testing to references/

### Team Feedback

Skill is used in onboarding documentation repository as foundational Git setup guidance. Positive feedback on multi-platform coverage and Quick Start clarity.

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
**Verified Against:** Git 2.47.0+ (Windows, macOS, Linux, WSL)
