# XC / Track + Computer Science — College Recruiting Board

A research board for a high school distance runner who wants to run cross country and
track in college while studying computer science. It covers three metro areas, lists
every college inside each radius that sponsors men's cross country, and ranks them by
the one question that predicts whether a distance runner actually develops:

> **Where would he finish inside this team's scoring seven?**

**Live site:** https://timhibbard.github.io/xc-cs-college-board/

78 schools on the board, 16 cut, 42 with real cross country depth data, all 78 with federal
cost and admissions data, and a detail page per school with a map of every meet that program
attended last season.

## The framing rule

**Arriving as a team's 5th through 9th man is the healthy target** — training partners ahead
of him and a path to scoring by junior year. Arriving *ahead* of a team's #1 means the program
is thin, not that the athlete is a star. Distance runners develop in packs.

An early version of this analysis had that backwards. The tiers reflect the corrected reading.

## How schools are ranked

The board used to rank on the gap to a team's best outdoor 5000 runner. **That method has been
retired** — it was systematically too generous, because a team's fastest outdoor 5000 is a floor
set by whichever athlete happened to race it, often not the athlete who leads their cross
country squad. DePaul's best outdoor 5000 was 14:22 while their cross country #1 was around
23:44 for 8K; Hofstra's was 14:32 against a 23:02 front-runner.

Ranking now runs on **actual 2025 cross country results** — every finisher in a team's top
seven, at every race on file:

| Signal | What it is |
|---|---|
| **slot** | where his projection would have finished inside their top seven, averaged over every race on file |
| **vs their 7th** | seconds between his projection and their 7th man; positive means outside the seven |
| **1–7 spread** | seconds from their #1 to their #7 — the most course-independent number available, because it compares a team only to itself |

