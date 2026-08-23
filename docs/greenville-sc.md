# College Search — Greenville SC (250 mile radius)

XC/Track + Computer Science. Last updated 2026-08-22 (v5 — radius widened to 250 miles, candidate list rebuilt)

> **The radius went from 200 to 250 miles, and the list went from 27 schools to 82 — but almost
> none of that growth came from the extra fifty miles. It came from admitting the original list
> was incomplete.** Rebuilding the candidate list conference by conference from each conference's
> own men's-sponsored-sports tables found **56 schools**, and **41 of them were inside the original
> 200-mile ring the whole time** — including one 25 driving miles from home. Every one enters at
> Verify with full federal cost and admissions data and no cross country data, so the ranked
> analysis below is unchanged. Two other corrections and one new cut are in §2. See §2a first.

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
2025 — it agreed within about 7 seconds.

The track 5000 of **15:20 is anchored on the 3200, not the 1600, deliberately.** Solving Riegel's
fatigue exponent on his own marks gives **1.12** from 1600 → 3200 against a textbook **1.06**, which
says he is speed-leaning: the 1600 flatters his 5K and a 1600-anchored projection would put him
roughly twenty seconds faster than he should be treated as. The full derivation, with every
exponent solved, is in `../methodology.html` §1a.

**The framing rule, unchanged.** For this projection, **arriving as a team's 5th through 9th man
is the healthy target** — training partners ahead of him and a path to scoring by junior year.
Being *ahead* of a team's #1 means the program is thin, not that he is a star. Distance runners
develop in packs.

## 2. Read this first

### 2a. The list was incomplete, and that is the biggest finding in this document

Versions 1–4 of this document, and the README that went with them, claimed to list **every** school
inside the radius that sponsors men's cross country. That claim was false. The candidate list had
been assembled from general knowledge and then each entry verified individually — which validates
what is on the list and says nothing about what is missing.

The rebuild works the other way round: for every NCAA D1, D2 and D3 conference with a member inside
250 miles, read that conference's own men's-sponsored-sports table and take every school in range.
That found **56 additions**:

| | Added | Of which inside the old 200 miles |
|---|---|---|
| Division 1 | 12 | 6 |
| Division 2 | **35** | 27 |
| Division 3 | 7 | 6 |
| NAIA / NCCAA | 2 | 2 |
| **Total** | **56** | **41** |

**The Division 2 number is the one that matters.** D2 is where partial athletic scholarships live,
and this document previously listed **seven** D2 programs in range. There are **forty-two**. The
closest omission, **Southern Wesleyan**, is 25 driving miles from home. **Bob Jones** is three.

Every addition enters at **Verify — meaning unmeasured, not borderline.** None has a cross country
result or an outdoor 5000 on file, so none can be ranked yet, and none of §6's or §7's conclusions
moves. What changed is the size of the unexplored space: **60 of the 82 schools on this list have no
running data at all.**

Two limits worth stating. The rebuild inherits the conferences' own errors — a stale sponsored-sports
table is wrong in both directions, and no addition's sponsorship was re-confirmed on the school's
own athletics site. And **NAIA and NCCAA coverage is still incomplete**: only Bob Jones (NCCAA) and
Montreat (NAIA) are here, while at least Toccoa Falls, Truett McConnell, Brenau, Columbia
International, Columbia College SC, Milligan, Johnson University, Reinhardt, Voorhees, Tennessee
Wesleyan, Morris College, Bryan College, Bluefield University, Point University, Life University,
Spartanburg Methodist and Warren Wilson are not. NAIA allows **12 scholarships** for men's XC and
track with looser eligibility rules, so that gap sits exactly where money is easiest to find.

### 2b. Georgia State has no men's cross country team

It sat at **Verify** on every earlier version of this document at 16.2% CS degrees, which made it
look like an attractive unmeasured D1. Georgia State sponsors **no men's cross country and no men's
track and field** — the distance programs are women's only. There was never a team there to verify.
This is the failure mode of a tier that means "no data yet": it reads as a program awaiting
measurement rather than one that does not exist. It is kept on the map rather than deleted so the
correction stays visible. If an error of this kind was sitting in a 27-school list, assume there
are others in an 82-school one.

### 2c. Four rows on the cut list said "out of range" and were not

