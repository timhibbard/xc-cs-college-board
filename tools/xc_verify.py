"""Re-verify every race on file against the results page it came from.

  in:   tools/.work/board.json   (node tools/dump_board.js)
        tools/slugmap.json
  out:  tools/.work/verify.json  -- one record per race, with every disagreement found
        stdout                   -- the violations, grouped by kind

Why this exists, and why the check it replaces was worse than no check at all. A
-96.5s course correction was once written *into* the stored `runners` array while
`corr: -96.5` stayed on the race object, so every gap derived from it subtracted the
offset twice and five schools were promoted to Target on arithmetic alone. The audit in
place at the time recomputed the stored `slot`/`g1`/`v7`/`spread` from the stored
`runners` and passed cleanly, because a pre-corrected array is indistinguishable from a
raw one when the array is all you compare against. A self-consistent file can be wholly
wrong; only the source settles it.

The strong invariant was then restored for 228 races, and the 2026 sweep wrote another
204 straight off their fetched pages, which is the same guarantee from the other side.
The ~1,100 races swept in between have only ever had the weak check. This closes that:
every race, every number, back to the published times.

How a race finds its page. No rid is stored on a race -- XCRACES carries meet name and
date and nothing else -- so the link is rebuilt from each program's own TFRRS page, whose
LATEST RESULTS table is dated and reaches back several seasons. Resolving on (slug, date)
rather than on the meet name is deliberate: names in the file carry trailing spaces, year
prefixes and host abbreviations that no normaliser gets right, and a mis-joined race is
verified against the wrong page, which is worse than an unverified one.

What counts as anchored. A race is anchored when some men's individual section of its page
holds that team's first seven times EXACTLY as stored. Sections are not chosen by a
heuristic and then diffed -- a meet can run a varsity 8K and an open 8K, and picking the
deeper one by rule would report a false violation on whichever race was read from the
other. So every men's section is tried, and it is the file's own numbers that select the
section. If none matches, the closest is reported with its diff.

Then, from that section's times: nfin, the class years, the team place and score, the
distance, the date, the level the meet name implies, and every derived field recomputed
with the stored `corr` added back -- g1, v7, vlast, slot, spread.

usage:
  python3 tools/xc_verify.py            # cache first, fetch what is missing (~10 min paced)
  python3 tools/xc_verify.py --offline  # only what is already cached, for iterating
  python3 tools/xc_verify.py --fresh    # re-fetch every page
  python3 tools/xc_verify.py --limit N  # first N meets only
  python3 tools/xc_verify.py --emit     # also write .work/tails.json for tail_apply.py
"""
import collections
import datetime
import glob
import gzip
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '.work')
TEAMS = os.path.join(WORK, 'tfrrs-teams')
RESULTS = os.path.join(WORK, 'tfrrs-results')
OUT = os.path.join(WORK, 'verify.json')
sys.path.insert(0, HERE)
import parse_xc                                             # noqa: E402
import xc_fetch                                             # noqa: E402
import xc_season                                            # noqa: E402

AGENT = xc_season.AGENT
PAUSE = 1.5
MILE = 1609.344
# Within this much of the scored distance, a course length is the same race. Board rows are
# scored at 5K/6K/8K/10K and courses are not: 8,057m, 4.97 miles and 8,000m are all the same
# 8K, and the widest case on file is a 3-mile course scored as a 5K, 3.4% short.
DIST_TOL = 0.05


def metres(d):
    """'8000m', '4.97M', '7.85k', '5.2M' -> metres. Small numbers in miles, large in metres."""
    m = re.match(r'^(\d+(?:\.\d+)?)\s*([kKmM])', (d or '').strip())
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2).lower()
    return v * 1000 if u == 'k' else (v if v > 100 else v * MILE)


def days(iso):
    return datetime.date.fromisoformat(iso).toordinal()


