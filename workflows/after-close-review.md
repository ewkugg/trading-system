# Workflow: After-Close Review

**When:** after the close, on a day you opened or closed positions.
**Goal:** keep the journal current while memory is fresh.

| # | Step | Skill | Note |
|---|---|---|---|
| 1 | Pull the day's fills | `trade-journal-postmortem` | IBKR read-only (or pasted CSV). |
| 2 | Postmortem each close | `trade-journal-postmortem` (Mode 2) | Plan vs. actual, realized R, **MAE/MFE computed from IBKR price history** (period high/low over the holding window — never from memory), exit-plan adherence, process score. |
| 3 | Manage open trades | `trade-journal-postmortem` | For each open thesis, against the **trade-management rules** (constants): invalidation intact? +1R reached → breakeven stop due? +2R → the chosen `exit_plan` action due? `time_stop` date approaching? Crypto: resting stop confirmed at the exchange? Mark tomorrow's required actions. |
| 4 | Update drawdown status | `trade-journal-postmortem` | Add today's realized P&L to month-to-date; check the **drawdown circuit breaker** — if a throttle triggered, state tomorrow's reduced caps. |

**Artifacts:** updated journal notes (`status: closed` with postmortems filled in) and a
one-line "tomorrow's required actions" list (stop moves, partials, time-stop exits, throttle).

**Principle:** score process and P&L separately — a winning trade that broke the rules is a
process loss. The exit plan chosen at entry is part of the process score.
