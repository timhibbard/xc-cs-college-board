#!/usr/bin/env python3
"""Re-measure every row's `mi` on one router, because the column was not all one thing.

A thirty-row sample against OSRM disagreed on six, every one of them a whole number and
every one of them low: Medgar Evers 7 against 10.5, Stevens 3 against 4.6, NJIT 12 against
13.9. Small in absolute terms and none of them changed a shortlist, but the North Carolina
page claims in prose that the same router produced every Mi on the board, and that claim has
to be true rather than nearly true.

So this asks OSRM for all 243 rows, from the centre of the metro each row is already
assigned to -- not the nearest centre, which is how the column was first built. The two
agree for every row that is in the metro it is closest to, and where they would disagree the
assigned metro is the one the board actually presents the row under.

Nothing is dropped. A row that now measures past its metro's radius is printed loudly and
left in place: whether a school leaves the board is a decision, not a rounding.

  in:   tools/.work/board.json   (node tools/dump_board.js)
  out:  tools/.work/mi.json      -- merged, so a re-run only fetches what is missing
  then: python3 tools/apply_mi.py
  args: [n] rows this pass, or a school name to do one row
"""
import json, os, subprocess, sys, time

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.work')
OUT = os.path.join(WORK, 'mi.json')
PACE = 1.5
M_PER_MI = 1609.34


def drive_mi(frm, to, tries=4):
    """Miles by road, or None. curl rather than urllib: this python has no CA bundle."""
    url = ('https://router.project-osrm.org/route/v1/driving/'
           '%s,%s;%s,%s?overview=false' % (frm[1], frm[0], to[1], to[0]))
    for i in range(tries):
        out = subprocess.run(['curl', '-s', '-m', '30', url],
                             capture_output=True, text=True).stdout
        try:
            j = json.loads(out)
            if j.get('code') == 'Ok':
                return j['routes'][0]['distance'] / M_PER_MI
        except Exception:
            pass
        time.sleep(5 * (i + 1))
    return None


def main():
    board = json.load(open(os.path.join(WORK, 'board.json')))
    metros = board['METROS']
    rows = {r['name']: r for key in ('SCHOOLS', 'REMOVED', 'NO_TRACK', 'NO_PROGRAM')
            for r in board[key]}
    have = json.load(open(OUT)) if os.path.exists(OUT) else {}
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    todo = ([arg] if arg and not arg.isdigit()
            else [n for n in sorted(rows) if n not in have][:int(arg or 10)])

    for i, name in enumerate(todo, 1):
        r = rows[name]
        m = metros.get(r['metro'])
        if not m:
            print('%3d/%-3d %-26s no metro centre on file' % (i, len(todo), name))
            continue
        d = drive_mi(m['center'], (r['lat'], r['lon']))
        if d is None:
            print('%3d/%-3d %-26s OSRM failed, left for a later pass' % (i, len(todo), name),
                  flush=True)
            time.sleep(PACE)
            continue
        have[name] = {'mi': round(d, 1), 'was': r['mi'], 'metro': r['metro']}
        gap = round(d - r['mi'], 1)
        flag = ''
        if abs(gap) > 0.5:
            flag = '  moved'
        if d > m.get('radiusMi', 20):
            flag += '  PAST THE %s-MILE RADIUS' % m.get('radiusMi', 20)
        print('%3d/%-3d %-26s %-12s was %-6s now %-6s gap %+5s%s'
              % (i, len(todo), name, r['metro'], r['mi'], round(d, 1), gap, flag), flush=True)
        json.dump(have, open(OUT, 'w'), indent=1, sort_keys=True)
        if i < len(todo):
            time.sleep(PACE)

    moved = [(n, v) for n, v in have.items() if abs(v['mi'] - v['was']) > 0.5]
    print('\n%d rows measured, %d move by more than half a mile' % (len(have), len(moved)))
    for n, v in sorted(moved, key=lambda kv: -abs(kv[1]['mi'] - kv[1]['was']))[:20]:
        print('   %-26s %-12s %-6s -> %-6s %+.1f' % (n, v['metro'], v['was'], v['mi'],
                                                     v['mi'] - v['was']))
    over = [(n, v) for n, v in have.items()
            if v['mi'] > metros[v['metro']].get('radiusMi', 20)]
    if over:
        print('\n%d now measure past their metro radius -- left in place, decide by hand:'
              % len(over))
        for n, v in sorted(over, key=lambda kv: -kv[1]['mi']):
            print('   %-26s %-12s %-6s -> %s' % (n, v['metro'], v['was'], v['mi']))


if __name__ == '__main__':
    main()