def fetch(url, path, need, fresh=False, offline=False):
    """(html, 'cache'|'net') or (None, why). `need` is a string the real page must contain."""
    if not fresh and os.path.exists(path):
        with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
            return f.read(), 'cache'
    if offline:
        return None, 'not cached'
    r = subprocess.run(['curl', '-s', '-m', '90', '-A', AGENT, '-w', '\n%{http_code}', url],
                       capture_output=True, text=True)
    body, code = r.stdout, ''
    if '\n' in body:
        body, code = body.rsplit('\n', 1)[0], body.rsplit('\n', 1)[-1].strip()
    if code != '200':
        return None, 'HTTP ' + (code or 'no response')
    # A 200 that is really an error page is the dangerous case, because it does not look
    # like a failure. Both caches are keyed by id, so a bad body would be cached forever.
    if need not in body:
        return None, 'page does not contain %r (%d bytes)' % (need, len(body))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(body)
    return body, 'net'


def team_index(names, slugmap, fresh, offline):
    """{slug: {date: [rid rows]}} for every school that holds a race."""
    idx, failed, net = {}, [], 0
    todo = [(n, slugmap[n]) for n in names if slugmap.get(n)]
    missing = [s for _, s in todo if not os.path.exists(os.path.join(TEAMS, s + '.html.gz'))]
    print('team pages: %d needed, %d to fetch' % (len(todo), len(missing)))
    for name, slug in todo:
        path = os.path.join(TEAMS, slug + '.html.gz')
        if net and (fresh or not os.path.exists(path)):
            time.sleep(PAUSE)
        body, src = fetch('https://www.tfrrs.org/teams/xc/%s.html' % slug, path,
                          'Cross Country', fresh, offline)
        if body is None:
            failed.append((name, src))
            continue
        if src == 'net':
            net += 1
            print('   fetched %s' % slug)
        d = {}
        for row in xc_season.parse_team(body):
            if row['xc']:
                d.setdefault(row['date'], []).append(row)
        idx[slug] = d
    return idx, failed


def main():
    argv = sys.argv[1:]
    fresh, offline = '--fresh' in argv, '--offline' in argv
    limit = next((int(argv[i + 1]) for i, a in enumerate(argv) if a == '--limit'), None)

    board = json.load(open(os.path.join(WORK, 'board.json')))
    slugmap = json.load(open(os.path.join(HERE, 'slugmap.json')))
    X = board['XCRACES']
    A = board['ATHLETE']
    PROJ = {'5K': A['proj5kxc'], '6K': A['proj6k'], '8K': A['proj8k'], '10K': A['proj10k']}
    PROJ.update(A['projOff'])   # 4M, 7K, 5.2M and the rest -- see the note in data.js

    races = [(n, i, r) for n, v in X.items() for i, r in enumerate(v)]
    print('%d races across %d schools\n' % (len(races), len(X)))

    idx, tfail = team_index(sorted(X), slugmap, fresh, offline)
    if tfail:
        print('  team page FAILED: %d' % len(tfail))
        for n, why in tfail[:10]:
            print('      %-28s %s' % (n[:28], why))

    # ---- race -> rid ------------------------------------------------------------
    plan = {}
    unresolved = []
    for name, i, r in races:
        slug = slugmap.get(name)
        by = idx.get(slug, {})
        rows = by.get(r['date'], [])
        if not rows:
            # A team page sometimes dates a row from when the result was posted rather than
            # when it was run -- Newberry's Wilmington Beach Blast is listed 15 September
            # and the page itself is headed the 12th -- so widen by a few days and let the
            # times decide. Exact first, because widening multiplies candidate pages.
            rows = [w for d, v in by.items() if abs(days(d) - days(r['date'])) <= 4
                    for w in v]
        if not rows:
            unresolved.append({'school': name, 'i': i, 'meet': r['meet'], 'date': r['date'],
                               'why': 'no dated XC row for %s within 4 days of %s'
                                      % (slug, r['date'])})
            continue
        # More than one XC result on one date happens (a meet split across two result ids).
        # Every one of them is a candidate; the times decide which page the race came from.
        for row in rows:
            plan.setdefault(row['rid'], {'url': row['url'], 'meet': row['meet'],
                                         'races': []})['races'].append((name, i, r))
    order = sorted(plan, key=lambda k: plan[k]['meet'])
    if limit:
        order = order[:limit]
    cached = sum(1 for k in order if os.path.exists(os.path.join(RESULTS, k + '.html.gz')))
    print('\nresult pages: %d meets, %d cached, %d to fetch  (~%d min paced)\n'
          % (len(order), cached, len(order) - cached, round((len(order) - cached) * PAUSE / 60)))

    # ---- fetch and compare -----------------------------------------------------
    seen = {}            # (school, i) -> best record, because a race may have 2 candidate pages
    pfail, net = [], 0
    for k, rid in enumerate(order, 1):
        p = plan[rid]
        path = os.path.join(RESULTS, rid + '.html.gz')
        if net and (fresh or not os.path.exists(path)):
            time.sleep(PAUSE)
        body, src = fetch(p['url'], path, 'Individual Results', fresh, offline)
        if body is None:
            pfail.append((rid, p['meet'], src))
            print('%3d/%d  %-44s FAILED %s' % (k, len(order), p['meet'][:44], src))
            continue
        if src == 'net':
            net += 1
        places = xc_fetch.team_places(body)
        pdate, venue, host = xc_fetch.header(body)
        d = pdate or p['races'][0][2]['date']
        secs = parse_xc.parse(body, int(d[:4]) - (1 if d[5:7] < '08' else 0))
        ntab = len([1 for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', body, re.S)
                    if 'Team Results' in m.group(1)
                    and not re.search(r'(?<!\w)wo?men|\(W\)|\bgirls\b', m.group(1), re.I)])
        for name, i, r in p['races']:
            rec = check(r, name, rid, secs, places, pdate, p['meet'], ntab, slugmap[name], PROJ)
            old = seen.get((name, i))
            # A race with two candidate pages keeps the better verdict: the page that
            # reproduces it is the page it came from, whatever the other one says. A page
            # that does not hold the team at all always loses, however short its list of
            # complaints -- one `nosection` used to outrank a real comparison and hid a
            # clean NC State race behind the Pirate Invitational it did not run.
            if old is None or (rank(rec) < rank(old)):
                seen[(name, i)] = rec
        print('%3d/%d  %-44s %-5s %2d race(s)%s'
              % (k, len(order), p['meet'][:44], src, len(p['races']),
                 '' if all(not seen[(n, i)]['bad'] for n, i, _ in p['races'] if (n, i) in seen)
                 else '  <-'))

    report(seen, unresolved, pfail, len(races), limit, '--emit' in argv)


