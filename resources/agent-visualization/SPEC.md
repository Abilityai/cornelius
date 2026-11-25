# The Self-Rendering Mind — Agent Visualization Spec

> **Purpose of this file:** a complete, self-contained brief for building a visual
> interface for the Cornelius agent (a knowledge-base "second brain"). It is written to be
> implemented on a **fresh/empty context** — assume the implementer has not seen the
> conversation that produced it. Everything needed is here or pointed to.
>
> **Created:** 2026-06-22 · **Status:** SHIPPED (2026-06-23) · **Location:** `resources/agent-visualization/`
> (a working artifact, not an Obsidian/Brain note — do not move it into `Brain/`).
>
> ℹ️ **This file is the original design brief, kept for rationale and the design tokens (§4).**
> The build shipped and went well past it. For *what actually exists and how to run it*, see
> **`README.md`** (current source of truth) and the **`/brain-orb`** skill. Highlights beyond this
> brief: find-and-jump search, hover highlighting, rendered markdown + wikilinks, clickable tensions,
> recency + **domains** colour modes (domains highlights areas of the KB as connected groups), a
> three-panel briefing fed by real metrics/activity, freeze-on-zoom motion, and an embedded **voice**
> (Cornelius) that drives the orb (topic-cluster highlight, open any note, persisted while showing)
> and queries the live KB. Phases 1–4 (§9) are all complete.

---

## 0. The core idea (read this first)

Most "AI agent" UIs are a chat box plus a decorative gradient blob. **Do not build that.**
This agent has a genuinely unusual internal structure, and the visualization's whole job is
to make that structure *visible and alive*. The guiding line:

> **The orb is not a mascot in front of the brain. The orb *is* the brain, rendered in real time.**

The reference north star is the Midjourney homepage hero: a sphere built **from its own
generated text**, so the interface "feels like it's generating intelligence in real time."
Our sphere is built from the agent's own notes/edges/activation, curled into a globe.

Three truths about the agent must be expressible in the visual:

1. **It is made of its own structure** — atomic notes (nodes) bonded by typed edges.
2. **It metabolizes** — notes have heat, decay, contradictions, and a life cycle; the system
   even gets "hungry" when idle and reaches outward for new input.
3. **It has a guarded membrane** — the line between what it has merely *read* and what its
   owner has *endorsed*. This is the emotional center, not a footnote.

---

## 1. What is actually being visualized (the agent's internals)

This is the data model the visuals encode. (Engine: a "Brain Dependency Graph" / BDG layered
over a local vector search. You do **not** need to modify the engine — you read from it. See §6.)

- **Nodes** = atomic notes (~700 permanent + thousands of extracted/document insights).
- **Edges** are **typed + directed**: `derives-from`, `instantiates`, `references`,
  `associates`, `tension`, `supersedes`. Authority is *edge-local* (a note can be authoritative
  in one relationship and subordinate in another).
- **7 layers (altitude/meaning):** `signal → impression → insight → framework → lens →
  synthesis → index`. Raw signal at the top; bedrock structure (frameworks, indices) at the bottom.
- **Lifecycle phase per note:** `reflective → crystallizing → generative`. Notes mature with use.
- **Staleness propagation:** when a framework note changes, staleness flows *downstream* with
  attenuation (distance decay + hub dampening). It is a contagion/diffusion, not a flag.
- **Tension edges** = productive contradictions (high semantic similarity + opposing
  conclusions). They are **immune to staleness** and surfaced as synthesis opportunities.
- **Spreading activation** (query time): relevance propagates as a wavefront with **lateral
  inhibition** — competing notes suppress each other. Intent classification colors the wave.
- **Q-values / usage learning:** notes used often (retrieved/read/referenced/linked) get
  reinforced — a heat/reward landscape that reshapes over time.
- **Two outward/inward organs:**
  - *Perception* ("domain-watch"): scans the outside world for signals, pulls them in.
  - *Cognition* ("incubation-loop"): open questions gestate over days; each scheduled run
    applies one rotating analytical move (ACH audit / Bayesian update / steelman / cross-domain
    bridge / implication check) until a topic **converges** (same hypothesis leads 3+ runs).
  - *Starvation floor:* when the thinking queue empties, the system self-seeds a new topic
    from watched domains rather than going idle — it "gets hungry."
- **The membrane (provenance):** every note carries `provenance ∈ {originated, endorsed,
  encountered, ai-inferred}`. The guarded boundary is `encountered → endorsed`: **only the human
  owner promotes a claim across it.** AI may synthesize, but its output stays quarantined and
  tagged `ai-inferred` until endorsed. **This is the one thing the interface must dramatize.**

---

## 2. The concept: one living object

A single, full-bleed living sphere on a deep cosmic-void background. Not a dashboard.

