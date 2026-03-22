# Nano Banana (Gemini Image Generation) - Best Practices

## Model Overview

**Two Tiers:**
- **Gemini 3.1 Flash Image Preview (Nano Banana 2)**: $0.067/image, 1024px, optimized for speed (~22 sec), 500 free daily requests
- **Nano Banana Pro (Gemini 3 Pro)**: Up to 4K, Google Search grounding, professional-grade (released Nov 20, 2025)

**Core Strengths:**
- Best-in-class text rendering (logos, infographics, diagrams)
- Conversational editing (iterative refinement through follow-ups)
- Character/brand consistency across multiple generations
- 10x cheaper than competitors with fast generation

**Limitations:**
- Fonts can be inconsistent (requires iteration)
- Over-smoothing on detailed elements
- Weaker artistic stylization vs Midjourney
- Complex typography struggles

---

## CRITICAL: Complexity Limits

**MANDATORY constraints for all diagram/infographic generation:**

| Element | Maximum |
|---------|---------|
| Visual boxes/shapes | **10 maximum** |
| Text pieces/labels | **10 maximum** |
| Hierarchy levels | **3 maximum** (title, main content, footer) |

**Why:** Overly complex diagrams become unreadable on mobile and fail to communicate the core concept. Simplicity = clarity.

**High-Level Explanation Approach:**
- Focus on ONE key concept per diagram
- Use visual metaphors that explain at a glance
- Prioritize "aha moment" over comprehensive detail
- If you need more than 10 elements, split into multiple diagrams

---

## Brand Styling Reference

**MANDATORY:** Apply Eugene's carousel styleguide for all infographics and diagrams.

**Styleguide Location:** `Eugene Personal Brand/Prompts/Eugene_carousel_styleguide.md`

### Quick Reference - Design Tokens

**Colors (Dark Theme):**
- Background: `#000000` (primary black)
- Text Primary: `#ffffff` (white)
- Text Secondary: `#9da2bc` (subtle gray-blue)
- Text Tertiary: `#888888` (muted gray)
- Accent Success: `#22c55e` (green checkmarks)
- Accent Error: `#ef4444` (red X marks)
- Border: `#333333` (subtle borders)

**Typography:**
- Font Family: DM Sans (primary)
- Hero/Title: Bold 700-800 weight, VERY LARGE (60-80% of frame)
- Body: Medium 500-600 weight
- Footer: Smaller, subtle

**When prompting, include:**
```
Use Eugene's brand style: black background (#000000), white text (#ffffff),
DM Sans font, bold 700 weight for titles, clean minimal design.
```

---

## Optimal Use Cases

**Perfect For:**
- Infographics and social media carousels
- Product mockups and marketing materials
- Diagrams and technical documentation
- Business graphics requiring readable text
- High-volume production workflows
- Mobile-optimized content

**Not Ideal For:**
- Hyper-realistic artistic photography
- Complex typography with multiple custom fonts
- Fine detail preservation in technical renders

---

## Prompt Engineering Best Practices

### 1. Structure: Narrative Over Keywords

**DO:** Write descriptive paragraphs
```
Create a simple infographic with black background showing a central concept
with 4-5 supporting elements around it. Use white text, DM Sans font,
bold titles. Keep it minimal - no more than 8 text labels total.
```

**DON'T:** Use keyword lists or request excessive detail
```
LinkedIn post, gradient, red, white, large text, centered, 15 boxes,
arrows everywhere, multiple fonts, detailed annotations...
```

### 2. Simplicity First

**DO:**
- "Show 3-5 key points maximum"
- "One central idea with supporting elements"
- "Clean, minimal, easy to grasp in 3 seconds"

**DON'T:**
- Request complex multi-layer diagrams
- Ask for 7+ labeled elements
- Include excessive annotations or callouts

### 3. Be Specific About Style

- **Colors**: Reference brand colors or use descriptive names
- **Typography**: Specify size relationships (VERY LARGE title, medium body, small footer)
- **Layout**: Define clear positioning (centered, top-aligned, etc.)
- **Spacing**: Request "plenty of negative space" and "clean minimal design"

### 4. Positive Framing

**DO:** "Make text very large and bold for mobile readability"
**DON'T:** "Don't make text too small"

### 5. Mobile-First Design

Always include: "optimized for mobile readability"
- Text must be readable at phone screen size
- High contrast between text and background
- Simple shapes that render clearly at small sizes

---

## Diagram Types & Templates

### Simple Framework Diagram (3-7 elements)

