---
description: Create information architecture for a product including site structure, navigation, and taxonomy. Use for organizing content and improving findability.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <product> [--scope full|section|navigation]
---

# Design Information Architecture

Create comprehensive information architecture for the specified product.

## Workflow

### Step 1: Load Required Skills

Load these skills:

- `information-architecture` - IA methodology and patterns

### Step 2: Understand IA Context

Gather context about: {{ product }}

Scope: {{ scope | default: "full site" }}

Understand:

- What content exists or will exist?
- Who are the primary user groups?
- What are the key user tasks?
- Any existing IA or content inventory?

### Step 3: Spawn IA Architect Agent

Spawn the `ia-architect` agent with the following prompt:

```text
Design comprehensive information architecture for: {{ product }}

Scope: {{ scope | default: "full site" }}

Provide:

1. Content Analysis
   - Content types identified
   - Content relationships
   - Volume and growth considerations

2. User Analysis
   - Primary user segments
   - Key user tasks and goals
   - Finding behaviors (browsing vs. searching)

3. Organization System
   - Primary organization scheme
   - Hierarchy structure
   - Faceted dimensions (if applicable)
   - Metadata requirements

4. Site Map
   - Visual hierarchy diagram
   - Page types and templates
   - Depth analysis
   - Cross-linking strategy

5. Navigation Design
   - Global navigation structure
   - Local/contextual navigation
   - Utility navigation
   - Breadcrumb strategy
   - Mobile considerations

6. Labeling System
   - Navigation labels
   - Category labels
   - Key terminology decisions
   - Label testing recommendations

7. Search Strategy
   - Search scope
   - Filters and facets
   - Search results organization

8. Taxonomy (if applicable)
   - Category hierarchy
   - Term definitions
   - Synonyms and related terms
   - Governance approach

9. Validation Recommendations
   - Card sorting approach
   - Tree testing plan
   - First-click testing

10. Implementation Guidance
    - URL structure
    - SEO considerations
    - CMS requirements

Use the information-architecture skill for methodology guidance.
Output complete IA documentation.
```

### Step 4: Generate Validation Plans

Provide plans to validate the IA:

- Card sort study design
- Tree test specifications
- Navigation usability test

## Example Usage

```bash
# Full site IA
/ux-research:design-ia "enterprise documentation portal"

# Section-specific IA
/ux-research:design-ia "e-commerce product catalog" --scope "category navigation"

# Navigation redesign
/ux-research:design-ia "corporate website" --scope "navigation only"
```

## Output Format

````markdown
# Information Architecture: [Product]

## Executive Summary
[Overview of IA approach and key decisions]

---

## Content Landscape

### Content Types
| Type | Volume | Growth | Priority |
|------|--------|--------|----------|
| [Type] | [Count] | [Rate] | [H/M/L] |

### Content Relationships
[Diagram or description of how content relates]

---

## User Analysis

### Primary Users
| Segment | Goals | Behaviors |
|---------|-------|-----------|
| [Segment] | [Goals] | [Behaviors] |

### Key User Tasks
1. [Task] - Frequency: [H/M/L]
2. [Task] - Frequency: [H/M/L]

---

## Site Structure

### Site Map

```text
Home
├── [Section 1]
│   ├── [Page 1.1]
│   └── [Page 1.2]
├── [Section 2]
│   ├── [Page 2.1]
│   │   └── [Page 2.1.1]
│   └── [Page 2.2]
└── [Section 3]

```

### Page Types

| Type | Template | Count |
|------|----------|-------|
| [Type] | [Template] | [N] |

---

## Navigation Design

### Global Navigation

| Label | Destination | Notes |
|-------|-------------|-------|
| [Label] | [Page] | [Notes] |

### Local Navigation

[By section...]

### Utility Navigation

- [Item 1]
- [Item 2]

### Mobile Navigation

[Approach and considerations]

---

## Labeling System

### Navigation Labels

| Current | Proposed | Rationale |
|---------|----------|-----------|
| [Label] | [Label] | [Why] |

### Testing Needs

[What labels need validation]

---

## Taxonomy

### Category Hierarchy

```text

[Top Level]
├── [Category 1]
│   ├── [Subcategory]
│   └── [Subcategory]
└── [Category 2]

```

### Term Definitions

| Term | Definition | Synonyms |
|------|------------|----------|
| [Term] | [Definition] | [Synonyms] |

---

## Validation Plan

### Card Sort

- **Type:** [Open/Closed/Hybrid]
- **Cards:** [List or count]
- **Participants:** [Number]

### Tree Test

- **Tasks:** [Number]
- **Participants:** [Number]
- **Success Target:** [%]

---

## Implementation Notes

### URL Structure

[Pattern and examples]

### SEO Considerations

[Key points]

### CMS Requirements

[What the CMS needs to support]

````
