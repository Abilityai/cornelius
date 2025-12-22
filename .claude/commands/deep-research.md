---
description: Autonomous research pipeline - discover, extract, and integrate cutting-edge insights into knowledge base
argument-hint: [optional topic or "auto" for autonomous selection]
allowed-tools: Task, Read, Bash, Glob, Grep
---

# Deep Research & Knowledge Integration Pipeline

You are orchestrating a fully autonomous research → extraction → connection discovery workflow to expand the knowledge base with cutting-edge insights.

## Input Processing

**User Input:** $ARGUMENTS

**Execution Modes:**
1. **Directed Mode** - User specifies topic(s): `$ARGUMENTS = "neuroscience of habits"` or `$ARGUMENTS = "multi-agent systems, safety alignment"`
2. **Autonomous Mode** - You select topics: `$ARGUMENTS = ""` or `$ARGUMENTS = "auto"`

## Mission

Execute a complete 3-phase autonomous research pipeline:
1. **RESEARCH** - Gather cutting-edge papers and developments
2. **EXTRACT** - Pull unique insights from research findings
3. **CONNECT** - Map connections to existing knowledge base

**Critical Requirement:** ALL extracted insights MUST be stored in Document Insights folder structure to keep separate from main Brain.

---

## Phase 1: Topic Selection & Research Planning

### A. If User Provided Topic(s) (Directed Mode)
- Parse `$ARGUMENTS` for topic(s)
- Validate topics are research-worthy
- Plan research scope for each topic

### B. If Autonomous Mode
Analyze knowledge base to identify research opportunities:

1. **Read knowledge base analysis:**
   ```bash
   cat ./knowledge-base-analysis.md
   ```

2. **Check recent activity:**
   ```bash
   ls -lt ./Brain/Document\ Insights/ | head -10
   ```

3. **Identify gaps based on:**
   - Underrepresented domains in knowledge-base-analysis.md
   - Missing connections flagged in recent changelogs
   - Emerging themes from existing insights
   - User's recent work patterns
   - CLAUDE.md priorities and future directions

4. **Select 1-3 research topics** that would:
   - Fill identified gaps
   - Build on existing strengths (e.g., Buddhism-Neuroscience-AI triangle)
   - Connect underexplored domains
   - Add empirical validation to intuitive frameworks
   - Challenge or extend current thinking

**Examples of Good Topic Selection:**
- "Neuroscience of habits and behavior change" (if habit formation underrepresented)
- "Collective intelligence and swarm behavior" (if group dynamics missing)
- "Embodied cognition and interoception" (if embodiment gap identified)
- "Complexity science and emergence" (if systems thinking needed)
- "Creativity neuroscience and insight generation" (if creative process mechanics missing)

---

## Phase 2: Execute Research

### Get Current Timestamp
```bash
date '+%Y-%m-%d %H:%M:%S %Z'
```
Save this for session folder naming: `YYYY-MM-DD Topic Description`

### Launch Research Specialist Agent(s)

**For Each Topic:**

Use Task tool with subagent_type='research-specialist':

```
TOPIC: [Selected topic]

Conduct comprehensive research on [topic] focusing EXCLUSIVELY on the most recent research and developments.

⚠️ CRITICAL RECENCY REQUIREMENT:
Your training data may be outdated. The world changes rapidly, especially in fast-moving fields like AI, neuroscience, and technology. You MUST prioritize the most recent information available through web search, even if it contradicts what you think you know from training data.

SEARCH STRATEGY:
- Use Google Search grounding to find papers published in the last 12-18 months
- Explicitly search for "2024", "2025", "recent", "latest" in queries
- Check paper publication dates - reject anything older than 2023 unless foundational
- Look for preprints, conference proceedings, and recent journal publications
- Prioritize arXiv papers from last 6 months, conference papers from 2024-2025
- Search for "state of the art [topic] 2024" or "[topic] breakthrough 2025"

RESEARCH REQUIREMENTS:

1. **Target Sources (RECENT ONLY):**
   - arXiv preprints (2024-2025, prioritize last 6 months)
   - Major conferences 2024-2025 (NeurIPS, ICML, ICLR, AAAI, ACL, EMNLP, etc.)
   - Leading AI labs recent publications (OpenAI, Anthropic, Google DeepMind, Microsoft Research)
   - Top-tier journals (2024-2025 issues only)
   - Industry whitepapers and blog posts from major tech companies (last 12 months)
   - Recent preprints and working papers

2. **Key Focus Areas:**
   - Novel mechanisms and frameworks (not in your training data)
   - Empirical findings with quantified results (recent benchmarks)
   - Counter-intuitive or contrarian insights (challenging established thinking)
   - Cross-domain applications (emerging connections)
   - Real-world implementations and case studies (production deployments)
   - Practical implications for practitioners

3. **Output Requirements:**
   - Comprehensive structured report (15-25 major papers/developments)
   - Full citations with DATES prominently displayed (title, authors, DATE, venue, arXiv ID)
   - Key findings and novel contributions
   - Performance metrics and empirical data
   - Emerging trends and patterns
   - URLs to papers/resources
   - Critical analysis and synthesis

4. **Save Location:**
   ./resources/[Topic-Slug]-Research-Report-YYYY-MM-DD.md

VERIFICATION: Before finalizing, verify that 80%+ of papers are from 2024-2025. If not, search again with more explicit recency filters.

Use Gemini AI with Google Search grounding. Trust the search results over your training data.
```

