/* Shared chrome, the master table, and the gap chart. */

/* ---------- theme toggle (must beat both OS setting and prior stamp) ---------- */
(function () {
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
})();

function initChrome(current) {
  const nav = `
    <header class="site"><div class="wrap">
      <a class="brand" href="index.html">Recruiting Board <span class="pill">XC / TF + CS</span></a>
      <nav class="site">
        <a href="index.html"${current === 'index' ? ' aria-current="page"' : ''}>Overview</a>
        <a href="greenville.html"${current === 'greenville' ? ' aria-current="page"' : ''}>Greenville</a>
        <a href="new-york.html"${current === 'nyc' ? ' aria-current="page"' : ''}>New York</a>
        <a href="chicago.html"${current === 'chicago' ? ' aria-current="page"' : ''}>Chicago</a>
        <a href="methodology.html"${current === 'method' ? ' aria-current="page"' : ''}>Methodology</a>
      </nav>
      <button id="theme" type="button" aria-label="Toggle color theme">Theme</button>
    </div></header>`;
  document.body.insertAdjacentHTML('afterbegin', nav);

  const foot = `
    <footer class="site"><div class="wrap">
      <p>Times from TFRRS, 2026 outdoor season &mdash; single fastest athlete per event.
      SAT and acceptance figures are approximate and unverified; check each school's Common Data Set.
      <a href="methodology.html">Read the caveats</a> before acting on anything here.</p>
    </div></footer>`;
  document.body.insertAdjacentHTML('beforeend', foot);

  document.getElementById('theme').addEventListener('click', () => {
    const isDark = getComputedStyle(document.documentElement)
      .getPropertyValue('--page').trim() === '#0d0d0d';
    const next = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    if (window.renderChart) window.renderChart();
  });
}

