---
created: 2026-06-04
updated: 2026-06-04
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 02.25
tags: [copper, operating-leverage, cost-curve, torque, mining-equities, investment-research, beta, value-trap, scenario-analysis]
type: investment-research
evidence-level: synthesis
horizon: "0-18 months forward; thesis is structural"
---

# Copper Equities Through the Operating-Leverage Lens

**Date**: June 4, 2026
**Thesis under test**: In a copper bull run, the best-performing copper stocks are those with the *worst margins* (highest-cost producers). Inversely, in a flat or bear market the same names fall the most.
**Spot reference**: Copper ~$13,966/t LME / ~$6.48/lb COMEX HG (June 2-4, 2026, near record highs). Goldman raised year-end target to $13,735/t on June 1.

---

## Executive Summary

The thesis is **correct, and the current data confirms it cleanly** - but the right way to operationalize it is not "buy the highest-cost miner." It is "buy the highest *operating leverage* miner whose torque is genuinely copper-price-driven and not captured, subsidized, or decoupled by something else."

Three findings:

1. **Operating leverage is real and the market prices it as beta.** Across the 12-name producer universe, the correlation between beta and the trailing one-month return (the acute bull-run window into June 4) is **+0.71, rising to +0.82 excluding the one idiosyncratically-broken name (Ivanhoe)**. The highest-torque names led: First Quantum +45.9%, Hudbay +42.2%, Capstone +40.7%, Ero +29.2% - versus the low-cost majors BHP +16.7% and Southern Copper +20.0%.

2. **Raw cost (AISC) is a noisy proxy for torque** - correlation with one-month return only **+0.25**. Three wedges break the simple "high cost = high return" rule: (a) **by-product subsidy** (Hudbay's negative cash cost is gold, not efficiency, so its torque comes from a different engine), (b) **financial / small-cap leverage** (amplifies returns independent of cost), and (c) **value extraction** (KGHM is genuinely high-cost but the Polish state copper tax captures the upside, so it returned +22.9% versus First Quantum's +45.9% despite near-identical AISC).

3. **The torque is convex and bidirectional.** Earnings sensitivity to the copper price is `Price / (Price - AISC)`. As copper falls toward a high-cost producer's all-in cost, that multiple goes vertical. At $6.40/lb copper the torque spread across the universe is modest (1.4x to 2.1x). At $3.50/lb copper it explodes: First Quantum 35x, Capstone and KGHM 17.5x, Teck 11.7x - while Southern Copper and BHP sit near 2x. **The worst-margin names are not just higher-torque; their torque accelerates exactly when copper weakens, which is why they crater hardest in a downturn and can go cash-flow-negative below their cost wall.**

**Net**: the user's instinct is sound and tradeable. The refined expression is a **clean-torque basket** - Capstone (CS), Ero (ERO), Teck (TECK) - high-cost, ~90% copper revenue, no value-extraction wedge, no disqualifying binary - plus First Quantum (FM) as a now-resolving binary kicker. The trap to avoid is mistaking *nominal* high cost (KGHM, gold-subsidized Hudbay) for *capturable* copper torque.

---

## Part 1: The Mechanism - Why Worst Margins Win in a Bull Run

A copper miner's gross profit per pound is `Copper Price - Cash Cost`. The *percentage* change in that profit for a given move in the copper price is:

```
Earnings torque  =  ΔPrice / (Price - Cost)  =  Price / (Price - Cost)   (per 1% move)
```

The denominator is the margin. A thin margin (high-cost producer) means a small absolute copper move is a large percentage swing in profit. A fat margin (low-cost producer) dilutes the same move.

**Worked example at $6.40/lb copper:**

- Low-cost producer (Southern Copper, AISC ~$1.85): margin $4.55/lb. A $1 copper move = +22% to margin.
- High-cost producer (First Quantum, AISC ~$3.40): margin $3.00/lb. The same $1 move = +33% to margin.

That gap looks small at $6.40 because *everyone* has fat margins at record copper prices. The gap widens dramatically as copper falls - which is the whole point of the inverse claim.

This is the same operating-leverage physics as a high-fixed-cost business: the closer you operate to breakeven, the more violently profit swings with revenue. In mining, the cost curve *is* the leverage ladder. The producers sitting highest on the global cost curve are, by construction, the highest-torque equities.

---

## Part 2: The Cost Curve - Ranking the Universe by Torque

