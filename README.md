# XC / Track + Computer Science — College Recruiting Board

A research board for a high school distance runner who wants to run cross country and
track in college while studying computer science. It covers three metro areas, lists the
colleges inside each radius that sponsor men's cross country, and ranks them by
the one question that predicts whether a distance runner actually develops:

> **Where would he finish inside this team's scoring seven?**

**Live site:** https://timhibbard.github.io/xc-cs-college-board/

**131 schools on the board, 12 cut as walk-on, 8 with no men's program to join.** All 151 carry
federal cost and admissions data, a detail page, and **the name and contact details of the coach who
would recruit him**; **129 of the 131 have real cross country depth data** — it was 37 — and eleven
of those also have a map of every meet the program attended last season. Only Calumet College and
Shorter still sit at *Verify*, which means **unmeasured, not borderline**.

Measuring all of them produced one finding that changed the method: **43 of the 129 measured
programs never finished seven runners in any 2025 championship race**, so there is no 7th man to
compare against. Those schools are compared to the team's *last* finisher instead and say so, and
the five that could not finish the scoring five — Roosevelt, Benedict, John Jay, Mount Saint Vincent
and York College (CUNY) — are held at *Caution* regardless of times.

An earlier version of this file claimed the board listed *every* college inside each radius that
sponsors men's cross country. **That was false**, and the correction is the largest single change
in the project: rebuilding the candidate lists conference by conference from each conference's own
men's-sponsored-sports tables added 72 schools, 40 of which had been inside the original Greenville
radius the whole time — including one 25 driving miles from home. NAIA and NCCAA coverage is
[still incomplete and documented as such](https://timhibbard.github.io/xc-cs-college-board/methodology.html).

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

Where a team never finished seven, **vs their 7th** is left blank rather than guessed at, and the
comparison runs against their last finisher instead. Races with fewer than five finishers are not
team results and are excluded from the averages entirely — 16 of the 212 races on file.

Four tiers follow from that: **Target** (a clean 4th–9th man fit), **Deep** (just outside the
travel squad — a good development environment, no freshman travel), **Verify** (no cross country
data yet, so the tier is a placeholder), **Caution** (he arrives at or ahead of their #1). *Verify*
now means **unmeasured and nothing else**; an earlier version also used it for measured schools with
a borderline slot, which made the tier impossible to read.

Cross country times are also **course-corrected** where at least three teams cross-check the
same course against a calibrated one. The 212 races span roughly fifty courses and exactly two
cleared that bar, so most schools rest on an uncorrected time — the largest remaining source of
error here. Getting the sign of one correction backwards briefly promoted a cut school to
target tier, which is documented rather than quietly fixed.

## Metros

| Metro | Radius | Schools | Target tier | With XC data | No 7th man | Source document |
|---|---|---|---|---|---|---|
| Greenville, SC | 250 mi | 81 | 23 | 80 | 25 | [`docs/greenville-sc.md`](docs/greenville-sc.md) |
| New York City | 20 mi + all of Long Island | 38 | 4 | 38 | 13 | [`docs/new-york-city.md`](docs/new-york-city.md) |
| Chicago | 20 mi | 12 | 1 | 11 | 5 | [`docs/chicago.md`](docs/chicago.md) |

The New York rule is a shape, not a circle: 20 driving miles from Midtown **plus all of Nassau and
Suffolk County** regardless of distance, because Long Island is a commutable corridor while
Westchester and central New Jersey at the same distance are a different decision. The map draws that
rule literally — a 20-mile circle around Midtown unioned with a traced outline of the two Long Island
counties — rather than a circle with a caption apologising for the pins outside it.

Radii were widened in Greenville and tightened in the other two after the first pass. The tightening
was not free: New York lost target-tier **Fairfield** and deep-tier **Monmouth**, and Chicago lost
**North Central**, a D3 national program whose 7th man was about ten seconds outside his projection,
along with **Purdue Northwest**, which had been the metro's only scholarship program. **Roosevelt**
(D2, one mile from the Loop) was supposed to fill that slot, and then its GLIAC result came in:
**four finishers**, where five are needed to score.

## Withdrawn recommendations

The cross country data reversed four confident earlier claims. All four are stated in place
rather than edited out, because the pattern is the useful part:

- **Hofstra** was the #2 pick in New York on a 14:32 outdoor 5000. They won the CAA with a
  top seven of 23:02–24:45; he projects ~82 seconds outside it. **Cut.**
- **Loyola Chicago** was called co-equal with DePaul. They won the Atlantic 10 with seven
  runners inside 47 seconds; he projects ~82 seconds outside that pack. **Cut.**
- **Lenoir-Rhyne** was one of three D2 top picks in Greenville. At the D2 regional its scoring
  six ran 33:44–39:11 and he would be their #1. **Caution.**
- **Lewis University** was called "probably the single best fit in metro Chicago," and widening the
  radius was recommended specifically to reach it. Its roster then showed a 13:45 5000 and a 95-second
  gap. **Cut**, and now out of range as well.

The fifth withdrawal is the completeness claim at the top of this file, and it is the biggest one.

**Two schools were also cut in error and are back on the board.** Clemson and Columbia were both
removed on their track marks alone — a 14:36 and a 13:43 5000 read as out of reach. Their actual
championship results say otherwise: he would have been Clemson's 8th man at the ACC meet and their
7th at the Southeast regional, and Columbia's #5 at Ivy Heps before slipping to 8th at the Northeast
regional. Clemson returns at *Deep*, Columbia at *Target*. Cutting a school on one fast 5000 is the
same mistake as recommending one on it.

Also structural: **eight schools on these maps have no men's program to join.** Northwestern sponsors
no men's cross country or men's track and field at all — men's track is listed as defunct, only the
women's programs exist, which is worth stating plainly because Northwestern is the obvious first
thought for Chicago plus elite CS. Georgia State, NYIT, Montclair State, William Paterson and
**North Georgia** were all sitting on the board at *Verify* tier when in fact no men's cross country
team exists at any of them, which is exactly how that tier fails — it reads as a program awaiting
measurement rather than one that does not exist. **St. John's** was worse: it sat on the *cut* list,
so the board was declining to recruit a program that does not exist. Trinity Christian announced on
4 November 2025 that it will close after the 2025–26 year. All eight are kept on the maps rather
than deleted so the corrections stay visible.
**Chicago is also thin on its own merits, not because of the radius** — at 30 miles it held four
extra schools and still only one target-tier fit, and now that all eleven programs in range are
measured, five of them never finished seven.

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

**Town population:** the U.S. Census Bureau's American Community Survey, table B01003, **2024
5-year estimates**, read through the Census Reporter API and matched to the exact place each campus
sits in. Collected for the **Greenville ring only** — how big New York and Chicago are is not a
question this board needs to answer. Undergraduate enrollment comes from the same federal record as
the cost data. Both appear as columns on the Greenville table and as rows on every school page.
Three figures are consolidated city-county governments (Augusta, Macon, Athens) and are therefore
county-wide; four places are census-designated rather than incorporated (Buies Creek, Cullowhee,
Tigerville, Emory VA); and a small figure inside a large metro describes the address, not the
setting.

**Coach names and contacts:** each school's **own athletics staff directory** and nowhere else —
three platforms cover nearly all of them (Sidearm Sports at `/sports/<sport>/coaches` or
`/staff-directory`, PrestoSports at `/information/directory/index`, and a handful of hand-built
department pages). Every school page links the exact directory its entry came from. Two schools
publish no email at all (Fayetteville State and West Georgia) and say so rather than guessing at an
address pattern. Sidearm splits addresses across two JavaScript variables that are joined in the
browser, so a naive fetch reports them as missing; reassembling those is the difference between full
coverage and about half. **This is the fastest-decaying data on the site** — staffs turn over yearly
and these were read in August 2026, so the link matters more than the name.

**Individual athletes are not named anywhere.** Race tables show times in finishing order as
"Their #1 … Their #7". The times are what the comparison needs; the identities are not, and this
is a public page. Every race names the meet and date so any of it can be checked at source. Coaches
*are* named, which is not an inconsistency: a head coach is a public professional whose employer
publishes their name and work email in order to be contacted.

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
into finishing order, a season-colored map of every meet the program attended, a **Who to email**
block with the coach's name, title, phone, address and the directory it was read from, and a closing
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
  xc: { slot: 4, g1: 97.4, v7: -41.3, spread: 138.7, disagree: false, nraces: 1 },
  coach: { name: 'Matt Stuck', title: "Director of Men's Cross Country and Track & Field",
           email: 'mastuck@davidson.edu', phone: null,
           src: 'https://www.davidsonwildcats.com/sports/mens-cross-country/coaches' } }
```

`b5000`, `spread`, `g1` and `v7` are in **seconds**; `b1500` is the mark as written on the results
page, tenths and all, parsed at render time; `null` means no data was found. `tier` is
`target`, `deep`, `verify`, or `caution`, and `tierSrc` records whether it came from cross
country results (`xc`) or from track marks alone (`5000`). Changing a value updates the tables,
the chart, the maps, the KPI tiles and the school page with no other edits.

A team that never finished seven carries `v7: null` plus `short: true` and `maxfin: N` — the most
runners they ever got to a finish line. `nraces` counts only races with five or more finishers,
so a school whose every race was short averages over zero races and the page says exactly that
instead of printing a number. `coach.src` is required: it is the page the rest of the block was read
off, and it is what makes a stale name recoverable.

`ATHLETE` in the same file holds his projections, including `proj1600`/`proj1500`: the 1500 is the
projected 4:18 1600 converted at the textbook Riegel exponent (4:01), which is the one conversion on
this board anchored to the 1600 rather than the 3200 — over 100 metres *less* than a race he has run,
a speed lean is an asset. `TOWNPOP` maps each `city` string to its ACS population; a key that does
not match shows as a missing number rather than a wrong one.

`assets/detail.js` holds the per-race data behind the school pages: `XCRACES` (each race's finishers
as raw seconds, in order — 212 races across 140 schools; a short race also carries `nfin` and
`vlast`, the gap to their last finisher), `SCHED` (full season schedules for eleven schools), and
`VENUES` (meet name → coordinates, with a flag for whether the location was read off the results page
or inferred from the host).

`mi` is approximate **driving** distance from the metro center; `lat`/`lon` are approximate
main-campus coordinates used only to place a map pin. The two are different measurements, so a
school sitting on the radius line can plot just outside the map's circle — driving distance is
always the larger number. On the New York map that happens at scale and on purpose, because
everything on Long Island is in range regardless of miles.

For the 73 schools added when the radii changed, `mi` is an **estimate**, not a looked-up route:
straight-line distance × 1.18, or × 1.35 in the mountain states (TN, VA, WV, KY), rounded to the
nearest 5. Expect ±15%, which matters only for the handful near the 250-mile line.

## Note on scope

This is a research artifact about college programs, not a public profile. The athlete is a
minor and is not named anywhere in this repository, and neither is any college athlete whose
result appears in it. The marks used are a projection for scoring purposes.
