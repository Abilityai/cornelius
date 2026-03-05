---
name: update-dashboard
description: Update dashboard.yaml with current knowledge base metrics from analysis report
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Update Dashboard

Refresh the Trinity dashboard with current knowledge base metrics extracted from the analysis report.

## Output Location

Write to: `/home/developer/dashboard.yaml`

---

## STEP 1: Read Analysis Report

```
Read knowledge-base-analysis.md from the project root
```

Extract the following metrics using regex or line parsing:

### Core Metrics (from header section, lines 4-5)
- **Analysis Date**: Pattern `**Analysis Date:** YYYY-MM-DD`
- **Total Notes**: Pattern `**Total Notes:** X,XXX`
- **Blocks**: Pattern `**Blocks:** XX,XXX`
- **Permanent Notes**: Pattern `**Permanent Notes:** XXX`
- **AI Insights**: Pattern `**AI Insights:** XXX`
- **Document Insights**: Pattern `**Document Insights:** XXX`

### From Summary Table (lines 14-25)
- **Document Sessions**: From table row
- **MOCs**: From table row
- **Changelogs**: From table row
- **Source notes**: From table row
- **Output pieces**: From table row
- **Change values**: The "+XX" column for trends

### From Domain Distribution (lines 389-398)
- **AI/Agents**: XX%
- **Neuroscience/Dopamine**: XX%
- **Buddhism/Consciousness**: XX%
- **Decision-Making/Biases**: XX%
- **Identity/Belief Systems**: XX%
- **Business/Content Marketing**: XX%
- **Flow/Performance**: XX%

### From Statistics (lines 383-385)
- **Original frameworks**: Count

---

## STEP 2: Build Dashboard YAML

Construct the dashboard with gathered values:

```yaml
title: "Cornelius Knowledge Base"
refresh: 300

sections:
  - title: "Knowledge Base Overview"
    layout: grid
    columns: 3
    widgets:
      - type: metric
        label: "Total Notes"
        value: {total_notes}
        trend: up
        trend_value: "{notes_change}"
        description: "All notes in vault"
      - type: metric
        label: "Total Blocks"
        value: {total_blocks}
        trend: up
        trend_value: "{blocks_change}"
        description: "Content blocks indexed"
      - type: text
        content: "Last Analysis: {analysis_date}"
        size: small
        color: gray

  - title: "Note Categories"
    layout: grid
    columns: 3
    widgets:
      - type: metric
        label: "Permanent Notes"
        value: {permanent_notes}
        trend: up
        trend_value: "{permanent_change}"
        description: "Atomic insights"
      - type: metric
        label: "AI Insights"
        value: {ai_insights}
        trend: up
        trend_value: "{ai_change}"
        description: "AI-extracted notes"
      - type: metric
        label: "Document Insights"
        value: {document_insights}
        trend: up
        trend_value: "{doc_change}"
        description: "Research extracts"
      - type: metric
        label: "MOCs"
        value: {mocs}
        trend: up
        trend_value: "{mocs_change}"
        description: "Navigation hubs"
      - type: metric
        label: "Source Notes"
        value: {source_notes}
        description: "Books & articles"
      - type: metric
        label: "Output Pieces"
        value: {output_pieces}
        trend: up
        trend_value: "{output_change}"
        description: "Published content"

  - title: "Domain Distribution"
    layout: grid
    columns: 2
    widgets:
      - type: progress
        label: "AI/Agents"
        value: {ai_percent}
        color: blue
      - type: progress
        label: "Neuroscience/Dopamine"
        value: {neuro_percent}
        color: purple
      - type: progress
        label: "Buddhism/Consciousness"
        value: {buddhism_percent}
        color: green
      - type: progress
        label: "Decision-Making"
        value: {decision_percent}
        color: orange
      - type: progress
        label: "Identity/Belief"
        value: {identity_percent}
        color: yellow
      - type: progress
        label: "Business/Marketing"
        value: {business_percent}
        color: gray

  - title: "Growth & Activity"
    layout: grid
    columns: 4
    widgets:
      - type: metric
        label: "Document Sessions"
        value: {doc_sessions}
        description: "Research sessions"
      - type: metric
        label: "Original Frameworks"
        value: {frameworks}
        description: "Custom models"
      - type: metric
        label: "Changelogs"
        value: {changelogs}
        description: "Activity records"
      - type: text
        content: "Phase: Technical Implementation"
        size: small
        color: blue

  - title: "Seven Thematic Hubs"
    layout: list
    widgets:
      - type: list
        title: "Primary Knowledge Domains"
        items:
          - "Consciousness & Self (Buddhism-Neuroscience Bridge)"
          - "Dopamine & Motivation (Master Hub)"
          - "Decision-Making & Cognitive Biases"
          - "Identity & Belief Systems"
          - "AI Agents & Digital Intelligence (Largest - 546 notes)"
          - "Flow States & Peak Performance"
          - "Business & Content Marketing Psychology"
        style: bullet
        max_items: 7
```

---

## STEP 3: Parse Metrics from Report

Use the following extraction logic:

### For header metrics (line 5):
```
Pattern: **Total Notes:** (\d+,?\d*) | **Blocks:** (\d+,?\d*) | **Permanent Notes:** (\d+) | **AI Insights:** (\d+) | **Document Insights:** (\d+)
```

### For table metrics (lines 14-25):
```
Look for lines with | Total notes | X,XXX | +XXX |
Extract value and change columns
```

### For domain percentages (lines 389-398):
```
Pattern: AI/Agents.*:\s+(\d+)%
Pattern: Neuroscience.*:\s+(\d+)%
etc.
```

---

## STEP 4: Write Dashboard

```
Write the constructed YAML to /home/developer/dashboard.yaml
```

Ensure:
- All numeric values are integers (no commas in YAML)
- Percentages are integers without % symbol
- Trends use "up" or "down" based on change values
- Date is in YYYY-MM-DD format

---

## STEP 5: Confirm Update

Report what was updated:

```
Dashboard updated at {current_timestamp}

Metrics refreshed:
- Total Notes: {value} ({change})
- Permanent Notes: {value} ({change})
- AI Insights: {value} ({change})
- Document Insights: {value} ({change})
- Domain distribution: AI {X}%, Neuro {X}%, Buddhism {X}%...

Dashboard written to: /home/developer/dashboard.yaml
```

---

## Scheduling

This skill can be scheduled via `/trinity-schedules`:

```
# Daily update (recommended)
/trinity-schedules add update-dashboard --cron "0 9 * * *"

# After each /analyze-kb run
Run manually: /update-dashboard
```

**Note:** Dashboard data is only as fresh as the last `/analyze-kb` run. Consider running analyze-kb before update-dashboard for accurate metrics.
