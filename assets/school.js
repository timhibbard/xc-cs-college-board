/* One school, in detail. Reads ?s=<slug> and renders from data.js + detail.js.

   There is one template rather than 78 hand-written pages, so every school gets
   the same sections in the same order and a missing section is visibly missing
   rather than quietly absent. */

const QS = new URLSearchParams(location.search).get('s');
const S = SCHOOLS.find(s => s.slug === QS) || REMOVED.find(s => s.slug === QS);
const IS_CUT = !!(S && !SCHOOLS.includes(S));

const usd = (n) => n == null ? null : '$' + n.toLocaleString('en-US');
const SEASONS = {
  x: { key: 'x', label: 'Cross country', glyph: 'X', long: 'cross country' },
  o: { key: 'o', label: 'Outdoor track', glyph: 'O', long: 'outdoor track' },
  i: { key: 'i', label: 'Indoor track', glyph: 'I', long: 'indoor track' },
};

/* ---------- shell ---------- */
function notFound() {
  document.getElementById('body').innerHTML = `
    <h1>School not found</h1>
    <p class="prose">No school on the board has the id <code>${QS ? QS.replace(/[<>&]/g, '') : '(none)'}</code>.
    Start from the <a href="index.html">overview</a> or a metro page.</p>`;
}

function head() {
  const m = METROS[S.metro];
  document.title = `${S.name} — recruiting detail`;
  const tierLine = IS_CUT
    ? `<span class="badge cut"><span class="g" aria-hidden="true">✕</span>Cut</span>`
    : badge(S.tier);

  return `
    <p class="eyebrow"><a href="${m.page}">${m.label}</a> · ${m.radius} radius</p>
    <h1>${S.name}</h1>
    <p class="lede">${S.city ?? ''}${S.div ? ' · ' + S.div : ''}${S.conf ? ' ' + S.conf : ''}${S.mi != null ? ' · ' + S.mi + ' mi from ' + m.label.replace(' SC', '') : ''}</p>
    <p class="badge-row">${tierLine}${S.xc ? `<span class="src-tag">tier from cross country results</span>`
      : IS_CUT ? '' : `<span class="src-tag">tier from one outdoor 5000 mark &mdash; no cross country data</span>`}</p>
    ${S.note ? `<p class="prose note-lede">${S.note}</p>` : ''}
    ${IS_CUT ? `<div class="callout crit"><span class="c-title">Cut from the board</span><p>${S.why}</p></div>` : ''}`;
}

/* ---------- cost ---------- */
function cost() {
  const c = S.cost;
  if (!c) return `<h2>Cost</h2><p class="prose nodata">No federal cost record matched this school.</p>`;
  const inState = c.own === 'public' && S.metro === 'greenville' && /SC$/.test(S.city ?? '');
  const rows = [
    ['Tuition and fees', usd(c.tuition), c.own === 'public' ? 'out-of-state rate — he is a South Carolina resident' : 'private, one rate for everyone'],
    ['Room and board, on campus', usd(c.rb), ''],
    ['Sticker price for one year', usd(c.sticker), 'tuition + room and board, before any aid'],
    ['Average net price actually paid', usd(c.net), 'after grants and scholarships, averaged across all students — the number to plan against'],
    ['Undergraduate enrollment', c.size == null ? null : c.size.toLocaleString('en-US'), ''],
  ];
  return `
    <h2>Cost</h2>
    <div class="kpi-row">
      <div class="kpi"><div class="k-label">Sticker price</div><div class="k-value">${usd(c.sticker) ?? '—'}</div><div class="k-sub">tuition + room and board</div></div>
      <div class="kpi"><div class="k-label">Average net price</div><div class="k-value">${usd(c.net) ?? '—'}</div><div class="k-sub">what students actually pay</div></div>
      <div class="kpi"><div class="k-label">Admit rate</div><div class="k-value">${S.accept ?? '—'}</div><div class="k-sub">${S.acceptSrc === 'fed' ? 'federal data' : 'estimate'}</div></div>
      <div class="kpi"><div class="k-label">SAT, middle 50%</div><div class="k-value" style="font-size:22px">${S.sat ?? '—'}</div><div class="k-sub">${S.satSrc === 'fed' ? 'federal data' : 'estimate'}</div></div>
    </div>
    <div class="table-scroll">
      <table><tbody>
        ${rows.map(([k, v, n]) => `<tr><th scope="row">${k}</th>
          <td class="num money">${v ?? '<span class="nodata">not reported</span>'}</td>
          <td class="rownote">${n}</td></tr>`).join('')}
      </tbody></table>
    </div>
    <p class="map-note">
      U.S. Department of Education College Scorecard, most recent year available${c.ipeds ? `, IPEDS unit ${c.ipeds}` : ''}.
      ${c.own === 'public' ? 'This is a public institution, so the figure above is the <strong>out-of-state</strong> rate.' : ''}
      ${inState ? ' In-state rates would apply here.' : ''}
      Net price is an average across all incoming students, not a prediction for one applicant — a strong
      student stacking merit aid usually lands below it.
    </p>`;
}

