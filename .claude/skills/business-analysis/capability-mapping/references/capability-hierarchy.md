# Capability Hierarchy Reference

## Industry Frameworks

Start with an industry-specific framework and customize. Common starting points:

### Technology Company (SaaS)

```text
L1 Capabilities:
├── Product Development
│   ├── Product Strategy
│   ├── Product Design
│   ├── Engineering
│   └── Quality Assurance
├── Go-to-Market
│   ├── Marketing
│   ├── Sales
│   └── Partnerships
├── Customer Success
│   ├── Onboarding
│   ├── Support
│   ├── Retention
│   └── Expansion
├── Platform Operations
│   ├── Infrastructure
│   ├── Security
│   └── Reliability
├── Data & Analytics
│   ├── Data Platform
│   ├── Business Intelligence
│   └── Data Science
├── Finance
│   ├── Revenue Operations
│   ├── Accounting
│   └── FP&A
├── People
│   ├── Talent Acquisition
│   ├── People Operations
│   └── Learning & Development
└── Legal & Compliance
    ├── Legal Operations
    ├── Compliance
    └── Privacy
```

### Financial Services

```text
L1 Capabilities:
├── Customer Management
│   ├── Customer Acquisition
│   ├── Customer Onboarding (KYC/AML)
│   ├── Customer Service
│   └── Relationship Management
├── Product Management
│   ├── Product Development
│   ├── Product Pricing
│   └── Product Distribution
├── Transaction Processing
│   ├── Payment Processing
│   ├── Settlement
│   └── Reconciliation
├── Risk Management
│   ├── Credit Risk
│   ├── Market Risk
│   ├── Operational Risk
│   └── Fraud Prevention
├── Compliance
│   ├── Regulatory Reporting
│   ├── AML/BSA
│   └── Consumer Protection
├── Investment Management
│   ├── Portfolio Management
│   ├── Trading
│   └── Custody
└── Enterprise Services
    ├── Finance
    ├── HR
    ├── IT
    └── Legal
```

### Healthcare

```text
L1 Capabilities:
├── Patient Care
│   ├── Patient Access
│   ├── Clinical Services
│   ├── Care Coordination
│   └── Patient Experience
├── Clinical Operations
│   ├── Clinical Workflow
│   ├── Medical Records
│   ├── Lab & Diagnostics
│   └── Pharmacy
├── Revenue Cycle
│   ├── Patient Registration
│   ├── Charge Capture
│   ├── Claims Management
│   └── Collections
├── Quality & Compliance
│   ├── Quality Improvement
│   ├── Regulatory Compliance
│   └── Risk Management
├── Population Health
│   ├── Care Management
│   ├── Analytics
│   └── Wellness Programs
└── Enterprise Services
    ├── Finance
    ├── HR
    ├── IT
    └── Facilities
```

### Retail

```text
L1 Capabilities:
├── Merchandising
│   ├── Assortment Planning
│   ├── Pricing
│   ├── Promotions
│   └── Private Label
├── Supply Chain
│   ├── Sourcing
│   ├── Inventory Management
│   ├── Distribution
│   └── Logistics
├── Store Operations
│   ├── Store Management
│   ├── Associate Management
│   ├── In-Store Experience
│   └── Loss Prevention
├── Digital Commerce
│   ├── E-commerce Platform
│   ├── Mobile Commerce
│   ├── Digital Marketing
│   └── Omnichannel Fulfillment
├── Customer
│   ├── Loyalty Programs
│   ├── Customer Service
│   └── Customer Insights
└── Enterprise
    ├── Finance
    ├── HR
    ├── IT
    └── Real Estate
```

## Decomposition Rules

### L1 → L2 Decomposition

#### Rule: 3-7 L2 capabilities per L1

Ask:

- What distinct activities make up this capability?
- What could be owned by different people?
- What has different maturity levels?
- What uses different systems?

### L2 → L3 Decomposition

#### Rule: 3-10 L3 capabilities per L2, only where needed

Only decompose to L3 when:

- Detailed planning is needed
- Maturity varies within L2
- Different investment decisions apply
- System mapping requires granularity

### Stop Decomposition When

- You're describing "how" instead of "what"
- Further breakdown doesn't enable decisions
- The capability is simple and atomic
- You've reached organizational task level

## Naming Conventions

### Use Noun Phrases (What)

**Good:** "Customer Onboarding"
**Bad:** "Onboard Customers" (verb phrase = process)

### Be Specific

**Good:** "Identity Verification"
**Bad:** "Verification" (too generic)

### Avoid Technology

**Good:** "Customer Communication"
**Bad:** "Email System" (technology, not capability)

### Avoid Organization

**Good:** "Financial Reporting"
**Bad:** "Finance Department Work" (org, not capability)

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Too many L1s | Overwhelming, loses strategic view | Consolidate to 8-15 |
| Process in capabilities | Capabilities are "what", not "how" | Rename to noun phrases |
| Technology as capability | Systems change, capabilities don't | Abstract to business capability |
| Org as capability | Departments ≠ capabilities | Map capabilities to owners instead |
| Inconsistent granularity | Hard to compare/assess | Apply decomposition rules consistently |

## Maturity Assessment Rubric

### Level 1: Initial

- Ad hoc, reactive
- Heroic efforts to deliver
- No documentation
- Person-dependent

### Level 2: Developing

- Some structure emerging
- Basic documentation exists
- Inconsistent execution
- Limited measurement

### Level 3: Defined

- Standardized processes
- Documented procedures
- Consistent execution
- Basic metrics tracked

### Level 4: Managed

- Quantitative management
- Proactive improvement
- Advanced metrics
- Predictable outcomes

### Level 5: Optimizing

- Continuous improvement
- Innovation culture
- Industry-leading practices
- Strategic differentiator

## Strategic Classification Guidance

### Strategic Capabilities

Characteristics:

- Differentiate from competitors
- Create unique customer value
- Hard for competitors to replicate
- Core to business model

**Action:** Invest, innovate, build in-house

### Core Capabilities

Characteristics:

- Essential to operations
- Expected by customers
- Industry standard
- Must execute well

**Action:** Optimize efficiency, ensure reliability

### Supporting Capabilities

Characteristics:

- Enable other capabilities
- Not customer-facing
- Commodity activities
- Can be standardized

**Action:** Minimize cost, consider outsourcing
