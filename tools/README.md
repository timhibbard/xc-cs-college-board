# tools/

The scripts that build the board. They lived in `/tmp/sweep/` until this directory
existed, which meant the data on the site was reproducible only until the next reboot
cleared the directory — nothing in the repo could regenerate `assets/data.js` or
`assets/detail.js`. That is what this is fixing.

Paths are derived from each script's own location, so everything runs from a clone
rather than from one machine's home directory. Intermediates go to `tools/.work/`,
which is gitignored: they are fetch caches, TFRRS result dumps and multi-megabyte
joins, not source.

## The trap, first, because it has cost more time here than anything else

**The stored `xc` aggregate carries no `vlast`.** Any ladder or "never finished seven"
computation has to recompute from the raw `XCRACES` times. Reading the stored aggregate
silently skips the 46 schools measured on their last finisher rather than a seventh man,
and returns plausible-looking zeros — it reported 87 runnable schools instead of the true
172. `ladder.py` does this correctly and prints the split it found (`172 (126 on a 7th
man, 46 on the last finisher)`); anything new should copy it rather than reinvent it.

## The second trap: a row with no aggregate is not necessarily unmeasured

`aggregate.py` will not average a championship race with fewer than five finishers, so a
school that turned up to its conference meet with two men gets no `xc` block at all — and
for a while those rows kept whatever tier they were seeded with, which was `verify`. On this
site *Verify* means **unmeasured**, and that is the wrong word for them: a conference or
regional championship is the race a program brings everyone to, so a field of two there is a
measurement of how thin the squad is rather than an absence of evidence. Five rows were
mislabelled that way — Carlow, Marymount, Hilbert, Greensboro College and William Peace, all
now `caution` / `tierSrc: 'hand'`.

**The level decides this, not the field size.** A *national* championship is the exception:
only individual qualifiers go, so Thomas Jefferson's single finisher there says nothing about
its roster and that row is correctly still `verify`. `ladder.py` prints every row in this
state and flags only the ones still at `verify` on a short *conference, area or regional*
field, which is the check that has to stay quiet. Do not lower the five-finisher floor to
make these rows measurable: `cmpable` filters races before they are averaged, so a lower
floor would also pull short championship races into healthy programs' aggregates and move
tiers across the whole board.

## Checks — these run today, with no fetching

| Script | What it does |
| --- | --- |
| `render-check.js` | Renders three metro pages and every school page with jsdom, and asserts row counts derived from `assets/data.js` plus the totals README.md publishes in prose. Needs `jsdom`: `npm install --no-save jsdom`, or point `NODE_PATH` at an install that has it. |
| `page-check.js` | Renders all 13 site pages, reporting uncaught JS errors, dead relative links and broken in-page anchors. This is what caught the `washington.html` failure, where a missing `id="k-lead"` threw and took the master table, the map and three off-board tables down with it. |
| `page-debug.js` | `node tools/page-debug.js washington.html` — runs one page's inline script against a stub DOM and prints what each element received. Faster than jsdom and it names the throwing line, so it is the right first stop when `page-check.js` reports a page. |
| `metro_digest.py` | `python3 tools/metro_digest.py washington` — the per-metro fact sheet. Everything a metro page's prose claims has to come from a row on that page, and this prints those rows with the aggregates a lede needs. Use it to check a page's numbers rather than counting by hand. |
| `ladder.py` | Runs the published tier ladder over every measured school and prints only the disagreements with the hand tiers, for a human to decide. Five today. Then it sweeps **every row that carries a tier, on the board or off it**, for championships too short to average, and flags any still sitting at `verify` on a short conference or regional field — the second trap above. Zero flags is the passing state. |
| `dump_board.js` | Flattens `assets/data.js` + `assets/detail.js` to `.work/board.json` so the Python tooling can read them. Run this after any data edit; the Python scripts read the dump, not the JS. |

## Pipeline order

```
edit assets/data.js
  → node tools/dump_board.js          # .work/board.json
  → python3 tools/metro_digest.py <metro>
  → python3 tools/gen_pages.py        # writes the metro pages
  → node tools/page-check.js          # all 13 pages render, no dead links
  → node tools/render-check.js        # row counts match the data and the prose
```

## Stages that need fetched input

These are the ones that built the board in the first place, and they need inputs not
vendored here — so they are kept for the record and for the next sweep, not because
they run from a clean clone.

| Script | Needs | Produces |
| --- | --- | --- |
| `stage1.py` | the College Scorecard institution CSV, downloaded by hand into `.work/` from <https://collegescorecard.ed.gov/data/> (~250MB unzipped) | `.work/candidates.json` — candidate schools with driving distance per metro centre, routed through OSRM (`router.project-osrm.org`) |
| `parse_xc.py` | a saved TFRRS results page as `argv[1]` | parsed finishers for one race |
| `aggregate.py` | `.work/byteam.json`, `.work/allslugs.json` | `.work/agg.json` — per-school championship aggregates and squad shape |
| `apply_aggs.py` | `.work/xcagg.json` | rewrites each school's `xc` block in `assets/data.js` |
| `apply_races.py` | `.work/xcraces_new.js` | splices the rebuilt races into `assets/detail.js`, preserving `@@KEEP@@` blocks |

`slugmap.json` is the explicit school-name → TFRRS-slug map. It is the most valuable
file in here and the reason #7 (Shorter was never measured) is a one-line fix rather
than an investigation. **Explicit only — no fuzzy matching.** Fuzzy matching produced
confident false positives once already.

## Deliberately not moved

`/tmp/render_test.js` was a stub-DOM sweep of the school pages. `render-check.js` does
the same job against real jsdom and asserts its counts, so importing it would have meant
carrying two harnesses that disagree about what "rendered" means. The rest of
`/tmp/sweep/` is one-off scratch — audits, restatements and splices already applied to
`assets/` — plus the fetch caches, which `.gitignore` now covers by convention.