/* ---------- academics ---------- */
function academics() {
  const csTxt = S.cs === 'verified'
    ? 'Confirmed — the school reports bachelor\'s degrees in computer and information sciences to the federal government'
    : S.cs === 'none'
      ? 'Not offered'
      : 'Not confirmed';
  return `
    <h2>Computer science</h2>
    <div class="table-scroll">
      <table><tbody>
        <tr><th scope="row">CS degree</th><td class="${S.cs === 'verified' ? 'cs-ok' : 'cs-no'}">${csTxt}</td></tr>
        <tr><th scope="row">Share of all bachelor's degrees in CS</th>
          <td class="num">${S.csShare == null ? '<span class="nodata">not reported</span>' : S.csShare + '%'}</td></tr>
        <tr><th scope="row">Source</th><td class="rownote">${S.csSrc === 'fed'
          ? 'Federal program data (CIP family 11). A CS degree housed under mathematics reads as zero here, which is why a low share is not proof of absence.'
          : 'Checked by hand against the school\'s own site or Wikipedia.'}</td></tr>
      </tbody></table>
    </div>`;
}

/* ---------- cross country ---------- */
function xcSection() {
  const races = (typeof XCRACES !== 'undefined' && XCRACES[S.name]) || [];
  if (!races.length) {
    return `
      <h2>Cross country</h2>
      <div class="callout"><span class="c-title">No cross country results on file</span>
      <p>${S.b5000
        ? `This school's tier rests on a single outdoor 5000m mark (${fmtTime(S.b5000)}), which is a
           floor rather than a measure of depth.`
        : `No cross country result and no outdoor 5000m mark has been collected for this program yet, so
           it carries no real tier — <b>Verify</b> here means unmeasured, not borderline.`}
      It is the highest-value thing left to look up here:
      the 2025 conference championship result would show their whole scoring seven.</p></div>`;
  }
  const P = { '8K': ATHLETE.proj8k, '10K': ATHLETE.proj10k };
  const PL = { '8K': ATHLETE.proj8kLabel, '10K': ATHLETE.proj10kLabel };

  return `
    <h2>Cross country — where he would have finished</h2>
    <p class="prose">
      Every 2025 championship result on file for this team, with their scoring seven in finishing
      order and his projection dropped into place. This is the comparison that decides the tier; the
      outdoor 5000 mark below is only a floor. The individual athletes are not named — their times
      are what the comparison needs, their identities are not, and each meet is named so any of it
      can be checked against TFRRS.
    </p>
    ${races.map(r => {
      const corr = r.corr || 0;
      /* Athletes are not named — their times are what the comparison needs, and this
         is a public page. The meet and date are given so any of it can be checked. */
      const runners = r.runners.map((t, i) => ({ n: `Their #${i + 1}`, t, adj: t + corr }));
      const me = { t: P[r.dist], adj: P[r.dist], me: true };
      const all = [...runners, me].sort((a, b) => a.adj - b.adj);
      return `
      <div class="race">
        <div class="race-head">
          <div>
            <div class="race-meet">${r.meet}</div>
            <div class="race-meta">${r.date} · ${r.dist}${r.level === 'conference' ? ' · conference championship' : r.level === 'regional' ? ' · NCAA regional' : ''}${r.place != null ? ` · finished ${r.place}${r.score != null ? ` with ${r.score} points` : ''}` : ''}</div>
          </div>
          <div class="race-slot"><span class="rs-n">${r.slot}</span><span class="rs-l">he would be<br>their #${r.slot}</span></div>
        </div>
        <div class="table-scroll">
          <table class="race-table">
            <thead><tr><th scope="col">Place</th><th scope="col">Runner</th><th scope="col" class="num">Time</th>${corr ? '<th scope="col" class="num">Course-adjusted</th>' : ''}</tr></thead>
            <tbody>${all.map((x, i) => `<tr class="${x.me ? 'me' : ''}">
              <td class="num">${i + 1}</td>
              <td>${x.me ? `<strong>His projection &mdash; ${PL[r.dist]}</strong>` : x.n}</td>
              <td class="num time">${fmtTime(x.t)}</td>
              ${corr ? `<td class="num time">${x.me ? '<span class="nodata">—</span>' : fmtTime(x.adj)}</td>` : ''}
            </tr>`).join('')}</tbody>
          </table>
        </div>
        <p class="map-note">
          ${r.v7 != null ? `His projection is <strong>${r.v7 <= 0 ? Math.abs(r.v7).toFixed(0) + 's inside' : r.v7.toFixed(0) + 's outside'}</strong> their 7th man, and ${Math.abs(r.g1).toFixed(0)}s ${r.g1 >= 0 ? 'behind' : 'ahead of'} their #1. ` : ''}
          Their 1-through-${r.runners.length} spread is <strong>${r.spread.toFixed(0)}s</strong> — the most course-independent
          number here, because it compares the team only to itself.
          ${corr ? `<br><strong>Course correction of ${corr > 0 ? '+' : ''}${corr}s applied.</strong> ${COURSE_NOTES[r.meet] ? 'This meet ' + COURSE_NOTES[r.meet] + '.' : ''}` : ''}
        </p>
      </div>`;
    }).join('')}
    <div class="table-scroll" style="margin-top:18px">
      <table><tbody>
        <tr><th scope="row">Averaged over ${races.length} race${races.length === 1 ? '' : 's'}: his slot in their seven</th><td class="num"><strong>${S.xc.slot}</strong></td></tr>
        <tr><th scope="row">Versus their 7th man</th><td class="num">${S.xc.v7 == null ? '<span class="nodata">—</span>' : (S.xc.v7 <= 0 ? '−' + Math.abs(S.xc.v7) + 's (inside)' : '+' + S.xc.v7 + 's (outside)')}</td></tr>
        <tr><th scope="row">Versus their #1</th><td class="num">${S.xc.g1 >= 0 ? '+' + S.xc.g1 + 's behind' : '−' + Math.abs(S.xc.g1) + 's ahead'}</td></tr>
        <tr><th scope="row">Tightest 1&ndash;7 spread on file</th><td class="num">${S.xc.spread}s</td></tr>
      </tbody></table>
    </div>
    ${S.xc.disagree ? `<div class="callout"><span class="c-title">Their races disagree</span><p>His slot moves by three or more places
      between these results. Treat the tier as provisional and weight the race on the course most like the one he would run.</p></div>` : ''}`;
}

