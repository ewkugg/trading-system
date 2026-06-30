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
- **Portfolio heat cap (aggregate open risk):** **6%** total across all open swing positions.
  Before adding a new trade, sum the risk (entry-to-stop × size) of every open position.
  If the new trade would push total open risk above 6%, size down or skip — five "safe" 2%
  trades quietly become 10% exposure without this cap.
  *(6% is the default; set your own ceiling and change it here.)*

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

## Signal-quality filter (don't trust raw prints)

Before acting on any single indicator, sanity-check what's underneath it. A raw reading can
invert once filtered — e.g. a sector put/call ratio spiking to an extreme can be 90%+ penny
lottery-ticket volume, flipping "neutral" into "bearish." Always ask: is this signal real, or
an artifact of low-quality flow?
