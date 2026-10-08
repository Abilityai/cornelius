# Source-Authority Map (Template)

**Purpose:** The single source of truth for which sources Cornelius trusts when **ingesting or analyzing** information. Every skill that gates content at the door (extraction, research) or probes the web (incubation loop, domain watch) references THIS file rather than keeping its own list. Update sources here - not in individual skills.

> **This is a template.** The tier model and reject patterns are the reusable discipline. The per-domain source diet and the allowlist below are *examples* - replace them with the domains your own knowledge base actually covers. Your source diet is part of your filter; curate it deliberately.

**Not a knowledge-base structure.** This is operational config in `resources/`, deliberately outside `Brain/`.

---

## The tier model

Every source resolves to one tier (consistent with the `epistemic-classification` skill, which stamps `source-tier:` on each note):

| Tier | Meaning | Action |
|------|---------|--------|
| `primary` | The paper / text / lab / dataset itself - the issuer of the idea. | Trust, pull, extract. |
| `credible-interpreter` | A trusted secondary reading the primary faithfully. | Use; note the primary was not consulted. |
| `discovery-tier` | A source outside the allowlist surfaced by an **unanchored discovery probe** (e.g. `/domain-watch`) - a specialist analyst shop, trade press, or an outlet the allowlist never contemplated. | **May RAISE a question; may never SETTLE one.** May seed a thinking topic; may never be cited as evidence or weighed in a Bayesian update. Promote only on independent corroboration. |
| `rejected` | Content-farm / AI-generated / regurgitation / unsourced leak. | Do not extract. Reject at the door. |

**The one cross-domain rule:** prefer the primary over anyone summarizing it; reject machine-generated and content-farm material before extraction; record the tier on ingestion.

**Reach vs trust - why `discovery-tier` exists.** An allowlist is a *trust* filter - exactly right when the job is verifying a claim, exactly wrong when the job is *noticing* something. A story broken by a paywalled analyst and carried only by commentary has no legal path through a trust filter, so a strictly-allowlisted probe can only confirm, never discover. `discovery-tier` moves the gate from the door to the conclusion: an unvetted source is admitted far enough to raise a question, and no further. It is only reachable through an unanchored discovery probe - not a loophole for ordinary ingestion - and it never upgrades on its own.

---

## Per-domain source diet (EXAMPLE - replace with your domains)

### Example: Neuroscience / cognition
- **Primary:** peer-reviewed journals, preprint servers, the lab's own publications.
- **Credible interpreters:** science journalism that links and quotes the primary.
- **Reject:** pop-neuro listicles, "your brain on X" explainers without citations.

### Example: AI / agents
- **Primary:** papers, official lab research posts, model cards, reproducible benchmarks.
- **Credible interpreters:** practitioners who show code or data.
- **Reject:** hype aggregators, screenshot threads without a source.

*(Add one block per domain your KB watches.)*

---

## Web allowlist (for autonomous web probes - EXAMPLE)

The `site:` allowlist for skills that run WebSearch. Keep autonomous skills' inline copies in sync with this list.

- **Peer-reviewed:** `arxiv.org` `nature.com` `science.org` `pubmed.ncbi.nlm.nih.gov` `biorxiv.org` `pnas.org`
- **Labs / official:** `openai.com` `anthropic.com` `deepmind.google` `ai.meta.com`
- **Established outlets:** `reuters.com` `apnews.com` `economist.com` `ft.com`
- **Analytical:** `hbr.org` `quantamagazine.org` `ourworldindata.org`
- **Discovery probes are NOT bound by this list** - see `discovery-tier` above.

---

## Global reject patterns (all domains)

| Pattern | Why rejected |
|---------|--------------|
| AI-generated / content-farm articles | No original reporting, no provenance, lag |
| A summary of a paper when the paper is accessible | Prefer the primary; the summary drops nuance and can distort |
| Single-tweet / single-post "leaks" without corroboration | No accountability; high fabrication risk |
| SEO explainers, listicles, "X explained" mills | No primary content, optimised for clicks not accuracy |
| Quote mills / decontextualised quote images | Stripped of source and context; frequently misattributed |
| Hype aggregators & thought-leader reposts | Repackage others' work, add no primary signal |

---

## Maintenance

- **This file is the source of truth.** When a source proves reliable or unreliable, add/move/remove it **here**, not in a skill.
- Skills reference this file by path: `resources/SOURCE-AUTHORITY.md`.
- Autonomous skills that need an inline `site:` list keep a short synced copy labelled "subset of `resources/SOURCE-AUTHORITY.md`".
