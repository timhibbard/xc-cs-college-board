#!/usr/bin/env node
/* Renders every page with jsdom and asserts the row counts the data implies.
 *
 * The site has no build step, so nothing else catches a selector that stopped
 * matching or a table that silently renders empty. Every expectation here is
 * derived from assets/data.js rather than hard-coded, so the check tracks the
 * board instead of having to be updated alongside it.
 *
 * Run:  node tools/render-check.js        (needs jsdom; NODE_PATH also works)
 */
const fs = require('fs');
const http = require('http');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
let JSDOM;
try {
  ({ JSDOM } = require('jsdom'));
} catch (e) {
  console.error('render-check needs jsdom:  npm install --no-save jsdom');
  console.error('or point NODE_PATH at an install that has it.');
  process.exit(2);
}

// --- the board's own data, read the same way the pages read it -------------
const ctx = {};
vm.createContext(ctx);
vm.runInContext(
  fs.readFileSync(path.join(ROOT, 'assets/data.js'), 'utf8') + '\n' +
  fs.readFileSync(path.join(ROOT, 'assets/detail.js'), 'utf8') +
  ';__out={SCHOOLS,REMOVED,NO_TRACK,NO_PROGRAM,XCRACES,T1500,ATHLETE,MEETS,VENUES,SCHED,NC_REGIONS,SETTING,SETLINES};', ctx);
const { SCHOOLS, REMOVED, NO_TRACK, NO_PROGRAM, XCRACES, T1500, ATHLETE,
        MEETS, VENUES, SCHED, NC_REGIONS, SETTING, SETLINES } = ctx.__out;

const fails = [];
const checks = [];
function ok(name, got, want) {
  const pass = got === want;
  checks.push({ name, got, want, pass });
  if (!pass) fails.push(`${name}: got ${got}, expected ${want}`);
}

// The pages must be served over http, not read off disk: a file:// document has
// an opaque origin, and the theme toggle's localStorage call throws there, which
// aborts the inline script before any table is built.
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
let PORT = 0;
const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '') || 'index.html';
  const abs = path.join(ROOT, rel);
  if (!abs.startsWith(ROOT) || !fs.existsSync(abs)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': MIME[path.extname(abs)] || 'application/octet-stream' });
  res.end(fs.readFileSync(abs));
});

async function render(file, query) {
  const dom = await JSDOM.fromURL(`http://127.0.0.1:${PORT}/${file}${query || ''}`, {
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
  });
  // Leaflet is a CDN script jsdom will not fetch; the tables do not need it.
  await new Promise(r => {
    if (dom.window.document.readyState === 'complete') return r();
    dom.window.addEventListener('load', r);
    setTimeout(r, 4000);
  });
  return dom;
}

