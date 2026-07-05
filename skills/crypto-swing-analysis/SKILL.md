---
name: crypto-swing-analysis
description: >
  A systematic checklist framework — a Layer-0 R/R gate plus a 4-layer checklist — for swing trading BTC and ETH (days to weeks). Layer numbering matches swing-trade-analysis (1 macro, 2 catalyst, 3 technical, 4 sentiment).
  Use this skill whenever the user asks to analyze Bitcoin or Ethereum for swing trading,
  wave trading, or short-to-medium term entry/exit decisions. Triggers include:
  "should I buy BTC now", "is ETH a good entry", "analyze bitcoin for swing trading",
  "help me trade ETH", "is bitcoin going up", "good time to buy crypto",
  "BTC entry point", "ETH setup", "crypto swing trade", or any request combining
  BTC/ETH/Bitcoin/Ethereum with trading, buying, entry, or timing intent.
  The skill fetches live data (price, RSI, moving averages, Fear & Greed, funding rate,
  ETF flows, DXY, VIX) and synthesizes it into a concrete recommendation with specific
  entry/exit/stop-loss levels. Always run this skill for BTC or ETH swing trade questions
  even if it seems like a simple price check — the user almost always wants actionable guidance.
---

> **Canonical constants.** Risk/reward gates, the 1–2% per-trade cap, the portfolio-heat
> ceiling, VIX/RSI thresholds, and the catalyst window are defined once in
> [`references/trading-constants.md`](../../references/trading-constants.md). Use those values;
> if a number here ever disagrees with that file, the constants file wins.


# Crypto Swing Trade Analysis Skill

A systematic framework for evaluating BTC or ETH swing trading opportunities over a
days-to-weeks timeframe. Covers macro filter, on-chain sentiment, technical setup,
and catalyst calendar — then translates all four into a clear actionable judgment.

Each coin is analyzed **separately** since BTC and ETH have different drivers.

---

## Core Philosophy

**The crypto market is a probability game shaped by liquidity, sentiment, and macro.**

Crypto amplifies both the upside and the downside of stock market dynamics. The same
R/R discipline that applies to stocks applies here — but with higher volatility,
24/7 price action, and sentiment that can reverse within hours on a single headline.

Three conditions must align for a high-quality crypto swing setup:
1. **Asymmetry**: Does this entry offer at least 2:1 reward/risk? If not, skip.
2. **Momentum**: Is price action and on-chain sentiment supporting the thesis?
3. **Catalyst**: Is there a macro or crypto-specific event that can drive the move?

---

## Key Differences from Stock Swing Trading

| Factor | Stocks | BTC / ETH |
|---|---|---|
| Earnings catalyst | Yes | No — use macro events + ETF flows instead |
| Valuation | PE ratio | MVRV ratio (skip if not available) |
| Sentiment tools | Analyst ratings | Fear & Greed Index, funding rate |
| Market hours | 9:30–4 PM | 24/7 — gaps don't exist, but Asia/US sessions matter |
| Correlation | Sector | BTC leads ETH; both follow macro risk appetite |
| Safe haven behavior | Gold goes up in fear | Crypto goes DOWN in fear (risk asset, not safe haven) |
| Dollar effect | Moderate | Strong — DXY up = crypto down |

---

## Step 1: Gather Live Data

**Check this conversation first.** If `daily-market-brief` already ran earlier in this
session, reuse its VIX, 10Y yield, and DXY figures instead of re-searching — they won't
have moved enough intraday to matter, and re-fetching just burns calls for the same answer.
Otherwise, search for current values before running any layer. Each search should be fresh —
do not rely on memory for price or sentiment data.

**Prefer computed numbers over scraped ones.** If a crypto-capable data connector is
available (IBKR carries BTC/ETH via crypto contracts and futures), pull daily bars and
**compute** RSI(14) and the 20/50/200-day MAs directly rather than trusting a scraped
article's values — stops sit at these levels. web_search remains the source for
sentiment-type data (Fear & Greed, funding, ETF flows).

### For BTC:
| Data Point | Search Query |
|---|---|
| Current BTC price | "bitcoin price today" |
| BTC RSI (14-day) | "bitcoin RSI technical analysis today" |
| BTC 20-day & 50-day MA | "bitcoin moving average 20 50 200 day today" |
| BTC key support/resistance | "bitcoin support resistance levels today" |
| Fear & Greed Index | "crypto fear and greed index today" |
| BTC funding rate | "bitcoin funding rate today" |
| Bitcoin ETF flows | "bitcoin ETF inflows outflows today" |
| VIX | "VIX index today" |
| DXY (US Dollar Index) | "DXY dollar index today" |
| Geopolitical / macro news | "bitcoin crypto news today" |

