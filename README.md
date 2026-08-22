# XC / Track + Computer Science — College Recruiting Board

A research board for a high school distance runner who wants to run cross country and
track in college while studying computer science. It covers three metro areas, lists
every college inside each radius that sponsors men's cross country, and ranks them by
the one question that predicts whether a distance runner actually develops:

> **How far back of this team's best runner would he be?**

**Live site:** https://timhibbard.github.io/xc-cs-college-board/

## The framing rule

Being **40–60 seconds behind a team's best 5000m runner is the healthy target** — that is
a 5th-to-9th man as a freshman, with training partners ahead of him and a path to scoring
by junior year. Arriving *ahead* of a team's #1 means the program is thin, not that the
athlete is a star. Distance runners develop in packs.

An earlier version of this analysis had that backwards. The tiers reflect the corrected reading.

## Metros

| Metro | Radius | Source document |
|---|---|---|
| Greenville, SC | 200 mi | [`docs/greenville-sc.md`](docs/greenville-sc.md) |
| New York City | 50 mi | [`docs/new-york-city.md`](docs/new-york-city.md) |
| Chicago | 20 mi | [`docs/chicago.md`](docs/chicago.md) |

## Two structural findings

- **Northwestern sponsors no men's cross country or men's track and field at all.** Men's
  track is listed as defunct; only the women's programs exist. Worth stating plainly,
  because Northwestern is the obvious first thought for Chicago plus elite CS.
- **The 20-mile Chicago radius excludes every strong distance program in the region.** The
  most consequential exclusion is Lewis University (D2 GLVC, ~30 mi), which on the
  available evidence is a better athletic-and-CS fit than anything inside 20 miles.

## Data caveats — read these

Roster marks come from [TFRRS](https://www.tfrrs.org). Team pages there return the
**single fastest athlete, in one event, in the 2026 outdoor season only**:

1. **It is a floor, never a ceiling.** Programs whose runners focused on the 10K, steeple,
   or indoor season show artificially slow outdoor 5000s.
2. **Only the 5000 and 1500 are trustworthy.** The mile, 3000, and 10,000 columns are
   sparse enough to be misleading.
3. **No team depth is available** — no 5th or 7th man. Getting conference-championship
   results is the highest-value outstanding task.

SAT and acceptance-rate figures are approximate, drawn from general knowledge, and
unverified against current Common Data Sets. CS degrees are marked verified or
needs-confirmation individually. Full detail on the
[methodology page](https://timhibbard.github.io/xc-cs-college-board/methodology.html).

## Structure

```
index.html          overview: KPIs, gap chart, filterable table of every school
greenville.html     per-metro write-up + filtered table and chart
new-york.html
chicago.html
methodology.html    conversions, data caveats, NCAA rules, known gaps
assets/data.js      the entire dataset — edit here, everything re-renders
assets/app.js       table sort/filter, diverging gap chart, theme toggle
assets/styles.css   light/dark tokens, accessible status tiers
docs/*.md           the original long-form research documents
```

## Deploying

No build step and no dependencies — plain HTML, CSS, and one JS file. `.nojekyll` is
present so GitHub Pages serves the files as-is. To publish: **Settings → Pages → Source:
Deploy from a branch → `main` / `(root)`**.

To run locally:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Updating the data

`assets/data.js` is the single source of truth for the site. Each school is one object:

```js
{ name: 'Davidson', city: 'Davidson NC', metro: 'greenville', mi: 115,
  div: 'D1', conf: 'Atlantic 10', cs: 'verified', sat: '1360–1500',
  accept: '~18%', b1500: '3:48.3', b5000: 856, tier: 'target' }
```

`b5000` is in **seconds** so it can be charted; `null` means no data was found. `tier` is
`target`, `verify`, or `caution`. Changing a value updates the tables, the chart, and the
KPI tiles with no other edits.

## Note on scope

This is a research artifact about college programs, not a public profile. The athlete is a
minor and is not named anywhere in this repository; the marks used are a projection for
scoring purposes.
