---
description: Conduct a heuristic evaluation of an interface using Nielsen's 10 heuristics. Use for expert usability review without user testing.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <interface> [--scope <pages-or-flows>]
---

# Heuristic Evaluation

Conduct an expert usability review using Nielsen's 10 heuristics.

## Workflow

### Step 1: Load Required Skills

Load these skills:

- `heuristic-evaluation` - Nielsen's heuristics and evaluation methodology

### Step 2: Understand Evaluation Scope

Gather context about: {{ interface }}

{% if scope %}Scope: {{ scope }}{% endif %}

Understand:

- What is being evaluated (live product, prototype, designs)?
- What are the key user flows?
- Are there known usability concerns?
- Who are the target users?

### Step 3: Conduct Heuristic Analysis

For each of Nielsen's 10 heuristics, evaluate the interface:

#### 1. Visibility of System Status

- Does the system keep users informed?
- Are there loading indicators, progress bars?
- Is feedback provided after actions?

#### 2. Match Between System and Real World

- Is language user-friendly?
- Are concepts familiar?
- Is information organized logically?

#### 3. User Control and Freedom

- Can users undo/redo?
- Are there clear exit paths?
- Can users cancel actions?

#### 4. Consistency and Standards

- Is design consistent throughout?
- Are platform conventions followed?
- Are similar actions similar?

#### 5. Error Prevention

- Are destructive actions confirmed?
- Is input validated before submission?
- Are error-prone situations eliminated?

#### 6. Recognition Rather Than Recall

- Are options visible?
- Is context provided?
- Do users need to remember information?

#### 7. Flexibility and Efficiency of Use

- Are there shortcuts for experts?
- Can users customize?
- Are frequent actions optimized?

#### 8. Aesthetic and Minimalist Design

- Is information prioritized?
- Is there visual clutter?
- Is content focused?

#### 9. Help Users Recognize, Diagnose, and Recover from Errors

- Are error messages helpful?
- Do they suggest solutions?
- Are errors clearly indicated?

#### 10. Help and Documentation

- Is help available in context?
- Is documentation searchable?
- Are instructions task-focused?

### Step 4: Document Findings

For each issue found:

- Location in interface
- Violated heuristic
- Severity (0-4)
- Description
- Recommendation

### Step 5: Generate Report

Compile findings into prioritized report:

- Executive summary
- Issues by severity
- Issues by heuristic
- Recommendations

## Example Usage

```bash
# Full heuristic evaluation
/ux-research:evaluate-heuristics "project management dashboard"

# Focused evaluation
/ux-research:evaluate-heuristics "e-commerce site" --scope "checkout flow"

# Prototype evaluation
/ux-research:evaluate-heuristics "new onboarding designs"
```

## Output Format

```markdown
# Heuristic Evaluation: [Interface]

## Executive Summary

**Evaluation Date:** [Date]
**Scope:** [What was evaluated]
**Overall Assessment:** [Good/Needs Work/Poor]

### Issue Summary
| Severity | Count |
|----------|-------|
| Catastrophic (4) | [N] |
| Major (3) | [N] |
| Minor (2) | [N] |
| Cosmetic (1) | [N] |

### Top Issues
1. [Issue] - Severity [N]
2. [Issue] - Severity [N]
3. [Issue] - Severity [N]

---

## Heuristic Analysis

### 1. Visibility of System Status

**Score:** [Good/Needs Work/Poor]

#### Issues Found

**Issue 1.1: [Title]**
- **Location:** [Where in interface]
- **Severity:** [0-4]
- **Description:** [What's wrong]
- **Recommendation:** [How to fix]

[Continue for each issue...]

#### Strengths
- [What works well]

---

### 2. Match Between System and Real World

[Continue pattern for all 10 heuristics...]

---

## Issues by Severity

### Catastrophic (4)
| # | Heuristic | Issue | Location |
|---|-----------|-------|----------|
| 1 | [H#] | [Issue] | [Location] |

### Major (3)
[Table...]

### Minor (2)
[Table...]

### Cosmetic (1)
[Table...]

---

## Recommendations

### Immediate Actions (Severity 4)
1. [Action with specific guidance]

### High Priority (Severity 3)
1. [Action]

### Medium Priority (Severity 2)
1. [Action]

---

## Methodology

This evaluation used Nielsen's 10 Usability Heuristics as the framework for assessing [interface]. The evaluation was conducted [describe approach - systematic review of each screen/flow].

### Severity Scale Used
| Rating | Meaning |
|--------|---------|
| 0 | Not a usability problem |
| 1 | Cosmetic problem only |
| 2 | Minor usability problem |
| 3 | Major usability problem |
| 4 | Usability catastrophe |

---

## Next Steps

1. [Recommended next step]
2. [Recommended next step]
3. [Recommended next step]
```

## Severity Rating Guide

| Factor | Question |
|--------|----------|
| **Frequency** | How often does this occur? |
| **Impact** | How serious when it happens? |
| **Persistence** | Can users overcome it easily? |

**Rating Decision:**

- **4 (Catastrophic):** High frequency + High impact + Hard to overcome
- **3 (Major):** Common or impactful, causes significant problems
- **2 (Minor):** Occasional inconvenience, users can work around
- **1 (Cosmetic):** Noticed but doesn't really affect tasks
