---
name: nano-banana-image-generator
description: Generate images using Google's Nano Banana 2 (Gemini 3.1 Flash Image Preview). Use when creating infographics, diagrams, thumbnails, social media graphics, or any AI-generated images. Costs $0.067/image.
allowed-tools: Bash, Read, Write
---

# Nano Banana Image Generator

Generate images using Google's Gemini 3.1 Flash Image Preview model (codename: Nano Banana 2).

## Quick Start

**Generate a simple image:**
```bash
bash ~/.claude/skills/nano-banana-image-generator/scripts/generate.sh "A red apple on white background" apple.png
```

**Generate a 16:9 thumbnail:**
```bash
python3 ~/.claude/skills/nano-banana-image-generator/scripts/generate_thumbnail.py "YouTube thumbnail showing AI agents" /tmp/thumb.png
```

**Generate with custom output directory:**
```bash
OUTPUT_DIR=/tmp bash ~/.claude/skills/nano-banana-image-generator/scripts/generate.sh "Sunset over mountains" sunset.png
```

## Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `scripts/generate.sh` | General image generation | 1024x1024 PNG |
| `scripts/generate_thumbnail.py` | 16:9 thumbnails | 1344x768 PNG |
| `scripts/generate_image.py` | Python with aspect ratio control | Configurable |

## Pricing & Limits

- **Cost**: $0.067 per image
- **Free tier**: 500 requests/day
- **Generation time**: ~22 seconds
- **Resolution**: 1024x1024 (square), 1344x768 (16:9)

## Best Practices

For detailed prompt engineering and brand styling guidelines, see [best_practices.md](best_practices.md).

### Critical Constraints

| Element | Maximum |
|---------|---------|
| Visual boxes/shapes | **10 maximum** |
| Text pieces/labels | **10 maximum** |
| Hierarchy levels | **3 maximum** |

### Prompt Structure

**DO:** Write narrative descriptions
```
Create a simple infographic with black background showing a central concept
with 4-5 supporting elements. Use white text, DM Sans font, bold titles.
```

**DON'T:** Use keyword lists
```
LinkedIn post, gradient, red, white, large text, 15 boxes, arrows everywhere
```

### Brand Styling (Eugene's)

Include in prompts for brand consistency:
```
Use Eugene's brand style: black background (#000000), white text (#ffffff),
DM Sans font, bold 700 weight for titles, clean minimal design.
```

## Use Cases

**Perfect For:**
- Social media infographics and carousels
- YouTube thumbnails
- Diagrams and technical documentation
- Product mockups
- Mobile-optimized content

**Not Ideal For:**
- Hyper-realistic photography
- Complex multi-font typography
- Fine detail technical renders

## Environment Variables

- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - API key (required)
- `OUTPUT_DIR` - Output directory (default: current directory)

## Examples

**Infographic:**
```bash
bash scripts/generate.sh "Simple framework diagram with black background. CENTER: 'AI Agents' in large white text. SURROUNDING: 4 icons for Planning, Memory, Tools, Learning. DM Sans font, minimal design." agents_framework.png
```

**Thumbnail:**
```bash
python3 scripts/generate_thumbnail.py "Professional YouTube thumbnail: bold white text 'DEEP AGENTS' on dramatic black background with subtle blue glow, tech aesthetic" deep_agents_thumb.png
```
