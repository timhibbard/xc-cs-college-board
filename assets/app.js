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
      <p>Cross country depth from 2025 championship results on TFRRS; track marks from the 2026
      outdoor season, single fastest athlete per event. Cost, SAT, admit rate and CS-program data
      from the U.S. Department of Education College Scorecard.
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

const TIER_ORDER = ['target', 'deep', 'verify', 'caution'];
const link = (s) => `school.html?s=${encodeURIComponent(s.slug)}`;

/* Where he lands relative to the team's 7th man. Negative is inside the seven. */
function v7Txt(s) {
  if (!s.xc || s.xc.v7 == null) return '<span class="nodata">&mdash;</span>';
  return s.xc.v7 <= 0
    ? `<span class="gap-pos">&minus;${Math.abs(s.xc.v7).toFixed(0)}s</span>`
    : `<span class="gap-neg">+${s.xc.v7.toFixed(0)}s</span>`;
}

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
  { key: 'net',    label: 'Net cost',    num: true, sort: (a, b) => (a.cost?.net ?? 1e9) - (b.cost?.net ?? 1e9) },
  { key: 'b5000',  label: 'Team best 5K', num: true, sort: (a, b) => (a.b5000 ?? 1e9) - (b.b5000 ?? 1e9) },
  { key: 'slot',   label: 'His slot in their 7', num: true, sort: (a, b) => (a.xc?.slot ?? 1e9) - (b.xc?.slot ?? 1e9) },
  { key: 'v7',     label: 'vs their 7th', num: true, sort: (a, b) => (a.xc?.v7 ?? 1e9) - (b.xc?.v7 ?? 1e9) },
  { key: 'tier',   label: 'Fit',      sort: (a, b) => TIER_ORDER.indexOf(a.tier) - TIER_ORDER.indexOf(b.tier) },
];

let sortKey = 'tier', sortDir = 1, filters = { metro: 'all', div: 'all', tier: 'all', q: '' };

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
  tb.innerHTML = rows.map(s => `<tr>
      <td><a class="school" href="${link(s)}">${s.name}</a><span class="city">${s.city}</span></td>
      <td>${METROS[s.metro].label}</td>
      <td class="num">${s.mi}</td>
      <td>${s.div}</td>
      <td>${s.conf}</td>
      <td class="${s.cs === 'verified' ? 'cs-ok' : 'cs-no'}">${s.cs === 'verified' ? 'Verified' : s.cs === 'none' ? 'None' : 'Confirm'}</td>
      <td class="time">${s.sat}</td>
      <td class="num">${s.accept}</td>
      <td class="num money">${s.cost?.net == null ? '<span class="nodata">&mdash;</span>' : '$' + s.cost.net.toLocaleString('en-US')}</td>
      <td class="num time">${fmtTime(s.b5000) ?? '<span class="nodata">&mdash;</span>'}</td>
      <td class="num">${s.xc ? '#' + s.xc.slot : '<span class="nodata">&mdash;</span>'}</td>
      <td class="num">${v7Txt(s)}</td>
      <td>${badge(s.tier)}</td>
      <td class="rownote">${s.note ?? ''}</td>
    </tr>`).join('');

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
  if (window.renderMap) window.renderMap();
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

/* ---------- metro map ----------------------------------------------------------
   Leaflet + CARTO basemap. Pins carry the tier glyph and a text label in the
   popup, so tier is never communicated by color alone. Coordinates are
   approximate main-campus points; the circle is the search radius drawn as a
   straight-line distance, while the table's "Mi" column is driving distance,
   so a school near the line can sit a mile or two outside the circle. */

const TILES = {
  light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
  dark:  'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
};

const isDarkNow = () => getComputedStyle(document.documentElement)
  .getPropertyValue('--page').trim() === '#0d0d0d';

/* Nudge apart pins that share a campus town so both stay clickable. Greedy
   proximity clustering rather than grid bucketing — a grid misses the pairs that
   straddle a cell boundary, which is most of them. */
function declutter(pts, thresh = 0.02) {
  const clusters = [];
  pts.forEach(p => {
    const near = clusters.find(c =>
      Math.abs(c[0].lat - p.lat) < thresh && Math.abs(c[0].lon - p.lon) < thresh);
    if (near) near.push(p); else clusters.push([p]);
  });
  const out = [];
  clusters.forEach(c => {
    if (c.length === 1) { out.push({ ...c[0], nudged: false }); return; }
    const rad = thresh * 0.75;
    c.forEach((p, i) => {
      const a = (2 * Math.PI * i) / c.length;
      out.push({ ...p, lat: p.lat + rad * Math.sin(a), lon: p.lon + rad * Math.cos(a), nudged: true });
    });
  });
  return out;
}

