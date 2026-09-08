/* One school, in detail. Reads ?s=<slug> and renders from data.js + detail.js.

   There is one template rather than 78 hand-written pages, so every school gets
   the same sections in the same order and a missing section is visibly missing
   rather than quietly absent. */

const QS = new URLSearchParams(location.search).get('s');
const S = SCHOOLS.find(s => s.slug === QS) || REMOVED.find(s => s.slug === QS)
  || NO_TRACK.find(s => s.slug === QS) || NO_PROGRAM.find(s => s.slug === QS);
/* Three different kinds of "off the board", and they read differently on the page:
   REMOVED is a judgement about level, and NO_TRACK and NO_PROGRAM are facts about which
   sports exist. NO_PROGRAM rows mostly carry no slug and so never reach this page; the one
   that does is South Carolina, which earns a page precisely because it looks available. */
const IS_NOTRACK = !!(S && NO_TRACK.includes(S));
const IS_NOXC = !!(S && NO_PROGRAM.includes(S));
const IS_CUT = !!(S && !SCHOOLS.includes(S) && !IS_NOTRACK && !IS_NOXC);

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
    : IS_NOTRACK
      ? `<span class="badge notrack"><span class="g" aria-hidden="true">⊗</span>No men&rsquo;s track</span>`
      : IS_NOXC
        ? `<span class="badge notrack"><span class="g" aria-hidden="true">⊘</span>No men&rsquo;s cross country</span>`
        : badge(S.tier);

  return `
    <p class="eyebrow"><a href="${m.page}">${m.label}</a> · ${m.radius} radius</p>
    <h1>${S.name}</h1>
    <p class="lede">${S.city ?? ''}${S.div ? ' · ' + S.div : ''}${S.conf ? ' ' + S.conf : ''}${S.mi != null ? ' · ' + S.mi + ' mi from ' + m.label.replace(' SC', '') : ''}</p>
    <p class="badge-row">${tierLine}${IS_NOTRACK ? `<span class="src-tag">cross country only &mdash; the tier below is the cross country measurement, not a recommendation</span>`
      : S.xc ? `<span class="src-tag">tier from cross country results</span>`
      : IS_CUT || IS_NOXC ? '' : `<span class="src-tag">tier from one outdoor 5000 mark &mdash; no cross country data</span>`}</p>
    ${S.note ? `<p class="prose note-lede">${S.note}</p>` : ''}
    ${IS_CUT ? `<div class="callout crit"><span class="c-title">Cut from the board</span><p>${S.why}</p></div>` : ''}
    ${IS_NOXC ? `<div class="callout crit"><span class="c-title">Off the board &mdash; there is no men&rsquo;s cross country team</span>
      <p>${S.why}</p>
      <p>Nothing below is a measurement of him against this school, because there is nobody to
      measure him against: every number on this board comes from slotting him into a men&rsquo;s
      cross country scoring seven, and this school does not field one. The cost, admissions and
      coach details are kept because they are true and because they are what makes the absence
      worth recording.</p></div>` : ''}
    ${IS_NOTRACK ? `<div class="callout crit"><span class="c-title">Off the board &mdash; cross country without track</span>
      <p>${S.why}</p>
      <p>He wants to run cross country <em>and</em> track. A program that sponsors one without the other
      cannot give him both, so this school comes off the board no matter how the cross country
      numbers read. Everything below is still here, and still true.</p></div>` : ''}`;
}

/* ---------- cost ---------- */

/* Two kinds of town figure that mean something other than what they look like.
   Both are documented in TOWNPOP's header comment in data.js. */
const CONSOLIDATED = ['Augusta GA', 'Macon GA', 'Athens GA'];
const CDP = ['Buies Creek NC', 'Cullowhee NC', 'Tigerville SC', 'Emory VA'];

function townNote(pop) {
  let out = 'U.S. Census, ACS 2024 5-year estimate for the place itself';
  if (CONSOLIDATED.includes(S.city))
    out += ' — a consolidated city-county government, so this is county-wide and reads larger than the campus surroundings';
  else if (CDP.includes(S.city))
    out += ' — a census-designated place rather than an incorporated town, so the boundary is a statistical convenience';
  /* The comparison that actually decides what the place feels like on a Tuesday night. */
  if (S.cost?.size != null && S.cost.size > pop)
    out += '. There are more undergraduates here than residents — the school <em>is</em> the town';
  return out;
}

