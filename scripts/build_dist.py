#!/usr/bin/env python3
"""
build_dist.py — regenerate web-app .skill files from skills/ (single source of truth).

A .skill file is just a zip of a skill folder. For the web app, each skill must be
self-contained (separately-uploaded skills can't read sibling files at runtime), so this
script copies the shared references into each skill's own references/ folder before zipping.
Run after editing any skill or references/trading-constants.md.

Usage:
    python3 scripts/build_dist.py
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REFS = ROOT / "references"
DIST = ROOT / "dist"

# Which shared references each skill should carry in its packaged (web-app) copy.
SHARED = {
    "swing-trade-analysis":        ["trading-constants.md"],
    "crypto-swing-analysis":       ["trading-constants.md"],
    "sector-rotation-stock-hunter":["trading-constants.md"],
    "daily-market-brief":          ["trading-constants.md", "news-sources.md"],
    "ai-tech-pulse":               ["trading-constants.md", "news-sources.md"],
    "trade-journal-postmortem":    ["trading-constants.md"],
    "trading-navigator":           ["trading-constants.md"],
}


def build_one(skill_dir: Path) -> Path:
    name = skill_dir.name
    if not (skill_dir / "SKILL.md").exists():
        raise FileNotFoundError(f"{name}: no SKILL.md")

    # Stage a self-contained copy in a temp build dir.
    stage = DIST / "_stage" / name
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(skill_dir, stage)

    # Inline the shared references this skill depends on.
    for ref in SHARED.get(name, []):
        (stage / "references").mkdir(exist_ok=True)
        shutil.copy2(REFS / ref, stage / "references" / ref)

    # Zip the staged folder into dist/<name>.skill
    out = DIST / f"{name}.skill"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(stage.parent))  # arcname: <name>/...
    return out


def main():
    DIST.mkdir(exist_ok=True)
    built = []
    for skill_dir in sorted(d for d in SKILLS.iterdir() if d.is_dir()):
        built.append(build_one(skill_dir))
    # Clean up staging.
    stage_root = DIST / "_stage"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    print(f"Built {len(built)} skills into {DIST}/")
    for b in built:
        print(f"  - {b.name}")


if __name__ == "__main__":
    main()