def emit_tails(seen):
    """Write the finishers behind each race's stored seven, for tail_apply.py to splice.

    Only races that reproduced exactly are written. A race whose times did not match is a
    race whose section is in doubt, and an eighth man read off a page that might be the
    wrong page is worse than no eighth man: it would be the one number in XCRACES that no
    check had ever agreed with."""
    out, men, deepest = {}, 0, (0, None)
    for (name, i), r in sorted(seen.items()):
        if r['bad'] or 'pfin' not in r:
            continue
        # date and seven are the writer's guard, not data it needs: XCRACES is a positional
        # list, so an index written here and applied after the file moved would hang one
        # team's eighth man off another team's race. The seven that picked the section is
        # the one thing that identifies the race beyond doubt.
        rec = {'date': r['date'], 'seven': r['pfin'][:7],
               'n': len(r['pfin']), 'tail': r['pfin'][7:], 'tyears': r['pyr'][7:]}
        out.setdefault(name, {})[str(i)] = rec
        men += len(rec['tail'])
        if rec['n'] > deepest[0]:
            deepest = (rec['n'], '%s, %s' % (name, r['meet'].strip()))
    json.dump({'generated': datetime.date.today().isoformat(), 'races': out},
              open(os.path.join(WORK, 'tails.json'), 'w'), indent=1, sort_keys=True)
    withtail = sum(1 for v in out.values() for x in v.values() if x['tail'])
    print('\n--- tools/.work/tails.json ---')
    print('  races with a verified field      %d' % sum(len(v) for v in out.values()))
    print('  of those, deeper than seven      %d' % withtail)
    print('  men behind a stored seven        %d' % men)
    print('  deepest field                    %d  (%s)' % deepest)


def rank(rec):
    """Lower is a better verdict. A page with no section for the team is never the source."""
    return (any(k == 'nosection' for k, _ in rec['bad']), len(rec['bad']))