/* ---------- track marks ---------- */
function trackMarks() {
  if (S.b5000 == null && !S.b1500) return '';
  const g = S.b5000 == null ? null : ATHLETE.proj5000 - S.b5000;
  return `
    <h2>Track marks</h2>
    <div class="table-scroll">
      <table><tbody>
        <tr><th scope="row">Their fastest outdoor 5000, 2026</th><td class="num time">${fmtTime(S.b5000) ?? '<span class="nodata">no data</span>'}</td></tr>
        <tr><th scope="row">Their fastest outdoor 1500, 2026</th><td class="num time">${S.b1500 ?? '<span class="nodata">no data</span>'}</td></tr>
        <tr><th scope="row">His projected 5000</th><td class="num time">${ATHLETE.proj5000Label}</td></tr>
        <tr><th scope="row">Gap to their #1</th><td class="num">${g == null ? '<span class="nodata">—</span>'
          : g >= 0 ? `<span class="gap-pos">+${g}s</span>` : `<span class="gap-neg">−${Math.abs(g)}s</span>`}</td></tr>
      </tbody></table>
    </div>
    <p class="map-note">One athlete, one event, one season — a fast number here is strong evidence, a slow one is weak evidence.
    <a href="methodology.html">Why that is</a>.</p>`;
}