### For ETH:
| Data Point | Search Query |
|---|---|
| Current ETH price | "ethereum price today" |
| ETH RSI (14-day) | "ethereum RSI technical analysis today" |
| ETH 20-day & 50-day MA | "ethereum moving average 20 50 day today" |
| ETH key support/resistance | "ethereum support resistance levels today" |
| Fear & Greed Index | (same as BTC — it covers the whole market) |
| ETH funding rate | "ethereum funding rate today" |
| ETH staking yield / network activity | "ethereum staking yield gas fees today" |
| ETH-specific catalyst | "ethereum upgrade roadmap 2025 2026" |

---

## Step 2: Run the Checklist

### Layer 0 — Risk/Reward Gate (run this FIRST)
*Purpose: Is this trade worth playing at all?*

This is the most important filter. A trade with bad R/R should be rejected even if
all other layers are green. Crypto's volatility makes this gate even more critical
than it is for stocks.

**Calculate the three numbers:**
- **Entry**: The price you would buy at (current price, or target pullback level)
- **Stop**: The price at which the thesis is broken (key support, MA, or volatility-based %)
- **Target**: The first realistic resistance / round-number / catalyst objective

**Reward/Risk Ratio = (Target − Entry) ÷ (Entry − Stop)**

| Ratio | Verdict |
|---|---|
| < 1.5:1 | ❌ Reject. Do not proceed. |
| 1.5–2:1 | ⚠️ Marginal. Only proceed if 3/4 other layers are green. |
| 2:1 or better | ✅ Acceptable. Proceed with full checklist. |
| 3:1 or better | ✅✅ Strong. This is the target to aim for. |

Because crypto moves further and faster than stocks, set stops at structural levels
(not arbitrary tight percentages) or the position will be shaken out by normal noise.

**Output**: PASS (≥2:1) / MARGINAL (1.5–2:1) / REJECT (<1.5:1)

If REJECT → stop here. Note the entry price that *would* make it acceptable, and monitor.

---

### Layer 1 — Macro Filter
*Purpose: Is the broad risk environment permissive?*

- **Market regime first:** if `market-regime` ran this session, its verdict overrides the
  spot checks below — 🔴 RISK-OFF means Layer 1 FAILs (crypto sells off hardest in a
  risk-off tape), 🟡 CAUTION caps size at half within the reduced heat ceiling. If no
  verdict exists yet, run `market-regime` before continuing.
- **VIX < 18**: Green. (Tighter than the stock skill's <20 threshold — intentional. Crypto's
  baseline volatility is higher, so the same level of market fear shows up at a lower VIX print.)
- **VIX 18–25**: Yellow. Proceed with smaller size, tighter structural stops.
- **VIX > 25**: Red. Skip or wait — crypto sells off hardest in fearful tape.
- **DXY direction**: Dollar strength is the single most consistent crypto headwind. Rising DXY = headwind; falling DXY = tailwind.
- **Equity risk tone**: Is QQQ / S&P above its 20-day MA? Crypto rides the same risk-on/off current.

**Output**: PASS / CAUTION / FAIL

---

### Layer 2 — Catalyst Calendar
*Purpose: Is there a known event in the next 2–6 weeks that can drive a move?*

- **ETF flow trends** — the dominant institutional catalyst for BTC; watch for accelerating in/outflows.
- **Macro events** — FOMC, CPI, jobs data. Crypto is highly rate- and liquidity-sensitive.
- **Protocol events** — for ETH especially: upgrades, staking/roadmap milestones, gas dynamics.
- **Geopolitical / regulatory** — headlines move crypto faster and harder than stocks.

**Output**: YES (catalyst within window) / NO (no near-term catalyst)

If no catalyst exists within 6 weeks, downgrade confidence and reduce target size.

---

### Layer 3 — Technical Setup
*Purpose: Is price at a favorable entry, not already extended?*

- **Trend**: Above 20-day MA = short-term uptrend; above 50-day = medium-term; above 200-day = the longer-term trend is confirmed (below 200-day = any long is counter-trend — size down).
- **RSI**: <40 potential oversold bounce; 40–60 neutral; 60–70 trending; >70 overbought, wait for pullback.
- **Support / resistance**: Identify nearest support below and resistance above. **Round numbers matter more in crypto** ($60K, $70K, $100K are psychological magnets).
- **Best entry**: Pullback to 20/50-day MA or a defended support level with RSI cooling from overbought to neutral.