Four tiers follow from that: **Target** (a clean 4th–9th man fit), **Deep** (just outside the
travel squad — a good development environment, no freshman travel), **Verify** (no cross country
data yet, so the tier is a placeholder), **Caution** (he arrives at or ahead of their #1).

Cross country times are also **course-corrected** where at least three teams cross-check the
same course against a calibrated one. Two corrections survived that bar; twelve courses remain
uncalibrated. Getting the sign of one correction backwards briefly promoted a cut school to
target tier, which is documented rather than quietly fixed.

## Metros

| Metro | Radius | Schools | Target tier | Source document |
|---|---|---|---|---|
| Greenville, SC | 200 mi | 27 | 9 | [`docs/greenville-sc.md`](docs/greenville-sc.md) |
| New York City | 50 mi | 34 | 3 | [`docs/new-york-city.md`](docs/new-york-city.md) |
| Chicago | 30 mi | 17 | 1 | [`docs/chicago.md`](docs/chicago.md) |

## Four withdrawn recommendations

The cross country data reversed four confident earlier claims. All four are stated in place
rather than edited out, because the pattern is the useful part:

- **Hofstra** was the #2 pick in New York on a 14:32 outdoor 5000. They won the CAA with a
  top seven of 23:02–24:45; he projects ~82 seconds outside it. **Cut.**
- **Loyola Chicago** was called co-equal with DePaul. They won the Atlantic 10 with seven
  runners inside 47 seconds; he projects ~82 seconds outside that pack. **Cut.**
- **Lenoir-Rhyne** was one of three D2 top picks in Greenville. At the D2 regional its scoring
  six ran 33:44–39:11 and he would be their #1. **Caution.**
- **North Central** was cut as a D3 national champion presumed far beyond him. Their 7th man
  ran 25:34; he is about 10 seconds off the scoring seven. **Restored to the board.**

Also structural, and unchanged: **Northwestern sponsors no men's cross country or men's track
and field at all** — men's track is listed as defunct, only the women's programs exist. Worth
stating plainly, because Northwestern is the obvious first thought for Chicago plus elite CS.
And **Chicago is thin on its own merits, not because of the radius** — widening it from 20 to
30 miles added four schools and no target-tier fit, and the cross country data then took the
metro from two target-tier schools to one.

The [methodology page](https://timhibbard.github.io/xc-cs-college-board/methodology.html) has
the full list of withdrawn claims. Every one started as a confident statement from general
knowledge that the results data then contradicted.

## Where the data comes from

**Cross country and track results:** [TFRRS](https://www.tfrrs.org) — 2025 conference and NCAA
championship results for depth, team pages for individual bests. Team pages return the single
fastest athlete per event per season, which is why they are a floor and not a measure of a
squad. Only the 5000 and 1500 columns there are dense enough to trust; the mile, 3000 and
10,000 are sparse enough to mislead.

**Cost, admissions and CS degree share:** the U.S. Department of Education
[College Scorecard](https://collegescorecard.ed.gov/data/) via `api.data.gov`. Net price is the
federal average after grant aid — not sticker, and not a quote for any individual. Out-of-state
tuition is used at public schools, since the athlete is a South Carolina resident. The CS
figure is the share of a school's bachelor's degrees awarded in the computer science family, so
a program housed under mathematics can read as zero.

Federal data replaced every estimate in the previous version: **33 SAT ranges were off by 60
points or more, and 9 acceptance rates by 15 points or more.**

**Individual athletes are not named anywhere.** Race tables show times in finishing order as
"Their #1 … Their #7". The times are what the comparison needs; the identities are not, and this
is a public page. Every race names the meet and date so any of it can be checked at source.

## Structure

```
index.html          overview: KPIs, filterable table of every school, gap chart
greenville.html     per-metro write-up + filtered table, chart, and radius map
new-york.html
chicago.html
school.html         one data-driven detail page, routed by ?s=<slug>
methodology.html    conversions, how the XC comparison is built, withdrawn claims, known gaps
assets/data.js      schools, tiers, cost, admissions, XC summary — the board's source of truth
assets/detail.js    per-race results, meet venue coordinates, full season schedules
assets/school.js    the school detail template + its per-season meet map
assets/app.js       table sort/filter, gap chart, Leaflet metro maps, theme toggle
assets/styles.css   light/dark tokens, accessible tier and season palettes
docs/*.md           the long-form research documents, one per metro
```

Every school name in every table and every map popup links to `school.html?s=<slug>`, which
renders cost, admissions, CS, track marks, each cross country race with his projection dropped
into finishing order, a season-colored map of every meet the program attended, and a closing
table of what on that page is verified and what is not.

## Deploying

No build step and no dependencies — plain HTML, CSS, and JS, plus Leaflet from a CDN for the
maps. `.nojekyll` is present so GitHub Pages serves the files as-is. To publish:
**Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.

To run locally:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Updating the data

`assets/data.js` is the source of truth for the board. Each school is one object:

```js
{ name: 'Davidson', slug: 'davidson', city: 'Davidson NC', metro: 'greenville', mi: 115,
  lat: 35.5010, lon: -80.8480, div: 'D1', conf: 'Atlantic 10',
  cs: 'verified', csSrc: 'fed', csShare: 6.9,
  sat: '1400–1530', satSrc: 'fed', accept: '13%', acceptSrc: 'fed',
  cost: { own: 'private', resid: 'out', tuition: 64410, rb: 17100,
          sticker: 81510, net: 17379, size: 1867, ipeds: 198385 },
  b1500: '3:48.3', b5000: 856,
  tier: 'target', tierSrc: 'xc',
  xc: { slot: 4, g1: 97.4, v7: -41.3, spread: 138.7, disagree: false, nraces: 1 } }
```

`b5000`, `spread`, `g1` and `v7` are in **seconds**; `null` means no data was found. `tier` is
`target`, `deep`, `verify`, or `caution`, and `tierSrc` records whether it came from cross
country results (`xc`) or from track marks alone (`5000`). Changing a value updates the tables,
the chart, the maps, the KPI tiles and the school page with no other edits.

`assets/detail.js` holds the per-race data behind the school pages: `XCRACES` (each race's top
seven as raw seconds), `SCHED` (full season schedules), and `VENUES` (meet name → coordinates,
with a flag for whether the location was read off the results page or inferred from the host).

`mi` is approximate **driving** distance from the metro center; `lat`/`lon` are approximate
main-campus coordinates used only to place a map pin. The two are different measurements, so a
school sitting on the radius line can plot just outside the map's circle — driving distance is
always the larger number. Sacred Heart is the one visible instance and is kept deliberately as
a boundary case.

## Note on scope

This is a research artifact about college programs, not a public profile. The athlete is a
minor and is not named anywhere in this repository, and neither is any college athlete whose
result appears in it. The marks used are a projection for scoring purposes.
