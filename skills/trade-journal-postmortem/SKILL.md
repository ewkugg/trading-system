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

**Repo fallback (used by scheduled/cloud runs):** if `<OBSIDIAN_VAULT_PATH>` is unset or
unreachable — e.g. this skill is running in a cloud session as part of the daily automation
loop (`workflows/daily-automation.md`) — read and write journal notes in the repo's own
`journal/` folder instead, and **commit + push** any notes created or updated so the journal
survives the session. The repo is then the sync bridge: point Obsidian at a clone of it (or
copy notes over) and both environments see the same journal. Same schema either way.

If IBKR isn't connected yet, fall back to asking the user for fill price/date or a pasted CSV.
**This skill is read-only on the broker — it never sends, modifies, or cancels orders.**

---

## The modes — Heat Check + Modes 1–3

### Heat Check — portfolio heat & exposure (before any new entry)
*(Named, not numbered — "Layer 0" is the analysis skills' R/R gate; this is a different thing.)*
Triggered by "how much heat am I carrying", "can I add another position", or automatically
as the sizing step of the pre-market routine. This makes the heat ceiling self-enforcing
instead of manual math:
1. Scan `<JOURNAL_SUBFOLDER>` for all notes with `status: open` and sum their `risk_pct` —
   **total, and grouped by theme** (the note's primary tag).
2. Get the ceiling in effect: the regime-scaled ceiling from today's `market-regime`
   verdict (see the regime-scaled heat table in `trading-constants.md`), then apply the
   **drawdown circuit breaker** on top — the effective ceiling is whichever is lower.
   If no regime verdict exists in this session, run `market-regime` first — don't fall
   back to the flat 6%.
3. Report three things: current total heat vs. ceiling, **heat by theme vs. the
   correlated-exposure cap** (half the ceiling per theme — see constants), and the
   **remaining risk budget** for a new trade. If a proposed trade's risk would exceed
   either cap, state the max `risk_pct` that fits (or "no new positions" in RISK-OFF).
   A candidate in an already-capped theme is a skip or a swap, not an add.
4. Cross-check against reality when IBKR is connected: if broker positions exist that have
   no open journal note (or vice versa), flag the mismatch — the journal is only a valid
   heat ledger if it matches the account.
5. **Output the open-position list** (ticker, theme, risk_pct) so downstream skills in the
   same session can see it — the hunter uses it to flag candidates that duplicate existing
   exposure.

### Mode 1 — Open a thesis (at entry)
Triggered when a trade is taken (often right after an analysis skill passes Layer 0).
Capture the *plan* while it's honest — before outcome bias sets in:
- Ticker/coin, date, direction
- Entry zone, stop, target, **R/R ratio**, planned position size & % portfolio risk
- The **exit plan**, chosen now per the trade-management rules in `trading-constants.md`:
  breakeven at +1R, then *either* partial at +2R *or* MA-trail (pick one → `exit_plan:`),
  plus the time-stop date
- The checklist snapshot: which layers were green, the catalyst and its date
- Today's `market-regime` verdict (`regime_at_entry`) and a Heat Check confirming the
  trade fits both the regime-scaled ceiling and the theme cap
- One-sentence thesis and the explicit **invalidation** ("thesis is wrong if ___")

Write it as a new journal note (schema below) with `status: open`.

### Mode 2 — Close + postmortem (at exit)
Triggered when a position is closed. Pull the actual fills (IBKR read-only or user-provided), then:
1. **Plan vs. actual:** planned entry/stop/target vs. real fills; realized **R-multiple** = (exit − entry) ÷ (entry − planned stop).
2. **MAE / MFE — computed, not recalled:** pull the holding period's low and high from IBKR
   (`get_price_history` between the open and close dates; daily bars are fine). MAE =
   (period low − entry) ÷ (entry − planned stop); MFE = (period high − entry) ÷ (entry −
   planned stop). Memory cannot reconstruct these — if IBKR is unavailable, record "n/a"
   rather than a guess. Was the exit shaken out near the period low? Did the trade see
   +2R and give it back (exit plan not followed)?
3. **Exit-plan adherence:** was the `exit_plan` chosen at entry actually executed —
   breakeven move at +1R, the chosen partial/trail at +2R, the time stop honored?
   Deviations score as process losses even when they made money.
4. **Process adherence** (score against `trading-constants.md`, *separate from P&L*):
   - Did Layer 0 actually pass before entry, or was the gate skipped?
   - Was risk within the 1–2% cap and total heat under the ceiling?
   - Was the stop respected, or moved/widened in the moment?
   - Held through earnings against the rule?
   - **A winning trade that broke the rules is a process loss; a losing trade that followed them is a process win.** Score both axes.
5. **Month-to-date drawdown update:** add this trade's realized P&L to the running
   month-to-date figure and check it against the **drawdown circuit breaker** in
   `trading-constants.md` — if a throttle level is crossed, state the reduced caps
   explicitly (they apply from the next session).
6. **One concrete lesson** and, if it recurs, a candidate rule for next session.

Update the note to `status: closed` with the postmortem section filled in.

### Mode 3 — Periodic review (weekly / monthly)
Triggered by "review my trades" or via `workflows/weekly-review.md`. Read all closed notes in
the window and aggregate:
- Win rate, average win R, average loss R, **expected value per trade** (see constants —
  and net of friction, per the EV section there).
- **Current drawdown-throttle status** (month-to-date realized P&L vs. the circuit-breaker
  levels) — state it even when it's "no throttle."
- Process-adherence rate (how often rules were followed) vs. outcome — the relationship matters
  more than either number alone.
- Recurring patterns (e.g. "chasing RSI > 70 entries," "cutting winners early").
- **Regime attribution:** group closed trades by the market-regime verdict recorded at
  entry — did trades opened in CAUTION/RISK-OFF underperform GREEN-regime trades? This is
  the check that validates (or indicts) the regime gate itself.
- Output **next-session operating rules**. Every candidate rule must be stated
  **falsifiably**, with its own invalidation — same discipline as a trade thesis:
  > "Rule: no entries with RSI > 70. **This rule is wrong if** trades it would have
  > blocked show avg realized R ≥ the trades it allowed, over the next 20 trades."
- **Promotion gate:** a rule is proposed for `references/trading-constants.md` only if it
  passes the **rule-promotion standard** defined there (falsifiable + recurring in ≥ 3
  trades + back-checked against the closed-trade log once ≥ 20 trades exist; below that,
  promote as `provisional:`). The back-check is mechanical: replay the closed-trade log,
  ask "what would avg R have been if this rule had been enforced," and compare. Re-check
  all `provisional:` rules each week as the sample grows; demote ones that fail.

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
regime_at_entry: GREEN    # market-regime verdict the day the thesis opened
exit_plan: partial-at-2R  # partial-at-2R | ma-trail — chosen at entry, per constants
time_stop: 2026-07-08     # exit by this date if no +1R progress
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