```
Create a simple framework diagram with black background.

CENTER: One main concept in a large circle, white text, bold
SURROUNDING: 4-5 smaller elements connected to center with simple lines
Each element: icon + 2-3 word label only

HEADER: [Title] in VERY LARGE white text
FOOTER: [Tagline] in small gray text

Style: DM Sans font, minimal, high contrast, mobile-optimized.
Maximum 8 text pieces total.
```

### Before/After Comparison (2 panels)

```
Create a simple before/after comparison with black background.

LEFT PANEL: "BEFORE" label, 2-3 pain points with red X icons
RIGHT PANEL: "AFTER" label, 2-3 benefits with green checkmarks

HEADER: [Title] spanning both panels
FOOTER: [Key insight] in small text

Style: Split design, DM Sans font, high contrast, clean.
Maximum 10 text pieces total.
```

### Visual Metaphor (single powerful image)

```
Create a visual metaphor diagram with black background.

MAIN IMAGE: [Metaphor description - e.g., "cockpit with instruments"]
LABELS: 3-4 key callouts pointing to relevant parts
Keep labels short (2-3 words each)

HEADER: [Title] in VERY LARGE white text
FOOTER: [Memorable quote]

Style: Dramatic, simple, one clear visual. DM Sans font.
Maximum 6 text labels.
```

### Timeline/Evolution (horizontal flow)

```
Create a simple timeline with black background.

LEFT: Past state (muted colors, 2-3 words)
ARROW: Transition indicator
RIGHT: Future state (vibrant colors, 2-3 words)

HEADER: [Title] in VERY LARGE white text
FOOTER: [Call to action]

Style: Horizontal flow, DM Sans font, clear progression.
Maximum 8 text pieces total.
```

---

## Article Illustration Style: Warm Infographic

**Use for:** In-article explanatory diagrams that blend cinematic warmth with clear concept explanation.

This style bridges the gap between:
- **B-roll/title images** (photographic, emotional, no explanation)
- **Standard infographics** (cold, clinical, purely functional)

### Warm Infographic Aesthetic

| Element | Specification |
|---------|---------------|
| **Background** | Warm charcoal `#2D2926` or cream `#F5F0E8` |
| **Text Primary** | Warm white `#FAF8F5` or deep brown `#3D3530` |
| **Accent 1** | Dusty rose `#D4A5A5` |
| **Accent 2** | Warm coral `#E8B4A0` |
| **Accent 3** | Muted teal `#7BA3A3` |
| **Accent 4** | Soft gold `#D4C4A0` |
| **Style** | Illustrated flat design with soft shadows |
| **Feel** | Warm, approachable, like a hand-drawn explanation |

### Key Principles

1. **Explain, don't decorate** - Every element must communicate meaning
2. **Warm palette** - Film-inspired colors, never harsh pure black/white
3. **Illustrated style** - Flat icons, soft shapes, hand-crafted feel
4. **Clear hierarchy** - Title → Main concept → Supporting details
5. **Visual metaphors** - Use relatable imagery to explain abstract concepts

### Prompt Template: Warm Infographic

```
Create a warm, illustrated infographic explaining [CONCEPT].

STYLE:
- Warm charcoal background (#2D2926)
- Soft cream text (#FAF8F5)
- Illustrated flat design with soft shadows
- Dusty rose and coral accent colors
- Hand-crafted, approachable aesthetic
- Film-inspired warm color grading

CONTENT:
- [MAIN VISUAL: Describe the central explanatory element]
- [LABELS: 3-5 key terms with brief explanations]
- [FLOW/STRUCTURE: How elements connect]

LAYOUT:
- Title at top in large warm white text
- Central diagram/illustration
- Labels with clear visual hierarchy
- Generous negative space

Keep it simple: maximum 8 text labels, one core concept.
Aspect ratio: 16:9 horizontal
```

### CRITICAL: Use Simple Words

AI image generators struggle with complex words. Use short, common words:

| Avoid (misspells) | Use Instead |
|-------------------|-------------|
| SOVEREIGNTY | ISOLATE, OWN SPACE |
| ORCHESTRATION | COORDINATE, TEAMWORK |
| HIERARCHICAL | TOP-DOWN, LEADER |
| INFRASTRUCTURE | BUILD, FOUNDATION |
| OBSERVABILITY | MONITOR, VISIBILITY |
| GOVERNANCE | CONTROL, AUDIT |

**Rule**: If a word has 4+ syllables, find a simpler alternative.

