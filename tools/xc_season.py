"""Read every board program's TFRRS cross country page and list the races it has run
this season, so a stale board can be told from a program that has not raced.

  in:   tools/.work/board.json   (node tools/dump_board.js)
        tools/slugmap.json       -- explicit name -> TFRRS slug, no fuzzy matching
  out:  tools/.work/season26.json

Why this is its own stage. The season sweep used to be done by hand, and what it left
behind was 126 rows carrying a 2026 average and 54 carrying nothing -- with no way to
tell which of the 54 had not raced from which had simply not been read. That distinction
is the whole point. A program that has not turned up by late September is a finding
about the program; a program this board failed to read is a bug. #7 is the precedent:
Shorter sat at Verify for want of a result that was on file the whole time, because the
failure mode of a missing lookup is silence rather than an error.

So this stage only discovers and compares. It fetches no result page and computes no
average. It answers one question per row: what has this program run this season, and
what does the board not hold yet.

Every team page is cached gzipped under .work/tfrrs-teams/, so a re-run costs nothing
and --fresh is the only way to get new answers. A measurement kept without the answer
it came from cannot be rechecked, which is the lesson the Overpass work paid for.

usage:
  python3 tools/xc_season.py                 # cached where possible, fetch what is missing
  python3 tools/xc_season.py --fresh         # ignore the cache, re-fetch every page
  python3 tools/xc_season.py --only NAME     # one row, repeatable
"""
import gzip, json, os, re, subprocess, sys, time, html as htmllib
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '.work')
CACHE = os.path.join(WORK, 'tfrrs-teams')
OUT = os.path.join(WORK, 'season26.json')

AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')

MONTHS = {m: i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'])}

# Cross country runs autumn into November, so the season is named for the year it starts
# in and July is a safe cut: no college XC result is dated June or July.
TODAY = date.today()
SEASON = TODAY.year if TODAY.month >= 7 else TODAY.year - 1
SEASON_START = '%d-07-01' % SEASON


def fetch(url, cache_key, fresh=False):
    """Return (html, source). source is 'cache' or 'net', or None with an error string."""
    path = os.path.join(CACHE, cache_key + '.html.gz')
    if not fresh and os.path.exists(path):
        with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
            return f.read(), 'cache'
    r = subprocess.run(['curl', '-s', '-m', '60', '-A', AGENT, '-w', '\n%{http_code}', url],
                       capture_output=True, text=True)
    body = r.stdout
    code = body.rsplit('\n', 1)[-1].strip() if '\n' in body else ''
    body = body.rsplit('\n', 1)[0] if '\n' in body else body
    if code != '200':
        return None, 'HTTP ' + (code or 'no response')
    # A team page always names the sport. Anything shorter is an error page dressed as a 200,
    # which is the failure that is dangerous precisely because it does not look like one.
    if 'Cross Country' not in body:
        return None, 'page does not mention Cross Country (%d bytes)' % len(body)
    os.makedirs(CACHE, exist_ok=True)
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(body)
    return body, 'net'


def parse_team(html):
    """The LATEST RESULTS table: a DATE column and a MEET column holding the result link.

    Read off that table rather than off every /results/ link on the page, because the page
    also lists track meets and previous seasons with no date beside them -- and an undated
    meet cannot be placed in a season, which is the one thing this stage has to do."""
    out = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.S):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if len(tds) < 2:
            continue
        dm = re.match(r'([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})$',
                      re.sub(r'<[^>]+>', '', tds[0]).strip())
        if not dm or dm.group(1) not in MONTHS:
            continue
        iso = '%s-%02d-%02d' % (dm.group(3), MONTHS[dm.group(1)], int(dm.group(2)))
        lm = re.search(r'href="(/results/(xc/)?(\d+)/[^"]*)"', tds[1])
        if not lm:
            continue
        meet = ' '.join(htmllib.unescape(re.sub(r'<[^>]+>', ' ', tds[1])).split())
        out.append({'date': iso, 'meet': meet, 'rid': lm.group(3),
                    'url': 'https://www.tfrrs.org' + lm.group(1),
                    'xc': bool(lm.group(2))})
    return out


def main():
    argv = sys.argv[1:]
    fresh = '--fresh' in argv
    only = [argv[i + 1] for i, a in enumerate(argv) if a == '--only']

    board = json.load(open(os.path.join(WORK, 'board.json')))
    rows = board['SCHOOLS']
    held = board['XCRACES']            # keyed by name, same as assets/detail.js
    slugmap = json.load(open(os.path.join(HERE, 'slugmap.json')))
    if only:
        rows = [r for r in rows if r['name'] in only]
        if len(rows) != len(only):
            sys.exit('--only named a row not on the board: ' +
                     ', '.join(sorted(set(only) - {r['name'] for r in rows})))

    print('season %d (races dated %s or later), today %s, %d rows\n'
          % (SEASON, SEASON_START, TODAY.isoformat(), len(rows)))

    result, nokey, failed = {}, [], []
    fetched = 0
    for i, r in enumerate(rows, 1):
        name = r['name']
        slug = slugmap.get(name)
        if not slug:
            nokey.append(name)
            print('%3d/%d  %-28s NO SLUGMAP KEY' % (i, len(rows), name[:28]))
            continue
        if fetched and (fresh or not os.path.exists(
                os.path.join(CACHE, slug + '.html.gz'))):
            time.sleep(1.5)
        body, src = fetch('https://www.tfrrs.org/teams/xc/%s.html' % slug, slug, fresh)
        if body is None:
            failed.append((name, src))
            print('%3d/%d  %-28s FETCH FAILED: %s' % (i, len(rows), name[:28], src))
            continue
        if src == 'net':
            fetched += 1
        races = [x for x in parse_team(body) if x['xc'] and x['date'] >= SEASON_START]
        races.sort(key=lambda x: x['date'])
        have = {x.get('date') for x in held.get(name, []) if x.get('date')}
        new = [x for x in races if x['date'] not in have]
        result[name] = {'slug': slug, 'races': races,
                        'new': [x['date'] for x in new], 'src': src}
        flag = ('%d NEW' % len(new)) if new else ('' if races else 'none this season')
        print('%3d/%d  %-28s %-6s %2d race(s)  %s   %s'
              % (i, len(rows), name[:28], src, len(races),
                 races[-1]['date'] if races else '          ', flag))

    os.makedirs(WORK, exist_ok=True)
    json.dump({'season': SEASON, 'generated': TODAY.isoformat(), 'rows': result},
              open(OUT, 'w'), indent=1, sort_keys=True)

    raced = {k: v for k, v in result.items() if v['races']}
    idle = sorted(k for k, v in result.items() if not v['races'])
    newly = {k: v['new'] for k, v in result.items() if v['new']}
    print('\n--- %s ---' % os.path.relpath(OUT, os.path.dirname(HERE)))
    print('  read              %d  (%d over the network)' % (len(result), fetched))
    print('  raced this season %d' % len(raced))
    print('  no race on file   %d' % len(idle))
    print('  rows with a race the board does not hold: %d, %d race(s) total'
          % (len(newly), sum(len(v) for v in newly.values())))
    if newly:
        for k in sorted(newly):
            print('      %-28s %s' % (k[:28], ' '.join(newly[k])))
    if idle:
        print('  raced nothing this season (a finding about the program, not a gap):')
        for k in idle:
            print('      ' + k)
    if nokey:
        print('  NO SLUGMAP KEY (silent skip -- see #7): ' + ', '.join(nokey))
    if failed:
        print('  FETCH FAILED:')
        for k, why in failed:
            print('      %-28s %s' % (k[:28], why))


if __name__ == '__main__':
    main()
