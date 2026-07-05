---
name: sector-rotation-stock-hunter
description: >
  Use this skill to find potential stocks in whatever sector currently has hot money rotating
  into it — AI/semiconductors, energy, biotech, defense, financials, or anywhere else. Supports
  two modes: riding currently popular/high-momentum names with dip-buying within an intact
  uptrend, and finding less-discovered names before they run by waiting for a completed bottom.
  Trigger on "find me potential stocks," "screen for stock picks," "semiconductor small caps,"
  "is [hot ticker] a buying opportunity," "[ticker] is down today should I add," "what's
  everyone trading right now," "hot money rotation," "swing trade setup," or any request to
  find or evaluate a breakout/continuation stock in a sector. Also trigger to follow up on a
  theme or ticker surfaced by daily-market-brief or ai-tech-pulse — pull it from there rather
  than asking the user to restate it. Use whenever the user wants to evaluate a sector-rotation
  or momentum-based stock idea, in any sector.
---

> **Canonical constants.** Risk/reward gates, the 1–2% per-trade cap, the portfolio-heat
> ceiling, VIX/RSI thresholds, and the catalyst window are defined once in
> [`references/trading-constants.md`](../../references/trading-constants.md). Use those values;
> if a number here ever disagrees with that file, the constants file wins.


# Sector Rotation Stock Hunter

## Core Philosophy

This is swing trading, not value investing. A name showing up in the news, in `ai-tech-pulse`'s
geeky-voices roster, or all over fintwit is **not disqualifying** — it's often the whole point.
Coverage and popularity usually mean real liquidity and institutional sponsorship, which is what
actually makes a swing trade executable. Waiting for something nobody's talking about means
waiting for something that, by definition, hasn't been validated by the money that moves price.

There are two genuinely different ways a candidate can qualify here. They are not the same
screen and shouldn't be blended:

- **Track A — Momentum Continuation (default).** Ride what's already working. Source from
  currently hot/popular names. The entry is a pullback *within* an intact uptrend, not a
  multi-month base. This is "go with the flow" — if the market is trading AI supply chain, trade
  AI supply chain, using the names that are already leading it.
- **Track B — Early Discovery (use on request).** Find it before the crowd notices. Source from
  sector ETF constituents that haven't run yet. The entry is a completed bottom after a real
  correction. Use this when the user explicitly wants to get ahead of a story that hasn't broken
  yet, not as the default.

**Default to Track A** unless the user says something like "find me something nobody's talking
about yet" or asks specifically for early-stage/undiscovered names.

Whichever track: this skill finds and ranks candidates. It does not decide entry price,
stop-loss, or position size — that's `swing-trade-analysis`, which every candidate from here
should pass through before any money moves. Sizing and concentration limits (the 1–2% cap,
regime-scaled heat ceiling, and correlated-exposure/theme cap) are all defined in
`references/trading-constants.md`.

**Check current positions first.** If the journal's Heat Check ran this session, use its
open-position list; otherwise ask for (or pull via IBKR) current holdings before ranking.
A candidate in a theme the portfolio already holds gets flagged — if that theme is at its
correlated-exposure cap, the candidate is a **swap decision** (is it better than what's
held?), never an add. Don't rank the user into a position they already own.

---

## Step 1: Identify the Sector/Theme to Hunt In

Three ways to land on a sector — try them in this order:

