# College Search — Greenville SC (200 mile radius)

XC/Track + Computer Science. Last updated 2026-08-22 (v4 — rebuilt on cross country results)

> **Rewritten on cross country data.** Versions 1–3 ranked schools by the gap to their fastest
> outdoor 5000 runner. That method has been retired. This version ranks schools by **where he
> would finish inside their scoring seven at an actual cross country race**, which is what he is
> actually being recruited for. Two schools moved up, one recommendation is withdrawn, and the
> two standing "boundary" cases are resolved. See §2.

Live version, with per-school pages, per-race results and meet maps:
<https://timhibbard.github.io/xc-cs-college-board/greenville.html>

## 1. Athlete profile

| Event | Current | Projected |
|---|---|---|
| 1600m | 4:21 | ~4:18 |
| 3200m | 9:40 | 9:29 |
| 5K XC | 16:29 | ~15:59 |

Converted: **1500 4:03** · **3000 8:53** · **track 5000 15:20** · **8K XC 26:07** · **10K XC 32:54**

The 8K and 10K projections are what the comparison runs on, because college cross country is
raced at 8K (D2, D3 and most conference meets) and 10K (D1 regionals and nationals). The 10K
figure is the 8K figure × 1.26, a factor validated against teams that raced both distances in
2025 — it agreed within about 7 seconds. Full method: `../methodology.html`.

**The framing rule, unchanged.** For this projection, **arriving as a team's 5th through 9th man
is the healthy target** — training partners ahead of him and a path to scoring by junior year.
Being *ahead* of a team's #1 means the program is thin, not that he is a star. Distance runners
develop in packs.

## 2. Read this first: what the cross country data changed

**Withdrawn: Lenoir-Rhyne is no longer a top pick.** Version 3 listed it alongside Catawba and
Anderson as one of the three D2 schools "where the actual scholarship dollars are, all with a
healthy gap to the #1." That rested on an 8:47 3000, which turns out to have been a sparse-table
artifact. At the D2 regional their **scoring six ran 33:44 to 39:11** over 10K — a 326 second
spread — and he would arrive as their **#1 by nearly a minute**. It moves to Caution.

**Resolved upward: UNC Charlotte and Emory.** Both were boundary cases and both improve.

- **UNC Charlotte** was kept in v3 with a flag ("~65–75 seconds off their best runner"). At the
  D1 Southeast regional their seven ran **30:18–33:05** over 10K, putting him right at their 7th
  man, 11 seconds outside the scoring seven. A 167 second 1-through-7 spread means the back of
  that squad is soft — which is exactly where a freshman wants to land. **Target**, and it has
  the highest CS degree share of any D1 school on this list at 15.2%.
- **Emory** sat in the caution tier on a 15:06 outdoor 5000 that read as "immediate top-2." That
  was a sparse-table artifact too, in the opposite direction: the UAA championship shows a
  **25:14–26:27 top seven**, so he slots in around **5th man**. **Target.**

**Resolved downward: Appalachian State and Anderson (SC).** Both were listed in the ideal band or
as boundary keeps; both now sit at **Deep** — just outside the travel squad rather than inside it.
App State is about 35 seconds outside their scoring seven at the regional. Anderson is within
**two seconds** of their 7th man, which sounds better than Deep but is precisely the definition:
last man in, not comfortably in.

**Furman and Wingate stay cut, and cross country confirms both.** Furman won the Southern
Conference with seven runners inside 42 seconds (24:15–24:57) — he would be 70 to 87 seconds
outside that. Wingate's regional seven ran 30:48–31:58, about 56 seconds clear of him. Worth
naming the cost again: this cuts the closest school on the entire board (Furman at 0 miles, with
a verified CS degree) and the second-closest strong CS department (Clemson at 32).

**A correction that nearly went the other way.** The South Atlantic Conference championship
course ran about **96 seconds slow** at 8K — confirmed independently by Anderson, Catawba and
Wingate against the D2 regional. An early version of the correction had the **sign backwards**,
which briefly promoted Wingate from cut to target. Course corrections are applied only where at
least three teams cross-check, and the two that survived that bar are documented in
`../methodology.html` §3a.

