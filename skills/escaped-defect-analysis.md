---
name: escaped-defect-analysis
description: "Analyzes a set of escaped defects to identify patterns, root causes, and actionable regression improvements. Use this skill whenever someone asks to analyze bugs that reached production, review escaped defects, understand why QA missed something, identify testing blind spots, or improve the regression suite based on past failures. Also trigger when the user mentions defect trends, QA retrospective data, incident reports, or wants to know what test coverage changes should follow a set of production bugs — even if they don't explicitly say 'escaped defect analysis.'"
---

# Escaped Defect Pattern Analysis

This skill analyzes a set of escaped defects — bugs that passed through QA and reached production or end users — to identify systemic patterns, root causes, and targeted improvements to test coverage and QA process. The goal is not to assign blame but to produce a prioritized, evidence-based action plan that reduces the likelihood of similar defects escaping in the future.

The output is a structured analysis report ending in concrete regression candidates, risk reclassifications, and process recommendations the team can act on immediately.

## How This Skill Works

When invoked, follow these five steps in order. Each step builds on the previous one.

---

## Step 1: Data Collection Gate

Before analysis can begin, establish the scope and verify that sufficient defect data exists to produce meaningful patterns.

### Define the scope

Confirm the following with the user if not already provided:

- **Time period** — What date range should be analyzed? (e.g., last sprint, last quarter, last release cycle)
- **Team or product area** — Is this analysis for a specific delivery team, component, or the whole product?
- **Defect source** — Where do escaped defects live? (Jira bug tickets, incident reports, Sentry alerts, customer support tickets, a combination)
- **Minimum defect count** — Pattern analysis requires at least 5 defects to be meaningful. If fewer exist, flag this and note that findings will be directional rather than statistically reliable.

### Gather the defects

For each escaped defect, collect as much of the following as possible:

- Ticket ID and title
- Description of the failure observed in production
- Severity and customer impact
- Component or feature area affected
- Date discovered in production
- Date the code was introduced (sprint/release, if known)
- Which team or engineer introduced the change
- Whether a test case existed for the scenario
- Whether the defect was linked to a Jira story or epic

Infer what you can from Jira ticket data. Only ask the user for information that cannot be found in the source.

### If data is insufficient

Flag the analysis as **"Limited Data — Directional Only"** and note exactly what's missing. Proceed with what's available but be transparent about how gaps affect confidence in the findings.

---

## Step 2: Defect Classification

Classify each defect across four dimensions. This classification is the foundation for pattern detection in Step 3.

### Dimension 1: Defect Type

| Type | Description |
|---|---|
| Functional | A feature doesn't behave as specified |
| Data Integrity | Data is corrupted, lost, duplicated, or incorrectly transformed |
| UI/UX | Visual or interaction issues that affect usability |
| Integration | Failure at a service boundary or between systems |
| Performance | Response times, timeouts, or resource consumption issues |
| Security | Auth, authorization, or data exposure failures |
| Regression | A previously working behavior broke due to a new change |
| Configuration | Environment, feature flag, or deployment setting issue |

### Dimension 2: STLC Escape Point

Identify which phase of the STLC should have caught this defect but didn't:

| Escape Point | Meaning |
|---|---|
| Requirements | Ambiguous, missing, or conflicting requirements allowed the defect to be built |
| Design | Architectural or technical design flaw not caught in review |
| Development | A unit or integration test should have caught this |
| Test Execution | A test case existed or should have existed and was missed during QA |
| Regression | An existing regression test should have caught this but didn't (or wasn't run) |

### Dimension 3: Escape Reason

For each defect, identify the primary reason it wasn't caught:

| Reason | Description |
|---|---|
| Missing test case | No test existed for this scenario |
| Test not executed | A relevant test existed but wasn't run |
| Insufficient assertion | Test ran but didn't verify the right behavior |
| Risk misclassified | The scenario was deemed low-risk and deprioritized |
| Environment mismatch | The defect only manifested in production conditions |
| Data/state dependency | The defect required a specific data state that wasn't tested |
| New code path | A code change introduced a path not covered by existing tests |
| Knowledge gap | The team didn't know this scenario existed |

