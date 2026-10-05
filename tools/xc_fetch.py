"""Fetch and parse the result pages behind the races xc_season.py found unread.

  in:   tools/.work/season26.json  (python3 tools/xc_season.py)
        tools/.work/board.json     (node tools/dump_board.js)
        tools/slugmap.json
  out:  tools/.work/newraces.json

Fetched once per MEET, not once per race. 207 unread races sit at 81 meets, because a
September invitational carries a dozen board programs at the same start line -- so this
is 81 requests rather than 207, and each page answers for every school that ran it.

What is read off each page: the meet's own name, date, venue string and host; the men's
individual section with its distance; and the men's team-results table for each team's
place and score. Athletes are never named -- parse_xc drops the NAME column and this
keeps only times and the YEAR column, which is the repo rule for a public page.

Projection-dependent fields are computed only where a projection exists for the race's
distance: 5K, 6K, 8K and 10K. The 6K was added for this sweep because 89 of the 204
races read were run at it, and it is the one distance that can be added honestly -- it
falls *between* the 5K and 8K anchors, so it is interpolated off the line those two
already draw rather than extrapolated past them. assets/data.js carries the derivation
and, more usefully, the reason the obvious measurement was rejected.

The off-distances are projected too, from ATHLETE.projOff: 4M, 5.2M, 7K, 6.2K, 7.2K, 7.7K,
3.73M and 5.8K each fall between two anchors, so each takes the slower of the line between
them and a measurement off the file's own slot pairs. tools/offdist.py derives that table
and documents why the slower of the two is the only safe choice.

What still stays unprojected is a race SHORTER than 5K -- 2M, 3.6K, 4K, 4.34K. It gets its
spread, place and score, all projection-free, and a null slot/g1/v7 with `noproj` naming the
distance. There is nothing to interpolate between below his own shortest mark, so the only
route left is extrapolating past his evidence, and every one of this board's worst bugs has
been a plausible number standing where an absence belonged.

A team can appear in a result page and still have no finisher in it. All three cases in
the 2026 sweep -- North Park at the Lewis Early Bird, Morehouse at the Julius Johnson,
Saint Xavier at the Rumble In The Fort -- were entered squads whose every row reads DNS.
That is neither a parse failure nor a program that did not turn up, so it is counted and
named at the end of the run rather than silently dropped or stored as a race.

usage:
  python3 tools/xc_fetch.py              # cached where possible
  python3 tools/xc_fetch.py --fresh      # re-fetch every meet page
  python3 tools/xc_fetch.py --limit N    # first N meets, for a smoke test
"""
import gzip, json, os, re, subprocess, sys, time, html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '.work')
CACHE = os.path.join(WORK, 'tfrrs-results')
OUT = os.path.join(WORK, 'newraces.json')
sys.path.insert(0, HERE)
import parse_xc

AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')

