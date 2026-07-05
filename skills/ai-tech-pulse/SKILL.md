---
name: ai-tech-pulse
description: >
  Use this skill whenever the user wants a daily AI/tech pulse, an update on what's happening
  in AI and tech, or a roundup of interesting takes from tech/AI accounts on X. Triggers
  include: "what's new in AI today", "ai tech brief", "give me today's AI pulse", "今天AI圈有什么新闻",
  "AI科技简报", "今天科技圈怎么样", "any interesting stock ideas from twitter", "what are people saying
  about AI on X", or any request combining frontier model releases, AI/chip infrastructure news,
  research breakthroughs, and policy with speculative stock-idea threads from geeky/anon X
  accounts. This is distinct from daily-market-brief (which is macro/Fed-focused) and from
  sector-rotation-stock-hunter (which is a technical entry-timing screener) — this skill is
  about sourcing what's genuinely new and what sharp, unconventional voices are thinking about,
  not trading signals. Use it even if the user only asks generically for "AI news" or "what's
  going on in tech" — gather a well-rounded pulse by default rather than waiting for specifics.
---

> **Canonical constants.** Risk/reward gates, the 1–2% per-trade cap, the portfolio-heat
> ceiling, VIX/RSI thresholds, and the catalyst window are defined once in
> [`references/trading-constants.md`](../../references/trading-constants.md). Use those values;
> if a number here ever disagrees with that file, the constants file wins.

> **News sources.** Curated, prioritized feeds live in
> [`references/news-sources.md`](../../references/news-sources.md). Pull from there rather than
> hard-coding sources in this skill.


# AI & Tech Pulse

A daily pulse on two genuinely different things, kept in two genuinely separate sections:
**what's actually new** in AI/tech (verifiable: releases, research, infrastructure, policy), and
**what geeky voices are speculating about** (unverifiable: theses, narratives, stock ideas).
Blending these two is how a digest quietly turns a hot take into a fact. Keep them apart.

---

## Core Philosophy

- **News is reported; takes are sourced.** A model release or a regulatory filing happened —
  report it as fact. A thesis about why $TICKER will 10x did not happen, it was *said* by
  someone — report it as "X argues / X is betting that," never as settled fact.
- **Signal over influencer noise.** The web is full of "AI is changing everything 🚀" accounts
  that mostly repackage press releases for engagement. Prefer people who actually build, train,
  or do primary research and analysis — the kind of account that's right often enough to be worth
  the read even when the writing is dry or anonymous.
- **Geeky means technical and a little unfiltered**, not mainstream-polished. An anonymous poster
  with a sharp, idiosyncratic thesis across 30 tickers is more valuable here than a verified
  account with a generic "AI stocks to watch" listicle.
- **This is for literacy and idea-sourcing, not execution.** If something in Section 2 is
  interesting enough to actually act on, that's what `sector-rotation-stock-hunter` is for —
  this skill surfaces candidates, it doesn't screen or size them.

---

## Step 1: Orient

Use today's actual date in every search — don't rely on memory for "latest." Check quickly
whether there's a dominant story today (a major model launch, an export-control change, a big
funding round) — if so, that leads both sections rather than being one bullet buried in a list.

---

## Section 1: What's Actually New (AI/Tech News & Research)

Run searches across these categories — skip any category with nothing genuinely new today
rather than padding it:

| Category | What it covers | Search starting points |
|---|---|---|
| Frontier models | New model releases, benchmark results, capability jumps | web_search "AI model release this week", "[lab name] new model" |
| Infrastructure & hardware | Chips, datacenters, power, supply chain | web_search "AI datacenter news today", "semiconductor AI news today" |
| Research | Notable papers, breakthroughs, technique shifts | web_search "AI research breakthrough this week" |
| Policy & regulation | Export controls, AI regulation, antitrust | web_search "AI policy news today", "AI export controls today" |
| Business | Funding rounds, M&A, major partnerships | web_search "AI funding news today" |

Official lab/company accounts are useful as primary sources for releases — search by name
since there's no live feed (e.g. "Anthropic announcement today", "OpenAI announcement today",
"Google DeepMind research today"). For technical color and the reaction beyond the press
release, pull from researcher/builder voices — a starting roster, not an exhaustive one:

