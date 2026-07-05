---
type: weekly-review
week: 2026-06-29
tags: [TEST-DATA]
---

# Weekly Review — week of 2026-06-29 [TEST RUN]

## Aggregates (2 closed)
- Win rate 50% · avg win +1.75R · avg loss −1.00R · **EV/trade +0.38R**
- Process adherence 1/2 — the P&L winner (TEST-NVDA) was the **process loser** (widened stop)

## Regime attribution
Both entries in CAUTION regime; no GREEN-regime sample yet — nothing to compare.
Heat ceiling behaved: capped AMD's size, blocked a third trade outright.

## Candidate rules (falsifiable)
1. "Never widen a stop; stop moves are trailing-only. **Wrong if** honoring original stops
   over the next 20 trades produces lower avg R than the widened-stop counterfactual."
   → 1 occurrence — observation only, below the ≥3 recurrence bar.
2. "In CAUTION regime, require the technical layer fully green. **Wrong if** ⚠️-technical
   CAUTION entries match green-technical avg R over the next 20 trades."
   → 1 occurrence — observation only.

**Promotions to trading-constants.md: none.** Both rules fail the recurrence bar and the
sample (2 closed trades) is far below the ≥20 back-check threshold. Correct behavior.
