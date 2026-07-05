---
name: institutional-flow
description: >
  Track where institutional ("big player") money is going — accumulation vs. distribution on
  a specific ticker, and which sectors/themes the large flows are rotating into or out of.
  Use this skill whenever the user asks "what are institutions doing", "is smart money
  buying X", "who's accumulating/dumping this", "13F check", "insider buying", "follow the
  big money", "主力资金", "机构在买什么" — and as the flow check inside other skills: the
  hunter's sponsorship test, the decision skills' Layer 4, and the after-close review's
  exit-side check on open positions. Reads market data only; never places orders.
---

> **Canonical constants.** Caps, gates, and bands live in
> [`references/trading-constants.md`](../../references/trading-constants.md); this skill
> informs entries/exits but never overrides the Layer-0 gate or the heat ceilings.

# Institutional Flow

The market is a strategic game played around intrinsic value — price gets there via the
positioning of players large enough to move it. This skill reads their footprints. Retail
can't see order flow directly, but institutions can't hide three things: **volume** (they
are the volume), **mandatory filings** (13F, Form 4, 13D/G), and **fund flows** (ETF
creations/redemptions). Each has a different lag and a different use — the discipline is
matching the signal to the decision it can actually support.

**The signal-lag table (which evidence supports which decision):**

| Signal | Lag | Good for | Useless for |
|---|---|---|---|
| Volume signature (daily) | none | **timing** entries/exits | conviction about "who" |
| Insider Form 4 buys | ~2 days | conviction + timing | index/mega-cap names (noise) |
| ETF / fund flows | days | theme confirmation | single-stock timing |
| 13F holdings | **up to 45 days stale** | conviction, theme, "is it sponsored" | timing — never timing |
| Short interest | ~2 weeks | squeeze setups, crowding | direction by itself |

---

## Mode A — Per-ticker read ("is this name under accumulation or distribution?")

Run for a candidate before entry, or for a held position when deciding whether to stay.

### 1. Volume signature — the timely footprint (primary signal)
Pull ~60 daily bars (IBKR `get_price_history` preferred — compute, don't scrape):
- **Up/down volume balance:** are up days on higher volume than down days (accumulation),
  or the reverse (distribution)? Same logic as the index distribution-day count in
  `market-regime`, applied to one stock.
- **Volume-at-level:** heavy volume on days that *defend* a support level = someone big is
  buying there (that level is also your stop's best friend). Heavy volume on failed
  rallies = supply overhead.
- **Quiet pullbacks vs. loud breaks:** low-volume dips in an uptrend are the institutional
  "no seller" tell — this is what the hunter's Dip Diagnosis is detecting.

### 2. Filings — the conviction check
- **Form 4 insider buys** (web_search "[TICKER] insider buying Form 4"): clustered open-market
  buys by officers/directors are among the strongest single signals; sales are mostly noise
  (compensation). Weight buys, ignore routine sales.
- **13F trend** (web_search "[TICKER] 13F institutional ownership latest quarter"): is the
  institutional holder count / total position rising quarter-over-quarter? Any new
  high-conviction holders (concentrated funds, not index adds)? **State the filing date** —
  a 13F says what a fund held up to 45 days ago, so it confirms *sponsorship*, never *entry
  timing*.
- **13D/G** filings = activist/concentrated stakes — rare but decision-relevant.

### 3. Positioning extremes
- **Short interest & days-to-cover:** high + rising against an uptrend = squeeze fuel;
  high + price breaking down = informed shorts, respect them.
- **Options skew, if notable** (web_search "unusual options activity [TICKER]"): treat as
  anecdote unless corroborated — much "unusual activity" reporting is engagement bait.

### Verdict
```
## [TICKER] Institutional Flow — [Date]
Volume signature (60d): ACCUMULATION / NEUTRAL / DISTRIBUTION  [key evidence, 1 line]
Insider activity:       BUYING / QUIET / (noise)               [who, when]
13F trend (as of [filing date]): SPONSORED-RISING / FLAT / THINNING
Short interest:         XX% float, X days to cover → [read]
→ Flow verdict: BIG MONEY ACCUMULATING / NEUTRAL / DISTRIBUTING
→ For an OPEN decision: [supports entry / neutral / argues for waiting]
→ For a CLOSE decision: [no distribution signs / warning: distribution while you hold]
```

## Mode B — Market-wide rotation ("where is the big money going?")

Run when the question is themes, not tickers (feeds the hunter's Step 1):
- **Sector ETF flows, 1–4 weeks** (web_search "sector ETF flows this week"): which sectors
  are taking in money, which are bleeding.
- **Relative volume by sector:** which sector ETFs are trading above average volume on up
  moves.
- **Breadth by sector** (reuse `market-regime` data if it ran): a sector whose % above
  50-MA is expanding while the index's is flat = rotation target.
- **13F season note:** in the weeks after quarterly deadlines (mid-Feb/May/Aug/Nov),
  web_search "13F filings [quarter] biggest new positions" for the conviction map.

Output: 2–3 sectors money is rotating **into** (hand to the hunter), 1–2 it's leaving
(flag if you hold them).

---

## Handoffs

- **→ `sector-rotation-stock-hunter`:** Mode B's inflow sectors are hunt targets; Mode A's
  ACCUMULATING verdict is the "institutional sponsorship" evidence Track A wants.
- **→ decision skills (Layer 4):** the flow verdict slots into the sentiment layer — a
  crowded-hot name *with* distribution signature is the classic top; a cold name under
  quiet accumulation is the setup.
- **→ after-close review (exit-side):** for each open position, a DISTRIBUTING verdict
  while the trade is aging is a "tighten the stop / take the partial early" flag — record
  it in the thesis note.
- **→ journal:** Mode A verdict at entry goes in the checklist snapshot, so postmortems can
  eventually test whether flow-confirmed entries outperform (rule-promotion standard applies).

## Principles

- **Match signal lag to decision speed.** 13Fs answer "is it sponsored," volume answers
  "now or not now." Using a 45-day-old filing to time an entry is the classic retail error.
- **Insider buys > insider sales, always.** People sell for many reasons; they buy
  open-market for one.
- **You are not front-running them; you are surfing them.** Institutions take weeks to
  build positions — the goal is to be positioned *while* they accumulate, which is why the
  volume signature outranks every filing.
- **Absence of evidence is evidence here:** a "hot" narrative name with no accumulation
  signature and thinning 13F sponsorship is retail holding the bag — that's a Layer 4 fail.
