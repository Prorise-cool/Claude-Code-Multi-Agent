---
description: Design a usability test with tasks, scripts, and success metrics. Use for validating user experience before or after launch.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <feature> [--format moderated|unmoderated|guerrilla]
---

# Create Usability Test

Design a complete usability test plan including tasks, moderator script, and metrics.

## Workflow

### Step 1: Load Required Skills

Load these skills:

- `usability-testing` - Test design methodology
- `user-research-planning` - Participant recruitment

### Step 2: Understand Test Context

Gather context about: {{ feature }}

Test format: {{ format | default: "moderated" }}

Understand:

- What's the current state (prototype, live product)?
- What specific questions need answering?
- Who are the target users?
- What resources are available?

### Step 3: Spawn UX Researcher Agent

Spawn the `ux-researcher` agent with the following prompt:

```text
Design a comprehensive usability test for: {{ feature }}

Test format: {{ format | default: "moderated" }}

Create the following deliverables:

1. Test Objectives
   - Primary usability questions (3-5)
   - Success criteria for the feature
   - What decisions this test will inform

2. Participant Profile
   - Target user characteristics
   - Inclusion/exclusion criteria
   - Recommended sample size with justification

3. Task Scenarios (5-7 tasks)
   For each task:
   - Realistic scenario context
   - Task instruction (goal, not steps)
   - Success criteria (binary or graded)
   - Time benchmark (if applicable)
   - Post-task questions

4. Moderator Script
   - Introduction and consent
   - Warm-up questions
   - Task introduction template
   - Think-aloud prompts
   - Post-test questions
   - Wrap-up and debrief

5. Metrics Framework
   - Task success rates
   - Time on task benchmarks
   - Error tracking
   - Satisfaction measures (SUS, SEQ)
   - Qualitative observation categories

6. Materials Checklist
   - What to prepare before testing
   - Recording setup requirements
   - Note-taking templates

7. Analysis Plan
   - How findings will be analyzed
   - Issue severity rating approach
   - Reporting format

Use the usability-testing skill for methodology guidance.
Output a complete, ready-to-use test plan.
```

### Step 4: Generate Test Materials

Provide complete, copy-paste ready materials:

- Full moderator script
- Task cards/scenarios
- Note-taking template
- Post-test questionnaire (SUS)

## Example Usage

```bash
# Create moderated usability test
/ux-research:create-test "checkout flow optimization"

# Create unmoderated test
/ux-research:create-test "onboarding experience" --format unmoderated

# Create guerrilla test
/ux-research:create-test "navigation redesign" --format guerrilla
```

## Output Format

```markdown
# Usability Test Plan: [Feature]

## Test Overview
- **Format:** [Moderated/Unmoderated/Guerrilla]
- **Duration:** [Time per session]
- **Participants:** [Number]
- **Location:** [Remote/In-person]

## Objectives
1. [Primary question]
2. [Primary question]
3. [Primary question]

---

## Participant Criteria

### Must Have
- [Criterion]
- [Criterion]

### Nice to Have
- [Criterion]

### Exclusions
- [Criterion]

---

## Tasks

### Task 1: [Name] (Warm-up)
**Scenario:**
[Context for the task]

**Task:**
[What to accomplish]

**Success Criteria:**
- [ ] [Observable indicator]

**Time Benchmark:** [X minutes]

### Task 2: [Name]
[Continue pattern...]

---

## Moderator Script

### Introduction
[Full script text]

### Task Introduction Template
[Template for introducing each task]

### Prompts
- Think-aloud: [Prompts]
- Stuck user: [Prompts]

### Post-Test
[Questions to ask]

### Wrap-up
[Closing script]

---

## Metrics

| Task | Success Rate Target | Time Target |
|------|--------------------|--------------|
| [Task] | [%] | [Time] |

## SUS Questionnaire
[Include full SUS or SEQ]

---

## Analysis Approach
[How to analyze findings]

## Issue Severity Scale
[Rating definitions]
```
