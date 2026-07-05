---
name: trading-navigator
description: >
  The front door to the trading system — routes a natural-language goal to the right skill or
  workflow, and is the map of how the pieces fit together. Use this skill whenever the user is
  unsure where to start, states a broad goal, or asks to run a routine: "what should I do today",
  "where do I start", "which skill for this", "run my pre-market routine", "help me get set up",
  "我该用哪个", or any vague trading intent that doesn't clearly name one skill. Also use it to
  resolve overlap when several skills could plausibly trigger (brief vs. pulse vs. hunter).
---

# Trading System Navigator

The router and map. It doesn't analyze markets itself — it points the user at the right skill or
workflow and documents how the system fits together. When a request clearly names a single skill,
just use that skill; reach for the navigator when the goal is broad, ambiguous, or spans steps.

> **Canonical constants** live in [`references/trading-constants.md`](../../references/trading-constants.md).
> **Workflows** (formalized multi-skill routines) live in [`workflows/`](../../workflows/).

---

## The system in five stages

*("Stage" = a tier of this pipeline. "Layer 0–4" always means the checklist inside the
decision skills — Layer 0 is the R/R gate. The journal's functions are the Heat Check and
Modes 1–3. Three distinct vocabularies, on purpose.)*

```
REGIME       is it safe to trade   → market-regime (sets the heat ceiling for the day)
   ↓
INTEL        what's happening      → daily-market-brief, ai-tech-pulse
   ↓
DISCOVERY    what to look at       → sector-rotation-stock-hunter
   ↓
DECISION     enter? where?         → swing-trade-analysis, crypto-swing-analysis
   ↓
MEMORY       what happened / learn → trade-journal-postmortem
```

Data flows top to bottom; lessons flow back up. The navigator (this skill) and the constants
file sit beside all five stages as the meta level. The regime verdict scales the portfolio-heat
ceiling for everything below it (see the regime-scaled heat table in the constants file).

---

## Routing table

| User goal / phrasing | Send them to |
|---|---|
| "is it safe to trade", "market health/breadth", "how much exposure", "大盘环境" | `market-regime` |
| "how much heat am I carrying", "can I add a position" | `trade-journal-postmortem` (Heat Check) |
| "what's going on in markets", "morning macro", "今日市场" | `daily-market-brief` |
| "what's new in AI/tech", "interesting takes on X" | `ai-tech-pulse` |
| "find candidates in [sector]", "what's hot right now" | `sector-rotation-stock-hunter` |
| "should I buy [stock] here", "analyze [ticker]", "波段" | `swing-trade-analysis` |
| "should I buy BTC/ETH", "crypto entry" | `crypto-swing-analysis` |
| "log / journal this trade", "I closed X", "复盘" | `trade-journal-postmortem` |
| "review my month", "did I follow my rules" | `trade-journal-postmortem` (Mode 3) |
| "run my pre-market routine" | `workflows/pre-market-routine.md` |
| "end-of-day review" | `workflows/after-close-review.md` |
| "weekly review" | `workflows/weekly-review.md` |
| "what should I do / where do I start" | ask one scoping question, then route |

---

## Resolving overlap

- **brief vs. pulse:** macro/rates/Fed → brief; AI/chips/model news → pulse. If both apply, run
  brief first (sets the risk backdrop), then pulse.
- **brief/pulse vs. hunter:** the digests *surface* themes; the hunter *screens tickers* within a
  theme. A digest should hand off to the hunter, not screen tickers itself.
- **hunter vs. analysis:** hunter produces a ranked watchlist; analysis runs the full Layer-0
  checklist on a single name. Hunter → analysis, never skip the gate.
- **any analysis → journal:** whenever an analysis skill yields an actionable entry, offer to open
  a thesis in `trade-journal-postmortem`.

---

## Handoff principle

Every handoff carries forward the numbers already computed (don't re-fetch what a prior skill in
the same session already pulled — the regime verdict + heat ceiling from `market-regime`, the
open-position list from the journal's Heat Check, the brief's VIX/DXY). The journal closes the loop:
its periodic review can promote a durable lesson into `references/trading-constants.md`, which then
updates every skill at once.
