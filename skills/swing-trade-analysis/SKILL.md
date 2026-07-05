---
name: swing-trade-analysis
description: >
  A systematic checklist framework — a Layer-0 R/R gate plus a 4-layer checklist
  (1 macro, 2 catalyst, 3 technical, 4 sentiment) — for swing trading analysis on any stock.
  Use this skill whenever the user asks to analyze a stock for swing trading, wave trading
  (波段交易), or short-to-medium term entry/exit decisions. Triggers include: "should I buy X now",
  "is X a good entry", "analyze X for swing trading", "help me trade X", "给我分析一下X波段", 
  "X现在能不能买", or any request combining a stock ticker with trading intent.
  The skill fetches live data (price, VIX, RSI, moving averages, earnings date, analyst sentiment)
  and synthesizes it into a concrete recommendation with specific entry/exit/stop-loss levels.
---

> **Canonical constants.** Risk/reward gates, the 1–2% per-trade cap, the portfolio-heat
> ceiling, VIX/RSI thresholds, and the catalyst window are defined once in
> [`references/trading-constants.md`](../../references/trading-constants.md). Use those values;
> if a number here ever disagrees with that file, the constants file wins.


# Swing Trade Analysis Skill

A systematic framework for evaluating any stock's swing trading opportunity. Covers macro filter,
catalyst calendar, technical setup, and sentiment — then translates all four into a clear
actionable judgment.

---

## Core Philosophy

**The market is a probability game. Predicting direction is a coin flip. Execution is what shapes the die.**

Most traders lose not because their directional judgment is wrong, but because they play games
with symmetric or negative expected value. The goal is never to "be right" — it's to ensure
every trade has a positive expected value before entry.

Expected Value = (Win Rate × Avg Gain) − (Loss Rate × Avg Loss)

A 35% win rate with 3:1 reward/risk = +EV. A 70% win rate with 0.5:1 reward/risk = −EV.
**Win rate is secondary. The shape of the die is everything.**

Three conditions must align to form a high-quality swing trade setup:
1. **Asymmetry**: Does this entry offer at least 2:1 reward/risk? If not, skip — regardless of conviction.
2. **Momentum**: Is price action supporting the directional thesis?
3. **Catalyst**: Is there a known event in the next 2–6 weeks that can drive the move?

All data serves one question: *Does the current price offer a favorable risk/reward entry for a
move toward an identifiable target, before an identifiable catalyst?*

---

## Step 1: Gather Live Data

**Check this conversation first.** If `daily-market-brief` already ran earlier in this session,
reuse its VIX, 10Y yield, and Nasdaq/S&P trend figures instead of re-searching — they won't have
moved enough intraday to matter, and re-fetching just burns calls for the same answer.

**Prefer computed numbers over scraped ones.** When the Interactive Brokers connector is
available, it is the **primary** source for anything price-derived: `search_contracts` →
`get_price_snapshot` for live prices, and `get_price_history` (daily bars) to **compute**
RSI(14), the 20/50/200-day MAs, and actual swing-high/low support-resistance levels
yourself. Entries and stops are set at these levels — they deserve exact values, not a
third-party article's stale or differently-parameterized print. Use web_search as the
fallback, and for things that aren't price series (earnings dates, analyst consensus, news):

| Data Point | Where to Find | Why It Matters |
|---|---|---|
| Current stock price | web_search "[TICKER] stock price today" | Baseline |
| VIX | web_search "VIX index today" | Macro risk filter |
| Nasdaq/S&P trend | Yahoo Finance / web_search | Directional tailwind |
| RSI (14-day) | web_search "[TICKER] RSI technical analysis" | Overbought/oversold |
| 20-day & 50-day MA | Same technical search | Trend and support |
| Next earnings date | web_search "[TICKER] next earnings date" | Catalyst anchor |
| Analyst consensus + avg target | web_search "[TICKER] analyst price target" | Sentiment gauge |
| Recent key news | web_search "[TICKER] news this week" | Sentiment events |

---

## Step 2: Run the Checklist

### Layer 0 — Risk/Reward Gate (run this FIRST, before anything else)
*Purpose: Is this trade worth playing at all, regardless of direction?*

This is the most important filter. It runs before macro, before technicals, before everything.
A trade with bad risk/reward should be rejected even if all other layers are green.

**Calculate the three numbers:**
- **Entry**: The price you would buy at (current price, or target pullback level)
- **Stop**: The price at which the trade thesis is broken (key support level, MA — see the
  stop-placement rule in `trading-constants.md`)
- **Target**: The first realistic resistance / catalyst-driven price objective

**Reward/Risk Ratio = (Target − Entry) ÷ (Entry − Stop)**

| Ratio | Verdict |
|---|---|
| < 1.5:1 | ❌ Reject. Do not proceed. The die is not in your favor. |
| 1.5–2:1 | ⚠️ Marginal. Only proceed if 3/4 other layers are green. |
| 2:1 or better | ✅ Acceptable. Proceed with full checklist. |
| 3:1 or better | ✅✅ Strong. This is the target to aim for. |

