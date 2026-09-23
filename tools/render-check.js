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
  ';__out={SCHOOLS,REMOVED,NO_TRACK,NO_PROGRAM,XCRACES};', ctx);
const { SCHOOLS, REMOVED, NO_TRACK, NO_PROGRAM, XCRACES } = ctx.__out;

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

  for (const c of checks) {
    console.log(`${c.pass ? 'ok  ' : 'FAIL'}  ${c.name}: ${c.got}${c.pass ? '' : ' (want ' + c.want + ')'}`);
  }
  if (fails.length) {
    console.error(`\n${fails.length} failure(s):`);
    fails.forEach(f => console.error('  ' + f));
    server.close();
    process.exit(1);
  }
  console.log(`\nall clear — ${checks.length} counts, ${sample.length} school pages rendered`);
  server.close();
})().catch(e => { console.error(e); server.close(); process.exit(1); });
