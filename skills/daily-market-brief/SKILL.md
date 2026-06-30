---
name: daily-market-brief
description: >
  Use this skill whenever the user wants a daily/today's market brief, morning macro update,
  or a synthesized overview of what's happening in markets right now. Triggers include:
  "give me today's market brief", "what's happening in markets today", "morning brief",
  "macro update", "give me a rundown of the market", "今天市场怎么样", "给我一个今日市场简报",
  "宏观简报", "市场综述", or any request to combine rates/inflation/growth data, market
  sentiment/structure indicators, today's market-moving news, and notable commentary from
  market commentators on X (Twitter) into one digest. Use this skill even if the user only
  asks generically for "today's market" or "what's going on out there" — don't wait for them
  to name specific indicators; gather a well-rounded set by default and synthesize it into a
  short, opinionated brief, not a data dump.
---

> **Canonical constants.** Risk/reward gates, the 1–2% per-trade cap, the portfolio-heat
> ceiling, VIX/RSI thresholds, and the catalyst window are defined once in
> [`references/trading-constants.md`](../../references/trading-constants.md). Use those values;
> if a number here ever disagrees with that file, the constants file wins.

> **News sources.** Curated, prioritized feeds live in
> [`references/news-sources.md`](../../references/news-sources.md). Pull from there rather than
> hard-coding sources in this skill.


# Daily Market Brief

A skill for producing the kind of short, synthesized brief a macro trading desk reads before
the open: a handful of high-signal data points, the news that actually moved something, and
a couple of sharp quotes from people worth listening to — not a wall of every indicator that
exists.

---

## Core Philosophy

**A brief is a filter, not a feed.** The point isn't to report every number — it's to tell the
reader what changed, why it matters, and what to watch. Three questions should guide every
section:

1. **What's new?** Skip data points that haven't moved or haven't been refreshed since the last
   release — a number repeated for the tenth day in a row adds noise, not signal.
2. **So what?** Every figure should connect to a takeaway ("10Y up 8bps on hot PPI → reduces
   odds of a September cut") rather than sit there unexplained.
3. **What's next?** Flag the next catalyst (FOMC, CPI print, NFP Friday, a Fed speaker) so the
   reader knows what could move things before the next brief.

If there's nothing notable in a category that day, say so in one line ("Inflation: no new prints
since last week's CPI, no change to the picture") rather than padding it out.

---

## Step 1: Orient — date, session, and what's on the calendar today

Before pulling data, establish:
- Today's actual date (use it in every search query — don't rely on memory for "latest")
- Whether markets are open today (skip/note accordingly on weekends and holidays)
- Whether today is itself a major data/event day (FOMC decision, CPI/PCE print, NFP Friday,
  major earnings). If so, that's almost certainly the lead story — structure the brief around it
  rather than burying it under generic categories.

A quick `web_search` for "<today's date> economic calendar" or "what's on the calendar today
markets" is the fastest way to find this.

---

## Step 2: Gather macro data

These four categories are the reference set — pull from them, but don't feel obligated to fill
every row every time. Surface what's genuinely notable; skip what's stale.

### Rates & Liquidity (most important — leads the brief most days)
| Data point | How to get it | Why it matters |
|---|---|---|
| Fed funds rate + dot plot | web_search "Fed funds rate FOMC dot plot" | Sets the policy anchor; dot plot shows forward path |
| 10Y Treasury yield ($TNX) | IBKR `get_price_snapshot` if connected (search_contracts for TNX/TLT/IEF as proxy), else web_search | Benchmark long rate; moves growth & duration assets |
| Real rate (10Y − breakeven inflation / TIPS spread) | web_search "10 year TIPS breakeven inflation rate" | The rate that actually matters for valuations and gold |
| Fed balance sheet size (QT/QE pace) | web_search "Fed balance sheet size this week" (H.4.1 release) | Liquidity backdrop; QT pace affects reserves and risk appetite |

### Inflation
| Data point | How to get it | Why it matters |
|---|---|---|
| Core PCE | web_search "core PCE inflation latest" | The Fed's actual preferred gauge, not CPI |
| CPI / Core CPI | web_search "CPI report latest" | Leads PCE by a few weeks; market-moving on release day |
| PPI | web_search "PPI report latest" | Leading indicator for CPI/PCE |
| Michigan inflation expectations | web_search "University of Michigan inflation expectations" | Gauges whether expectations are anchored or drifting |

### Economic Cycle
| Data point | How to get it | Why it matters |
|---|---|---|
| Non-farm payrolls (NFP) | web_search "non-farm payrolls latest report" | Labor market health; first Friday of the month |
| ISM Manufacturing & Services PMI | web_search "ISM manufacturing PMI latest" / "ISM services PMI latest" | Forward-looking growth signal, above/below 50 |
| GDP & GDPNow | web_search "Atlanta Fed GDPNow latest estimate" | Real-time GDP tracking between official prints |
| Unemployment rate & initial claims | web_search "initial jobless claims this week" | Weekly claims are the freshest labor signal available |

