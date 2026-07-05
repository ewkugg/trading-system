# Workflow: Pre-Market Routine

**When:** before the open, on a day you might trade.
**Goal:** go from "what's the world doing" to a sized, journaled trade plan — with gates that
stop you early when conditions aren't right.

| # | Step | Skill | Decision gate → stop condition |
|---|---|---|---|
| 1 | Regime check | `market-regime` | 🔴 RISK-OFF → **stop here**: no new positions today; only manage/exit existing (skip to step 8). 🟡 CAUTION → half heat ceiling, best setups only. |
| 2 | Heat Check | `trade-journal-postmortem` (Heat Check) | Total open risk vs. today's regime-scaled ceiling **and heat by theme vs. the correlated-exposure cap**. Outputs the open-position list for steps 4–6. No remaining budget → analysis is watchlist-only today. |
| 3 | Set the backdrop | `daily-market-brief` | If VIX is in the **Red** band (see constants) or a major event (FOMC/CPI) lands today → reduce risk or stand down. |
| 4 | Tech/AI read (optional) | `ai-tech-pulse` | Only if trading tech/semis. Section 2 tickers are a **handoff feed** to step 5, not conclusions. |
| 5 | Find candidates | `sector-rotation-stock-hunter` | Only if a leading sector emerged in steps 3–4. **Flag any candidate that duplicates a theme already held (from step 2's position list)** — capped theme = skip or swap. No clear leader → no new screens today. |
| 6 | Run the gate | `swing-trade-analysis` / `crypto-swing-analysis` | On each candidate. **Layer 0 must PASS (≥2:1).** REJECT → drop it, note the entry that would qualify. |
| 7 | Size it | (constants) | Position size from the 1–2% cap; must fit both the **regime-scaled ceiling** and the **theme cap** confirmed in step 2. |
| 8 | Journal the plan | `trade-journal-postmortem` (Mode 1) | Open a thesis for every trade taken, with its invalidation and `regime_at_entry`. No journal entry → no trade. On the RISK-OFF path: instead review each open thesis's invalidation against the correction — mark anything that should be cut. |

**Artifacts:** a macro note, a ranked watchlist, one checklist per candidate, and an open
thesis note per trade taken.

**Reuse rule:** steps 3–7 reuse the VIX/breadth/trend figures already fetched in step 1, and
the position list from step 2 — don't re-fetch.
