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
    const want = SCHOOLS.filter(s => s.metro === metro).length;
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

  ok('rows total', SCHOOLS.length, 120);
  ok('off-board rows', REMOVED.length + NO_TRACK.length + NO_PROGRAM.length, 41);

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