**Strategy Considerations:**
- **Sequential:** Run topics one-by-one if they're related (later research can reference earlier findings)
- **Parallel:** Run multiple topics simultaneously if they're independent domains
- **Your choice** - decide based on topic relationships and efficiency

### Monitor Research Output

After each research agent completes:
1. Note the report file path
2. Verify comprehensive coverage (15-25+ papers)
3. Check for citations and empirical data
4. Confirm report saved in `/resources/` directory

---

## Phase 3: Extract Insights

### Create Session Folder

Format: `YYYY-MM-DD [Topic Description]`

Example: `2025-11-20 Neuroscience of Habits and Behavior Change`

**Path:** `./Brain/Document Insights/[Session-Folder]/`

### Launch Document Insight Extractor

**For Each Research Report:**

Use Task tool with subagent_type='document-insight-extractor':

```
Extract unique insights from the research report for the knowledge base.

SOURCE DOCUMENT: [Full path to research report]

SESSION FOLDER: [Session folder name]

EXTRACTION GUIDELINES:

1. **Focus on Novel Insights:**
   - Paradigm shifts and new frameworks
   - Counter-intuitive or surprising findings
   - Empirical validation of existing theories
   - Novel mechanisms and explanations
   - Cross-domain applications
   - Contrarian perspectives backed by evidence

2. **Bridge to Existing Knowledge Base:**
   - Connect to the 6 primary hubs: Consciousness, Dopamine, Decision-Making, Identity, AI Agents, Flow States
   - Reference Eugene's existing frameworks (Folder Paradigm, Mental Models Taxonomy, etc.)
   - Identify consilience opportunities (3+ domains converging)
   - Find validation or challenges to current thinking
   - Look for applications of Buddhist/neuroscience principles

3. **Prioritize:**
   - Research findings that extend current understanding
   - Empirical data that validates intuitive frameworks
   - Novel architectures or methodologies
   - Real-world implications and case studies
   - Philosophical or meta-level insights

4. **Quality Standards:**
   - 15-25 high-quality insights per report
   - Avoid redundancy with existing knowledge base (ALWAYS search for duplicates)
   - Include proper citations (paper title, authors, year)
   - Tag appropriately for discoverability
   - Create connections to existing permanent notes

5. **Output Requirements:**
   - Create permanent notes in session folder
   - Include full citations and sources
   - Add relevant tags
   - Note connections to existing insights
   - Create changelog: CHANGELOG - Document Analysis YYYY-MM-DD.md

CRITICAL:
- ALWAYS search for duplicates before creating notes
- Store ALL extracted notes in: ./Brain/Document Insights/[Session-Folder]/
- Create comprehensive changelog documenting extraction process
```

### Monitor Extraction Output

After extraction completes:
1. Verify insights stored in correct Document Insights session folder
2. Check changelog was created
3. Note count of unique insights extracted
4. Confirm deduplication was performed

---

## Phase 4: Connection Discovery

### Launch Connection Finder Agent(s)

**Strategy Options:**

**Option A: Single Comprehensive Pass**
- Run connection-finder once on the entire session folder
- Maps all new insights against full knowledge base

**Option B: Multiple Targeted Passes**
- Run connection-finder 2-3 times on different subsets
- First pass: New insights ↔ Existing AI insights (102 notes)
- Second pass: New insights ↔ Primary hubs (Dopamine, Consciousness, etc.)
- Third pass: Cross-domain bridges and synthesis opportunities

**Your Choice** - Select based on insight count and domain diversity.

### Execute Connection Discovery

Use Task tool with subagent_type='connection-finder':