**Output**: STRONG SETUP / NEUTRAL / EXTENDED (don't chase)

---

### Layer 4 — On-Chain Sentiment
*Purpose: Is the crowd already positioned, or is there room for the move?*

- **Fear & Greed Index**: Extreme Fear (<25) near support = contrarian long setup. Extreme Greed (>75) = late, expect chop or pullback; don't chase.
- **Funding rate**: The crowd's leveraged bet. Heavily positive funding = longs crowded, squeeze risk to the downside. Negative funding + extreme fear = squeeze setup to the upside.
- **ETF flows**: Sustained net inflows = institutional bid underneath price. Outflows = distribution; treat rallies with suspicion.

**Output**: COLD (good for entry) / NEUTRAL / HOT (crowded, caution)

---

## Step 3: Synthesize Into a Recommendation

### Decision Matrix

Layer 0 must PASS before counting other layers.

| Layer 0 | Other Layers Green | Confidence | Suggested Action |
|---|---|---|---|
| REJECT | Any | None | Stop. State the price that creates 2:1 R/R. Monitor. |
| PASS | 4/4 | High | Full-size entry at current or on small pullback |
| PASS | 3/4 | Medium | Half-size entry; add on confirmation |
| PASS | 2/4 | Low | Wait. Track the thesis. |
| PASS | 1/4 | None | No trade. State what would need to change. |

### Always Specify Four Numbers — and the Exit Plan

Every recommendation must include:
1. **Entry zone**: Price range where R/R becomes favorable
2. **Stop-loss**: Level where trade thesis is broken — and it must be a **resting order at
   the exchange**, never mental (24/7 market, per constants)
3. **Target**: First realistic resistance / catalyst price objective
4. **R/R Ratio**: Explicitly state (Target−Entry) ÷ (Entry−Stop)
5. **Exit plan** (per the trade-management rules in the constants): breakeven at +1R, then
   *partial-at-2R* or *MA-trail* — pick one now, plus the time-stop date.

### Crypto Position Sizing & Portfolio Risk Cap

Always remind the user:
- Crypto is significantly more volatile than stocks (roughly 3–5x).
- Never risk more than **1–2% of total portfolio** on a single crypto swing trade — the
  same cap used in `swing-trade-analysis`, kept consistent across the suite regardless of
  asset class.
- If using leverage, reduce size further — liquidation risk is asymmetric.

**Position size = (Portfolio risk %) ÷ (Entry-to-stop distance %)**

Example: $100K portfolio, 1.5% risk = $1,500 max loss. Entry $60,000, stop $55,200 (8%
distance) → max position = $1,500 ÷ 8% = $18,750 notional.

If the user's portfolio size isn't known, fall back to the qualitative full/half-size
guidance in the Decision Matrix, and mention that a stated portfolio size would let you
give a precise figure instead.

---

## Step 4: Present the Analysis

```
## [BTC / ETH] Swing Trade Checklist — [Date]

**Current price**: $XX,XXX
**Coin**: Bitcoin / Ethereum

### Layer 0: Risk/Reward Gate
- Entry zone: $XX,XXX – $XX,XXX
- Stop-loss: $XX,XXX ([reason: below 50MA / key support / -X%])
- Target: $XX,XXX ([reason: resistance / round number / prior high])
- R/R Ratio: X.X:1 → PASS / MARGINAL / REJECT

### Checklist (only run if Layer 0 passes)
| Layer | Status | Key Data |
|---|---|---|
| Macro | ✅/⚠️/❌ | VIX: XX, DXY: XXX, Market trend: up/down |
| Catalyst | ✅/⚠️/❌ | [Event] in N weeks / no near-term catalyst |
| Technical | ✅/⚠️/❌ | RSI: XX, Price vs 50MA: above/below, vs 200MA: above/below |
| On-Chain Sentiment | ✅/⚠️/❌ | Fear & Greed: XX, Funding rate: X.XX%, ETF flows: +/-$XXM |

### Judgment
R/R: X:1 | [X]/4 layers green → [High/Medium/Low/No] confidence
Suggested action: [specific action or "wait for $XX,XXX entry"]

### Scenarios
**Scenario A (base case)**: [entry, target, stop, R/R if trade plays out]
**Scenario B (risk case)**: [what happens if key level breaks, revised R/R]

### What to Watch
[2–3 specific signals that would confirm entry or invalidate the thesis]

### Position Sizing Reminder
Max risk per trade: 1–2% of total portfolio. Crypto volatility is 3–5x stocks.
```

---

## Key Principles

- **Crypto is a risk asset, not a safe haven.** Fear = sell crypto. Relief = buy crypto.
- **BTC leads ETH.** If BTC is breaking down, don't enter ETH long just because ETH looks cheap.
- **The funding rate is the crowd's bet.** Negative funding + extreme fear = squeeze setup.
- **DXY is the invisible hand.** Dollar strength is the single most consistent crypto headwind.
- **Round numbers matter more in crypto** than in stocks. $60K, $70K, $100K are not just levels — they are psychological magnets.
- **24/7 market means news hits harder overnight.** A thesis can be invalidated while you sleep — size and stops must assume you won't be watching.
- **Below the 200-day, every long is counter-trend.** You can still trade it, but it's a bounce, not a new bull leg — take profits faster.