def check(r, name, rid, secs, places, pdate, meetname, ntab, slug, PROJ):
    """Everything stored about one race, against the page it came from."""
    stored = [round(float(t), 1) for t in r['runners']]
    nst = r.get('nfin') or len(r['runners'])
    rec = {'school': name, 'meet': r['meet'], 'date': r['date'], 'dist': r['dist'],
           'rid': rid, 'bad': []}
    bad = rec['bad']

    mine = [(s, [f for f in s['fin'] if f['team'] == slug]) for s in secs]
    mine = [(s, f) for s, f in mine if f]
    if not mine:
        bad.append(('nosection', 'no men\'s section on the page holds %s' % slug))
        return rec
    # The file's own times pick the section. Exact match first; otherwise the section that
    # agrees for the longest leading run, which is what makes a one-finisher-short store
    # legible instead of looking like a wholly different race.
    best = max(mine, key=lambda sf: (
        [x['sec'] for x in sf[1]][:7] == stored,
        sum(1 for a, b in zip([x['sec'] for x in sf[1]], stored) if abs(a - b) < 0.051),
        (sf[0]['dist'] or '').upper() == r['dist'],
        len(sf[1])))
    sec, fin = best
    src = [x['sec'] for x in fin]
    rec['src_n'] = len(fin)
    rec['section'] = sec['title'][:70]
    # The whole field this team put on the page, not just the seven the file stores. Carried
    # on the record so --emit can write it out: the section was chosen by the file's own
    # first seven, so an eighth man taken from it is anchored by the same match that proves
    # the race, which is the only basis on which this board stores a number at all.
    rec['pfin'] = src
    rec['pyr'] = [x['yr'] for x in fin]

    if src[:7] != stored:
        bad.append(('times', 'stored %s vs page %s' % (stored, src[:7])))
    # A stored seven is the first seven of a deeper field; a stored six has to mean the
    # team finished six. This is the shape of the UNC Asheville and UNC Greensboro bug.
    if len(src) >= 7:
        if nst != 7:
            bad.append(('nfin', 'stored %d finisher(s), page has %d' % (nst, len(src))))
    elif nst != len(src):
        bad.append(('nfin', 'stored %d finisher(s), page has %d' % (nst, len(src))))
    yrs = [x['yr'] for x in fin][:7]
    if [y or None for y in r['years'][:7]] != [y or None for y in yrs]:
        bad.append(('years', 'stored %s vs page %s' % (r['years'][:7], yrs)))
    # The men behind the seven are held in their own array and are checked like any other
    # number here. A tail is mandatory, not optional: if the page runs to twelve the file
    # has to hold twelve, or the eighth man is missing from a file that claims to carry the
    # evidence about a program's depth. That is what makes xc_fetch's tail a requirement
    # rather than a nicety -- a sweep that forgets it fails this check on the next run.
    tail = [round(float(t), 1) for t in (r.get('tail') or [])]
    tyr = [y or None for y in (r.get('tyears') or [])]
    if tail != src[7:]:
        bad.append(('tail', 'stored %d man/men behind the seven %s, page has %d %s'
                    % (len(tail), tail[:3], len(src[7:]), src[7:][:3])))
    elif tyr != [x['yr'] for x in fin][7:]:
        bad.append(('tyears', 'stored %s vs page %s'
                    % (tyr[:5], [x['yr'] for x in fin][7:][:5])))
    # Distances are compared as lengths, not as strings. A board row is scored at one of
    # four distances and a course is whatever it measures, so the file buckets: 8,057m,
    # 4.97 miles and 8,000m are all `8K`. That bucketing is a real thing to know about --
    # it is counted and its worst case named -- but it is not a disagreement.
    sm, rm = metres(sec['dist']), metres(r['dist'])
    if sm and rm:
        rec['off'] = round(sm / rm - 1, 4)
        if abs(rec['off']) > DIST_TOL:
            bad.append(('dist', 'stored %s (%dm), section says %s (%dm)'
                        % (r['dist'], rm, (sec['dist'] or '').upper(), sm)))
    if pdate and pdate != r['date']:
        bad.append(('date', 'stored %s, page header says %s' % (r['date'], pdate)))
    lvl = xc_fetch.level_of(r['meet'])
    if lvl != r['level']:
        bad.append(('level', 'stored %r, the meet name implies %r' % (r['level'], lvl)))
    pl, sc = places.get(slug, (None, None))
    # Only where the page runs a single men's team table: with a varsity and an open race
    # both scored, one dict keyed by team slug cannot say which row belongs to which race,
    # and a guess here would manufacture violations.
    if ntab == 1:
        if r.get('place') is not None and pl is not None and int(r['place']) != pl:
            bad.append(('place', 'stored %s, page says %s' % (r['place'], pl)))
        if r.get('score') is not None and sc is not None and int(r['score']) != sc:
            bad.append(('score', 'stored %s, page says %s' % (r['score'], sc)))
    else:
        rec['multi_team_table'] = ntab

    # ---- the derived fields, recomputed from the page ---------------------------
    corr = r.get('corr') or 0
    adj = [t + corr for t in src[:7]]
    proj = PROJ.get(r['dist'])
    want = {}
    if proj is not None:
        want['g1'] = round(proj - adj[0], 1)
        want['v7'] = round(proj - adj[6], 1) if len(adj) >= 7 else None
        want['slot'] = sum(1 for t in adj if t < proj) + 1
        if len(src) < 7:
            want['vlast'] = round(proj - adj[-1], 1)
    else:
        want['g1'] = want['v7'] = want['slot'] = None
    # 1st to 7th, not 1st to last: the file stores a team's first seven, and a deep squad
    # puts thirty men in an invitational. Recomputing off the whole field reported 125
    # violations, every one of them this mistake rather than the file's.
    want['spread'] = round(src[:7][-1] - src[0], 1) if len(src) > 1 else 0
    for f, w in want.items():
        g = r.get(f)
        g = round(float(g), 1) if isinstance(g, (int, float)) else g
        if (w is None) != (g is None) or (w is not None and abs(w - g) > 0.051):
            bad.append((f, 'stored %s, page gives %s' % (g, w)))
    return rec