### Example: Framework Diagram (Warm Style)

```
Create a warm, illustrated infographic showing "Four Pillars".

STYLE:
- Warm charcoal background (#2D2926)
- Soft cream text (#FAF8F5)
- Illustrated flat design with soft shadows
- Each pillar uses a different warm accent color

CONTENT:
- Four illustrated pillars/columns as the central visual
- Each pillar has an icon and SHORT label (1-2 syllables):
  1. Shield icon - "ISOLATE" (dusty rose)
  2. Network icon - "COORDINATE" (coral)
  3. Lock icon - "CONTROL" (muted teal)
  4. Eye icon - "MONITOR" (soft gold)
- Pillars support a roof labeled "SUCCESS"
- Foundation labeled "YOUR TEAM"

LAYOUT:
- Title "FOUR PILLARS" large at top
- Architectural pillar diagram centered

Maximum 8 text labels. Use simple words only.
Aspect ratio: 16:9 horizontal
```

### Example: Before/After Comparison (Warm Style)

```
Create a warm before/after comparison.

STYLE:
- Warm charcoal background (#2D2926)
- Left side: muted red tones
- Right side: warm green tones

CONTENT:
LEFT ("CHAOS"):
- 5 dots with tangled messy lines
- Red X icon
- Label: "MESSY"

RIGHT ("ORDER"):
- 5 dots with clean straight lines
- Green checkmark
- Label: "CLEAN"

LAYOUT:
- Title: "CHAOS vs ORDER"
- VS in center
- Clear visual split

Maximum 6 text labels. Simple words only.
Aspect ratio: 16:9 horizontal
```

### Example: Visual Metaphor (Warm Style)

```
Create a warm, illustrated visual metaphor showing "Agent Governance as Air Traffic Control".

STYLE:
- Warm charcoal background (#2D2926)
- Soft cream and coral tones
- Illustrated, stylized (not photorealistic)
- Soft glows and shadows

CONTENT:
- Stylized control tower in center (illustrated, not photo)
- 4-5 simplified airplane icons representing agents
- Dotted flight paths showing coordination
- Control screens showing monitoring dashboards
- Labels: "Audit Trails", "Permission Gates", "Kill Switches"

LAYOUT:
- Dramatic but warm composition
- Tower as focal point
- Agents in organized flight patterns around it

Maximum 6 labels. One metaphor: governance = control tower.
Aspect ratio: 16:9 horizontal
```

### When to Use Each Style

| Style | Use Case | Example |
|-------|----------|---------|
| **Dark Infographic** (black bg) | Social media, carousels, high contrast | LinkedIn posts |
| **Warm Infographic** (charcoal bg) | Article illustrations, concept explanations | In-article diagrams |
| **Cinematic Lifestyle** (photo) | Title images, hero shots, B-roll | Article headers |

---

## Quality Checklist

Before finalizing any diagram, verify:

- [ ] **10 boxes max** - No more than 10 visual elements/shapes
- [ ] **10 text pieces max** - No more than 10 labels/text items
- [ ] **One core concept** - Can you explain it in one sentence?
- [ ] **Mobile readable** - Text visible at phone screen size
- [ ] **Brand colors** - Using Eugene's dark theme palette
- [ ] **High contrast** - White on black, clear visibility
- [ ] **Negative space** - Not cluttered, room to breathe

---

## Common Pitfalls & Fixes

| Issue | Solution |
|-------|----------|
| Too complex | Reduce to 5-7 core elements, split into multiple diagrams if needed |
| Text too small | Request "VERY LARGE text occupying 60-80% of frame" for titles |
| Cluttered design | Request "clean minimal design with plenty of negative space" |
| Low contrast | Use black background with white text per brand guide |
| Off-brand colors | Reference Eugene's carousel styleguide explicitly |
| Too many labels | Limit to 10 text pieces maximum, use icons instead of words |

---

## Cost Management

- Gemini 2.5 Flash: $0.039/image (use for most work)
- 500 free daily requests on Flash tier
- Reserve Pro tier for final deliverables requiring 4K

---

## Resources

- **Brand Styleguide**: `Eugene Personal Brand/Prompts/Eugene_carousel_styleguide.md`
- **Official Documentation**: Google AI Studio (aistudio.google.com)
- **API Access**: Gemini API via Google Cloud
- **Pricing**: $0.039/image (Flash), tier-based for Pro

---

*Last Updated: December 5, 2025*
*Added complexity limits (10 boxes/10 text max), brand styling reference, simplified templates*
