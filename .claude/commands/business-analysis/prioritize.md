---
description: Prioritize items using MoSCoW, Kano, or weighted scoring methods. Supports requirements, features, backlog items, or any list needing ranking.
argument-hint: <items-or-context> [--mode moscow|kano|weighted|all] [--output yaml|markdown|both] [--dir <path>]
allowed-tools: Task, Read, Write, Glob, Grep, Skill
---

# Prioritize Command

Systematically prioritize items using proven frameworks: MoSCoW for stakeholder-driven categorization, Kano for customer satisfaction, and weighted scoring for multi-criteria decisions.

## Arguments

- `<items-or-context>`: Items to prioritize (inline list, file reference, or context description)
- `--mode`: Prioritization method (default: `moscow`)
  - `moscow`: Must/Should/Could/Won't categorization (~4K tokens)
  - `kano`: Customer satisfaction categorization (~5K tokens)
  - `weighted`: Multi-criteria weighted scoring (~6K tokens)
  - `all`: All three methods for comparison (~12K tokens)
- `--output`: Output format (default: `both`)
  - `yaml`: Structured YAML for downstream processing
  - `markdown`: Formatted markdown tables
  - `both`: Both formats

- `--dir`: Output directory (default: `docs/analysis/`)

## Execution

### Step 1: Parse Arguments

Extract items, mode, and output format from arguments.

If no items provided, ask the user:
"What items would you like to prioritize? You can provide a list, reference a file, or describe the context."

Default mode is `moscow`. Default output is `both`.

### Step 2: Load Prioritization Skill

Invoke the `prioritization` skill to access:

- MoSCoW categorization rules
- Kano model categories and survey approach
- Weighted scoring matrix methodology
- Value vs Effort matrix
- Selection guidance (when to use which method)

### Step 3: Gather Items

Collect items to prioritize:

**From inline list:**

```text
/prioritize "Feature A, Feature B, Feature C, Feature D"
```

**From file reference:**

```text
/prioritize @backlog.md --mode weighted
```

**From context:**

```text
/prioritize "Sprint planning for authentication module"
```

For context-based requests, explore the codebase or ask clarifying questions to identify items.

### Step 4: Execute Based on Mode

#### MoSCoW Mode (Default)

Categorize items into four groups:

1. **Must Have**: Critical requirements, non-negotiable
   - Without these, the solution is not viable
   - Core functionality, compliance, safety

2. **Should Have**: Important but not critical
   - Significant value but workarounds exist
   - High priority for next iteration

3. **Could Have**: Desirable if time/resources permit
   - Nice-to-have features
   - Enhance user experience

4. **Won't Have (This Time)**: Explicitly excluded
   - Documented for future consideration
   - Helps manage scope creep

For each item, gather stakeholder input on:

- Business criticality
- Technical dependencies
- Compliance requirements
- User impact

#### Kano Mode (Customer Satisfaction)

Categorize items by satisfaction impact:

1. **Basic (Must-Be)**: Expected features
   - Absence causes dissatisfaction
   - Presence doesn't increase satisfaction
   - Example: Login functionality

2. **Performance (One-Dimensional)**: Linear satisfaction
   - More = better satisfaction
   - Less = dissatisfaction
   - Example: Page load speed

3. **Delighter (Attractive)**: Unexpected value
   - Presence creates excitement
   - Absence doesn't cause dissatisfaction
   - Example: AI-powered suggestions

4. **Indifferent**: No satisfaction impact
   - Users don't care either way
   - Consider removing from scope

5. **Reverse**: Causes dissatisfaction
   - Some users actively dislike
   - Segment or reconsider

For each item, consider:

- Customer expectations
- Competitive baseline
- Emotional response to presence/absence

#### Weighted Scoring Mode (Multi-Criteria)

Apply weighted criteria scoring:

##### Step A: Define Criteria

```markdown
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Business Value | 30% | Revenue/strategic impact |
| User Impact | 25% | User experience improvement |
| Effort | 20% | Development complexity (inverse) |
| Risk | 15% | Technical/business risk (inverse) |
| Dependencies | 10% | Blocking other work |
```

##### Step B: Score Each Item

Rate each item 1-5 on each criterion.

