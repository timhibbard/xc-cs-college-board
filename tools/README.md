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
measurement of how thin the squad is rather than an absence of evidence. Six rows were
mislabelled that way — Carlow, Marymount, Hilbert, Greensboro College, William Peace and
**Shorter**, all now `caution` / `tierSrc: 'hand'`. Shorter is the odd one out: its short
championship field is from 2024 and nothing has been added since, so the row is caution for the
squad it last fielded and its note says plainly that the program appears to have stopped racing.

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
| `render-check.js` | Renders three metro pages and every school page with jsdom, and asserts row counts derived from `assets/data.js` plus the totals README.md and methodology.html publish in prose — the board totals, the coach-block count, the Instagram coverage, the 1500 fields and the schedule totals (meets, venues, appearances and the precision split, in all three files that publish them). It also holds every venue inside a bounding box for the state its own string names — a wrong state is a wrong pin however sure the geocoder was, and that check found five. The 1500 block asserts the promise #5 closed on (every row with a `b1500` has a `T1500` to drop his projection into, keyed by **slug** — the one thing issue #5 itself got wrong) rather than only a count, and holds `dslot` against `d15` wherever the seven-man cap does not hide a faster man. Needs `jsdom`: `npm install --no-save jsdom`, or point `NODE_PATH` at an install that has it. |
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

`slugmap.json` is the explicit school-name → TFRRS-slug map, and the most valuable file
in here. **Explicit only — no fuzzy matching.** Fuzzy matching produced confident false
positives once already.

Its failure mode is silence, which #7 demonstrated: **Shorter had no key**, so every pass
skipped it and the row sat at *Verify* — unmeasured — for want of a result that was on file
the whole time. Adding the key was one line; the fix was not. The line bought an
investigation rather than replacing one, because what TFRRS then returned was a program that
has not posted a men's cross country result since October 2024. A missing key looks exactly
like a program that never raced, so when a row has no result, check this file before
believing it.

## Reading a program's Instagram, for the next sweep

Not a script in here — the fetch pass that filled this column was scratch, like the coach pass
before it — but the rule it found is worth keeping, because the obvious approach is wrong.
**Do not count how often a handle appears on a sport page.** Arcadia's men's cross country page
links `arcadia_tf` twelve times and `Arcadia_XC` six, and the twelve are men's *indoor track*: the
frequent handle is the one the site templates into every sport. Ask the page which sport owns the
link instead, in this order:

1. **The sport record.** A Sidearm sport page carries `window.associated_sport`, a JSON object for
   the sport the page is about, with an `instagram` field. Read it and you are done — and an
   *empty* field there is evidence too: it is the school saying the sport has no account.
2. **The link's label.** Both platforms write `aria-label="Men's Cross Country Instagram"` (Presto
   uses a colon: `Cross Country: Instagram`).
3. **The sport navigation block.** Sidearm ships the whole sport menu as JSON, where each sport's
   social links follow that sport's own `title`/`short_name` — so the nearest sport title *above* a
   handle names its owner. Beware the short titles (`M-TF`, `MXC`) and the schedule widgets, whose
   titles (`2026 Men's Cross Country Schedule`) sit between the two and must be skipped.
   PrestoSports needs none of this: it serves one page per sport, so a handle in the navigation of
   `/sports/mxc/` is the men's cross country account.

Two failure modes to expect. A handful of athletics homepages serve an **interstitial** — a
"Gameday" or ticket-drive splash with no sport navigation in it — so fetch the sport path directly
(`/sports/mens-cross-country`, `/sports/mxc/index`) rather than crawling from the homepage. And one
site, Pittsburgh's, renders its social icons with JavaScript *and* points them at a click-tracking
redirect (`/api/v2/promotions/247/click?redirect=…instagram.com/pitt_athletics/`), so the handle is
invisible to `curl` and to a URL-decoded grep alike: it took a headless-Chrome `--dump-dom` plus
`urllib.parse.unquote` to see. Where a rendered copy also shows nothing, that is the finding —
George Mason and Emerson link no Instagram at all, and their pages say so.

## Reading a 1500 field, for the next sweep

