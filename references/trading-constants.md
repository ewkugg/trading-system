# Trading Constants — Canonical Source of Truth

**This file is authoritative.** Every skill in this repo defers to the numbers below.
If any threshold written inside a SKILL.md ever disagrees with this file, **this file wins** —
and the SKILL.md should be corrected to point here. Change a value once, here, and the whole
system stays consistent. This is the fix for cross-skill threshold drift.

> When packaging skills as `.skill` files for the web app, `scripts/build_dist.py` copies this
> file into each skill so the web-app version stays self-contained.

---

## Layer 0 — Risk/Reward Gate (universal)

| R/R Ratio | Verdict |
|---|---|
| < 1.5 : 1 | REJECT — do not proceed |
| 1.5–2 : 1 | MARGINAL — only if 3/4 other layers green |
| ≥ 2 : 1   | PASS — proceed with full checklist |
| ≥ 3 : 1   | STRONG — the target to aim for |

`Reward/Risk = (Target − Entry) ÷ (Entry − Stop)`

The gate runs **first**, before any other layer. A bad-R/R trade is rejected even if
everything else is green. Entry price is the primary lever — waiting for a better entry
is the edge, not hesitation.

---

## Position Risk & Portfolio Heat

- **Per-trade risk cap:** **1–2% of total portfolio** on any single swing trade.
  Applies identically to stocks and crypto — no looser rule for "less volatile" assets.
- **Position size = (portfolio risk %) ÷ (entry-to-stop distance %)**
- **Stop placement:** always at a structural level (support, MA, prior swing low) — never an
  arbitrary tight %. Default max entry-to-stop distance **~7–8% for stocks**; crypto stops are
  structural-only (its noise band is wider). If the structural stop is further than the max,
  the entry is too early or the size must shrink — don't widen the risk to fit the trade.
- **Portfolio heat cap (aggregate open risk):** **6%** total across all open swing positions.
  Before adding a new trade, sum the risk (entry-to-stop × size) of every open position.
  If the new trade would push total open risk above the ceiling, size down or skip — five
  "safe" 2% trades quietly become 10% exposure without this cap.
  *(6% is the full-ceiling default; set your own and change it here.)*

### Regime-scaled heat ceiling

The 6% ceiling is the **maximum**, allowed only in a confirmed uptrend. The ceiling in
effect on any given day comes from the `market-regime` skill's verdict:

| Regime (from `market-regime`) | Heat ceiling in effect | New positions? |
|---|---|---|
| 🟢 GREEN — confirmed uptrend | 6% (full) | Yes |
| 🟡 CAUTION — uptrend under pressure | 3% (half) | Half-size only, best setups only |
| 🔴 RISK-OFF — correction | 0–1% | No new positions; manage/exit existing |

`trade-journal-postmortem`'s **Heat Check** computes current open heat from the journal's
open notes and compares it against **this regime-scaled ceiling**, not the flat 6%.

### Correlated-exposure cap (theme heat)

Three semi positions are one trade wearing three tickers. In addition to the total ceiling:

- **No single theme/sector may carry more than half the regime ceiling in effect**
  (GREEN: 3% per theme · CAUTION: 1.5% · RISK-OFF: n/a).
- Theme = the journal note's primary tag (`tags: [swing, semis]` → theme "semis"). Tag
  honestly — "AI compute" and "semis" are usually the same theme for this purpose.
- The Heat Check reports heat **by theme**, and a new candidate in an already-capped theme
  is a skip or a swap (close the weaker position first), not an add.

---

## Macro Filter — VIX thresholds

| Asset class | Green | Caution | Red (skip/wait) |
|---|---|---|---|
| Stocks / indices | VIX < 20 | 20–25 | > 25 |
| Crypto (BTC/ETH) | VIX < 18 | 18–25 | > 25 |

Crypto uses the tighter 18 threshold **intentionally** — its baseline volatility is higher,
so the same level of market fear shows up at a lower VIX print. This is not a typo.

Also check: index trend (QQQ/SPY vs 20-day MA), 10Y yield direction (rising = headwind for
growth/tech), and for crypto, DXY (dollar strength = the most consistent crypto headwind).

---

## Technical — RSI bands

| RSI | Read |
|---|---|
| < 40 | Potential oversold bounce (look for long entry) |
| 40–60 | Neutral, momentum not extended |
| 60–70 | Trending, not yet dangerous |
| > 70 | Overbought — don't chase; state the pullback level that restores good R/R |

Trend reference: price vs 20-day MA (short-term), 50-day (medium), 200-day (long-term;
below it, any long is counter-trend — size down and take profit faster).

---

## Catalyst window

- Target a known catalyst **2–6 weeks** out.
- Earnings (stocks): build 3–4 weeks before, exit 1–2 days before the report.
  **Never hold through earnings** on a swing trade unless it's explicitly a binary bet.
- No catalyst within 6 weeks → downgrade confidence, reduce target size.

---

## Expected-value framing

`EV = (Win rate × Avg gain) − (Loss rate × Avg loss)`

Direction is close to a coin flip; the R/R ratio is the shape of the die. A 35% win rate at
3:1 is +EV; a 70% win rate at 0.5:1 is −EV. Optimize the die, not the hit rate.

---

## Market-regime inputs (used by `market-regime`)

- **Distribution day:** index closes down ≥ 0.2% on volume higher than the prior session;
  counted over a rolling 25-session window. 3–4 = caution; **5+ on either index = pressure**.
- **Follow-through day (FTD):** on day 4+ of a rally attempt, a major index gains ≥ 1.25%
  on higher volume than the prior day. A correction is not over until an FTD confirms it.
- **Breadth bands (% of S&P 500 above 50-day MA):** > 60% healthy · 40–60% mixed · < 40% narrow.
- **Tie-break rule: downgrade, don't average.** Mixed inputs → the lower regime.

---

## Rule-promotion standard (weekly review → this file)

A candidate rule from the journal gets promoted into this file only if **all three** hold:

1. **Falsifiable.** Stated with an explicit invalidation, same as a trade thesis:
   "Rule: ___. This rule is wrong if ___." A rule that can't be wrong can't be trusted.
2. **Recurring.** The pattern appears in ≥ 3 separate closed trades, not one memorable loss.
3. **Back-checked.** Once ≥ 20 closed trades exist in the journal: applying the rule
   retroactively to the closed-trade log must improve average realized R (or cut average
   loss R) versus not applying it. Below 20 trades, promote provisionally and tag the rule
   `provisional:` here — the weekly review re-checks provisional rules as the sample grows,
   and demotes any that fail the back-check.

---

## Signal-quality filter (don't trust raw prints)

Before acting on any single indicator, sanity-check what's underneath it. A raw reading can
invert once filtered — e.g. a sector put/call ratio spiking to an extreme can be 90%+ penny
lottery-ticket volume, flipping "neutral" into "bearish." Always ask: is this signal real, or
an artifact of low-quality flow?