##### Step C: Calculate Weighted Scores

```text
Score = Σ (Criterion Weight × Item Score)
```

##### Step D: Rank by Total Score

#### All Mode (Comparison)

Run all three methods and compare:

- Identify items with consistent priority across methods
- Highlight items with priority conflicts
- Recommend final priority based on synthesis

### Step 5: Generate Output Artifacts

#### YAML Output

```yaml
prioritization:
  version: "1.0"
  date: "[ISO Date]"
  method: "[moscow|kano|weighted|all]"
  analyst: "ba-orchestrator"

  items:
    - id: "ITEM-1"
      name: "[Item name]"
      moscow:
        category: "must"
        rationale: "[Why must-have]"
      kano:
        category: "basic"
        rationale: "[Why expected]"
      weighted:
        scores:
          business_value: 5
          user_impact: 4
          effort: 3
          risk: 2
          dependencies: 4
        total: 3.85
        rank: 1

  summary:
    moscow:
      must: 3
      should: 4
      could: 2
      wont: 1
    kano:
      basic: 2
      performance: 4
      delighter: 2
      indifferent: 1
      reverse: 1
    weighted:
      top_3:
        - "ITEM-1"
        - "ITEM-3"
        - "ITEM-2"

  recommendations:
    immediate: ["ITEM-1", "ITEM-2"]
    next_iteration: ["ITEM-3", "ITEM-4"]
    backlog: ["ITEM-5"]
    remove: ["ITEM-6"]
```

#### Markdown Output

**MoSCoW Summary:**

```markdown
## MoSCoW Prioritization

### Must Have (Critical)
| Item | Rationale |
|------|-----------|
| [Item 1] | [Why critical] |

### Should Have (Important)
| Item | Rationale |
|------|-----------|
| [Item 2] | [Why important] |

### Could Have (Desirable)
| Item | Rationale |
|------|-----------|
| [Item 3] | [Why nice-to-have] |

### Won't Have (This Time)
| Item | Rationale | Future? |
|------|-----------|---------|
| [Item 4] | [Why excluded] | Yes |
```

**Weighted Scoring Matrix:**

```markdown
## Weighted Scoring Matrix

| Item | Business (30%) | User (25%) | Effort (20%) | Risk (15%) | Deps (10%) | Total | Rank |
|------|----------------|------------|--------------|------------|------------|-------|------|
| Item 1 | 5 (1.50) | 4 (1.00) | 3 (0.60) | 4 (0.60) | 3 (0.30) | 4.00 | 1 |
| Item 2 | 4 (1.20) | 5 (1.25) | 2 (0.40) | 3 (0.45) | 4 (0.40) | 3.70 | 2 |
```

#### Summary Report

```markdown
## Prioritization Summary

**Date:** [ISO Date]
**Method:** [moscow|kano|weighted|all]
**Total Items:** [Count]

### Priority Distribution

| Priority | Items | Percentage |
|----------|-------|------------|
| High | [Count] | [%] |
| Medium | [Count] | [%] |
| Low | [Count] | [%] |
| Excluded | [Count] | [%] |

### Top Priorities

1. **[Item 1]**: [Brief rationale]
2. **[Item 2]**: [Brief rationale]
3. **[Item 3]**: [Brief rationale]

### Recommendations

- **Immediate Action**: [Items to start now]
- **Next Iteration**: [Items for next phase]
- **Review Needed**: [Items with conflicting priorities]
```

### Step 6: Save Results

Save outputs based on format flag:

**YAML file:**

- `docs/analysis/prioritization.yaml`

**Markdown file:**

- `docs/analysis/prioritization.md`

Use `--dir` to specify a custom output directory.

### Step 7: Suggest Follow-Up Actions

After completing prioritization:

```markdown
## Suggested Next Steps

1. **Stakeholder Review**: Share priorities with stakeholders for validation
2. **Effort Estimation**: Use estimation techniques for high-priority items
3. **Risk Analysis**: Use `/ba:risk-register` for high-priority, high-risk items
4. **Roadmap Planning**: Sequence items into delivery phases
5. **Capability Mapping**: Use `/ba:capability-map` to align with capabilities
```