function cost() {
  const c = S.cost;
  if (!c) return `<h2>Cost</h2><p class="prose nodata">No federal cost record matched this school.</p>`;
  /* He is a South Carolina resident, so `resid` is a fact about the school, not a choice:
     in-state at an SC public, out-of-state at every other public, irrelevant at a private. */
  const inState = c.own === 'public' && c.resid === 'in';
  const prem = netPremium(S);
  const tuiNote = c.own !== 'public'
    ? 'private, one rate for everyone'
    : inState
      ? `<strong>in-state rate</strong> — he is a South Carolina resident and this is a South Carolina public${c.tuiOut ? `. Out-of-state students pay ${usd(c.tuiOut)}` : ''}`
      : `<strong>out-of-state rate</strong> — he is a South Carolina resident and this school is not in South Carolina${c.tuiIn ? `. Its own residents pay ${usd(c.tuiIn)}` : ''}`;
  const rows = [
    ['Tuition and fees', usd(c.tuition), tuiNote],
    ['Room and board, on campus', usd(c.rb), ''],
    ['Sticker price for one year', usd(c.sticker), 'tuition + room and board, before any aid'],
    ['Average net price actually paid', usd(c.net),
      'after grants and scholarships, averaged across all students' + (c.own === 'public'
        ? ' — and averaged across <strong>in-state</strong> students only, which is how the federal file computes it at every public'
        : ' — the number to plan against')],
    ...(prem > 0 ? [['Net price on his residency', usd(c.net + prem),
      `<strong>estimate</strong> — the federal net price above plus the ${usd(prem)} non-resident tuition premium, holding average grant aid constant. A non-resident waiver or athletic money can erase it`]] : []),
    ['Undergraduate enrollment', c.size == null ? null : c.size.toLocaleString('en-US'),
      'federal headcount — the number that decides whether he is one of a hundred distance runners or one of six', 'num'],
  ];
  /* Town population is collected for the Greenville ring only; the other two metros
     do not need a number to answer the question. */
  const pop = typeof TOWNPOP === 'undefined' ? null : TOWNPOP[S.city];
  if (pop != null) rows.push(['Town population', pop.toLocaleString('en-US'), townNote(pop), 'num']);
  return `
    <h2>Cost</h2>
    <div class="kpi-row">
      <div class="kpi"><div class="k-label">Sticker price</div><div class="k-value">${usd(c.sticker) ?? '—'}</div><div class="k-sub">tuition + room and board</div></div>
      <div class="kpi"><div class="k-label">Net price</div><div class="k-value">${prem > 0 ? '≈' + usd(c.net + prem) : usd(c.net) ?? '—'}</div><div class="k-sub">${prem > 0 ? 'estimated, on his residency' : 'what students actually pay'}</div></div>
      <div class="kpi"><div class="k-label">Admit rate</div><div class="k-value">${S.accept ?? '—'}</div><div class="k-sub">${S.acceptSrc === 'fed' ? 'federal data' : 'estimate'}</div></div>
      <div class="kpi"><div class="k-label">SAT, middle 50%</div><div class="k-value" style="font-size:22px">${S.sat ?? '—'}</div><div class="k-sub">${S.satSrc === 'fed' ? 'federal data' : 'estimate'}</div></div>
    </div>
    <div class="table-scroll">
      <table><tbody>
        ${rows.map(([k, v, n, cls]) => `<tr><th scope="row">${k}</th>
          <td class="${cls ?? 'num money'}">${v ?? '<span class="nodata">not reported</span>'}</td>
          <td class="rownote">${n}</td></tr>`).join('')}
      </tbody></table>
    </div>
    <p class="map-note">
      U.S. Department of Education College Scorecard, most recent year available${c.ipeds ? `, IPEDS unit ${c.ipeds}` : ''}.
      ${c.own !== 'public' ? 'A private college charges one tuition rate regardless of where a student lives, so residency does not enter this table.'
        : inState ? 'A South Carolina public, so the in-state rate applies to him and the federal net price is already on the right basis.'
        : `An out-of-state public. The tuition line is the rate he would pay, but the federal net price is computed from
           in-state students only${prem > 0 ? `, so the two are on different bases — hence the ${usd(prem)} adjustment above` : ''}.
           <a href="methodology.html#residency">How residency enters the net cost</a>.`}
      Net price is an average across all incoming students, not a prediction for one applicant — a strong
      student stacking merit aid usually lands below it.
      ${pop == null ? '' : `Town population is the place the campus sits in, not the metro around it — a small
      number inside Atlanta or Charlotte describes the address, not the setting${S.mi != null
        ? `, so read it against the ${S.mi} miles above` : ''}.`}
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

/* ---------- coach ---------- */

/* Coaches are public professionals listed on their own employer's staff directory,
   so they are named here — unlike the athletes in XCRACES, who are not. Everything
   in this block was read off the page linked as the source in August 2026; staffs
   turn over, so the link matters more than the name. */
function coachSection() {
  const c = S.coach;
  if (!c) return `
    <h2>Who to email</h2>
    <p class="prose nodata">No coach has been recorded for this program yet.</p>`;

  const vacant = c.name ? /vacant|\bTBA\b/i.test(c.name) : false;
  const rows = [
    ['Coach', c.name ? `<strong>${c.name}</strong>` : null,
      vacant ? 'the directory names no coach for this program, which is itself worth knowing — write to the department address below and ask who is running it' : ''],
    ['Title', c.title, 'as the school lists it — a "Director of Cross Country/Track &amp; Field" runs both seasons; a distance-specific title is the person who would actually coach him'],
    ['Email', c.email ? `<a href="mailto:${c.email}">${c.email}</a>` : null,
      c.email ? (vacant
        ? 'a department address rather than a coach&rsquo;s — he can still write today; NCAA contact rules limit when <em>coaches</em> may initiate, not when a recruit may'
        : 'he can email this address today — NCAA contact rules limit when <em>coaches</em> may initiate, not when a recruit may')
        : `no address is published on the staff directory — use ${c.phone ? 'the phone number below or ' : ''}the team's online recruit form`],
    ['Phone', c.phone ? `<a href="tel:${c.phone.replace(/[^0-9]/g, '')}">${c.phone}</a>` : null, c.phone ? 'office line' : ''],
    ['Instagram', S.ig ? `<a href="https://instagram.com/${S.ig}" rel="noopener">@${S.ig}</a>` : null,
      S.ig
        ? (S.igDept
          ? 'a <b>department-wide</b> account — this school links no cross country or track account of its own, so there is no public window on the distance squad. Worth asking the coach whether one exists'
          : 'the team&rsquo;s own account, linked from the page above. Read it before writing: who they signed last year, what their workouts look like, and whether the distance men get posted at all')
        : 'no Instagram is linked from the school&rsquo;s own athletics pages'],
    ['Coach&rsquo;s Instagram',
      c.ig ? `<a href="https://instagram.com/${c.ig}" rel="noopener">@${c.ig}</a>` : null,
      c.ig
        ? `the coach&rsquo;s <b>own</b> account, not the program&rsquo;s &mdash; recorded only because the account
           itself says who they are${c.igSrc ? ` (${c.igSrc})` : ''}. Read it, do not message it: a recruiting question
           belongs in the email above, where it is on the record and the coach can answer it as a coach`
        : 'either this coach keeps no public account, or nothing found identifies one as theirs. A matching name alone was not accepted, so an empty cell here means <b>unverified</b>, not absent'],
  ];
  /* A staff change found while checking Instagram, and the more valuable of the two
     findings: the coach who recruited the class in the results below has gone, and the
     email that was here would have reached nobody. Shown rather than silently corrected,
     because a name a recruit half-remembers from last season should not just vanish. */
  if (c.prev) rows.push(['Recently changed', `${c.prev} &rarr; <strong>${c.name}</strong>`,
    `the staff page named ${c.prev} when this board was built and names ${c.name} now, so the
     season measured below was coached by someone else. Read the results as the program&rsquo;s,
     not the new coach&rsquo;s &mdash; and expect a new coach to be recruiting harder than a settled one`]);
  return `
    <h2>Who to email</h2>
    <div class="table-scroll">
      <table><tbody>
        ${rows.map(([k, v, n]) => `<tr><th scope="row">${k}</th>
          <td>${v ?? '<span class="nodata">not published</span>'}</td>
          <td class="rownote">${n}</td></tr>`).join('')}
      </tbody></table>
    </div>
    <p class="map-note">
      Read from <a href="${c.src}" rel="noopener">the school's own staff directory</a> in August 2026 and
      <b>re-checked against it in September 2026</b>, when five names across the board turned out to have
      changed. Coaching staffs turn over between seasons, so check the link before writing &mdash; and if
      the title above names a different sport or an interim, that is what the directory said.
    </p>`;
}