MONTHS = {m: i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'])}

# A meet that calls itself a preview, an invitational or a tune-up is one of those,
# whatever else the name carries. "Tusculum XC Meet - SAC Conference Preview" and "United
# East Conference Preview" are September races with a conference's name in them, and the
# old classifier promoted all 23 of them into the championship set on the word
# "conference" alone -- which would have moved them inside CHAMP and into the class-mix
# floor pool and the ladder's depth count.
NOT_CHAMP = re.compile(r'invit|preview|opener|tune ?up|classic|festival|challenge'
                       r'|scrimmage|duals?\b|open\b|alumni')

# Conference championships whose name does not contain the word "conference", which is
# most of them: a conference is known by its initials and does not spell itself out. This
# is a list rather than a pattern because the alternative is guessing, and guessing here
# put 62 real conference championships on file as `area championship` -- a label this
# board reserves for the multi-conference meets (IC4A/ECAC, NEICAAA, the Metropolitan,
# DIII North, the Private Colleges) that sit between a conference and an NCAA region.
CONF = re.compile(r'\b(a-?10|acc|amcc|america east|appalachian athletic|asun|atlantic east'
                  r'|atlantic sun|big east|big sky|big south|big ten|big 12|c2c|caa|cacc'
                  r'|cciw|ciaa|cne|colonial|cunyac|cusa|centennial|ecc|gliac|gnac|gsc'
                  r'|horizon|ivy|landmark|little east|lone star|maac|mac|mac commonwealth'
                  r'|meac|missouri valley|mountain east|mountain west|mvc|nac|nacc|ne-?10'
                  r'|nec|nescac|newmac|njac|odac|ovc|pac|pac-?12|patriot|peach belt|psac'
                  r'|saa|sec|siac|socon|summit|sun belt|sunbelt|sunyac|swac|uaa|wac|wcc)\b')


# The five levels already in XCRACES. Order matters: a conference championship that also
# says "invitational" in its name is a championship, so the specific tests run first.
def level_of(meet):
    m = meet.lower()
    if 'ncaa' in m and 'region' in m:
        return 'NCAA regional'
    if NOT_CHAMP.search(m):
        return 'invitational'
    # "Championship"/"Champs", not "Champions": the Iona Br Paddy Doyle Meet of Champions
    # is a February invitational and the only race on file that the loose test got wrong.
    if not re.search(r'champs?\b|championship|nationals\b', m):
        return 'invitational'
    if re.search(r'\b(ncaa|naia|nccaa|usciaa|uscaa|njcaa)\b', m) or 'national champion' in m:
        return 'national championship'
    if 'conference' in m or CONF.search(m):
        return 'conference'
    return 'area championship'


def fetch(url, key, fresh=False):
    path = os.path.join(CACHE, key + '.html.gz')
    if not fresh and os.path.exists(path):
        with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
            return f.read(), 'cache'
    r = subprocess.run(['curl', '-s', '-m', '90', '-A', AGENT, '-w', '\n%{http_code}', url],
                       capture_output=True, text=True)
    body, code = r.stdout, ''
    if '\n' in body:
        body, code = body.rsplit('\n', 1)[0], body.rsplit('\n', 1)[-1].strip()
    if code != '200':
        return None, 'HTTP ' + (code or 'no response')
    if 'Individual Results' not in body:
        return None, 'no Individual Results section (%d bytes)' % len(body)
    os.makedirs(CACHE, exist_ok=True)
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(body)
    return body, 'net'


def header(html):
    """Meet name, date and the venue line, from the block above the first <h3>."""
    c = re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)
    # The meet name is itself the first <h3>, and the date, venue and host follow it -- so the
    # block runs from that heading to the next one, not up to it. Slicing before the first <h3>
    # read the site navigation instead and returned a null venue for every meet.
    h3 = [m.start() for m in re.finditer(r'<h3[^>]*>', c)]
    seg = c[h3[0]:h3[1]] if len(h3) > 1 else (c[h3[0]:] if h3 else c)
    # The block prints name, then "September 4, 2026", then the venue, then "HOST: ...".
    parts = [' '.join(htmllib.unescape(re.sub(r'<[^>]+>', ' ', p)).split())
             for p in re.split(r'</?(?:h1|h3|div|p|span|td|br)[^>]*>', seg)]
    parts = [p for p in parts if p]
    date, venue, host = None, None, None
    for i, p in enumerate(parts):
        dm = re.match(r'([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})$', p)
        if dm and dm.group(1) in MONTHS:
            date = '%s-%02d-%02d' % (dm.group(3), MONTHS[dm.group(1)], int(dm.group(2)))
            for q in parts[i + 1:i + 5]:
                if q.upper().startswith('HOST:'):
                    host = q[5:].strip()
                elif q != '|' and venue is None and not re.match(r'^[|\s]*$', q):
                    venue = q
    return date, venue, host


def team_places(html):
    """{team_slug: (place, score)} from the men's Team Results table."""
    heads = [(m.start(), ' '.join(htmllib.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).split()))
             for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', html, re.S)]
    out = {}
    for i, (pos, title) in enumerate(heads):
        if 'Team Results' not in title:
            continue
        up = title.upper()
        if 'WOMEN' in up or "GIRL" in up:
            continue
        if not re.search(r"(?<!WO)\bMEN'?S?\b|\(M\)|\bBOYS\b", up):
            continue
        end = heads[i + 1][0] if i + 1 < len(heads) else len(html)
        seg = html[pos:end]
        th = re.search(r'<thead.*?</thead>', seg, re.S)
        tb = re.search(r'<tbody.*?</tbody>', seg, re.S)
        if not (th and tb):
            continue
        cols = [' '.join(re.sub(r'<[^>]+>', '', c).split()).upper()
                for c in re.findall(r'<th[^>]*>(.*?)</th>', th.group(0), re.S)]
        idx = {c: j for j, c in enumerate(cols)}
        for tr in re.findall(r'<tr.*?</tr>', tb.group(0), re.S):
            tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
            sm = re.search(r'/teams/xc/([A-Za-z0-9_\-]+)\.html', tr)
            if not sm or not tds:
                continue

            def cell(n):
                j = idx.get(n)
                return ' '.join(re.sub(r'<[^>]+>', ' ', tds[j]).split()) if j is not None and j < len(tds) else ''
            pl = re.sub(r'\D', '', cell('PL'))
            sc = re.sub(r'\D', '', cell('SCORE'))
            out[sm.group(1)] = (int(pl) if pl else None, int(sc) if sc else None)
    return out