**Key insight**: Entry price is the primary lever you control.
The same stock at two different entry points can flip a 1:1 trade into a 3:1 trade.
*Waiting for a better entry is not hesitation — it is the edge.*

**Output**: PASS (≥2:1) / MARGINAL (1.5–2:1) / REJECT (<1.5:1)

If REJECT → stop here. Note the entry price that *would* make it acceptable, and monitor.

---

### Layer 1 — Macro Filter
*Purpose: Is the environment permissive for risk-on trades?*

- **Market regime first:** if `market-regime` ran this session, its verdict overrides the
  spot checks below — 🔴 RISK-OFF means Layer 1 FAILs regardless of today's VIX print, and
  🟡 CAUTION caps this trade at half size within the reduced heat ceiling. If no verdict
  exists yet, run `market-regime` before continuing.
- **VIX < 20**: Green. Clean environment for swing trades.
- **VIX 20–25**: Yellow. Proceed with smaller size, tighter stops.
- **VIX > 25**: Red. Skip or wait. Even good setups fail in fearful markets.
- **Nasdaq trend**: Is QQQ / Nasdaq above its 20-day MA? If yes, tailwind. If not, headwind.
- **10Y yield direction**: Rising = headwind for growth/tech. Falling = tailwind.

*(`crypto-swing-analysis` uses a tighter <18 threshold for "green" — that's intentional, not a
typo. Crypto's baseline volatility is higher, so the same level of market fear shows up at a
lower VIX print.)*

**Output**: PASS / CAUTION / FAIL

---

### Layer 2 — Catalyst Calendar (forward-looking)
*Purpose: Is there a known event within 2–6 weeks that can drive a move?*

Primary catalysts to check:
- **Earnings date** — the most reliable recurring catalyst. Ideal window: build position 3–4 weeks before, exit 1–2 days before the report. Never hold through earnings for a swing trade unless it's explicitly a binary bet.
- **Sector conferences / product launches** — for tech stocks especially (e.g. NVDA: GTC, CES, customer capex reports from Microsoft/Google/Amazon/Meta).
- **Macro events** — FOMC, CPI, jobs data — if the stock is highly rate-sensitive.

**Output**: YES (catalyst within window) / NO (no near-term catalyst)

If no catalyst exists within 6 weeks, downgrade confidence and reduce target size.

---

### Layer 3 — Technical Setup
*Purpose: Is price at a favorable entry point, not already extended?*

**Trend check**:
- Price above 20-day MA → short-term uptrend
- Price above 50-day MA → medium-term uptrend
- Both → strong trend confirmation

**Momentum check (RSI)**:
- RSI < 40 → potential oversold bounce setup (look for long entry)
- RSI 40–60 → neutral, momentum not extended
- RSI 60–70 → trending but not yet dangerous
- RSI > 70 → overbought, avoid chasing; wait for pullback

**Entry quality**:
- **Best entry**: Price pulling back to 20-day MA or 50-day MA on low volume, RSI declining from overbought back to neutral
- **Acceptable entry**: Price at a key support/resistance level with RSI neutral
- **Poor entry**: Price extended above moving averages with RSI > 70 (already ran)

**Support & Resistance**:
- Identify the nearest support level below current price (recent swing low, MA, round number)
- Identify the nearest resistance above (recent high, previous breakout level)
- Calculate rough risk/reward: distance to resistance ÷ distance to support