- **Body:** a globe woven from the real graph — nodes as points of light, typed edges as
  threads. At rest it slowly rotates (cf. the "cell-lattice orb": fused cells held by an
  iridescent membrane — Endless Tools reference, §5).
- **Skin:** glassy, iridescent, with an atmospheric particle field drifting around it (Active
  Theory reference). Drifting motes = `encountered` signals and incoming domain-watch particles.
- **Metabolism (always-on, subtle):**
  - recently-active notes glow **hot**; cold ones dim (Q-values → luminance).
  - editing/touching a framework triggers a **grey staleness wave** that bleeds outward across
    the surface and fades.
  - **tension edges pulse red** — live seams that never heal.
- **Fly inside:** zoom in and the sphere becomes a navigable world (Mapbox-style luminous
  labeled nodes / Memotron-style radial graph). Depth maps to the 7 layers: surface = today's raw
  signal, core = bedrock generative notes. Incubating topics appear as warm "thought-cells" in the
  interior that **hatch** on convergence.
- **The membrane moment:** `ai-inferred` crystallizations hover *just outside* the bright
  `endorsed` core — glowing but quarantined. An endorsement action opens a pore and lets one in.
  Make this legible and deliberate.

**Selecting a node** opens a minimal inspector (note title, layer, lifecycle phase, provenance,
heat, top connections) — cf. Memotron's right-side metadata panel. Keep it quiet; the orb is the star.

---

## 3. Visual state machine

The orb has states (this is what separates it from a static graphic). Each is a distinct
"behavior" of the same object — animate transitions, don't hard-cut.

| State | Trigger | Visual behavior |
|---|---|---|
| **Idle** | no activity | slow rotation, gentle breathing scale (~6s loop), low ambient heat |
| **Hungry** | idle past threshold (starvation floor) | sphere contracts slightly, dims, then emits searching tendrils/particles outward (perception reaching out) |
| **Ingesting** | new note / domain-watch hit | particle streams *into* the surface; a new node lights up and finds its layer/neighbors |
| **Listening** | user speaking (voice) | surface ripples in time with audio amplitude (cf. Vapi equalizer field); cool palette |
| **Thinking** | query / incubation run | spreading-activation **wavefront** crosses the graph with lateral inhibition; intent tints the wave (Unicorn aurora) |
| **Speaking** | agent responding | rhythmic pulses synced to output cadence; warm palette |
| **Converged** | incubation topic converges | an interior thought-cell brightens and "hatches"; one-time celebratory bloom |

If wiring real voice/agent events is out of scope for v1, drive states from a simple
scripted timeline or keyboard toggles so the behaviors are demonstrable.

---

## 4. PRIMARY design tokens — Midjourney ("Deep-ocean bioluminescent terminal")

Use this as the foundation for mood, palette, and type. (Reverse-engineered from midjourney.com;
Refero style id `1e85631f-1e2e-41fa-a5dc-b1604bdbe25a`.)

### Colors
```
--color-cosmic-void:   #06051d   /* base background — violet-black, NOT pure #000 */
--color-deep-navy:     #061434   /* hero gradient terminus (top) */
--color-abyssal-blue:  #0f1c36   /* secondary surfaces, button bg variant */
--color-steel-navy:    #1d293d   /* cards, nav, containers */
--color-deep-slate:    #314062   /* elevated / hover surfaces */
--color-mist:          #cad5e2   /* primary body text (blue-gray, not white) */
--color-fog:           #e5e7eb   /* borders, dividers, icon strokes */
--color-ghost-white:   #ffffff   /* headings, max contrast */
--color-ice-blue:      #ebf8ff   /* high-brightness text on dark */
--color-portal-blue:   #63b3ed   /* the ONLY saturated body accent — links */
/* "specimen" accent triad — use sparingly, categorical not hierarchical */
--color-spec-green:    #00bc7d   /* on bg #004f3b @20% */
--color-spec-amber:    #f0b100   /* on bg #733e0a @20% (section-heading icons) */
--color-fault-red:     #ff2056   /* error/icon strokes — also good for tension pulses */
```
Background base: `linear-gradient(0deg, #06051d 30%, #061434)`.

### Typography
- **JetBrains Mono** is the universal typeface — nav, headings, body, buttons, labels.
  Monospace as identity, not a code exception. Weight **400** everywhere (headings are NOT bold).
  Substitutes: Fira Code, Source Code Pro.
- **DM Sans** (weights 400/500) only for occasional body prose. Substitutes: Inter, Outfit.
- Type scale: caption 14px/1.63 · body 16px/1.5 · heading 30px/1.25.

### Spacing & shape
- Radius: cards/images/inputs **8px**; buttons/pills **9999px** (only these two values).
- Section gap 64px · card padding 32px · element gap 8–16px · content max-width ~800px.
- Density: comfortable.