const METROS = [
  ['greenville.html', 'greenville'],
  ['new-york.html', 'nyc'],
  ['chicago.html', 'chicago'],
];

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;

  for (const [file, metro] of METROS) {
    const dom = await render(file);
    const doc = dom.window.document;
    const rows = doc.querySelectorAll('#master tbody tr');
    /* `metro` is an array wherever a school sits in two rings, so this has to match the
       pages' own inMetro() rather than compare against a string. It read `s.metro === metro`
       until the Newark fold left no array rows to catch it out, at which point the check
       started passing for the wrong reason. */
    const want = SCHOOLS.filter(s =>
      (Array.isArray(s.metro) ? s.metro : [s.metro]).includes(metro)).length;
    ok(`${file} board rows`, rows.length, want);
    dom.window.close();
  }

  /* north-carolina.html is the one page whose grouping is data the board holds rather than a
     radius it can recompute, so the grouping is checked both ways: every NC row belongs to
     exactly one NC_REGIONS group, and every name a group lists is a row that exists. A name
     misspelled in NC_REGIONS renders a short table and no error, and a row added to data.js with
     a North Carolina city silently disappears from this page, which is the failure that matters. */
  {
    const isNC = s => / NC$/.test(s.city);
    const ncRows = [...SCHOOLS, ...REMOVED, ...NO_TRACK, ...NO_PROGRAM].filter(isNC);
    const seen = new Map();
    for (const r of NC_REGIONS) for (const n of r.names) seen.set(n, (seen.get(n) || 0) + 1);
    const dup = [...seen].filter(([, c]) => c > 1).map(([n]) => n);
    if (dup.length) fails.push(`NC_REGIONS lists a school in two groups: ${dup.join(', ')}`);
    const names = new Set(ncRows.map(s => s.name));
    const orphanRow = ncRows.filter(s => !seen.has(s.name)).map(s => s.name);
    if (orphanRow.length) {
      fails.push(`North Carolina row in no NC_REGIONS group, so north-carolina.html drops it: ` +
        orphanRow.join(', '));
    }
    const orphanName = [...seen.keys()].filter(n => !names.has(n));
    if (orphanName.length) fails.push(`NC_REGIONS names no row on the board: ${orphanName.join(', ')}`);

    const dom = await render('north-carolina.html');
    const doc = dom.window.document;
    const tables = doc.querySelectorAll('table[data-region]');
    ok('north-carolina region tables', tables.length, NC_REGIONS.length);
    let grouped = 0;
    for (const r of NC_REGIONS) {
      const tbl = doc.querySelector(`table[data-region="${r.id}"]`);
      if (!tbl) { fails.push(`north-carolina.html: no table for region ${r.id}`); continue; }
      const rows = tbl.querySelectorAll('tbody tr').length;
      grouped += rows;
      ok(`north-carolina ${r.id} rows`, rows, SCHOOLS.filter(s => r.names.includes(s.name)).length);
    }
    ok('north-carolina board rows grouped', grouped, SCHOOLS.filter(isNC).length);
    for (const [sel, set] of [['#removed', REMOVED], ['#notrack-tbl', NO_TRACK], ['#noprog-tbl', NO_PROGRAM]]) {
      ok(`north-carolina ${sel} rows`,
        doc.querySelectorAll(`${sel} tbody tr`).length, set.filter(isNC).length);
    }
    dom.window.close();
    /* The card on index.html is filled by hand, because this page has no metro id for the loop
       that fills the other ten to count. A hand-filled number is exactly the kind that goes
       stale, so it is held against the data here. */
    const idxNC = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')
      .match(/id="k-m-north-carolina">(\d+)</);
    if (!idxNC) fails.push('index.html: the North Carolina card no longer publishes a count');
    else ok('index NC card', SCHOOLS.filter(isNC).length, Number(idxNC[1]));
  }

  // Every school page must render its own races, and the count must match.
  const sample = SCHOOLS.filter(s => XCRACES[s.name]);
  for (const s of sample) {
    const dom = await render('school.html', '?s=' + s.slug);
    const doc = dom.window.document;
    const title = (doc.querySelector('h1') || {}).textContent || '';
    if (!title.includes(s.name)) fails.push(`school.html?s=${s.slug}: h1 is "${title.trim()}"`);
    const tables = doc.querySelectorAll('div.race[data-kind="xc"]');
    if (tables.length !== XCRACES[s.name].length) {
      fails.push(`school.html?s=${s.slug}: ${tables.length} race tables, ${XCRACES[s.name].length} races on file`);
    }
    dom.window.close();
  }

  /* The line under the badge says where the tier came from, and it is chosen by a fall-through in
     school.js rather than stored. A row with no aggregate and no stored races falls all the way to
     "unmeasured", which is right for a Verify row and a contradiction of its own badge on any other.
     Shorter is why: its championship field is on file for 2024, the row reads Caution by hand, and
     the page called it unmeasured until it was given a tierTag. These are the only rows that can
     reach that branch, so they are the only ones worth rendering for it. */
  const noEvidence = [...SCHOOLS, ...REMOVED, ...NO_TRACK].filter(
    s => !s.xc && s.b5000 == null && !(XCRACES[s.name] || []).length);
  for (const s of noEvidence) {
    const dom = await render('school.html', '?s=' + s.slug);
    const tag = (dom.window.document.querySelector('.badge-row .src-tag') || {}).textContent || '';
    if (/^\s*unmeasured/.test(tag) && s.tier !== 'verify') {
      fails.push(`school.html?s=${s.slug}: badge says ${s.tier} and the line under it says ` +
        `"unmeasured" — give the row a tierTag saying what the tier does rest on`);
    }
    dom.window.close();
  }

  /* These two were literal 120 and 41 for a long time, which is exactly the thing the header
     above says this file does not do: the board grew to 185 rows and 55 off-board ones and the
     two assertions just failed on every run until they became noise you learned to scroll past.
     Comparing SCHOOLS.length to itself would pass forever and check nothing, so the useful
     version reads the totals README.md publishes in prose and holds them against the data. That
     is the drift that actually happens here — the data file gets a row and the sentences that
     count it are updated by hand, one file at a time, until one of them is missed. */
  const readme = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');
  const byDiv = d => SCHOOLS.filter(s => s.div === d).length;
  // The small divisions are spelled as words in that sentence; everything else is digits.
  const WORD = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 };
  const num = t => (/^\d+$/.test(t) ? Number(t) : WORD[t.toLowerCase()]);
  const head = readme.match(
    /(\d+) schools on it — (\d+) D1, (\d+) D2, (\d+) D3, (\w+) NAIA and (\w+) USCAA —\s*plus (\d+) cut as walk-on, (\d+) with cross country but no men's track, and (\d+) with no men's program/);
  if (!head) {
    fails.push('README.md: the published board totals sentence no longer parses — check tools/render-check.js');
  } else {
    ok('README board total', SCHOOLS.length, num(head[1]));
    ok('README D1 total', byDiv('D1'), num(head[2]));
    ok('README D2 total', byDiv('D2'), num(head[3]));
    ok('README D3 total', byDiv('D3'), num(head[4]));
    ok('README NAIA total', byDiv('NAIA'), num(head[5]));
    ok('README USCAA total', byDiv('USCAA'), num(head[6]));
    ok('README cut-as-walk-on total', REMOVED.length, num(head[7]));
    ok('README no-men\'s-track total', NO_TRACK.length, num(head[8]));
    ok('README no-men\'s-program total', NO_PROGRAM.length, num(head[9]));
  }
  // A truncated or half-parsed data.js is the one failure the derived checks above cannot see,
  // because every expectation would shrink with it. A floor catches that and nothing else.
  if (SCHOOLS.length < 150) fails.push(`SCHOOLS is ${SCHOOLS.length} rows — data.js looks truncated`);

  /* The coach column is the one every page now claims is complete, in prose, on index.html and
     in §6 of the methodology. So hold both halves of that claim against the data: every row with
     a men's program carries a block, and the number §6 publishes is the number of blocks on file.
     A row added without a coach is not a harness failure in itself — it is a sentence that has
     become false, which is the same drift the README totals above are here to catch. */
  const coachRows = [...SCHOOLS, ...REMOVED, ...NO_TRACK, ...NO_PROGRAM].filter(s => s.coach);
  const uncoached = [...SCHOOLS, ...REMOVED, ...NO_TRACK].filter(s => !s.coach).map(s => s.name);
  if (uncoached.length) {
    fails.push(`${uncoached.length} row(s) with a men's program carry no coach block, which index.html ` +
      `and methodology.html §6 both say is impossible: ${uncoached.join(', ')}`);
  }
  // coach.src is the point of the block: without it the name rests on nothing a reader can check.
  const noSrc = coachRows.filter(s => !s.coach.src).map(s => s.name);
  if (noSrc.length) fails.push(`coach block with no src: ${noSrc.join(', ')}`);
  const meth = fs.readFileSync(path.join(ROOT, 'methodology.html'), 'utf8');
  const cm = meth.match(/Each of the (\d+) school pages that has a coach/);
  if (!cm) fails.push('methodology.html: the published coach-page count no longer parses — check tools/render-check.js');
  else ok('methodology coach-block total', coachRows.length, Number(cm[1]));

  /* The Instagram column is the second one the site now claims in prose is finished, so hold it the
     same way. The claim has a shape worth keeping honest: a row with no handle means the school's own
     pages link none, and that only stays true while every row that was never looked up has been. */
  const igRows = [...SCHOOLS, ...REMOVED, ...NO_TRACK, ...NO_PROGRAM].filter(s => s.ig);
  const im = meth.match(/Instagram handles cover (\d+) of the (\d+) schools with a men's program &mdash; (\d+) of the (\d+) on the board/);
  if (!im) {
    fails.push('methodology.html: the published Instagram coverage sentence no longer parses — check tools/render-check.js');
  } else {
    const withProgram = [...SCHOOLS, ...REMOVED, ...NO_TRACK];
    ok('methodology Instagram total', withProgram.filter(s => s.ig).length, Number(im[1]));
    ok('methodology Instagram denominator', withProgram.length, Number(im[2]));
    ok('methodology Instagram on the board', SCHOOLS.filter(s => s.ig).length, Number(im[3]));
    ok('methodology Instagram board denominator', SCHOOLS.length, Number(im[4]));
  }
  // igDept without ig would render a degree sign on nothing; a handle stored as a URL or with an @
  // would render a dead link, because app.js and school.js both interpolate it straight into a path.
  const badIg = igRows.filter(s => !/^[A-Za-z0-9_.]{2,30}$/.test(s.ig)).map(s => `${s.name}: ${s.ig}`);
  if (badIg.length) fails.push(`ig is a bare handle, not a URL: ${badIg.join(', ')}`);
  const orphanDept = [...SCHOOLS, ...REMOVED, ...NO_TRACK, ...NO_PROGRAM]
    .filter(s => s.igDept && !s.ig).map(s => s.name);
  if (orphanDept.length) fails.push(`igDept with no ig: ${orphanDept.join(', ')}`);

  /* The 1500 is the third finished column, and #5 closed it on a specific promise: every row with a
     b1500 has a conference field to drop his projection into. That promise is the whole reason the
     medians on index.html and in README moved — the thirteen rows that were missing a field were the
     thirteen with the fastest 1500s, plus South Carolina, which no query had looked at because it is
     in NO_PROGRAM (men's track, no men's cross country). So assert the promise itself rather than a
     count: a new row with a fast 1500 and no field would put the board back where it was. */
  const everyRow = [...SCHOOLS, ...REMOVED, ...NO_TRACK, ...NO_PROGRAM];
  const noField = everyRow.filter(s => s.b1500 != null && !T1500[s.slug]).map(s => s.name);
  if (noField.length) {
    fails.push(`${noField.length} row(s) have a b1500 and no T1500 field to drop his projection ` +
      `into, which #5 closed and README and methodology.html §7 both state: ${noField.join(', ')}`);
  }
  // T1500 is keyed by slug, not name — the one thing issue #5 itself got wrong. A key that matches
  // no row renders nowhere and is invisible to every other check here.
  const orphan15 = Object.keys(T1500).filter(k => !everyRow.some(s => s.slug === k));
  if (orphan15.length) fails.push(`T1500 key matching no row's slug: ${orphan15.join(', ')}`);
  /* dslot is where his projection lands on the program's whole depth chart — nath men, not the seven
     d15 publishes — so it can exceed 8 and usually does at a program that runs milers. The first
     version of this check read it off d15 and reported twelve failures, six of them real: the rows #5
     added had dslot capped at 8 because the emitter ranked him inside the published seven instead of
     inside the squad. d15 still pins the number whenever the cap hides nobody faster than he is, which
     is the case the emitter got wrong and the only case worth asserting. */
  const P15 = ATHLETE.proj1500;
  for (const [k, T] of Object.entries(T1500)) {
    const d = T.d15 || [];
    if (d.length > 7) fails.push(`T1500.${k}: d15 has ${d.length} marks, capped at 7`);
    if (d.some((t, i) => i && t < d[i - 1])) fails.push(`T1500.${k}: d15 is not sorted`);
    const under = d.filter(t => t < P15).length;
    if (!d.length) {
      if (T.dslot != null) fails.push(`T1500.${k}: dslot is ${T.dslot} with nobody on the depth chart`);
    } else if (under < d.length) {
      // Sorted, so every man past the cap is slower than the slowest published one, hence slower
      // than him: the chart ends here as far as his placing is concerned.
      if (T.dslot !== under + 1) fails.push(`T1500.${k}: dslot is ${T.dslot}, d15 puts him at ${under + 1}`);
    } else if (!(T.dslot >= d.length + 1 && T.dslot <= (T.nath || d.length) + 1)) {
      fails.push(`T1500.${k}: dslot is ${T.dslot}, and all ${d.length} published men beat his ` +
        `projection with ${T.nath} on the chart — it has to fall between ${d.length + 1} and ${(T.nath || d.length) + 1}`);
    }
    if (T.nath != null && d.length && T.nath < d.length) {
      fails.push(`T1500.${k}: nath is ${T.nath} with ${d.length} marks on the depth chart`);
    }
    if (!T.cm || !T.cm.url) fails.push(`T1500.${k}: no conference field`);
  }
  // The published count, in both files that publish it.
  const t15n = Object.keys(T1500).length;
  const rm = readme.match(/the 2026 outdoor 1500 for the (\d+) schools where one/);
  if (!rm) fails.push('README.md: the published T1500 count no longer parses — check tools/render-check.js');
  else ok('README T1500 total', t15n, Number(rm[1]));
  const m7 = meth.match(/for <strong>all (\d+) schools with a 2026 field on file<\/strong>/);
  if (!m7) fails.push('methodology.html §7: the published T1500 count no longer parses — check tools/render-check.js');
  else ok('methodology T1500 total', t15n, Number(m7[1]));
  /* index.html leads the 1500 callout with the programs that entered nobody. It is the figure most
     likely to go stale, because adding a field moves the denominator and not the numerator. */
  const idx = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const im15 = idx.match(/<strong>(\d+) of the (\d+) with a 1500 on file entered nobody/);
  if (!im15) {
    fails.push('index.html: the entered-nobody sentence no longer parses — check tools/render-check.js');
  } else {
    const nobody = Object.values(T1500).filter(T => !T.cm.theirs.length).length;
    ok('index entered-nobody count', nobody, Number(im15[1]));
    ok('index entered-nobody denominator', t15n, Number(im15[2]));
  }

  /* The schedule totals, in the three files that publish them. Every one of these moves whenever a
     pass adds a metro or a season, and none of them is derivable by a reader, so each is parsed back
     out of the prose and compared against the tables it describes. */
  const n = s => Number(s.replace(/,/g, ''));
  const meetIds = Object.keys(MEETS);
  const placed = meetIds.filter(k => MEETS[k].v != null).length;
  const withSched = everyRow.filter(s => SCHED[s.name]);
  const appearances = withSched.reduce((a, s) => a + SCHED[s.name].length, 0);
  /* README counts over the 227 rows with a men's program, methodology over all 243 with a page, and
     the two differ by exactly South Carolina — a row with 22 track meets and no cross country team. */
  const boardRows = [...SCHOOLS, ...REMOVED, ...NO_TRACK].filter(s => SCHED[s.name]);
  const boardApp = boardRows.reduce((a, s) => a + SCHED[s.name].length, 0);
  const prec = { r: 0, z: 0, c: 0 };
  VENUES.forEach(v => prec[v.src]++);

  const rv = readme.match(/`VENUES` \(([\d,]+) places/);
  const rmt = readme.match(/`MEETS` \(([\d,]+) meets keyed/);
  const ra = readme.match(/([\d,]+) appearances across (\d+) of the (\d+) schools with\s*\n?a page/);
  if (!rv || !rmt || !ra) fails.push('README.md: the schedule totals no longer parse — check tools/render-check.js');
  else {
    ok('README venue total', VENUES.length, n(rv[1]));
    ok('README meet total', meetIds.length, n(rmt[1]));
    ok('README appearance total', boardApp, n(ra[1]));
    ok('README rows with a schedule', boardRows.length, Number(ra[2]));
    ok('README page total', SCHOOLS.length + REMOVED.length + NO_TRACK.length, Number(ra[3]));
  }
  const mm = meth.match(/cover (\d+) of the (\d+) rows with a page/);
  const mt = meth.match(/holds <strong>([\d,]+) distinct meets and ([\d,]+) school-meet appearances<\/strong>, of which <strong>([\d,]+) \(/);
  const mv = meth.match(/Of the (\d+) distinct venues, <strong>(\d+) resolved to the facility itself, (\d+) only\s*\n?\s*to the ZIP the results page printed, and (\d+) only/);
  if (!mm || !mt || !mv) fails.push('methodology.html §6a: the schedule totals no longer parse — check tools/render-check.js');
  else {
    ok('methodology rows with a schedule', withSched.length, Number(mm[1]));
    ok('methodology page total', everyRow.length, Number(mm[2]));
    ok('methodology meet total', meetIds.length, n(mt[1]));
    ok('methodology appearance total', appearances, n(mt[2]));
    ok('methodology placed meets', placed, n(mt[3]));
    ok('methodology venue total', VENUES.length, Number(mv[1]));
    ok('methodology venues by facility', prec.r, Number(mv[2]));
    ok('methodology venues by ZIP', prec.z, Number(mv[3]));
    ok('methodology venues by town', prec.c, Number(mv[4]));
  }
  const det = fs.readFileSync(path.join(ROOT, 'assets/detail.js'), 'utf8');
  const dm = det.match(/([\d,]+) of ([\d,]+) meets are\s*\n?\s*placed/);
  if (!dm) fails.push('assets/detail.js: the placed-meet count no longer parses — check tools/render-check.js');
  else {
    ok('detail.js placed meets', placed, n(dm[1]));
    ok('detail.js meet total', meetIds.length, n(dm[2]));
  }
  /* Every id a schedule names has to exist, or a school page drops a meet silently. */
  const orphan = withSched.flatMap(s => SCHED[s.name].filter(k => !MEETS[k]));
  if (orphan.length) fails.push(`SCHED names ${orphan.length} meet id(s) MEETS does not hold: ${orphan.slice(0, 5)}`);

  /* Every venue names its own state, so a pin that lands outside that state is wrong however
     confident the geocoder was. This is not hypothetical: "University Park, PA" ranks Penn State
     first and a hamlet of the same name in Huntsville, Alabama second, and the pass that placed
     the Ashenfelter track took the hamlet — 700 miles out, flagged as a town centroid, and
     invisible on a map zoomed to one school. The boxes are generous on purpose; they catch a
     wrong state, not a wrong street. */
  const BBOX = {
    AL: [30.1, 35.1, -88.5, -84.8], AK: [51.2, 71.5, -180, -129.9], AZ: [31.3, 37.1, -114.9, -109.0],
    AR: [32.9, 36.6, -94.7, -89.6], CA: [32.5, 42.1, -124.5, -114.1], CO: [36.9, 41.1, -109.1, -102.0],
    CT: [40.9, 42.1, -73.8, -71.7], DE: [38.4, 39.9, -75.8, -74.9], DC: [38.7, 39.1, -77.2, -76.8],
    FL: [24.4, 31.1, -87.7, -79.9], GA: [30.3, 35.1, -85.7, -80.7], HI: [18.8, 22.3, -160.3, -154.7],
    ID: [41.9, 49.1, -117.3, -110.9], IL: [36.9, 42.6, -91.6, -87.4], IN: [37.7, 41.8, -88.1, -84.7],
    IA: [40.3, 43.6, -96.7, -90.1], KS: [36.9, 40.1, -102.1, -94.5], KY: [36.4, 39.2, -89.6, -81.9],
    LA: [28.8, 33.1, -94.1, -88.7], ME: [42.9, 47.5, -71.2, -66.9], MD: [37.8, 39.8, -79.5, -75.0],
    MA: [41.1, 42.9, -73.6, -69.8], MI: [41.6, 48.4, -90.5, -82.1], MN: [43.4, 49.5, -97.3, -89.4],
    MS: [30.1, 35.1, -91.7, -88.0], MO: [35.9, 40.7, -95.9, -88.9], MT: [44.3, 49.1, -116.1, -104.0],
    NE: [39.9, 43.1, -104.1, -95.2], NV: [35.0, 42.1, -120.1, -114.0], NH: [42.6, 45.4, -72.6, -70.5],
    NJ: [38.9, 41.4, -75.6, -73.8], NM: [31.3, 37.1, -109.1, -103.0], NY: [40.4, 45.1, -79.8, -71.8],
    NC: [33.7, 36.7, -84.4, -75.4], ND: [45.9, 49.1, -104.1, -96.5], OH: [38.3, 42.1, -84.9, -80.4],
    OK: [33.6, 37.1, -103.1, -94.4], OR: [41.9, 46.4, -124.7, -116.4], PA: [39.6, 42.4, -80.6, -74.6],
    RI: [41.1, 42.1, -71.9, -71.0], SC: [32.0, 35.3, -83.4, -78.4], SD: [42.4, 46.0, -104.1, -96.4],
    TN: [34.9, 36.8, -90.4, -81.6], TX: [25.8, 36.6, -106.7, -93.4], UT: [36.9, 42.1, -114.1, -108.9],
    VT: [42.7, 45.1, -73.5, -71.4], VA: [36.5, 39.5, -83.7, -75.1], WA: [45.5, 49.1, -124.8, -116.9],
    WV: [37.1, 40.7, -82.7, -77.6], WI: [42.4, 47.4, -92.9, -86.7], WY: [40.9, 45.1, -111.1, -104.0],
  };
  const stray = VENUES.filter(v => {
    const st = (v.v.match(/ ([A-Z]{2})$/) || [])[1];
    const b = BBOX[st];
    if (!b) return true;
    return !(v.lat >= b[0] && v.lat <= b[1] && v.lon >= b[2] && v.lon <= b[3]);
  });
  if (stray.length) {
    fails.push(`${stray.length} venue(s) placed outside the state they name: ` +
      stray.map(v => `${v.v} at ${v.lat},${v.lon}`).join(' | '));
  }

  /* And it has to reach the page. Every meet on file is one card, so the count is the check: the
     conference field plus any postseason rounds. This also covers the rows the loop above skips —
     South Carolina has no cross country result at all and still has a 1500 section. */
  for (const s of everyRow.filter(s => T1500[s.slug])) {
    const dom = await render('school.html', '?s=' + s.slug);
    const cards = dom.window.document.querySelectorAll('div.race[data-kind="t1500"]');
    const want = 1 + (T1500[s.slug].post || []).length;
    if (cards.length !== want) {
      fails.push(`school.html?s=${s.slug}: ${cards.length} 1500 cards, ${want} meets on file`);
    }
    dom.window.close();
  }

  /* ---------- campus setting, the errands axis (#13) ----------

     SETTING is keyed by name and SETLINES by slug, which is the one thing that can rot here:
     rename a row and the setting silently belongs to nobody. Both directions are checked,
     because a stale key is as wrong as a missing one and neither throws on its own. */
  const everyName = new Set(everyRow.map(s => s.name));
  ok('SETTING rows', Object.keys(SETTING).length, everyRow.length);
  ok('SETTING rows with a Walk Score',
    Object.values(SETTING).filter(g => g.walk != null).length, everyRow.length);
  for (const name of Object.keys(SETTING)) {
    if (!everyName.has(name)) fails.push(`SETTING has "${name}", which is not a row on the board`);
  }
  for (const s of everyRow) {
    if (!SETTING[s.name]) fails.push(`${s.name}: no SETTING entry — run tools/apply_setting.py`);
  }
  const bySlug = new Map(everyRow.filter(s => s.slug).map(s => [s.slug, s]));
  for (const slug of Object.keys(SETLINES)) {
    if (!bySlug.has(slug)) fails.push(`SETLINES has "${slug}", which is not a row's slug`);
  }
  /* The counts in data.js and the lists in detail.js come off the same page in the same pass,
     so a disagreement means one of the two files was written by an older run. This is the check
     that catches a half-applied splice, which is the failure apply_setting.py can produce. */
  for (const s of everyRow) {
    const g = SETTING[s.name], L = (s.slug && SETLINES[s.slug]) || {};
    if (!g) continue;
    if (g.walk != null && (g.walk < 0 || g.walk > 100)) {
      fails.push(`${s.name}: Walk Score ${g.walk} is outside 0-100`);
    }
    if (!['address', 'approx', 'town'].includes(g.lvl)) {
      fails.push(`${s.name}: setting lvl "${g.lvl}" is not address, approx or town`);
    }
    if (!/^https:\/\/www\.walkscore\.com\/score\//.test(g.ws || '')) {
      fails.push(`${s.name}: setting has no walkscore.com source url`);
    }
    if (!s.slug) continue;
    const rail = (L.rail || []).length, bus = (L.bus || []).length;
    if (rail !== g.railN || bus !== g.busN) {
      fails.push(`${s.name}: SETTING says ${g.railN} rail / ${g.busN} bus, SETLINES holds ` +
        `${rail} / ${bus} — data.js and detail.js were written by different runs`);
    }
  }

  /* One page rendered per level, because the caveat sentence is chosen by that field and the
     two rarer branches are exactly the ones nobody would notice were broken: 230 rows read
     "address" and the other two branches cover 13 between them. */
  for (const lvl of ['address', 'approx', 'town']) {
    const s = everyRow.find(r => r.slug && SETTING[r.name] && SETTING[r.name].lvl === lvl);
    if (!s) { fails.push(`no row with setting lvl "${lvl}" to render`); continue; }
    const dom = await render('school.html', '?s=' + s.slug);
    const doc = dom.window.document;
    const h2 = [...doc.querySelectorAll('h2')].map(h => h.textContent.trim());
    if (!h2.includes('Setting')) fails.push(`school.html?s=${s.slug}: no Setting section`);
    const txt = doc.body.textContent;
    if (!txt.includes('walkscore.com')) {
      fails.push(`school.html?s=${s.slug}: Setting section does not attribute Walk Score`);
    }
    /* The promise the whole section is built on: it must say it is only the errands half. */
    if (!/one axis of two/i.test(txt)) {
      fails.push(`school.html?s=${s.slug}: Setting section does not say it is one axis of two`);
    }
    dom.window.close();
  }

  /* A template hole that reads a missing field prints the word "undefined" into the prose and
     nothing throws, which is how "scored on the campus's own street address, undefined mi from
     the coordinate this board holds" reached a rendered page. Two rows had no map-tile
     coordinate to measure and every other row had one, so the branch was invisible in testing.
     Sweeping the rows most likely to have a hole is cheap; sweeping all 180 is not. */
  const holey = [
    ...everyRow.filter(s => s.slug && SETTING[s.name] && SETTING[s.name].off == null),
    ...everyRow.filter(s => s.slug && SETTING[s.name] && SETTING[s.name].bike == null).slice(0, 3),
    ...everyRow.filter(s => s.slug && SETTING[s.name] && SETTING[s.name].town == null).slice(0, 3),
  ];
  for (const s of holey) {
    const dom = await render('school.html', '?s=' + s.slug);
    const txt = dom.window.document.body.textContent;
    for (const bad of ['undefined', 'NaN', 'null']) {
      if (txt.includes(bad)) fails.push(`school.html?s=${s.slug}: the word "${bad}" is in the rendered page`);
    }
    dom.window.close();
  }

  /* An absent Transit Score must never render as a zero or a dash — it means the city
     publishes no feed that site has ingested, and 121 rows are in that state. */
  const noFeed = everyRow.find(s => s.slug && SETTING[s.name] && SETTING[s.name].tscore == null
    && SETTING[s.name].busN > 0);
  if (!noFeed) {
    fails.push('no row with a bus line and no Transit Score to render — that combination is the ' +
      'one the section exists to state honestly');
  } else {
    const dom = await render('school.html', '?s=' + noFeed.slug);
    if (!dom.window.document.body.textContent.includes('no feed published')) {
      fails.push(`school.html?s=${noFeed.slug}: missing Transit Score does not read ` +
        `"no feed published"`);
    }
    dom.window.close();
  }

  /* The master table's two opt-in columns. Header and cell count must move together: the
     comment on SIZE_COLS in app.js records a bug where they did not. */
  {
    const dom = await render('index.html', '');
    const doc = dom.window.document;
    const heads = [...doc.querySelectorAll('#master thead th')].map(th => th.textContent.replace('▲', '').trim());
    ok('index Walk column present', heads.includes('Walk'), true);
    ok('index Locale column present', heads.includes('Locale'), true);
    const firstRow = doc.querySelector('#master tbody tr');
    ok('index master cells match its header',
      firstRow ? firstRow.children.length : 0, heads.length);
    dom.window.close();
  }

  for (const c of checks) {
    console.log(`${c.pass ? 'ok  ' : 'FAIL'}  ${c.name}: ${c.got}${c.pass ? '' : ' (want ' + c.want + ')'}`);
  }
  if (fails.length) {
    console.error(`\n${fails.length} failure(s):`);
    fails.forEach(f => console.error('  ' + f));
    server.close();
    process.exit(1);
  }
  console.log(`\nall clear — ${checks.length} counts, ${sample.length} school pages rendered, ` +
    `${Object.keys(T1500).length} 1500 fields`);
  server.close();
})().catch(e => { console.error(e); server.close(); process.exit(1); });
