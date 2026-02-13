---
name: synthesize-insights
description: Combine multiple insights into coherent narrative
---

# Synthesize Insights

Combine multiple insights or permanent notes into a coherent narrative, framework, or argument. Discovers patterns and connections across disparate ideas.

## Usage

```
/synthesize-insights <note names or topic cluster>
```

## Parameters

- **note names**: List of specific notes to synthesize
  - Comma-separated: "[[Note A]], [[Note B]], [[Note C]]"
  - Or topic cluster: "All notes about dopamine and AI"
  - Or theme: "Buddhism and neuroscience connections"

## Examples

### Synthesize Specific Notes
```
/synthesize-insights [[AI adoption bottleneck is psychological]], [[Professional identity creates AI resistance]], [[Belief is a way to deal with Uncertainty]]
```

### Synthesize Topic Cluster
```
/synthesize-insights All notes connecting dopamine, social media, and AI
```

### Synthesize Theme
```
/synthesize-insights Buddhism-neuroscience-AI triangle
```

## Workflow

1. **Gather Notes**
   - If specific notes listed: Retrieve those notes
   - If topic/theme: Use /recall or Local Brain Search to find cluster
   - Aim for 5-10 notes minimum

2. **Find Patterns**
   - Identify common themes
   - Discover non-obvious connections
   - Note contradictions or tensions
   - Find consilience zones (multiple perspectives converging)

3. **Build Narrative**
   - Structure: Pattern → Evidence → Implications
   - Show how insights relate and build on each other
   - Highlight emergent understanding
   - Suggest frameworks or models

4. **Output Synthesis**
   - Coherent narrative (3-5 paragraphs)
   - Pattern description
   - Supporting evidence from notes
   - Implications and applications
   - Suggested next steps or questions

## Output Format

```
🔗 Synthesis: [Topic/Theme]

**Pattern Identified:**
[Description of overarching pattern or framework emerging from notes]

**Key Connections:**

1. [Connection 1]: [[Note A]] + [[Note B]]
   [How these notes relate and what emerges]

2. [Connection 2]: [[Note C]] + [[Note D]] + [[Note E]]
   [Multi-way connection and emergent insight]

3. [Connection 3]: [[Note F]] ↔ [[Note G]]
   [Bidirectional or tension between notes]

**Emergent Understanding:**
[What new insight emerges from synthesizing these notes that wasn't obvious in any single note]

**Implications:**
- [Implication 1 for thinking/practice]
- [Implication 2 for content/frameworks]
- [Implication 3 for future exploration]

**Suggested Applications:**
- Article topic: "[Potential article title]"
- Framework: "[Potential framework name]"
- Research direction: "[Area to explore further]"

📝 Synthesized Notes:
- [[Note 1]] - Role in synthesis
- [[Note 2]] - Role in synthesis
- [[Note 3]] - Role in synthesis
[...]
```

## Use Cases

### 1. Article Development
```
User: "I want to write about AI and psychology"

/synthesize-insights AI adoption psychological barriers cluster

# Output: Synthesized narrative showing how notes connect
# → Use as article foundation
```

### 2. Framework Creation
```
User: "Help me create a framework for AI resistance"

/synthesize-insights [[AI adoption bottleneck]], [[Professional identity]], [[Dopamine reinforcement]], [[Belief systems]]

# Output: Framework showing how psychological factors interact
# → Visualize in diagram or model
```

### 3. Connection Discovery
```
User: "How do my Buddhism notes relate to AI?"

/synthesize-insights Buddhism and AI connections

# Output: Non-obvious bridges between ancient wisdom and digital intelligence
# → Potential contrarian article angle
```

### 4. Content Planning
```
User: "What content can I create from my dopamine notes?"

/synthesize-insights All dopamine-related notes

# Output: Multiple synthesis narratives
# → Suggests 3-5 article topics or video series
```

## Quality Indicators

High-quality synthesis:
✅ Identifies non-obvious patterns
✅ Shows connections between 5-10+ notes
✅ Produces emergent understanding
✅ Suggests practical applications
✅ Highlights tensions or contradictions
✅ Creates actionable frameworks

Low-quality (try different notes):
❌ Only surface-level connections
❌ No emergent insight
❌ Obvious or generic patterns
❌ Doesn't inspire new thinking

## Advanced Techniques

### Multi-Domain Synthesis
```
/synthesize-insights Notes connecting Buddhism, neuroscience, and AI agent design
```
Reveals consilience - where independent domains converge on same truth

### Temporal Synthesis
```
/synthesize-insights Evolution of my thinking on AI from 2024 to 2025
```
Shows how perspectives change over time

### Contrarian Synthesis
```
/synthesize-insights Notes that challenge conventional AI wisdom
```
Gathers all contrarian perspectives for provocative content

### Problem-Solution Synthesis
```
/synthesize-insights Problem: AI adoption barriers + Solutions from psychology and Buddhism
```
Connects problem notes with solution notes from different domains

## Integration with Other Commands

```
# Synthesis → Article workflow
/synthesize-insights Dopamine, social media, AI cluster
# → Get synthesis with connections
# → Use in /create-article skill

# Synthesis → Connections workflow
/synthesize-insights AI notes
/find-connections [synthesized theme]
# → Discover even more connections

# Synthesis → Video series workflow
/synthesize-insights Buddhism-AI connections
# → Extract 3-5 narratives
# → Ruby creates video series from each
```

## Notes

- Best with 5-10+ notes for rich synthesis
- Looks for non-obvious connections semantic search might miss
- Produces frameworks and models, not just summaries
- Ideal for article planning and content strategy
- Cost: ~$0.30-0.50 depending on number of notes
- Can be called by Ruby for content ideation

## Future Enhancements

- Auto-suggest synthesis clusters
- Visual network diagrams
- Multi-layered synthesis (synthesis of syntheses)
- Export as Mermaid diagram
- Track synthesis quality over time

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Permanent notes, AI insights, Document insights |
| Local Brain Search | `resources/local-brain-search/` | X | | Semantic search for topic clusters |
| MOCs | `Brain/03-MOCs/` | X | | Map of Content for thematic organization |

## Completion Checklist

- [ ] Notes gathered (5-10+ for rich synthesis)
- [ ] Common themes identified
- [ ] Non-obvious connections discovered
- [ ] Contradictions or tensions noted
- [ ] Emergent understanding articulated
- [ ] Pattern → Evidence → Implications structured
- [ ] Practical applications suggested
- [ ] Cited notes listed with their role