Tennessee (Knoxville, ~145 mi), Georgia (Athens, ~140), Wake Forest (Winston-Salem, ~175) and South
Carolina (Columbia, ~105 — the in-state flagship) all carried `why: "Out of range."` They were never
out of a 200-mile range, let alone a 250-mile one. They are **cut on level, not on distance and not
on measurement**: no 2025 cross country times have been transcribed for any of them. Those rows now
say so. Treat all four as cuts by reputation, reopenable if the numbers ever come in.

**Two genuinely new cuts came in with the wider radius:** **UNC Chapel Hill** (~250 mi) and **Duke**
(~255, so genuinely borderline). Both are cut on level; Duke is also cut on admissions at a 6%
rate, which means the running is not the binding constraint there.

### 2d. What the cross country data changed (unchanged from v4)

**Withdrawn: Lenoir-Rhyne is no longer a top pick.** Version 3 listed it alongside Catawba and
Anderson as one of the three D2 schools "where the actual scholarship dollars are, all with a
healthy gap to the #1." That rested on an 8:47 3000, which turns out to have been a sparse-table
artifact. At the D2 regional their **scoring six ran 33:44 to 39:11** over 10K — a 326 second
spread — and he would arrive as their **#1 by nearly a minute**. It sits at Caution.

**Resolved upward: UNC Charlotte and Emory.** Both were boundary cases and both improved.

- **UNC Charlotte** was kept in v3 with a flag ("~65–75 seconds off their best runner"). At the
  D1 Southeast regional their seven ran **30:18–33:05** over 10K, putting him right at their 7th
  man, 11 seconds outside the scoring seven. A 167 second 1-through-7 spread means the back of
  that squad is soft — which is exactly where a freshman wants to land. **Target**, and it has
  the highest CS degree share of any D1 school on this list at 15.2%.
- **Emory** sat in the caution tier on a 15:06 outdoor 5000 that read as "immediate top-2." That
  was a sparse-table artifact too, in the opposite direction: the UAA championship shows a
  **25:14–26:27 top seven**, so he slots in around **5th man**. **Target.**

**Resolved downward: Appalachian State and Anderson (SC).** Both were listed in the ideal band or
as boundary keeps; both sit at **Deep** — just outside the travel squad rather than inside it.
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
| **Tier** | Target = clean 4th–9th man fit · Deep = just outside the travel squad · Verify = **unmeasured**, no cross country data yet — a placeholder for a lookup nobody has done, not a judgement · Caution = he arrives at or ahead of their #1 |
| **Net cost/yr** | federal average net price after grant aid, from the College Scorecard — **not** sticker price. Out-of-state rates are used at public schools, except at the nine South Carolina publics, where the in-state rate applies. |
| **CS** | ✅ with a percentage = share of that school's bachelor's degrees awarded in computer science, from federal completion data. A low share is not a bad program. |

**Mileage caveat for the 56 additions.** Their `Mi` figures are **estimates**, not looked-up routes:
straight-line distance × 1.18, or × 1.35 in the mountain states (TN, VA, WV, KY), rounded to the
nearest 5. Expect ±15%. That matters only near the line — **Campbell, Savannah State and NC
Central at an estimated 250 could each be over it.**