All figures are 2025 actuals or 2026 guidance, $/lb. `Net cash cost` is after by-product credits; `AISC` is all-in sustaining (estimated where not separately disclosed); `Cu %` is copper's share of revenue (how much of the earnings stream actually re-rates when copper moves).

| Rank (by AISC) | Company | Net cash cost | AISC | Cu % rev | Beta | Torque type |
|---|---|---|---|---|---|---|
| 1 (lowest) | **Hudbay (HBM)** | $(0.22) | $1.74 | 62% | 2.15 | Gold-subsidized; torque is gold+small-cap, not Cu cash margin |
| 2 | **Southern Copper (SCCO)** | $0.58 | $1.85 | 78% | 1.08 | True low-cost anchor; low torque |
| 3 | **BHP (copper)** | $1.19 | $2.00 | 29% | 0.80 | Diversified; iron ore dilutes Cu torque |
| 4 | **Antofagasta (ANTO)** | $1.19 | $2.45 | 87% | 1.35 | Moderate; net cost gold/moly-dependent |
| 5 | **Freeport (FCX)** | $1.75 | $2.60 | 65% | 1.32 | Grasberg gold does the heavy lifting |
| 6 | **Lundin (LUN)** | $1.87 | $2.65 | 75% | 1.98 | Moderate-high, clean-ish |
| 7 | **Ero Copper (ERO)** | $2.06 | $2.70 | 92% | 1.56 | **Pure copper torque, small-cap amplified** |
| 8 | **Ivanhoe (IVN)** | $2.16 | $2.75 | 92% | 1.79 | High torque inside high-risk DRC wrapper |
| 9 | **Teck (TECK)** | $2.03 | $3.20 | 85% | 1.57 | **High torque, QB2 issue solvable** |
| 10 | **Capstone (CS)** | $2.44 | $3.30 | 92% | 2.08 | **Highest clean cost = purest torque** |
| 11 | **KGHM** | $2.58 | $3.30 | 72% | 1.23 | High cost but Polish tax captures upside |
| 12 (highest) | **First Quantum (FM)** | $2.00 | $3.40 | 92% | 1.94 | Maximum torque, EXTREME Panama binary |