**Output**: STRONG SETUP / NEUTRAL / EXTENDED (don't chase)

---

### Layer 4 — Sentiment Check
*Purpose: Is the crowd already positioned, or is there room for upside surprise?*

- **Analyst consensus**: If >90% Buy ratings, sentiment is already crowded. Any miss will cause outsized selling. If consensus is mixed (50–70% Buy), there's more room for upgrades to drive the stock.
- **Recent news tone**: Look for whether news is incrementally positive (analyst upgrades, product announcements, beat-and-raise) or negative (downgrades, macro concerns, supply issues).
- **Implied Volatility (optional)**: If options IV is low, options pricing is cheap (good for buying calls ahead of catalysts). If IV is elevated, options are expensive.

**Output**: COLD (good for entry) / NEUTRAL / HOT (crowded, caution)

---

## Step 3: Synthesize Into a Recommendation

### Decision Matrix

Layer 0 (Risk/Reward) must pass before counting other layers.

| Layer 0 | Other Layers Green | Confidence | Suggested Action |
|---|---|---|---|
| REJECT | Any | None | Stop. Find the entry price that creates 2:1, then wait. |
| PASS | 4/4 | High | Full-size entry at current or on small pullback |
| PASS | 3/4 | Medium | Half-size entry; add on confirmation |
| PASS | 2/4 | Low | Wait. Paper trade to track the thesis |
| PASS | 1/4 | None | No trade. Note what would need to change. |

### Always Specify Four Numbers — and the Exit Plan

Every recommendation must include:
1. **Entry zone**: The price range where the R/R becomes favorable
2. **Stop-loss**: The level at which the trade thesis is broken
3. **Target**: The first realistic resistance / catalyst price objective
4. **R/R Ratio**: Explicitly state (Target−Entry) ÷ (Entry−Stop)
5. **Exit plan** (per the trade-management rules in the constants): breakeven at +1R, then
   *partial-at-2R* or *MA-trail* — pick one now, plus the time-stop date. A trade without a
   pre-chosen exit plan is only half planned.

### Expected Value Statement (optional but powerful)
If you have a rough win rate estimate for this setup type, state the EV explicitly:
> "If this setup wins 40% of the time at 2.5:1 R/R → EV = (0.4 × 2.5) − (0.6 × 1) = +0.4 per unit risked"

This makes the probabilistic logic transparent and removes emotional attachment to any single trade.

### Position Sizing & Portfolio Risk Cap

Risk no more than **1–2% of total portfolio** on any single swing trade — the same cap used in
`crypto-swing-analysis`, kept consistent across the suite regardless of asset class. There's no
good reason stocks should be governed more loosely than crypto just because they're less volatile
per-trade; the cap is what keeps one bad trade from mattering.

**Position size = (Portfolio risk %) ÷ (Entry-to-stop distance %)**

Example: $100K portfolio, 1.5% risk tolerance = $1,500 max loss on this trade. Entry $50, stop
$47 (6% distance) → max position = $1,500 ÷ 6% = $25,000 notional (500 shares).

If the user's portfolio size isn't known, fall back to the qualitative full/half-size guidance in
the Decision Matrix above, and mention that a stated portfolio size would let you give a precise
share count instead.

---

## Step 4: Present the Analysis

Structure the output as follows:

```
## [TICKER] Swing Trade Checklist — [Date]

**Current price**: $XXX
**Next earnings**: [Date] (~N weeks away)

### Layer 0: Risk/Reward Gate
- Entry zone: $XX–$XX
- Stop-loss: $XX ([reason: below 50MA / key support / max-distance rule per constants])
- Target: $XX ([reason: resistance level / catalyst objective])
- R/R Ratio: X.X:1 → PASS / MARGINAL / REJECT

### Checklist (only run if Layer 0 passes)
| Layer | Status | Key Data |
|---|---|---|
| Macro | ✅/⚠️/❌ | VIX: XX, Nasdaq trend: up/down |
| Catalyst | ✅/⚠️/❌ | Earnings in N weeks / no near-term catalyst |
| Technical | ✅/⚠️/❌ | RSI: XX, Price vs 50MA: above/below |
| Sentiment | ✅/⚠️/❌ | XX% Buy ratings, tone: hot/neutral/cold |

### Judgment
R/R: X:1 | [X]/4 layers green → [High/Medium/Low/No] confidence
Suggested action: [specific action or "wait for $XX entry"]
Position size: $XX,XXX (Y shares) at Z% portfolio risk — or full/half-size if portfolio size unknown

### Scenarios
**Scenario A (base case)**: [entry zone, target, stop, R/R]
**Scenario B (alternative)**: [if price does X instead, R/R becomes Y]

### What to Watch
[1–2 specific things that would change the thesis or improve the R/R]
```

---

## Key Principles to Always Apply

- **Direction is a coin flip. R/R is the die shape.** Never enter a trade without first calculating the ratio. A good trade at the wrong price is a bad trade.
- **Waiting for entry IS the strategy.** Identifying the right R/R entry point and waiting for price to come to you is not hesitation — it is the primary edge.
- **Stop-loss = buying the right to play again.** A trade without a stop is unlimited downside for limited upside — the exact inverse of what you want.
- **Never hold through earnings** in a swing trade unless explicitly framed as a binary catalyst bet.
- **The best entry has already passed** if RSI > 70 and price is extended. State the pullback level that would restore good R/R instead.
- **Narrative ≠ setup.** A stock can have a great long-term story and a terrible near-term R/R. Both things can be true simultaneously.

---

## Notes on Specific Asset Classes

This framework was built primarily for **individual growth stocks** (especially tech/AI like NVDA).
Adjustments for other assets:

- **S&P 500 / Index ETFs**: Replace earnings catalyst with FOMC/macro events. Use Shiller CAPE as valuation layer instead of PE.
- **Gold / GLD**: Replace RSI momentum with real interest rate direction (TIPS yield). Catalyst = Fed meetings, CPI prints.
- **BTC / ETH**: don't adapt this skill — use `crypto-swing-analysis`, which is the same
  framework with crypto-native layers (same numbering: 1 macro, 2 catalyst, 3 technical, 4 sentiment).