Eight of the additions carry a **`❌ none` CS reading that needs one catalog check rather than
dismissal**: Brevard, Belmont Abbey, Young Harris, Queens (Charlotte), Allen, Oglethorpe, Emory &
Henry and Lees-McRae all report 0% computing degrees *and* a live mathematics program, which at a
small college is usually CS filed under mathematics. Each of those school pages says so.

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
| **[Campbell](https://timhibbard.github.io/xc-cs-college-board/school.html?s=campbell)** | Buies Creek NC | 250 | CAA | ✅ 6.5% | not reported | 87% | $24,516 | — | — | — | Verify |
| **[Charleston Southern](https://timhibbard.github.io/xc-cs-college-board/school.html?s=charleston-southern)** | Charleston SC | 220 | Big South | ✅ 4.7% | 930–1160 | 96% | $21,666 | — | — | — | Verify |
| **[Chattanooga](https://timhibbard.github.io/xc-cs-college-board/school.html?s=chattanooga)** | Chattanooga TN | 225 | Southern | ✅ 4.2% | 1013–1210 | 81% | $14,265 | — | — | — | Verify |
| **[Coastal Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coastal-carolina)** | Conway SC | 245 | Sun Belt | ✅ 2.5% | 1050–1220 | 75% | $13,966 | — | — | — | Verify |
| **[College of Charleston](https://timhibbard.github.io/xc-cs-college-board/school.html?s=college-of-charleston)** | Charleston SC | 235 | CAA | ✅ 4.1% | 1140–1310 | 60% | $18,960 | — | — | — | Verify |
| **[Kennesaw State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kennesaw-state)** | Kennesaw GA | 125 | CUSA | ✅ 11.1% | 1000–1220 | 69% | $15,048 | — | — | — | Verify |
| **[Mercer](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mercer)** | Macon GA | 185 | Southern | ✅ 4.9% | 1160–1350 | 69% | $23,847 | — | — | — | Verify |
| **[NC A&T](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-aandt)** | Greensboro NC | 200 | CAA | ✅ 8.9% | 1020–1190 | 50% | $10,846 | — | — | — | Verify |
| **[NC Central](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-central)** | Durham NC | 250 | MEAC | ✅ 3.9% | ~1050 avg | 87% | $15,359 | — | — | — | Verify |
| **[Queens (Charlotte)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=queens-charlotte)** | Charlotte NC | 105 | ASUN | ❌ none | 1140–1340 | 62% | $30,857 | — | — | — | Verify |
| **[SC State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=sc-state)** | Orangeburg SC | 150 | MEAC | ✅ 3.8% | not reported | 83% | $18,097 | — | — | — | Verify |
| **[The Citadel](https://timhibbard.github.io/xc-cs-college-board/school.html?s=the-citadel)** | Charleston SC | 235 | Southern | ✅ 4.0% | 1085–1285 | 23% | $20,723 | — | — | — | Verify |
| **[West Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=west-georgia)** | Carrollton GA | 210 | United Athletic | ✅ 2.7% | 950–1140 | 52% | $12,786 | — | — | — | Verify |
| **[Gardner-Webb](https://timhibbard.github.io/xc-cs-college-board/school.html?s=gardner-webb)** | Boiling Springs NC | 60 | Big South | ✅ 1.9% | 975–1198 | 77% | $17,674 | 1 | — | 966s | Caution |
| **[Presbyterian](https://timhibbard.github.io/xc-cs-college-board/school.html?s=presbyterian)** | Clinton SC | 45 | Big South | ✅ 1.4% | 980–1200 | 68% | $20,528 | 1 | −263s | 234s | Caution |
| **[USC Upstate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-upstate)** | Spartanburg SC | 32 | Big South | ✅ 8.3% | 1005–1175 | 67% | $13,557 | 2 | −43s | 82s | Caution |
| **[Western Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=western-carolina)** | Cullowhee NC | 60 | Southern | ✅ 1.3% | 1080–1270 | 82% | $13,315 | 2 | −82s | 105s | Caution |
| **[Winthrop](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winthrop)** | Rock Hill SC | 100 | Big South | ✅ 2.5% | 1010–1220 | 79% | $15,343 | 1 | — | 143s | Caution |
| **[Wofford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wofford)** | Spartanburg SC | 32 | Southern | ✅ 3.6% | 1198–1343 | 52% | $18,732 | 1 | — | 222s | Caution |

### Division 2 (scholarship money exists)

Forty-two programs, thirty-five of them new to this document. Every new one is unmeasured.

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba)** | Salisbury NC | 130 | South Atlantic | ✅ 1.6% | 1030–1300 | 75% | $17,879 | 5.5 | −96s | 133s | Target |
| **[Anderson (SC)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=anderson-sc)** | Anderson SC | 30 | South Atlantic | ✅ 5.0% | 1100–1280 | 55% | $23,544 | 7.5 | +2s | 66s | Deep |
| **[Allen University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=allen-university)** | Columbia SC | 115 | SIAC | ❌ none | not reported | 73% | $10,972 | — | — | — | Verify |
| **[Augusta University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=augusta-university)** | Augusta GA | 115 | Peach Belt | ✅ 15.6% | 970–1140 | 86% | $13,787 | — | — | — | Verify |
| **[Belmont Abbey](https://timhibbard.github.io/xc-cs-college-board/school.html?s=belmont-abbey)** | Belmont NC | 95 | Conference Carolinas | ❌ none | 960–1200 | 75% | $24,639 | — | — | — | Verify |
| **[Benedict](https://timhibbard.github.io/xc-cs-college-board/school.html?s=benedict)** | Columbia SC | 115 | SIAC | ✅ 3.2% | not reported | 96% | $18,250 | — | — | — | Verify |
| **[Bluefield State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=bluefield-state)** | Bluefield WV | 240 | CIAA | ✅ 1.9% | 870–1080 | 97% | $13,684 | — | — | — | Verify |
| **[Claflin](https://timhibbard.github.io/xc-cs-college-board/school.html?s=claflin)** | Orangeburg SC | 150 | CIAA | ✅ 3.3% | not reported | 65% | $17,800 | — | — | — | Verify |
| **[Clark Atlanta](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clark-atlanta)** | Atlanta GA | 165 | SIAC | ✅ 1.9% | not reported | 64% | $37,702 | — | — | — | Verify |
| **[Clayton State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clayton-state)** | Morrow GA | 165 | Peach Belt | ✅ 8.9% | 860–1078 | 68% | $8,365 | — | — | — | Verify |
| **[Coker](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coker)** | Hartsville SC | 160 | South Atlantic | ✅ | not reported | 94% | $20,286 | — | — | — | Verify |
| **[Converse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=converse)** | Spartanburg SC | 35 | Conference Carolinas | ✅ 1.6% | 1010–1250 | 68% | $23,283 | — | — | — | Verify |
| **[Emmanuel (GA)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emmanuel-ga)** | Franklin Springs GA | 70 | Conference Carolinas | ✅ 1.7% | not reported | 74% | $20,925 | — | — | — | Verify |
| **[Emory & Henry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory-and-henry)** | Emory VA | 185 | South Atlantic | ❌ none | 1051–1223 | 84% | $19,061 | — | — | — | Verify |
| **[Erskine](https://timhibbard.github.io/xc-cs-college-board/school.html?s=erskine)** | Due West SC | 40 | Conference Carolinas | ✅ 0.7% | not reported | 63% | $16,525 | — | — | — | Verify |
| **[Fayetteville State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fayetteville-state)** | Fayetteville NC | 235 | CIAA | ✅ 3.3% | 890–1090 | 82% | $7,892 | — | — | — | Verify |
| **[Fort Valley State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fort-valley-state)** | Fort Valley GA | 215 | SIAC | ✅ 4.6% | 930–1070 | 66% | $10,338 | — | — | — | Verify |
| **[Francis Marion](https://timhibbard.github.io/xc-cs-college-board/school.html?s=francis-marion)** | Florence SC | 190 | Conference Carolinas | ✅ 2.4% | 870–1115 | 86% | $11,386 | — | — | — | Verify |
| **[Georgia College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-college)** | Milledgeville GA | 155 | Peach Belt | ✅ 6.2% | 1070–1230 | 78% | $20,686 | — | — | — | Verify |
| **[Johnson C. Smith](https://timhibbard.github.io/xc-cs-college-board/school.html?s=johnson-c-smith)** | Charlotte NC | 105 | CIAA | ✅ 10.4% | not reported | 45% | $20,894 | — | — | — | Verify |
| **[Lee University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lee-university)** | Cleveland TN | 190 | Gulf South | ✅ 2.0% | 1040–1230 | 71% | $18,878 | — | — | — | Verify |
| **[Lees-McRae](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lees-mcrae)** | Banner Elk NC | 130 | Conference Carolinas | ❌ none | not reported | 77% | $28,340 | — | — | — | Verify |
| **[Lincoln Memorial](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lincoln-memorial)** | Harrogate TN | 190 | South Atlantic | ✅ 1.0% | 1000–1210 | 63% | $20,406 | — | — | — | Verify |
| **[Livingstone](https://timhibbard.github.io/xc-cs-college-board/school.html?s=livingstone)** | Salisbury NC | 145 | CIAA | ✅ 3.4% | not reported | 59% | $13,479 | — | — | — | Verify |
| **[Mars Hill](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mars-hill)** | Mars Hill NC | 80 | South Atlantic | ✅ 0.4% | not reported | 68% | $19,910 | — | — | — | Verify |
| **[Morehouse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=morehouse)** | Atlanta GA | 165 | SIAC | ✅ 3.8% | ~1090 avg | 44% | $39,013 | — | — | — | Verify |
| **[Newberry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=newberry)** | Newberry SC | 70 | South Atlantic | ✅ 1.5% | not reported | 90% | $21,656 | — | — | — | Verify |
| **[North Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=north-georgia)** | Dahlonega GA | 110 | Peach Belt | ✅ 9.2% | 980–1210 | 68% | $9,823 | — | — | — | Verify |
| **[Savannah State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=savannah-state)** | Savannah GA | 250 | SIAC | ✅ 0.9% | not reported | not reported | $8,172 | — | — | — | Verify |
| **[Shorter](https://timhibbard.github.io/xc-cs-college-board/school.html?s=shorter)** | Rome GA | 195 | Conference Carolinas | ✅ 3.4% | 1040–1200 | 96% | $16,646 | — | — | — | Verify |
| **[Southern Wesleyan](https://timhibbard.github.io/xc-cs-college-board/school.html?s=southern-wesleyan)** | Central SC | 25 | Conference Carolinas | ✅ 2.7% | 1040–1210 | 100% | $15,464 | — | — | — | Verify |
| **[Tusculum](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tusculum)** | Greeneville TN | 125 | South Atlantic | ✅ 0.9% | not reported | 72% | $21,131 | — | — | — | Verify |
| **[UNC Pembroke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-pembroke)** | Pembroke NC | 215 | Conference Carolinas | ✅ 4.8% | 970–1200 | 93% | $10,260 | — | — | — | Verify |
| **[USC Aiken](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-aiken)** | Aiken SC | 110 | Peach Belt | ✅ 6.8% | 980–1220 | 79% | $11,641 | — | — | — | Verify |
| **[UVA Wise](https://timhibbard.github.io/xc-cs-college-board/school.html?s=uva-wise)** | Wise VA | 200 | South Atlantic | ✅ 2.3% | 945–1120 | 29% | $9,210 | — | — | — | Verify |
| **[Winston-Salem State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winston-salem-state)** | Winston-Salem NC | 175 | CIAA | ✅ 1.4% | 830–1020 | 78% | $13,479 | — | — | — | Verify |
| **[Young Harris](https://timhibbard.github.io/xc-cs-college-board/school.html?s=young-harris)** | Young Harris GA | 95 | Conference Carolinas | ❌ none | not reported | 63% | $22,034 | — | — | — | Verify |
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
| **[Brevard College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=brevard-college)** | Brevard NC | 40 | USA South | ❌ none | 870–1220 | 42% | $23,509 | — | — | — | Verify |
| **[Covenant College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=covenant-college)** | Lookout Mtn GA | 200 | Collegiate Conf. of the South | ✅ 1.4% | 1160–1380 | 87% | $26,265 | — | — | — | Verify |
| **[LaGrange](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lagrange)** | LaGrange GA | 230 | Collegiate Conf. of the South | ✅ | not reported | 62% | $20,875 | — | — | — | Verify |
| **[Maryville College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=maryville-college)** | Maryville TN | 145 | Southern Athletic | ✅ 2.8% | not reported | 61% | $19,360 | — | — | — | Verify |
| **[Methodist](https://timhibbard.github.io/xc-cs-college-board/school.html?s=methodist)** | Fayetteville NC | 235 | USA South | ✅ 4.4% | 1080–1250 | 75% | $24,704 | — | — | — | Verify |
| **[Oglethorpe](https://timhibbard.github.io/xc-cs-college-board/school.html?s=oglethorpe)** | Atlanta GA | 155 | Southern Athletic | ❌ none | 1090–1310 | 88% | $19,509 | — | — | — | Verify |
| **[Pfeiffer](https://timhibbard.github.io/xc-cs-college-board/school.html?s=pfeiffer)** | Misenheimer NC | 150 | USA South | ✅ 5.5% | not reported | 96% | $19,076 | — | — | — | Verify |
| **[Piedmont University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=piedmont-university)** | Demorest GA | 100 | USA South | ⚠️ thin | 1038–1245 | 93% | $20,599 | — | — | — | Verify |
| **[Berry College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=berry-college)** | Rome GA | 150 | SAA | ✅ 5.8% | 1125–1330 | 64% | $22,320 | — | — | — | Caution |
| **[Guilford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=guilford)** | Greensboro NC | 180 | ODAC | ✅ 7.2% | 1120–1260 | 80% | $22,270 | — | — | — | Caution |

### NAIA and NCCAA

Neither is NCAA, which changes the rules rather than the running. NAIA allows **12 scholarships**
for men's XC and track with looser eligibility rules; NCCAA has no NCAA eligibility clock and no
NCAA championship path. Coverage here is known to be incomplete (§2a).

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | Tier |
|---|---|---|---|---|---|---|---|---|
| **[Montreat](https://timhibbard.github.io/xc-cs-college-board/school.html?s=montreat)** | Montreat NC | 70 | Appalachian Athletic (NAIA) | ✅ 13.9% | not reported | 69% | $27,061 | Verify |
| **[Bob Jones](https://timhibbard.github.io/xc-cs-college-board/school.html?s=bob-jones)** | Greenville SC | 3 | NCCAA D2 South | ✅ 3.9% | not reported | not reported | $16,641 | Verify |

**Bob Jones is three miles from home** and does sponsor men's cross country. Montreat's **13.9% CS
degree share** is the third highest on this entire list. Both are unmeasured on running.

## 5. Schools removed — he would be a walk-on

| School | Div | Conf. | Location | XC slot | vs their 7th | 1–7 spread | Why removed |
|---|---|---|---|---|---|---|---|
| **[Furman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=furman)** | D1 | Southern | Greenville SC | 8 | +79s | 42s | Team best 5000 13:40; nationally elite, ~1:40 gap. Zero miles away with a verified CS degree, which is what makes the cut hurt. Cross country confirms it: they won the Southern Conference with seven runners inside 42 seconds (24:15–24:57) and were 7th at the regional. He would be 70 to 87 seconds outside the scoring seven. |
| **[Clemson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clemson)** | D1 | ACC | Clemson SC | — | — | — | ACC program 32 miles away. Their 1500 best of 3:43 implies a ~14:15 5K runner even though the outdoor 5000 table reads 14:36 — the sparse-table problem in the direction that flatters them. |
| **[Georgia Tech](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-tech)** | D1 | ACC | Atlanta GA | — | — | — | 5000 13:41, 10K 29:45. Also the hardest CS admit on the list — GT computing is far more selective than the university's overall rate suggests. |
| **[Wingate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wingate)** | D2 | South Atlantic | Wingate NC | 8 | +34s | 70s | 5000 13:37, 10K 29:20 — the strongest D2 distance program in the region. Cross country is mixed but does not rescue it: at the D2 regional their seven ran 30:48–31:58, about 56 seconds clear of his projection. Kept as a cut on the regional evidence, and this is the school the sign-error correction briefly promoted. |
| **[South Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=south-carolina)** | D1 | SEC | Columbia SC | — | — | — | SEC program, ~105 mi — the in-state flagship. Cut on **level**, not distance: the earlier "out of range" on this row was simply wrong (§2c). No 2025 times transcribed. |
| **[Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia)** | D1 | SEC | Athens GA | — | — | — | SEC program, ~140 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[Tennessee](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tennessee)** | D1 | SEC | Knoxville TN | — | — | — | SEC program, ~145 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[Wake Forest](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wake-forest)** | D1 | ACC | Winston-Salem NC | — | — | — | ACC program, ~175 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[UNC Chapel Hill](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-chapel-hill)** | D1 | ACC | Chapel Hill NC | — | — | — | **New at 250 miles** (~250 mi). ACC program with one of the strongest public-university CS departments in the country and a 15% admit rate. Cut on level: their scoring seven is a national-championship-qualifying group. A cut by reputation, not by measurement. |
| **[Duke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=duke)** | D1 | ACC | Durham NC | — | — | — | **New at 250 miles** (~255 mi, so genuinely borderline). ACC program, elite CS, 6% admit. Cut on level and also on admissions — the running is not the binding constraint here. |

If a walk-on or redshirt path ever becomes acceptable, Furman and Clemson go straight back to the
top of the list on every non-athletic axis. **Georgia State is not on this list** — there is no
men's program to be removed from (§2b).

## 6. Tiering

**Target — clean development band, concentrate effort here.** UNC Asheville · Davidson · UNC
Greensboro · ETSU · Elon · High Point · UNC Charlotte · Catawba (D2) · Emory (D3)

**Deep — just outside the travel squad.** Anderson (SC) · Appalachian State

**Verify — unmeasured, not borderline (58 schools).** Kennesaw State · Piedmont University · and the
56 additions from §2a

**Caution — he arrives at or ahead of their #1.** USC Upstate · Western Carolina · Wofford ·
Winthrop · Presbyterian · Gardner-Webb · North Greenville · Lander · Lenoir-Rhyne · Carson-Newman ·
King University · Berry College · Guilford

**Cut on results or on level.** Furman · Clemson · Georgia Tech · Wingate · South Carolina ·
Georgia · Tennessee · Wake Forest · UNC Chapel Hill · Duke

Eighty-two schools, **nine of them target tier** — still by far the strongest of the three metros
and still the reason this list is the primary one. But note what the ratio now means: **58 schools
are unmeasured**, so nine-of-eighty-two is not a worse hit rate than v4's nine-of-twenty-seven, it
is the same nine measured against a much larger and mostly unexplored field.

That caution tier still needs care rather than dismissal. Being a team's #1 is fine *if* the coach
is building a class around him — always ask who else they are signing. It is bad if he trains
alone for four years. **Wofford is the sharpest version:** strong academics, verified CS, 32 miles,
and a team he would lead on arrival. **Gardner-Webb's 966 second 1-through-7 spread** is the most
extreme number in this document and means there is effectively no distance squad to join.

## 7. Top picks

Unchanged by the radius change, because **none of the 56 additions has a cross country result yet**.
Treat this list as "the best of what has been measured," not "the best available."

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
   cheapest *target-tier* school in this document**, with an 89% accept rate and a 7.4% CS degree
   share. If money is the deciding axis among the measured schools, this is the answer. (Eight
   additions are cheaper still — seven D2 schools and NC A&T at D1 — and every one is unmeasured.)
4. **[UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte)**
   — the upgrade described in §2d. Right at their 7th man with a soft 167 second back end, a real
   CS school (15.2% of degrees), $15,435 net, 80% accept. A large university with multiple
   sections of every CS course, which matters for the lab-conflict problem in §9.
5. **[Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory)** — the other
   upgrade. 5th man in a 74 second UAA pack, elite CS, no athletic money but strong need-based aid
   bringing net cost to $22,585. An **11% admit**, so the coach's pre-read matters as much as it
   does at Davidson.
6. **[Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba)** — the D2
   pick now that Lenoir-Rhyne is withdrawn. 5th man at the regional and, after correcting the 96
   second course offset, about the same at the conference meet. D2 means partial athletic aid
   genuinely exists. $17,879 net. It is now one of forty-two D2 programs in range rather than one
   of seven, which makes it the *best measured* D2 fit rather than the best D2 fit.

Also worth the email, one tier down: **ETSU** and **High Point** are both solid target-tier fits
(ETSU with a soft 171 second middle, High Point confirmed 7th man twice), and **Anderson (SC)** is
30 miles away and within two seconds of their travel squad.

**And the highest-value unmeasured shortlist**, on cost, CS share and proximity rather than on
running: **Southern Wesleyan** (25 mi), **Bob Jones** (3 mi), **Erskine** (40), **Newberry** (70),
**Montreat** (70, 13.9% CS), **North Georgia** ($9,823 net, 9.2% CS), **Augusta** (15.6% CS),
**Clayton State** ($8,365 net, 8.9% CS) and **USC Aiken** (in-state). One conference championship
result covers seven or eight of these at a time.

## 8. Academic and money notes

**Recruitment is an admissions lever at selective schools.** Coaches at Davidson (13%) and Emory
(11%) get supported slots and will run a **pre-read** — send transcript and scores, and admissions
tells the coach informally whether he would get in. This is how running unlocks a school his
stats alone would not. Initiate spring of junior year.

**Where academics are an asset rather than a constraint:** UNC Asheville (92%), Appalachian State
(90%), UNC Greensboro (89%), ETSU (86%), Western Carolina (82%), and most of the D2 list — where
Southern Wesleyan and King University both report a **100%** admit rate. Admission is close to
automatic, so all the leverage shifts to **money**.

**Nine of these schools are South Carolina publics, so the in-state rate applies.** Lander, USC
Upstate, Winthrop, USC Aiken, SC State, Francis Marion, Coastal Carolina, the College of Charleston
and The Citadel are all quoted at in-state tuition in the tables above; every other public school on
the list is quoted out-of-state. USC Aiken ($11,641) and Francis Marion ($11,386) are the cheapest
of the nine, and both are unmeasured D2 programs where partial athletic aid also exists.

**Thirty-five new Division 2 programs changes the money picture more than the running picture.**
D2 is where partial athletic scholarships live, and the cheapest schools on this entire board are
now all D2 additions: **Fayetteville State $7,892, Savannah State $8,172, Clayton State $8,365,
UVA Wise $9,210, North Georgia $9,823**. Those are half the net price of UNC Greensboro and a fifth
of Elon's. Whether any of them is a training environment is completely unknown, which is exactly
what §10 item 1 is for.

**Academic aid often beats athletic aid.** D1 XC/track is a 12.6-scholarship equivalency spread
across a 35–45 man roster — quarter and half rides, not fulls. A strong student stacking merit aid
at UNC Greensboro ($10,965 net), UNC Asheville ($12,250) or Western Carolina ($13,315) can land
well below the net cost of a bigger athletic offer somewhere expensive. **Model net cost, not
scholarship percentage.** The net figures in this document are federal averages across all
students, not a quote for him — treat them as a ranking tool and get real aid estimates from the
schools that survive.

**The two expensive target-tier schools.** Elon ($41,555 net) and High Point ($38,707) are three
to four times the cost of UNCG for a comparable athletic fit. They are on the list because the
running works; rank them last on money unless something specific offsets it. Clark Atlanta
($37,702) and Morehouse ($39,013) are in the same band among the additions.

## 9. Practical notes

**CS labs collide with 3:00–5:30 practice.** Large schools (UNC Charlotte, App State, Kennesaw
State, Coastal Carolina, College of Charleston) run multiple sections; small ones (Wofford,
Presbyterian, Berry, Piedmont, North Greenville, Catawba, Anderson, and most of the new D2 and D3
additions) may offer a required course in exactly one afternoon slot.
**Ask every coach: "how many of your athletes major in CS or engineering, and how do you handle
lab conflicts?"** This eliminates programs faster than times do.

**Contact rules.** D1 coaches may initiate contact **June 15 after sophomore year**; D2 July 15
after sophomore year; D3 essentially unrestricted. **He may email coaches any time, any age, any
division** — the restriction runs one direction only. NAIA and NCCAA have no equivalent contact
calendar.

**What to put in the email.** Lead with the **8K/10K cross country projection**, not the 1600
time, and say what it is projected from. Coaches think in the distance they recruit for, and the
whole point of this document is that a track 1600 is a poor predictor of where someone lands in a
scoring seven.

**Two special cases among the additions.** **The Citadel** is a military college — the corps of
cadets schedule is a real constraint on both training and a CS course load, not a detail.
**Lees-McRae** sits at about 3,700 feet, the highest campus on this board, which is a genuine
altitude-training advantage.

## 10. To-dos, priority order

1. **Get cross country results for the twelve schools inside 100 miles that have none.**
   This is now the single highest-value action in the entire project. Bob Jones (3 mi), Southern
   Wesleyan (25), Converse (35), Brevard (40), Erskine (40), Newberry (70), Emmanuel GA (70),
   Montreat (70), Mars Hill (80), Belmont Abbey (95), Young Harris (95), Piedmont (100). Most are
   Conference Carolinas or South Atlantic, so **two championship results cover almost all of them.**
2. **Then sweep the rest of the conferences.** Peach Belt, SIAC, CIAA, USA South, Southern Athletic,
   Collegiate Conference of the South, Gulf South and MEAC would resolve most of the remaining 58
   Verify-tier schools — 19 of them sit between 100 and 160 miles. Also Kennesaw State, which
   predates the additions, plus Berry and Guilford, ranked Caution on track marks alone.
3. **Close the NAIA/NCCAA gap** listed in §2a — seventeen named programs, in the division with the
   most scholarships and the loosest eligibility rules.
4. **Email UNC Asheville, Davidson, UNC Greensboro and Emory.** Four target-tier schools, two of
   which need a pre-read that takes months to arrange.
5. **Verify the driving distance for Campbell, Savannah State and NC Central**, all estimated at
   exactly 250 miles and any of which could be outside the ring.
6. **Calibrate more courses.** Only two of the fourteen courses in this dataset have a correction
   applied, because a correction requires at least three cross-checking teams. The Big South,
   Southern and South Atlantic families agree closely; the Peach Belt, Conference Carolinas and
   USA South courses are uncalibrated — and those are now the three most important conferences on
   the list.
7. Confirm a **true BS in Computer Science** (not IT, cybersecurity, or applied AI) at Anderson
   SC, Presbyterian, North Greenville and USC Upstate; resolve **Piedmont**, whose site has been
   unreachable across several attempts; and check the catalogs of the eight additions reporting
   `❌ none` alongside a mathematics program (§3).
8. Confirm each program carries **full men's indoor and outdoor track**, not cross country only.
   Five New York schools turned out to be cross-country-only and **not one has been identified here**,
   which almost certainly means the check is incomplete rather than that the number is zero. Each
   school's detail page maps every meet they attended last year by season, which is a decent first
   check for the eleven schools that have one.
9. Verify SAT figures for the **24 schools reporting no SAT range at all** in the federal file, and
   admit rates for Bob Jones and Savannah State.