## 3. How to read the numbers below

| Column | What it means |
|---|---|
| **XC slot** | where his projection would have finished inside their top seven, averaged over every 2025 race on file. 1 = ahead of their #1. |
| **vs their 7th** | seconds between his projection and their 7th man. `+35s` = he is 35 seconds *outside* the seven. `−41s` = 41 seconds *inside* it. Blank where fewer than seven of their runners finished. |
| **1–7 spread** | seconds from their #1 to their #7. The most course-independent number here, because it compares a team only to itself. A wide spread means a soft back end to slot into; a tight one means there is no room. |
| **Tier** | Target = clean 4th–9th man fit · Deep = just outside the travel squad · Verify = no cross country data yet · Caution = he arrives at or ahead of their #1 |
| **Net cost/yr** | federal average net price after grant aid, from the College Scorecard — **not** sticker price. Out-of-state rates are used at public schools, since he is a South Carolina resident. |
| **CS** | ✅ with a percentage = share of that school's bachelor's degrees awarded in computer science, from federal completion data. A low share is not a bad program. |

Where a school still shows no XC data, the tier is a placeholder, not a judgement.

## 4. Master list

Miles = approximate driving distance from Greenville. School names link to a full detail page with
per-race results, a map of every meet they attended last year, cost, and admissions detail.

