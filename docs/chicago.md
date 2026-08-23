# College Search — Chicago (20 mile radius)

XC/Track + Computer Science. Last updated 2026-08-22

> **Radius changed from 30 miles back to 20.** That is not a cosmetic edit: it removes five
> schools, including **North Central**, the best training environment on the Chicago list, and
> **Purdue Northwest**, which was the metro's only scholarship program. Their data is preserved
> in §5b rather than deleted. **Roosevelt University** enters as the replacement scholarship
> option. §2 has the whole accounting.

Live version, with per-school pages and meet maps:
<https://timhibbard.github.io/xc-cs-college-board/chicago.html>

## 1. Athlete profile

| Event | Current | Projected |
|---|---|---|
| 1600m | 4:21 | ~4:18 |
| 3200m | 9:40 | 9:29 |
| 5K XC | 16:29 | ~15:59 |

Converted: **1500 4:03** · **3000 8:53** · **track 5000 15:20** · **8K XC 26:07** · **10K XC 32:54**

The 8K and 10K projections are what the comparison actually runs on, because college cross
country is raced at 8K (D2, D3, most conference meets) and 10K (D1 regionals and nationals).
The 10K figure is the 8K figure × 1.26; that factor was validated against teams that raced both
distances in 2025 and it agreed within about 7 seconds. The track 5000 of **15:20** is anchored
on the 3200 rather than the 1600 on purpose — solving Riegel's exponent on his own marks gives
1.12 from 1600→3200 against a textbook 1.06, so he is speed-leaning and the 1600 flatters the
5K. Full derivation and caveats: `../methodology.html` §1a.

**Target: a program where he would arrive as roughly their 5th through 9th man.** Ahead of their
#1 is not a good sign — it means the program is thin and he would train alone for four years.

## 2. Read this first: what the 20-mile radius costs, and three findings

**The radius went 20 → 30 → 20, and the round trip was informative.** Widening to 30 miles was
recommended specifically to reach Lewis University, which the roster data then killed. Coming back
to 20 costs five schools:

| School | Mi | Tier it held | Does the loss matter? |
|---|---|---|---|
| **North Central** | 28 | Deep | **Yes — the real loss.** D3 national-championship program, 7th man 25:34 (CCIW) and 25:46 (D3 Midwest regional), so roughly 10 seconds outside the scoring seven. Best *training environment* on the list. |
| **Purdue Northwest** | 25 | Caution | **Yes, on mechanism not merit.** The only Division 2 program in range, therefore the only place partial athletic money existed. |
| **Wheaton College** | 25 | Caution | No. Interesting but settled: he arrives near the front of that squad. |
| **Benedictine (IL)** | 25 | Caution | No. He would lead them by nearly two minutes. |
| **Lake Forest** | 30 | Caution | No. He would lead them by about fifty seconds. |

**Roosevelt University fills the scholarship slot.** D2, GLIAC, one mile from the centre of the
Loop, still transitioning into Division 2 — which is exactly the situation where a mid-pack recruit
ends up scoring. It has **no cross country data at all**, so it enters at Verify, and that one
lookup is now the highest-value email in the metro. It is also a straight upgrade on location: the
Loop instead of Hammond, Indiana.

**Northwestern is out — they do not sponsor men's cross country or men's track and field at
all.** ✅ Verified. Men's track & field is listed as defunct; only the women's programs exist.
Worth stating plainly, because Northwestern is the obvious first thought for Chicago plus elite
CS and it is simply not available to him.

**Trinity Christian is out — the college is closing.** It announced on **4 November 2025** that it
will close at the end of the 2025–26 academic year. It did sponsor men's cross country and track in
the NAIA and sat at Verify on an earlier version of this document. It is not an option, and it is
kept on the map rather than deleted so the correction stays visible.

**Withdrawn: Loyola Chicago is a cut, not a co-equal first pick.** Every earlier version of
this document said *"essentially co-equal with DePaul; pick on CS department fit and money,"* on
the strength of a 14:23 outdoor 5000 that read as a clean +57 second gap. Then their cross
country results came in. Loyola **won the Atlantic 10** with seven runners between 23:58 and
24:45 — a 47 second 1-through-7 spread. He projects about **82 seconds outside** that pack.
The tight spread is what makes it decisive: on a team packed inside 47 seconds there is no soft
back end to slot into. **The recommendation is withdrawn and Loyola is on the cut list.**

