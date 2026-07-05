# Workflow: Pre-Market Routine

**When:** before the open, on a day you might trade.
**Goal:** go from "what's the world doing" to a sized, journaled trade plan — with gates that
stop you early when conditions aren't right.

| # | Step | Skill | Decision gate → stop condition |
|---|---|---|---|
| 0 | Regime check | `market-regime` | 🔴 RISK-OFF → **stop here**: no new positions today; only manage/exit existing (skip to step 6a). 🟡 CAUTION → half heat ceiling, best setups only. |
| 0b | Heat check | `trade-journal-postmortem` (Mode 0) | Sum open risk vs. today's regime-scaled ceiling. No remaining budget → analysis is watchlist-only today. |
| 1 | Set the backdrop | `daily-market-brief` | If VIX is in the **Red** band (see constants) or a major event (FOMC/CPI) lands today → reduce risk or stand down. |
| 2 | Tech/AI read (optional) | `ai-tech-pulse` | Only if trading tech/semis. Note any theme with an equity angle. |
| 3 | Find candidates | `sector-rotation-stock-hunter` | Only if a leading sector emerged in steps 1–2. No clear leader → no new screens today. |
| 4 | Run the gate | `swing-trade-analysis` / `crypto-swing-analysis` | On each candidate. **Layer 0 must PASS (≥2:1).** REJECT → drop it, note the entry that would qualify. |
| 5 | Size it | (constants) | Position size from the 1–2% cap; heat must fit the **regime-scaled ceiling** confirmed in step 0b. |
| 6 | Journal the plan | `trade-journal-postmortem` (Mode 1) | Open a thesis for every trade taken, with its invalidation and `regime_at_entry`. No journal entry → no trade. |
| 6a | (RISK-OFF path) Review open theses | `trade-journal-postmortem` | Check each open position's invalidation against the correction — mark anything that should be cut. |

**Artifacts:** a macro note, a ranked watchlist, one checklist per candidate, and an open
thesis note per trade taken.

**Reuse rule:** steps 1–5 reuse the VIX/breadth/trend figures already fetched in step 0 —
don't re-fetch.