| Account | Why they're worth it |
|---|---|
| @karpathy (Andrej Karpathy) | Clearest technical writer on LLMs/training; now at Anthropic |
| @fchollet (François Chollet) | ARC-AGI creator; the sharpest skeptic of "it's just scaling" narratives — good counter-programming |
| @JeffDean (Jeff Dean) | Google Chief Scientist; infrastructure and distributed systems, the "metal" under the models |
| @demishassabis (Demis Hassabis) | DeepMind CEO; AI-for-science angle (AlphaFold etc.), not just LLMs |
| @dylan522p (Dylan Patel, SemiAnalysis) | The most-cited independent voice on AI infrastructure/chip supply chains; technical and unsparing about hype |

Pull in whoever is actually the source of that day's story (a lab researcher who just posted
about their own release, a Fed-of-AI-policy figure during a hearing, etc.) even if they're not
on this list — the roster is a baseline, not a ceiling.

### Section 1 output format
```
### What's New in AI/Tech — [Date]

**Frontier Models**
- [bullet: what happened, who, why it matters]

**Infrastructure & Hardware**
- [bullet]

**Research**
- [bullet, or skip the heading entirely if nothing notable]

**Policy**
- [bullet]

**Business**
- [bullet]
```

---

## Section 2: Geeky Voices & Stock Ideas (X)

This section is explicitly speculative and should read that way. The value isn't "these are good
trades" — it's "here's how a sharp, slightly unhinged person is currently thinking about the
sector," which is useful even when (especially when) you disagree with the conclusion.

**This section is a handoff feed, not a screen.** Its job ends at *ticker + one-line
attribution* — who said it, what the claimed angle is. Do not evaluate, rank, or add
technical/fundamental color to the ideas here; that duplicates `sector-rotation-stock-hunter`,
which is where any name worth a second look goes next (and it will pull this list from the
session automatically). One skill discovers, one skill judges.

There's no live X firehose connector by default — check once whether one is connected in the
current environment; otherwise `web_search` per account (e.g. "[handle] stock thesis" or
just the handle + today's date) to surface recent posts.

Starting roster — extend freely, this category lives or dies on finding fresh idiosyncratic
voices, not on sticking to a fixed list:

| Account | Style |
|---|---|
| @aleabitoreddit ("Serenity") | Anon, sprawling multi-ticker thesis threads across AI/semis/space/robotics/crypto-infra — narrative-driven, not technical-chart-driven |
| @dylan522p | Half Section 1, half Section 2 — his hardware calls often double as stock theses (e.g. memory pricing, CoWoS capacity) |
| @zerohedge | Fast but noisy — only include a claim from here if corroborated elsewhere, and say so explicitly |

When summarizing a thesis-list post like Serenity's, don't reproduce the whole list — pull out
the 3-5 most interesting or contrarian picks rather than all 30, and always paraphrase the
reasoning rather than quoting it. Note explicitly that these are one person's speculative,
unvetted opinions.

### Section 2 output format
```
### Geeky Voices — [Date]

**@handle**: [one-line paraphrase of their overall framing/mood today]
- $TICKER — [paraphrased one-line claim — attribution only, no evaluation]
- $TICKER — [paraphrased one-line claim]

[Repeat per account with something notable to say today]

**Handoff feed for the hunter:** [$TICKER (@handle), $TICKER (@handle), ...]

⚠️ Speculative, unvetted, not a recommendation — anything worth a second look goes through
sector-rotation-stock-hunter for the actual technical/fundamental read; nothing here has one.
```

---

## Step 2: Present

Daily cadence, conversational response (not a saved file/artifact) unless the user asks to log
or archive it — this is a "read once" pulse like the market brief. Lead with whichever section
has the bigger story that day; don't mechanically run Section 1 before Section 2 if a stock-idea
thread is genuinely the more interesting thing that happened.

---

## Edge Cases

- **Quiet day**: say so plainly ("nothing major in research/infra today") rather than padding
  either section with stale or marginal items.
- **A thesis post turns out to be wrong/outdated by the time you check**: note that rather than
  silently passing along stale numbers.
- **Overlap with `sector-rotation-stock-hunter`**: if a name from Section 2 looks genuinely
  interesting, say so and offer to run it through that skill — don't duplicate its technical
  screening work here.
- **Overlap with `daily-market-brief`**: if the day's AI/tech story is *also* the macro story
  (e.g. a chip export-control change that moves the whole market), it's fine for both skills to
  cover it from their own angle — no need to suppress either.