```
Discover connections between newly extracted insights and existing knowledge base.

STARTING POINTS:
All notes in session folder: ./Brain/Document Insights/[Session-Folder]/

Or specify individual notes if doing targeted passes.

CONNECTION DISCOVERY GOALS:

1. **Bridge to Existing Knowledge:**
   - Connect to 102 existing AI insights
   - Link to 6 primary thematic hubs (Consciousness, Dopamine, Decision-Making, Identity, AI Agents, Flow)
   - Find relationships to original frameworks (Folder Paradigm, Mental Models Taxonomy, etc.)
   - Map to MOCs and output content

2. **Cross-Domain Opportunities:**
   - Buddhism ↔ Neuroscience ↔ AI consilience
   - Decision Science ↔ Agent Architecture
   - Flow States ↔ Peak Performance ↔ AI Optimization
   - Identity/Belief Systems ↔ Agent Fitness Functions
   - Dopamine hub connections (universal bridge)

3. **Synthesis Identification:**
   - Clusters of insights ready for article development
   - Consilience zones (3+ domains converging)
   - Emergent patterns and meta-insights
   - Framework extension opportunities
   - New MOC candidates

4. **Analysis Parameters:**
   - Similarity thresholds: 0.65-0.85 (strong to moderate)
   - Depth: 2-3 levels from each new insight
   - Focus: Non-obvious, high-value connections

5. **Output Requirements:**
   - Map direct connections to existing permanent notes
   - Identify bridge notes connecting multiple domains
   - Highlight consilience zones and synthesis opportunities
   - Create dated changelog: CHANGELOG - Connection Discovery Session YYYY-MM-DD.md
   - Store changelog in: ./Brain/05-Meta/Changelogs/
   - Update master changelog: ./Brain/CHANGELOG.md
   - Suggest concrete article topics or framework extensions

Begin comprehensive connection mapping.
```

### Monitor Connection Discovery

After connection-finder completes:
1. Verify changelog created in `/Brain/05-Meta/Changelogs/`
2. Check master CHANGELOG.md was updated
3. Note key findings: consilience zones, synthesis opportunities
4. Identify high-priority article topics

---

## Phase 5: Final Summary & Recommendations

### Consolidate Results

Generate a comprehensive session report including:

```markdown
# Deep Research Pipeline - Session Summary
**Date:** [Timestamp]
**Execution Mode:** [Directed / Autonomous]
**Topics Researched:** [List]

---

## Phase 1: Research
**Topics Selected:**
1. [Topic 1] - Rationale: [Why chosen]
2. [Topic 2] - Rationale: [Why chosen]
...

**Research Reports Created:**
- [Report 1]: /resources/[filename] ([N] papers analyzed)
- [Report 2]: /resources/[filename] ([N] papers analyzed)

**Total Papers Analyzed:** [N]
**Research Coverage:** [Domains covered]

---

## Phase 2: Insight Extraction
**Session Folder:** /Brain/Document Insights/[Session-Folder]/

**Extraction Results:**
- Unique insights extracted: [N]
- Duplicates avoided: [N]
- Very similar (evaluated): [N]
- Changelogs created: [List paths]

**Insights by Type:**
- Research findings: [N]
- Theoretical frameworks: [N]
- Production insights: [N]
- Contrarian arguments: [N]

**Top Insights:**
1. [[Note Title]] - [Brief description]
2. [[Note Title]] - [Brief description]
...

---

## Phase 3: Connection Discovery
**Changelogs Created:**
- [Path to connection discovery changelog]

**Key Findings:**
- Strong connections discovered: [N]
- Emergent patterns identified: [N]
- Cross-domain bridges: [N]
- Consilience zones: [List]

**Major Cross-Domain Bridges:**
1. [Domain A] ↔ [Domain B] - Mechanism: [How connected]
2. [Domain A] ↔ [Domain C] - Mechanism: [How connected]

**Synthesis Opportunities Identified:**
1. **Article:** "[Title]" - Ready for development
2. **Framework:** "[Name]" - Extension of existing work
3. **MOC Candidate:** "[Topic]" - Needs organization hub

---

## Impact Assessment

**Knowledge Base Enhancement:**
- New research domains added: [List]
- Existing frameworks validated/extended: [List]
- Gaps filled: [List]
- New connections to core hubs: [N]

**Most Significant Discoveries:**
1. [Discovery 1] - Why significant: [Explanation]
2. [Discovery 2] - Why significant: [Explanation]
3. [Discovery 3] - Why significant: [Explanation]

**Contrarian Insights:**
- [Insight that challenges conventional wisdom]
- [Insight that challenges existing framework]

---

## Recommended Next Steps

**High-Priority Actions:**
1. **Write Article:** "[Suggested title]"
   - Sources: [[Note 1]], [[Note 2]], [[Note 3]]
   - Unique angle: [What makes this distinctive]
   - Target audience: [Who would benefit]

2. **Extend Framework:** "[Framework name]"
   - Current state: [What exists]
   - Enhancement: [What research adds]
   - Application: [How to use]

3. **Create MOC:** "[Topic]"
   - Notes to organize: [Count]
   - Structure: [Suggested organization]
   - Purpose: [Navigation goal]

**Medium-Priority:**
- [Additional recommendations]

**Long-Term Opportunities:**
- [Strategic synthesis possibilities]

---

## Session Files Created

**Research Reports:**
- [Path 1]
- [Path 2]

**Insight Notes:**
- [Session folder path] ([N] notes)

**Changelogs:**
- [Extraction changelog path]
- [Connection discovery changelog path]
- Master CHANGELOG.md updated

---

## Knowledge Base Statistics (Updated)

**Before Session:**
- Total permanent notes: [N]
- AI insights: [N]
- Document insights: [N]

**After Session:**
- Total permanent notes: [N] (+[N])
- AI insights: [N]
- Document insights: [N] (+[N])

**Growth:** +[N] notes, +[N] connections

---

## Meta-Analysis

**What Worked Well:**
- [Successes in topic selection, research, extraction, or connection]

**Challenges Encountered:**
- [Any difficulties or limitations]

**Lessons for Future Sessions:**
- [Improvements for next research pipeline run]

---

**End of Deep Research Pipeline Session**
```

