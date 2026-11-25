---
created: 2026-02-25
updated: 2026-02-25
created_by: claude-sonnet-4-5-20250929
updated_by: claude-sonnet-4-5-20250929
agent_version: 01.25
title: Task Routing is Categorization Problem (Agent Orchestration Insight)
type: speculative-synthesis
status: strongly-supported
confidence: high
tags: #speculative-synthesis #agent-orchestration #task-routing #categorization #intent-classification #multi-agent
---

# Task Routing is Categorization Problem (Agent Orchestration Insight)

**Source**: Multiple 2024-2025 papers on LLM routing, agent orchestration, difficulty-aware systems
**Document Type**: Cross-analysis synthesis
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-25
**Session**: 2026-02-25 Dynamic Categorization Cognitive AI

---

## Core Insight

Tool selection and task routing in multi-agent systems are **essentially categorization problems**: mapping user intents (inputs) to appropriate tools/models/agents (categories). All categorization principles from cognitive science apply: prototype matching, exemplar retrieval, hybrid strategies, attention gating.

**Reframe**: "Which agent should handle this?" = "Which category does this task belong to?"

---

## Evidence from Agent Research (2024-2025)

**LLM-Based Routing Controllers**:
- **Intent router**: Examines prompt → identifies task category
- **Model router**: Chooses appropriate LLM instance based on task type
- **Method**: Analyzing prompt intent → dynamic model/tool selection

**Difficulty-Aware Orchestration** (arXiv:2509.11079, Sept 2024):
- Categorize tasks by difficulty level
- Route easy tasks → small models (efficient)
- Route hard tasks → large models (capable)
- Adaptive categorization based on task characteristics

**LLM Heterogeneity Research**:
- Different-sized LLMs have complementary strengths (domain specialization)
- Smaller models outperform larger in specific domains
- **Routing = Categorization**: Match task domain to specialized model

**Citation**: Multiple sources including "LLM-Based Routing Controllers" (2024-2025), "Difficulty-Aware Agent Orchestration" arXiv:2509.11079 (Sept 2024)

---

## Categorization Principles Applied to Routing

### 1. **Prototype-Based Routing** (Fast Path)
- Maintain prototype task descriptions for each agent/tool
- New task → compute similarity to prototypes
- Route to nearest prototype match
- **Advantage**: Low latency, simple

### 2. **Exemplar-Based Routing** (Precision Path)
- Store successful task-agent pairings (exemplars)
- New task → find most similar past task
- Route to agent that handled similar task well
- **Advantage**: Handles edge cases

### 3. **Hybrid Routing** (Production Reality)
- Fast prototype matching for common cases
- Exemplar fallback for unusual tasks
- **Meta-routing**: Categorize which categorization strategy to use

### 4. **Attention-Gated Routing**
- Extract task features
- Gate irrelevant features (suppress noise)
- Amplify diagnostic features (focus on what matters)
- Route based on attended features