**Withdrawn: Lewis University, twice over.** An earlier version called Lewis *"probably the single
best fit in metro Chicago"* and recommended widening the radius specifically to reach it. Its 13:45
5000, 29:58 10K and 3:51 1500 are internally consistent and put him ~95 seconds off their #1, the
same band as Furman and Wingate. At 30 miles it sat on the cut list as a documented reversal; at 20
miles it is out of range as well as out of contention, so it no longer appears anywhere. **Keep the
lesson, not the school: the original error was reading one fast 5000 as a measure of a squad's
depth.** It happened here with Lewis and again with Loyola, and it is why this document now ranks on
cross country results.

**Net effect.** Twelve schools, **one of them target tier**, and DePaul is the answer in Chicago —
which has now been true through three versions of this document, two radii and two ranking methods.
The thinness is a property of the metro, not an artifact of the radius: at 30 miles the metro held
four more schools and still exactly one target-tier fit. If the search can flex, the next thing
worth reaching for is not another ten miles of Chicagoland, it is the Greenville or New York list.

## 3. How to read the numbers below

| Column | What it means |
|---|---|
| **XC slot** | where his projection would have finished inside their top seven, averaged over every 2025 race on file. 1 = ahead of their #1. |
| **vs their 7th** | seconds between his projection and their 7th man. `+31s` = he is 31 seconds *outside* the seven. `−3s` = 3 seconds *inside* it. |
| **1–7 spread** | seconds from their #1 to their #7. This is the most course-independent number on the page, because it compares a team only to itself. A wide spread means a soft back end he can slot into; a tight one means there is no room. |
| **Tier** | Target = clean 4th–9th man fit · Deep = just outside the travel squad · Verify = **unmeasured**, no cross country data yet — a placeholder for a lookup nobody has done, not a judgement · Caution = he arrives at or ahead of their #1 |
| **Net cost/yr** | federal average net price after grant aid, from the College Scorecard — not sticker price. Out-of-state rates are used at public schools, since he is a South Carolina resident. |
| **CS** | ✅ with a percentage = share of that school's bachelor's degrees awarded in computer science (federal data). A low share is not a bad program; a `0%` usually means CS is filed under mathematics. |

## 4. Master list

Miles = approximate driving distance from the Loop. School names link to a full detail page with
per-race results, a map of every meet they attended last year, and cost/admissions detail.

