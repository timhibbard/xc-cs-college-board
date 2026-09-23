# -*- coding: utf-8 -*-
"""Write the eight new metro pages.

The chrome is identical on every metro page - KPI row, map card, filters, master table,
off-board tables - so it lives in one template here rather than being copied eight times and
drifting. The prose is written per metro and every number in it comes from that metro's rows
in assets/data.js, checked against metro_digest.py.

Off-board sections are emitted only where that metro actually has such rows, because an
empty table with a heading reads as a data error.
"""
import io
import json
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'

# gen_pages.py concatenates REPO with page names, so it wants the trailing slash form.
REPO = str(REPO) + '/'
b = json.load(open(R + 'board.json'))


def ms(s):
    return s['metro'] if isinstance(s['metro'], list) else [s['metro']]


def rows_in(arr, m):
    return [s for s in b[arr] if m in ms(s)]


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<main class="wrap">

  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="lede">
    {lede}
  </p>

  <div class="kpi-row">
{kpis}  </div>

{callouts}
  <h2>Where they are</h2>
  <div class="map-card">
    <div class="chart-title">Every school in this metro, plotted against the {rmi}-mile radius</div>
    <p class="chart-sub">{mapsub}</p>
    <div class="map-bar">
      <label><input type="checkbox" id="map-showcut" checked> Show schools that are off the board (cut, no men's track, no men's program)</label>
      <span class="count" id="map-count"></span>
    </div>
    <div id="map"></div>
    <div id="map-legend"></div>
    <p class="map-note">
      Pins are approximate main-campus locations. The dashed circle is a straight-line {rmi}-mile
      radius from {centre}, while the table's "Mi" column is driving distance &mdash; so a school
      right on the line can plot just outside it. Filters below drive this map too.
    </p>
  </div>
{chart}
  <h2>The ones worth real effort</h2>
  <div class="prose">
{worth}  </div>

  <h2>Full list</h2>
  <div id="legend-slot"></div>
  <div class="controls">
    <label for="f-tier">Fit</label>
    <select id="f-tier"><option value="all">All</option><option value="target">Target</option><option value="deep">Deep</option><option value="verify">Verify</option><option value="caution">Caution</option></select>
    <input type="search" id="f-q" placeholder="Search school, city, conference" aria-label="Search schools">
    <span class="count" id="count"></span>
  </div>
  <div class="table-scroll">
    <table id="master">
      <caption>Miles are approximate driving distance from {centre}. Click any school for its full page.
        <em>His slot in their 7</em> comes from 2025 championship cross country results;
        <em>vs their 7th</em> is negative when he is inside the seven, and blank where a team never
        finished seven runners. Click a header to sort.</caption>
      <thead></thead><tbody></tbody>
    </table>
  </div>
  <p class="prose" style="margin-top:14px">
    {money}
  </p>

{offboard}
  <div class="prose">
    <p><a href="methodology.html">Methodology and caveats &rarr;</a></p>
  </div>

</main>
<div id="tip" role="status" aria-live="polite"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="assets/data.js"></script>
<script src="assets/app.js"></script>
<script>
initChrome('{id}');
filters.metro = '{id}';

const mine = SCHOOLS.filter(s => inMetro(s, '{id}'));
document.getElementById('k-n').textContent = mine.length;
document.getElementById('k-t').textContent = mine.filter(s => s.tier === 'target').length;
document.getElementById('k-lead').textContent = mine.filter(s => s.xc && s.xc.slot <= 1.5).length;
document.getElementById('legend-slot').innerHTML = tierLegend();
document.getElementById('map-legend').innerHTML = mapLegend();

const TIERLBL = {{ target: 'Target', deep: 'Deep', verify: 'Verify', caution: 'Caution' }};
const byMi = (a, b) => (miIn(a, '{id}') ?? 999) - (miIn(b, '{id}') ?? 999);
const miCell = r => miIn(r, '{id}') ?? '\\u2014';
{offjs}
initMap('{id}');
initTable();
{chartcall}</script>
</body>
</html>
"""

KPI = ('    <div class="kpi"><div class="k-label">%s</div><div class="k-value"%s>%s</div>'
       '<div class="k-sub">%s</div></div>\n')


def kpi(label, val, sub, kid=None):
    return KPI % (label, ' id="%s"' % kid if kid else '', '&mdash;' if kid else val, sub)


CALLOUT = '  <div class="callout%s">\n    <span class="c-title">%s</span>\n%s  </div>\n\n'


def callout(title, *paras, cls=' crit'):
    return CALLOUT % (cls, title, ''.join('    <p>%s</p>\n' % p.strip() for p in paras))


CUT_SEC = """  <h2>Cut as walk-on</h2>
  <p class="prose">{intro}</p>
  <div class="table-scroll">
    <table id="removed"><thead><tr><th scope="col">School</th><th scope="col">Division</th>
      <th scope="col" class="num">Mi</th><th scope="col">Why it was cut</th></tr></thead><tbody></tbody></table>
  </div>

"""

NOTRACK_SEC = """  <h2 id="notrack">Cross country but no men's track</h2>
  <p class="prose">{intro}
    <a href="methodology.html#both-sports">The rule, written out</a>.</p>
  <div class="table-scroll">
    <table id="notrack-tbl"><thead><tr><th scope="col">School</th><th scope="col">Division</th>
      <th scope="col" class="num">Mi</th><th scope="col">Tier it held on cross country</th>
      <th scope="col">What it does and does not sponsor</th></tr></thead><tbody></tbody></table>
  </div>

"""

NOXC_SEC = """  <h2 id="noxc">No men's cross country at all</h2>
  <p class="prose">{intro}</p>
  <div class="table-scroll">
    <table id="noxc-tbl"><thead><tr><th scope="col">School</th><th scope="col">Conference</th>
      <th scope="col" class="num">Mi</th><th scope="col">What it does and does not sponsor</th></tr></thead><tbody></tbody></table>
  </div>

"""

CUT_JS = """
document.querySelector('#removed tbody').innerHTML = REMOVED.filter(r => inMetro(r, '%s'))
  .sort(byMi)
  .map(r => `<tr><td>${r.slug ? `<a class="school" href="school.html?s=${encodeURIComponent(r.slug)}">${r.name}</a>` : r.name}</td>
   <td>${r.div}</td><td class="num">${miCell(r)}</td>
   <td class="rownote" style="max-width:64ch">${r.why}</td></tr>`).join('');
"""

NOTRACK_JS = """
document.querySelector('#notrack-tbl tbody').innerHTML = NO_TRACK.filter(r => inMetro(r, '%s'))
  .sort(byMi)
  .map(r => `<tr><td>${r.slug ? `<a class="school" href="school.html?s=${encodeURIComponent(r.slug)}">${r.name}</a>` : r.name}</td>
   <td>${r.div}</td><td class="num">${miCell(r)}</td>
   <td>${TIERLBL[r.tier] ?? '\\u2014'}${r.xc ? '' : ' <span class="nodata">(unmeasured)</span>'}</td>
   <td class="rownote" style="max-width:56ch">${r.why}</td></tr>`).join('');
"""

NOXC_JS = """
document.querySelector('#noxc-tbl tbody').innerHTML = NO_PROGRAM.filter(r => inMetro(r, '%s'))
  .sort(byMi)
  .map(r => `<tr><td>${r.slug ? `<a class="school" href="school.html?s=${encodeURIComponent(r.slug)}">${r.name}</a>` : r.name}</td>
   <td>${r.conf ?? '\\u2014'}</td><td class="num">${miCell(r)}</td>
   <td class="rownote" style="max-width:64ch">${r.why}</td></tr>`).join('');
