# The World Today — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rifki500/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/rifki500/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120)

A make.fun entry for **news-image-20261120**: one image summing up the
world's news of Friday, 20 November 2026. Entered on
[make.fun](https://make.fun/bounty/news-image-20261120).

The image is a newspaper front page drawn entirely in code
(`build_image.py`, PIL): a masthead naming the day, a lead story on
Russia's strikes on Kyiv's bridges, and six more stories — Asia's market
plunge, Saudi Arabia shooting down a Houthi missile, GTA 6's record first
day, the UK–EU reset deal, the US nationwide ground stop, and COP31 ending
in deadlock. Every story happened, or was first reported, on 20 November
2026. See `BUILD-LOG.md` for the story list, sources and verification.

## How it runs

`main.py` (standard library only) copies the pre-built `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). It runs with
no network and writes byte-identical output on every run.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint (stdlib only)
- `entry.png` — the 1024×1024 front page (under 1 MiB)
- `build_image.py` — the generator that drew `entry.png` (PIL)
- `BUILD-LOG.md` — stories, sources, verification results
- `LICENSE` — MIT