### Division 1

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Davidson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=davidson)** | Davidson NC | 115 | Atlantic 10 | ✅ 6.9% | 1400–1530 | 13% | $17,379 | 4 | −41s | 139s | Target |
| **[Elon](https://timhibbard.github.io/xc-cs-college-board/school.html?s=elon)** | Elon NC | 200 | Coastal | ✅ 2.6% | 1130–1280 | 66% | $41,555 | 5 | −40s | 78s | Target |
| **[ETSU](https://timhibbard.github.io/xc-cs-college-board/school.html?s=etsu)** | Johnson City TN | 140 | Southern | ✅ 4.2% | 980–1200 | 86% | $15,983 | 4 | −28s | 171s | Target |
| **[High Point](https://timhibbard.github.io/xc-cs-college-board/school.html?s=high-point)** | High Point NC | 180 | Big South | ✅ 2.3% | 1110–1320 | 75% | $38,707 | 7 | −31s | 66s | Target |
| **[UNC Asheville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-asheville)** | Asheville NC | 62 | Big South | ✅ 3.2% | 1170–1360 | 92% | $12,250 | 5.5 | −50s | 64s | Target |
| **[UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte)** | Charlotte NC | 100 | American | ✅ 15.2% | 1140–1330 | 80% | $15,435 | 7 | −11s | 167s | Target |
| **[UNC Greensboro](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-greensboro)** | Greensboro NC | 170 | Southern | ✅ 7.4% | 1150–1355 | 89% | $10,965 | 4.5 | −126s | 93s | Target |
| **[Appalachian State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=appalachian-state)** | Boone NC | 130 | Sun Belt | ✅ 2.9% | 1120–1280 | 90% | $16,836 | 8 | +35s | 101s | Deep |
| **[Georgia State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-state)** | Atlanta GA | 150 | Sun Belt | ✅ 16.2% | 940–1180 | 55% | $15,931 | — | — | — | Verify |
| **[Kennesaw State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kennesaw-state)** | Kennesaw GA | 125 | CUSA | ✅ 11.1% | 1000–1220 | 69% | $15,048 | — | — | — | Verify |
| **[Gardner-Webb](https://timhibbard.github.io/xc-cs-college-board/school.html?s=gardner-webb)** | Boiling Springs NC | 60 | Big South | ✅ 1.9% | 975–1198 | 77% | $17,674 | 1 | — | 966s | Caution |
| **[Presbyterian](https://timhibbard.github.io/xc-cs-college-board/school.html?s=presbyterian)** | Clinton SC | 45 | Big South | ✅ 1.4% | 980–1200 | 68% | $20,528 | 1 | −263s | 234s | Caution |
| **[USC Upstate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-upstate)** | Spartanburg SC | 32 | Big South | ✅ 8.3% | 1005–1175 | 67% | $13,557 | 2 | −43s | 82s | Caution |
| **[Western Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=western-carolina)** | Cullowhee NC | 60 | Southern | ✅ 1.3% | 1080–1270 | 82% | $13,315 | 2 | −82s | 105s | Caution |
| **[Winthrop](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winthrop)** | Rock Hill SC | 100 | Big South | ✅ 2.5% | 1010–1220 | 79% | $15,343 | 1 | — | 143s | Caution |
| **[Wofford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wofford)** | Spartanburg SC | 32 | Southern | ✅ 3.6% | 1198–1343 | 52% | $18,732 | 1 | — | 222s | Caution |

### Division 2 (scholarship money exists)

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba)** | Salisbury NC | 130 | South Atlantic | ✅ 1.6% | 1030–1300 | 75% | $17,879 | 5.5 | −96s | 133s | Target |
| **[Anderson (SC)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=anderson-sc)** | Anderson SC | 30 | South Atlantic | ✅ 5.0% | 1100–1280 | 55% | $23,544 | 7.5 | +2s | 66s | Deep |
| **[Carson-Newman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=carson-newman)** | Jefferson City TN | 150 | South Atlantic | ✅ 3.1% | 955–1215 | 90% | $20,251 | 1 | — | 289s | Caution |
| **[King University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=king-university)** | Bristol TN | 155 | Conf. Carolinas | ✅ 4.7% | not reported | 100% | $22,347 | 1 | — | 230s | Caution |
| **[Lander](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lander)** | Greenwood SC | 55 | Peach Belt | ✅ 3.4% | 950–1178 | 81% | $15,363 | 1 | −406s | 305s | Caution |
| **[Lenoir-Rhyne](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lenoir-rhyne)** | Hickory NC | 90 | South Atlantic | ✅ 3.7% | not reported | 85% | $20,689 | 1 | — | 326s | Caution |
| **[North Greenville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=north-greenville)** | Tigerville SC | 25 | Conf. Carolinas | ✅ 4.2% | 1060–1240 | 67% | $21,063 | 1 | −397s | 266s | Caution |

> **Limestone University (Gaffney SC) closed in 2025** — remove it from any older list.
> **Anderson (SC) CS note:** the federal file shows 5.0% of their bachelor's degrees in computer
> science, which does confirm a real CS pipeline. Their own site leads with a BA in Applied AI and
> a Center for Cybersecurity, so still ask specifically whether the **BS in Computer Science**
> is the degree he would enrol in.

### Division 3 (no athletic scholarships)

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory)** | Atlanta GA | 145 | UAA | ✅ 3.9% | 1470–1550 | 11% | $22,585 | 5 | −20s | 74s | Target |
| **[Piedmont University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=piedmont-university)** | Demorest GA | 100 | USA South | ⚠️ thin | 1038–1245 | 93% | $20,599 | — | — | — | Verify |
| **[Berry College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=berry-college)** | Rome GA | 150 | SAA | ✅ 5.8% | 1125–1330 | 64% | $22,320 | — | — | — | Caution |
| **[Guilford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=guilford)** | Greensboro NC | 180 | ODAC | ✅ 7.2% | 1120–1260 | 80% | $22,270 | — | — | — | Caution |

## 5. Schools removed — he would be a walk-on

| School | Div | Conf. | Location | XC slot | vs their 7th | 1–7 spread | Why removed |
|---|---|---|---|---|---|---|---|
| **[Furman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=furman)** | D1 | Southern | Greenville SC | 8 | +79s | 42s | Team best 5000 13:40; nationally elite, ~1:40 gap. Zero miles away with a verified CS degree, which is what makes the cut hurt. Cross country confirms it: they won the Southern Conference with seven runners inside 42 seconds (24:15–24:57) and were 7th at the regional. He would be 70 to 87 seconds outside the scoring seven. |
| **[Clemson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clemson)** | D1 | ACC | Clemson SC | — | — | — | ACC program 32 miles away. Their 1500 best of 3:43 implies a ~14:15 5K runner even though the outdoor 5000 table reads 14:36 — the sparse-table problem in the direction that flatters them. |
| **[Georgia Tech](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-tech)** | D1 | ACC | Atlanta GA | — | — | — | 5000 13:41, 10K 29:45. Also the hardest CS admit on the list — GT computing is far more selective than the university's overall rate suggests. |
| **[Wingate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wingate)** | D2 | South Atlantic | Wingate NC | 8 | +34s | 70s | 5000 13:37, 10K 29:20 — the strongest D2 distance program in the region. Cross country is mixed but does not rescue it: at the D2 regional their seven ran 30:48–31:58, about 56 seconds clear of his projection. Kept as a cut on the regional evidence, and this is the school the sign-error correction briefly promoted. |
| **[Tennessee](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tennessee)** | D1 | SEC | Knoxville TN | — | — | — | Out of range. |
| **[Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia)** | D1 | SEC | Athens GA | — | — | — | Out of range. |
| **[Wake Forest](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wake-forest)** | D1 | ACC | Winston-Salem NC | — | — | — | Out of range. |
| **[South Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=south-carolina)** | D1 | SEC | Columbia SC | — | — | — | Out of range. |

If a walk-on or redshirt path ever becomes acceptable, Furman and Clemson go straight back to the
top of the list on every non-athletic axis.

## 6. Tiering

**Target — clean development band, concentrate effort here.** UNC Asheville · Davidson · UNC
Greensboro · ETSU · Elon · High Point · UNC Charlotte · Catawba (D2) · Emory (D3)

**Deep — just outside the travel squad.** Anderson (SC) · Appalachian State

**Verify — no cross country data yet.** Georgia State · Kennesaw State · Piedmont University

**Caution — he arrives at or ahead of their #1.** USC Upstate · Western Carolina · Wofford ·
Winthrop · Presbyterian · Gardner-Webb · North Greenville · Lander · Lenoir-Rhyne · Carson-Newman ·
King University · Berry College · Guilford

**Cut on results.** Furman · Clemson · Georgia Tech · Wingate (plus four out-of-range SEC/ACC
schools)

Twenty-seven schools, **nine of them target tier** — by far the strongest of the three metros, and
the reason this list remains the primary one.

That caution tier still needs care rather than dismissal. Being a team's #1 is fine *if* the coach
is building a class around him — always ask who else they are signing. It is bad if he trains
alone for four years. **Wofford is the sharpest version:** strong academics, verified CS, 32 miles,
and a team he would lead on arrival. **Gardner-Webb's 966 second 1-through-7 spread** is the most
extreme number in this document and means there is effectively no distance squad to join.

## 7. Top picks

1. **[UNC Asheville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-asheville)**
   — 62 miles, Big South, mountain terrain, and the closest target-tier school on the board.
   Confirmed across **two races**: 6th man at the conference meet, 7th at the regional, inside a
   64 second 1-through-7 spread. This is also the school that validated the whole method — the
   direct comparison predicted 6th man before the regional results were pulled, and the regional
   matched. Add a **92% accept rate** and a **$12,250 net price** and it is the single best
   combination of proximity, fit, admission and money in this document.
2. **[Davidson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=davidson)** — 4th
   man in the Atlantic 10 seven, and at a **13% accept rate** coach support is real admissions
   leverage. Net price $17,379, which is remarkable for a school of its sticker. The caveat is
   depth: their 4th through 7th ran 26:22–26:48 and they failed to field a full scoring team at
   the regional, so the front three are strong and behind that it is thin. Highest-value
   application on the list — initiate a **pre-read** in spring of junior year.
3. **[UNC Greensboro](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-greensboro)**
   — 5th man at the conference meet, 7th at the regional, 93 second spread, **$10,965 net — the
   cheapest school in this document**, with an 89% accept rate and a 7.4% CS degree share. If
   money is the deciding axis, this is the answer.
4. **[UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte)**
   — the upgrade described in §2. Right at their 7th man with a soft 167 second back end, a real
   CS school (15.2% of degrees), $15,435 net, 80% accept. A large university with multiple
   sections of every CS course, which matters for the lab-conflict problem in §9.
5. **[Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory)** — the other
   upgrade. 5th man in a 74 second UAA pack, elite CS, no athletic money but strong need-based aid
   bringing net cost to $22,585. An **11% admit**, so the coach's pre-read matters as much as it
   does at Davidson.
6. **[Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba)** — the D2
   pick now that Lenoir-Rhyne is withdrawn. 5th man at the regional and, after correcting the 96
   second course offset, about the same at the conference meet. D2 means partial athletic aid
   genuinely exists. $17,879 net.

Also worth the email, one tier down: **ETSU** and **High Point** are both solid target-tier fits
(ETSU with a soft 171 second middle, High Point confirmed 7th man twice), and **Anderson (SC)** is
30 miles away and within two seconds of their travel squad.

## 8. Academic and money notes

**Recruitment is an admissions lever at selective schools.** Coaches at Davidson (13%) and Emory
(11%) get supported slots and will run a **pre-read** — send transcript and scores, and admissions
tells the coach informally whether he would get in. This is how running unlocks a school his
stats alone would not. Initiate spring of junior year.

**Where academics are an asset rather than a constraint:** UNC Asheville (92%), Appalachian State
(90%), UNC Greensboro (89%), ETSU (86%), Western Carolina (82%), and most of the D2 list.
Admission is close to automatic, so all the leverage shifts to **money**.

**Academic aid often beats athletic aid.** D1 XC/track is a 12.6-scholarship equivalency spread
across a 35–45 man roster — quarter and half rides, not fulls. A strong student stacking merit aid
at UNC Greensboro ($10,965 net), UNC Asheville ($12,250) or Western Carolina ($13,315) can land
well below the net cost of a bigger athletic offer somewhere expensive. **Model net cost, not
scholarship percentage.** The net figures in this document are federal averages across all
students, not a quote for him — treat them as a ranking tool and get real aid estimates from the
schools that survive.

**The two expensive target-tier schools.** Elon ($41,555 net) and High Point ($38,707) are three
to four times the cost of UNCG for a comparable athletic fit. They are on the list because the
running works; rank them last on money unless something specific offsets it.

## 9. Practical notes

**CS labs collide with 3:00–5:30 practice.** Large schools (UNC Charlotte, App State, Georgia
State, Kennesaw State) run multiple sections; small ones (Wofford, Presbyterian, Berry, Piedmont,
North Greenville, Catawba, Anderson) may offer a required course in exactly one afternoon slot.
**Ask every coach: "how many of your athletes major in CS or engineering, and how do you handle
lab conflicts?"** This eliminates programs faster than times do.

**Contact rules.** D1 coaches may initiate contact **June 15 after sophomore year**; D2 July 15
after sophomore year; D3 essentially unrestricted. **He may email coaches any time, any age, any
division** — the restriction runs one direction only.

**What to put in the email.** Lead with the **8K/10K cross country projection**, not the 1600
time, and say what it is projected from. Coaches think in the distance they recruit for, and the
whole point of this document is that a track 1600 is a poor predictor of where someone lands in a
scoring seven.

## 10. To-dos, priority order

1. **Get cross country results for the three Greenville-list schools that still lack them** —
   Georgia State, Kennesaw State, Piedmont University — plus Berry and Guilford, which are ranked
   Caution on track marks alone.
2. **Calibrate more courses.** Only two of the fifteen courses in this dataset have a correction
   applied, because a correction requires at least three cross-checking teams. The Big South,
   Southern and South Atlantic families agree closely; the Peach Belt, Conference Carolinas and
   USA South courses are uncalibrated.
3. Confirm a **true BS in Computer Science** (not IT, cybersecurity, or applied AI) at Anderson
   SC, Presbyterian, North Greenville and USC Upstate; resolve **Piedmont**, whose site has been
   unreachable across several attempts.
4. **Email UNC Asheville, Davidson, UNC Greensboro and Emory.** Four target-tier schools, two of
   which need a pre-read that takes months to arrange.
5. Confirm each program carries **full men's indoor and outdoor track**, not cross country only.
   Each school's detail page maps every meet they attended last year by season, which is a decent
   first check.
6. Verify SAT figures for **King University** and **Lenoir-Rhyne**, which report no SAT range in
   the federal file at all.