/* ---------- cross country ---------- */
function xcSection() {
  const races = (typeof XCRACES !== 'undefined' && XCRACES[S.name]) || [];
  /* No results and no team are different findings, and only one of them is worth
     chasing. Do not invite the reader to go look up a championship result for a
     program that does not exist. */
  if (IS_NOXC) return `
      <h2>Cross country</h2>
      <div class="callout crit"><span class="c-title">There is no men&rsquo;s cross country team here</span>
      <p>Not a missing result &mdash; a missing team. There is no scoring seven to slot him into, now or
      in any past season, so the single number this whole board turns on cannot be computed for this
      school and never will be. The outdoor marks below are real, and they are men&rsquo;s track marks:
      distance runners do enrol here, they just race on the track only.</p></div>`;
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
            <div class="race-meta">${r.date} · ${r.dist}${/conference/i.test(r.level || '') ? ' · conference championship' : /regional/i.test(r.level || '') ? ' · NCAA regional' : ''}${r.place != null ? ` · finished ${r.place}${r.score != null ? ` with ${r.score} points` : ''}` : ''}${r.nfin != null ? ` · only ${r.nfin} finisher${r.nfin === 1 ? '' : 's'}` : ''}</div>
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
          ${r.v7 != null
            ? `His projection is <strong>${r.v7 <= 0 ? Math.abs(r.v7).toFixed(0) + 's inside' : r.v7.toFixed(0) + 's outside'}</strong> their 7th man, and ${Math.abs(r.g1).toFixed(0)}s ${r.g1 >= 0 ? 'behind' : 'ahead of'} their #1. `
            : (r.nfin ?? r.runners.length) <= 2
            ? `<strong>Only ${r.nfin === 1 ? 'one runner' : r.nfin + ' runners'} from this team ran here &mdash; ${r.nfin === 1 ? 'an individual qualifier' : 'individual qualifiers'} rather than a team
               entry</strong>, so there is nothing to slot into. It is shown because it is part of the record:
               ${r.nfin === 1 ? 'their fastest man was' : 'their fastest men were'} ${Math.abs(r.g1).toFixed(0)}s ${r.g1 >= 0 ? 'ahead of' : 'behind'} his projection at this distance.`
            : `<strong>They finished ${r.nfin ?? r.runners.length}, not seven, so there is no 7th man to compare to.</strong>
               ${r.vlast != null ? `Against their last finisher he is
               <strong>${r.vlast <= 0 ? Math.abs(r.vlast).toFixed(0) + 's faster' : r.vlast.toFixed(0) + 's slower'}</strong>, and ` : ''}${Math.abs(r.g1).toFixed(0)}s
               ${r.g1 >= 0 ? 'behind' : 'ahead of'} their #1.
               ${(r.nfin ?? r.runners.length) < 5 ? `Five finishers are the minimum for a team score, so this one is not a team
               result at all and does not enter the averages below &mdash; it is here because it is the only evidence there is.` : ''} `}
          ${r.runners.length < 3 ? '' : `Their 1-through-${r.runners.length} spread is <strong>${r.spread.toFixed(0)}s</strong> — the most course-independent
          number here, because it compares the team only to itself.`}
          ${corr ? `<br><strong>Course correction of ${corr > 0 ? '+' : ''}${corr}s applied.</strong> ${COURSE_NOTES[r.meet] ? 'This meet ' + COURSE_NOTES[r.meet] + '.' : ''}` : ''}
        </p>
      </div>`;
    }).join('')}
    ${aggTable(races)}
    ${S.xc.disagree ? `<div class="callout"><span class="c-title">Their races disagree</span><p>His slot moves by three or more places
      between these results. Treat the tier as provisional and weight the race on the course most like the one he would run.</p></div>` : ''}
    ${shortNote(races)}`;
}