function initMap(metro) {
  const host = document.getElementById('map');
  if (!host || typeof L === 'undefined') return;
  const M = METROS[metro];

  const map = L.map(host, { scrollWheelZoom: false, zoomControl: true })
    .setView(M.center, M.zoom);
  L.control.scale({ imperial: true, metric: false }).addTo(map);

  let tiles = L.tileLayer(TILES[isDarkNow() ? 'dark' : 'light'], {
    subdomains: 'abcd', maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
  }).addTo(map);

  const circle = L.circle(M.center, {
    radius: M.radiusMi * 1609.34,
    className: 'radius-ring', interactive: false,
  }).addTo(map);

  L.marker(M.center, {
    icon: L.divIcon({ className: 'pin-wrap', html: '<span class="pin pin-center" aria-hidden="true">◎</span>', iconSize: [22, 22], iconAnchor: [11, 11] }),
    keyboard: false,
  }).addTo(map).bindPopup(`<b>${M.label}</b><br>Center of the ${M.radius} search radius`);

  map.fitBounds(circle.getBounds(), { padding: [12, 12] });

  const layer = L.layerGroup().addTo(map);
  const showCut = document.getElementById('map-showcut');

  window.renderMap = function () {
    layer.clearLayers();

    const kept = visible().filter(s => s.metro === metro)
      .map(s => ({ ...s, kind: s.tier }));

    let extra = [];
    if (showCut && showCut.checked) {
      extra = [
        ...REMOVED.filter(r => r.metro === metro).map(r => ({ ...r, kind: 'cut' })),
        ...NO_PROGRAM.filter(r => r.metro === metro).map(r => ({ ...r, kind: 'none' })),
      ];
    }

    const GLYPH = { cut: '✕', none: '⊘' };
    const KIND = { cut: 'Cut &mdash; he would be a walk-on', none: 'No men&rsquo;s program' };

    declutter([...kept, ...extra]).forEach(s => {
      const glyph = GLYPH[s.kind] ?? TIERS[s.kind].glyph;
      const g = s.b5000 != null ? gapOf(s) : null;

      const body = s.kind === 'cut' || s.kind === 'none'
        ? `<div class="mp-meta">${s.div ?? ''}</div><div class="mp-why">${s.why}</div>`
        : `<div class="mp-meta">${s.city} &middot; ${s.div} ${s.conf} &middot; ${s.mi} mi</div>
           ${s.xc
             ? `<div class="mp-line">In their scoring seven he is <b>#${s.xc.slot}</b>, ${s.xc.v7 <= 0 ? Math.abs(s.xc.v7).toFixed(0) + 's inside' : s.xc.v7.toFixed(0) + 's outside'} their 7th man</div>`
             : `<div class="mp-line">No cross country data &mdash; team best 5K <b>${fmtTime(s.b5000) ?? 'unknown'}</b>${g == null ? '' : `, gap ${g >= 0 ? '+' + g : g}s`}</div>`}
           <div class="mp-line">Net cost: <b>${s.cost?.net == null ? 'unknown' : '$' + s.cost.net.toLocaleString('en-US')}</b> &middot; SAT ${s.sat}</div>
           <div class="mp-line">CS degree: <b>${s.cs === 'verified' ? 'verified' : s.cs === 'none' ? 'not offered' : 'unconfirmed'}</b></div>
           ${s.note ? `<div class="mp-why">${s.note}</div>` : ''}`;

      L.marker([s.lat, s.lon], {
        icon: L.divIcon({
          className: 'pin-wrap',
          html: `<span class="pin pin-${s.kind}" aria-hidden="true">${glyph}</span>`,
          iconSize: [22, 22], iconAnchor: [11, 11],
        }),
        title: s.name,
        alt: `${s.name} — ${s.kind === 'cut' || s.kind === 'none' ? 'excluded' : TIERS[s.kind].label}`,
      }).addTo(layer).bindPopup(
        `<div class="mp"><div class="mp-name">${s.name}</div>
         <div class="mp-tier pin-${s.kind}-txt">${glyph} ${KIND[s.kind] ?? TIERS[s.kind].label}</div>
         ${body}${s.nudged ? '<div class="mp-nudge">Pin nudged slightly &mdash; another school shares this town.</div>' : ''}
         ${s.kind === 'none' ? '' : `<div class="mp-line"><a href="${link(s)}">Full detail &rarr;</a></div>`}</div>`,
        { maxWidth: 300 }
      );
    });

    const n = document.getElementById('map-count');
    if (n) n.textContent = `${kept.length} school${kept.length === 1 ? '' : 's'} shown${extra.length ? ` + ${extra.length} excluded` : ''}`;
  };

  if (showCut) showCut.addEventListener('change', window.renderMap);

  document.getElementById('theme').addEventListener('click', () => {
    map.removeLayer(tiles);
    tiles = L.tileLayer(TILES[isDarkNow() ? 'dark' : 'light'], {
      subdomains: 'abcd', maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    }).addTo(map);
    tiles.bringToBack();
  });

  window.renderMap();
}

function mapLegend() {
  const item = (cls, glyph, label) =>
    `<span class="legend-item"><span class="pin pin-${cls}" aria-hidden="true">${glyph}</span> <span>${label}</span></span>`;
  return `<div class="legend">
    ${Object.entries(TIERS).map(([k, t]) => item(k, t.glyph, t.label)).join('')}
    ${item('cut', '✕', 'Cut on roster times')}
    ${item('none', '⊘', 'No men’s program')}
    ${item('center', '◎', 'Search center')}
  </div>`;
}