Also scratch rather than a script in here, and the reason to write it down is that the obvious
approach is wrong four separate ways. All four produce a plausible number rather than an error.

1. **A results page's round table carries several `TIME` columns, and the page's own CSS hides all
   but one** — `.round_1_<meetid>_65 { display: none !important; }`. The hidden ones hold other
   marks entirely, so reading the first `TIME` column returns a time that is not the 1500. Collect
   the hidden class names from the stylesheet first and keep the one visible `round_*` column.
2. **`heat_*` tables are the prelim runners re-grouped by heat, not extra runners.** Counting them
   doubles the field. A table with more than one visible `round_*` column is one of these.
3. **The final is the round table with an `SC` (score) column**, not the last table on the page. A
   meet with no prelims has exactly one round table, and then `n` and `fn` are equal — the Southern
   Conference at 14 is the shape to expect, not a parse failure.
4. **The decathlon 1500 is a separate event id at the same meet.** At the D1 outdoor championships
   the open 1500 is `6005721` and the decathlon's is `6005746`, both honestly labelled "1500
   Meters". Merging them inflates every field and drops multi-eventers into teams' entrant lists; it
   also makes a program look like it reached a national final in the event. Three of the fourteen rows
   #5 added arrived carrying them.

   **Ask the meet page which events the meet held — do not compare the two races.** The meet page at
   `/results/<mid>` links every event it ran, as `/results/<mid>/<eid>/<Meet_Name>/Mens-1500-Meters`,
   and the decathlon's internal 1500 is never in that list: the decathlon is listed as the decathlon.
   So the test is `eid not in <the meet's 1500 list>`, which needs no times at all. Proven on Ivy
   96712 (open `6000114` listed, dec `6000159` absent, `Mens-Decathlon` = `6000121`) and on Berry
   Field Day 95109 (open `5923306` listed, `5923350` absent).

   The rule #5 used instead — keep the 1500 page with the fastest winning time, or the one with a
   scored (`SC`) round — **is only true at championships.** An invitational that scores nothing has an
   unscored open 1500 too, and at a small April meet a good decathlete can beat the open field. #3
   applied the exact test to 157 meets and dropped 51 marks at 29 events; all 29 of those meets do
   list a decathlon, which is the check that it is not eating real races. It also found that
   **Shorter's only two 1500 marks are both decathlon legs**, so a row already on the site had a
   one-man depth chart that should have been empty.

   Sanity check the whole filter cheaply: print every dropped mark with its meet, then confirm each
   dropped event's meet page also links a `Mens-Decathlon`. A drop at a meet with no multi-event is a
   bug in the event-list regex, not a decathlon.

**Depth charts come from `all_performances/<tfslug>.html?list_hnd=5771&season_hnd=730`** (2026
outdoor; the same parameters work for every division), not from `top_performances`, which looks
right and **silently omits men** — it dropped one of ETSU's eleven and one of West Georgia's
fourteen. Both pages are div grids (`performance-list-row`, fields tagged `data-label="Time"`), not
`<table>`s, so the results-page parser does not work on them; and `all_performances` lists every
performance, so dedupe to one best per athlete id before counting.

**Truncate `b1500` with `floor(round(s * 10, 6)) / 10`, not `int(s * 10)`.** `281.2 - 240` is
`41.199999999999996` in binary, so the bare version writes the tenth *below* the one on the results
page. It did that to four of the 134 rows #5 added before the round() was put in, and the four look
like ordinary marks — nothing about the output says it happened. (Auburn, Samford and Virginia Tech
are rounded rather than truncated for a different reason: they were entered by hand.)

**`dslot` is his rank on the whole squad, not inside the seven `d15` publishes.** That is the bug
`render-check.js` caught in the rows #5 added: the emitter ranked him inside the published seven and
capped six rows at 8, where Virginia Tech's thirteen men under 4:01 put him 14th. `d15` is capped at
the fastest seven; `nath` and `dslot` are not.

## Reading a team's schedule and placing its meets, for the next sweep

Scratch again, and again worth writing down because four of these produce plausible data rather
than an error.