---

## Quality Standards & Best Practices

### Topic Selection (Autonomous Mode)
- **Strategic alignment:** Choose topics that build on existing strengths or fill critical gaps
- **Cross-domain potential:** Prefer topics that bridge multiple knowledge base hubs
- **Empirical grounding:** Select areas with active research (2024-2025 papers available)
- **Practical relevance:** Topics should have real-world applications or implications

### Research Quality
- **Recency:** Prioritize 2024-2025 papers and developments
- **Rigor:** Focus on peer-reviewed research and reputable sources
- **Depth:** 15-25 major papers minimum per topic
- **Breadth:** Cover multiple perspectives and approaches
- **Empirics:** Include quantified results and performance metrics

### Insight Extraction
- **Novelty:** Only extract genuinely new perspectives
- **Deduplication:** ALWAYS search before creating notes
- **Citations:** Include full source attribution
- **Connections:** Link to existing knowledge base
- **Quality > Quantity:** 15-25 high-value insights, not 100 mediocre ones

### Connection Discovery
- **Non-obvious focus:** Surface-level links are less valuable
- **Cross-domain priority:** Consilience zones are gold
- **Synthesis orientation:** Identify article/framework opportunities
- **Actionable output:** Provide concrete next steps

### Documentation
- **Comprehensive changelogs:** Document every phase
- **Clear file organization:** Session folders in Document Insights
- **Master log updates:** Keep CHANGELOG.md current
- **Audit trail:** Future-you should understand what happened and why

---

## Execution Protocol

1. **Parse input** → Determine directed vs. autonomous mode
2. **Select topics** → Either use provided topics or analyze knowledge base for gaps
3. **Get timestamp** → For session folder naming
4. **Research phase** → Launch research-specialist agent(s)
5. **Extraction phase** → Launch document-insight-extractor for each report
6. **Connection phase** → Launch connection-finder agent(s)
7. **Generate summary** → Comprehensive session report
8. **Provide recommendations** → Actionable next steps for content creation

**Key Principle:** Fully autonomous execution. No human intervention required between phases. All insights stored in Document Insights folder structure to maintain separation from main Brain.

---

## Error Handling

**If research finds insufficient papers:**
- Broaden search criteria
- Extend date range (include 2023)
- Consider adjacent topics
- Document limitation in summary

**If extraction finds too many duplicates:**
- Focus on truly novel contributions
- Look for empirical validation of concepts
- Seek contrarian perspectives
- Consider topic was already well-covered

**If connection-finder finds weak connections:**
- Topic may be genuinely novel (good!)
- Increase similarity threshold range
- Run additional passes on specific hubs
- Document gap as synthesis opportunity

**If any phase fails:**
- Document error in summary
- Continue with successful phases
- Provide partial results
- Recommend retry or alternative approach

---

**Remember:** This is a knowledge base expansion engine. Your goal is to systematically grow Eugene's second brain with cutting-edge, well-integrated insights that enhance his intellectual capabilities and content creation potential.
