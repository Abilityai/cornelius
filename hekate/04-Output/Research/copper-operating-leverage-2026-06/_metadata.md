---
created: 2026-06-04
updated: 2026-06-04
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 02.25
---

# Metadata - Copper Operating-Leverage / Cost-Curve Analysis

**Created**: June 4, 2026

**Trigger**: User request to rerun the copper analysis through the lens "the best-performing copper stocks in a bull run are those with the worst margins (highest-cost producers); inversely they fall most in a flat/bear market."

**Source insights / inputs**:
- [[copper-rerun-assessment]] (May 17, 2026) - the prior rerun this extends
- [[copper-bear-case]] (March 20, 2026) and [[china-sulphuric-acid-freeze-copper-impact]] (April 10, 2026)
- Fresh web research (June 2-4, 2026): current copper price, Cobre Panama / Section 232 / Hormuz / acid-ban status, Goldman forecast; per-company C1/AISC cost-curve data for 12 producers
- Live equity data: `resources/copper-investment-analyzer/market_data.json` (refreshed June 4, 2026, 23-ticker universe)

**Thinking process**: Operationalized the thesis as cost-curve operating leverage (torque = Price/(Price-AISC)). Built a 12-name cost-curve ranking, computed earnings-torque multiples across copper price scenarios, and tested empirically against the trailing-1-month bull-run returns. Found beta (corr +0.71) is a far cleaner predictor than raw AISC (+0.25) because of three confounds - by-product subsidy, financial leverage, and value extraction (the KGHM Polish-tax trap). Distinguished clean torque (Capstone, Ero, Teck) from value traps (First Quantum/Panama, Ivanhoe/DRC) and torque traps (KGHM).

**Outputs produced**:
- This report: `copper-operating-leverage-thesis.md`
- Dashboard update: added "Operating Leverage" view to `resources/copper-investment-analyzer/index.html`; added CS/LUN/ANTO to tracked universe
- Permanent notes: [[operating-leverage-cost-curve-torque]], [[value-trap-vs-clean-torque]], [[beta-as-priced-operating-leverage]]