/* ---------- meets: map + schedule ---------- */
function meetSection() {
  const sched = (typeof SCHED !== 'undefined' && SCHED[S.name]) || [];
  if (!sched.length) {
    return `
      <h2>Where they compete</h2>
      <div class="callout"><span class="c-title">Meet schedule not collected for this school</span>
      <p>Full season schedules were pulled for the twelve schools that came out of the cross country
      analysis as target tier. If this school moves up, its schedule is the next thing to add.</p></div>`;
  }
  const placed = sched.filter(m => VENUES[m.m]);
  const unplacedNames = [...new Set(sched.filter(m => !VENUES[m.m]).map(m => m.m))];
  const bySeason = { x: 0, i: 0, o: 0 };
  sched.forEach(m => bySeason[m.s]++);

  return `
    <h2>Where they compete</h2>
    <p class="prose">
      Every meet this team travelled to across the ${bySeason.x} cross country,
      ${bySeason.i} indoor and ${bySeason.o} outdoor entries on their results page, colored by season.
      Each pin carries a letter as well as a color, so the seasons stay separable without relying on hue.
    </p>
    <div class="map-card">
      <div class="map-bar">
        ${Object.values(SEASONS).map(s => `<label><input type="checkbox" class="f-season" value="${s.key}" checked> ${s.label}</label>`).join('')}
        <span class="count" id="meet-count"></span>
      </div>
      <div id="meetmap"></div>
      <div class="legend" id="meet-legend">
        ${Object.values(SEASONS).map(s => `<span class="legend-item"><span class="pin pin-s-${s.key}" aria-hidden="true">${s.glyph}</span><span>${s.label}</span></span>`).join('')}
        <span class="legend-item"><span class="pin pin-home" aria-hidden="true">⌂</span><span>Campus</span></span>
      </div>
      <p class="map-note">
        <strong>${placed.length} of ${sched.length} appearances are placed</strong>
        (${unplacedNames.length} distinct meet${unplacedNames.length === 1 ? '' : 's'} could not be located and are listed below the table).
        Almost all of the gap is conference and NCAA championships, whose host rotates each year, so a
        single coordinate would be wrong more often than right. Pins marked <em>host campus</em> place the
        school that hosts the meet, not necessarily the course itself.
      </p>
    </div>
    <h3>Full schedule</h3>
    <div class="table-scroll">
      <table id="sched">
        <caption>The table is the accessible view of the map above — same data, no color needed.</caption>
        <thead><tr><th scope="col">Season</th><th scope="col">Date</th><th scope="col">Meet</th><th scope="col">Where</th></tr></thead>
        <tbody>${sched.map(m => {
          const v = VENUES[m.m];
          return `<tr>
            <td><span class="s-tag s-${m.s}">${SEASONS[m.s].glyph}</span> ${SEASONS[m.s].label}</td>
            <td class="time">${m.d}</td>
            <td>${m.m}</td>
            <td class="rownote">${v ? `${v.v}${v.src === 'h' ? ' <span class="src-tag">host campus</span>' : ''}`
              : '<span class="nodata">not located</span>'}</td></tr>`;
        }).join('')}</tbody>
      </table>
    </div>
    ${unplacedNames.length ? `<p class="map-note"><strong>Not located:</strong> ${unplacedNames.join(' · ')}.</p>` : ''}`;
}

