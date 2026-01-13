---
description: Plan an accessibility audit against WCAG 2.2 or other standards. Use for ensuring digital products meet accessibility compliance requirements.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <product> [--level A|AA|AAA] [--scope <pages-or-components>]
---

# Plan Accessibility Audit

Create a comprehensive accessibility audit plan for the specified product.

## Workflow

### Step 1: Load Required Skills

Load these skills:

- `accessibility-planning` - WCAG requirements and audit methodology

### Step 2: Understand Audit Scope

Gather context about: {{ product }}

Target level: {{ level | default: "AA" }}
{% if scope %}Scope: {{ scope }}{% endif %}

Understand:

- Is this a new product or existing?
- What technology stack is used?
- Are there known accessibility issues?
- What's the compliance driver (legal, policy, ethical)?

### Step 3: Spawn Accessibility Specialist Agent

Spawn the `accessibility-specialist` agent with the following prompt:

```text
Create a comprehensive accessibility audit plan for: {{ product }}

Target conformance: WCAG 2.2 Level {{ level | default: "AA" }}

{% if scope %}
Focus scope: {{ scope }}
{% endif %}

Provide:

1. Audit Scope and Standards
   - Specific WCAG 2.2 success criteria to evaluate
   - Any additional standards (Section 508, EN 301 549)
   - Pages/components in scope
   - Testing boundaries

2. Testing Strategy

   ### Automated Testing
   - Recommended tools (axe, WAVE, Lighthouse)
   - What automated tests can catch
   - Limitations of automated testing

   ### Manual Testing
   - Keyboard navigation testing
   - Screen reader testing matrix (which AT, browsers)
   - Visual inspection points
   - Cognitive accessibility checks

   ### Assistive Technology Matrix
   | AT | Browser | OS | Priority |
   |----|---------|----|----|
   | [AT] | [Browser] | [OS] | [P1/P2/P3] |

3. Page/Component Priority
   - Critical paths to test first
   - High-traffic pages
   - Core functionality

4. Issue Documentation Template
   - How to log issues found
   - Severity rating criteria
   - WCAG mapping requirements

5. Timeline and Resources
   - Estimated effort
   - Skills needed
   - Recommended phases

6. Deliverables
   - Issue log format
   - Executive summary template
   - VPAT outline (if needed)
   - Remediation roadmap template

7. Remediation Planning
   - Prioritization framework
   - Quick wins vs. major efforts
   - Regression prevention

Use the accessibility-planning skill for WCAG criteria reference.
Output a complete audit plan document.
```

### Step 4: Generate Audit Materials

Provide ready-to-use materials:

- WCAG 2.2 Level AA checklist
- Issue logging template
- Severity rating guide
- Testing procedures

## Example Usage

```bash
# Full accessibility audit
/ux-research:audit-accessibility "enterprise dashboard application"

# Audit to AAA level
/ux-research:audit-accessibility "public website" --level AAA

# Focused audit
/ux-research:audit-accessibility "e-commerce site" --scope "checkout flow"
```

## Output Format

```markdown
# Accessibility Audit Plan: [Product]

## Audit Overview
- **Target Standard:** WCAG 2.2 Level [A/AA/AAA]
- **Additional Standards:** [Section 508, EN 301 549, etc.]
- **Scope:** [What's included]
- **Timeline:** [Duration]

---

## Success Criteria in Scope

### Level A ([N] criteria)
| # | Criterion | Testing Method |
|---|-----------|----------------|
| 1.1.1 | Non-text Content | Manual + Auto |
| ... | ... | ... |

### Level AA ([N] criteria)
| # | Criterion | Testing Method |
|---|-----------|----------------|
| 1.4.3 | Contrast (Minimum) | Automated |
| ... | ... | ... |

---

## Testing Approach

### Automated Testing
**Tools:**
- [Tool 1] - [Purpose]
- [Tool 2] - [Purpose]

**Scope:** [What automated tests cover]
**Limitations:** [What they miss]

### Manual Testing

#### Keyboard Testing
- [ ] All interactive elements focusable
- [ ] Visible focus indicator
- [ ] Logical focus order
- [ ] No keyboard traps
- [ ] Skip links functional

#### Screen Reader Testing
| AT | Browser | OS | Tester |
|----|---------|----|----|
| NVDA | Chrome | Windows | TBD |
| VoiceOver | Safari | macOS | TBD |
| VoiceOver | Safari | iOS | TBD |

---

## Pages/Components to Test

| Priority | Page/Component | URL | Status |
|----------|----------------|-----|--------|
| P1 | [Page] | [URL] | Pending |
| P1 | [Page] | [URL] | Pending |
| P2 | [Page] | [URL] | Pending |

---

## Issue Severity Ratings

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Blocks access completely | Must fix before launch |
| Major | Significant barrier | Should fix before launch |
| Minor | Causes inconvenience | Fix when possible |
| Enhancement | Best practice | Consider for future |

---

## Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Automated scan | [Time] | Run tools, log issues |
| Manual testing | [Time] | Keyboard, visual |
| AT testing | [Time] | Screen readers |
| Report | [Time] | Compile findings |

---

## Deliverables
- [ ] Issue log (all findings)
- [ ] Executive summary
- [ ] Remediation roadmap
- [ ] VPAT/ACR (if required)
```