### Division 1

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[DePaul](https://timhibbard.github.io/xc-cs-college-board/school.html?s=depaul)** | Lincoln Park | 3 | Big East | ✅ 10.7% | 1140–1330 | 76% | $30,902 | 7 | −3s | 146s | Target |
| **[UIC](https://timhibbard.github.io/xc-cs-college-board/school.html?s=uic)** | Near West Side | 3 | Missouri Valley | ✅ 11.9% | 1130–1350 | 77% | $10,974 | 8 | +31s | 72s | Deep |
| **[Chicago State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=chicago-state)** | Far South Side | 10 | NEC | ✅ 5.4% | not reported | 43% | $12,335 | 1 | — | 514s | Caution |

### Division 2

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Roosevelt](https://timhibbard.github.io/xc-cs-college-board/school.html?s=roosevelt)** | The Loop | 1 | GLIAC | ✅ 3.7% | 895–1175 | 97% | $20,194 | — | — | — | Verify |

### Division 3

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[University of Chicago](https://timhibbard.github.io/xc-cs-college-board/school.html?s=university-of-chicago)** | Hyde Park | 7 | UAA | ✅ 8.3% | 1510–1580 | 4% | $14,860 | 8 | +34s | 33s | Deep |
| **[Concordia Chicago](https://timhibbard.github.io/xc-cs-college-board/school.html?s=concordia-chicago)** | River Forest | 10 | CCIW | ✅ 3.2% | not reported | 93% | $18,436 | 1 | −323s | 236s | Caution |
| **[Dominican University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=dominican-university)** | River Forest | 10 | NACC | ✅ 6.7% | 880–1100 | 90% | $11,745 | — | — | — | Caution |
| **[Elmhurst University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=elmhurst-university)** | Elmhurst | 16 | CCIW | ✅ 5.9% | 990–1260 | 74% | $24,185 | 1 | — | 184s | Caution |
| **[Illinois Tech](https://timhibbard.github.io/xc-cs-college-board/school.html?s=illinois-tech)** | Bronzeville | 4 | NACC | ✅ 28.7% | 1180–1440 | 55% | $18,425 | 1 | — | 437s | Caution |
| **[North Park University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=north-park-university)** | North Park | 8 | CCIW | ❌ none | not reported | 69% | $16,948 | 1 | −457s | 282s | Caution |

### NAIA

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Calumet College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=calumet-college)** | Whiting IN | 20 | CCAC | ⚠️ thin | not reported | not reported | $22,451 | — | — | — | Verify |
| **[Saint Xavier](https://timhibbard.github.io/xc-cs-college-board/school.html?s=saint-xavier)** | Southwest Side | 13 | CCAC | ✅ 5.4% | not reported | 84% | $10,970 | — | — | — | Verify |

NAIA allows 12 scholarships for men's XC/track and has looser eligibility rules than the NCAA.
Neither of the two has cross country results on file yet, which is why both sit at Verify rather
than at a real tier. Trinity Christian was the third NAIA option and is closing (§2).

## 5. Schools removed — he would be a walk-on

| School | Div | Conf. | Location | XC slot | vs their 7th | 1–7 spread | Why removed |
|---|---|---|---|---|---|---|---|
| **[Loyola Chicago](https://timhibbard.github.io/xc-cs-college-board/school.html?s=loyola-chicago)** | D1 | Atlantic 10 | Chicago IL | 8 | +82s | 47s | Cut on cross country data, reversing an earlier recommendation. Its 14:23 outdoor 5000 read as a clean +57 second gap and this document ranked it co-equal with DePaul. They then won the Atlantic 10 with seven runners inside 47 seconds of each other (23:58–24:45); he would be about 82 seconds outside that pack. The tight spread is what makes it decisive — there is no soft back end to slot into. |

**Northwestern and Trinity Christian are not on the removal list** — Northwestern because there is
no men's program to be removed from, Trinity Christian because the college is closing (§2). Both
stay on the map so the corrections are visible.

**Lewis University is no longer on this list either**, because at 20 miles it is out of range. It
was cut on results at 30 miles and that cut still stands on the merits (§2).

## 5b. Dropped by the radius change, with their data preserved

These are not cuts. They are schools whose numbers were collected and which now sit outside the
ring. Recorded here because if the radius ever flexes again, this is the work already done.

| School | Div | Mi | Conf. | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier it held |
|---|---|---|---|---|---|---|---|---|
| **North Central** | D3 | 28 | CCIW | $21,044 | 8 | +11s | 86s | **Deep** |
| **Wheaton College** | D3 | 25 | CCIW | $26,975 | 1.5 | −80s | 65s | Caution |
| **Lake Forest** | D3 | 30 | Midwest | $28,673 | 1 | −272s | 168s | Caution |
| **Benedictine (IL)** | D3 | 25 | NACC | $22,313 | — | — | — | Caution |
| **Purdue Northwest** | D2 | 25 | GLIAC | $6,079 | — | — | — | Caution |

**Wheaton was reversed twice and this is the settled reading.** Their tight CCIW pack
(25:43–26:48) suggested he would be their 5th man, which would have made it a target. At the D3
Midwest regional their 4th through 7th ran 27:03–27:35 and he would have been their **#2**.
Correcting the CCIW course, which ran about 31 seconds fast, the two races agree: he arrives near
the front of that squad. Good academics, thin training group.

**North Central is worth one phone call regardless of the ring.** Naperville is 28 miles from the
Loop, which is a commute rather than an impossibility, and being 8th man on a team that goes to
nationals is one of the better development environments on the entire board.

## 6. Tiering

**Target — clean development band, concentrate effort here.** DePaul

**Deep — just outside the travel squad, still a good environment.** UIC · University of Chicago

**Verify — unmeasured, not borderline.** Roosevelt · Saint Xavier · Calumet College

**Caution — he arrives at or ahead of their #1, in some cases by minutes.** Elmhurst ·
Concordia Chicago · Dominican · Chicago State · North Park · Illinois Tech

**Cut on results.** Loyola Chicago

Twelve schools, **one of them target tier**. That ratio is the finding, and neither the cross
country data nor the radius change moved it.

## 7. Top picks

1. **[DePaul](https://timhibbard.github.io/xc-cs-college-board/school.html?s=depaul)** — 3 miles
   from the Loop, Big East D1, a genuinely strong CS program (School of Computing), and the one
   school in the metro where the cross country data actually confirms the fit. Their Big East
   seven ran 23:45–26:10 and he lands **7th man, three seconds inside it**. The 146 second
   1-through-7 spread is the widest of any target-tier school here, which is the good kind of
   soft: there is real room at the back of that squad. Net price $30,902. Best fit in Chicago,
   comfortably, and now the only one.
2. **[UIC](https://timhibbard.github.io/xc-cs-college-board/school.html?s=uic)** — the standing
   "borderline keep, resolve the depth question" note is now resolved, and the answer is **too
   deep, not too thin**: their Missouri Valley seven ran 24:24–25:36 inside a 72 second spread
   and he is about 31 seconds outside it. At **$10,974 net** it is far and away the cheapest
   strong CS option in the metro, and 31 seconds is one good freshman year. Worth the email.
3. **[University of Chicago](https://timhibbard.github.io/xc-cs-college-board/school.html?s=university-of-chicago)**
   — the roster times are finally resolved: seven runners inside **33 seconds**, the tightest
   pack on the entire 130-school board, with him about 34 seconds outside. Elite CS, and the net
   price of $14,860 is startlingly low for a $90k sticker. The obstacle is a **4% admit rate**,
   not the running.
4. **[Roosevelt](https://timhibbard.github.io/xc-cs-college-board/school.html?s=roosevelt)** —
   new to the board, unmeasured, and worth an email rather than a ranking. It is the **only
   scholarship program left in metro Chicago** now that Purdue Northwest is out of range, it is a
   mile from the centre of the Loop, and it is still transitioning into Division 2. Ask for their
   2025 8K results and their incoming distance class in the same email. Note the 97% admit rate
   and the modest 3.7% CS share: this is an access school, not a tech school.

**The hard truth about Illinois Tech:** **28.7% of its bachelor's degrees are in computer
science** — by far the highest share on this list — and it is 4 miles from downtown. Its distance
squad ran a 437 second 1-through-7 spread and he would beat their best runner by over two
minutes. That is not a training environment; it is a solo career with a good CS degree attached.
If CS is the priority and he accepts that, fine — but go in knowing it, and ask the coach
directly what they are recruiting.

## 8. Chicago-specific considerations

**Illinois public tuition.** UIC's out-of-state sticker is $29,884 tuition plus $16,500 room and
board, but its **federal average net price is $10,974** — the gap between sticker and net is the
whole story at UIC, and it makes the cheapest strong CS program in the metro also one of the
cheapest schools on the entire board. Chicago State is $12,335 net. Both are worth a financial
aid pre-read rather than a ranking on sticker price.

**Winter training is a real factor.** Chicago indoor track runs through genuine winter and
lakefront wind is not a joke. Ask coaches what indoor facility they have access to — a full 200m
banked track versus a fieldhouse straightaway meaningfully affects indoor development. DePaul,
UIC and Illinois Tech all have differing arrangements; ask specifically. Each school's detail
page has a map of every indoor meet they attended last year, which is a decent proxy for how
seriously they treat the season.

**Training terrain, and now with less of it.** The lakefront path is excellent for volume and
flat as a table. Ask where they find hills — the answer is usually Waterfall Glen, Palos, or Busse
Woods, all a drive away, and at 20 miles every school on this list is inside the flat part of
Chicagoland. A program that never runs hills will limit him as a 5K/XC runner.

**The 20-mile ring is genuinely urban, and that is the one gain.** Every school here is in the
city or on its immediate edge; eleven of the twelve are inside 16 miles. The tradeoff is stated in §2
and it is not a small one — the suburban campuses the 30-mile ring reached were where the D3
national program and the only scholarship money were.

## 9. To-dos, priority order

1. **Get cross country results for Roosevelt.** It is the only scholarship program in range and it
   is completely unmeasured. This is the single highest-value lookup in the metro. Ask for their
   2025 GLIAC 8K result.
2. **Email DePaul.** They are the only target-tier school in the metro and the data supports the
   approach. Lead with the 8K projection, not the 1600 time.
3. **Get cross country results for the other three unmeasured schools** — Saint Xavier, Calumet
   College, and Dominican, which sits at Caution on a track mark alone.
4. **Ask UIC what their incoming class looks like.** They are about 31 seconds outside the scoring
   seven, which one freshman year can close — but only if they are not already bringing in four
   runners ahead of him.
5. **Calibrate the Big East, Missouri Valley, UAA and NEC courses.** Those four meets are the
   only 2025 races on file for DePaul, UIC, University of Chicago and Chicago State respectively,
   and none has a cross-checking team on a calibrated course — so all four reads rest on an
   uncorrected course.
6. Confirm a **true BS in Computer Science** at Calumet College — the federal data shows CS
   degrees but the count is too small to confirm a standalone major, and their site was
   unreachable.
7. Verify SAT and accept figures for the five schools where the federal file reports no SAT
   range at all.
8. Ask each coach the CS-lab-conflict question (see `greenville-sc.md` §9).

**Resolved and off this list:** University of Chicago's roster times (§7), Wheaton's cross country
results (§5b), 5th/7th man times for DePaul, Loyola and UIC (§2, §7), and Trinity Christian's
status (§2 — the college is closing).