/* A team that never finished seven has no 7th man to compare against, so the
   headline number of this whole board does not exist for them. Say that rather
   than printing a dash and leaving it to be read as missing data. */
function aggTable(races) {
  const x = S.xc;
  const counted = races.filter(r => (r.nfin ?? r.runners.length) >= 5).length;
  const gap = (v) => v <= 0 ? '−' + Math.abs(v) + 's (inside)' : '+' + v + 's (outside)';
  const rows = [
    [counted === 0
      ? 'His slot among the runners they did finish'
      : `Averaged over ${counted} race${counted === 1 ? '' : 's'}: his slot in their ${x.v7 == null ? 'finishers' : 'seven'}`,
      `<strong>${x.slot ?? '—'}</strong>`],
    ['Versus their 7th man', x.v7 == null
      ? `<span class="nodata">no 7th man &mdash; they never finished seven</span>`
      : gap(x.v7)],
    ['Versus their #1', x.g1 == null ? '<span class="nodata">—</span>'
      : (x.g1 >= 0 ? '+' + x.g1 + 's behind' : '−' + Math.abs(x.g1) + 's ahead')],
    [x.short ? `Tightest front-to-back spread on file` : `Tightest 1&ndash;7 spread on file`,
      x.spread == null ? '<span class="nodata">—</span>' : x.spread + 's'],
  ];
  if (x.maxfin != null) rows.push(['Most runners they finished in any of these races',
    `${x.maxfin}${x.maxfin < 5 ? ' — below the five needed for a team score' : ''}`]);
  return `
    <div class="table-scroll" style="margin-top:18px">
      <table><tbody>${rows.map(([k, v]) =>
        `<tr><th scope="row">${k}</th><td class="num">${v}</td></tr>`).join('')}</tbody></table>
    </div>`;
}

function shortNote(races) {
  const x = S.xc;
  if (!x.short) return '';
  const counted = races.filter(r => (r.nfin ?? r.runners.length) >= 5).length;
  if (counted === 0) return `
    <div class="callout crit"><span class="c-title">This program never finished five runners in 2025</span>
      <p>Five finishers are the minimum for a team score, and the most this team got to the line in any
      championship race was <strong>${x.maxfin}</strong>. There is no scoring seven to slot into because
      there is no scoring five. That is not a gap in the data &mdash; it is the finding, and it is the
      reason this school sits at <b>caution</b> no matter how the times compare. Ask the coach directly
      how many men are on the roster for the coming season before anything else.</p></div>`;
  if (x.v7 == null) return `
    <div class="callout"><span class="c-title">They never finished seven runners</span>
      <p>Every result on file for this team ends before a 7th man, so the column this board is built on
      &mdash; how far he would be from their 7th &mdash; cannot be computed. The comparison shown instead
      is against their <em>last</em> finisher, which is a weaker test: he could be comfortably inside a
      five-man squad and still have nobody to train with. A team that cannot field seven at its own
      conference championship is a thin program, which is the same warning the number would have given.</p></div>`;
  return `
    <div class="callout"><span class="c-title">One of these races was short of seven</span>
      <p>The team finished fewer than seven in at least one result above, so that race contributes a
      last-finisher comparison rather than a 7th-man one. The averages use the ${counted} race${counted === 1 ? '' : 's'}
      with at least five finishers.</p></div>`;
}