### Dimension 4: Severity and Customer Impact

Use the severity already assigned in Jira if available. If not, classify as:

- **Critical** — Data loss, security breach, complete feature failure, revenue impact
- **High** — Core workflow broken for a significant user population
- **Medium** — Non-critical feature degraded; workaround exists
- **Low** — Minor UI issue or edge case with minimal user impact

### Output for this step

Produce a classification table:

```
| Ticket | Title | Type | Escape Point | Escape Reason | Severity |
|--------|-------|------|-------------|---------------|----------|
| BUG-123 | ... | Functional | Test Execution | Missing test case | High |
```

---

## Step 3: Pattern Identification

With defects classified, identify systemic patterns across the dataset. Look for signal across six pattern categories.

### Pattern Category 1: Component Hotspots

Which areas of the product are producing the most escaped defects? Calculate defect density per component. Flag any component that accounts for more than 20% of total escaped defects as a **hotspot** requiring targeted coverage investment.

### Pattern Category 2: Defect Type Clustering

Are certain defect types recurring? A cluster of Data Integrity defects suggests a gap in how data transformations are tested. A cluster of Regression defects suggests the regression suite isn't adequately maintained. Name the cluster and what it implies.

### Pattern Category 3: STLC Phase Concentration

Which STLC phase is failing most often? If most defects escape at the Test Execution phase, the problem is coverage. If most escape at Development, the problem is unit and integration test discipline. If most escape at Requirements, the problem is earlier — test planning isn't starting early enough. The concentration tells you where to invest.

### Pattern Category 4: Escape Reason Trends

Is there a dominant escape reason? "Missing test case" at scale means test planning is incomplete. "Risk misclassified" at scale means the risk framework needs recalibration. "Test not executed" at scale means execution discipline or capacity is the problem. Each requires a different response.

### Pattern Category 5: Regression Blind Spots

Identify any scenarios that escaped multiple times across the analysis period. These are confirmed regression blind spots — areas where the existing regression suite has a structural gap. List each blind spot explicitly.

### Pattern Category 6: Severity Distribution

Are Critical and High defects escaping at a disproportionate rate relative to Medium and Low? This signals a risk prioritization problem — the team is investing test effort in low-risk areas while high-risk paths go under-tested.

### Significance threshold

Only call out a pattern if it appears in at least 3 defects or represents 20%+ of the dataset, whichever is lower for small datasets. Don't manufacture patterns from noise.

---

## Step 4: Root Cause Analysis

For each pattern identified in Step 3, perform a root cause analysis. Do not stop at the surface symptom — identify the underlying process or coverage failure that allowed the pattern to persist.

### Root cause categories

| Category | Description |
|---|---|
| Coverage Gap | Tests for these scenarios don't exist and were never planned |
| Execution Gap | Tests exist but aren't being run consistently |
| Risk Assessment Failure | The area was incorrectly classified as low-risk |
| Regression Maintenance Gap | The regression suite hasn't kept pace with the codebase |
| Process Gap | The STLC phase responsible for catching this type of defect isn't functioning effectively |
| Environment/Data Gap | Production conditions aren't replicated in test environments |
| Knowledge Gap | The team lacked awareness of a behavior, dependency, or edge case |

### For each root cause, document:

1. **Pattern** — Which pattern does this root cause explain?
2. **Root Cause Category** — From the table above
3. **Contributing Factors** — What specific conditions allowed this root cause to persist?
4. **Blast Radius** — If this root cause isn't addressed, how many future defects is it likely to produce? (Low / Medium / High)
5. **Evidence** — Which specific defects support this root cause?

### Example root cause entry