1. **A team page's LATEST RESULTS table holds both sports, and the cross country links have an
   extra path segment.** `/teams/xc/<slug>.html` lists track meets as `/results/<id>` and cross
   country meets as `/results/xc/<id>`, in one table, capped at 50 rows. A link regex of
   `/results/(\d+)` matches the track ones only, and the page then looks like a program that ran no
   cross country at all. Key the meets as `xc-<id>` / `tf-<id>` and keep them apart, because the two
   id spaces overlap.
2. **A meet's season comes off the events it held, not its date.** The meet page links a result per
   event, and some events exist in one season only, so the list decides it. No date rule works: a
   warm-weather program holds outdoor meets in December, and the seasons overlap for a week in March —
   of the fourteen letters this corrected, twelve sit in a five-day window either side of 13 March and
   the other two are a November meet that is outdoor and a December meet that is indoor. Read the
   events out of the **results hrefs** (`/results/<mid>/<eid>/<Meet_Name>/Mens-1500-Meters`), not the
   page's headings — a meet page's only `<h3>` is its own title.

   **Derive the event vocabulary; do not write one down.** The hand-written list used for the 76-row
   sweep was wrong four ways at once, and every one of them yields a plausible letter rather than an
   error. `'500-Meters'` is a substring of `'1500-Meters'`, so a substring test saw an indoor 500 at
   every outdoor meet that ran a 1500. `Heptathlon` is the men's *indoor* multi and the women's
   *outdoor* one, so a gender-blind test points both ways at once — match the whole `Mens-`/`Womens-`
   slug. Three of its indoor markers are contested outdoors (the mile, the distance medley, the
   4×800 at relay meets) and its outdoor 1500 is contested indoors at eight meets in this corpus.
   And the weight throw and the **discus** are not the safe anchors they look like: a fall throws
   series runs the weight throw next to the hammer, and Youngstown State's field house has a discus
   ring, which is the one page in 606 where an indoor 60 and a discus sit together.

   What works is a contingency table. Cross-tabulate every event slug on every cached page against
   the two anchors that cannot be faked — a 60/55 (no outdoor meet contests them) and a javelin or
   hammer (no arena does) — and keep a marker only if it never once lands on the wrong side. That
   leaves 60/55 and their hurdles, the 500, 600 and 1000 indoors; the 100, high hurdles, 400 hurdles,
   4×100, 10,000 and steeplechase, plus the javelin and hammer, outdoors; and the multis by gender.
   Report a page that links no marker rather than guessing: one meet in 503 does, and its letter came
   from the venue being a banked indoor track.
3. **Validate the parse against the rows already on file before splicing anything.** The 76 rows this
   pass added name 248 meets the board already held; reproducing all 248 on date, name and venue
   string is what proves the parser, and it is free. Every venue string that *is* new can then be
   audited on its own.
4. **TFRRS prints a venue three different ways, and one of them is a postal address.** Track pages
   print `Facility - City, ST`; cross country pages print `Stanley Park 577 Western Avenue
   Westfield, MA 01085`, sometimes with a four-digit ZIP (the leading zero dropped), sometimes with a
   ZIP from another state, and occasionally with a county, a street or a campus where the town goes.
   Learn town names from the lines that state one unambiguously, then fall back to the ZIP's town —
   but only when the line's tail actually matches it.
5. **Check the geocoder's answer against the state the venue names, twice.** Ask Nominatim for a
   town *and* require the result's `ISO3166-2-lvl4` to be that state: `University Park, PA` ranks
   Penn State first and a hamlet outside Huntsville, Alabama second, and a place-type filter alone
   takes the hamlet — 700 miles out, flagged as a town centroid, invisible unless you look at the
   map of that one school. Then assert it again over the whole table afterwards:
   `render-check.js` now holds every venue inside a generous bounding box for its own state, which is
   how four older rows placed from a wrong-state ZIP were found.

## Deliberately not moved

`/tmp/render_test.js` was a stub-DOM sweep of the school pages. `render-check.js` does
the same job against real jsdom and asserts its counts, so importing it would have meant
carrying two harnesses that disagree about what "rendered" means. The rest of
`/tmp/sweep/` is one-off scratch — audits, restatements and splices already applied to
`assets/` — plus the fetch caches, which `.gitignore` now covers by convention.
