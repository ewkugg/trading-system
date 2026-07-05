---
name: market-regime
description: >
  Determine the current market regime — GREEN / CAUTION / RISK-OFF — from breadth,
  distribution days, follow-through-day status, and VIX, and output the portfolio-heat
  ceiling that regime allows. Use this skill whenever the user asks "is it safe to trade",
  "what's the market regime", "how's market health/breadth", "are we in an uptrend or
  correction", "how much exposure should I carry", "现在大盘环境怎么样", or at the START of
  any pre-market routine — the regime verdict gates everything downstream. Also run it
  whenever swing-trade-analysis or crypto-swing-analysis is about to run and no regime
  verdict exists yet in this session. This is upstream of every entry decision: VIX
  measures fear, this skill measures whether the rally actually has participation.
---

> **Canonical constants.** VIX bands, the regime→heat-ceiling mapping, and all other
> thresholds live in [`references/trading-constants.md`](../../references/trading-constants.md).
> If a number here disagrees with that file, the constants file wins.

# Market Regime

The top of the funnel. Individual setups fail in a weak tape no matter how clean the chart —
the O'Neil finding this skill operationalizes is that three out of four stocks follow the
general market's direction. This skill answers one question before any name is analyzed:
**does the general market currently support new risk, and how much?**

It does not pick stocks or time entries. It outputs a regime verdict plus the heat ceiling
that verdict allows, which every downstream skill then inherits.

---

## Step 1: Gather the four inputs

**Check this conversation first** — if `daily-market-brief` already ran, reuse its VIX and
index-trend figures. Prefer the Interactive Brokers connector for live prints
(`search_contracts` → `get_price_snapshot` for SPY/QQQ/VIX, `get_price_history` for the
volume comparisons below); fall back to web_search where IBKR isn't available.

### A. Distribution-day count (institutional selling)
Over the **last 25 trading sessions**, count days where the S&P 500 or Nasdaq closed
**down ≥ 0.2% on volume higher than the prior session**. (A distribution day "falls off"
the count after 25 sessions, or after the index rallies ≥ 5% above that day's close.)
- 0–2 days: normal
- 3–4 days: institutions are lightening up — caution
- 5+ days on either index: the uptrend is under real pressure — expect a correction

Search fallback: "distribution days count S&P Nasdaq [current month]" — IBD publishes this
daily in its Market Pulse; use their count if a fresh one is available rather than
reconstructing it.

### B. Follow-through-day (FTD) status — only when in a correction
If the market has been in a correction (index below recent highs after a ≥ 5% decline),
check whether a **follow-through day** has confirmed a new rally attempt: on **day 4 or
later** of a rally attempt, a major index rises **≥ 1.25% on volume higher than the prior
day**. No FTD → the correction is not confirmed over, regardless of how green today looks.

Search fallback: "follow through day market [current month]" (again, IBD's Market Pulse
states the current outlook explicitly: "confirmed uptrend", "uptrend under pressure",
"market in correction").

### C. Breadth (participation)
- **% of S&P 500 stocks above their 50-day MA** (and 200-day if easily available).
  Search: "percent of stocks above 50 day moving average S&P 500 today" (or index
  $SPXA50R). Above ~60% = healthy participation; 40–60% = mixed; below ~40% = narrow,
  rally is being carried by a handful of megacaps.
- Quick cross-check: equal-weight vs cap-weight (RSP vs SPY, both vs their 20-day MA).
  Cap-weight up while equal-weight lags = narrow leadership.

### D. VIX
Use the bands in `references/trading-constants.md` (stocks: <20 green, 20–25 caution,
>25 red).

---

## Step 2: Score the regime

| Regime | Conditions (typical shape) |
|---|---|
| 🟢 **GREEN** — confirmed uptrend | ≤ 2 distribution days, no unresolved correction (or FTD confirmed), breadth > 60% above 50-MA, VIX in green band |
| 🟡 **CAUTION** — uptrend under pressure | 3–4 distribution days, or breadth 40–60% / narrowing, or VIX in caution band, or FTD recent but unproven (< 2 weeks old) |
| 🔴 **RISK-OFF** — correction | 5+ distribution days, or index below 50-day MA with breadth < 40%, or VIX in red band, or in correction with no FTD |

Judgment call at the margins: **downgrade, don't average.** If two inputs say GREEN and two
say RISK-OFF, the verdict is CAUTION at best — mixed signals are themselves information
that the environment is not clean.

---

## Step 3: Output the verdict and the heat ceiling

The regime maps to a **portfolio-heat ceiling** (canonical mapping in
`references/trading-constants.md`): GREEN → full ceiling, CAUTION → half, RISK-OFF →
no new positions. State the ceiling explicitly so downstream skills and the journal's
Heat Check (`trade-journal-postmortem`) can use it without re-deriving it.

```
## Market Regime — [Date]

**Verdict: 🟢 GREEN / 🟡 CAUTION / 🔴 RISK-OFF**
**Heat ceiling in effect: X% (see constants: regime-scaled heat table)**

| Input | Reading | Signal |
|---|---|---|
| Distribution days (25d) | N on SPX / N on Nasdaq | normal / caution / pressure |
| FTD status | n/a — in uptrend / FTD confirmed [date] / correction, no FTD | ... |
| Breadth (% > 50MA) | XX% | healthy / mixed / narrow |
| VIX | XX.X | green / caution / red |

**What changes the verdict:** [the 1–2 specific things that would upgrade or downgrade it —
e.g. "a 6th distribution day", "an FTD on volume", "breadth reclaiming 60%"]
```

---

## Handoffs

- **→ `swing-trade-analysis` / `crypto-swing-analysis`:** the verdict feeds their Layer 1
  macro filter — a RISK-OFF verdict means Layer 1 FAILs regardless of that day's VIX print.
- **→ `trade-journal-postmortem` (Heat Check):** the heat ceiling from this verdict is the
  number open-position risk gets compared against.
- **→ `sector-rotation-stock-hunter`:** in RISK-OFF, the hunter should build watchlists
  only — no "buyable dip" verdicts while the general market is in correction.
- Record the verdict in any journal thesis opened the same day (the checklist snapshot's
  macro row), so postmortems can later test whether trades taken in CAUTION/RISK-OFF
  regimes underperformed — that's the feedback loop that validates this skill itself.

---

## Principles

- **Three of four stocks follow the market.** A perfect setup in a RISK-OFF tape is still
  a low-probability trade — the gate exists to be respected precisely when a chart looks
  tempting.
- **Breadth beats price.** An index at highs on 35% participation is weaker than an index
  chopping sideways on 65% — narrow rallies fail from the inside out.
- **Count, don't feel.** Distribution days and FTDs are mechanical definitions; use the
  counts, not the mood of that morning's headlines.
- **The verdict decays.** A regime read is good for the day, not the week — re-run it each
  session you might trade (the pre-market routine does this automatically).
