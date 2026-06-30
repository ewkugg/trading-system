# Workflow: After-Close Review

**When:** after the close, on a day you opened or closed positions.
**Goal:** keep the journal current while memory is fresh.

| # | Step | Skill | Note |
|---|---|---|---|
| 1 | Pull the day's fills | `trade-journal-postmortem` | IBKR read-only (or pasted CSV). |
| 2 | Postmortem each close | `trade-journal-postmortem` (Mode 2) | Plan vs. actual, realized R, MAE/MFE, process-adherence score. |
| 3 | Update open theses | `trade-journal-postmortem` | For still-open trades: is the invalidation still intact? Mark any that should be cut tomorrow. |

**Artifacts:** updated journal notes (`status: closed` with postmortems filled in).

**Principle:** score process and P&L separately — a winning trade that broke the rules is a
process loss.
