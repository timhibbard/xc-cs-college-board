"""Splice the races xc_fetch.py read into assets/detail.js and rebuild every xc26.

  in:   tools/.work/newraces.json  (python3 tools/xc_fetch.py)
        tools/.work/board.json     (node tools/dump_board.js)
  out:  assets/detail.js  -- XCRACES, new races merged in per school, in date order
        assets/data.js    -- each row's xc26 block only

Why this touches xc26 and nothing else. `xc` is the tier-bearing aggregate and it means
one specific thing: 2025 championship races at a five-finisher floor. Every tier on the
board rests on it. Recomputing it here would put the whole ladder at risk for a sweep
that adds only September invitationals -- which by definition cannot enter it. So `xc`,
`xcInv` and `shape` are left exactly as they are and only xc26 is rewritten, in place.

The xc26 formula was not invented here. It was reverse-engineered from the 153 blocks
already in data.js and then checked against all 153 before being used to write any of
them: mean slot, mean g1, mean spread and mean v7 over this season's races that have a
projection and at least five finishers, every component scaled to 8K-equivalent seconds
first. Two details are easy to get wrong and both were:
  * `short` is true when ANY race in the average fell short of seven finishers, not when
    none reached it -- nine rows carry `short` and a `v7` together, which is the only
    thing that distinguishes the two readings.
  * v7 is averaged over the races that HAVE seven finishers, while g1, slot and spread
    average over all of them, so the two are not means of the same set of races.
If a change here drops that 153/153 agreement, the formula is wrong, not the file.

usage:
  python3 tools/xc_apply.py --dry     # report what would change, write nothing
  python3 tools/xc_apply.py
"""
import json, re, statistics, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
DETAIL = REPO / 'assets' / 'detail.js'
DATA = REPO / 'assets' / 'data.js'

SEASON_START = '2026-07-01'


def num(v):
    """Match the file's own number style: 1638 rather than 1638.0."""
    if v is None:
        return 'null'
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v)


def race_js(r):
    """One race object, formatted the way the 1,339 already in the file are.

    nfin and vlast appear exactly when the team finished fewer than seven -- that is not
    a style choice, it is how the existing 446 short races are written and how school.js
    tells a short field from a full one."""
    n = r.get('nfin') or len(r['runners'])
    head = ('    { meet: %s, date: %s, dist: %s, level: %s, place: %s, score: %s,'
            % (json.dumps(r['meet']), json.dumps(r['date']), json.dumps(r['dist']),
               json.dumps(r['level']), num(r['place']), num(r['score'])))
    mid = '      slot: %s, g1: %s, v7: %s, spread: %s, corr: %s,' % (
        num(r['slot']), num(r['g1']), num(r['v7']), num(r['spread']), num(r.get('corr') or 0))
    lines = [head, mid]
    if n < 7:
        lines.append('      nfin: %d, vlast: %s,' % (n, num(r.get('vlast'))))
    lines.append('      runners: [%s],' % ', '.join(num(t) for t in r['runners']))
    lines.append('      years: [%s] },'
                 % ', '.join(json.dumps(y) if y else 'null' for y in r['years']))
    return '\n'.join(lines)


def parse_blocks(body):
    """Existing per-school blocks of XCRACES, keyed by name, kept as raw text.

    The key is decoded, because the file writes names \\u-escaped ("Rutgers\\u2013Camden")
    while every other stage carries them as real characters. Left escaped, four schools
    would look like two different schools and be emitted twice."""
    out = {}
    for m in re.finditer(r'\n?(  "([^"]+)": \[\n.*?\n  \],)', body, re.S):
        out[json.loads('"%s"' % m.group(2))] = m.group(1)
    return out


