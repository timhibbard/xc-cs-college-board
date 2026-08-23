# College Search — New York City (50 mile radius)

XC/Track + Computer Science. Last updated 2026-08-22 (v2 — rebuilt on cross country results)

> **Rewritten on cross country data, and this metro took the worst of it.** The first version
> ranked schools by the gap to their fastest outdoor 5000 runner. Under that method five schools
> sat in the ideal band. With actual cross country results, **Hofstra is cut**, Wagner and NYU are
> downgraded, and **three target-tier schools remain out of 34**. See §2.

Live version, with per-school pages, per-race results and meet maps:
<https://timhibbard.github.io/xc-cs-college-board/new-york.html>

## 1. Athlete profile

| Event | Current | Projected |
|---|---|---|
| 1600m | 4:21 | ~4:18 |
| 3200m | 9:40 | 9:29 |
| 5K XC | 16:29 | ~15:59 |

Converted: **1500 4:03** · **3000 8:53** · **track 5000 15:20** · **8K XC 26:07** · **10K XC 32:54**

Target: a program where he would arrive as their **5th through 9th man**. Being ahead of a team's
#1 is not a good sign — it means the program is thin and he would train alone. Full method and
caveats: `../methodology.html`; the framing rule and the practical notes are in
`greenville-sc.md` §1 and §9 and apply identically here.

## 2. Read this first: the reversal, and two downgrades

**Withdrawn: Hofstra is cut.** The first version of this document listed Hofstra as the #2 pick in
the metro — *"Coastal Athletic D1, ~40s gap, Long Island campus with actual space to train, clean
athletic and academic fit."* That rested on a 14:32 outdoor 5000. Hofstra then **won the CAA
championship with a top seven of 23:02–24:45**, and his projection lands roughly **82 seconds
outside** the scoring seven — walk-on territory by the same rule that cut Furman and Lewis. The
14:32 was a floor set by whichever athlete happened to race the outdoor 5000, not a measure of the
squad. **Recommendation withdrawn; Hofstra moves to the cut list.**