/* ---------- track marks ---------- */
/* "3:51.1" -> 231.1. Marks are stored as written on the results page, tenths and all,
   because rounding a 1500 to whole seconds throws away a tenth of the useful precision. */
const parseMark = (t) => {
  const m = /^(\d+):(\d+(?:\.\d+)?)$/.exec(String(t ?? '').trim());
  return m ? +m[1] * 60 + +m[2] : null;
};

/* Positive = their runner is faster = he has room to grow into the squad, which is the
   healthy direction. Same sign convention as the cross country columns. */
function gapCell(g, dp = 0) {
  if (g == null) return '<span class="nodata">&mdash;</span>';
  const v = Math.abs(g).toFixed(dp);
  return g >= 0 ? `<span class="gap-pos">+${v}s</span>` : `<span class="gap-neg">&minus;${v}s</span>`;
}

/* "3:58.39" out of 238.39. Marks are kept to the hundredth because that is how a
   1500 is timed, and because fmtTime() rounds to whole seconds — which turns 3:59.9
   into 3:60 and a 0.4s gap into a tie. */
const fmt15 = (s) => {
  if (s == null) return null;
  const m = Math.floor(s / 60), r = s - m * 60;
  return `${m}:${r < 10 ? '0' : ''}${r.toFixed(2)}`;
};

function trackMarks() {
  if (IS_NOTRACK) return `
    <h2>Track marks</h2>
    <div class="callout crit"><span class="c-title">There are none, and that is the finding</span>
      <p>This school fields no men&rsquo;s track and field team, so there is no outdoor 1500 or 5000 to
      compare against and no conference 1500 field to place him in. TFRRS holds no top mark for the
      program in any event. The cross country section above is the whole of the running record here.</p></div>`;
  if (S.b5000 == null && !S.b1500) return '';
  const g5 = S.b5000 == null ? null : ATHLETE.proj5000 - S.b5000;
  const their15 = parseMark(S.b1500);
  const g15 = their15 == null ? null : ATHLETE.proj1500 - their15;
  return `
    <h2>Track marks</h2>
    <div class="table-scroll">
      <table><tbody>
        <tr><th scope="row">Their fastest outdoor 5000, 2026</th><td class="num time">${fmtTime(S.b5000) ?? '<span class="nodata">no data</span>'}</td></tr>
        <tr><th scope="row">His projected 5000</th><td class="num time">${ATHLETE.proj5000Label}</td></tr>
        <tr><th scope="row">Gap to their #1 at 5000</th><td class="num">${gapCell(g5)}</td></tr>
        <tr><th scope="row">Their fastest outdoor 1500, 2026</th><td class="num time">${S.b1500 ?? '<span class="nodata">no data</span>'}</td></tr>
        <tr><th scope="row">His projected 1500</th><td class="num time">${ATHLETE.proj1500Label}</td></tr>
        <tr><th scope="row">Gap to their #1 at 1500</th><td class="num">${gapCell(g15, 1)}</td></tr>
      </tbody></table>
    </div>
    <p class="map-note">One athlete, one event, one season — a fast number here is strong evidence, a slow one is weak evidence.
    His projected 1500 of ${ATHLETE.proj1500Label} converts a projected ${ATHLETE.proj1600Label} 1600, one more track season on
    from the 4:21 he has run. Read the 1500 gap on its own scale: the healthy band at 5000 is 40&ndash;60 seconds behind a
    team's best, and the same percentage over 1500 is only <strong>10 to 15 seconds</strong>.
    <a href="methodology.html">Why that is</a>.</p>`;
}

/* ---------- the 1500 in May ---------- */

/* A team best is one man on one day. A championship field is the thing he would
   actually line up in, so T1500 (detail.js) holds the whole field and this section
   drops his projection into it. Athletes are not named, for the same reason they are
   not named in XCRACES; every card links its TFRRS results page. */

const ORD = (n) => {
  const t = n % 100;
  if (t >= 11 && t <= 13) return n + 'th';
  return n + ({ 1: 'st', 2: 'nd', 3: 'rd' }[n % 10] || 'th');
};

/* One card per meet: their entrants with his projection slotted in, then what the
   field around them looked like. Identical shape for the conference meet and for
   the postseason, because the question is identical. */
