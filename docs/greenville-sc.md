# College Search — Greenville SC (250 mile radius)

XC/Track + Computer Science. Last updated 2026-08-23 (v8 — both sports required, 1500 championship depth added)

> **Four schools left this ring because they sponsor cross country and not men's track — and one of
> them was a target.** The board now requires *both* sports, and **Mercer** fails it: Macon sponsors
> men's cross country and *women's* track and field, so there is nothing for him to run in the
> spring. Measured on cross country it was their 4th man, 185 miles out, with a verified CS degree.
> Clark Atlanta, USC Aiken and Winston-Salem State go with it, all three already at Caution. That
> leaves **77 schools here, 22 of them target tier**, with **76 of the 77 measured** — only
> **Shorter** is still unmeasured. The rule and every removal are in §2h.
>
> **The 1500 now has a championship field behind it rather than a season best.** Every school page
> carries that team's 2026 conference-championship 1500 — the whole field, the entrants that team
> sent, and where a **4:01** would have finished in it. In this ring **72 of the 77 raced a 1500**,
> and 4:01 **makes 66 of those conference finals, scores in 35 of them, and would be the fastest man
> on 33 teams**. See §2i.
>
> The rest of v7 stands. The sweep that measured everything found **thirty-four of the seventy-seven
> would have him as their #1**, and **twenty-three of the seventy-six never finished seven runners**
> in a championship race. Every school page carries the coach's name, email, title and office phone.
> See §2e.

Live version, with per-school pages, per-race results and meet maps:
<https://timhibbard.github.io/xc-cs-college-board/greenville.html>

## 1. Athlete profile

| Event | Current | Projected |
|---|---|---|
| 1600m | 4:21 | ~4:18 |
| 3200m | 9:40 | 9:29 |
| 5K XC | 16:29 | ~15:59 |

Converted: **1500 4:01** · **3000 8:53** · **track 5000 15:20** · **8K XC 26:07** · **10K XC 32:54**

The **1500 of 4:01** is the one conversion anchored to the 1600 rather than the 3200, and
deliberately so: it comes from the projected **4:18** 1600 at the textbook Riegel exponent
(factor (1500/1600)^1.06 = 0.9339, so 258s → 240.9s), and the coach's rule of thumb — subtract
about 17 seconds from a 1600 — gives the same answer. Over a distance 100 metres *shorter* than
the race he has actually run, his speed lean is an asset rather than a flattering distortion. From
today's 4:21 the same math gives 4:03.7; the board uses the projected figure because he has another
track season first. Every school page now shows this next to that team's fastest 1500 *and*
against the field that team's conference championship actually produced (§2i), and **110 of the 116
programs on the board raced a 1500 in 2026** — marginally more than have a 5000 (106). In this ring
it is **72 of 77** with a 1500 and 68 with a 5000. Those tables were filled in during the same
sweep that measured the cross country, and the exercise made the point of §2e for itself: at several
schools the fast 1500 belongs to a middle-distance runner whose team has no distance squad behind him.

**Read the 1500 gap on its own scale.** The healthy band at 5000 is 40–60 seconds behind a team's
best runner; the same percentage over 1500 is only **10 to 15 seconds**. Twelve seconds back at
1500 is the same relationship as fifty back at 5000.

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
That found **55 additions** — one of which, **North Georgia**, later turned out to field no men's
cross country team at all (§2b), leaving 54 real ones:

| | Added | Of which inside the old 200 miles |
|---|---|---|
| Division 1 | 12 | 6 |
| Division 2 | **35** | 27 |
| Division 3 | 7 | 6 |
| NAIA | 1 | 1 |
| **Total** | **55** | **40** |

**The Division 2 number is the one that matters.** D2 is where partial athletic scholarships live,
and this document previously listed **seven** D2 programs in range. There are **thirty-eight** that
field both men's cross country and men's outdoor track, plus three more that field cross country only
(§2h). The
closest omission, **Southern Wesleyan**, is 25 driving miles from home — and it came out of the
measurement sweep at Target tier, which makes it the most consequential single omission on the board.

Every addition entered at **Verify — meaning unmeasured, not borderline** — and every one of them
has since been measured, which is the work described in §2e. That is what makes the rebuild the
biggest finding here rather than a bookkeeping note: **eleven of the twenty-two target-tier
schools in §6 are additions**, including the closest one on the board. Had the list not been rebuilt,
the ranked answer would still be v3's, and it would have been wrong by a wide margin. Of the 77
schools, exactly **one — Shorter — still has no cross country result.**

Two limits worth stating. The rebuild inherits the conferences' own errors — a stale sponsored-sports
table is wrong in both directions, and no addition's sponsorship was re-confirmed on the school's
own athletics site. And **NAIA and NCCAA coverage is still incomplete**: only Montreat (NAIA) is
here, while at least Toccoa Falls, Truett McConnell, Brenau, Columbia
International, Columbia College SC, Milligan, Johnson University, Reinhardt, Voorhees, Tennessee
Wesleyan, Morris College, Bryan College, Bluefield University, Point University, Life University,
Spartanburg Methodist and Warren Wilson are not. NAIA allows **12 scholarships** for men's XC and
track with looser eligibility rules, so that gap sits exactly where money is easiest to find.

### 2b. Two schools here have no men's cross country team

**Georgia State** sat at **Verify** on every earlier version of this document at 16.2% CS degrees,
which made it look like an attractive unmeasured D1. Georgia State sponsors **no men's cross country
and no men's track and field** — the distance programs are women's only. There was never a team there
to verify.

**North Georgia** is the same error found by the measurement sweep, and it was a more expensive one:
at **$9,823 net and 9.2% CS degrees** it was named in v6's §7 as one of the highest-value unmeasured
prospects on the board. Trying to find its 2025 results is how the mistake surfaced — the Peach Belt
sponsors men's cross country, and North Georgia is not one of the members that fields it. There was
nothing to measure.

This is the failure mode of a tier that means "no data yet": it reads as a program awaiting
measurement rather than one that does not exist, and it is precisely the reason **Verify now means
one thing only — no result exists yet** — and the reason the sweep had to be finished rather than
sampled. Both schools are kept on the map rather than deleted so the correction stays visible. If
an error of this kind was sitting in a 27-school list, assume there are others in a 77-school one.

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
naming the cost again: this cuts the closest school on the entire board — Furman, at 0 miles, with a
verified CS degree. **Clemson, the other local cut, did not stay cut**; see §2e.

**A correction that nearly went the other way.** The South Atlantic Conference championship
course ran about **96 seconds slow** at 8K — confirmed independently by Anderson, Catawba and
Wingate against the D2 regional. An early version of the correction had the **sign backwards**,
which briefly promoted Wingate from cut to target. Course corrections are applied only where at
least three teams cross-check, and the two that survived that bar are documented in
`../methodology.html` §3a.

### 2e. The full sweep: 57 unmeasured schools became 1

This is the change that matters in this revision. Every school in this ring except **Shorter** now has
at least one 2025 championship result on file, and the tier column is a measurement rather than a
placeholder. Where the 56 newly measured programs landed:

| Moved from Verify to | Count | Notable |
|---|---|---|
| **Target** | 12 | **Southern Wesleyan (25 mi)**, Augusta (15.6% CS), Kennesaw State, Chattanooga, UNC Pembroke, Pfeiffer, College of Charleston, Coastal Carolina, Campbell, West Georgia, Fayetteville State, Queens (Charlotte) |
| **Deep** | 2 | Charleston Southern (10s outside their seven), Lee University (25s) |
| **Caution** | 37 | he would be at or ahead of their #1 |
| **Measured, then removed for having no men's track** | 4 | §2h — **Mercer** was one of the thirteen new targets |
| **No program to measure** | 1 | North Georgia (§2b) |

**Southern Wesleyan is the headline.** Twenty-five driving miles from home, D2 so partial athletic
aid exists, **$15,464 net**, and the running works cleanly: **their #4, 105 seconds inside their
seventh, on a 116 second 1-through-7 spread.** v6 could only call it "the closest omission" and hope.
The one weakness is academic — 2.7% of degrees in CS, and a 100% admit rate means no admissions
leverage to gain from running.

**Clemson is reinstated at Deep.** It was cut on a 3:43 1500 and a 14:36 5000 that read as out of
reach. Its actual depth says otherwise: 14th at the ACC championship and 15th at the D1 Southeast
regional put him at their **7th-to-8th man, 15 seconds outside the seven** and 119 seconds behind
their #1. That is not a place he travels as a freshman, and it is 32 miles from home with a real CS
department at **$22,253 in-state**. Cutting a school on team best track marks is the same error as
recommending one on them, and this board has now made it in both directions — see Lenoir-Rhyne above
for the other.

