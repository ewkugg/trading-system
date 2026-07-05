# Workflow: Weekly Review

**When:** end of week.
**Goal:** turn the week's individual notes into patterns and next-week rules.

| # | Step | Skill | Output |
|---|---|---|---|
| 1 | Aggregate closed trades | `trade-journal-postmortem` (Mode 3) | Win rate, avg win R, avg loss R, expected value per trade. |
| 2 | Process vs. outcome | `trade-journal-postmortem` | Adherence rate this week, and how it tracked against P&L. |
| 3 | Find recurring patterns | `trade-journal-postmortem` | e.g. chasing RSI>70, cutting winners early, skipping the gate. Include **regime attribution**: how did CAUTION/RISK-OFF entries do vs. GREEN? |
| 4 | Write next-week rules | `trade-journal-postmortem` | Every rule stated **falsifiably** ("wrong if ___"). Promote into `references/trading-constants.md` only via the **rule-promotion standard** there (recurring ≥3 trades + back-checked against the closed-trade log once ≥20 trades exist; `provisional:` below that). |
| 5 | Re-check provisional rules | `trade-journal-postmortem` | Replay the closed-trade log against each `provisional:` rule in the constants file; demote any that fail the back-check. Apply the **statistical-honesty bar** (constants): <50 trades → only large effects (≥0.3R) count; regime buckets need ≥10 trades each. |
| 6 | Drawdown-throttle status | `trade-journal-postmortem` | Report month-to-date realized P&L vs. the **circuit-breaker** levels and any caps in effect for next week. |

**Artifacts:** a weekly summary note + any constants-file updates.

**This is where the loop pays off:** the system gets smarter only if durable lessons flow back
into the shared constants.