function meetCard(m, kind) {
  const P = ATHLETE.proj1500, PL = ATHLETE.proj1500Label;
  const isConf = kind === 'conf';
  const rows = [...m.theirs.map((t, i) => ({ n: `Their #${i + 1} at this meet`, t })),
    { t: P, me: true }].sort((a, b) => a.t - b.t);
  const g1 = m.theirs.length ? P - m.theirs[0] : null;
  /* Field sizes are quoted with him in them: N men ran it, so with his projection
     dropped in the field is N + 1 and "21st of 20" never appears. */
  const field = m.n + 1;
  const madeFinal = isConf && m.flast != null ? m.flast - P : null;
  /* A conference final won slower than its own prelims is a tactical race, not a
     level. Say so, or "1st in the final" reads as a result it is not. */
  const tactical = isConf && m.fwin > m.win + 0.01;

  return `
    <div class="race">
      <div class="race-head">
        <div>
          <div class="race-meet"><a href="${m.url}" rel="noopener">${m.meet}</a></div>
          <div class="race-meta">${m.date}${isConf ? ` · ${m.conf} championship` : ' · postseason'} · ${m.n} men ran the 1500</div>
        </div>
        <div class="race-slot"><span class="rs-n">${m.place}</span><span class="rs-l">he would be<br>${ORD(m.place)} of ${field}</span></div>
      </div>
      ${m.theirs.length ? `
      <div class="table-scroll">
        <table class="race-table">
          <thead><tr><th scope="col">Order</th><th scope="col">Runner</th><th scope="col" class="num">Time</th></tr></thead>
          <tbody>${rows.map((x, i) => `<tr class="${x.me ? 'me' : ''}">
            <td class="num">${i + 1}</td>
            <td>${x.me ? `<strong>His projection &mdash; ${PL}</strong>` : x.n}</td>
            <td class="num time">${fmt15(x.t)}</td>
          </tr>`).join('')}</tbody>
        </table>
      </div>
      <p class="map-note">
        ${m.theirs.length === 1
          ? 'This team put one man in the 1500 here, and he would be'
          : `Among the ${m.theirs.length} men this team put in the 1500 here he would be`}
        <strong>their #${m.slot ?? rows.findIndex(x => x.me) + 1}</strong>, ${Math.abs(g1).toFixed(1)}s
        ${g1 >= 0 ? 'behind' : 'ahead of'} their fastest.
        ${isConf ? (m.nfinal === 0
          ? (m.theirs.length === 1 ? 'He did not make the final.' : 'None of them made the final.')
          : `${m.nfinal === m.theirs.length ? (m.theirs.length === 1 ? 'He' : 'All of them') : m.nfinal + ' of them'} made the final.`) : ''}
      </p>`
      : `<div class="callout"><span class="c-title">They entered nobody in the 1500</span>
        <p>No runner from this team appears in the 1500 at ${isConf ? 'its own conference championship' : 'this meet'}.
        The field is still the field he would be running into${isConf ? ', and a program that skips the championship round of an event is telling you where its distance men actually race — ask the coach whether the 1500 is part of the plan' : ''}.</p></div>`}
      <p class="map-note">
        Fastest 1500 at the meet: <strong>${fmt15(m.win)}</strong>.
        ${isConf ? `The final took ${m.fn} runners and was won in ${fmt15(m.fwin)}; the slowest man in it ran
          <strong>${fmt15(m.flast)}</strong>, so on this year's marks his ${PL} projection would have
          <strong>${madeFinal >= 0
            ? `made that final with ${madeFinal.toFixed(1)}s to spare</strong> and finished ${ORD(m.fplace)} of ${m.fn + 1} in it`
            : `missed that final by ${Math.abs(madeFinal).toFixed(1)}s</strong>`}.
          ${tactical ? `That final was <em>tactical</em> — won in ${fmt15(m.fwin)}, slower than the ${fmt15(m.win)}
            run in the rounds that fed it — so a placing inside it describes the race, not the level.` : ''}` : ''}
        The ${ORD(m.place)}-of-${field} figure above compares every man who ran the event at this meet on
        time, prelims included; it is the number to trust for exactly that reason.
        <a href="${m.url}" rel="noopener">Full results</a>.
      </p>
    </div>`;
}