def main():
    dry = '--dry' in sys.argv[1:]
    board = json.load(open(WORK / 'board.json'))
    new = json.load(open(WORK / 'newraces.json'))['races']
    A = board['ATHLETE']
    P = {'5K': A['proj5kxc'], '6K': A['proj6k'], '8K': A['proj8k'], '10K': A['proj10k']}
    EQ = {d: P['8K'] / P[d] for d in P}

    # vlast is projection-derived, so it exists only where the distance converts. Computed
    # here rather than in xc_fetch because it is a display field, not a measurement.
    for r in new:
        n = r.get('nfin') or len(r['runners'])
        proj = P.get(r['dist'])
        r['vlast'] = round(proj - r['runners'][-1], 1) if (proj and n < 7) else None

    # ---- XCRACES ---------------------------------------------------------------
    src = DETAIL.read_text()
    m = re.search(r'(const XCRACES = \{\n)(.*?)(\n\};\n)', src, re.S)
    if not m:
        raise SystemExit('XCRACES block not found in assets/detail.js')
    old = parse_blocks(m.group(2))

    byschool = {}
    for r in new:
        byschool.setdefault(r['school'], []).append(r)

    # xc_fetch only ever returns a race on a date the school had nothing on, so a clash
    # here means the two stages disagree about what is on file -- worth stopping for.
    held = {k: {x['date'] for x in v} for k, v in board['XCRACES'].items()}
    for name, rs in byschool.items():
        clash = sorted({r['date'] for r in rs} & held.get(name, set()))
        if clash:
            raise SystemExit('%s: already holds a race on %s' % (name, ', '.join(clash)))

    # Each school's block is swapped in place rather than the whole body being rebuilt from
    # the parsed blocks. Two reasons, both learned the hard way: rebuilding reorders the
    # file (it is not alphabetical - it opens DePaul, Davidson, ETSU, Elon), which buries
    # 204 added races in a 12,000-line diff; and it silently drops anything that is not a
    # block, which here is the comment explaining why Drew's nine races are kept with no
    # page behind them. An in-place swap cannot lose what it does not touch.
    body = m.group(2)
    added_school, added_race, appended = 0, 0, []
    for name, rs in byschool.items():
        rows = board['XCRACES'].get(name, [])
        # Sorted on date ALONE, and Python's sort is stable, so races already on file keep
        # their relative order and a new race lands after an existing one of the same date.
        # Adding meet to the key would reshuffle races the board already had.
        merged = sorted(rows + rs, key=lambda r: r['date'])
        block = '  %s: [\n%s\n  ],' % (json.dumps(name), '\n'.join(race_js(r) for r in merged))
        if name in old:
            if body.count(old[name]) != 1:
                raise SystemExit('%s: block is not uniquely locatable' % name)
            body = body.replace(old[name], block, 1)
        else:
            appended.append(block)
        added_school += 1
        added_race += len(rs)
    if appended:
        body = body + '\n' + '\n'.join(appended)

    newsrc = src[:m.start(2)] + body + src[m.end(2):]
    print('XCRACES: %d schools touched (%d new to the file), %d races added'
          % (added_school, len(appended), added_race))
    if not dry:
        DETAIL.write_text(newsrc)

    # ---- xc26 ------------------------------------------------------------------
    allraces = dict(board['XCRACES'])
    for name, rs in byschool.items():
        allraces[name] = allraces.get(name, []) + rs

    def fin(r):
        return r.get('nfin') or len(r['runners'])

    def xc26(races):
        rs = [r for r in races if r['date'] >= SEASON_START and r['dist'] in P
              and fin(r) >= 5 and r.get('g1') is not None]
        if not rs:
            return None
        eqv = lambda k: [r[k] * EQ[r['dist']] for r in rs if r.get(k) is not None]
        sev = [r['v7'] * EQ[r['dist']] for r in rs if fin(r) >= 7 and r.get('v7') is not None]
        sp = eqv('spread')
        o = {'slot': round(statistics.fmean([r['slot'] for r in rs]), 1),
             'g1': round(statistics.fmean(eqv('g1')), 1),
             'v7': round(statistics.fmean(sev), 1) if sev else None,
             'spread': round(statistics.fmean(sp), 1) if sp else None,
             'nraces': len(rs), 'date': max(r['date'] for r in rs)}
        if any(r['dist'] != '8K' for r in rs):
            o['eq'] = True
        if any(fin(r) < 7 for r in rs):
            o['short'] = True
            o['maxfin'] = max(fin(r) for r in rs)
        return o

    def xc26_js(a, ind):
        order = ('slot', 'g1', 'v7', 'spread', 'eq', 'nraces', 'short', 'maxfin', 'date')
        parts = []
        for k in order:
            v = a.get(k)
            if v is None or v is False:
                continue
            parts.append('%s: %s' % (k, 'true' if v is True else
                                     json.dumps(v) if isinstance(v, str) else num(v)))
        return '%sxc26: { %s },' % (ind, ', '.join(parts))

    dsrc = DATA.read_text()
    parts = re.split(r'(\n  \{ name: ")', dsrc)
    rebuilt = [parts[0]]
    changed, created, removed = 0, 0, 0
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        name = body.split('"', 1)[0]
        a = xc26(allraces.get(name, []))
        had = re.search(r'\n(\s*)xc26: \{[^\n]*\},', body)
        if had:
            body = body[:had.start()] + body[had.end():]
        if a:
            # Insert where the file already puts it: after xc/xcInv, before shape.
            # `xc: null` is a real value on this board - a program measured at a
            # championship and found to field one man - so the anchor has to match it as
            # well as an object. Thomas Jefferson is that row, and it has a 2026 race.
            anchor = (re.search(r'\n(\s*)shape: \{', body)
                      or re.search(r'\n(\s*)xcInv: \{[^\n]*\},', body)
                      or re.search(r'\n(\s*)xc: (?:\{[^\n]*\}|null),', body))
            if not anchor:
                raise SystemExit('%s: xc26 computed but no xc/xcInv/shape to place it by' % name)
            ind = anchor.group(1)
            at = anchor.start() if 'shape' in anchor.group(0) else anchor.end()
            body = body[:at] + '\n' + xc26_js(a, ind) + body[at:]
            changed += 1 if had else 0
            created += 0 if had else 1
        elif had:
            removed += 1
        rebuilt.append(head)
        rebuilt.append(body)
    print('xc26: %d rewritten, %d new, %d removed' % (changed, created, removed))
    if not dry:
        DATA.write_text(''.join(rebuilt))
    if dry:
        print('\n--dry: nothing written')


if __name__ == '__main__':
    main()