### Component flavor
- **Pill buttons:** 9999px, `8px 20px` padding, translucent tinted bg @~20% opacity, matching
  bright text, white border @10%, soft double shadow. They read as "specimen labels," not CTAs.
- **Section heading:** 30px JetBrains Mono w400 + small amber icon prefix, 8px gap.
- **Inline link:** `#63b3ed`, no underline.

### Do / Don't (load-bearing)
- ✅ Mono dominates; backgrounds stay in the `#06051d`→`#314062` dark range; whisper-weight headings.
- ❌ No pure black, no light mode, no bold headings, no solid-fill opaque buttons, no 4th accent color.

---

## 5. Secondary aesthetic references (borrow one detail each)

Local previews in `./references/`. To pull *full tokens* for any of these, a fresh agent with the
Refero MCP can call `refero_get_style` with the id. Source sites work; Refero `/styles/` page URLs
do **not** resolve in a browser (SPA) — use the source site or the local image.

| Role in our design | Site / source | Refero style id | Local image |
|---|---|---|---|
| **Self-rendering hero** (primary, §4) | midjourney.com | `1e85631f-1e2e-41fa-a5dc-b1604bdbe25a` | `references/midjourney.jpg` |
| **Skin + particle field** (orb material, drifting motes) | activetheory.net | `9d795615-79d0-4544-ac5e-2858971c3b3b` | `references/active-theory.jpg` |
| **Activation aurora** (thinking wavefront, violet WebGL) | unicorn.studio | `48b99380-a66c-46b3-adc7-96158448e1a8` | `references/unicorn-studio.jpg` |
| **Activation bars** (Q-value heat / listening equalizer) | vapi.ai | `11db6cab-35f4-43bb-9ec3-053523f6b531` | `references/vapi.jpg` |
| **Living tissue / world surface** (fly-inside) | monopo.vn | `76c30104-1a19-42e7-a585-19505882f600` | `references/monopo-saigon.jpg` |
| **Metabolism heat palette** (warm = active) | suno.com | `9844e7bf-4bff-48e6-8efc-e45002ce5226` | `references/suno.jpg` |

**Screen references** (re-pull pixels with `refero_get_screen_image` + id, full size):
- Orb-as-fused-cells (the literal "membrane lattice"): Endless Tools `4c94b142-3b65-49ce-bc62-43b64a1cfcaf`
- Luminous labeled world (fly-inside): Mapbox `38ad837d-dab4-42f4-9cff-d7932157784d`
- Radial knowledge graph + metadata inspector: Memotron `b95bc43c-7b44-4f0a-9375-91d393a7b39a`,
  `1f61c589-764c-43fd-a363-13eacac93467`
- Orb + voice/chat split (state inspiration): Xbox `a2abc259-c7d1-4fbd-aca3-ea165b10f2db`,
  ChatGPT voice `3c237d7b-9a87-4393-a536-d6726a7888a7`

---

## 6. Mapping data → visual encoding

| Internal signal | Source field | Visual encoding |
|---|---|---|
| Note | graph node | point of light on/in the sphere |
| Edge type | `derives-from / references / ...` | thread color/style; `tension` = red |
| Layer (1–7) | BDG layer | depth from surface (signal) to core (index) |
| Lifecycle phase | `reflective/crystallizing/generative` | size / solidity / glow maturity |
| Q-value (usage heat) | learning data | luminance / warmth |
| Staleness | propagation output | grey diffusion wave, attenuating with distance |
| Tension | tension edges | persistent red pulse, immune to dimming |
| Provenance | `originated/endorsed/encountered/ai-inferred` | position vs. membrane; `ai-inferred` quarantined outside core |
| Spreading activation | query event | traveling wavefront + lateral inhibition dimming of neighbors |
| Incubation topic | thinking registry | interior thought-cell; brightness = confidence; hatch on convergence |

---

## 7. Real data sources (to feed the prototype real graph data)

The agent's repo root is the working dir. Read-only:

```bash
# Graph health + counts (good first call)
resources/brain-graph/run_brain_graph.sh status --json

# Per-note lifecycle phases (reflective/crystallizing/generative)
resources/brain-graph/run_brain_graph.sh lifecycle --json

# Productive contradictions (tension edges)
resources/brain-graph/run_brain_graph.sh tensions --json

# One node's neighborhood + authority
resources/brain-graph/run_brain_graph.sh inspect "Note Name" --json

# Downstream staleness from a changed note
resources/brain-graph/run_brain_graph.sh propagate "Note Name" --json
```