function initMeetMap() {
  const host = document.getElementById('meetmap');
  if (!host || typeof L === 'undefined') return;
  const sched = SCHED[S.name] || [];

  const map = L.map(host, { scrollWheelZoom: false }).setView([S.lat, S.lon], 6);
  L.control.scale({ imperial: true, metric: false }).addTo(map);
  let tiles = L.tileLayer(TILES[isDarkNow() ? 'dark' : 'light'], {
    subdomains: 'abcd', maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
  }).addTo(map);

  L.marker([S.lat, S.lon], {
    icon: L.divIcon({ className: 'pin-wrap', html: '<span class="pin pin-home" aria-hidden="true">⌂</span>', iconSize: [22, 22], iconAnchor: [11, 11] }),
  }).addTo(map).bindPopup(`<div class="mp"><div class="mp-name">${S.name}</div><div class="mp-meta">${S.city} — campus</div></div>`);

  const layer = L.layerGroup().addTo(map);

  const render = () => {
    layer.clearLayers();
    const on = new Set([...document.querySelectorAll('.f-season:checked')].map(el => el.value));

    // one marker per venue+season: a venue used for both indoor and outdoor is two
    // real facts about the schedule, not one, so both get a pin and declutter nudges them apart
    const bucket = new Map();
    sched.filter(m => on.has(m.s) && VENUES[m.m]).forEach(m => {
      const v = VENUES[m.m], k = `${v.v}|${m.s}`;
      if (!bucket.has(k)) bucket.set(k, { lat: v.lat, lon: v.lon, v: v.v, src: v.src, s: m.s, meets: [] });
      bucket.get(k).meets.push(m);
    });
    const pts = declutter([...bucket.values()], 0.05);

    pts.forEach(p => {
      const S_ = SEASONS[p.s];
      L.marker([p.lat, p.lon], {
        icon: L.divIcon({ className: 'pin-wrap', html: `<span class="pin pin-s-${p.s}" aria-hidden="true">${S_.glyph}</span>`, iconSize: [22, 22], iconAnchor: [11, 11] }),
        title: `${p.v} — ${S_.label}`,
        alt: `${p.v}, ${S_.long}, ${p.meets.length} meet${p.meets.length === 1 ? '' : 's'}`,
      }).addTo(layer).bindPopup(
        `<div class="mp"><div class="mp-name">${p.v}</div>
         <div class="mp-tier pin-s-${p.s}-txt">${S_.glyph} ${S_.label}</div>
         ${p.meets.map(m => `<div class="mp-line">${m.d} &middot; ${m.m}</div>`).join('')}
         ${p.src === 'h' ? '<div class="mp-nudge">Located from the host named in the meet title — the campus, not necessarily the course.</div>' : ''}
         ${p.nudged ? '<div class="mp-nudge">Pin nudged slightly — another season used this venue.</div>' : ''}</div>`,
        { maxWidth: 300 });
    });

    if (pts.length) map.fitBounds(L.latLngBounds([...pts.map(p => [p.lat, p.lon]), [S.lat, S.lon]]), { padding: [26, 26] });
    const n = document.getElementById('meet-count');
    const shown = sched.filter(m => on.has(m.s) && VENUES[m.m]).length;
    if (n) n.textContent = `${shown} appearance${shown === 1 ? '' : 's'} at ${pts.length} venue${pts.length === 1 ? '' : 's'}`;
  };

  document.querySelectorAll('.f-season').forEach(el => el.addEventListener('change', render));
  document.getElementById('theme').addEventListener('click', () => {
    map.removeLayer(tiles);
    tiles = L.tileLayer(TILES[isDarkNow() ? 'dark' : 'light'], {
      subdomains: 'abcd', maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    }).addTo(map);
    tiles.bringToBack();
  });

  render();
}

/* ---------- what's known and what isn't ---------- */
function completeness() {
  const has = (x) => x ? '<span class="cs-ok">have it</span>' : '<span class="cs-no">missing</span>';
  const rows = [
    ['Cross country top seven', !!S.xc, S.xc ? `${S.xc.nraces} championship result${S.xc.nraces === 1 ? '' : 's'}` : 'the highest-value gap here'],
    ['Cost and net price', !!(S.cost && S.cost.tuition), 'College Scorecard'],
    ['SAT range', S.satSrc === 'fed', S.satSrc === 'fed' ? 'federal' : 'not reported federally — the figure shown is an estimate'],
    ['Admit rate', S.acceptSrc === 'fed', S.acceptSrc === 'fed' ? 'federal' : 'estimate'],
    ['CS program', S.cs === 'verified', S.csSrc === 'fed' ? 'federal program data' : 'checked by hand'],
    ['Meet schedule', !!(typeof SCHED !== 'undefined' && SCHED[S.name]), 'pulled for target-tier schools only'],
  ];
  return `
    <h2>What is verified here, and what is not</h2>
    <div class="table-scroll">
      <table><tbody>${rows.map(([k, ok, n]) =>
        `<tr><th scope="row">${k}</th><td>${has(ok)}</td><td class="rownote">${n}</td></tr>`).join('')}</tbody></table>
    </div>
    <p class="map-note">Nothing on this page is inferred from a school's reputation. Where a number is
      missing it is shown as missing. <a href="methodology.html">Read the methodology</a>.</p>`;
}

/* ---------- go ---------- */
initChrome(S ? S.metro : 'index');
if (!S) {
  notFound();
} else {
  document.getElementById('body').innerHTML =
    head() + cost() + academics() + xcSection() + trackMarks() + meetSection() + completeness() + `
    <hr>
    <p class="prose"><a href="${METROS[S.metro].page}">&larr; Back to ${METROS[S.metro].label}</a>
      &nbsp;·&nbsp; <a href="index.html">All ${SCHOOLS.length} schools</a></p>`;
  initMeetMap();
}
