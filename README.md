# Trading System

A personal trading-skill system, organized as **one source of truth**. The stateful core
(journal, postmortem, navigator, shared constants) lives here in Claude Code with local file +
broker access; the lightweight analysis skills are regenerated as `.skill` files for quick checks
in the Claude web app / mobile. Obsidian Sync is the bridge — your vault follows you across
devices, and Claude Code reads it at your desk.

> Research, analysis, and journaling assistant — **not** an automated trading system. It never
> places orders. It is not financial advice.

## Layout

```
trading-system/
├── CLAUDE.md                     project guidance for Claude Code
├── references/
│   ├── trading-constants.md      ← canonical: R/R gate, 1–2% cap, portfolio heat, VIX/RSI
│   └── news-sources.md           ← canonical: curated feeds for the digests
├── journal/                      trade notes for scheduled/cloud runs (the system's memory)
├── skills/
│   ├── market-regime/               ← breadth/distribution/FTD → GREEN/CAUTION/RISK-OFF gate
│   ├── swing-trade-analysis/        ┐
│   ├── crypto-swing-analysis/       │  master copies of your 5 existing skills
│   ├── sector-rotation-stock-hunter/│  (now pointing at the constants file)
│   ├── daily-market-brief/          │
│   ├── ai-tech-pulse/               ┘
│   ├── trade-journal-postmortem/    ← NEW: reads Obsidian + IBKR fills, writes postmortems
│   └── trading-navigator/           ← NEW: router + system map
├── workflows/
│   ├── pre-market-routine.md     regime → heat → brief → hunter → analysis → size → journal
│   ├── after-close-review.md     pull fills → postmortem each close
│   ├── weekly-review.md          aggregate → regime attribution → falsifiable rules
│   └── daily-automation.md       the self-running loop: 3 scheduled routines + journal/ state
└── scripts/
    └── build_dist.py             regenerate dist/*.skill from skills/ (constants inlined)
```

## Finish setup (3 local steps)

These are machine-specific, so they're left as placeholders for you to fill in Claude Code:

1. **Point at your Obsidian vault.** In `skills/trade-journal-postmortem/SKILL.md`, set
   `<OBSIDIAN_VAULT_PATH>` and `<JOURNAL_SUBFOLDER>`.
2. **Connect IBKR (read-only).** Wire fills/positions via IBKR MCP, a Flex query export, or the
   pasted-CSV fallback. The journal only ever *reads* the broker.
3. **Choose your data layer.** Stay on web_search (free, works anywhere) or add a paid API
   (FMP / Finviz / Alpaca) for precise data and screening. Everything runs either way.

## Install the skills in Claude Code

Copy each folder under `skills/` into your Claude Code skills directory (or keep this repo as your
project and let Claude Code discover them). Restart/reload so they register.

## Regenerate web-app / mobile copies

After any edit to a skill or to `references/trading-constants.md`:

```bash
python3 scripts/build_dist.py
```

This copies the shared references into each skill so the packaged version is self-contained, then
writes `dist/<skill>.skill`. Upload those in the web app under **Settings → Skills**. Never edit
the `dist/` files by hand — they're rebuilt from `skills/`.

## Suggested build order (from here)

1. ✅ Repo + constants file (drift fixed — done in this scaffold)
2. `trading-navigator` (front door) — included; refine triggers to taste
3. `trade-journal-postmortem` — included; wire to your vault + IBKR (the main local step)
4. Workflows — included; adjust gates once the skills they chain feel settled

## Still open

- **News source (item 4):** currently delivered as the shared `references/news-sources.md` that
  both digests read. If you'd rather have a *dedicated* news-sourcing skill instead of a shared
  reference, that's a small addition — decide once you've used the shared file for a bit.
- **crypto-swing-analysis** is the reconstructed copy — diff it against your authoritative download
  if you kept one.