def main():
    argv = sys.argv[1:]
    fresh = '--fresh' in argv
    limit = next((int(argv[i + 1]) for i, a in enumerate(argv) if a == '--limit'), None)

    season = json.load(open(os.path.join(WORK, 'season26.json')))
    board = json.load(open(os.path.join(WORK, 'board.json')))
    slugmap = json.load(open(os.path.join(HERE, 'slugmap.json')))
    held = {k: {x['date'] for x in v if x.get('date')} for k, v in board['XCRACES'].items()}
    ath = board['ATHLETE']
    PROJ = {'5k': ath['proj5kxc'], '6k': ath['proj6k'],
            '8k': ath['proj8k'], '10k': ath['proj10k']}
    # The off-distances, keyed the way this stage keys them: dist comes off the section
    # title and is lowercased, so '4M' in the published table is '4m' here. Merged rather
    # than written out, because data.js is the one place the numbers live.
    PROJ.update({d.lower(): t for d, t in ath['projOff'].items()})

    # meet -> the schools that ran it and this board has not read
    want = {}
    for name, v in season['rows'].items():
        for r in v['races']:
            if r['date'] in held.get(name, set()):
                continue
            want.setdefault(r['rid'], {'url': r['url'], 'meet': r['meet'],
                                       'date': r['date'], 'schools': []})['schools'].append(name)
    order = sorted(want, key=lambda k: (want[k]['date'], k))
    if limit:
        order = order[:limit]
    print('%d unread race(s) at %d meet(s); fetching %d\n'
          % (sum(len(want[k]['schools']) for k in want), len(want), len(order)))

    races, failed, noproj, missing, dup = [], [], [], [], []
    fetched = 0
    for i, rid in enumerate(order, 1):
        w = want[rid]
        if fetched and (fresh or not os.path.exists(os.path.join(CACHE, rid + '.html.gz'))):
            time.sleep(1.5)
        body, src = fetch(w['url'], rid, fresh)
        if body is None:
            failed.append((rid, w['meet'], src))
            print('%3d/%d  %-46s FETCH FAILED: %s' % (i, len(order), w['meet'][:46], src))
            continue
        if src == 'net':
            fetched += 1
        pdate, venue, host = header(body)
        # The season is what turns a graduation year in the YEAR column into a class, so
        # parse_xc gets it: August starts the season the autumn is named for.
        d = pdate or w['date']
        secs = parse_xc.parse(body, int(d[:4]) - (1 if d[5:7] < '08' else 0))
        places = team_places(body)
        lvl = level_of(w['meet'])
        got = 0
        for name in w['schools']:
            slug = slugmap[name]
            # The date on a team's results table is sometimes the day the result was posted
            # rather than the day it was run: Newberry's Wilmington Beach Blast is listed
            # 15 September and the page itself is headed the 12th. The discovery stage can
            # only compare the date it was given, so a race already on file looks new to it
            # and would be added twice. The page's own header is the date that settles it.
            if (pdate or w['date']) in held.get(name, set()):
                dup.append((name, pdate or w['date'], w['date'], w['meet']))
                continue
            # A varsity section always wins, however few men this team put in it, and the
            # deepest field breaks the tie inside each kind. parse_xc now hands back the
            # open and JV sections it used to drop, flagged, so the fallback only ever
            # reaches a team with no finisher in any varsity men's race on the page --
            # which until now was recorded as a DNS. Ordering it this way is what keeps
            # every race already on file reading from the section it was read from.
            best = None
            for s in sorted(secs, key=lambda s: (bool(s.get('sub')), -s['n'])):
                fin = [f for f in s['fin'] if f['team'] == slug]
                if fin and (best is None
                            or (bool(s.get('sub')), -len(fin)) < (bool(best[0].get('sub')), -len(best[1]))):
                    best = (s, fin)
            if not best:
                missing.append((name, rid, w['meet']))
                continue
            sec, fin = best
            dist = (sec['dist'] or '').lower()
            runners = [f['sec'] for f in fin][:7]
            years = [f['yr'] for f in fin][:7]
            # Seven is what scores and seven is what every aggregate is defined over, so the
            # eighth man onward goes in his own array rather than lengthening this one. He is
            # kept because the board's own reasoning needs him: the invitationals are carried
            # on the argument that they are the evidence about a program's 5th through 9th,
            # and for 819 races on file that evidence was read off the page and dropped.
            tail = [f['sec'] for f in fin][7:]
            tyears = [f['yr'] for f in fin][7:]
            proj = PROJ.get(dist)
            rec = {'school': name, 'rid': rid, 'meet': w['meet'],
                   'date': pdate or w['date'], 'dist': dist.upper(), 'level': lvl,
                   'venue': venue, 'host': host,
                   'place': places.get(slug, (None, None))[0],
                   'score': places.get(slug, (None, None))[1],
                   'nfin': len(fin), 'runners': runners, 'years': years,
                   'tail': tail, 'tyears': tyears,
                   # One finisher is a spread of 0, which is how the 1,339 races already on
                   # file record it. school.js does not print a spread below three runners
                   # either way, but matching the convention keeps the audit at zero.
                   'spread': round(runners[-1] - runners[0], 1) if len(runners) > 1 else 0,
                   'corr': 0}
            if proj is None:
                rec.update(slot=None, g1=None, v7=None, noproj=dist.upper())
                noproj.append((name, dist.upper(), w['meet']))
            else:
                rec['g1'] = round(proj - runners[0], 1)
                rec['v7'] = round(proj - runners[6], 1) if len(runners) >= 7 else None
                rec['slot'] = sum(1 for t in runners if t < proj) + 1
            races.append(rec)
            got += 1
        print('%3d/%d  %-46s %-5s %-4s %2d/%d school(s)%s'
              % (i, len(order), w['meet'][:46], src,
                 (secs[0]['dist'] or '?').upper() if secs else '-', got, len(w['schools']),
                 '' if got == len(w['schools']) else '  <- some had no finisher here'))

    json.dump({'generated': season['generated'], 'races': races}, open(OUT, 'w'), indent=1)
    print('\n--- %s ---' % os.path.relpath(OUT, os.path.dirname(HERE)))
    print('  races parsed            %d' % len(races))
    print('  with a projection       %d' % sum(1 for r in races if r['slot'] is not None))
    print('  no projection for dist  %d' % len(noproj))
    print('  deeper than seven       %d  (%d men behind a scoring seven)'
          % (sum(1 for r in races if r['tail']), sum(len(r['tail']) for r in races)))
    if noproj:
        from collections import Counter
        print('      by distance: ' + ', '.join('%s %d' % kv for kv in
                                                Counter(d for _, d, _ in noproj).most_common()))
    # Named on the page with no finisher = an entered squad that did not start. Worth
    # printing every time: it is the one outcome that looks like a parse bug and is not.
    # Not an error and not a race: a row the discovery stage offered under one date that the
    # board already holds under the date the page itself gives. Printed because a silent skip
    # here and a silent duplicate are the two ways this stage can go wrong.
    print('  already on file under the page\'s own date: %d' % len(dup))
    for n, pd, td, meet in dup:
        print('      %-26s page %s, team page said %s  %s' % (n[:26], pd, td, meet[:34]))
    print('  team named on the page but with no finisher in it (DNS): %d' % len(missing))
    for n, rid, meet in missing[:20]:
        print('      %-26s %s  %s' % (n[:26], rid, meet[:44]))
    if failed:
        print('  FETCH FAILED: %d' % len(failed))
        for rid, meet, why in failed:
            print('      %-8s %-40s %s' % (rid, meet[:40], why))


if __name__ == '__main__':
    main()