**Downgraded: Wagner.** Also previously in the ideal band ("Staten Island, ~40s gap, easy
admission, D1. Underrated."). Their front two ran 25:55 and 26:05, which is respectable, and he
would be their 3rd man — but their 4th runner is at 28:59 and the 1-through-7 spread is **360
seconds**. There is no pack behind the top two to train with. It sits at **Verify** pending a
second race, not at Target.

**Downgraded: NYU — too good, not too thin.** The old note called it a borderline keep at "~75–80
seconds off the #1." They won the UAA with a seven spanning 24:50–25:32, a **42 second spread**, and
he would be about 35 seconds outside it. That is Deep, not Target: he would be a development
runner rather than a scorer. Because D3 has no scholarship stakes the downside of aiming here is
low, but the 9% admit rate is the real obstacle.

**Also downgraded: Monmouth**, from unknown to **Deep** — about 21 seconds outside their scoring
seven, with a 94 second spread that leaves room to move up.

**Iona's cut is now confirmed in the most emphatic way available.** At the MAAC championship all
seven Iona runners crossed **within 0.8 seconds of each other** in a deliberate pack finish, 114
seconds ahead of his projection. When a team can do that, there is no back end to slot into.

**Net effect: three target-tier schools in a 34-school metro** — Fordham, Fairfield and Seton Hall,
and Seton Hall's rating still rests on track marks rather than cross country results. This is the
weakest of the three metros and the cross country data made that clearer, not less clear.

## 3. How to read the numbers below

| Column | What it means |
|---|---|
| **XC slot** | where his projection would have finished inside their top seven, averaged over every 2025 race on file. 1 = ahead of their #1. |
| **vs their 7th** | seconds between his projection and their 7th man. `+35s` = 35 seconds *outside* the seven; `−12s` = 12 seconds *inside* it. Blank where fewer than seven of their runners finished. |
| **1–7 spread** | seconds from their #1 to their #7 — the most course-independent number here, because it compares a team only to itself. Wide = a soft back end to slot into. Tight = no room (see Iona, at 0.8 seconds). |
| **Tier** | Target = clean 4th–9th man fit · Deep = just outside the travel squad · Verify = no usable cross country data yet · Caution = he arrives at or ahead of their #1 |
| **Net cost/yr** | federal average net price after grant aid, from the College Scorecard — **not** sticker price. Out-of-state rates are used at public schools, since he is a South Carolina resident. |
| **CS** | ✅ with a percentage = share of that school's bachelor's degrees awarded in computer science, from federal completion data. `❌ none` means the federal file shows no CS degrees awarded — usually a real absence, occasionally CS filed under mathematics. |

**Most of this metro is at Verify**, because 25 of the 34 schools still have no cross country
results on file at all. Those tiers are placeholders, not judgements.

## 4. Master list

Miles = approximate driving distance from Midtown Manhattan. School names link to a full detail
page with per-race results, a map of every meet they attended last year, cost and admissions
detail.

### Division 1

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Fairfield](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fairfield)** | Fairfield CT | 50 | MAAC | ✅ 2.9% | 1260–1390 | 33% | $48,095 | 3.5 | −84s | 59s | Target |
| **[Fordham](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fordham)** | Bronx NY | 8 | Atlantic 10 | ✅ 4.6% | 1320–1480 | 59% | $44,338 | 6 | −12s | 95s | Target |
| **[Seton Hall](https://timhibbard.github.io/xc-cs-college-board/school.html?s=seton-hall)** | South Orange NJ | 18 | Big East | ✅ 2.4% | 1220–1390 | 73% | $31,446 | — | — | — | Target |
| **[Monmouth](https://timhibbard.github.io/xc-cs-college-board/school.html?s=monmouth)** | W. Long Branch NJ | 45 | Coastal | ✅ 3.2% | 1140–1310 | 89% | $30,988 | 8 | +21s | 94s | Deep |
| **[Army West Point](https://timhibbard.github.io/xc-cs-college-board/school.html?s=army-west-point)** | West Point NY | 50 | Patriot | ✅ 5.9% | 1200–1430 | 12% | — | — | — | — | Verify |
| **[NJIT](https://timhibbard.github.io/xc-cs-college-board/school.html?s=njit)** | Newark NJ | 12 | America East | ✅ 33.0% | 1210–1460 | 65% | $16,504 | — | — | — | Verify |
| **[Wagner](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wagner)** | Staten Island NY | 12 | NEC | ✅ 3.8% | 1190–1290 | 88% | $28,241 | 3 | — | 360s | Verify |
| **[Fairleigh Dickinson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fairleigh-dickinson)** | Teaneck NJ | 12 | NEC | ✅ 2.0% | not reported | 91% | $15,404 | 1 | −143s | 128s | Caution |
| **[LIU](https://timhibbard.github.io/xc-cs-college-board/school.html?s=liu)** | Brooklyn NY | 5 | NEC | ✅ 3.3% | 1110–1350 | 86% | $33,062 | 1 | — | 143s | Caution |
| **[Manhattan](https://timhibbard.github.io/xc-cs-college-board/school.html?s=manhattan)** | Bronx NY | 10 | MAAC | ✅ 6.1% | 1180–1358 | 79% | $27,256 | 2 | — | 112s | Caution |
| **[Sacred Heart](https://timhibbard.github.io/xc-cs-college-board/school.html?s=sacred-heart)** | Fairfield CT | 52 | NEC | ✅ 1.3% | not reported | 65% | $46,174 | — | — | — | Caution |
| **[Saint Peter's](https://timhibbard.github.io/xc-cs-college-board/school.html?s=saint-peter-s)** | Jersey City NJ | 5 | MAAC | ✅ 6.9% | not reported | 90% | $12,199 | 2 | −205s | 212s | Caution |

> **Army note:** requires a congressional nomination and carries a **5-year active-duty service
> obligation** after graduation. No tuition, excellent CS, a real distance program — but a
> fundamentally different life decision, not just a college choice. The federal file reports no net
> price because students do not pay one.
>
> **Sacred Heart** plots at 52 miles, just outside the circle. Kept as a boundary case.

### Division 2 (scholarship money exists)

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Adelphi](https://timhibbard.github.io/xc-cs-college-board/school.html?s=adelphi)** | Garden City NY | 25 | NE10 | ✅ 5.8% | 1120–1340 | 66% | $30,783 | — | — | — | Verify |
| **[Mercy University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mercy-university)** | Dobbs Ferry NY | 25 | ECC | ✅ 3.9% | not reported | 86% | $14,072 | — | — | — | Verify |
| **[Molloy](https://timhibbard.github.io/xc-cs-college-board/school.html?s=molloy)** | Rockville Centre NY | 25 | ECC | ✅ 0.7% | 1088–1290 | 82% | $24,347 | — | — | — | Verify |
| **[NYIT](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nyit)** | Old Westbury NY | 25 | ECC | ✅ 23.9% | 1190–1420 | 81% | $22,443 | — | — | — | Verify |
| **[Pace](https://timhibbard.github.io/xc-cs-college-board/school.html?s=pace)** | Pleasantville NY | 30 | NE10 | ✅ 7.3% | 1180–1340 | 76% | $30,892 | — | — | — | Verify |
| **[Queens College (CUNY)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=queens-college-cuny)** | Queens NY | 10 | ECC | ✅ 10.7% | 1010–1290 | 64% | $4,195 | — | — | — | Verify |
| **[St. Thomas Aquinas](https://timhibbard.github.io/xc-cs-college-board/school.html?s=st-thomas-aquinas)** | Sparkill NY | 20 | CACC | ✅ 3.6% | 880–1085 | 93% | $19,994 | — | — | — | Verify |

**NYIT is the standout on paper** — 23.9% of its bachelor's degrees are in computer science, it is
D2 so partial athletic aid exists, and admission is 81%. Confirm they still sponsor men's cross
country before spending time on it.

### Division 3 (no athletic scholarships)

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[NYU](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nyu)** | Manhattan NY | 0 | UAA | ✅ 10.1% | 1480–1560 | 9% | $37,050 | 8 | +35s | 42s | Deep |
| **[Baruch College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=baruch-college)** | Manhattan NY | 5 | CUNYAC | ✅ 9.6% | 1100–1400 | 48% | $3,033 | — | — | — | Verify |
| **[Drew University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=drew-university)** | Madison NJ | 30 | Landmark | ✅ 5.6% | 1103–1338 | 68% | $24,280 | — | — | — | Verify |
| **[Farmingdale State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=farmingdale-state)** | Farmingdale NY | 35 | Skyline | ✅ 9.4% | 1040–1240 | 63% | $10,867 | — | — | — | Verify |
| **[Kean University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kean-university)** | Union NJ | 20 | NJAC | ✅ 5.6% | 930–1150 | 76% | $12,447 | — | — | — | Verify |
| **[Manhattanville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=manhattanville)** | Purchase NY | 30 | Skyline | ✅ 1.2% | not reported | 87% | $20,991 | — | — | — | Verify |
| **[Merchant Marine Acad.](https://timhibbard.github.io/xc-cs-college-board/school.html?s=merchant-marine-acad)** | Kings Point NY | 20 | Skyline | ❌ none | 1110–1300 | 34% | $6,174 | — | — | — | Verify |
| **[Montclair State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=montclair-state)** | Montclair NJ | 15 | NJAC | ✅ 4.5% | 910–1210 | 88% | $15,566 | — | — | — | Verify |
| **[Mount Saint Vincent](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mount-saint-vincent)** | Bronx NY | 12 | Skyline | ❌ none | 1011–1178 | 85% | $21,696 | — | — | — | Verify |
| **[Ramapo College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=ramapo-college)** | Mahwah NJ | 25 | NJAC | ✅ 6.5% | 1130–1300 | 71% | $18,173 | — | — | — | Verify |
| **[St. Joseph's Univ NY](https://timhibbard.github.io/xc-cs-college-board/school.html?s=st-joseph-s-univ-ny)** | Brooklyn NY | 10 | Skyline | ✅ 4.9% | 1110–1270 | 72% | $19,035 | — | — | — | Verify |
| **[Stevens Institute](https://timhibbard.github.io/xc-cs-college-board/school.html?s=stevens-institute)** | Hoboken NJ | 3 | MAC | ✅ 21.2% | 1380–1505 | 48% | $41,346 | — | — | — | Verify |
| **[SUNY Purchase](https://timhibbard.github.io/xc-cs-college-board/school.html?s=suny-purchase)** | Purchase NY | 30 | Skyline | ❌ none | 1185–1380 | 74% | $18,913 | — | — | — | Verify |
| **[William Paterson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=william-paterson)** | Wayne NJ | 20 | NJAC | ✅ 3.8% | not reported | 90% | $18,745 | — | — | — | Verify |
| **[Yeshiva University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=yeshiva-university)** | Manhattan NY | 5 | Skyline | ✅ 3.3% | 1340–1510 | 56% | $49,965 | — | — | — | Verify |

> **SUNY Purchase's `❌ none` is a data artifact worth naming.** The federal completion file counts
> only degrees filed under the computer science family; a CS program housed inside a mathematics
> department reads as zero. Purchase does teach computer science. Merchant Marine and Mount Saint
> Vincent look like genuine absences — confirm before ruling either in.

## 5. Schools removed — he would be a walk-on

| School | Div | Conf. | Location | XC slot | vs their 7th | 1–7 spread | Why removed |
|---|---|---|---|---|---|---|---|
| **[Hofstra](https://timhibbard.github.io/xc-cs-college-board/school.html?s=hofstra)** | D1 | Coastal | Hempstead NY | 8 | +82s | 104s | Cut on cross country data, reversing an earlier recommendation. An outdoor 5000 of 14:32 suggested a clean 40 second gap and this document called it one of the best fits in the metro. They then won the CAA championship with a top seven of 23:02–24:45 — he would be roughly 82 seconds outside the scoring seven, which is walk-on territory by the same rule that cut Furman and Lewis. The team best 5000 was a floor, not a measure of the squad. |
| **[Columbia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=columbia)** | D1 | Ivy | New York NY | — | — | — | 5000 13:43, 3000 8:30, 10K 29:09. Elite — and one of the best CS departments in the country, which is what makes this cut expensive. |
| **[Iona](https://timhibbard.github.io/xc-cs-college-board/school.html?s=iona)** | D1 | MAAC | New Rochelle NY | 8 | +114s | 1s | 5000 14:03, 10K 29:02, 1500 3:38 — a national cross country program, 20 miles out. Cross country confirms it emphatically: at the MAAC championship all seven runners crossed within 0.8 seconds of each other in a deliberate pack finish, 114 seconds ahead of his projection. |
| **[Princeton](https://timhibbard.github.io/xc-cs-college-board/school.html?s=princeton)** | D1 | Ivy | Princeton NJ | — | — | — | Elite Ivy distance squad at ~50 miles. |
| **[St. John's](https://timhibbard.github.io/xc-cs-college-board/school.html?s=st-john-s)** | D1 | Big East | Queens NY | — | — | — | Nationally strong Big East distance program. |
| **[Rutgers](https://timhibbard.github.io/xc-cs-college-board/school.html?s=rutgers)** | D1 | Big Ten | New Brunswick NJ | — | — | — | Big Ten; out of range. |

This is a real loss on the CS side — Columbia and Princeton are two of the best computer science
departments in the country. They return if a walk-on or redshirt path ever becomes acceptable.

## 6. Tiering

**Target — concentrate effort here.** Fordham · Fairfield · Seton Hall

**Deep — just outside the travel squad.** Monmouth · NYU

**Caution — he arrives at or ahead of their #1.** Manhattan · Saint Peter's · LIU · Fairleigh
Dickinson · Sacred Heart

**Verify — no usable cross country data yet (24 schools).** Wagner · NJIT · Army West Point · all
seven D2 schools · fourteen of the fifteen D3 schools

**Cut on results.** Hofstra · Columbia · Iona · Princeton · St. John's · Rutgers

Thirty-four schools, **three of them target tier**, and 24 still at Verify. The ratio is
worse than Greenville's and the unresolved fraction is much larger, which is the main reason this
metro is second priority.

## 7. Ones worth real effort

1. **[Fordham](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fordham)** — still
   the best fit in the metro, and now confirmed on cross country rather than inferred: **6th man in
   the Atlantic 10 championship seven**, 12 seconds inside it, against a 95 second 1-through-7
   spread. They train at **Van Cortlandt Park**, the most historic cross country course in America,
   next to campus — which answers the "where do you actually run in New York" question better than
   anyone. The problem is money: **$44,338 net**, among the highest on the board.
2. **[Fairfield](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fairfield)** — the
   strongest genuinely new find, and it comes with a caveat. **6th man at the MAAC championship**
   against a tight 59 second spread, which is a good read. At the Northeast regional the squad came
   apart (141 second spread, 33rd in the field) and he would have been their #1. The two races
   disagree; the MAAC result is the better guide to a normal week. Also note the admit rate is
   **33%**, not the ~57% the first version of this document estimated — Fairfield is meaningfully
   more selective than assumed, and at **$48,095 net** it is the most expensive school in this
   metro.
3. **[Seton Hall](https://timhibbard.github.io/xc-cs-college-board/school.html?s=seton-hall)** —
   Big East D1, 18 miles, **$31,446 net**, 73% accept. Their distance squad is weaker than the
   conference name suggests, which works in his favor. **The one target-tier rating in this metro
   still resting on track marks alone** — get their cross country results before treating it as
   settled.
4. **[NJIT](https://timhibbard.github.io/xc-cs-college-board/school.html?s=njit)** — **33.0% of its
   bachelor's degrees are in computer science**, the highest share on the entire 78-school board,
   it is D1, and at **$16,504 net** it is a third the cost of Fordham. If the running fits, this is
   the best value in the metro by a wide margin. Everything hinges on roster times that do not
   exist yet — this is the single highest-value data gap in this document.
5. **[Stevens Institute](https://timhibbard.github.io/xc-cs-college-board/school.html?s=stevens-institute)**
   — the strongest CS on the D3 list (21.2% of degrees), Hoboken, three miles out, no
   athletic-scholarship pressure. $41,346 net and a 48% admit. Also needs roster times.

**NYU and Monmouth: too good, not too thin.** Both are Deep rather than Target, and both are still
worth an email. NYU's 42 second pack is elite for D3 and he would be 35 seconds off it; Monmouth's
94 second spread at 21 seconds outside is one good freshman year from a travel spot. Neither is a
place he would score as a freshman, and both are places he would improve.

## 8. NYC-specific considerations

**Cost of living is the dominant variable, and the federal net prices make it concrete.** The
three most attractive private schools here — Fairfield ($48,095), Fordham ($44,338) and Stevens
($41,346) — are three to twelve times the net price of the public and CUNY options: **Baruch at
$3,033, Queens College at $4,195, Merchant Marine at $6,174, Farmingdale at $10,867, Saint Peter's
at $12,199, Kean at $12,447**. Note that these are federal averages across all enrolled students,
not a quote for him, and that the New York and New Jersey publics will charge **out-of-state**
tuition coming from South Carolina — the net figures above already reflect the average student, so
treat them as a ranking tool and get real estimates from the schools that survive.

**Training terrain is a genuine question to raise with coaches.** Ask specifically where the team
does long runs and workouts. Good answers: Van Cortlandt Park (Fordham, Manhattan), Central Park,
the Rockefeller State Park carriage trails, Bear Mountain for hills, Long Island's parks. Bad
answer: a hesitation, or "we do a lot on the track." Each school's detail page maps every meet they
attended last year, which shows how far and how often they actually travel.

**Three states, three sets of in-state tuition.** NJ publics (Montclair, Kean, Ramapo, William
Paterson, NJIT) and NY publics (the CUNYs, Queens College, SUNY Purchase, Farmingdale) all charge
out-of-state rates coming from South Carolina.

## 9. To-dos, priority order

1. **Get cross country results for NJIT, Stevens, Seton Hall and Army.** Four plausible fits with
   no depth data, and NJIT and Stevens are the two best CS options in the metro. NJIT is first —
   it is the highest-CS-share school on the entire board at a fraction of Fordham's cost.
2. **Get a second race for Fairfield and Wagner.** Fairfield's two races disagree by three places,
   and Wagner's single race showed a 360 second spread that one result cannot confirm.
3. **Pull the D2 and D3 conference championship results** — ECC, NE10, CACC, NJAC, Skyline, CUNYAC,
   Landmark, MAC. That single sweep would resolve most of the 26 Verify-tier schools at once.
4. **Calibrate the northeastern courses.** The NEC, UAA, Big East, MAAC and CAA courses in this
   dataset have no cross-checking team on a calibrated course, so their times cannot yet be put on
   a common scale — which matters most for Fairfield, whose two reads disagree.
5. Confirm NYIT still sponsors men's cross country, and confirm the computer science situation at
   SUNY Purchase, Merchant Marine and Mount Saint Vincent, where the federal file shows no CS
   degrees.
6. Verify SAT figures for Fairleigh Dickinson, Sacred Heart, Saint Peter's, Mercy, Manhattanville
   and William Paterson, which report no SAT range in the federal file.
7. Ask each coach the CS-lab-conflict question (see `greenville-sc.md` §9).