**Two of the new targets carry a warning that the tier does not.** **Queens (Charlotte)** fits the
running well (their #5, 56 second spread) and has **no bachelor's computer science program in the
federal file** — it is the only Target-tier school on the entire 116-school board with a `❌ none` CS
reading, so the catalog check in §10 item 7 has to happen before it goes on any list. **Berry College**
went the other way, moving up from Caution to Target on its championship result (their #3–4, 82 seconds
inside the seven) after v6 had ranked it on track marks alone.

### 2f. Twenty-three programs here never finished seven runners

A cross country team scores five and travels seven, and the 7th man is what this document ranks on. At
twenty-three of the seventy-six measured schools here **there is no 7th man** — they never got seven men to the
finish of a championship race in 2025. Those rows show a blank in *vs their 7th*, and their pages
compare him to the team's last finisher instead:

**Allen, Benedict, Bluefield State, Brevard, Carson-Newman, Claflin, Coker, Fort Valley State,
Gardner-Webb, Johnson C. Smith, King University, LaGrange, Lenoir-Rhyne, Methodist, Montreat, NC
Central, Newberry, Oglethorpe, Piedmont, Savannah State, UVA Wise, Winthrop, Wofford.**

Two more — **USC Aiken** and **Winston-Salem State** — were on this list in v7 and have since left the
board for having no men's track (§2h), which is the same finding twice: a program that cannot fill a
scoring seven in the autumn is often a program that does not contest the spring either.

Two D1 programs are on that list — **Winthrop (five finishers) and Wofford (six)** — which is worth
sitting with, because both are inside 100 miles and both look like functioning athletic departments
from the outside. **Benedict finished three**, so it has no team result at all and is held at Caution
on that basis rather than on times. Nothing in this group can be ranked as a fit; a program that
cannot fill a scoring seven is a program in trouble, and the useful question there is not "where would
he slot in" but "is this team going to exist in four years."

### 2g. Every school page now names a coach

All 77 pages carry the **name, title, email and office phone of the coach who would actually recruit
him**, read off that school's own staff directory in August 2026, with a link to the directory on each
page. Two schools have a coach but no published email — **Fayetteville State** and **West Georgia** —
where the phone number is the way in.

Coaches are named here; individual college athletes are not. A coach is a public professional listed
on their employer's own site, and the whole point of this document is to know who to write to. The
runners whose times produce these numbers are recorded as times only. The provenance rules are in
`../methodology.html` §6.

### 2h. Both sports, or off the board

The rule for being on this board used to be "sponsors men's cross country." It is now **"sponsors
men's cross country *and* men's outdoor track,"** and four schools in this ring fail it. He wants both
seasons; a cross-country-only program gives him one, and it also means no 1500, no 5000 on the track,
and no spring competition to develop through.

The check uses **two signals that have to agree**, because a school's own website is often stale and a
conference sponsored-sports table is often wrong (§2a). Signal one: the school's own published sport
list — either no men's track page at all, or a "track and field" page that turns out to be the
women's program. Signal two: **TFRRS holds no 2026 men's outdoor mark for that school at any
distance**. Where the two disagree, the school stays on the board; that is why Fayetteville State and
Allen University are still here despite thin track pages — they have 2026 men's marks on file.

| School | Div | Conf. | Mi | Tier when removed | What the two signals showed |
|---|---|---|---|---|---|
| **[Mercer](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mercer)** | D1 | Southern | 185 | **Target** | 30 sports published, *women's* track and field among them and no men's track page; no 2026 men's outdoor mark on TFRRS. |
| **[Clark Atlanta](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clark-atlanta)** | D2 | SIAC | 165 | Caution | The single track and field page is the women's program; the men's track roster URL serves a 2016 roster; no 2026 men's outdoor mark. |
| **[USC Aiken](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-aiken)** | D2 | Peach Belt | 110 | Caution | Cross country for both sexes, track and field for neither — 23 sports, no track page of any kind, no 2026 outdoor marks. |
| **[Winston-Salem State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winston-salem-state)** | D2 | CIAA | 175 | Caution | Men's cross country and women's track and field; the men's side does not exist; no 2026 men's outdoor mark. |

**Mercer is the one that hurts.** It was one of the thirteen targets the measurement sweep produced —
their 4th man, 92 seconds inside their seven, a 134 second spread, D1 Southern Conference, 4.9% CS,
$23,847 net. Nothing about the running or the academics is wrong with it. If a cross-country-only
program ever becomes acceptable, **Mercer is the first school to put back**, and it goes back at
Target.

Three of the four were already at Caution, and two of those three — USC Aiken and Winston-Salem State
— also never finished seven runners (§2f). For them the rule removed schools that were not going to
be recommended anyway.

**They keep their pages.** All four still have full detail pages with their cross country results,
1500 fields, costs, coaches and maps, and they still carry the tier the measurement gave them. A
removal that deletes the evidence is a removal you cannot check, and this is the same reason Georgia
State and North Georgia stayed on the map in §2b. They are simply out of the master list, out of the
tier counts and off the map by default.

Board-wide the rule moved **15 schools**, and the distribution says something about the metros:
**ten of the fifteen are in New York**, where small D3 colleges commonly field cross country and no
track, against four here and one in Chicago.

### 2i. The 1500 in May

A cross country slot answers the autumn. The 1500 answers May — and it is now built from a
championship field rather than from a season best. For **all 77 schools here** the board records that
team's **2026 conference-championship 1500**: the whole field, the men that team actually entered, the
winning time, and the time that cut into the final. That is **22 conference meets** in this ring, plus
three postseason cards: Catawba and Lee University at the Division 2 national championships, and UNC
Charlotte at the NCAA Division 1 East First Rounds.

One exclusion has to be named, because the first build got it wrong. TFRRS files the 1500 run at the
end of a **decathlon** as a second "1500 Meters" page at the same meet, and merging the two inflated
every field size and dropped multi-eventers into teams' entrant lists — High Point looked like it had
taken a 1500 runner to the Division 1 championships when what it took was a decathlete at 4:31. The
decathlon round is now excluded. It changed no placing, because every decathlon 1500 on file is slower
than 4:01, but it changed field sizes, entrant lists and the postseason count. The rule is written out
in `../methodology.html` §7.

| For a 4:01 | Count |
|---|---|
| Schools that raced a 1500 in 2026 | **72 of 77** |
| He would be their **fastest man** | **33 of 72** |
| He would be their **#3 or better** | 51 of 72 |
| Makes the conference final on time | **66 of 77** |
| Would have **scored** in that final (top 8) | 35 of 77 |
| The school **entered nobody** in its own conference 1500 | **23 of 77** |
| No 1500 run anywhere in 2026 | 5 of 77 |

The median program in this ring has a fastest 1500 of **4:00.7**, which puts his projection **0.3
seconds off the median team's best man**. Read that on the 1500's own scale, not the 5000's: the
healthy band is **10 to 15 seconds behind a team's best**, and being *ahead* of their #1 is the same
warning it is in cross country — nobody to train with.

Where the eight top picks in §7 sit. The "of N" figures include his projection dropped into the
field, and they compare **every man who ran the event at that meet on time, prelims included**, which
is the number to trust:

| School | Their fastest | His slot on their chart | Conference field | Their final |
|---|---|---|---|---|
| Southern Wesleyan | 3:58.4 | **#2 of 9** | 5th of 25, Conference Carolinas | in by 10.1s, 5th of 13 |
| UNC Asheville | 3:51.1 | #6 of 11 | 13th of 21, Big South | in by 7.6s, 11th of 13 |
| UNC Charlotte | 3:41.2 | #17 of 23 | 18th of 20, American | in by 3.7s, 11th of 12 |
| Augusta University | 3:53.1 | #6 of 9 | 11th of 20, Peach Belt | in by 15.6s, 11th of 20 |
| Kennesaw State | 3:47.7 | #4 — behind all three who ran it | 13th of 15, CUSA | in by 4.2s, 10th of 11 |
| Davidson | 3:48.3 | #7 of 7 | 32nd of 40, Atlantic 10 | in by 9.8s — see the tactical note below |
| UNC Greensboro | 3:47.9 | #8 of 13 | 15th of 15, Southern | **misses by 0.2s** |
| Emory | 3:49.5 | #8 of 20 | 16th of 25, UAA | in by 24.0s, 16th of 25 |

**Southern Wesleyan is the awkward one, and it is the top pick.** A 4:01 would be their **#2** — their
fastest man ran 3:58.4 and their third was 4:05.5. That is a thin 1500 group by the standard in §1,
and it sits next to a clean #4 cross country slot at the same school. Ask specifically who else is
being signed at 1500–5000 pace.

**Three of the eight would have to earn the final rather than get in on time**, and one does not make
it: **UNC Greensboro misses the Southern Conference final by two tenths of a second**, and UNC
Charlotte (3.7s) and Kennesaw State (4.2s) are inside it by less than the margin a bad day costs.
Across the whole ring **eleven schools' conference finals are out of reach on a 4:01** — six of them
target tier: **ETSU, UNC Greensboro, Chattanooga, Coastal Carolina, Queens (Charlotte) and West
Georgia**, plus Appalachian State and Clemson at Deep and The Citadel, Western Carolina and Wofford at
Caution. Conference level in the 1500 does not track conference level in cross country, and this is
where the two measurements disagree most.

**Davidson's final needs its caveat.** He clears the Atlantic 10 cut by 9.8 seconds, and the A10 final
was won in **4:03.6** — slower than the **3:47.7** run in the rounds that fed it. A placing inside a
tactical final describes that race, not the level; the 32nd-of-40 figure on time is the honest read.

**Twenty-three schools here entered nobody in their own conference 1500**, which is a finding rather
than a gap: **Elon, Campbell, Chattanooga, College of Charleston, Fayetteville State, Wofford, The
Citadel, Presbyterian, Lander, Newberry, King University, Lenoir-Rhyne, Francis Marion, Georgia
College, Lincoln Memorial, Coker, Methodist, LaGrange, Guilford, Shorter, Allen University, Bluefield
State and Johnson C. Smith**. **Five of them are target tier** — Elon, Campbell, Chattanooga, College
of Charleston and Fayetteville State — which is nearly a quarter of the target list. A program that
sends no one to the conference 1500 either has no milers or does not race them there, and the
distinction matters enough to ask.

**The sharpest single number in this section belongs to Fayetteville State.** It is the cheapest
target-tier school on the entire board at **≈$11,892 net on his residency** ($7,892 for a North
Carolinian, plus a $4,000 non-resident premium that is unusually small), it came out of the sweep at
Target — and it ran **no 1500 anywhere in 2026**. The CIAA championship 1500 was won in **4:02.0**. A 4:01 would have won that
conference championship as a freshman, in a race his own school did not enter. Read that as the state
of the program, not as a compliment to the projection.

The method — how a championship page is read, what happens when the round-0 result is a combined
all-sections file rather than a final, and why prelim times are included — is in
`../methodology.html` §7. Individual college athletes are not named anywhere in this project; the
1500 fields are recorded as times only.

## 3. How to read the numbers below

| Column | What it means |
|---|---|
| **XC slot** | where his projection would have finished inside their top seven, averaged over every 2025 race on file. 1 = ahead of their #1. |
| **vs their 7th** | seconds between his projection and their 7th man. `+35s` = he is 35 seconds *outside* the seven. `−41s` = 41 seconds *inside* it. **Blank at the twenty-three programs that never finished seven** (§2f), whose pages compare him to the team's last finisher instead. |
| **1–7 spread** | seconds from their #1 to their #7. The most course-independent number here, because it compares a team only to itself. A wide spread means a soft back end to slot into; a tight one means there is no room. On a short squad it is first-to-last, and blank where fewer than five finished, because that is not a team result. |
| **Tier** | Target = clean 4th–9th man fit · Deep = just outside the travel squad · Verify = **unmeasured**, no cross country result exists yet · Caution = he arrives at or ahead of their #1. **Only Shorter is at Verify now** — read every other tier as a measurement. |
| **Net cost/yr** | federal average net price after grant aid, from the College Scorecard — **not** sticker price. Out-of-state rates are used at public schools, except at the ten South Carolina publics, where the in-state rate applies. |
| **CS** | ✅ with a percentage = share of that school's bachelor's degrees awarded in computer science, from federal completion data. A low share is not a bad program. |
| **Coach** | the person who would actually recruit him, linked as a mailto, read off that school's own staff directory in August 2026. Title, office phone and a link to the directory are on each detail page. Staffs turn over yearly, so if the name is stale the linked directory is not. |

**Mileage caveat for the 55 additions.** Their `Mi` figures are **estimates**, not looked-up routes:
straight-line distance × 1.18, or × 1.35 in the mountain states (TN, VA, WV, KY), rounded to the
nearest 5. Expect ±15%. That matters only near the line — **Campbell, Savannah State and NC
Central at an estimated 250 could each be over it.**

Eight of the additions carry a **`❌ none` CS reading that needs one catalog check rather than
dismissal**: Brevard, Belmont Abbey, Young Harris, Queens (Charlotte), Allen, Oglethorpe, Emory &
Henry and Lees-McRae all report 0% computing degrees *and* a live mathematics program, which at a
small college is usually CS filed under mathematics. Each of those school pages says so.

**One of those eight now matters much more than the others.** **Queens (Charlotte)** came out of the
sweep at Target tier — the only `❌ none` school on the entire 116-school board to do so. Its catalog
is the highest-value single lookup left in §10 item 7: if the program exists and is filed under
mathematics, Queens is a genuine target 105 miles away, and if it does not, the school is disqualified
outright no matter how the running reads.

## 4. Master list

Miles = approximate driving distance from Greenville. School names link to a full detail page with
per-race results, a map of every meet they attended last year, cost, and admissions detail.

### Division 1

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier | Coach |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Campbell](https://timhibbard.github.io/xc-cs-college-board/school.html?s=campbell)** | Buies Creek NC | 250 | CAA | ✅ 6.5% | not reported | 87% | $24,516 | 3 | −72s | 141s | Target | [Evan Darm](mailto:edarm@campbell.edu) |
| **[Chattanooga](https://timhibbard.github.io/xc-cs-college-board/school.html?s=chattanooga)** | Chattanooga TN | 225 | Southern | ✅ 4.2% | 1013–1210 | 81% | ≈$22,329 | 4.5 | −113s | 220s | Target | [Steve Picucci](mailto:steve-picucci@utc.edu) |
| **[Coastal Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coastal-carolina)** | Conway SC | 245 | Sun Belt | ✅ 2.5% | 1050–1220 | 75% | $13,966 | 3.5 | −22s | 89s | Target | [Michael Bianchina](mailto:mbianchin@coastal.edu) |
| **[College of Charleston](https://timhibbard.github.io/xc-cs-college-board/school.html?s=college-of-charleston)** | Charleston SC | 235 | CAA | ✅ 4.1% | 1140–1310 | 60% | $18,960 | 5.5 | −20s | 97s | Target | [Chris Bailey](mailto:crbailey@cofc.edu) |
| **[Davidson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=davidson)** | Davidson NC | 115 | Atlantic 10 | ✅ 6.9% | 1400–1530 | 13% | $17,379 | 4 | −41s | 139s | Target | [Matt Stuck](mailto:mastuck@davidson.edu) |
| **[Elon](https://timhibbard.github.io/xc-cs-college-board/school.html?s=elon)** | Elon NC | 200 | Coastal | ✅ 2.6% | 1130–1280 | 66% | $41,555 | 5 | −40s | 78s | Target | [Mark Elliston](mailto:melliston@elon.edu) |
| **[ETSU](https://timhibbard.github.io/xc-cs-college-board/school.html?s=etsu)** | Johnson City TN | 140 | Southern | ✅ 4.2% | 980–1200 | 86% | ≈$20,033 | 4 | −28s | 171s | Target | [Sterling Jones](mailto:jonessp6@etsu.edu) |
| **[High Point](https://timhibbard.github.io/xc-cs-college-board/school.html?s=high-point)** | High Point NC | 180 | Big South | ✅ 2.3% | 1110–1320 | 75% | $38,707 | 7 | −31s | 66s | Target | [Remy Tamer](mailto:rtamer@highpoint.edu) |
| **[Kennesaw State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kennesaw-state)** | Kennesaw GA | 125 | CUSA | ✅ 11.1% | 1000–1220 | 69% | ≈$26,976 | 4.5 | −82s | 275s | Target | [Cale McDaniel](mailto:cmcdan10@kennesaw.edu) |
| **[Queens (Charlotte)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=queens-charlotte)** | Charlotte NC | 105 | ASUN | ❌ none | 1140–1340 | 62% | $30,857 | 5 | −15s | 56s | Target | [Will Crocker](mailto:crockerw@queens.edu) |
| **[UNC Asheville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-asheville)** | Asheville NC | 62 | Big South | ✅ 3.2% | 1170–1360 | 92% | ≈$29,598 | 5.5 | −50s | 64s | Target | [Adam Puett](mailto:apuett@unca.edu) |
| **[UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte)** | Charlotte NC | 100 | American | ✅ 15.2% | 1140–1330 | 80% | ≈$30,688 | 7 | −11s | 167s | Target | [Riley Macon](mailto:rmacon4@charlotte.edu) |
| **[UNC Greensboro](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-greensboro)** | Greensboro NC | 170 | Southern | ✅ 7.4% | 1150–1355 | 89% | ≈$27,316 | 4.5 | −126s | 93s | Target | [Kaleigh Roach](mailto:k_roach@uncg.edu) |
| **[West Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=west-georgia)** | Carrollton GA | 210 | United Athletic | ✅ 2.7% | 950–1140 | 52% | ≈$24,498 | 6 | −28s | 114s | Target | Ryan Bailey *(no email)* |
| **[Appalachian State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=appalachian-state)** | Boone NC | 130 | Sun Belt | ✅ 2.9% | 1120–1280 | 90% | ≈$34,469 | 8 | +35s | 101s | Deep | [Damion McLean](mailto:mcleandm@appstate.edu) |
| **[Charleston Southern](https://timhibbard.github.io/xc-cs-college-board/school.html?s=charleston-southern)** | Charleston SC | 220 | Big South | ✅ 4.7% | 930–1160 | 96% | $21,666 | 7.5 | +10s | 81s | Deep | [Jim Stintzi](mailto:jstintzi@csuniv.edu) |
| **[Clemson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clemson)** | Clemson SC | 32 | ACC | ✅ 4.5% | 1240–1410 | 38% | $22,253 | 7.5 | +15s | 104s | Deep | [Mark Elliott](mailto:maellio@clemson.edu) |
| **[Gardner-Webb](https://timhibbard.github.io/xc-cs-college-board/school.html?s=gardner-webb)** | Boiling Springs NC | 60 | Big South | ✅ 1.9% | 975–1198 | 77% | $17,674 | 1 | — | 966s | Caution | [Greg Thiel](mailto:gthiel@gardner-webb.edu) |
| **[NC A&T](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-aandt)** | Greensboro NC | 200 | CAA | ✅ 8.9% | 1020–1190 | 50% | ≈$24,706 | 1 | −175s | 169s | Caution | [Allen Johnson](mailto:akjohnson5@ncat.edu) |
| **[NC Central](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-central)** | Durham NC | 250 | MEAC | ✅ 3.9% | ~1050 avg | 87% | ≈$28,395 | 3 | — | 355s | Caution | [Fabrienne Swepson](mailto:fswepson@nccu.edu) |
| **[Presbyterian](https://timhibbard.github.io/xc-cs-college-board/school.html?s=presbyterian)** | Clinton SC | 45 | Big South | ✅ 1.4% | 980–1200 | 68% | $20,528 | 1 | −263s | 234s | Caution | [Robert "Bus" Baker](mailto:bbaker@presby.edu) |
| **[SC State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=sc-state)** | Orangeburg SC | 150 | MEAC | ✅ 3.8% | not reported | 83% | $18,097 | 2 | −195s | 241s | Caution | [Donald Cooper](mailto:dcoope17@scsu.edu) |
| **[The Citadel](https://timhibbard.github.io/xc-cs-college-board/school.html?s=the-citadel)** | Charleston SC | 235 | Southern | ✅ 4.0% | 1085–1285 | 23% | $20,723 | 1 | −163s | 96s | Caution | [Kris Kut](mailto:kutk@citadel.edu) |
| **[USC Upstate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-upstate)** | Spartanburg SC | 32 | Big South | ✅ 8.3% | 1005–1175 | 67% | $13,557 | 2 | −43s | 82s | Caution | [Carson Blackwelder](mailto:cblackwelder@uscupstate.edu) |
| **[Western Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=western-carolina)** | Cullowhee NC | 60 | Southern | ✅ 1.3% | 1080–1270 | 82% | ≈$17,315 | 2 | −82s | 105s | Caution | [Jesse Norman](mailto:jnorman@email.wcu.edu) |
| **[Winthrop](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winthrop)** | Rock Hill SC | 100 | Big South | ✅ 2.5% | 1010–1220 | 79% | $15,343 | 1 | — | 143s | Caution | [Raffael Craig](mailto:craigr@winthrop.edu) |
| **[Wofford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wofford)** | Spartanburg SC | 32 | Southern | ✅ 3.6% | 1198–1343 | 52% | $18,732 | 1 | — | 222s | Caution | [Johnny Bomar](mailto:bomarjc@wofford.edu) |

### Division 2 (scholarship money exists)

Thirty-eight programs, thirty-one of them new to this document, and **thirty-seven of the thirty-eight
are measured** — Shorter is the one that is not. This is where the scholarship money is and where the
sweep did the most work: it produced five of the twenty-two targets — **Southern Wesleyan (25 mi)**,
Augusta, UNC Pembroke, Fayetteville State and Catawba — and it also produced thirteen of the
twenty-three programs that never finished seven runners. Three D2 programs that were on this table in
v7 are gone from it: Clark Atlanta, USC Aiken and Winston-Salem State sponsor no men's outdoor track
(§2h).

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier | Coach |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Augusta University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=augusta-university)** | Augusta GA | 115 | Peach Belt | ✅ 15.6% | 970–1140 | 86% | ≈$30,107 | 5 | −94s | 148s | Target | [Jacob Burgamy](mailto:jburgamy@augusta.edu) |
| **[Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba)** | Salisbury NC | 130 | South Atlantic | ✅ 1.6% | 1030–1300 | 75% | $17,879 | 5.5 | −96s | 133s | Target | [Jason Bryan](mailto:jpbryan14@catawba.edu) |
| **[Fayetteville State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fayetteville-state)** | Fayetteville NC | 235 | CIAA | ✅ 3.3% | 890–1090 | 82% | ≈$11,892 | 4.5 | −158s | 250s | Target | Frank Hyland *(no email)* |
| **[Southern Wesleyan](https://timhibbard.github.io/xc-cs-college-board/school.html?s=southern-wesleyan)** | Central SC | 25 | Conference Carolinas | ✅ 2.7% | 1040–1210 | 100% | $15,464 | 4 | −105s | 116s | Target | [Peyton Shelton](mailto:pshelton@swu.edu) |
| **[UNC Pembroke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-pembroke)** | Pembroke NC | 215 | Conference Carolinas | ✅ 4.8% | 970–1200 | 93% | ≈$14,260 | 3 | −143s | 166s | Target | [Dr. Peter Ormsby](mailto:peter.ormsby@uncp.edu) |
| **[Anderson (SC)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=anderson-sc)** | Anderson SC | 30 | South Atlantic | ✅ 5.0% | 1100–1280 | 55% | $23,544 | 7.5 | +2s | 66s | Deep | [Kevin Eagle](mailto:keagle@andersonuniversity.edu) |
| **[Lee University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lee-university)** | Cleveland TN | 190 | Gulf South | ✅ 2.0% | 1040–1230 | 71% | $18,878 | 7.5 | +25s | 83s | Deep | [Caleb Morgan](mailto:cmorgan@leeuniversity.edu) |
| **[Shorter](https://timhibbard.github.io/xc-cs-college-board/school.html?s=shorter)** | Rome GA | 195 | Conference Carolinas | ✅ 3.4% | 1040–1200 | 96% | $16,646 | — | — | — | Verify | [Anthony Yates](mailto:ayates@shorter.edu) |
| **[Allen University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=allen-university)** | Columbia SC | 115 | SIAC | ❌ none | not reported | 73% | $10,972 | 1 | — | 914s | Caution | [Orinthal Striggles](mailto:ostriggles@allenuniversity.edu) |
| **[Belmont Abbey](https://timhibbard.github.io/xc-cs-college-board/school.html?s=belmont-abbey)** | Belmont NC | 95 | Conference Carolinas | ❌ none | 960–1200 | 75% | $24,639 | 1 | −199s | 136s | Caution | [Dan Finanger](mailto:danielfinanger@bac.edu) |
| **[Benedict](https://timhibbard.github.io/xc-cs-college-board/school.html?s=benedict)** | Columbia SC | 115 | SIAC | ✅ 3.2% | not reported | 96% | $18,250 | 1 | — | — | Caution | [Danny Brooks](mailto:daniel.brooks@benedict.edu) |
| **[Bluefield State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=bluefield-state)** | Bluefield WV | 240 | CIAA | ✅ 1.9% | 870–1080 | 97% | ≈$21,412 | 1 | — | 557s | Caution | [Wesley Arthur](mailto:warthur@bluefieldstate.edu) |
| **[Carson-Newman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=carson-newman)** | Jefferson City TN | 150 | South Atlantic | ✅ 3.1% | 955–1215 | 90% | $20,251 | 1 | — | 289s | Caution | [Brent Borden](mailto:bborden@cn.edu) |
| **[Claflin](https://timhibbard.github.io/xc-cs-college-board/school.html?s=claflin)** | Orangeburg SC | 150 | CIAA | ✅ 3.3% | not reported | 65% | $17,800 | 1 | — | 338s | Caution | [Malcolm Watts](mailto:mawatts@claflin.edu) |
| **[Clayton State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clayton-state)** | Morrow GA | 165 | Peach Belt | ✅ 8.9% | 860–1078 | 68% | ≈$19,717 | 1 | −229s | 183s | Caution | [Chris Brown, OLY](mailto:ChristopherBrown@Clayton.edu) |
| **[Coker](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coker)** | Hartsville SC | 160 | South Atlantic | ✅ 0.0% | not reported | 94% | $20,286 | 1 | — | 302s | Caution | [Eugene Galloway](mailto:egalloway@coker.edu) |
| **[Converse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=converse)** | Spartanburg SC | 35 | Conference Carolinas | ✅ 1.6% | 1010–1250 | 68% | $23,283 | 1 | −188s | 168s | Caution | [Roger Malonda](mailto:roger.malonda@converse.edu) |
| **[Emmanuel (GA)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emmanuel-ga)** | Franklin Springs GA | 70 | Conference Carolinas | ✅ 1.7% | not reported | 74% | $20,925 | 1 | −339s | 210s | Caution | [Jesse Kemmerer](mailto:jesse.kemmerer@ec.edu) |
| **[Emory & Henry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory-and-henry)** | Emory VA | 185 | South Atlantic | ❌ none | 1051–1223 | 84% | $19,061 | 1.5 | −285s | 269s | Caution | [Leroy Worley](mailto:lworley@emoryhenry.edu) |
| **[Erskine](https://timhibbard.github.io/xc-cs-college-board/school.html?s=erskine)** | Due West SC | 40 | Conference Carolinas | ✅ 0.7% | not reported | 63% | $16,525 | 1 | −325s | 251s | Caution | [Dylan Anderson](mailto:danderson@erskine.edu) |
| **[Fort Valley State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fort-valley-state)** | Fort Valley GA | 215 | SIAC | ✅ 4.6% | 930–1070 | 66% | ≈$21,744 | 1 | — | 200s | Caution | [Alexander Jones](mailto:Alexander.jones@fvsu.edu) |
| **[Francis Marion](https://timhibbard.github.io/xc-cs-college-board/school.html?s=francis-marion)** | Florence SC | 190 | Conference Carolinas | ✅ 2.4% | 870–1115 | 86% | $11,386 | 1 | −518s | 312s | Caution | [Mark Bluman](mailto:mbluman@fmarion.edu) |
| **[Georgia College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-college)** | Milledgeville GA | 155 | Peach Belt | ✅ 6.2% | 1070–1230 | 78% | ≈$41,012 | 1.5 | −140s | 115s | Caution | [Alexander Bruno](mailto:alexander.bruno@gcsu.edu) |
| **[Johnson C. Smith](https://timhibbard.github.io/xc-cs-college-board/school.html?s=johnson-c-smith)** | Charlotte NC | 105 | CIAA | ✅ 10.4% | not reported | 45% | $20,894 | 1 | — | 527s | Caution | [Carol Lawrence](mailto:clawrence@jcsu.edu) |
| **[King University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=king-university)** | Bristol TN | 155 | Conf. Carolinas | ✅ 4.7% | not reported | 100% | $22,347 | 1 | — | 230s | Caution | [Jack Brunecz](mailto:jebrunecz@king.edu) |
| **[Lander](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lander)** | Greenwood SC | 55 | Peach Belt | ✅ 3.4% | 950–1178 | 81% | $15,363 | 1 | −406s | 305s | Caution | [Colin Lamb](mailto:clamb@lander.edu) |
| **[Lees-McRae](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lees-mcrae)** | Banner Elk NC | 130 | Conference Carolinas | ❌ none | not reported | 77% | $28,340 | 1.5 | −220s | 244s | Caution | [Ley Fletcher](mailto:fletcherl@lmc.edu) |
| **[Lenoir-Rhyne](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lenoir-rhyne)** | Hickory NC | 90 | South Atlantic | ✅ 3.7% | not reported | 85% | $20,689 | 1 | — | 326s | Caution | [Bob Braman](mailto:robert.braman@lr.edu) |
| **[Lincoln Memorial](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lincoln-memorial)** | Harrogate TN | 190 | South Atlantic | ✅ 1.0% | 1000–1210 | 63% | $20,406 | 1.5 | −161s | 159s | Caution | [Jeff Kavalunas](mailto:jeffrey.kavalunas@lmunet.edu) |
| **[Livingstone](https://timhibbard.github.io/xc-cs-college-board/school.html?s=livingstone)** | Salisbury NC | 145 | CIAA | ✅ 3.4% | not reported | 59% | $13,479 | 1 | −442s | 337s | Caution | [Justin Davis](mailto:jdavis@livingstone.edu) |
| **[Mars Hill](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mars-hill)** | Mars Hill NC | 80 | South Atlantic | ✅ 0.4% | not reported | 68% | $19,910 | 1 | −199s | 155s | Caution | [Carter Benge](mailto:carter_benge@mhu.edu) |
| **[Morehouse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=morehouse)** | Atlanta GA | 165 | SIAC | ✅ 3.8% | ~1090 avg | 44% | $39,013 | 2 | −336s | 352s | Caution | [Christopher Doomes](mailto:christopher.doomes@morehouse.edu) |
| **[Newberry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=newberry)** | Newberry SC | 70 | South Atlantic | ✅ 1.5% | not reported | 90% | $21,656 | 1 | — | 581s | Caution | [Scott Hutchinson](mailto:scott.hutchinson@newberry.edu) |
| **[North Greenville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=north-greenville)** | Tigerville SC | 25 | Conf. Carolinas | ✅ 4.2% | 1060–1240 | 67% | $21,063 | 1 | −397s | 266s | Caution | [Jarvis Robinson](mailto:Jarvis.Robinson@ngu.edu) |
| **[Savannah State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=savannah-state)** | Savannah GA | 250 | SIAC | ✅ 0.9% | not reported | not reported | ≈$21,465 | 1 | — | 642s | Caution | [Ted Whitaker](mailto:whitaket@savannahstate.edu) |
| **[Tusculum](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tusculum)** | Greeneville TN | 125 | South Atlantic | ✅ 0.9% | not reported | 72% | $21,131 | 2 | −158s | 181s | Caution | [Alaric Gwynn](mailto:agwynn@tusculum.edu) |
| **[UVA Wise](https://timhibbard.github.io/xc-cs-college-board/school.html?s=uva-wise)** | Wise VA | 200 | South Atlantic | ✅ 2.3% | 945–1120 | 29% | ≈$25,440 | 1.5 | — | 210s | Caution | [Andrew Howard](mailto:andrewhoward@uvawise.edu) |
| **[Young Harris](https://timhibbard.github.io/xc-cs-college-board/school.html?s=young-harris)** | Young Harris GA | 95 | Conference Carolinas | ❌ none | not reported | 63% | $22,034 | 2 | −102s | 104s | Caution | [Matt Logan](mailto:mjlogan@yhc.edu) |

> **Limestone University (Gaffney SC) closed in 2025** — remove it from any older list.
> **Anderson (SC) CS note:** the federal file shows 5.0% of their bachelor's degrees in computer
> science, which does confirm a real CS pipeline. Their own site leads with a BA in Applied AI and
> a Center for Cybersecurity, so still ask specifically whether the **BS in Computer Science**
> is the degree he would enrol in.

### Division 3 (no athletic scholarships)

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier | Coach |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Berry College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=berry-college)** | Rome GA | 150 | SAA | ✅ 5.8% | 1125–1330 | 64% | $22,320 | 3.5 | −82s | 130s | Target | [Paul Deaton](mailto:pdeaton@berry.edu) |
| **[Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory)** | Atlanta GA | 145 | UAA | ✅ 3.9% | 1470–1550 | 11% | $22,585 | 5 | −20s | 74s | Target | [Linh Nguyen](mailto:linh.nguyen@emory.edu) |
| **[Pfeiffer](https://timhibbard.github.io/xc-cs-college-board/school.html?s=pfeiffer)** | Misenheimer NC | 150 | USA South | ✅ 5.5% | not reported | 96% | $19,076 | 6.5 | −35s | 105s | Target | [Bob Marchinko](mailto:bob.marchinko@pfeiffer.edu) |
| **[Brevard College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=brevard-college)** | Brevard NC | 40 | USA South | ❌ none | 870–1220 | 42% | $23,509 | 1 | — | 332s | Caution | [Matthew Jelley](mailto:jelleymm@brevard.edu) |
| **[Covenant College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=covenant-college)** | Lookout Mtn GA | 200 | Collegiate Conf. of the South | ✅ 1.4% | 1160–1380 | 87% | $26,265 | 1 | −131s | 109s | Caution | [Eli Kaczinski](mailto:eli.kaczinski@covenant.edu) |
| **[Guilford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=guilford)** | Greensboro NC | 180 | ODAC | ✅ 7.2% | 1120–1260 | 80% | $22,270 | 1 | −1059s | 635s | Caution | [Kevin Scola](mailto:kscola@guilford.edu) |
| **[LaGrange](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lagrange)** | LaGrange GA | 230 | Collegiate Conf. of the South | ✅ 0.0% | not reported | 62% | $20,875 | 1 | — | 1344s | Caution | [Cire Campbell](mailto:ecampbell1@lagrange.edu) |
| **[Maryville College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=maryville-college)** | Maryville TN | 145 | Southern Athletic | ✅ 2.8% | not reported | 61% | $19,360 | 1 | −259s | 181s | Caution | [Kaitlyn Carringer-Adams](mailto:kaitlyn.carringeradams@maryvillecollege.edu) |
| **[Methodist](https://timhibbard.github.io/xc-cs-college-board/school.html?s=methodist)** | Fayetteville NC | 235 | USA South | ✅ 4.4% | 1080–1250 | 75% | $24,704 | 1 | — | 1119s | Caution | [William Helms](mailto:whelms@methodist.edu) |
| **[Oglethorpe](https://timhibbard.github.io/xc-cs-college-board/school.html?s=oglethorpe)** | Atlanta GA | 155 | Southern Athletic | ❌ none | 1090–1310 | 88% | $19,509 | 3 | — | 382s | Caution | [Margaret Fox](mailto:mfox1@oglethorpe.edu) |
| **[Piedmont University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=piedmont-university)** | Demorest GA | 100 | USA South | ⚠️ thin | 1038–1245 | 93% | $20,599 | 2 | — | 453s | Caution | [Dr. Remel Williams](mailto:rwilliams@piedmont.edu) |

### NAIA

Not NCAA, which changes the rules rather than the running: NAIA allows **12 scholarships** for
men's XC and track and has looser eligibility rules. Coverage here is known to be incomplete (§2a),
and no NCCAA program is on this list.

| School | Location | Mi | Conf. | CS | SAT | Accept | Net cost/yr | XC slot | vs their 7th | 1–7 spread | Tier | Coach |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **[Montreat](https://timhibbard.github.io/xc-cs-college-board/school.html?s=montreat)** | Montreat NC | 70 | Appalachian Athletic | ✅ 13.9% | not reported | 69% | $27,061 | 3 | — | 228s | Caution | [Jacob Simms](mailto:jacob.simms@montreat.edu) |

Montreat's **13.9% CS degree share** is the third highest on this entire list, and it is the only
non-NCAA program in range that made this list. It has now been measured, and it does not work: he
would arrive as their **#3 of six finishers** on a 228 second spread. That is a Caution, and the
scholarship rules that make NAIA attractive cannot fix a squad that thin. The NAIA gap in §2a is
still the place to look for money, but Montreat itself is answered.

## 5. Schools removed — he would be a walk-on

| School | Div | Conf. | Location | XC slot | vs their 7th | 1–7 spread | Why removed |
|---|---|---|---|---|---|---|---|
| **[Furman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=furman)** | D1 | Southern | Greenville SC | 8 | +79s | 42s | Team best 5000 13:40; nationally elite, ~1:40 gap. Zero miles away with a verified CS degree, which is what makes the cut hurt. Cross country confirms it: they won the Southern Conference with seven runners inside 42 seconds (24:15–24:57) and were 7th at the regional. He would be 70 to 87 seconds outside the scoring seven. |
| **[Georgia Tech](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-tech)** | D1 | ACC | Atlanta GA | — | — | — | 5000 13:41, 10K 29:45. Also the hardest CS admit on the list — GT computing is far more selective than the university's overall rate suggests. |
| **[Wingate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wingate)** | D2 | South Atlantic | Wingate NC | 8 | +34s | 70s | 5000 13:37, 10K 29:20 — the strongest D2 distance program in the region. Cross country is mixed but does not rescue it: at the D2 regional their seven ran 30:48–31:58, about 56 seconds clear of his projection. Kept as a cut on the regional evidence, and this is the school the sign-error correction briefly promoted. |
| **[South Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=south-carolina)** | D1 | SEC | Columbia SC | — | — | — | SEC program, ~105 mi — the in-state flagship. Cut on **level**, not distance: the earlier "out of range" on this row was simply wrong (§2c). No 2025 times transcribed. |
| **[Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia)** | D1 | SEC | Athens GA | — | — | — | SEC program, ~140 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[Tennessee](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tennessee)** | D1 | SEC | Knoxville TN | — | — | — | SEC program, ~145 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[Wake Forest](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wake-forest)** | D1 | ACC | Winston-Salem NC | — | — | — | ACC program, ~175 mi. Cut on level; the earlier "out of range" was wrong (§2c). No 2025 times transcribed. |
| **[UNC Chapel Hill](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-chapel-hill)** | D1 | ACC | Chapel Hill NC | — | — | — | **New at 250 miles** (~250 mi). ACC program with one of the strongest public-university CS departments in the country and a 15% admit rate. Cut on level: their scoring seven is a national-championship-qualifying group. A cut by reputation, not by measurement. |
| **[Duke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=duke)** | D1 | ACC | Durham NC | — | — | — | **New at 250 miles** (~255 mi, so genuinely borderline). ACC program, elite CS, 6% admit. Cut on level and also on admissions — the running is not the binding constraint here. |

**Clemson has left this list**, which is the change worth noting here: it was cut on a 3:43 1500 and a
14:36 5000, and its championship depth puts him at their 7th-to-8th man. It is back on the board at
Deep, 32 miles away (§2e). Furman stays cut and stays the most expensive cut on the board — zero
miles, verified CS — and if a walk-on or redshirt path ever becomes acceptable it goes straight back to
the top on every non-athletic axis.

**Nine cuts, and only three of them are measured.** Furman and Wingate were confirmed by cross country
results; the other seven — Georgia Tech, South Carolina, Georgia, Tennessee, Wake Forest, UNC Chapel
Hill and Duke — are cut **by reputation, on team best track marks or on conference level, with no 2025
times transcribed**. Clemson is the proof that this is not a safe basis for a cut. Of the seven,
**South Carolina at ~105 miles is the one to actually measure**: it is the in-state flagship, in-state
tuition, and nobody has looked at its scoring seven.

**Georgia State and North Georgia are not on this list** — there is no men's program to be removed
from (§2b). Neither are **Mercer, Clark Atlanta, USC Aiken and Winston-Salem State**, which were
measured, ranked, and then removed for sponsoring no men's outdoor track (§2h). Nothing about their
running was the problem, which is why they are not cuts.

## 6. Tiering

**Target — clean development band, concentrate effort here (22).** Nearest first: Southern Wesleyan
(25 mi) · UNC Asheville (62) · UNC Charlotte (100) · Queens (Charlotte) (105) · Davidson (115) ·
Augusta University (115) · Kennesaw State (125) · Catawba (130) · ETSU (140) · Emory (145) ·
Pfeiffer (150) · Berry College (150) · UNC Greensboro (170) · High Point (180) · Elon (200) · West Georgia (210) · UNC Pembroke (215) · Chattanooga (225) · College of Charleston
(235) · Fayetteville State (235) · Coastal Carolina (245) · Campbell (250)

**Deep — just outside the travel squad (5).** Anderson (SC) (30) · Clemson (32) · Appalachian State
(130) · Lee University (190) · Charleston Southern (220)

**Verify — unmeasured (1).** Shorter.

**Caution — he arrives at or ahead of their #1 (49).** Everything else, including the four closest
schools on the board after Southern Wesleyan: North Greenville (25) · USC Upstate (32) · Wofford (32) ·
Converse (35). The full list is in the tables in §4.

**Cut on results or on level (9).** Furman · Georgia Tech · Wingate · South Carolina · Georgia ·
Tennessee · Wake Forest · UNC Chapel Hill · Duke

Seventy-seven schools, **twenty-two of them target tier** — by a wide margin the strongest of the three
metros and the reason this list is the primary one. The comparison worth drawing is with the other two
boards: New York has 28 schools and four targets, Chicago 11 and one. **This ring holds 22 of the 27
targets on the entire board.** The ratio is now a real hit rate rather than an artifact of what had
been measured — v6 reported nine of eighty-one with fifty-seven unknowns, and the honest reading of
that was "nine of the twenty-four measured." The sweep tripled the numerator without changing the
denominator.

Two shapes inside the target tier are worth separating, and the residency correction (§8) makes the
second one much starker. **Eight of the twenty-two are inside 130 miles** — Southern Wesleyan, UNC
Asheville, UNC Charlotte, Queens (Charlotte), Davidson, Augusta, Kennesaw State and Catawba — which is
the list to work first on travel alone. On the federal in-state basis, eight were also under $15,000
and the two lists overlapped at UNC Asheville and Augusta. **On the rate he would actually pay, only
three targets are under $15,000 — Fayetteville State (≈$11,892), Coastal Carolina ($13,966) and UNC
Pembroke (≈$14,260) — and they are 235, 245 and 215 miles out. The overlap is now empty.** Every cheap
target in this ring is a long drive, and every close target is a North Carolina or Georgia public
carrying an $11,900-to-$17,400 non-resident premium, or a private at private prices. The nearest target
under $16,000 is **Southern Wesleyan at 25 miles and $15,464** — a private, so residency never enters
— which makes it the only school in the ring that is both close and cheap, and it is 747 students.

That caution tier still needs care rather than dismissal, and it is now 49 schools deep. Being a
team's #1 is fine *if* the coach is building a class around him — always ask who else they are
signing. It is bad if he trains alone for four years. **Wofford is still the sharpest version:**
strong academics, verified CS, 32 miles, six finishers at their championship, and a team he would lead
on arrival. A handful of Caution schools are genuine near misses where a season either way flips the
reading — **NC A&T (7 seconds ahead of their #1), Lincoln Memorial (2s), UVA Wise (6s), Young Harris
(2s)** — and those are worth an email if something else about the school fits. At the other end,
**LaGrange's 1,344 second first-to-last spread, Methodist's 1,119 and Gardner-Webb's 966** are the
most extreme numbers in this document and mean there is effectively no distance squad to join.

## 7. Top picks

**Rebuilt from the measurement sweep.** Six of these eight were at Verify in v6, so this is a
different list rather than a re-ordering of the old one. Every entry below is measured; the email
address is the coach who would recruit him.

1. **[Southern Wesleyan](https://timhibbard.github.io/xc-cs-college-board/school.html?s=southern-wesleyan)**
   — **25 driving miles from home**, and the running works: **their #4, 105 seconds inside their
   seventh, on a 116 second 1-through-7 spread**. D2, so partial athletic aid genuinely exists, at
   **$15,464 net**. Nothing else on this board combines proximity, a clean development slot and
   scholarship money. Two honest caveats: **2.7% of degrees in CS**, and a **100% admit rate**, which
   means running buys him no admissions leverage — the leverage is all financial. It is also a small
   school (747 undergraduates) in a town of 5,320, so ask where the team runs.
   Email **[Peyton Shelton](mailto:pshelton@swu.edu)**.
2. **[UNC Asheville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-asheville)**
   — 62 miles, Big South, mountain terrain. Confirmed across **two races**: their 6th man at the
   conference meet, 7th at the regional, inside a **64 second 1-through-7 spread**. This is also the
   school that validated the whole method — the direct comparison predicted 6th man before the
   regional results were pulled, and the regional matched. Add a **92% accept rate**. The money is
   the part that changed: its federal net price is $12,250 for a North Carolinian, but on his
   residency it is **≈$29,598** — UNC Asheville charges non-residents $17,348 more in tuition, the
   third-largest premium in this ring. Ask about a non-resident waiver before ranking it on price.
   The other weakness is academic depth: 3.2% of degrees in CS at a 2,910-student campus.
   Email **[Adam Puett](mailto:apuett@unca.edu)**.
3. **[UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte)**
   — the best CS-and-running combination inside 100 miles. Right at their 7th man with a soft **167
   second** back end, a real CS school at **15.2% of degrees**, 80% accept, and **≈$30,688 net on his
   residency** ($15,435 in-state, plus a $15,253 non-resident premium). A large
   university with multiple sections of every CS course, which matters for the lab-conflict problem in
   §9 more than any other item on this list.
   Email **[Riley Macon](mailto:rmacon4@charlotte.edu)**.
4. **[Augusta University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=augusta-university)**
   — the sweep's best find on the academic axis: **15.6% of degrees in computer science, the highest
   share of any school in this ring**, and it is **D2**, so the scholarship money is real. The running
   is comfortable — **their #5, 94 seconds inside the seven**, on a 148 second spread — with an 86%
   admit rate, 115 miles out. v6 could only list it as a hopeful unknown. The money reads worse than
   it used to: $13,787 net is the Georgia-resident figure, and on his residency it is **≈$30,107**,
   a $16,320 premium. At a D2 with real scholarship money that is exactly the gap an offer could
   close, which makes it a concrete question rather than a deal-breaker.
   Email **[Jacob Burgamy](mailto:jburgamy@augusta.edu)**.
5. **[Kennesaw State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kennesaw-state)**
   — D1 CUSA, **11.1% CS**, **≈$26,976 net on his residency** ($15,048 for a Georgian), 69% accept,
   125 miles. **Their #4–5, 82 seconds inside
   the seven**, on a **275 second spread** — the widest back end of any target here, which cuts both
   ways: room to move up, and a squad whose 5th through 7th are a long way off its front. At 41,254
   undergraduates it is the largest school on the board, so he would be one of many; ask what the
   distance group actually looks like.
   Email **[Cale McDaniel](mailto:cmcdan10@kennesaw.edu)**.
6. **[Davidson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=davidson)** — their
   **#4** in the Atlantic 10 seven, and at a **13% accept rate** coach support is real admissions
   leverage. Net price **$17,379**, which is remarkable for a school of its sticker. The caveat is
   depth: their 4th through 7th ran 26:22–26:48 and they failed to field a full scoring team at the
   regional, so the front three are strong and behind that it is thin. Still the highest-value
   *application* on the list — initiate a **pre-read** in spring of junior year.
   Email **[Matt Stuck](mailto:mastuck@davidson.edu)**.
7. **[UNC Greensboro](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-greensboro)**
   — their #4–5 at the conference meet, 7th at the regional, 93 second spread, 89% accept, 7.4% CS.
   **This is the school the residency correction hurts most on this list**: $10,965 net for a North
   Carolinian becomes **≈$27,316** for him, a $16,351 premium, and it loses the cheap-D1 argument that
   put it here. Fayetteville State (≈$11,892) and UNC Pembroke (≈$14,260) are less than half the price
   on his rate, and both are measured targets too — UNCG's remaining case is that it is a D1 with a
   real CS share and a 93 second pack, not that it is cheap.
   Email **[Kaleigh Roach](mailto:k_roach@uncg.edu)**.
8. **[Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory)** — their #5 in a
   **74 second** UAA pack, elite academics, no athletic money but strong need-based aid bringing net
   cost to **$22,585**. An **11% admit**, so the coach's pre-read matters as much as it does at
   Davidson. The federal CS share reads only 3.9%, which understates a strong department at a school
   where most students major in something else.
   Email **[Linh Nguyen](mailto:linh.nguyen@emory.edu)**.

**The money outliers, both now measured and both Target tier.**
**[Fayetteville State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fayetteville-state)**
at **≈$11,892 net on his residency** is the cheapest target-tier school on the entire 116-school
board — its $4,000 non-resident premium is one of the three smallest anywhere on the board — and he
would be their #4–5, 158 seconds inside their seven. But it is 235 miles out, its CS share is 3.3%,
and it is one of two
schools on the board with **no published coach email**, so that one starts with a phone call
(Frank Hyland, number on the school page).
**[UNC Pembroke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-pembroke)** at
**≈$14,260** — also a $4,000 premium — is the better version of the same trade: their #3, 143 seconds
inside the seven, D2 money, 4.8% CS, 215 miles. Email **[Dr. Peter Ormsby](mailto:peter.ormsby@uncp.edu)**.

**One target with a disqualifying question attached.**
**[Queens (Charlotte)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=queens-charlotte)**
fits well on running — their #5, a tight 56 second spread, 105 miles — and the federal file shows **no
bachelor's computer science program at all**. It is the only `❌ none` school at Target tier anywhere on
the board. Check the catalog before anything else; at **$30,857 net** it needs to be right on academics
to justify the price. Email **[Will Crocker](mailto:crockerw@queens.edu)**.

Also worth the email, one tier down: **ETSU** (their #4, soft 171 second middle, and ≈$20,033 on his
residency — a $4,050 premium, among the four smallest in this ring),
**High Point** (7th man twice, 66 second spread, but $38,707), **Catawba** (their #5–6 at D2 with real
scholarship money, $17,879), **Pfeiffer** and **Berry College** (both D3 targets around $19–22k), and
**Chattanooga** and **College of Charleston** further out. **Mercer** was on this line in v7 and is
gone: it measured as a clean target at 185 miles and sponsors no men's outdoor track (§2h). On the Deep tier,
**[Clemson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clemson)** is 32 miles away
at in-state tuition and 15 seconds outside their seven — he would not travel as a freshman, and it is
the one Deep school where a redshirt year is a plausible plan rather than a consolation.
**Anderson (SC)** is 30 miles away and within two seconds of their travel squad.

## 8. Academic and money notes

**Recruitment is an admissions lever at selective schools.** Coaches at Davidson (13%) and Emory
(11%) get supported slots and will run a **pre-read** — send transcript and scores, and admissions
tells the coach informally whether he would get in. This is how running unlocks a school his
stats alone would not. Initiate spring of junior year.

**Where academics are an asset rather than a constraint:** UNC Asheville (92%), Appalachian State
(90%), UNC Greensboro (89%), ETSU (86%), Western Carolina (82%), and most of the D2 list — where
Southern Wesleyan and King University both report a **100%** admit rate. Admission is close to
automatic, so all the leverage shifts to **money**.

**Nine of these schools are South Carolina publics, so the in-state rate applies.** Clemson, Lander,
USC Upstate, Winthrop, SC State, Francis Marion, Coastal Carolina, the College of Charleston and The
Citadel are all quoted at in-state tuition in the tables above; every other public school on the list
is quoted out-of-state. USC Aiken was a tenth until the both-sports rule removed it (§2h). Francis
Marion ($11,386) and USC Upstate ($13,557) are the cheapest of the nine, and both came out of the sweep
at **Caution** — he would be their #1 — so the in-state price does not buy a training group. **Coastal Carolina ($13,966) is the in-state bargain that does**: a
measured Target at their #3–4, 22 seconds inside their seven.

**Thirty-one new Division 2 programs changed the money picture more than the running picture.**
D2 is where partial athletic scholarships live, and on the federal in-state basis the cheapest schools
on this entire board were all D2 additions: **Fayetteville State $7,892, Savannah State $8,172, Clayton
State $8,365, UVA Wise $9,210, UNC Pembroke $10,260**. On the rate he would pay, that list breaks in
half. Fayetteville State (≈$11,892) and UNC Pembroke (≈$14,260) hold up, because North Carolina charges
its non-residents only $4,000 more at both. Savannah State (≈$21,465), Clayton State (≈$19,717) and UVA
Wise (≈$25,440) do not — their premiums are $13,293, $11,352 and $16,230, which puts all three in the
same band as the mid-priced privates they were supposed to undercut. The sweep has now answered whether
any of them is a training environment, and the answer is split the same way by luck: **Fayetteville
State and UNC Pembroke came back at Target tier**, while Savannah State, Clayton State and UVA Wise are
all Caution. Cheap and thin is the common case; cheap and deep exists, twice.

**Academic aid often beats athletic aid.** D1 XC/track is a 12.6-scholarship equivalency spread
across a 35–45 man roster — quarter and half rides, not fulls. A strong student stacking merit aid
at Western Carolina (≈$17,315 on his residency), UNC Greensboro (≈$27,316) or UNC Asheville
(≈$29,598) can land well below the net cost of a bigger athletic offer somewhere expensive — and at
those three the merit aid has to clear a non-resident premium first, which is the whole argument for
asking about waivers early. Western Carolina is the one to notice: a $4,000 premium instead of
$16,000. **Model net cost, not scholarship percentage.** The net figures in this document are federal
averages across all students, not a quote for him; the ones marked ≈ add an estimated non-resident
tuition premium on top of that average (§6 of the
[methodology](https://timhibbard.github.io/xc-cs-college-board/methodology.html#residency)). Treat
them as a ranking tool and get real aid estimates from the schools that survive.

**The three expensive target-tier schools.** Elon ($41,555 net), High Point ($38,707) and Queens
(Charlotte) ($30,857) are all privates, so these are the rates he would pay. They used to look two to
four times the cost of UNCG; on his residency the multiple is closer to 1.1 to 1.5, which is the single
biggest ranking change the residency correction makes in this ring — and
Queens is the one with the unresolved CS question (§7). They are on the list because the running works;
rank them last on money unless something specific offsets it. **Morehouse ($39,013)** is in the same
price band and came back at Caution, which makes it hard to justify on any axis — and Clark Atlanta,
$37,702 at Caution, is off the board entirely for having no men's track (§2h).

### 8a. School size and town size

Two figures now sit beside the money on every school page, and as two extra columns in the master
table on the website — **undergraduate enrollment** (federal, present for all 77) and **town
population** (U.S. Census ACS 2024 5-year, table B01003, for the place the campus actually sits in).
They are collected for this ring only; how big New York and Chicago are is not a question worth a
column.

The median school here has **1,819 undergraduates in a town of 27,636**, and the median hides the
shape of it: **25 of the 77 sit in a place under 10,000 people** and **21 in one over 100,000**,
with not much in between. That is the real texture of a 250-mile ring that reaches both Charlotte
and towns of six hundred.

**Five campuses enroll more undergraduates than their town has residents** — Clemson (23,300 against
Clemson SC's 18,072), UNC Pembroke (5,330 / 2,822), Western Carolina (10,024 / 7,973), Kennesaw State
(41,254 / 34,605) and Montreat (762 / 630), with App State near-parity at 19,444 in a Boone of 20,032.
In those six the school *is* the town. Three of the six are on the ranked lists in §6 and §7 —
Clemson at Deep, Kennesaw State and UNC Pembroke at Target — so this is a live consideration rather
than a curiosity.

At the other end: **Montreat (630), Misenheimer NC (659 — where Pfeiffer's 655 students make school
and town the same size), Franklin Springs GA (1,108), Due West SC (1,177) and Young Harris GA
(1,252)**. For any of them, ask the coach one question: *where does the team run?* A 12-mile long run
out of a town of six hundred is either trails and gravel, which is ideal, or a state highway with no
shoulder, which is not.

Size cuts both ways on the two things that decide this. A small college means a small training group
— fewer people to chase, which is the whole point of §3's framing rule — and it is where the CS
lab-conflict problem in §9 is at its worst. A big state school means depth to chase and multiple lab
sections, and it means being one of forty distance runners competing for a coach's attention rather
than one of eight. The target tier spans the whole range, and even at twenty-two schools the
span is extreme: **Southern Wesleyan, 747 students in a town of 5,320**, and **Kennesaw State, 41,254
in a suburb of Atlanta**, are the same tier and completely different lives. **Catawba (1,235 in
Salisbury)** and **UNC Charlotte (24,453 in a city of 903,844)** are the same comparison one step in
from each end. Whatever the times say, this is the axis to decide on second.

Three caveats before quoting any of these numbers. **Augusta, Macon and Athens are consolidated
city-county governments**, so those figures are county-wide and read larger than the campus
surroundings. **Buies Creek, Cullowhee, Tigerville and Emory VA are census-designated places**, not
incorporated towns, so the boundary is a statistical convenience. And **a small place inside a large
metro describes the address, not the setting** — Morrow GA is 6,364 people and is Atlanta. Read the
town figure next to the *Mi* column, never alone.

All 77, smallest town first. Ratio is undergraduates per resident; bold is a school bigger than its
town.

| School | Div | Undergrads | Town | Town population | Ratio |
|---|---|---|---|---|---|
| [Montreat](https://timhibbard.github.io/xc-cs-college-board/school.html?s=montreat) | NAIA | 762 | Montreat NC | 630 | **1.21×** |
| [Pfeiffer](https://timhibbard.github.io/xc-cs-college-board/school.html?s=pfeiffer) | D3 | 655 | Misenheimer NC | 659 | 0.99× |
| [Emmanuel (GA)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emmanuel-ga) | D2 | 775 | Franklin Springs GA | 1,108 | 0.70× |
| [Erskine](https://timhibbard.github.io/xc-cs-college-board/school.html?s=erskine) | D2 | 766 | Due West SC | 1,177 | 0.65× |
| [Young Harris](https://timhibbard.github.io/xc-cs-college-board/school.html?s=young-harris) | D2 | 755 | Young Harris GA | 1,252 | 0.60× |
| [Emory & Henry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory-and-henry) | D2 | 1,078 | Emory VA | 1,419 | 0.76× |
| [Lees-McRae](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lees-mcrae) | D2 | 873 | Banner Elk NC | 1,473 | 0.59× |
| [Covenant College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=covenant-college) | D3 | 939 | Lookout Mtn GA | 1,721 | 0.55× |
| [North Greenville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=north-greenville) | D2 | 1,819 | Tigerville SC | 1,880 | 0.97× |
| [Piedmont University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=piedmont-university) | D3 | 1,117 | Demorest GA | 2,512 | 0.44× |
| [UNC Pembroke](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-pembroke) | D2 | 5,330 | Pembroke NC | 2,822 | **1.89×** |
| [UVA Wise](https://timhibbard.github.io/xc-cs-college-board/school.html?s=uva-wise) | D2 | 1,101 | Wise VA | 2,916 | 0.38× |
| [Mars Hill](https://timhibbard.github.io/xc-cs-college-board/school.html?s=mars-hill) | D2 | 1,044 | Mars Hill NC | 3,025 | 0.35× |
| [Campbell](https://timhibbard.github.io/xc-cs-college-board/school.html?s=campbell) | D1 | 2,680 | Buies Creek NC | 3,746 | 0.72× |
| [Lincoln Memorial](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lincoln-memorial) | D2 | 1,572 | Harrogate TN | 4,368 | 0.36× |
| [Gardner-Webb](https://timhibbard.github.io/xc-cs-college-board/school.html?s=gardner-webb) | D1 | 1,856 | Boiling Springs NC | 4,757 | 0.39× |
| [Southern Wesleyan](https://timhibbard.github.io/xc-cs-college-board/school.html?s=southern-wesleyan) | D2 | 747 | Central SC | 5,320 | 0.14× |
| [Clayton State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clayton-state) | D2 | 4,348 | Morrow GA | 6,364 | 0.68× |
| [Coker](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coker) | D2 | 840 | Hartsville SC | 7,419 | 0.11× |
| [Presbyterian](https://timhibbard.github.io/xc-cs-college-board/school.html?s=presbyterian) | D1 | 852 | Clinton SC | 7,676 | 0.11× |
| [Brevard College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=brevard-college) | D3 | 815 | Brevard NC | 7,897 | 0.10× |
| [Western Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=western-carolina) | D1 | 10,024 | Cullowhee NC | 7,973 | **1.26×** |
| [Carson-Newman](https://timhibbard.github.io/xc-cs-college-board/school.html?s=carson-newman) | D2 | 1,387 | Jefferson City TN | 8,579 | 0.16× |
| [Fort Valley State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fort-valley-state) | D2 | 2,684 | Fort Valley GA | 8,858 | 0.30× |
| [Bluefield State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=bluefield-state) | D2 | 1,042 | Bluefield WV | 9,387 | 0.11× |
| [Newberry](https://timhibbard.github.io/xc-cs-college-board/school.html?s=newberry) | D2 | 1,479 | Newberry SC | 10,790 | 0.14× |
| [Elon](https://timhibbard.github.io/xc-cs-college-board/school.html?s=elon) | D1 | 6,452 | Elon NC | 11,032 | 0.58× |
| [Claflin](https://timhibbard.github.io/xc-cs-college-board/school.html?s=claflin) | D2 | 1,706 | Orangeburg SC | 13,253 | 0.13× |
| [SC State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=sc-state) | D1 | 2,934 | Orangeburg SC | 13,253 | 0.22× |
| [Belmont Abbey](https://timhibbard.github.io/xc-cs-college-board/school.html?s=belmont-abbey) | D2 | 1,276 | Belmont NC | 15,546 | 0.08× |
| [Tusculum](https://timhibbard.github.io/xc-cs-college-board/school.html?s=tusculum) | D2 | 785 | Greeneville TN | 15,646 | 0.05× |
| [Davidson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=davidson) | D1 | 1,867 | Davidson NC | 15,660 | 0.12× |
| [Georgia College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=georgia-college) | D2 | 5,947 | Milledgeville GA | 16,748 | 0.36× |
| [Clemson](https://timhibbard.github.io/xc-cs-college-board/school.html?s=clemson) | D1 | 23,300 | Clemson SC | 18,072 | **1.29×** |
| [Appalachian State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=appalachian-state) | D1 | 19,444 | Boone NC | 20,032 | 0.97× |
| [Lander](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lander) | D2 | 3,397 | Greenwood SC | 22,536 | 0.15× |
| [Coastal Carolina](https://timhibbard.github.io/xc-cs-college-board/school.html?s=coastal-carolina) | D1 | 10,377 | Conway SC | 27,263 | 0.38× |
| [West Georgia](https://timhibbard.github.io/xc-cs-college-board/school.html?s=west-georgia) | D1 | 7,520 | Carrollton GA | 27,392 | 0.27× |
| [King University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=king-university) | D2 | 908 | Bristol TN | 27,636 | 0.03× |
| [Anderson (SC)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=anderson-sc) | D2 | 3,183 | Anderson SC | 30,051 | 0.11× |
| [LaGrange](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lagrange) | D3 | 636 | LaGrange GA | 32,078 | 0.02× |
| [Maryville College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=maryville-college) | D3 | 1,005 | Maryville TN | 32,392 | 0.03× |
| [Kennesaw State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=kennesaw-state) | D1 | 41,254 | Kennesaw GA | 34,605 | **1.19×** |
| [Catawba](https://timhibbard.github.io/xc-cs-college-board/school.html?s=catawba) | D2 | 1,235 | Salisbury NC | 35,825 | 0.03× |
| [Livingstone](https://timhibbard.github.io/xc-cs-college-board/school.html?s=livingstone) | D2 | 924 | Salisbury NC | 35,825 | 0.03× |
| [Berry College](https://timhibbard.github.io/xc-cs-college-board/school.html?s=berry-college) | D3 | 2,245 | Rome GA | 38,189 | 0.06× |
| [Shorter](https://timhibbard.github.io/xc-cs-college-board/school.html?s=shorter) | D2 | 1,028 | Rome GA | 38,189 | 0.03× |
| [Converse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=converse) | D2 | 1,173 | Spartanburg SC | 38,910 | 0.03× |
| [USC Upstate](https://timhibbard.github.io/xc-cs-college-board/school.html?s=usc-upstate) | D1 | 4,038 | Spartanburg SC | 38,910 | 0.10× |
| [Wofford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=wofford) | D1 | 1,816 | Spartanburg SC | 38,910 | 0.05× |
| [Francis Marion](https://timhibbard.github.io/xc-cs-college-board/school.html?s=francis-marion) | D2 | 2,628 | Florence SC | 40,408 | 0.07× |
| [Lenoir-Rhyne](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lenoir-rhyne) | D2 | 1,359 | Hickory NC | 44,258 | 0.03× |
| [Lee University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=lee-university) | D2 | 2,617 | Cleveland TN | 48,829 | 0.05× |
| [ETSU](https://timhibbard.github.io/xc-cs-college-board/school.html?s=etsu) | D1 | 10,004 | Johnson City TN | 72,222 | 0.14× |
| [Winthrop](https://timhibbard.github.io/xc-cs-college-board/school.html?s=winthrop) | D1 | 3,523 | Rock Hill SC | 75,259 | 0.05× |
| [UNC Asheville](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-asheville) | D1 | 2,910 | Asheville NC | 94,535 | 0.03× |
| [High Point](https://timhibbard.github.io/xc-cs-college-board/school.html?s=high-point) | D1 | 5,129 | High Point NC | 116,245 | 0.04× |
| [Allen University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=allen-university) | D2 | 576 | Columbia SC | 139,643 | 0.00× |
| [Benedict](https://timhibbard.github.io/xc-cs-college-board/school.html?s=benedict) | D2 | 1,536 | Columbia SC | 139,643 | 0.01× |
| [Savannah State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=savannah-state) | D2 | 2,833 | Savannah GA | 147,898 | 0.02× |
| [Charleston Southern](https://timhibbard.github.io/xc-cs-college-board/school.html?s=charleston-southern) | D1 | 2,893 | Charleston SC | 154,338 | 0.02× |
| [College of Charleston](https://timhibbard.github.io/xc-cs-college-board/school.html?s=college-of-charleston) | D1 | 10,558 | Charleston SC | 154,338 | 0.07× |
| [The Citadel](https://timhibbard.github.io/xc-cs-college-board/school.html?s=the-citadel) | D1 | 2,705 | Charleston SC | 154,338 | 0.02× |
| [Chattanooga](https://timhibbard.github.io/xc-cs-college-board/school.html?s=chattanooga) | D1 | 10,074 | Chattanooga TN | 185,783 | 0.05× |
| [Augusta University](https://timhibbard.github.io/xc-cs-college-board/school.html?s=augusta-university) | D2 | 5,613 | Augusta GA | 201,528 | 0.03× |
| [Fayetteville State](https://timhibbard.github.io/xc-cs-college-board/school.html?s=fayetteville-state) | D2 | 5,762 | Fayetteville NC | 210,815 | 0.03× |
| [Methodist](https://timhibbard.github.io/xc-cs-college-board/school.html?s=methodist) | D3 | 1,448 | Fayetteville NC | 210,815 | 0.01× |
| [NC Central](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-central) | D1 | 6,081 | Durham NC | 291,467 | 0.02× |
| [Guilford](https://timhibbard.github.io/xc-cs-college-board/school.html?s=guilford) | D3 | 1,001 | Greensboro NC | 301,198 | 0.00× |
| [NC A&T](https://timhibbard.github.io/xc-cs-college-board/school.html?s=nc-aandt) | D1 | 12,182 | Greensboro NC | 301,198 | 0.04× |
| [UNC Greensboro](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-greensboro) | D1 | 14,062 | Greensboro NC | 301,198 | 0.05× |
| [Emory](https://timhibbard.github.io/xc-cs-college-board/school.html?s=emory) | D3 | 7,298 | Atlanta GA | 505,268 | 0.01× |
| [Morehouse](https://timhibbard.github.io/xc-cs-college-board/school.html?s=morehouse) | D2 | 2,844 | Atlanta GA | 505,268 | 0.01× |
| [Oglethorpe](https://timhibbard.github.io/xc-cs-college-board/school.html?s=oglethorpe) | D3 | 1,352 | Atlanta GA | 505,268 | 0.00× |
| [Johnson C. Smith](https://timhibbard.github.io/xc-cs-college-board/school.html?s=johnson-c-smith) | D2 | 1,244 | Charlotte NC | 903,844 | 0.00× |
| [Queens (Charlotte)](https://timhibbard.github.io/xc-cs-college-board/school.html?s=queens-charlotte) | D1 | 1,211 | Charlotte NC | 903,844 | 0.00× |
| [UNC Charlotte](https://timhibbard.github.io/xc-cs-college-board/school.html?s=unc-charlotte) | D1 | 24,453 | Charlotte NC | 903,844 | 0.03× |

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

The first three items on v6's list — sweep the schools inside 100 miles, then sweep the rest of the
conferences, then rank what comes back — are done. **120 races across 32 championship courses** are now
on file for this ring, covering 76 of the 77 schools, and every one of the 77 now has a **2026
conference-championship 1500** on file as well (§2i). What is left is mostly contact and confirmation
rather than measurement.

1. **Email the eight schools in §7, starting with Southern Wesleyan.** Twenty-five miles, D2 money, a
   clean #4 slot — there is nothing left to look up before writing, and NCAA rules limit when a *coach*
   may initiate, not when he may. Davidson and Emory need a **pre-read** that takes months to arrange,
   so start those in parallel even though they rank 6th and 8th.
2. **Check the Queens (Charlotte) catalog** for a bachelor's computer science program. It is the only
   Target-tier school on the entire board with a `❌ none` CS reading, so this single lookup either adds
   a target 105 miles away or removes one. Then do the other seven `❌ none` schools in §3.
3. **Measure South Carolina.** Of the nine cuts in §5, seven rest on reputation and team best track
   marks with no 2025 times transcribed — and Clemson has just shown what that is worth. South Carolina
   is the one to start with: the in-state flagship, in-state tuition, 105 miles.
4. **Get Shorter's 2025 result** — the last unmeasured school in the ring, D2 Conference Carolinas,
   195 miles.
5. **Close the NAIA/NCCAA gap** listed in §2a — seventeen named programs, in the division with the most
   scholarships and the loosest eligibility rules. Montreat, the one NAIA school on the board, came back
   at Caution, so this gap is still entirely unexplored rather than merely unmeasured.
6. **Calibrate more courses.** Only **one of the 32 courses in this ring** has a correction applied (the
   South Atlantic Conference championship, 96 seconds slow), because a correction requires at least
   three cross-checking teams. This is now the largest remaining source of error here: every school has
   a result, but the results are not all on one scale. The Big South, Southern and South Atlantic
   families agree closely; the Peach Belt, Conference Carolinas, CIAA, SIAC and USA South courses are
   uncalibrated — and several §7 picks sit on them.
7. Confirm a **true BS in Computer Science** (not IT, cybersecurity, or applied AI) at Southern
   Wesleyan, Anderson SC, Presbyterian, North Greenville and USC Upstate — Southern Wesleyan first, since
   it is now the top pick on a 2.7% CS share. And resolve **Piedmont**, whose site has been unreachable
   across several attempts.
8. **Ask the twenty-three schools that entered nobody in their own conference 1500 what happened** (§2i),
   starting with the five at target tier — Elon, Campbell, Chattanooga, College of Charleston and
   Fayetteville State. A program with no man in the conference 1500 either has no milers or does not race
   them there, and the answer decides whether the event he is best at exists at that school.
9. **Ask Winthrop and Wofford what happened.** Two D1 programs inside 100 miles that could not field
   seven finishers at a championship (§2f) is the kind of fact that either has an explanation — injury,
   a young squad — or is the whole story.
10. **Confirm Fayetteville State's and West Georgia's coach contacts by phone.** They are the only two
    schools on the board with no published coach email, and Fayetteville State is the cheapest school on
    the board at Target tier, so it is worth the call.
11. **Verify the driving distance for Campbell, Savannah State and NC Central**, all estimated at exactly
    250 miles and any of which could be outside the ring. Campbell now matters: it came back at Target.
12. Verify SAT figures for the **22 schools reporting no SAT range at all** in the federal file, and an
    admit rate for Savannah State.
13. Ask each coach the CS-lab-conflict question in §9. With 22 targets, this is the question most likely
    to shorten the list quickly.

**Resolved and off this list:** the sweep of the schools inside 100 miles and of every remaining
conference (items 1–2 of v6 — all 56 measurable Verify schools are done, which produced 13 new targets,
one of which — Mercer — was then removed for having no men's track); **the both-sports check**, which was
v7's item 8 and is now done for every school on the board and moved four schools off this ring (§2h);
Kennesaw State, Berry and Guilford, all three of which had been ranked on track marks alone; North
Georgia's phantom program (§2b); Clemson's cut, reversed on its championship depth (§2e); and the coach
contact details, now on all 77 school pages.