**A. The user named it directly** (a sector, or a specific ticker they're already watching) →
use that, skip to Step 2.

**B. A theme or ticker already surfaced earlier in this conversation.** If `daily-market-brief`
or `ai-tech-pulse` ran earlier in this session and flagged something with an obvious equity
angle — a rate-cut call that favors utilities, a memory-pricing story that favors DRAM/NAND
suppliers, a specific ticker from the geeky-voices roster — use that and say explicitly where it
came from. This is the preferred path when available.

**C. Neither — find what's hot from scratch.** For Track A: web_search "[sector] stocks today
gainers," "most active [sector] stocks today," "[sector] stocks momentum [current month]." For
Track B: web_search "stock sector rotation [current month/year]," "[sector] stocks institutional
buying [current quarter]."

### Mapping a theme to investable sub-sectors

| Theme example | Sub-sector angle | Reference ETF to mine | Reference large-caps / leaders |
|---|---|---|---|
| AI compute | Chip architecture / IP | SOXX, SMH, SOXQ, XSD | ARM, NVDA |
| AI compute | Optical / high-speed interconnect | SMH, XSD | ALAB, CRDO, LITE, COHR |
| AI compute | Neocloud / GPU cloud capacity | SMH, XSD | CRWV, NBIS |
| AI compute | Power & cooling for datacenters | XLU, GRID | VRT, SMCI, CEG |
| Semi equipment | Etch / deposition / test | SOXX, SMH | LRCX, AMAT, ACLS |
| Advanced packaging | HBM / CoWoS / OSAT | SOXX | AMKR, ASX |
| Energy | Upstream oil & gas | XLE, XOP | CVX, XOM |
| Biotech | Clinical-stage / catalyst-driven | XBI, IBB | regional/mega-cap leaders in the same indication |
| Defense | Aerospace & defense supply chain | ITA, PPA | LMT, RTX, NOC |
| Financials | Regional banks | KRE, XLF | JPM, BAC |
| Materials | Rare earth / critical minerals | XME, REMX | MP, ALB |
| Power infrastructure | Grid, transmission, utilities | XLU, GRID | NEE, CEG |

Starting point, not a fixed universe — if the theme doesn't map cleanly here, search for the
relevant sector ETF directly and apply the same logic.

---

## Step 2A: Track A — Momentum Continuation Screen

### Sourcing hot names
- Pull straight from `ai-tech-pulse` Section 2 if it ran this session
- Or scan what's actually moving: web_search "[sector] stocks today," "trending stocks today"
- Or just start from a name the user already mentioned or is excited about — that's valid input here, not a shortcut that needs justifying

### Technical criteria — "intact uptrend + dip," not "completed bottom"
- [ ] Stock is above its rising 50-day MA (ideally 200-day too) — the trend is still up
- [ ] Currently pulling back from a recent high, but hasn't broken key trend support
- [ ] RSI cooling from overbought (>70) toward neutral (40–60) on the pullback — not collapsing through oversold, which would suggest something's actually broken
- [ ] **Dip Diagnosis passes** (below) — this is the gate that separates "buy the dip" from "catch the falling knife"

### Dip Diagnosis — is today's drop a chance or a broken thesis?

Run this whenever the question is "X is down today, is it a chance to add?":

1. **Sector-wide or name-specific?** Check 2–3 peers in the same theme. Down similarly across the
   group → probably a flush/profit-taking, not a thesis break. This name down meaningfully more
   than peers → relative-weakness red flag, treat with more caution.
2. **What does today's news say, specifically about this name?** A single negative catalyst tied
   to fundamentals (guidance cut, lost contract, downgrade with a real reason, lawsuit) → don't
   catch it. "No real news, just giving back part of a big run" or "down with the whole sector on
   a macro/rates headline" → candidate.
3. **Is price still above the level it broke out from, or its rising 50-day MA?** Holding above →
   dip within trend. Breaking through → the leg may be over, not pausing.
4. **Volume on the down day.** Elevated red-day volume in an uptrend is often capitulation/flush
   (can mark a short-term local low). Quiet drift down on light volume is less informative either
   way — wait for a confirming green day before sizing up.

**Verdict: BUYABLE DIP / WAIT FOR CONFIRMATION / AVOID — THESIS LIKELY BROKEN**

### Fundamental criteria — "already discovered" is fine, even expected
- [ ] Real revenue/contract exposure to the theme — narrative alone still isn't enough
- [ ] No thesis-breaking news (covered by Dip Diagnosis above)
- [ ] Liquidity: average daily dollar volume high enough to actually size a position and get out
  cleanly — this matters more here than a market-cap band, since efficient capital use depends on
  being able to enter/exit without moving the price

Being heavily covered, widely held, or "everyone's talking about it" is **not a strike** in this
track — it's usually confirmation of the institutional sponsorship and liquidity that makes the
trade workable in size.

---

## Step 2B: Track B — Early Discovery Screen (use only when explicitly requested)

### Technical criteria (all should be present)
- [ ] Stock is down 30%–60% from its 52-week high (meaningful correction already happened)
- [ ] Recent volume contraction (weak hands have been shaken out)
- [ ] A volume-backed reversal candle, or 4–8+ weeks of tight, low-volume consolidation
- [ ] Weekly MACD showing bullish divergence, or RSI recovering out of oversold territory

**Buy point framework:**
- **1st buy point**: first high-volume reversal candle off the bottom (starter position only)
- **2nd buy point** (primary entry): pullback holding above the prior low on lower volume
- **3rd buy point** (confirmation/add): breakout above the consolidation range on rising volume

### Fundamental criteria
- [ ] Real, direct revenue exposure to the theme — not just a narrative/concept tag
- [ ] Revenue growth accelerating over the last 1–2 quarters, or guidance was raised
- [ ] Institutional ownership has been increasing recently (13F filings)
- [ ] Market cap roughly $500M–$10B as a default sweet spot — flexes by sector

---

## Step 3: Run the Search Sequence

**Track A:**
```
1. "[sector] stocks today gainers losers"
2. "[ticker] stock news today"
3. "[ticker] vs [peer 1] [peer 2] stock today" (sector-wide vs name-specific check)
4. "[ticker] average daily volume liquidity"
```

**Track B:**
```
1. "[sub-sector keyword] stocks pullback [current month/year]"
2. "[sector] stocks under $10 billion market cap"
3. "[sector] stocks institutional buying [current quarter]"
4. "[specific company] earnings guidance revenue growth"
5. "[reference ETF] holdings small cap not yet run up"
```

Live price/volume/52-week-range data is best pulled from the Interactive Brokers connector
(`search_contracts` → `get_price_snapshot` with `misc_statistics`) when available — it's faster
and cleaner than reconciling conflicting web snapshots, especially for Track A's "is this still
above trend support" check.

---

## Step 4: Score Each Candidate

**Track A scoring:**

| Dimension | Criteria | Points |
|---|---|---|
| Theme fit | Is it a real leader/participant in the current hot-money theme? | 0–2 |
| Trend intact | Above rising 50d MA, dip hasn't broken key support? | 0–2 |
| Dip Diagnosis | BUYABLE DIP verdict from the checklist above? | 0–3 |
| Liquidity | Average daily dollar volume sufficient to size in/out cleanly? | 0–3 |

**Track B scoring:**

| Dimension | Criteria | Points |
|---|---|---|
| Sector direction | In the current hot-money theme? | 0–2 |
| Bottom structure | Has it completed a base? | 0–2 |
| Volume signal | Volume expansion + contraction pattern present? | 0–2 |
| Fundamentals | Revenue accelerating / guidance raised? | 0–2 |
| Market cap fit | Within the sector-appropriate sweet spot? | 0–2 |

**Only consider building a position at a score of 7+, either track.**

**Scores are a shortlisting device, not a measurement.** They're judgment calls and won't
be perfectly reproducible run-to-run, so: record the sub-score for each dimension with a
one-line justification (what fact earned the points), and never treat 7-vs-6 as a real
distinction — a borderline score means "look closer," and the real gate is
`swing-trade-analysis`'s Layer 0, which is arithmetic, not judgment.

---

## Step 5: Hand Off to swing-trade-analysis

Once a candidate scores 7+, hand the ticker to `swing-trade-analysis` for entry/stop/target
and sizing.

If multiple Track A names from the *same* theme clear the bar at once (likely, since "go with
the flow" naturally produces correlated candidates), flag that explicitly when handing off —
that's exactly the case the **correlated-exposure cap** in `trading-constants.md` exists for:
the theme as a whole can carry at most half the regime heat ceiling, however many tickers
it's spread across.

---

## Output Format

```
📊 Candidate Stock Report

Track: [A - Momentum Continuation / B - Early Discovery]
Sector/theme: [theme, and where it came from]

Ticker: [TICKER]
What they do: [one-line description]
Current stage: [Track A: pulling back in uptrend / Track B: bottoming / breakout / mid leg]
Dip Diagnosis verdict (Track A only): [BUYABLE DIP / WAIT FOR CONFIRMATION / AVOID]
Score: [X/10]
Proposed entry for swing-trade-analysis: $XX
Key risks: [main risk factors]
```

Close every report with a one-line reminder that this is not financial advice, and a prompt to
run the top candidate(s) through `swing-trade-analysis` before sizing any actual position.

---

## Common Mistakes to Avoid

- ❌ Don't treat "already in the news" as disqualifying in Track A — that's the wrong instinct for momentum trading
- ❌ Don't skip the Dip Diagnosis — buying a dip without checking *why* it's down is how you catch a falling knife
- ❌ In Track B, don't chase a name that's already run 100%+ — the easy money in the leg is gone
- ❌ Don't ignore broader market regime — run `market-regime` first; in 🔴 RISK-OFF this skill builds watchlists only, no BUYABLE DIP verdicts (three of four stocks follow the general market)
- ❌ Don't size or stop-loss a position here — that's `swing-trade-analysis`'s job
- ✅ If you can't find a high-conviction single name, the sector ETF itself is reasonable default exposure to the theme

---

## Reference Cases (illustrative, not predictive)

| Track | Entry Window | Ticker | Sector/Theme | Logic | Outcome |
|---|---|---|---|---|---|
| B | Early 2025 | SANM | AI compute | EMS provider with AI server orders, bottomed first | Primary leg up |
| B | Early 2025 | TTMI | AI compute | PCB maker, AI server supply chain, bottomed first | Primary leg up |
| A | May 2025 | ARM | AI compute | Already a leader, bought dips within the uptrend | Continued uptrend |
| A | May 2025 | ALAB | AI compute | Already hot, bought pullbacks within the leg | Primary leg up |

Past performance of these names is not a guarantee the same pattern repeats — use this table to
understand the *type* of setup being targeted in each track, not as current recommendations.

**This table is survivorship-biased by construction** — it contains only setups that worked.
The same patterns fail constantly: Track A dips that were actually thesis breaks (the Dip
Diagnosis exists because of them), and Track B "completed bottoms" that were mid-decline
consolidations. The base rate for these setups is closer to a coin flip than this table
implies; the edge is in the R/R of the entries, not the pattern's hit rate. As the journal
accumulates real closed trades, *your own* failed setups become the counter-table — review
them alongside this one.
