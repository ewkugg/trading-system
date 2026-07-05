# CLAUDE.md — Trading System

Project guidance for Claude Code. This repo is the **single source of truth** for a personal
trading-skill system. It is a research, analysis, and journaling assistant — **not** an automated
trading system. It never places, modifies, or cancels orders. Human decision gates stay central.

## Source-of-truth rules

1. **`references/trading-constants.md` is canonical.** All risk/reward gates, the 1–2% per-trade
   cap, the portfolio-heat ceiling, VIX/RSI thresholds, and the catalyst window live there. If any
   number in a SKILL.md disagrees, the constants file wins — fix the SKILL.md to point at it.
2. **`references/news-sources.md`** is the canonical feed list for the two digest skills.
3. **`skills/` holds the master copies.** `dist/*.skill` are build artifacts — never hand-edit them;
   regenerate with `python3 scripts/build_dist.py`.
4. **Workflows** (`workflows/*.md`) are the canonical multi-skill routines.

## The system (five layers + meta)

```
REGIME → INTEL → DISCOVERY → DECISION → MEMORY   (+ navigator & constants as the meta layer)
```
- **Regime:** `market-regime` (breadth / distribution days / FTD → GREEN/CAUTION/RISK-OFF
  verdict, which scales the portfolio-heat ceiling for everything downstream)
- **Intel:** `daily-market-brief`, `ai-tech-pulse`
- **Discovery:** `sector-rotation-stock-hunter`
- **Decision:** `swing-trade-analysis`, `crypto-swing-analysis`
- **Memory:** `trade-journal-postmortem`
- **Meta:** `trading-navigator` (router), `references/` (constants + sources)

Data flows down; lessons flow back up via the weekly review promoting durable rules into the
constants file — only through the **rule-promotion standard** defined there (falsifiable,
recurring in ≥3 trades, back-checked against the closed-trade log).

## State & automation

- **Journal:** local runs write to the Obsidian vault; scheduled/cloud runs use the repo's
  `journal/` folder and must commit + push it (see `workflows/daily-automation.md`).
- **Daily loop:** three scheduled routines (pre-market, after-close, weekly review) keep the
  system running on its own; they prepare and journal but never trade — human gates stay.

## Safety

- `trade-journal-postmortem` is **read-only** on the broker — it reads fills/positions to compare
  plan vs. actual, and writes only to the Obsidian vault (or the repo's `journal/` folder in
  cloud runs). No order actions, ever.
- Nothing in this repo should be framed as financial advice; outputs are analysis the user acts on.

## Local setup the user must complete (machine-specific, not in the repo)

1. **Obsidian vault path** — set `<OBSIDIAN_VAULT_PATH>` and `<JOURNAL_SUBFOLDER>` in
   `skills/trade-journal-postmortem/SKILL.md` to point at the real vault.
2. **IBKR read-only access** — wire up fills/positions (IBKR MCP, Flex query, or CSV fallback).
3. **Data layer (optional)** — stay on web_search, or add a paid API (FMP/Finviz/Alpaca) for
   precise OHLCV/screening. Skills work either way.

## Conventions

- SKILL.md descriptions are intentionally a little "pushy" to combat under-triggering.
- Keep each SKILL.md focused; shared logic goes in `references/`, not copied across skills.
- After editing any skill or the constants file, run `python3 scripts/build_dist.py` to refresh
  the `.skill` artifacts for web-app/mobile use.