/* ---------- helpers ---------- */
const fmtTime = (s) => s == null ? null :
  `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;

const gapOf = (s) => s.b5000 == null ? null : ATHLETE.proj5000 - s.b5000;

function badge(tier) {
  const t = TIERS[tier];
  return `<span class="badge ${tier}" title="${t.desc}"><span class="g" aria-hidden="true">${t.glyph}</span>${t.label}</span>`;
}

function tierLegend() {
  return `<div class="legend">${Object.entries(TIERS).map(([k, t]) =>
    `<span class="legend-item">${badge(k)} <span>${t.desc}</span></span>`).join('')}</div>`;
}

/* ---------- master table ---------- */
const COLS = [
  { key: 'name',   label: 'School',   sort: (a, b) => a.name.localeCompare(b.name) },
  { key: 'metro',  label: 'Metro',    sort: (a, b) => a.metro.localeCompare(b.metro) },
  { key: 'mi',     label: 'Mi',       num: true, sort: (a, b) => a.mi - b.mi },
  { key: 'div',    label: 'Div',      sort: (a, b) => a.div.localeCompare(b.div) },
  { key: 'conf',   label: 'Conference', sort: (a, b) => a.conf.localeCompare(b.conf) },
  { key: 'cs',     label: 'CS',       sort: (a, b) => a.cs.localeCompare(b.cs) },
  { key: 'sat',    label: 'SAT',      sort: (a, b) => a.sat.localeCompare(b.sat) },
  { key: 'accept', label: 'Admit',    num: true, sort: (a, b) => parseInt(a.accept.replace(/\D/g, '')) - parseInt(b.accept.replace(/\D/g, '')) },
  { key: 'b5000',  label: 'Team best 5K', num: true, sort: (a, b) => (a.b5000 ?? 1e9) - (b.b5000 ?? 1e9) },
  { key: 'gap',    label: 'Gap to #1', num: true, sort: (a, b) => (gapOf(a) ?? -1e9) - (gapOf(b) ?? -1e9) },
  { key: 'tier',   label: 'Fit',      sort: (a, b) => ['target', 'verify', 'caution'].indexOf(a.tier) - ['target', 'verify', 'caution'].indexOf(b.tier) },
];

let sortKey = 'gap', sortDir = -1, filters = { metro: 'all', div: 'all', tier: 'all', q: '' };

function visible() {
  return SCHOOLS.filter(s =>
    (filters.metro === 'all' || s.metro === filters.metro) &&
    (filters.div === 'all' || s.div === filters.div) &&
    (filters.tier === 'all' || s.tier === filters.tier) &&
    (filters.q === '' || (s.name + ' ' + s.city + ' ' + s.conf).toLowerCase().includes(filters.q))
  ).sort((a, b) => {
    const c = COLS.find(c => c.key === sortKey);
    return (c ? c.sort(a, b) : 0) * sortDir;
  });
}

function renderTable() {
  const rows = visible();
  const tb = document.querySelector('#master tbody');
  tb.innerHTML = rows.map(s => {
    const g = gapOf(s);
    const gTxt = g == null ? '<span class="nodata">&mdash;</span>'
      : g >= 0 ? `<span class="gap-pos">+${g}s</span>`
               : `<span class="gap-neg">&minus;${Math.abs(g)}s</span>`;
    return `<tr>
      <td><span class="school">${s.name}</span><span class="city">${s.city}</span></td>
      <td>${METROS[s.metro].label}</td>
      <td class="num">${s.mi}</td>
      <td>${s.div}</td>
      <td>${s.conf}</td>
      <td class="${s.cs === 'verified' ? 'cs-ok' : 'cs-no'}">${s.cs === 'verified' ? 'Verified' : 'Confirm'}</td>
      <td class="time">${s.sat}</td>
      <td class="num">${s.accept}</td>
      <td class="num time">${fmtTime(s.b5000) ?? '<span class="nodata">&mdash;</span>'}</td>
      <td class="num">${gTxt}</td>
      <td>${badge(s.tier)}</td>
      <td class="rownote">${s.note ?? ''}</td>
    </tr>`;
  }).join('');

  const pool = filters.metro === 'all'
    ? SCHOOLS.length
    : SCHOOLS.filter(s => s.metro === filters.metro).length;
  document.querySelector('#count').textContent = `${rows.length} of ${pool} schools`;

  document.querySelectorAll('#master thead th[data-key]').forEach(th => {
    const arrow = th.querySelector('.arrow');
    if (th.dataset.key === sortKey) {
      th.setAttribute('aria-sort', sortDir === 1 ? 'ascending' : 'descending');
      arrow.textContent = sortDir === 1 ? '▲' : '▼';
    } else {
      th.removeAttribute('aria-sort');
      arrow.textContent = '▲';
    }
  });
  if (window.renderChart) window.renderChart();
}

function initTable() {
  const head = COLS.map(c =>
    `<th data-key="${c.key}" class="sortable${c.num ? ' num' : ''}" scope="col">${c.label}<span class="arrow">▲</span></th>`
  ).join('') + '<th scope="col">Notes</th>';
  document.querySelector('#master thead').innerHTML = `<tr>${head}</tr>`;

  document.querySelectorAll('#master thead th[data-key]').forEach(th => {
    th.addEventListener('click', () => {
      const k = th.dataset.key;
      if (sortKey === k) sortDir *= -1; else { sortKey = k; sortDir = 1; }
      renderTable();
    });
  });

  ['metro', 'div', 'tier'].forEach(f => {
    const el = document.getElementById('f-' + f);
    if (el) el.addEventListener('change', e => { filters[f] = e.target.value; renderTable(); });
  });
  const q = document.getElementById('f-q');
  if (q) q.addEventListener('input', e => { filters.q = e.target.value.toLowerCase().trim(); renderTable(); });

  renderTable();
}

/* ---------- gap chart: diverging bars centered on his projected 5000 ----------
   Positive (blue, right)  = their #1 is this much faster than him  -> healthy
   Negative (red, left)    = he is this much faster than their #1   -> thin squad */
function initChart() {
  const svg = document.getElementById('gapchart');
  if (!svg) return;
  const tip = document.getElementById('tip');

  window.renderChart = function () {
    const rows = visible().filter(s => s.b5000 != null)
      .sort((a, b) => gapOf(b) - gapOf(a));

    const ROW = 22, BAR = 13, PADL = 168, PADR = 56, PADT = 30, PADB = 34;
    const W = Math.max(560, svg.clientWidth || 900);
    const H = PADT + rows.length * ROW + PADB;
    const plotW = W - PADL - PADR;

    const maxAbs = Math.max(90, ...rows.map(s => Math.abs(gapOf(s)))) * 1.08;
    const x = (v) => PADL + plotW / 2 + (v / maxAbs) * (plotW / 2);

    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('height', H);

    const ticks = [-120, -90, -60, -30, 0, 30, 60, 90, 120].filter(t => Math.abs(t) <= maxAbs);
    let out = '';

    ticks.forEach(t => {
      out += `<line class="${t === 0 ? 'zeroline' : 'gridline'}" x1="${x(t)}" y1="${PADT - 8}" x2="${x(t)}" y2="${H - PADB + 4}"/>`;
      out += `<text class="tick" x="${x(t)}" y="${H - PADB + 18}" text-anchor="middle">${t === 0 ? '0' : (t > 0 ? '+' + t : t) + 's'}</text>`;
    });
    out += `<text class="axis-note" x="${x(0)}" y="${PADT - 14}" text-anchor="middle">his projected 5000 &mdash; ${ATHLETE.proj5000Label}</text>`;

    rows.forEach((s, i) => {
      const g = gapOf(s), y = PADT + i * ROW, yb = y + (ROW - BAR) / 2;
      const x0 = x(0), x1 = x(g);
      const w = Math.abs(x1 - x0), r = Math.min(4, w);
      // rounded data-end, square end anchored to the zero baseline
      const p = g >= 0
        ? `M${x0} ${yb} H${x0 + w - r} a${r} ${r} 0 0 1 ${r} ${r} V${yb + BAR - r} a${r} ${r} 0 0 1 ${-r} ${r} H${x0} Z`
        : `M${x0} ${yb} H${x0 - w + r} a${r} ${r} 0 0 0 ${-r} ${r} V${yb + BAR - r} a${r} ${r} 0 0 0 ${r} ${r} H${x0} Z`;

      out += `<g class="bar-row" data-i="${i}">
        <text class="ylab" x="${PADL - 10}" y="${y + ROW / 2 + 4}" text-anchor="end">${s.name}</text>
        <path class="${g >= 0 ? 'bar-pos' : 'bar-neg'}" d="${p}"/>
        <text class="tick" x="${g >= 0 ? x1 + 6 : x1 - 6}" y="${y + ROW / 2 + 4}" text-anchor="${g >= 0 ? 'start' : 'end'}">${g >= 0 ? '+' + g : g}s</text>
        <rect class="bar-hit" x="${PADL}" y="${y}" width="${plotW}" height="${ROW}"/>
      </g>`;
    });

    svg.innerHTML = out;

    svg.querySelectorAll('.bar-row').forEach(gEl => {
      const s = rows[+gEl.dataset.i];
      gEl.addEventListener('mousemove', ev => {
        const g = gapOf(s);
        tip.innerHTML = `<div class="t-name">${s.name}</div>
          <div class="t-row">${s.div} &middot; ${s.conf} &middot; ${s.mi} mi</div>
          <div class="t-row">Their best 5K: ${fmtTime(s.b5000)}</div>
          <div class="t-row">His projection: ${ATHLETE.proj5000Label}</div>
          <div class="t-row">${g >= 0 ? `Their #1 is ${g}s faster` : `He is ${Math.abs(g)}s faster than their #1`}</div>`;
        tip.style.opacity = 1;
        tip.style.left = Math.min(ev.clientX + 14, innerWidth - 275) + 'px';
        tip.style.top = (ev.clientY + 14) + 'px';
      });
      gEl.addEventListener('mouseleave', () => { tip.style.opacity = 0; });
    });

    const n = document.getElementById('chart-count');
    if (n) n.textContent = `${rows.length} schools with 5000m data`;
  };

  window.renderChart();
  let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(window.renderChart, 150); });
}
