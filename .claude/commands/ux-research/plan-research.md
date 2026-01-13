---
description: Create a comprehensive user research plan for a product or feature. Use for planning interviews, surveys, and usability studies.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <topic> [--type generative|evaluative|both]
---

# Create User Research Plan

Design a comprehensive user research study for the specified topic.

## Workflow

### Step 1: Load Required Skills

Load these skills:

- `user-research-planning` - Research methodology and planning

### Step 2: Understand Research Context

Gather context about: {{ topic }}

Research type: {{ type | default: "both" }}

Ask clarifying questions if needed:

- What decisions will this research inform?
- What do you already know about users?
- What's your timeline and budget?
- Do you have access to users?

### Step 3: Spawn UX Researcher Agent

Spawn the `ux-researcher` agent with the following prompt:

```text
Create a comprehensive user research plan for: {{ topic }}

Research focus: {{ type | default: "both generative and evaluative" }}

Provide:

1. Research Objectives
   - Primary research questions (3-5)
   - What decisions this will inform
   - Success criteria for the research

2. Methodology Selection
   - Recommended research methods
   - Justification for each method
   - Method sequence and rationale

3. Participant Profile
   - Target user segments
   - Inclusion criteria (must have)
   - Exclusion criteria
   - Sample size per method with justification

4. Study Design
   - Research timeline
   - Session structure for each method
   - Key topics to explore

5. Materials Needed
   - Screener questions
   - Discussion guide outline
   - Consent and logistics templates

6. Deliverables
   - What outputs stakeholders will receive
   - Format and timeline for delivery
   - How findings will be shared

7. Risks and Mitigation
   - Recruitment challenges
   - Bias considerations
   - Timeline risks

Use the user-research-planning skill for methodology guidance.
Output a complete research plan document.
```

### Step 4: Generate Research Materials

Based on the plan, offer to generate:

- Detailed screener questionnaire
- Full interview/discussion guide
- Consent form template
- Note-taking template

## Example Usage

```bash
# Plan research for a new product
/ux-research:plan-research "mobile banking app for elderly users"

# Plan generative research
/ux-research:plan-research "developer workflow pain points" --type generative

# Plan evaluative research
/ux-research:plan-research "checkout flow optimization" --type evaluative
```

## Output Format

```markdown
# Research Plan: [Topic]

## Executive Summary
[1-2 paragraph overview]

## Research Objectives
### Primary Questions
1. [Question]
2. [Question]
3. [Question]

### Decisions to Inform
- [Decision 1]
- [Decision 2]

## Methodology

### Method 1: [Name]
- **Purpose:** [Why this method]
- **Participants:** [Number and type]
- **Duration:** [Session length]
- **Timing:** [When in timeline]

[Continue for each method...]

## Participant Profile

### Segments
| Segment | Criteria | Sample Size |
|---------|----------|-------------|
| [Name] | [Criteria] | [N] |

### Screener Highlights
- [Key screening question]
- [Key screening question]

## Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1 | [Activity] | [Output] |
| 2 | [Activity] | [Output] |

## Deliverables
- [Deliverable 1]
- [Deliverable 2]

## Next Steps
1. [Immediate action]
2. [Immediate action]
```
