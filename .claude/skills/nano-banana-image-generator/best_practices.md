# Nano Banana (Gemini Image Generation) - Best Practices

## Model Overview

**Two Tiers:**
- **Gemini 2.5 Flash Image**: $0.039/image, 1024px, optimized for speed (~22 sec), 500 free daily requests
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