function fifteen() {
  const T = (typeof T1500 !== 'undefined' && T1500[S.slug]) || null;
  if (!T) return '';
  const P = ATHLETE.proj1500, PL = ATHLETE.proj1500Label;
  const depth = [...T.d15.map((t, i) => ({ n: `Their #${i + 1}`, t })), { t: P, me: true }]
    .sort((a, b) => a.t - b.t);
  /* D1 has a real qualifying round between the conference meet and nationals; the other
     divisions go straight to a national championship, so "regional" means different things. */
  const regionalNote = S.div === 'D1'
    ? 'In Division 1 the round above the conference meet is the NCAA First Round &mdash; East or West &mdash; which is the qualifier for nationals.'
    : S.div === 'NAIA'
      ? 'The NAIA has no regional round in track: the conference meet feeds the national championship directly.'
      : `Division ${S.div.slice(1)} outdoor track has no regional round &mdash; the conference meet feeds the national championship on descending-order marks, so a fast time anywhere counts.`;

  return `
    <h2>The 1500 in May &mdash; where he would have finished</h2>
    <p class="prose">
      The mark above is one man on one day. This is the field: every 1500 this program's runners
      contested at their 2026 conference championship, with his projected ${PL} dropped in on time.
      ${regionalNote}
      Athletes are not named &mdash; their times are what the comparison needs &mdash; and every card links
      the TFRRS results page it was read from.
    </p>

    <h3>Their 2026 outdoor 1500, man by man</h3>
    ${T.nath === 0 ? `
      <div class="callout"><span class="c-title">Nobody on this team ran a 1500 in 2026</span>
        <p>They field a men's track team, but no one contested the 1500 outdoors this season, so there is
        no depth chart to slot into. It usually means their distance men race the 800 or the 5000 instead.
        Worth one line in the email: <em>is the 1500 part of the plan?</em></p></div>`
      : `
      <div class="table-scroll">
        <table class="race-table">
          <thead><tr><th scope="col">Order</th><th scope="col">Runner</th><th scope="col" class="num">Season best</th></tr></thead>
          <tbody>${depth.map((x, i) => `<tr class="${x.me ? 'me' : ''}">
            <td class="num">${i + 1}</td>
            <td>${x.me ? `<strong>His projection &mdash; ${PL}</strong>` : x.n}</td>
            <td class="num time">${fmt15(x.t)}</td>
          </tr>`).join('')}</tbody>
        </table>
      </div>
      <p class="map-note">
        <strong>${T.nath === 1 ? 'One man' : T.nath + ' different men'}</strong> ran the 1500 for them outdoors in 2026${T.nath > T.d15.length
          ? `; the ${T.d15.length} fastest are shown` : ''}. ${T.nath === 1 ? 'His best mark of the year.' : 'One mark each, their best.'}
        His projection would be <strong>their #${T.dslot}</strong>${T.nath > T.d15.length && T.dslot > T.d15.length
          ? ' — outside the group shown above' : ''}, ${P - T.d15[0] >= 0
            ? `${(P - T.d15[0]).toFixed(1)}s behind their fastest`
            : `${Math.abs(P - T.d15[0]).toFixed(1)}s ahead of their fastest`}.
        The healthy band here is 10 to 15 seconds behind a team's best, not the 40 to 60 the 5000 asks for
        &mdash; and being ahead of their #1 is a warning, not a win: it means the program has nobody to
        train with him.
      </p>`}

    <h3>Conference championship</h3>
    ${meetCard(T.cm, 'conf')}
    ${T.post ? `
      <h3>Postseason</h3>
      <p class="prose">Rounds above the conference meet where this team had a 1500 runner. Getting here is
      the thing to ask a coach about: it is the difference between a program that races the event and a
      program that fills a lane in it.</p>
      ${T.post.map(p => meetCard(p, 'post')).join('')}`
      : `<p class="map-note">No runner from this team reached a postseason 1500 &mdash; no NCAA round, no
        IC4A-ECAC. That is the common case, not a mark against them.</p>`}`;
}

/* How precisely a venue is placed. A facility coordinate needs no caveat; a ZIP or a
   town centroid does, so it is labelled in the table and in the popup. */
const SRCTAG = {
  z: ' <span class="src-tag">ZIP area</span>',
  c: ' <span class="src-tag">town</span>',
};
const SRCNOTE = {
  z: 'Placed from the ZIP the results page printed, not the facility — the pin is the middle of that postal area.',
  c: 'Placed from the town the results page named, not the facility — the pin is the middle of that town.',
};