**Critical modeling note**: do not rank torque by *net* cash cost. Net cost is gross operating cost minus by-product credits, and a low net cost can be built almost entirely from gold/silver/moly credits that do not move with copper. Hudbay's $(0.22) and Southern's $0.58 are credit-driven, not efficiency-driven. For copper-price torque, what matters is (gross cash cost) AND (copper's share of revenue). The names with both high gross cost and ~90% copper revenue - Capstone, Ero, First Quantum, Ivanhoe, Teck - are the genuine high-torque cohort.

---

## Part 3: Empirical Test - Does It Actually Hold Right Now?

Copper rallied from ~$11,500/t in early April to record highs above $14,000/t by late May, then held ~$13,966/t into June. The trailing one-month equity returns (to June 4) capture the acute leg of that bull run - the cleanest natural experiment available.

### Returns ranked

| Company | Beta | AISC | 1-month return | YTD return |
|---|---|---|---|---|
| First Quantum (FM) | 1.94 | $3.40 | **+45.9%** | +21.5% |
| Hudbay (HBM) | 2.15 | $1.74 | **+42.2%** | +52.8% |
| Capstone (CS) | 2.08 | $3.30 | **+40.7%** | +12.4% |
| Ero (ERO) | 1.56 | $2.70 | +29.2% | +8.0% |
| Freeport (FCX) | 1.32 | $2.60 | +27.1% | +36.7% |
| Lundin (LUN) | 1.98 | $2.65 | +25.9% | +42.5% |
| KGHM | 1.23 | $3.30 | +22.9% | +30.6% |
| Teck (TECK) | 1.57 | $3.20 | +21.0% | +42.0% |
| Southern (SCCO) | 1.08 | $1.85 | +20.0% | +36.0% |
| Antofagasta (ANTO) | 1.35 | $2.45 | +19.1% | +30.3% |
| BHP | 0.80 | $2.00 | +16.7% | +50.0% |
| Ivanhoe (IVN) | 1.79 | $2.75 | +16.2% | -23.0% |

### What the correlations say

- **corr(beta, 1-month return) = +0.71** (n=12); **+0.82 excluding Ivanhoe.** The market's encoding of operating leverage predicts bull-run outperformance strongly.
- **corr(AISC, 1-month return) = +0.25** (+0.28 ex-IVN). Raw cost is a much weaker predictor than beta - the confounds matter.
- **High-cost cohort (AISC ≥ $2.65) averaged +28.8% vs low-cost cohort +25.0%.** The high-cost cohort wins, but only modestly on a naive sort - because the cohort is dragged down by Ivanhoe (+16%, broken) and KGHM (+23%, taxed), and the low-cost cohort is lifted by Hudbay (+42%, high-beta/gold).

**Interpretation**: the thesis is confirmed, but beta is the tradeable signal and AISC is the fundamental *why*. A pure AISC-sorted long/short would have worked weakly; a beta-sorted or clean-torque-sorted book would have worked strongly.

---

## Part 4: The Three Wedges That Break the Naive Rule

The reason "highest cost" ≠ "highest return" in a clean 1:1 way is that three things sit between the cost curve and the stock return:

### Wedge 1: By-product subsidy (the Hudbay illusion)
Hudbay screens as the lowest-cost name (negative net cash cost) yet has the highest beta (2.15) and ripped +42%. Its negative cost is high-grade gold credits from Pampacancha (Peru) - now depleted as of December 2025. Its bull-run torque came from copper *and* gold rising together plus small-cap/financial leverage, not from a thin copper margin. **Lesson: a gold-subsidized "low-cost" miner can still be a high-torque equity, but the torque is not the copper-margin torque the thesis describes - and it decays as the by-product grade depletes.** The same caveat applies in reverse to Freeport (Grasberg gold) and Southern (zinc/silver/moly).

### Wedge 2: Financial and small-cap leverage (the amplifier)
Beta bundles operating leverage *and* balance-sheet leverage *and* liquidity/float effects. Capstone (β2.08) and Lundin (β1.98) carry more debt and smaller floats than their cost rank alone implies, which amplifies both directions. This is *additive* to the thesis (it makes high-cost small-caps even punchier) but means beta overstates the pure operating-leverage component.

### Wedge 3: Value extraction (the KGHM tax trap)
KGHM has among the highest costs in the universe ($3.30 AISC) and should, on the naive thesis, have been a top performer. It returned +22.9% - middle of the pack - because the Polish state copper tax escalates with the copper price, capturing the very torque the equity holder is trying to harvest. Management explicitly notes that ex-tax, unit costs would have fallen 17% versus the reported 3%. **A high-cost producer in a high-extraction jurisdiction is a torque trap: the operating leverage is real but it accrues to the government, not the shareholder.** Resource-nationalism royalties (Chile, DRC, Zambia, Indonesia) are softer versions of the same wedge.

---

## Part 5: Value Traps vs Clean Torque - The Idiosyncratic Layer

The highest-cost names are often high-cost *because* something is wrong with the asset or jurisdiction - and that same something can decouple the stock from copper entirely. The torque thesis only pays out if the idiosyncratic risk resolves (or is absent). A taxonomy:

| Company | Idiosyncratic overhang | Verdict |
|---|---|---|
| **Capstone (CS)** | Operational complexity (Mantoverde mill, Pinto Valley water), no single binary | **CLEAN TORQUE** - purest expression of the thesis |
| **Ero (ERO)** | Chronic Brazil execution / Tucumã ramp; no binary | **CLEAN TORQUE** - small-cap amplified |
| **Teck (TECK)** | QB2 tailings-facility constraint - *solvable*, multi-year | **CLEAN-ISH** - torque with a 2-3yr ramp drag |
| **Lundin (LUN)** | Chilean concentration, Caserones integration | **CLEAN-ISH** - moderate |
| **First Quantum (FM)** | Cobre Panama shutdown (~40% of capacity); restart decision live June 2026 | **VALUE TRAP → resolving.** +46% as anticipation cleared. A bet on Panama politics, not copper |
| **Ivanhoe (IVN)** | DRC country risk + 2025 Kakula seismic/flooding | **CONDITIONAL TRAP** - exceptional asset, decoupled near-term (YTD -23%) |
| **KGHM** | Polish copper tax (value extraction) | **TORQUE TRAP** - leverage accrues to the state |
| **Freeport (FCX)** | Grasberg mudflow (Sept 2025); restart ~2027 | **PARTIAL TRAP** - cost structure impaired until Grasberg returns |

The First Quantum case is the thesis's sharpest illustration in *both* directions: it was the worst-margin, highest-binary-risk name (a value trap through 2024-early 2026), and the moment its idiosyncratic overhang began to clear (Panama audit published May 29, restart decision imminent), its latent operating leverage delivered the single highest return in the universe (+46% in a month). **Maximum torque is maximum reward when the overhang lifts and maximum pain when it doesn't.**

---

## Part 6: The Inverse - What Happens in a Flat or Bear Market

The convexity of `Price / (Price - AISC)` is the engine of the downside claim. Earnings-torque multiple by copper price:

| Company | AISC | Torque @ $6.40 | @ $5.00 | @ $4.00 | @ $3.50 |
|---|---|---|---|---|---|
| Hudbay (HBM) | $1.74 | 1.37x | 1.53x | 1.77x | 1.99x |
| Southern (SCCO) | $1.85 | 1.41x | 1.59x | 1.86x | 2.12x |
| BHP | $2.00 | 1.45x | 1.67x | 2.00x | 2.33x |
| Antofagasta | $2.45 | 1.62x | 1.96x | 2.58x | 3.33x |
| Freeport (FCX) | $2.60 | 1.68x | 2.08x | 2.86x | 3.89x |
| Ero (ERO) | $2.70 | 1.73x | 2.17x | 3.08x | 4.38x |
| Teck (TECK) | $3.20 | 2.00x | 2.78x | 5.00x | **11.7x** |
| Capstone (CS) | $3.30 | 2.06x | 2.94x | 5.71x | **17.5x** |
| KGHM | $3.30 | 2.06x | 2.94x | 5.71x | **17.5x** |
| First Quantum (FM) | $3.40 | 2.13x | 3.12x | 6.67x | **35.0x** |

At record copper ($6.40), the torque spread is benign - 1.4x to 2.1x. As copper resets toward the high-cost cohort's all-in cost (~$3.30-3.40), their torque goes vertical and then **negative**: below ~$3.40/lb, First Quantum, Capstone, KGHM and Teck stop generating sustaining free cash flow entirely, while Southern Copper and BHP still mint $1.50-1.70/lb. That is the precise mechanism behind "they fall the most" - the high-cost names hit their cost wall first, their free cash flow collapses non-linearly, and their equity gets repriced toward distress/dilution risk while the low-cost anchors merely see compressed margins.

**Implication for positioning**: the worst-margin names are a *leveraged bet on the copper price direction*, not a structural hold. In the current setup (record price, partly-priced bull case, binary Cobre Panama supply risk into June), they are the right vehicle *if* you are bullish copper from here, and the most dangerous vehicle if you expect a flat-to-down reset. They are the high-beta sleeve, sized accordingly.

---

## Part 7: Investment Implications

### The refined expression of the thesis

**Clean-torque long basket (bullish-copper sleeve):**

| Name | Why | Sizing logic |
|---|---|---|
| **Capstone (CS)** | Highest clean cost ($3.30 AISC), 92% copper, β2.08, no binary. The single purest thesis expression. | Core of the torque sleeve |
| **Ero (ERO)** | $2.70 AISC, 92% copper, small-cap amplification, lagging YTD (+8%) = catch-up room | High-torque, watch Brazil execution |
| **Teck (TECK)** | $3.20 AISC, post-coal pure copper, QB2 issue solvable | Cleanest large-cap torque |
| **First Quantum (FM)** | Maximum torque; Panama overhang now resolving | Binary kicker - size for the binary, not as a core hold |

**Avoid as "torque plays" despite high nominal cost:**
- **KGHM** - Polish tax captures the upside (torque trap)
- **Ivanhoe (IVN)** - DRC + seismic decouple it near-term; buy on operational clarity, not as a torque proxy
- **Freeport (FCX)** - Grasberg-impaired cost structure until ~2027; a Grasberg-restart bet, not a clean torque bet

**Low-torque defensives (flat/bear sleeve):**
- **Southern Copper (SCCO), BHP** - fat margins, lowest torque, the names to rotate *into* if you turn neutral-to-bearish copper. BHP's iron-ore diversification and β0.80 make it the natural hedge against the high-cost sleeve.

### How to trade the inverse
If the view turns flat-to-bearish (e.g. Cobre Panama restart approved adding ~400kt supply, or Hormuz reopens unwinding the macro shock), the high-cost basket is where the damage concentrates. Expressions: trim/exit CS/FM/TECK, rotate to SCCO/BHP, or run a long-low-cost / short-high-cost pair to harvest the convexity directly. A long-SCCO / short-FM pair is a relatively pure "copper goes sideways or down" trade with the cost-curve convexity working for you.

### The cleanest single-factor takeaway
**Beta is the tradeable encoding of this entire thesis.** If you want the thesis in one number, sort the copper universe by beta and overweight the top in a bull tape, the bottom in a bear tape - then overlay the value-trap filter (strip out names whose high beta is a state-tax wedge, a binary event, or a gold subsidy rather than genuine copper operating leverage).

---

## Part 8: Caveats and What Would Falsify This

1. **n=12, one bull-run window.** The +0.71 beta correlation is from a single ~6-week episode. It is consistent with the structural mechanism but is not a multi-cycle backtest. A proper test would run the cost-curve-sorted long/short across the 2008, 2011, 2016, 2020 copper cycles.
2. **AISC estimates are imperfect.** Several names (BHP group copper, Freeport Americas-only, Hudbay gross) required estimation from segment disclosures. The torque table is directionally robust but not precise to the cent.
3. **By-product prices co-move.** In the current rally gold is also near records, which flatters the gold-subsidized names and muddies the "pure copper torque" read. A copper-only rally (gold flat) would separate the cohorts more cleanly and is the sharper test of the thesis.
4. **Beta is backward-looking and bundles balance-sheet leverage.** It overstates the pure operating-leverage component. A cleaner proxy would be `AISC / copper price` (proximity to the cost wall) times copper revenue share.
5. **Falsifier**: if, in the next copper down-leg, the high-cost cohort does *not* underperform the low-cost cohort by more than their beta differential implies, the convexity claim is wrong and the effect is just plain beta. Watch the Cobre Panama / Hormuz catalysts for the natural experiment.

---

## Connections to Knowledge Base

- [[copper-rerun-assessment]] - the May 17 rerun this analysis extends with the operating-leverage lens
- [[copper-bear-case]] - the original directional call; this note is factor-level, not directional
- [[china-sulphuric-acid-freeze-copper-impact]] - the supply shock driving the current bull tape that lets the torque thesis pay out
- [[copper-price-scenarios]] - the price distribution that determines whether the high-torque sleeve or the defensive sleeve is correct
- [[incentive-price-gap]] - structural floor under copper that caps the high-cost cohort's downside
- [[operating-leverage-cost-curve-torque]] - the generalizable framework (permanent note)
- [[value-trap-vs-clean-torque]] - the idiosyncratic-risk filter (permanent note)
- [[beta-as-priced-operating-leverage]] - why the market's beta already encodes the cost-curve position (permanent note)

---

## Sources

- LME cash settlement $13,966/t (Westmetall, June 2, 2026); COMEX HG $6.48-6.65/lb (Trading Economics, June 2-4, 2026)
- Goldman Sachs copper forecast raise to $13,735/t year-end (Reuters/TradingView, June 1, 2026)
- Company cost data: 2025 full-year results / 2026 guidance from SCCO, BHP, Antofagasta, FCX, Ivanhoe, KGHM, First Quantum, Teck, Hudbay, Ero, Lundin, Capstone earnings releases (Q4 2025 / Jan-Mar 2026)
- Cobre Panama final audit published May 29, 2026 (Investing News Network); restart decision pending June 2026
- US Section 232 copper tariff resolved April 6, 2026 (White House proclamation, 50% semi-finished)
- Strait of Hormuz closed since Feb 28, 2026 (CNN, day 94 as of June 2); China sulphuric acid export ban effective May 1, 2026 (Bloomberg, S&P Global)
- Equity prices, beta, returns: Yahoo Finance via market_data.json snapshot June 4, 2026
- Internal: [[copper-rerun-assessment]] (May 17, 2026), [[copper-bear-case]] (March 20, 2026)

---

*This is a factor-level analysis (which copper equities have the most torque) layered on top of the directional work in the rerun assessment. It does not make a fresh copper price call; it specifies how to express whatever directional view you hold with the right operating-leverage profile. The cost-curve torque mechanism is structural; the empirical confirmation is a single bull-run window and should be treated as corroborating, not conclusive.*
