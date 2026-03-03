---
created: '2026-01-08'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreibq6gu4o6l4h3ebwq7uaqmeghwpsxram47hmqn42do6mksvygom6y
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
---
# Multi-model coding harness   
## Description   
*[Written by Claude]*   
An open-source, Claude Code-like development harness that supports multi-model orchestration - using different LLMs for different tasks within a single coding session.   
## What is it for   
Getting the best of all models: use fast, cheap models for simple tasks, specialized models for specific domains, and powerful models for complex reasoning - all in one unified interface.   
## Goals   
- Model-agnostic Claude Code experience   
- Smart routing of tasks to optimal models   
- Seamless fallback when models fail or hit limits   
- Cost optimization through model selection   
- Comparison/benchmarking capabilities   
   
## Example orchestration patterns   
- **Fast path**: Use Haiku/GPT-4-mini for file reads, simple edits, clarifying questions   
- **Deep reasoning**: Route to Opus/o1 for architecture decisions, complex debugging   
- **Code generation**: Use Claude/GPT-4 for new code, specialized models for specific languages   
- **Embeddings**: Use dedicated embedding models for semantic search   
   
## Core features   
- Configurable model routing rules   
- Cost tracking and budgeting per session   
- Automatic fallback chains   
- Side-by-side model comparison mode   
- Plugin system for new model providers   
   
## Measure of success   
- Cost reduction vs. single-model usage   
- Task completion quality across model mix   
- Developer satisfaction with model switching   
- Time savings from optimized routing   
   
## Potential blockers   
- Consistent tool/function calling across providers   
- Context management when switching models   
- Rate limits across multiple providers   
- Complexity of routing configuration   
   
## Technical approach   
- Abstract provider interface for model-agnostic tools   
- Routing engine with configurable rules   
- Shared context/memory layer   
- Cost accounting middleware   
- Open plugin architecture for providers   
