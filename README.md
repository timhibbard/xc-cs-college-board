# XC / Track + Computer Science — College Recruiting Board

A research board for a high school distance runner who wants to run cross country and
track in college while studying computer science. It covers three metro areas, lists the
colleges inside each radius that sponsor **both** men's cross country and men's outdoor track, and
ranks them by the one question that predicts whether a distance runner actually develops:

> **Where would he finish inside this team's scoring seven?**

**Live site:** https://timhibbard.github.io/xc-cs-college-board/

**The board covers every division: 120 schools on it — 44 D1, 46 D2, 28 D3 and two NAIA — plus 13 cut
as walk-on, 17 with cross country but no men's track, and 11 with no men's program to join.** A
Division-1-only rule was tried on this board and **reversed**; the write-up of it is kept as a decision
made and undone rather than deleted, because the reason it failed is the useful part — it removed 96 rows,
thirteen of them at target tier and all thirteen in the Greenville ring. All 150 rows that have a men's
program carry federal cost and admissions data, a detail page, **the name and contact details of the coach
who would recruit him**, and **the program's Instagram** (147 of the 150) — plus **the coach's own
Instagram on 17 rows**, recorded only where the account's own bio says they coach this program; **119 of
the 120 on the board
rest on a real 2025 cross country result**, each with **its 2026 conference-championship 1500 field** and
his projected 4:01 dropped into it, and 150 of the 161 pages also carry a map of every meet the program
attended last season. Only **Shorter** and **Calumet College** still sit at *Verify*, which means
**unmeasured, not borderline**.

**The Greenville ring is 300 driving miles**, widened from 250. That pass turned up eight Division 1
programs new to the board: Auburn, Samford and Radford joined it, NC State, Virginia Tech and Eastern
Kentucky are cut on level, and Tennessee Tech and Jacksonville State fail the both-sports rule. It also
found two schools with no men's cross country to join at all — UAB and Georgia Southern.

**He has a new 5K cross country best: 15:55.** The whole cross-country chain used to run off a
*projected* ~15:59, so the board is now scored against a mark that exists rather than one he might
reach — **8K 26:00, 10K 32:46**, and his solved fatigue exponent drops from **1.196 to 1.117**, which
is the "upside case" the methodology page described arriving a season early. It moves less than it
sounds: seven seconds at 8K, and **two tier changes** (Anderson SC up to *Target*, Southern Wesleyan
down to *Caution*). The track 5000 stays at **15:20** — the 15:55 independently implies about 15:16 via
the grass-to-track differential, so 15:20 is now a floor rather than a goal. Nothing projects the 15:55
forward even though it was run early in the season; the methodology page has the sensitivity if you
want it.

**The board requires both sports.** He wants to run cross country *and* track, so a program that
sponsors one without the other cannot give him both: **seventeen schools came off the board** for that
reason alone, ten of them in New York, and one of them — **Mercer** — was sitting at *Target* tier
with his 4th man 196 miles from home. Each was checked twice: the sport list and published track roster
the school puts out itself, and TFRRS for the school's men at their **conference indoor and outdoor
championships**, where a sponsored program has to appear. That second check is deliberately narrow: men
on a cross country roster post open-meet 1500s and 5000s whether or not the school sponsors men's track,
which is exactly the case at **Tennessee Tech** — target tier at 270 miles, and removed. All seventeen
keep their pages and their cross country numbers, because the numbers are true and it is the rule that
removed them. Three of them are Division 1, and all three are in the Greenville ring.

Measuring all of them produced one finding that changed the method: **45 of the 148 measured
programs never finished seven runners in any 2025 championship race**, so there is no 7th man to
compare against. Those schools are compared to the team's *last* finisher instead and say so, and
the five that could not finish the scoring five — Roosevelt, Benedict, John Jay, Mount Saint Vincent
and York College (CUNY) — are held at *Caution* regardless of times. On the board itself the count is
**38 of 120**: 25 around Greenville, 8 around New York and 5 in Chicago. It is not a small-college
problem with a divisional fix — five of the 25 in Greenville are Division 1 — which is one of the
reasons the Division 1 rule did not survive.

