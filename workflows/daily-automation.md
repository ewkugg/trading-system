# Workflow: Daily Automation (the self-running loop)

**Goal:** the system runs every trading day without being asked, closes its own loop, and
the human only makes the actual trade decisions. Three scheduled routines drive it, each
launching a fresh Claude session in this repo's cloud environment (which has web search +
read-only IBKR):

| Routine | Schedule (UTC) | Runs | Delivers |
|---|---|---|---|
| **Pre-market** | 12:30 Mon–Fri (~08:30 ET) | `workflows/pre-market-routine.md` steps 0–4 (regime → heat → brief → hunt → gate) | Regime verdict, heat budget, and any candidates that passed Layer 0 — as a message to review before the open |
| **After-close** | 20:45 Mon–Fri (~16:45 ET) | `workflows/after-close-review.md` | Postmortems for the day's closes, open-thesis invalidation checks; journal notes committed to `journal/` |
| **Weekly review** | 21:30 Fri | `workflows/weekly-review.md` | Aggregates, regime attribution, falsifiable candidate rules; provisional-rule re-checks |

Adjust times for DST/holidays as needed (cron is UTC; ET shifts an hour in winter).

## Human decision gates (unchanged)

Automation prepares; it never trades. The scheduled runs stop exactly where a decision is
needed:
- Pre-market delivers *candidates + sizing math*; entering a position is the user's action.
- If the user takes a trade, they say so (or it appears in IBKR fills) and Mode 1 opens the
  thesis note.
- The weekly review *proposes* rule promotions; editing `references/trading-constants.md`
  for a non-provisional rule should be confirmed by the user.

## State: the `journal/` folder

Scheduled cloud runs read/write `journal/` in this repo (see the repo-fallback note in
`trade-journal-postmortem`) and commit + push after writing. That folder **is** the
system's memory across runs — regime verdicts recorded in theses, open heat, closed-trade
history for back-checks. Keep it in git; sync Obsidian from it if desired.

## Failure behavior

- Market holiday / weekend fire: note it and exit — no forced brief.
- IBKR unreachable: run everything except fill-dependent steps; flag what was skipped.
- A run must never leave uncommitted journal changes — commit even partial output.