### Sentiment & Structure
| Data point | How to get it | Why it matters |
|---|---|---|
| VIX | IBKR `get_price_snapshot` (search_contracts "VIX") if connected, else web_search | Baseline fear gauge |
| SPX options skew / put-call ratio | web_search "SPX put call skew" or "CBOE SKEW index" | Tail-risk pricing; complements VIX |
| AAII bull/bear sentiment | web_search "AAII investor sentiment survey latest" | Weekly retail sentiment, released Thursdays |
| DXY (Dollar Index) | IBKR `get_price_snapshot` (search_contracts "DXY" or UUP as proxy) if connected, else web_search | Cross-asset signal; strong dollar = tightening financial conditions globally |

If the Interactive Brokers connector is available, prefer it for anything that's a live tradeable
level (VIX, yields via bond ETF proxies, DXY via UUP, SPX) since it gives an exact real-time
print. Economic releases (CPI, NFP, PMI, GDPNow, AAII) aren't tradeable instruments — those
always come from `web_search`.

---

## Step 3: Gather today's market-moving news

Run 2-4 searches for what actually happened, e.g. "stock market news today", "Fed news today",
"<today's date> markets". Prioritize the last 24 hours and original financial outlets (Reuters,
Bloomberg, WSJ, AP) over aggregators. Keep this to the 3-5 things that actually moved price or
will move price tomorrow — not a general news roundup. Follow standard copyright practice:
paraphrase everything in your own words, one short quote (under 15 words) per source maximum.

---

## Step 4: Notable commentary on X

There's no live X/Twitter firehose connector available by default — check the registry once
(`search_mcp_registry`) in case one has since been connected; if not, use `web_search` per
account (e.g. "Nick Timiraos Fed" or "Lisa Abramowicz bonds" + today's date) to surface their
most recent relevant posts. Always paraphrase rather than quote verbatim, and don't quote any
single post over 15 words.

Starting roster (extend or trim as relevant — these aren't the only voices worth including, and
not all of them will have said something notable on a given day):

| Account | Who they are | Why they're worth checking |
|---|---|---|
| @nicktimiraos | WSJ Fed reporter | Most reliable first read on Fed policy signaling |
| @lisaabramowicz1 | Bloomberg | Sharp on bonds, macro, and real rates |
| @federalreserve | Federal Reserve (official) | Primary-source statements, no interpretation layer |
| @zerohedge | Aggregator | Fast, but noisy and prone to sensational framing — only include if a claim is corroborated elsewhere, and say so |

Feel free to pull in others when they're the most relevant voice for that day's story — a Fed
governor who just spoke, an economist who called the print, etc. The goal is informed
commentary that adds context the raw numbers don't, not volume of quotes.

---

## Step 5: Synthesize into the brief

Write the output as a chat response (this is a "read once this morning" digest, not an archival
document — don't create a file/artifact for it unless the user specifically asks to save or
log it). Use this structure:

```
## Market Brief — [Day, Month Date, Year]

**TL;DR:** [1-3 sentences — the single most important thing happening today]

### Rates & Liquidity
- [2-4 bullets, each a number + a so-what]

### Inflation
- [bullets, or "No new prints since X — no change to the picture"]

### Growth & Labor
- [bullets]

### Sentiment & Structure
- [bullets]

### Today's News
- [3-5 bullets, most market-relevant first, sourced]

### Notable Voices
- **@handle**: [paraphrased point, 1 sentence]

### What to Watch
- [next 1-3 catalysts: data releases, Fed speakers, earnings]
```

Keep the whole thing skimmable in under a couple of minutes — a busy reader should be able to
get the gist from the TL;DR and bullet headers alone, with detail available for anyone who wants
to read further.

---

## Edge Cases

- **Weekend/holiday**: note markets are closed, optionally give a lighter weekend-read version
  (weekly recap + what's on the calendar for the next session) rather than forcing a full brief.
- **Missing data**: if a number genuinely can't be found, write "data not available" rather than
  estimating or carrying over a stale figure silently.
- **Conflicting numbers across sources**: flag the discrepancy briefly rather than picking one
  arbitrarily.
- **Big single-event day** (FOMC, CPI, NFP): restructure the brief so that event leads the TL;DR
  and gets its own expanded section, rather than being one bullet buried in a category.
- **A theme here has an obvious equity angle** (e.g. rate-cut odds shifting in favor of
  utilities/real estate, a geopolitical event re-rating energy names): flag it explicitly and
  mention that `sector-rotation-stock-hunter` can screen that sector for specific candidates if
  the user wants to follow up — don't screen for tickers within this skill itself.
