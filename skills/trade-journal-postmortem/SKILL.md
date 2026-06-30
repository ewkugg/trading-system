---
name: trade-journal-postmortem
description: >
  Close the loop on every trade — record the thesis at entry, then compare plan vs. actual at
  exit and write a structured postmortem into the Obsidian journal. Use this skill whenever the
  user takes a trade, closes a trade, or wants to review past trades: "log this trade",
  "journal my NVDA entry", "I just closed BMNR", "postmortem on that trade", "did I follow my
  plan", "review my closed trades this week/month", "记录这笔交易", "复盘". Reads the local Obsidian
  vault and (read-only) IBKR fills; never places or modifies orders. Always offer to log a thesis
  whenever swing-trade-analysis or crypto-swing-analysis produces an actionable entry — a trade
  that isn't journaled can't be learned from.
---

# Trade Journal & Postmortem Skill

The memory layer of the system. The analysis skills decide *whether and where* to enter;
this skill records what was planned, what actually happened, and what to do differently —
turning a stream of one-off trades into a feedback loop that compounds.

> **Canonical constants.** Process-adherence checks (R/R gate, 1–2% cap, portfolio-heat ceiling,
> "never hold through earnings") are defined in
> [`references/trading-constants.md`](../../references/trading-constants.md). Score adherence
> against that file, not against numbers re-typed here.

---

## Local configuration (set these once on your machine)

This skill needs two local connections. Fill these in and Claude Code resolves them at runtime:

| Setting | Placeholder | What it is |
|---|---|---|
| Obsidian vault path | `<OBSIDIAN_VAULT_PATH>` | Absolute path to your vault (e.g. `~/Obsidian/Trading`) |
| Journal folder | `<JOURNAL_SUBFOLDER>` | Where trade notes go (e.g. `Trades/`) |
| IBKR access | `<IBKR_READONLY>` | Read-only fills/positions (IBKR MCP, Flex query export, or pasted CSV fallback) |

If IBKR isn't connected yet, fall back to asking the user for fill price/date or a pasted CSV.
**This skill is read-only on the broker — it never sends, modifies, or cancels orders.**

---

## Three modes

### Mode 1 — Open a thesis (at entry)
Triggered when a trade is taken (often right after an analysis skill passes Layer 0).
Capture the *plan* while it's honest — before outcome bias sets in:
- Ticker/coin, date, direction
- Entry zone, stop, target, **R/R ratio**, planned position size & % portfolio risk
- The checklist snapshot: which layers were green, the catalyst and its date
- One-sentence thesis and the explicit **invalidation** ("thesis is wrong if ___")

Write it as a new journal note (schema below) with `status: open`.

### Mode 2 — Close + postmortem (at exit)
Triggered when a position is closed. Pull the actual fills (IBKR read-only or user-provided), then:
1. **Plan vs. actual:** planned entry/stop/target vs. real fills; realized **R-multiple** = (exit − entry) ÷ (entry − planned stop).
2. **MAE / MFE:** worst and best excursion while open — did you get shaken out near the lows, or leave a runner?
3. **Process adherence** (score against `trading-constants.md`, *separate from P&L*):
   - Did Layer 0 actually pass before entry, or was the gate skipped?
   - Was risk within the 1–2% cap and total heat under the ceiling?
   - Was the stop respected, or moved/widened in the moment?
   - Held through earnings against the rule?
   - **A winning trade that broke the rules is a process loss; a losing trade that followed them is a process win.** Score both axes.
4. **One concrete lesson** and, if it recurs, a candidate rule for next session.

Update the note to `status: closed` with the postmortem section filled in.

### Mode 3 — Periodic review (weekly / monthly)
Triggered by "review my trades" or via `workflows/weekly-review.md`. Read all closed notes in
the window and aggregate:
- Win rate, average win R, average loss R, **expected value per trade** (see constants).
- Process-adherence rate (how often rules were followed) vs. outcome — the relationship matters
  more than either number alone.
- Recurring patterns (e.g. "chasing RSI > 70 entries," "cutting winners early").
- Output **next-session operating rules** — and if a rule proves durable, propose adding it to
  `references/trading-constants.md` so the whole system inherits it.

---

## Journal note schema (Obsidian markdown)

Write one note per trade as `<JOURNAL_SUBFOLDER>/<TICKER>-<YYYY-MM-DD>.md`:

```markdown
---
ticker: NVDA
direction: long
status: open            # open | closed
opened: 2026-06-23
closed:
planned_entry: 190
planned_stop: 178
planned_target: 220
planned_rr: 2.5
risk_pct: 1.5
catalyst: earnings 2026-07-15
tags: [swing, semis]
---

## Thesis
[one or two sentences]

**Invalidation:** [the specific condition that means the thesis is wrong]

## Checklist snapshot (at entry)
| Layer | Status | Key data |
|---|---|---|
| R/R gate | PASS | 2.5:1 |
| Macro | ✅ | VIX 16, QQQ above 20MA |
| Catalyst | ✅ | earnings in ~3w |
| Technical | ⚠️ | RSI 63, above 50MA |
| Sentiment | ✅ | 72% buy, cooling |

## Postmortem (filled at close)
- Actual entry / exit: __ / __
- Realized R: __        MAE: __   MFE: __
- Process adherence: gate ✅ · size ✅ · stop respected ✅ · earnings rule ✅
- Outcome vs. process: [win/loss] on P&L, [win/loss] on process
- **Lesson:** [one concrete thing]
- Candidate rule: [if it recurs]
```

---

## Output format (in chat)

Lead with the verdict, keep it short:

```
## [TICKER] Postmortem — [date]
Planned: entry $X / stop $X / target $X (R/R X.X:1)
Actual:  entry $X / exit $X → realized X.XR   (MAE -X.XR, MFE +X.XR)
Process: gate ✅ · size ✅ · stop ✅ · earnings ✅   → process WIN
Outcome: +/− X.XR on P&L
Lesson:  [one sentence]
Journaled to: <vault path>/<file>.md
```

---

## Principles

- **Log the plan before the outcome.** A thesis recorded after you know the result is worthless.
- **Score process and P&L separately.** Good process + bad luck is repeatable; bad process + good luck is not.
- **The journal is the only thing that compounds across trades.** Every closed trade either teaches a rule or confirms one.
- **Read-only on the broker, always.** This skill observes and records; it never trades.