- BDG enrichment sidecar (typed edges, layers, etc.): `resources/brain-graph/data/graph_enrichments.json`
- Vector index + semantic graph (nodes/edges, ~3k nodes / ~25k edges): `resources/local-brain-search/`
  (see its `README.md`; `data/q_values.json` + `data/usage_history.jsonl` hold the heat signal).

> ⚠️ Verify exact JSON shapes at build time — do not assume field names. **Build against the
> fixture below first** (so the prototype runs with zero dependencies), then swap in a real export.

### Data contract / fixture shape
```json
{
  "nodes": [
    { "id": "n1", "title": "Flow is a selfless state",
      "layer": 3, "lifecycle": "crystallizing",
      "provenance": "originated", "heat": 0.82, "stale": 0.0 }
  ],
  "edges": [
    { "source": "n1", "target": "n2", "type": "derives-from", "weight": 0.7 }
  ],
  "tensions": [ { "a": "n3", "b": "n4", "strength": 0.66 } ],
  "incubation": [ { "topic": "agentic-ai-regulation-principle", "confidence": 0.41, "converged": false } ]
}
```

> **As shipped, the export extends this fixture** (see `README.md` → Data and `export_data.py`):
> nodes also carry `degree`, `age_days`, and full `content`; top-level also includes `meta`,
> `converged` (real conclusion text), `metrics`, `activity`, and `recent`. The exporter is the
> source of truth for the shape.
> `meta.notice` is a plain-language line when the vault holds no notes yet (an empty brain, #21), otherwise null - show it in the briefing instead of an empty canvas.

---

## 8. Tech approach

- **Self-contained front-end** — `index.html` (markup + one inline Three.js module) plus a linked
  `styles.css`; no build step, no framework required. Open in a browser (works on `file://` too).
- Rendering: **Canvas 2D** is enough for an MVP (points + lines + glow via shadowBlur). For the
  3D sphere / fly-inside, **Three.js (r160+) via CDN** + a custom point/line material; particle
  field as an additive-blended `Points` cloud. Either is acceptable — choose by time budget.
- Animation loop: `requestAnimationFrame`; drive metabolism from a clock + the data fields.
- Keep all tokens from §4 in `:root` CSS variables. Use JetBrains Mono via Google Fonts CDN.
- Data: `fetch('./data.json')` against the fixture (§7); structure the loader so a real export
  drops in unchanged.
- No external analytics, no network calls beyond fonts + CDN libs. Self-contained and offline-capable.

Files (as shipped):
```
resources/agent-visualization/
├── SPEC.md            (this design brief)
├── README.md          (current source of truth — features, run, data shape)
├── index.html         (the visualization — markup + inline Three.js module)
├── styles.css         (the stylesheet, linked from index.html)
├── export_data.py     (builds data.json + data.js from the live graph)
├── data.json          (real export; loaded by fetch)
├── data.js            (same data as window.AGENT_DATA, for file://)
├── voice/             (embedded voice: orb.html + proxy_server.py, copied from voice-mode)
└── references/*.jpg    (aesthetic references)
```
Launched by the `/brain-orb` skill (`.claude/skills/brain-orb/`).

---

## 9. Build phases & acceptance criteria

**Phase 1 — Static identity (look locked).**
- [ ] `#06051d`→`#061434` gradient background; JetBrains Mono throughout; whisper-weight headings.
- [ ] A rotating sphere of node-points + edge-threads rendered from `data.json`.
- [ ] Nodes glow by `heat`; tension edges pulse red. Reads as "made of its own structure."

**Phase 2 — Metabolism.**
- [ ] Idle breathing + slow rotation.
- [ ] Trigger a staleness wave from a node and watch it diffuse + fade.
- [ ] Hungry state: contract + emit searching particles.

**Phase 3 — States + voice.**
- [ ] Listening/Thinking/Speaking states (scripted or wired to real events).
- [ ] Thinking shows a spreading-activation wavefront with neighbor dimming.

**Phase 4 — Fly inside + membrane.**
- [ ] Zoom transitions sphere → navigable interior world; depth = layer.
- [ ] Node selection → minimal inspector panel.
- [ ] Membrane: `ai-inferred` items quarantined outside the `endorsed` core; an endorse action
      opens a pore and admits one. (This is the signature moment — get it right.)

**Definition of done (v1):** Phases 1–2 complete and visually faithful to §4; runs by opening
`index.html`; clearly *not* a generic chat-blob — a stranger should look at it and say "that thing
is alive and made of something."

---

## 10. Things to NOT do
- Don't build a chat sidebar + decorative blob. Don't use pure black or a light theme.
- Don't make the graph a flat 2D force layout with no altitude/heat/membrane — that's the boring
  version this spec exists to avoid.
- Don't let `ai-inferred` content render as if it were endorsed/originated — the membrane is the
  ethical spine of the whole agent; honor it visually.