def report(seen, unresolved, pfail, total, limit, emit=False):
    recs = list(seen.values())
    clean = [r for r in recs if not r['bad']]
    dirty = [r for r in recs if r['bad']]
    kinds = collections.Counter(k for r in dirty for k, _ in r['bad'])
    json.dump({'checked': len(recs), 'clean': len(clean),
               'unresolved': unresolved, 'page_failures': pfail,
               'violations': [{k: v for k, v in r.items() if k not in ('pfin', 'pyr')}
                              for r in dirty]}, open(OUT, 'w'), indent=1)

    print('\n--- %s ---' % os.path.relpath(OUT, os.path.dirname(HERE)))
    print('  races on file            %d' % total)
    print('  checked against a page   %d' % len(recs))
    print('  reproduced exactly       %d' % len(clean))
    print('  with a disagreement      %d' % len(dirty))
    print('  no page to check against %d' % len(unresolved))
    off = [r for r in recs if r.get('off')]
    if off:
        w = max(off, key=lambda r: abs(r['off']))
        print('  run on a course whose length is not the distance it is scored at: %d'
              % len(off))
        print('      worst %+.1f%%: %s, %s, %s scored as %s'
              % (w['off'] * 100, w['school'], w['meet'].strip()[:34], w['section'][:16],
                 w['dist']))
    if pfail:
        print('  page fetch failed        %d' % len(pfail))
        for rid, meet, why in pfail[:10]:
            print('      %-8s %-40s %s' % (rid, meet[:40], why))
    if kinds:
        print('\n  by kind: ' + ', '.join('%s %d' % kv for kv in kinds.most_common()))
    for kind, _ in kinds.most_common():
        rs = [r for r in dirty if any(k == kind for k, _ in r['bad'])]
        print('\n  -- %s (%d) --' % (kind, len(rs)))
        for r in rs[:12]:
            why = next(m for k, m in r['bad'] if k == kind)
            print('      %-24s %s  %-30s %s'
                  % (r['school'][:24], r['date'], r['meet'][:30], why[:110]))
        if len(rs) > 12:
            print('      ... and %d more in verify.json' % (len(rs) - 12))
    if unresolved and not limit:
        print('\n  -- no page to check against (%d) --' % len(unresolved))
        for u in unresolved[:12]:
            print('      %-24s %s  %s' % (u['school'][:24], u['date'], u['why'][:70]))
    if emit:
        emit_tails(seen)


if __name__ == '__main__':
    main()