The 1500 data says the same thing a second way: at **57 of the 114 programs that raced a 1500 in
2026** his projected 4:01 would be their fastest man in the event, and the median program's best 1500
went 4:01.1. In the other direction he would have made the conference final at **105 of 120**
championships and scored — top eight — at **64**. The divisional split is stark, and it cuts the other
way from the tier ladder: across the 44 Division 1 rows the median best 1500 is **3:49.7**, he makes the
final at 29 of them and scores at 8. Read against 91 rows that actually entered somebody in the event at
their conference meet, he makes 79 finals and scores in 50 — **29 programs entered nobody in the 1500 at
all**, which is a fact about how the event is used rather than about him.

An earlier version of this file claimed the board listed *every* college inside each radius that
sponsors men's cross country. **That was false**, and the correction is the second largest change
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
team results and are excluded from the averages entirely — 17 of the 228 races on file.

Four tiers follow from that: **Target** (a clean 4th–9th man fit), **Deep** (just outside the
travel squad — a good development environment, no freshman travel), **Verify** (no cross country
data yet, so the tier is a placeholder), **Caution** (he arrives at or ahead of their #1). *Verify*
now means **unmeasured and nothing else**; an earlier version also used it for measured schools with
a borderline slot, which made the tier impossible to read.

**The 1500 does not move a tier.** Tiers come from cross country and nothing else. Every school page
also carries the full 1500 field from that program's 2026 outdoor conference championship — his
projected 4:01 dropped in on time, ranked against every man who ran the event at the meet with prelims
included, plus the program's own 1500 depth chart for the season and whether he would have made the
final. It is a second independent read on the same question, and it disagrees with the cross country
read often enough to be worth having: NJIT and Queens (Charlotte) are both *Target* on depth and would
have missed their conference 1500 final. Championship finals are frequently tactical — the Atlantic 10
final was won in 4:03.61 while a prelim went 3:47.69 — so the whole-field placing is the headline and a
tactical final is flagged as one rather than read as a level.

Cross country times are also **course-corrected** where at least three teams cross-check the
same course against a calibrated one. The 228 races span roughly fifty courses and exactly two
cleared that bar, so most schools rest on an uncorrected time — the largest remaining source of
error here. Getting the sign of one correction backwards briefly promoted a cut school to
target tier, which is documented rather than quietly fixed.

**And it was then only half-applied.** The −96.5s South Atlantic correction reached the three teams
used to *derive* it and none of the other seven, so those programs' times sat in the tables raw for
several passes. Because the correction makes their times faster, the omission made them read as
thinner than they are, and **five schools were sitting at *Caution* on an arithmetic omission**:
Emory & Henry, Lincoln Memorial, Mars Hill, Tusculum and UVA Wise, all now *Target*. Every derived
number in `assets/data.js` and `assets/detail.js` is now **generated from the raw runner times**
rather than edited in place, and the invariant is checkable: each stored `slot`, `g1`, `v7` and
`spread` must reproduce exactly from the times it summarises.

## Metros

Every count here is the live board, all divisions.

| Metro | Radius | On the board | Target tier | No 7th man | Cut as walk-on | No men's track | No men's program | Source document |
|---|---|---|---|---|---|---|---|---|
| Greenville, SC | 300 mi | 81 | 29 | 25 | 10 | 6 | 5 | [`docs/greenville-sc.md`](docs/greenville-sc.md) |
| New York City | 20 mi + all of Long Island | 28 | 4 | 8 | 2 | 10 | 4 | [`docs/new-york-city.md`](docs/new-york-city.md) |
| Chicago | 20 mi | 11 | 1 | 5 | 1 | 1 | 2 | [`docs/chicago.md`](docs/chicago.md) |

A "with XC data" column would read 80, 28 and 11 — every school on the board except **Shorter**, which
never fielded a measurable championship squad. The divisional shape of the three rings is completely
different and worth reading before the tiers: Greenville is 31 D1, 38 D2, 11 D3 and one NAIA; New York
is 10 D1, 7 D2 and 11 D3; Chicago is 3 D1, one D2, 6 D3 and one NAIA. **Chicago is a Division 3 city**
for men's distance running, and ten of New York's seventeen no-men's-track removals are D3 CUNY and
small-private programs.

The New York rule is a shape, not a circle: 20 driving miles from Midtown **plus all of Nassau and
Suffolk County** regardless of distance, because Long Island is a commutable corridor while
Westchester and central New Jersey at the same distance are a different decision. The map draws that
rule literally — a 20-mile circle around Midtown unioned with a traced outline of the two Long Island
counties — rather than a circle with a caption apologising for the pins outside it.

Radii were widened in Greenville — twice, to 250 miles and then to 300 — and tightened in the other
two after the first pass. The tightening
was not free: New York lost target-tier **Fairfield** and deep-tier **Monmouth**, and Chicago lost
**North Central**, a D3 national program whose 7th man was about five seconds outside his projection,
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

The fifth withdrawal is the completeness claim at the top of this file. The sixth is larger than any
of them and is a rule rather than a school: the board now requires **both** cross country and outdoor
track, which took seventeen schools off it including target-tier **Mercer** and target-tier **Tennessee
Tech**. The seventh is larger still, is also a rule, and is the only one that has itself been withdrawn: the
board was narrowed to **Division 1 only**, which removed 96 rows, thirteen of them at target tier and all
thirteen in the Greenville ring — including **Anderson (SC)**, 29 driving miles from home and the closest
target anywhere, and **Fayetteville State** at an $11,892 net price, the cheapest target anywhere. Nothing
about the running justified that: the thirteen were target tier on measured championship results, not on
division. Because the rule was implemented as an archive rather than a deletion, undoing it required no
re-measuring — every slot, gap, spread, tier and coach came back exactly as it went in. The lesson worth
keeping is about the shape of the mistake: a filter on a *label* silently deleted the two rows the whole
search existed to find.

**Two schools were also cut in error and are back on the board.** Clemson and Columbia were both
removed on their track marks alone — a 14:36 and a 13:43 5000 read as out of reach. Their actual
championship results say otherwise: he would have been Clemson's 8th man at the ACC meet and their
7th at the Southeast regional, and Columbia's #5 at Ivy Heps before slipping to 8th at the Northeast
regional. Clemson returns at *Deep*, Columbia at *Target*. Cutting a school on one fast 5000 is the
same mistake as recommending one on it.

Also structural: **ten schools on these maps have no men's program to join at all**, and an eleventh is
closing — a different finding from the seventeen that sponsor cross country without track. **UAB** came
into range at 300 miles and turned out to have nothing to come into range for, and **Georgia Southern**
was inside even the old 250-mile ring; neither sponsors men's cross country. Northwestern sponsors
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
measured, five of them never finished seven. Only three of the eleven are Division 1 and six are
Division 3, so athletic money in this metro exists at exactly two addresses: Roosevelt (D2, and it
finished four runners) and Saint Xavier (NAIA, and he would be their #1).

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

**Every coach name was re-checked against the school's own staff directory a month after it was
first read, and five had already changed** — Young Harris, Savannah State, Clayton State, Montreat and
Yeshiva, four of the five replacements carrying an *interim* title. 141 names confirmed on the live page,
three apparent misses that were the fetch's fault and confirmed correct elsewhere, and one row (Baruch)
whose site would not answer at all. That is a ~3%-per-month decay rate on the most actionable column on
the site, which is why every school page links the directory it was read from. The Young Harris change
was found the long way round: a coach handle matched the name perfectly and had to be rejected because
the bio placed him at Evansville — and it was right, and this board was a season out of date.

Every admit rate was then **re-verified row by row against the live Scorecard**, matched on IPEDS unit ID
rather than by name. **148 numeric rates match the federal figure exactly, with zero mismatches.** Two
things came out of it. Three rows that read "not reported" — Savannah State, Felician and Calumet College
— return no `admission_rate.overall` but carry `open_admissions_policy = 1` and a consumer rate of 1.0,
so they are **open-admission schools rather than missing data** and now read 100%; every one of the 150
rows has a federal admit rate. And **St. Joseph's Long Island and St. Joseph's Univ NY share IPEDS
195544**, correctly: they are one federally reporting institution fielding two NCAA programs, so the
admit rate, SAT range, net price and enrollment on both pages describe the combined university. Neither
is on the board, so no ranking depends on it.

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
"Their #1 … Their #7", and the 1500 tables the same way. The times are what the comparison needs; the
identities are not, and this is a public page. Names were used transiently to de-duplicate one man's
several 1500 marks and then discarded. Every race names the meet and date and links its results page,
so any of it can be checked at source. Coaches
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
into finishing order, the 2026 conference-championship 1500 field with the same projection dropped
into that, a season-colored map of every meet the program attended, a **Who to email**
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

At a public school `cost` also carries `tuiIn` and `tuiOut`, both from the same federal record.
`tuition` is already the rate that applies to him — in-state at the eleven South Carolina publics,
out-of-state everywhere else — and the two extra fields let the site reconcile it with the federal
average net price, which at a public is computed from **in-state students only**. Every net price
shown for an out-of-state public is therefore `net + (tuiOut − tuiIn)`, marked with a `≈`; the
[methodology](https://timhibbard.github.io/xc-cs-college-board/methodology.html#residency) explains
why and lists the two flat-rate exceptions.

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
as raw seconds, in order — 228 races across 148 schools; a short race also carries `nfin` and
`vlast`, the gap to their last finisher), `T1500` (the 2026 outdoor 1500 for 120 schools: the
program's season depth chart `d15`, its conference-championship field `cm`, and any postseason rounds
`post`, read from 40 conference championship result pages plus four postseason pages), and the 2025–26
schedule, which is three tables so that no fact is stated twice: `VENUES` (419 places, each geocoded
once, with `src` giving the precision — `r` the facility, `z` the ZIP the results page printed, `c` the
town it named), `MEETS` (712 meets keyed by their own TFRRS id, because two different meets can share a
name; each carries date, season and a `VENUES` index), and `SCHED` (school name → the meet ids its own
TFRRS results page shows it at, in date order — 3,241 appearances across 150 of the 161 schools with a
page).

`NO_TRACK` in `assets/data.js` holds all **17** schools removed under the both-sports rule — three of
them Division 1 (Mercer, Tennessee Tech and Jacksonville State), three D2, ten D3 and one NAIA. All of
them keep their complete records — tier, cross country, cost, coach — plus a `why` naming both signals
that agreed, so the removal is reversible with one line of data if a cross-country-only program ever
becomes acceptable.

**There is no `NOT_D1` array any more.** The Division 1 rule held 96 rows in one, each tagged with where
it sat before the filter, precisely so that reversing it would be mechanical; when it was reversed the 96
went back into `SCHOOLS`, `REMOVED` and `NO_TRACK` and the `was:` tags came off. That is the argument for
archiving rather than deleting, stated as an outcome rather than a plan: nothing had to be re-measured and
no page had to be rebuilt. Division is a column and a filter on every table on the site, so the
Division-1-only view is still one click away — it is just no longer the board.

`mi` is approximate **driving** distance from the metro center; `lat`/`lon` are approximate
main-campus coordinates used only to place a map pin. The two are different measurements, so a
school sitting on the radius line can plot just outside the map's circle — driving distance is
always the larger number. On the New York map that happens at scale and on purpose, because
everything on Long Island is in range regardless of miles.

Every school in the Greenville ring now carries a real **OSRM driving route** from the search center,
rounded to the mile, which is what decides whether it is inside the 300-mile line. New York and Chicago
mileages are still the looked-up or estimated figures the board started with — straight-line distance
× 1.18, or × 1.35 in the mountain states (TN, VA, WV, KY), rounded to the nearest 5, ±15% — and at a
20-mile radius that error cannot move a school across the line.

## Note on scope

This is a research artifact about college programs, not a public profile. The athlete is a
minor and is not named anywhere in this repository, and neither is any college athlete whose
result appears in it. The marks used are a projection for scoring purposes.