/* ---------- meets: map + schedule ---------- */
function meetSection() {
  const ids = (typeof SCHED !== 'undefined' && SCHED[S.name]) || [];
  const sched = ids.map(k => MEETS[k]).filter(Boolean);
  if (!sched.length) {
    return `
      <h2>Where they compete</h2>
      <div class="callout"><span class="c-title">No 2025&ndash;26 schedule exists to show</span>
      <p>Every other school on this board has its schedule read straight off its own TFRRS results
      page. This one has no result on that page inside the 2025&ndash;26 window at all, so there is
      nothing to map. That is itself the finding, and it is consistent with the program note above.</p></div>`;
  }
  const placed = sched.filter(m => m.v != null);
  const unplacedNames = [...new Set(sched.filter(m => m.v == null).map(m => m.m))];
  const prec = { r: 0, z: 0, c: 0 };
  new Set(placed.map(m => m.v)).forEach(i => prec[VENUES[i].src]++);
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
        <strong>${placed.length} of ${sched.length} appearances are placed</strong>${unplacedNames.length
          ? ` (${unplacedNames.length} meet${unplacedNames.length === 1 ? '' : 's'} printed no venue at all and ${unplacedNames.length === 1 ? 'is' : 'are'} listed below the table)`
          : ''}.
        Every venue here was read off that meet&rsquo;s own results page, so a conference or NCAA
        championship is placed where it was actually held this season rather than at whoever hosted it
        last year. The pins differ in how tightly they are placed:
        ${prec.r} of these ${prec.r + prec.z + prec.c} distinct venues resolved to the facility itself, ${prec.z} only
        to the ZIP the results page printed, and ${prec.c} only to the town it named. The looser two are
        tagged in the table below.
      </p>
    </div>
    <h3>Full schedule</h3>
    <div class="table-scroll">
      <table id="sched">
        <caption>The table is the accessible view of the map above — same data, no color needed.</caption>
        <thead><tr><th scope="col">Season</th><th scope="col">Date</th><th scope="col">Meet</th><th scope="col">Where</th></tr></thead>
        <tbody>${sched.map(m => {
          const v = m.v == null ? null : VENUES[m.v];
          return `<tr>
            <td><span class="s-tag s-${m.s}">${SEASONS[m.s].glyph}</span> ${SEASONS[m.s].label}</td>
            <td class="time">${m.d}</td>
            <td>${m.m}</td>
            <td class="rownote">${v ? `${v.v}${SRCTAG[v.src] || ''}`
              : '<span class="nodata">no venue printed</span>'}</td></tr>`;
        }).join('')}</tbody>
      </table>
    </div>
    ${unplacedNames.length ? `<p class="map-note"><strong>No venue printed:</strong> ${unplacedNames.join(' · ')}.
      TFRRS names a host for ${unplacedNames.length === 1 ? 'this meet' : 'these meets'} but no location, so there is
      nothing to geocode.</p>` : ''}`;
}

function initMeetMap() {
  const host = document.getElementById('meetmap');
  if (!host || typeof L === 'undefined') return;
  const sched = (SCHED[S.name] || []).map(k => MEETS[k]).filter(Boolean);

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
    sched.filter(m => on.has(m.s) && m.v != null).forEach(m => {
      const v = VENUES[m.v], k = `${v.v}|${m.s}`;
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
         ${SRCNOTE[p.src] ? `<div class="mp-nudge">${SRCNOTE[p.src]}</div>` : ''}
         ${p.nudged ? '<div class="mp-nudge">Pin nudged slightly — another season used this venue.</div>' : ''}</div>`,
        { maxWidth: 300 });
    });

    if (pts.length) map.fitBounds(L.latLngBounds([...pts.map(p => [p.lat, p.lon]), [S.lat, S.lon]]), { padding: [26, 26] });
    const n = document.getElementById('meet-count');
    const vis = sched.filter(m => on.has(m.s) && m.v != null);
    const shown = vis.length, nv = new Set(vis.map(m => m.v)).size;
    if (n) n.textContent = `${shown} appearance${shown === 1 ? '' : 's'} at ${nv} venue${nv === 1 ? '' : 's'}`
      + (pts.length > nv ? `, ${pts.length} pins` : '');
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
    ['Cross country top seven', !!S.xc,
      S.xc ? `${S.xc.nraces} championship result${S.xc.nraces === 1 ? '' : 's'}`
        : IS_NOXC ? 'there is no men’s cross country program to have a top seven'
          : 'the highest-value gap here'],
    ['1500 conference field', !!(typeof T1500 !== 'undefined' && T1500[S.slug]),
      IS_NOTRACK ? 'there is no men’s track program to have a 1500 field'
        : (typeof T1500 !== 'undefined' && T1500[S.slug])
          ? `their conference championship 1500, read off TFRRS${T1500[S.slug].nath ? ` — ${T1500[S.slug].nath} of their men ran the event in 2026` : ' — none of their men ran the event in 2026'}`
          : 'not collected'],
    ['Cost and net price', !!(S.cost && S.cost.tuition), 'College Scorecard'],
    ['SAT range', S.satSrc === 'fed', S.satSrc === 'fed' ? 'federal' : 'not reported federally — the figure shown is an estimate'],
    ['Admit rate', S.acceptSrc === 'fed', S.acceptSrc === 'fed' ? 'federal' : 'estimate'],
    ['CS program', S.cs === 'verified', S.csSrc === 'fed' ? 'federal program data' : 'checked by hand'],
    ['Meet schedule', !!(typeof SCHED !== 'undefined' && SCHED[S.name]),
      (typeof SCHED !== 'undefined' && SCHED[S.name])
        ? `every 2025–26 meet on their own TFRRS results page — ${SCHED[S.name].length} appearances`
        : 'their TFRRS results page holds nothing inside the 2025–26 season'],
    ['Coach name and contact', !!(S.coach && S.coach.name), S.coach && S.coach.email ? 'name, title and email off the school\'s staff directory' : 'no email published — phone or recruit form only'],
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
    head() + cost() + academics() + xcSection() + trackMarks() + fifteen() + meetSection() + coachSection() + completeness() + `
    <hr>
    <p class="prose"><a href="${METROS[S.metro].page}">&larr; Back to ${METROS[S.metro].label}</a>
      &nbsp;·&nbsp; <a href="index.html">All ${SCHOOLS.length} schools on the board</a></p>`;
  initMeetMap();
}