"""

CHART_SEC = """
  <h2>Gap to each team's #1 &mdash; the weaker of the two signals</h2>
  <div class="chart-card">
    <div class="chart-title">Projected 15:20 5000m vs. each team's fastest 5000m runner</div>
    <p class="chart-sub">{sub}</p>
    <div class="legend">
      <span class="legend-item"><span class="swatch pos"></span><span>Their #1 is faster &mdash; healthy gap</span></span>
      <span class="legend-item"><span class="swatch neg"></span><span>He is faster than their #1 &mdash; thin squad</span></span>
    </div>
    <svg id="gapchart" role="img" aria-label="Gap between a projected 15:20 5000m and each team's fastest 5000m runner"></svg>
    <p class="chart-sub" id="chart-count" style="margin-top:8px"></p>
  </div>
"""

# The disclosure every new page carries. The board's older pages have coach contacts, track
# marks and a 1500 panel; these rows do not yet, and a page that quietly omitted that would
# read as though the data were complete.
GAPS_NEW = (
    'Every tier on this page comes from <a href="methodology.html#tier-ladder">the published '
    'ladder</a> run over 2025 championship results &mdash; conference, regional and national '
    'meets only. Three things the older metro pages have and this one does not, yet: '
    '<b>no track marks</b>, so there is no 5000m gap chart and no 1500 field here; '
    '<b>no coach names, emails or Instagram handles</b>; and <b>no meet maps</b>. '
    'The one screen that is complete is the both-sports rule &mdash; men\'s outdoor track '
    'sponsorship was checked school by school against the sport list each athletics site '
    'publishes itself, because TFRRS cannot answer it.')


def build(spec):
    m = spec['id']
    M = b['METROS'][m]
    kept = rows_in('SCHOOLS', m)
    off = {'REMOVED': rows_in('REMOVED', m), 'NO_TRACK': rows_in('NO_TRACK', m),
           'NO_PROGRAM': rows_in('NO_PROGRAM', m)}
    sec, js = io.StringIO(), io.StringIO()
    if off['REMOVED']:
        sec.write(CUT_SEC.format(intro=spec['cut']))
        js.write(CUT_JS % m)
    if off['NO_TRACK']:
        sec.write(NOTRACK_SEC.format(intro=spec['notrack']))
        js.write(NOTRACK_JS % m)
    if off['NO_PROGRAM']:
        sec.write(NOXC_SEC.format(intro=spec['noxc']))
        js.write(NOXC_JS % m)

    html = HEAD.format(
        title=spec['title'], desc=spec['desc'], eyebrow=spec['eyebrow'], h1=M['label'],
        lede=spec['lede'], kpis=''.join(spec['kpis']),
        callouts=''.join(spec['callouts']) + callout('What is not on this page yet', GAPS_NEW, cls=''),
        rmi=M['radiusMi'], centre=M.get('centerLabel', M['label']), mapsub=spec['mapsub'],
        chart=CHART_SEC.format(sub=spec['chartsub']) if spec.get('chartsub') else '',
        worth=spec['worth'], money=spec['money'], offboard=sec.getvalue(),
        id=m, offjs=js.getvalue(),
        chartcall='initChart();\n' if spec.get('chartsub') else '')
    open(REPO + M['page'], 'w').write(html)
    print('%-22s %-3d kept  cut %d  notrack %d  noxc %d' % (
        M['page'], len(kept), len(off['REMOVED']), len(off['NO_TRACK']), len(off['NO_PROGRAM'])))


EYE = '20 mile radius · all divisions · new in this pass'
SPECS = []

# ------------------------------------------------------------------ Boston
SPECS.append(dict(
    id='boston',
    title='Boston — sixteen schools within 20 miles',
    desc="Every college within 20 miles of downtown Boston with men's cross country, men's "
         "outdoor track and a computer science degree, in any division. Sixteen schools, and "
         "all three of the best fits admit 11% or fewer.",
    eyebrow=EYE,
    lede="Sixteen schools, which is more than any metro on this board except Greenville, and "
         "<strong>twelve of them are Division 3</strong>. The usual problem is inverted here. The "
         "running works at the top &mdash; three target-tier programs, more than any new metro in "
         "this pass &mdash; but those three are <strong>MIT, Harvard and Tufts</strong>, which "
         "admit 5%, 4% and 11% of applicants. Below them the depth falls away fast: he would "
         "arrive as the <strong>#1 man at ten of the sixteen</strong>, and five never finished "
         "seven runners in a championship at all. In Boston this is an admissions decision "
         "wearing a running decision's clothes.",
    kpis=[kpi('Schools inside 20 mi', None, '3 D1, 1 D2, 12 D3', 'k-n'),
          kpi('Target tier', None, 'MIT, Harvard and Tufts', 'k-t'),
          kpi('He would be their #1 at', None, 'Ten of the sixteen', 'k-lead'),
          kpi('Median net price', '$31,033', 'The most expensive metro on the board')],
    callouts=[
        callout('All three fits are elite-admit schools, and two of them are the cheapest rows here',
                '<strong>MIT</strong> is the strongest single row in this pass: <b>35.2%</b> of its '
                "bachelor's degrees are in computer science &mdash; the highest share on the whole "
                'board &mdash; and across the NEWMAC championship, the Division 3 East regional and '
                'Division 3 nationals he lands as their <b>6th man</b>, 22 seconds inside their '
                'seven. Admit rate <b>5%</b>, average net price <b>$20,111</b>.',
                '<strong>Harvard</strong> measures almost identically to its seventh man &mdash; six '
                'seconds inside it across the Ivy League championship, the Division 1 Northeast '
                'regional and the national championship &mdash; at a <b>4%</b> admit rate and '
                '<b>$19,066</b>, the lowest net price in range. <strong>Tufts</strong> is the third: '
                'four championships on file including Division 3 nationals, 15 seconds inside their '
                'seventh, <b>11%</b> admit, and <b>$39,998</b>, which is nearly the most expensive '
                'row here. Need-based aid is why the two hardest admissions in the metro are also '
                'its two cheapest rows.',
                'The two <em>deep</em> rows are the near misses, and both are Division 1: '
                '<strong>Northeastern</strong> is <b>8 seconds</b> outside its seventh man across '
                'the IC4A, the CAA championship and the Division 1 regional, and <strong>Boston '
                'College</strong> is <b>31</b> outside in the ACC. Neither is out of reach in two '
                'years; both are on the wrong side of the line today.'),
        callout('What caution means in this metro',
                'Eleven of the sixteen rows are <em>caution</em>, and that word is doing real work '
                'here: at ten of them he would be the fastest man on the roster on arrival. '
                '<strong>Five programs never finished seven runners</strong> in a 2025 championship '
                '&mdash; Lesley, UMass Boston, Lasell, Curry and Regis &mdash; so there is no '
                'seventh man to measure against and the ladder falls back to their last finisher. '
                'Lesley is the extreme: he would arrive <b>184 seconds</b> ahead of their #1.',
                '<strong>Wentworth</strong> is the row to understand before writing the metro off. '
                "It is <b>23.9%</b> computer science, 2.7 miles from downtown, and admits "
                '<b>91%</b> &mdash; the accessible version of Boston CS &mdash; but he would arrive '
                'as their <b>#2 man</b>, two seconds behind their #1 and 167 seconds inside their '
                'seventh. That is a place to be the team rather than join one, and at '
                '<b>$34,170</b> it is not cheap.'),
    ],
    mapsub='Sixteen pins, almost all of them inside the city and along the Green Line corridor, '
           'and the three that matter most &mdash; MIT, Harvard and Tufts &mdash; sit within six '
           'miles of the centre. Distance is not the constraint in Boston; admissions is.',
    worth="""    <ol>
      <li><strong>MIT</strong> &mdash; 2.2 miles out, D3 NEWMAC, and the best CS row on the board at
        <b>35.2%</b> of degrees. He is their <strong>6th man</strong>, 22 seconds inside a seven that
        spans 73 seconds, measured across three championships including D3 nationals. Net price
        <b>$20,111</b> against a <b>5%</b> admit rate. Division 3, so there is no athletic money at
        all &mdash; the whole conversation is admissions, and a coach's support in that process is the
        only lever that exists.</li>
      <li><strong>Harvard</strong> &mdash; 5.5 miles out, Ivy League, <b>10.3%</b> CS, and the
        cheapest row in the metro at <b>$19,066</b> on need-based aid. He lands <b>six seconds inside
        their seventh man</b> averaged over the Ivy championship, the Division 1 Northeast regional
        and the national championship, which is as close to exactly-the-right-place as this board
        measures. The Ivy League offers no athletic scholarships either; the admit rate is
        <b>4%</b>.</li>
      <li><strong>Tufts</strong> &mdash; 6 miles, NESCAC, <b>12%</b> CS, four championships on file
        and 15 seconds inside their seventh. The most plausible of the three on admissions at
        <b>11%</b>, and the most expensive at <b>$39,998</b>.</li>
    </ol>
    <p>
      <strong>Two more belong here with an asterisk.</strong> <strong>Northeastern</strong> (D1 CAA,
      2.5 mi, 16% CS, $30,915) and <strong>Boston College</strong> (D1 ACC, 7 mi, $41,704) are both
      <em>deep</em> rather than thin &mdash; 8 and 31 seconds outside their sevenths &mdash; which
      means a real training environment where he would not score early. Northeastern's co-op program
      is a CS-specific reason to take it seriously. <strong>Bentley</strong> is the metro's only
      Division 2 program, so it is the only place partial athletic money exists inside 20 miles
      &mdash; and he would arrive 58 seconds ahead of their #1, which is the trade this metro keeps
      offering.
    </p>""",
    money="<strong>Thirteen of these sixteen schools cannot offer him a dollar of athletic money.</strong> "
          "Twelve are Division 3, where athletic aid does not exist by rule, and Harvard's Ivy League "
          "does not award it either; the only partial-aid door inside 20 miles is <strong>Bentley</strong> "
          "in Division 2. That makes the metro's <b>$31,033</b> median net price &mdash; the highest of "
          "any metro on this board &mdash; mostly a question about need-based and merit aid. The two "
          "cheapest rows are <strong>Harvard at $19,066</strong> and <strong>MIT at $20,111</strong>, "
          "both driven by need-based aid at schools that admit under 6%; the cheapest accessible rows "
          "are <strong>Emmanuel at $26,706</strong>, <strong>Regis at $27,477</strong> and "
          "<strong>Lasell at $27,511</strong>, and all three are caution tier. <strong>UMass Boston is "
          "the only public in range</strong>, so it is the only row where the residency question that "
          "dominates Chicago and Greenville arises at all &mdash; its $39,924 already carries the "
          "non-resident premium <a href=\"methodology.html#residency\">this board adds by hand</a>.",
    notrack="One school in this metro sponsors men's cross country and no men's <em>outdoor track</em>, "
            "which is enough to remove it: he wants both seasons. <strong>Emerson</strong> lists men's "
            "and women's cross country on its athletics site and no track program for anyone.",
))

# ------------------------------------------------------------------ Philadelphia
SPECS.append(dict(
    id='philadelphia',
    title='Philadelphia — fourteen schools within 20 miles',
    desc="Every college within 20 miles of Philadelphia City Hall with men's cross country, men's "
         "outdoor track and a computer science degree. Fourteen schools, four target tier, and the "
         "first email is not the Ivy.",
    eyebrow=EYE,
    lede="Fourteen schools and <strong>four of them target tier</strong>, the best hit rate of any "
         "metro in this pass &mdash; and the one to email first is not the Ivy. <strong>La Salle</strong> "
         "is Division 1 in the Atlantic 10, 6.9 miles from City Hall, admits <strong>97%</strong> of "
         "applicants, costs <strong>$19,409</strong>, and he lands as their seventh man nine seconds "
         "inside it. Penn, Haverford and Swarthmore are the other three targets and between them "
         "admit 5%, 12% and 7%. The two names most people would start with are both off the board: "
         "<strong>Villanova is cut</strong> on the measurement and <strong>Temple</strong> runs cross "
         "country with no men's track.",
    kpis=[kpi('Schools inside 20 mi', None, '3 D1, 3 D2, 8 D3', 'k-n'),
          kpi('Target tier', None, 'La Salle, Penn, Haverford, Swarthmore', 'k-t'),
          kpi('He would be their #1 at', None, 'Half the list', 'k-lead'),
          kpi('Median net price', '$27,316', 'Cheapest of the three big Northeast metros')],
    callouts=[
        callout('La Salle is the most unusual row in this pass',
                'A Division 1 program in the Atlantic 10 that admits <b>97%</b> of applicants, 6.9 '
                'miles from City Hall, at an average net price of <b>$19,409</b> &mdash; and on the '
                'running it is a genuine fit rather than a consolation: across the A10 championship '
                'and the Division 1 Mid-Atlantic regional he lands as their <b>7th man, nine seconds '
                'inside</b> their scoring seven, 79 seconds behind their #1. That combination '
                '&mdash; Division 1, open admissions, sub-$20,000 and a real slot &mdash; does not '
                'appear anywhere else on this board.',
                'Two things to check before ranking it. Its computer science share is <b>3.5%</b> of '
                'degrees, which is thin, so ask what the actual course catalogue and faculty look '
                'like; and it reports <b>no SAT range</b> at all, which usually means test-optional '
                'admissions with a small reporting sample rather than anything sinister.'),
        callout('Villanova and Temple, the two obvious names, are both unavailable',
                '<strong>Villanova</strong> is cut, and not narrowly: their championship seven spans '
                '<b>68 seconds</b> and he arrives <b>73 seconds outside the back of it</b>, 141 '
                'behind their #1. A program that has won national titles in this event; there is no '
                'soft back end to slot into.',
                "<strong>Temple</strong> is the more frustrating row. On the running it is a "
                "<em>target</em> &mdash; their 6th or 7th man, 64 seconds behind their #1 and 31 "
                "inside their seventh across the American championship and the Division 1 regional "
                "&mdash; but its athletics site lists men's cross country, women's cross country and "
                "<b>women's</b> track and field. Men's track and field is gone, which matches the "
                "sports Temple cut in 2013. It is on the no-track list below rather than in the "
                "table, and it is the first row to reopen if cross country alone ever becomes "
                "acceptable."),
    ],
    mapsub='Fourteen pins, tightly packed along the Main Line and the Delaware corridor. The four '
           'targets are spread right across the ring &mdash; Penn at 1.9 miles, La Salle at 6.9, '
           'Haverford at 10.4 and Swarthmore at 16.3 &mdash; so no single part of this metro is the '
           'answer.',
    worth="""    <ol>
      <li><strong>La Salle</strong> &mdash; D1 Atlantic 10, 6.9 mi, <b>97%</b> admit,
        <b>$19,409</b>, and he is their <strong>7th man, 9 seconds inside</strong> the seven. The
        single most actionable row in this pass. Division 1 means equivalency-share athletic money
        exists; ask what a partial share looks like and what the CS department actually offers.</li>
      <li><strong>Penn</strong> &mdash; 1.9 miles from City Hall, Ivy League, <b>7.3%</b> CS,
        <b>$28,699</b> on need-based aid, <b>5%</b> admit. He is their <strong>5th man</strong>,
        seven seconds inside their seven &mdash; a stronger slot than La Salle's, behind a much
        harder door. No athletic scholarships in the Ivy League.</li>
      <li><strong>Haverford</strong> and <strong>Swarthmore</strong> &mdash; the Centennial
        Conference pair, 10.4 and 16.3 miles out, <b>9.5%</b> and <b>11.4%</b> CS, <b>$25,314</b>
        and <b>$23,149</b>, admitting <b>12%</b> and <b>7%</b>. Haverford is the better running fit
        of the two: their <strong>4th man</strong>, 45 seconds inside their seven. Both are Division
        3, so admissions and merit aid are the only levers.</li>
    </ol>
    <p>
      <strong>Three more with an asterisk.</strong> <strong>Saint Joseph's</strong> is the closest
      call on the entire board &mdash; <b>one second</b> outside their seventh man, which is
      <em>deep</em> by a rounding error, at a 89% admit rate and $29,689. <strong>Penn State
      Abington</strong> has the highest CS share on the page at <b>17.6%</b> and admits 97%, but he
      would arrive 13 seconds ahead of their #1. And <strong>Thomas Jefferson</strong> and
      <strong>Rosemont</strong> sit at <em>Verify</em> meaning unmeasured, not borderline: Jefferson's
      only 2025 championship was the Division 2 national meet with a single individual qualifier, and
      Rosemont's most recent men's cross country roster is 2024 with no 2025 schedule and no
      appearance at its conference championship. Confirm Rosemont still fields a team before
      anything else.
    </p>""",
    money="<strong>Three Division 2 programs are the only partial-athletic-money doors inside 20 "
          "miles</strong> &mdash; Thomas Jefferson, Chestnut Hill and Holy Family &mdash; and "
          "<strong>Holy Family is also the cheapest row on the page at $13,143</strong>, though he "
          "would arrive 338 seconds ahead of their #1. Three Division 1 programs (Penn, La Salle, "
          "Saint Joseph's) have equivalency shares and academic aid; the eight Division 3 programs "
          "have neither by rule. The metro median is <b>$27,316</b>, and the practical ladder among "
          "the fits is <strong>La Salle at $19,409</strong>, <strong>Swarthmore at $23,149</strong>, "
          "<strong>Haverford at $25,314</strong> and <strong>Penn at $28,699</strong>. "
          "<strong>Rutgers&ndash;Camden</strong> is the one public in range and the only row where "
          "the residency premium applies &mdash; its $38,257 already includes it.",
    cut="One school, and the measurement is not close. Click through for the full page: the "
        "championship seven that decided it is there, timed runner by runner.",
    notrack="Two schools here sponsor men's cross country and no men's <em>outdoor track</em>. One of "
            "them, Temple, would otherwise be a target-tier Division 1 row 2.3 miles from City Hall "
            "&mdash; which makes this rule the most expensive one on the page. Sponsorship was "
            "checked against the sport list each athletics site publishes itself.",
))

# ------------------------------------------------------------------ Washington
SPECS.append(dict(
    id='washington',
    title='Washington DC — eleven schools in range, seven of them available',
    desc="Every college within 20 miles of downtown Washington with men's cross country, men's "
         "outdoor track and a computer science degree. Eleven in range, four unavailable, and two "
         "genuine targets left.",
    eyebrow=EYE,
    lede="Eleven schools sit inside 20 miles of downtown Washington and <strong>only seven of them "
         "are available to him</strong>. Georgetown is cut on the measurement. George Washington and "
         "Washington Adventist sponsor cross country and no men's track. Maryland sponsors men's "
         "track and <em>not</em> men's cross country. What survives is two genuine targets &mdash; "
         "<strong>American</strong> and <strong>George Mason</strong> &mdash; at $41,943 and $42,383, "
         "which is $12,000 above the metro median. This is the metro where the board's rules cost the "
         "most.",
    kpis=[kpi('Available inside 20 mi', None, '3 D1, 1 D2, 3 D3', 'k-n'),
          kpi('Target tier', None, 'American and George Mason', 'k-t'),
          kpi('Off the board', '4', 'Georgetown, GWU, Washington Adventist, Maryland'),
          kpi('Median net price', '$30,018', 'And the two targets are both above $41,000')],
    callouts=[
        callout('Four of the eleven are unavailable, each for a different reason',
                '<strong>Georgetown</strong> is cut: across the Big East championship, the Division 1 '
                'Mid-Atlantic regional and the national championship he arrives <b>55 seconds outside '
                'their seventh man</b>, past the board\'s 45-second cut line, into a seven that spans '
                'only 97 seconds.',
                "<strong>George Washington</strong> lists men's and women's cross country on its "
                "athletics site and <b>no track and field of any kind</b>, for anyone &mdash; the "
                "running would not have worked either, at 6.6 seconds outside their seventh. "
                "<strong>Washington Adventist</strong> is the same shape in the NAIA and unmeasured "
                "besides. <strong>Maryland</strong> is the reverse: men's indoor and outdoor track "
                "but no men's cross country, and the tell is on its own site, where the most recent "
                "men's cross country roster is <b>2012-13</b>.",
                'That leaves a seven-row table in a metro of five million people, which is worth '
                'knowing before planning a visit around it.'),
        callout('Gallaudet is the cheapest row in range, and unmeasured',
                '<b>$15,845</b> average net price, 3 miles from the centre, <b>4.6%</b> computer '
                'science, and the only university in the world designed from the ground up for deaf '
                'and hard-of-hearing students. On the running there is nothing to measure: seven '
                'races on file across 2025 and 2026, <b>never more than four finishers</b>, and no '
                'championship in either season. <em>Verify</em> here means unmeasured, not '
                'borderline.'),
    ],
    mapsub='Eleven pins including the four off-board ones, and they ring the District tightly '
           '&mdash; six of them inside five miles of the centre. George Mason at 19.8 miles is '
           'right on the line, so the pin can plot just outside the circle.',
    worth="""    <ol>
      <li><strong>American</strong> &mdash; D1 Patriot League, 4.5 miles out, <b>62%</b> admit, and
        on the running he is their <strong>5th or 6th man</strong>, 41 seconds inside their seven and
        65 behind their #1. That is the healthiest measurement on this page. The problem is the
        price: <b>$41,943</b> average net, and a <b>1.8%</b> computer science share that needs a
        hard look at the actual department.</li>
      <li><strong>George Mason</strong> &mdash; D1 Atlantic 10, <b>19.8 miles</b> out and therefore
        the row most sensitive to where you put the centre pin. <b>14.7%</b> CS &mdash; the strongest
        CS row available in this metro &mdash; <b>87%</b> admit, and he lands as their
        <strong>5th man</strong>, 98 seconds inside their seven. At <b>$42,383</b> it is the most
        expensive row on the page, and it is a Virginia public, so that figure already carries the
        non-resident premium.</li>
      <li><strong>Catholic</strong> &mdash; D3 Landmark, 3.2 miles, <b>83%</b> admit, $29,561, and
        he arrives <strong>level with their #1</strong> and 92 seconds inside their seventh. Caution
        tier, and the reason to keep it on the list anyway is location and price rather than
        depth.</li>
    </ol>
    <p>
      <strong>Two on the money question.</strong> <strong>Howard</strong> is Division 1 in the MEAC,
      1.9 miles from the centre, with a <b>41%</b> admit rate &mdash; and at <b>$50,539</b> it is the
      most expensive row on this page by $8,000, with a squad that never finished seven runners.
      <strong>Bowie State</strong> is the only Division 2 program in range, so it is the only place
      partial athletic money exists at all; it is <b>12.1%</b> computer science, and he would arrive
      201 seconds ahead of their #1.
    </p>""",
    money="<strong>The two best fits here are also the two most expensive rows.</strong> American at "
          "<b>$41,943</b> and George Mason at <b>$42,383</b> bracket a metro whose median is "
          "<b>$30,018</b>. George Mason is a Virginia public, so its figure includes the non-resident "
          "premium that <a href=\"methodology.html#residency\">this board adds by hand</a>; Bowie "
          "State is a Maryland public in the same position. The cheapest rows are "
          "<strong>Gallaudet at $15,845</strong>, <strong>Marymount at $29,137</strong> and "
          "<strong>Catholic at $29,561</strong>, and the only partial-athletic-aid door outside "
          "Division 1 is Bowie State in Division 2. Three of "
          "the seven are Division 3, where athletic money does not exist by rule.",
    cut="One school, and it is the biggest name in range. Click through for the championship seven "
        "that decided it.",
    notrack="Two schools here sponsor cross country and no men's <em>outdoor track</em>, including a "
            "Division 1 Atlantic 10 program 1.2 miles from the centre. Sponsorship was checked "
            "against the sport list each athletics site publishes itself.",
    noxc="<strong>Maryland</strong> is the obvious first thought for this metro plus a strong public "
         "computer science department, and it is not available to him: it sponsors men's indoor and "
         "outdoor track and field but not men's cross country. Worth stating plainly rather than "
         "leaving as an absence from a list.",
))

# ------------------------------------------------------------------ Baltimore
SPECS.append(dict(
    id='baltimore',
    title='Baltimore — six schools within 20 miles',
    desc="Every college within 20 miles of downtown Baltimore with men's cross country, men's "
         "outdoor track and a computer science degree. Six schools, and UMBC is the find.",
    eyebrow=EYE,
    lede="Six schools, and <strong>UMBC is the find of this pass</strong>: <strong>26.8%</strong> of "
         "its bachelor's degrees are in computer science &mdash; the highest share on the board "
         "outside MIT &mdash; it is Division 1 in America East, eight miles from downtown, and he "
         "lands as their <strong>6th man</strong>, 41 seconds inside their scoring seven. "
         "<strong>Johns Hopkins</strong> is four seconds the wrong side of its seventh man at a 6% "
         "admit rate. The other four are caution tier, and <strong>Loyola Maryland</strong> &mdash; "
         "where he would arrive level with their #1 &mdash; sponsors no men's track.",
    kpis=[kpi('Schools inside 20 mi', None, '3 D1, 3 D3', 'k-n'),
          kpi('Target tier', None, 'UMBC alone', 'k-t'),
          kpi('He would be their #1 at', None, 'Half the list', 'k-lead'),
          kpi('Median net price', '$24,175', 'Second-cheapest metro in this pass')],
    callouts=[
        callout('UMBC is the best computer-science-plus-running row in this pass',
                '<b>26.8%</b> computer science, Division 1 in America East, <b>72%</b> admit, '
                '<b>$34,486</b> on his residency as a Maryland public, and on the running he is '
                'their <b>6th man</b>, 41 seconds inside their seven and 68 behind their #1. There '
                'is no other row on this board that pairs a CS share above 25% with a target-tier '
                'measurement and an admit rate above 20%.',
                'The one caveat is the price basis: UMBC is a public, so the federal net price is an '
                'in-state figure and the number above adds the non-resident premium '
                '<a href="methodology.html#residency">the way this board does everywhere</a>. A '
                'non-resident waiver or an athletic share would change it materially, and Division 1 '
                'means both exist in principle.'),
        callout('Johns Hopkins, and the two cheap MEAC publics',
                '<strong>Johns Hopkins</strong> is <em>deep</em> by four seconds &mdash; their '
                'seventh man is that close &mdash; with <b>10.5%</b> CS, a <b>$18,809</b> net price '
                'and a <b>6%</b> admit rate. Division 3, so no athletic money; it is an admissions '
                'conversation like Harvard and MIT.',
                '<strong>Coppin State</strong> at <b>$16,901</b> and <strong>Morgan State</strong> '
                'at <b>$25,880</b> are the two Division 1 MEAC publics, 3.5 and 4.6 miles out, and '
                'both are thin: Coppin State never finished seven runners, and at Morgan State he '
                'would arrive level with their #1 and 367 seconds inside their seventh. The money '
                'and the location are real; ask both how many men are signed for the fall.'),
    ],
    mapsub='Six pins, four of them inside five miles of the Inner Harbour. UMBC at 8 miles and '
           'Stevenson at 18.8 are the two that sit out in the county.',
    worth="""    <ol>
      <li><strong>UMBC</strong> &mdash; D1 America East, 8 miles, <b>26.8%</b> CS, <b>72%</b> admit,
        <b>$34,486</b> on his residency, and his <strong>6th man</strong> slot is 41 seconds inside
        their seven. Best row on the page by a distance, and the residency question is the first
        thing to ask the coach.</li>
      <li><strong>Johns Hopkins</strong> &mdash; D3 Centennial, 3.6 miles, <b>10.5%</b> CS,
        <b>$18,809</b>, <b>6%</b> admit, and four seconds outside their seventh man. A real training
        environment where he would not score early, behind a hard admissions door.</li>
      <li><strong>Morgan State</strong> &mdash; D1 MEAC, 4.6 miles, <b>8%</b> CS, <b>82%</b> admit,
        <b>$25,880</b>. Caution tier because he would arrive as their #2 and level with their #1,
        which is a thin squad rather than a bad school; Division 1 money and an open door make it
        worth the email anyway.</li>
    </ol>
    <p>
      <strong>And the row that is not on the list.</strong> <strong>Loyola Maryland</strong> is
      Division 1 in the Patriot League, 4.1 miles from downtown, and he would arrive <em>level with
      their #1</em> &mdash; one second behind &mdash; and 110 seconds inside their seventh. It is on
      the no-track table below because its athletics site publishes a combined cross country section
      and <b>women's</b> track and field only. <strong>Goucher</strong> and
      <strong>Stevenson</strong> round out the page at caution: 14.2 and 18.8 miles, $22,470 and
      $26,505, and he would lead both.
    </p>""",
    money="<strong>Three of these six are Division 1 and three are Division 3, so there is no Division "
          "2 partial-aid door in range at all.</strong> The Division 1 three &mdash; UMBC, Coppin "
          "State and Morgan State &mdash; are all Maryland publics, which means all three carry a "
          "non-resident premium on top of the federal net price and all three can in principle waive "
          "it. The metro median is <b>$24,175</b>, the cheapest rows are <strong>Coppin State at "
          "$16,901</strong> and <strong>Johns Hopkins at $18,809</strong>, and the most expensive is "
          "<strong>UMBC at $34,486</strong> &mdash; which is the same row as the best fit, so the "
          "residency conversation matters more here than anywhere else in this pass.",
    notrack="One school in this metro sponsors men's cross country and no men's <em>outdoor track</em>, "
            "and it is a Division 1 Patriot League program four miles from downtown where he would "
            "have landed level with their #1.",
))

# ------------------------------------------------------------------ Pittsburgh
SPECS.append(dict(
    id='pittsburgh',
    title='Pittsburgh — seven schools within 20 miles, and the best depth on the board',
    desc="Every college within 20 miles of downtown Pittsburgh with men's cross country, men's "
         "outdoor track and a computer science degree. Seven schools, two targets, and every "
         "measured program finished seven runners.",
    eyebrow=EYE,
    lede="Seven schools, and the healthiest depth of any metro on this board: <strong>every one of "
         "the five measured programs finished seven runners in a 2025 championship</strong>, and he "
         "would arrive as the #1 man at only one of the seven. Compare Hampton Roads, where four of "
         "four never finished seven. Two targets sit half a mile and 3.7 miles from downtown "
         "&mdash; <strong>Duquesne</strong> and <strong>Carnegie Mellon</strong> &mdash; and "
         "<strong>Pitt</strong> and <strong>Robert Morris</strong> are both <em>deep</em> rather "
         "than thin. This is what a functioning running metro looks like on this board.",
    kpis=[kpi('Schools inside 20 mi', None, '3 D1, 1 D2, 3 D3', 'k-n'),
          kpi('Target tier', None, 'Duquesne and Carnegie Mellon', 'k-t'),
          kpi('He would be their #1 at', None, 'One of seven — the best ratio on the board', 'k-lead'),
          kpi('Median net price', '$29,954', 'Two targets at $37,730 and $31,944')],
    callouts=[
        callout('Why Pittsburgh reads differently from everywhere else in this pass',
                'The single most common finding on this board is a program that cannot field seven '
                'men. Five of sixteen in Boston, three of fourteen in Philadelphia, four of four in '
                'Hampton Roads. In Pittsburgh it is <b>none of the five</b> measured programs '
                '&mdash; every one of them finished a full scoring seven in a championship &mdash; '
                'and he would lead only Point Park. Two of the seven rows are unmeasured rather than '
                'thin.',
                'That matters more than any individual row here, because depth is the thing a '
                'recruit cannot fix by arriving. A metro where the sevenths are real is a metro '
                'where the tier means what it says.'),
        callout('Carnegie Mellon and Duquesne, half a mile apart in effect',
                '<strong>Carnegie Mellon</strong> is the better combination: <b>18.2%</b> computer '
                'science, 3.7 miles out, <b>$31,944</b>, and on the running their '
                '<b>3rd or 4th man</b>, 51 seconds inside a seven that he would be well into. The '
                'door is <b>12%</b>. <strong>Duquesne</strong> is the accessible one: Division 1 in '
                'the Atlantic 10, <b>0.5 miles</b> from the centre, <b>84%</b> admit, and also their '
                '<b>3rd or 4th man</b>, 52 seconds inside their seven, at <b>$37,730</b> with a '
                '<b>4.2%</b> CS share.',
                'In other words the two targets split the decision cleanly: CMU is the computer '
                'science answer behind a hard door, Duquesne is the running-and-location answer '
                'behind an open one, and the two campuses are three miles apart.'),
    ],
    mapsub='Seven pins and six of them within four miles of the Point &mdash; the tightest cluster '
           'on this board. Robert Morris at 17.9 miles is the only one out of the city.',
    worth="""    <ol>
      <li><strong>Carnegie Mellon</strong> &mdash; D3 UAA, 3.7 miles, <b>18.2%</b> CS, <b>12%</b>
        admit, <b>$31,944</b>, and he lands as their <strong>3rd or 4th man</strong>, 51 seconds
        inside their seven and 35 behind their #1. Division 3 means no athletic money; this is an
        admissions and merit-aid conversation, and the CS department needs no introduction.</li>
      <li><strong>Duquesne</strong> &mdash; D1 Atlantic 10, <b>half a mile</b> from downtown,
        <b>84%</b> admit, <b>$37,730</b>, and the same slot: their <strong>3rd or 4th man</strong>,
        52 seconds inside their seven. Division 1 equivalency shares exist here; the CS share is
        <b>4.2%</b>, so ask about the department directly.</li>
      <li><strong>Pitt</strong> and <strong>Robert Morris</strong> &mdash; both <em>deep</em>, at 38
        and 8 seconds outside their sevenths. Pitt is ACC Division 1, 3 miles out, <b>7.6%</b> CS
        and <b>$49,938</b>, the most expensive row on this page and a Pennsylvania public carrying
        the non-resident premium. Robert Morris is Horizon League Division 1 at 17.9 miles and
        <b>$23,003</b> &mdash; a third of Pitt's price, eight seconds off their seven, and the
        better value of the two by a wide margin.</li>
    </ol>
    <p>
      <strong>Three more to know.</strong> <strong>Point Park</strong> is the metro's only Division 2
      program, so it is the only partial-athletic-money door in range; it admits <b>97%</b>, costs
      <b>$25,942</b>, and he would arrive 120 seconds ahead of their #1. <strong>Carlow</strong> and
      <strong>Chatham</strong> are both <em>Verify</em> meaning unmeasured: Carlow finished one man
      at the AMCC championship and two at the USCAA national meet in the same season, and Chatham's
      entire 2025 record is one invitational with two finishers.
    </p>""",
    money="<strong>Pittsburgh has the widest price spread of any metro in this pass and the two ends "
          "are both Division 1.</strong> <strong>Pitt at $49,938</strong> is the most expensive row; "
          "<strong>Carlow at $20,786</strong> and <strong>Robert Morris at $23,003</strong> are the "
          "cheapest, and Robert Morris is a <em>deep</em>-tier Division 1 program, which makes it the "
          "value row on the page. The median is <b>$29,954</b>. Pitt is a Pennsylvania public and its "
          "figure carries the non-resident premium this board adds by hand; the only Division 2 "
          "partial-aid door is Point Park; the three Division 3 programs (Carnegie Mellon, Carlow, "
          "Chatham) can offer no athletic money by rule.",
    notrack="One school in this metro sponsors cross country and no men's <em>outdoor track</em>, and "
            "it is also the thinnest squad in range by a wide margin.",
))

# ------------------------------------------------------------------ Buffalo
SPECS.append(dict(
    id='buffalo',
    title='Buffalo — six schools within 20 miles, and the cheapest metro on the board',
    desc="Every college within 20 miles of downtown Buffalo with men's cross country, men's outdoor "
         "track and a computer science degree. Six schools, a $21,449 median net price, and one "
         "clear answer.",
    eyebrow=EYE,
    lede="Six schools, the <strong>cheapest metro on this board</strong> at a $21,449 median net "
         "price, and one clear answer: <strong>University at Buffalo</strong>, Division 1 in the "
         "Mid-American, where he lands <strong>two seconds inside their seventh man</strong>. The "
         "metro's other real fit is unavailable &mdash; <strong>Canisius</strong> is a target on the "
         "running and sponsors no track at all &mdash; and two of the remaining rows are unmeasured "
         "rather than thin. Small, cheap, and thinner than it looks.",
    kpis=[kpi('Schools inside 20 mi', None, '1 D1, 2 D2, 2 D3, 1 USCAA', 'k-n'),
          kpi('Target tier', None, 'University at Buffalo alone', 'k-t'),
          kpi('He would be their #1 at', None, 'Three of the six', 'k-lead'),
          kpi('Median net price', '$21,449', 'The cheapest metro on the board')],
    callouts=[
        callout('Canisius is the most painful row in this pass',
                'Division 1 in the MAAC, 3.3 miles from downtown, and on the running one of the best '
                'fits anywhere in this sweep: across three championships he arrives as their '
                '<b>5th man</b>, 86 seconds behind their #1 and <b>48 seconds inside their '
                'seventh</b>, into a seven that spans 134 seconds. Then the sponsorship check: its '
                'athletics site publishes a single combined cross country section and '
                '<b>not one track page</b>, for either gender.',
                'So it sits on the no-track table below rather than at the top of the list. It is '
                'the first row on this whole board to reopen if running cross country only ever '
                'becomes acceptable.'),
        callout('Two of the six rows are unmeasured, not thin',
                '<strong>Bryant &amp; Stratton</strong> is a USCAA college rather than an NCAA or '
                'NAIA one, 0.6 miles from the centre, and the entire men\'s cross country record on '
                'file is <b>two men in one 2026 invitational</b>. At <b>$14,135</b> it is the '
                'cheapest row on the page, and the federal file reports no admit rate and no SAT '
                'range for it at all.',
                "<strong>Hilbert</strong> finished two men at the 2025 AMCC championship and two at "
                "the Division 3 Niagara regional, and its athletics site is a further worry: the "
                "navigation lists neither cross country nor track among its sports, and the most "
                "recent schedules it publishes are <b>fall 2025</b> for cross country and "
                "<b>spring 2025</b> for men's outdoor track. Confirm both sports still exist before "
                "spending time on it."),
    ],
    mapsub='Six pins, five of them within six miles of downtown. University at Buffalo plots at 11.1 '
           'miles on its north campus, which is where the running program is.',
    worth="""    <ol>
      <li><strong>University at Buffalo</strong> &mdash; D1 Mid-American, 11.1 miles, <b>7.9%</b>
        CS, <b>74%</b> admit, <b>$41,595</b> on his residency as a New York public, and he lands
        <strong>two seconds inside their seventh man</strong>, 82 behind their #1. The only
        target-tier row in the metro and the only Division 1 program in it. Its price is also the
        highest here by $19,000, so the non-resident waiver question is the first one to ask.</li>
      <li><strong>Buffalo State</strong> &mdash; D3 SUNYAC, 5.1 miles, <b>5.4%</b> CS, <b>$22,466</b>,
        and he would arrive 35 seconds ahead of their #1 and 261 inside their seventh. Caution tier,
        cheap, and central; a place to be the team rather than join one.</li>
      <li><strong>Daemen</strong> and <strong>D'Youville</strong> &mdash; the two Division 2 programs
        and therefore the only partial-athletic-money doors in range, at <b>$18,693</b> and
        <b>$20,433</b>. Both are thin: he would lead Daemen by 16 seconds and D'Youville by 137, and
        D'Youville never finished seven runners.</li>
    </ol>""",
    money="<strong>This is the cheapest metro on the board and the one target in it is the most "
          "expensive row on the page.</strong> The median is <b>$21,449</b>; University at Buffalo is "
          "<b>$41,595</b> on his residency, because it is a New York public and the federal net price "
          "it reports is an in-state figure to which this board adds the non-resident premium "
          "(<a href=\"methodology.html#residency\">how that works</a>). Everything else in range is "
          "under $23,000: <strong>Bryant &amp; Stratton at $14,135</strong>, <strong>Daemen at "
          "$18,693</strong>, <strong>D'Youville at $20,433</strong>, <strong>Buffalo State at "
          "$22,466</strong> and <strong>Hilbert at $22,723</strong>. The two Division 2 programs are "
          "the only partial-aid doors; the two Division 3 programs can offer nothing by rule.",
    notrack="One school in this metro sponsors cross country and no track of any kind, and on the "
            "running it would have been the best fit in range.",
))

# ------------------------------------------------------------------ Hampton Roads
SPECS.append(dict(
    id='hampton-roads',
    title='Hampton Roads — four schools, and not one finished seven runners',
    desc="Every college within 20 miles of downtown Norfolk with men's cross country, men's outdoor "
         "track and a computer science degree. Four schools, and the thinnest depth on the board.",
    eyebrow=EYE,
    lede="Four schools, and the finding is the same at all four: <strong>not one of them finished "
         "seven runners in a 2025 championship</strong>. Norfolk State's target tier therefore rests "
         "on its last finisher rather than a seventh man, and at the other three he would arrive "
         "ahead of their #1 on the day he enrolled. This is the thinnest metro on the board, and the "
         "honest summary is that it is a place to be someone's #1 rather than a place to develop in "
         "a pack.",
    kpis=[kpi('Schools inside 20 mi', None, '2 D1, 2 D3', 'k-n'),
          kpi('Target tier', None, 'Norfolk State, on its last finisher', 'k-t'),
          kpi('He would be their #1 at', None, 'Three of the four', 'k-lead'),
          kpi('Never finished seven', '4 of 4', 'No other metro on the board reads like this')],
    callouts=[
        callout('What "target" means when nobody finished seven',
                'The board\'s ladder measures him against a team\'s <b>seventh</b> man, because the '
                'seventh is the last scorer and therefore the honest test of whether he would help. '
                'Where a team never finished seven in a championship there is no seventh man, so '
                '<a href="methodology.html#tier-ladder">the same thresholds run on the last finisher '
                'they did produce</a>. Every row on this page is tiered that way.',
                'So read <strong>Norfolk State\'s</strong> target tier as "he fits into the middle of '
                'what they managed to field", not "he is their fifth man". Division 1 in the MEAC, '
                '1.9 miles from downtown, <b>88%</b> admit, <b>$26,784</b>, <b>4.8%</b> computer '
                'science, and 75 seconds behind their #1. Ask how many men are signed for the fall '
                'before ranking it; that single answer decides whether this row is real.'),
        callout('The other three, in order of how close they come',
                "<strong>Hampton</strong> is the nearest thing to a squad: Division 1 in the CAA, 15 "
                "miles out, and he would arrive <b>20 seconds</b> ahead of their #1 &mdash; close "
                "enough that one recruiting class changes the picture. <b>1.8%</b> CS and "
                "<b>$25,319</b>.",
                "<strong>Regent</strong> (D3 Coast-to-Coast, 8.5 miles, <b>38%</b> admit, "
                "<b>$19,923</b>, <b>5.1%</b> CS) and <strong>Virginia Wesleyan</strong> (D3 ODAC, "
                "7.5 miles, <b>$19,676</b>) are both cheap and both thin: 107 and 168 seconds ahead "
                "of their #1 respectively."),
    ],
    mapsub='Four pins across the water from each other &mdash; Norfolk, Virginia Beach and Hampton '
           'are one metro on paper and three drives in practice. The 20-mile circle crosses open '
           'water, so driving distance and the pin positions disagree more here than anywhere else '
           'on the board.',
    worth="""    <ol>
      <li><strong>Norfolk State</strong> &mdash; D1 MEAC, 1.9 miles, <b>88%</b> admit,
        <b>$26,784</b>, <b>4.8%</b> CS. The only target here, measured on a last finisher rather
        than a seventh man, 75 seconds behind their #1. Division 1 means equivalency shares exist,
        and an HBCU in the MEAC with an open door is a real option &mdash; but the first question is
        roster size, not money.</li>
      <li><strong>Hampton</strong> &mdash; D1 CAA, 15 miles, <b>62%</b> admit, <b>$25,319</b>. He
        would be their #1 by 20 seconds, which is the smallest such gap on this page by a factor of
        five. Caution tier today; the row most likely to look different in a year.</li>
      <li><strong>Regent</strong> &mdash; D3 Coast-to-Coast, 8.5 miles, <b>$19,923</b>, and the most
        selective door on the page at <b>38%</b>. No athletic money in Division 3, and he would lead
        them by nearly two minutes.</li>
    </ol>
    <p>
      <strong>There is no Division 2 program inside 20 miles of Norfolk</strong>, so the partial
      athletic-aid door that exists in most metros on this board does not exist here at all: it is
      two Division 1 programs with equivalency shares, and two Division 3 programs with none.
    </p>""",
    money="<strong>Two Division 1 programs and two Division 3 programs, and no Division 2 at "
          "all.</strong> That makes the money picture unusually simple: athletic aid exists at "
          "Norfolk State and Hampton in the form of equivalency shares, and nowhere else in range. "
          "Norfolk State is a Virginia public, so its <b>$26,784</b> includes the non-resident "
          "premium this board adds by hand; Hampton, Regent and Virginia Wesleyan are private and "
          "charge one rate. The two Division 3 rows are the cheapest on the page &mdash; "
          "<strong>Virginia Wesleyan at $19,676</strong> and <strong>Regent at $19,923</strong> "
          "&mdash; and the metro median is <b>$22,621</b>.",
))

# ------------------------------------------------------------------ Newark
SPECS.append(dict(
    id='newark',
    title='Newark — thirteen New Jersey schools, read from the right centre',
    desc="Every college within 20 driving miles of downtown Newark with men's cross country, men's "
         "outdoor track and a computer science degree. Ten available, and NJIT has the highest "
         "computer science share on the board.",
    eyebrow='20 mile radius · New Jersey side · all divisions',
    lede="Thirteen rows, and <strong>twelve of them also appear on the New York page</strong> &mdash; "
         "buried in that list at 3 to 22 miles from Midtown, which is the wrong way to look at them. "
         "From downtown Newark they are 0.5 to 19.5 miles out. <strong>NJIT</strong> is the "
         "headline: <strong>33% of its degrees are in computer science</strong>, the highest share "
         "anywhere on this board, Division 1 in America East, 0.8 miles from the centre, and he "
         "lands as their <strong>3rd man</strong>. Seton Hall is the second target. Then it thins "
         "fast &mdash; he would be the #1 man at <strong>eight of the ten</strong> &mdash; and three "
         "NJAC publics in range sponsor no men's cross country at all.",
    kpis=[kpi('Available inside 20 mi', None, '4 D1, 2 D2, 4 D3', 'k-n'),
          kpi('Target tier', None, 'NJIT and Seton Hall', 'k-t'),
          kpi('He would be their #1 at', None, 'Eight of the ten', 'k-lead'),
          kpi('Median net price', '$28,068', 'Saint Peter’s is $12,199 of it')],
    callouts=[
        callout('Why this page exists when New York already carried these rows',
                'Twelve of these thirteen rows are inside 20 driving miles of downtown Newark '
                '<em>and</em> carried on <a href="new-york.html">the New York page</a> &mdash; the '
                'overlap is deliberate. What changes is the number in front of them. '
                '<strong>Rutgers&ndash;Newark</strong> reads as 13 miles from Midtown and '
                '<b>half a mile</b> from downtown Newark; <strong>Kean</strong> reads as 20 and '
                '<b>6.9</b>; <strong>NJIT</strong> as 12 and <b>0.8</b>. A page anchored on Midtown '
                'ranks them as outliers, and a page anchored on Newark ranks them as a cluster.',
                'Each row calls home whichever centre is actually nearer, which is what the Overview '
                'and its own school page name. Three of the twelve &mdash; Saint Peter\'s, Stevens '
                'Institute and Fairleigh Dickinson &mdash; are nearer Midtown and call New York '
                'home; the rest call Newark home. <strong>Drew</strong> at 16.2 miles is on this '
                'page only.'),
        callout('NJIT and Seton Hall',
                '<strong>NJIT</strong> is the strongest computer science row on the entire board by '
                'share of degrees &mdash; <b>33%</b> &mdash; and it is not a trade-off row: Division '
                '1 in America East, <b>65%</b> admit, <b>$34,194</b> on his residency as a New '
                'Jersey public, and on the running their <b>3rd or 4th man</b>, 125 seconds inside '
                'their scoring seven and 26 behind their #1. The one caution is that a 125-second '
                'margin inside a seven means their back end is soft, so read it as "he would score '
                'immediately", not "he would be pushed".',
                '<strong>Seton Hall</strong> is the tighter squad: Big East Division 1, 4.2 miles, '
                '<b>73%</b> admit, <b>$31,446</b>, and he lands as their <b>4th or 5th man</b>, 47 '
                'seconds inside their seven and 44 behind their #1. A <b>2.4%</b> CS share is the '
                'reason to ask hard questions about the department.'),
        callout('Three New Jersey publics in range sponsor no men’s cross country',
                '<strong>NJCU</strong> (3.3 miles), <strong>Montclair State</strong> (13.6) and '
                '<strong>William Paterson</strong> (19.5) are all NJAC members and none of them '
                'fields a men\'s cross country team: NJCU and William Paterson sponsor women\'s '
                'cross country and men\'s outdoor track, Montclair State sponsors men\'s track and '
                'not cross country. That is three of the conference\'s local footprint gone, and it '
                'is why the NJAC rows that do exist here &mdash; Rutgers&ndash;Newark and Kean '
                '&mdash; are so thin.'),
    ],
    mapsub='Thirteen pins filling the Newark, Jersey City and Passaic corridor. The circle reaches '
           'across the Hudson into Manhattan and Staten Island, but the rule for this page is the '
           'New Jersey side only &mdash; anything across the river is on the New York page, which '
           'already carries it.',
    chartsub='These rows predate this pass, so unlike the other new metro pages they carry 2026 '
             'outdoor track marks and this chart works. Read it second: it compares him to one '
             'athlete per team, which is exactly the mistake that produced this board\'s Loyola '
             'error. Where a cross country result exists, the table below supersedes it.',
    worth="""    <ol>
      <li><strong>NJIT</strong> &mdash; D1 America East, 0.8 miles from downtown, <b>33%</b> CS
        &mdash; the highest share on the board &mdash; <b>65%</b> admit, <b>$34,194</b> on his
        residency, and their <strong>3rd or 4th man</strong>. If one row in the New York area is
        worth a first email, this is it.</li>
      <li><strong>Seton Hall</strong> &mdash; D1 Big East, 4.2 miles, <b>73%</b> admit,
        <b>$31,446</b>, their <strong>4th or 5th man</strong> and 47 seconds inside their seven. The
        better <em>squad</em> of the two targets; the weaker computer science department at
        <b>2.4%</b>.</li>
      <li><strong>Stevens Institute</strong> &mdash; D3 MAC, <b>21.2%</b> CS, <b>48%</b> admit, and
        <b>$41,346</b>, the most expensive row on the page. Caution tier: he would arrive 45 seconds
        ahead of their #1. It calls New York home at 3 miles from Midtown, and it is on this page
        because Hoboken is 10 miles from Newark.</li>
    </ol>
    <p>
      <strong>And the money row.</strong> <strong>Saint Peter's</strong> is Division 1 in the MAAC at
      <b>$12,199</b> &mdash; the cheapest row anywhere in the New York area and a third of what
      Stevens costs &mdash; with a <b>90%</b> admit rate and <b>6.9%</b> CS. He would arrive 31
      seconds ahead of their #1, so it is caution tier, but Division 1 money at that price is worth
      an email regardless of the tier.
    </p>""",
    money="<strong>Four Division 1 programs, two Division 2 and four Division 3, which is the most "
          "balanced money picture in this pass.</strong> The Division 1 four (NJIT, Seton Hall, Saint "
          "Peter's, Fairleigh Dickinson) have equivalency shares and academic aid; Felician and "
          "Caldwell are the Division 2 partial-aid doors; the four Division 3 programs have neither "
          "by rule. <strong>NJIT, Rutgers&ndash;Newark and Kean are New Jersey publics</strong>, so "
          "their figures carry the non-resident premium this board adds by hand "
          "(<a href=\"methodology.html#residency\">how that works</a>) and all three could waive it. "
          "The spread is wide: <strong>Saint Peter's at $12,199</strong> and <strong>Fairleigh "
          "Dickinson at $15,404</strong> at one end, <strong>Stevens at $41,346</strong> and "
          "<strong>Felician at $40,045</strong> at the other, around a <b>$28,068</b> median.",
    noxc="Three New Jersey publics inside 20 miles field no men's cross country team, which is a "
         "quarter of the rows in range. All three are NJAC members; all three sponsor other running "
         "programs, which is why they turn up in searches at all.",
))

for s in SPECS:
    build(s)