```
Pattern: 4 of 6 escaped defects involve the donation form submission flow
Root Cause Category: Coverage Gap
Contributing Factors: The donation form has 3 payment method paths; only the credit card 
path has test coverage. ACH and check paths have no unit, integration, or manual tests.
Blast Radius: High — every release touching payment processing is at risk
Evidence: BUG-123, BUG-145, BUG-167, BUG-201
```

---

## Step 5: Recommendations

Translate root causes into a prioritized, actionable plan. Every recommendation must be specific enough that someone can act on it without a follow-up conversation.

### Recommendation Type 1: Regression Candidates

For each coverage gap identified, specify the exact test cases that should be added to the regression suite. Use the same format as the test-plan-generator output so these can feed directly into Xray:

```
Regression Candidate:
Area: [component or feature]
Scenario: [specific behavior to test]
Layer: Unit | Integration | Playwright | Manual
Risk Priority: P1 | P2 | P3
Rationale: [which defect(s) this would have caught]
```

### Recommendation Type 2: Risk Reclassifications

For any area where Risk Assessment Failure was identified as a root cause, recommend a reclassification:

```
Risk Reclassification:
Area: [component or feature]
Current Classification: Low | Medium | High
Recommended Classification: Medium | High | Critical
Rationale: [defect evidence supporting the upgrade]
Impact: [what changes when this area is treated as higher risk — test depth, regression inclusion, etc.]
```

### Recommendation Type 3: Process Improvements

For each Process Gap or Execution Gap root cause, recommend a specific process change:

```
Process Improvement:
Phase: [which STLC phase]
Current State: [what's happening now]
Recommended Change: [specific, actionable change]
Expected Outcome: [how this reduces future escapes]
```

### Recommendation Type 4: Regression Maintenance Actions

For Regression Maintenance Gaps, identify specific existing tests that need to be updated or retired:

```
Regression Maintenance:
Action: Add | Update | Remove
Test Reference: [Xray test ID or file path]
Change Required: [what specifically needs to change]
Rationale: [why the current test is insufficient or outdated]
```

### Prioritization

Prioritize all recommendations using:

- **P1** — Addresses a Critical or High severity pattern with High blast radius. Do this sprint.
- **P2** — Addresses a Medium severity pattern or a High severity pattern with Medium blast radius. Do this quarter.
- **P3** — Addresses Low severity patterns or maintenance hygiene. Schedule when capacity allows.

---

## Output Format

Deliver the analysis as a structured report with the following sections in order:

### Section 1: Executive Summary

- Total defects analyzed
- Analysis period
- Top 3 patterns identified
- Top 3 recommended actions
- Overall assessment: Is the current regression suite adequate, partially adequate, or inadequate for the areas affected?

### Section 2: Defect Classification Table

The full classification output from Step 2.

### Section 3: Pattern Report

For each pattern identified in Step 3:
- Pattern name and description
- Supporting defect IDs
- Defect count and percentage of total
- Severity breakdown within the pattern

### Section 4: Root Cause Analysis

For each root cause identified in Step 4, the full root cause entry as specified above.

### Section 5: Prioritized Recommendations

All recommendations from Step 5, sorted by priority (P1 first). Group by recommendation type within each priority level.

### Section 6: Metrics Snapshot

Provide a summary metrics table to support ongoing tracking:

```
| Metric | Value |
|--------|-------|
| Total Escaped Defects | |
| Critical/High Severity | |
| Regression Blind Spots Identified | |
| Net New Regression Candidates | |
| Risk Reclassifications Recommended | |
| Process Improvements Recommended | |
| Top Escape Reason | |
| Top Affected Component | |
```

This table is designed to be carried into team retrospectives and QA metrics dashboards.

---

## Reference Material

For defect severity definitions, risk priority criteria, and regression candidate standards, consult `references/ai-testing-guidelines.md`. When making judgment calls about blast radius or risk reclassification, apply the same P1/P2/P3 framework used in the test-plan-generator skill.
