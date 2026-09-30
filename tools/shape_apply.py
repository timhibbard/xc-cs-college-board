"""Recompute every row's `shape` block in assets/data.js from the races on file.

  in:   tools/.work/board.json   (node tools/dump_board.js)
  out:  assets/data.js           -- each row's shape block only

`shape` is the class mix: the seven men a team actually put on the course in one race,
counted by year, plus how many of them come back and how far behind their fastest
returning man he would have arrived. It is read off ONE race because no athlete names
are stored on this site, so there is nothing to deduplicate by and pooling two races
would count the same sophomore twice.

WHICH race, and why this changed. The rule published in methodology.html #class-years is
"the most recent season wins, because its years are the current ones; within that season
the deepest race wins, because it shows the most of the squad". The code that last wrote
these blocks did something else -- deepest CHAMPIONSHIP race of any season -- and that
was defensible while the file held only the 2025 season: a September invitational is a
soft place to read a front-runner gap, because the team is not sorted out yet and its #1
is not racing flat out. Then the 2026 sweep put 410 fall-2026 races on file and the two
rules came apart hard: 197 of these rows now have a more recent season to read, and the
stored mix was describing a squad whose seniors had already graduated. A soft gap is a
caveat; reporting graduated men as returning is an error. So the season wins, the page
says when the race it read was an invitational, and g1ret is read with that in mind.

The five-finisher floor is kept and the "any race at all" fallback is dropped. Every one
of the 205 blocks this replaces came off a race that fielded at least five, and below
five there is no mix to read -- one man's class year is not a squad shape.

Safety gate. Nothing is written until --verify reproduces all 205 stored blocks
byte-for-byte under the OLD rule, the same discipline xc_apply.py used on xc26. Three
details were reverse-engineered rather than guessed and all three are load-bearing:
  * g1ret is the gap to the first man in FINISH order who is not a senior, corrected and
    scaled to 8K-equivalent seconds like every other gap here -- not the fastest of the
    returning men taken as a set, which is the same thing only because finish order is
    time order.
  * the m* floors ("at least three freshmen raced for this team elsewhere") compare
    against OTHER races of the same season with no finisher floor at all, so a
    three-man championship can raise the floor even though it is too short to average.
  * a floor is carried only where it beats the race being shown, so `mfr: 3` means
    "there is at least one more freshman than you can see", never a roster total.
One thing --verify deliberately cannot cover: the floor pool is WIDENED here from
same-season championships to same-season races of any kind, which is what school.js has
always said it was ("the most of that class seen in any other race of the same season").
The old restriction was incidental -- the source race was a championship, so the pool was
too -- and carrying it forward would have quietly killed the line, because fall 2026 has
35 championship races in the whole file and a 2026-sourced row would have had nothing to
compare against. --verify proves the old pool reproduced 205/205 before the widening; the
widening itself shows up as added m* keys in the --dry diff and nowhere else.

usage:
  python3 tools/shape_apply.py --verify   # rebuild the stored blocks, write nothing
  python3 tools/shape_apply.py --dry      # report what the new rule changes
  python3 tools/shape_apply.py
"""
import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
DATA = REPO / 'assets' / 'data.js'

GROUPS = ('SCHOOLS', 'REMOVED', 'NO_TRACK', 'NO_PROGRAM')
CHAMP = {'conference', 'area championship', 'NCAA regional', 'national championship'}
ORDER = ['FR', 'SO', 'JR', 'SR']
KEYS = ('date', 'meet', 'dist', 'n', 'ret', 'g1ret', 'eq', 'inv',
        'fr', 'so', 'jr', 'sr', 'mfr', 'mso', 'mjr', 'msr')


def num(v):
    if v is None:
        return 'null'
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v)


def season(d):
    """A cross country season is named for its autumn: August starts a new one."""
    return int(d[:4]) - (1 if d[5:7] < '08' else 0)


def fin(r):
    return r.get('nfin') or len(r['runners'])


def pick(allr, old=False):
    """The one race a row's class mix is read from."""
    cmp_ = [r for r in allr if r.get('g1') is not None and fin(r) >= 5]
    if old:
        # The rule that wrote the stored blocks: deepest championship of any season,
        # falling back to the deepest comparable race. Kept only so --verify can prove
        # the emitter below reproduces the file before it is allowed to replace it.
        pool = [r for r in cmp_ if r['level'] in CHAMP] or cmp_
    else:
        pool = [r for r in cmp_ if season(r['date'])
                == max(season(x['date']) for x in cmp_)] if cmp_ else []
    if not pool:
        return None
    # Deepest first, later date breaking the tie.
    return sorted(pool, key=lambda r: (fin(r), r['date']))[-1]


def build(allr, src, eq, old=False):
    yrs = src['years'][:7]
    sn = season(src['date'])
    c = collections.Counter(y for y in yrs if y)
    corr = src.get('corr') or 0
    o = {'date': src['date'], 'meet': src['meet'], 'dist': src['dist'], 'n': len(yrs),
         # Returning = not a senior. Counted off known years only, so a row with an
         # unknown year understates rather than guesses.
         'ret': sum(1 for y in yrs if y and y != 'SR'),
         'g1ret': None, 'eq': src['dist'] != '8K', 'inv': src['level'] not in CHAMP}
    for i, y in enumerate(yrs):
        if y and y != 'SR':
            o['g1ret'] = round((eq['proj'][src['dist']] - (src['runners'][i] + corr))
                               * eq['f'][src['dist']], 1)
            break
    for k, lo in zip(ORDER, ('fr', 'so', 'jr', 'sr')):
        o[lo] = c.get(k, 0)
        # "Men this race did not have": the most of that class seen in any OTHER race of
        # the same season, carried only where it beats this one. No finisher floor here --
        # a three-man race proves a fourth junior exists just as well as a full seven.
        mx = max([sum(1 for y in r['years'][:7] if y == k) for r in allr
                  if r is not src and season(r['date']) == sn
                  and (r['level'] in CHAMP or not old)], default=0)
        o['m' + lo] = mx if mx > c.get(k, 0) else None
    return o


def shape_js(a, ind):
    parts = []
    for k in KEYS:
        v = a.get(k)
        if v is None or v is False:
            continue
        parts.append('%s: %s' % (k, 'true' if v is True else
                                 json.dumps(v) if isinstance(v, str) else num(v)))
    return '%sshape: { %s },' % (ind, ', '.join(parts))


def main():
    argv = sys.argv[1:]
    verify, dry = '--verify' in argv, '--dry' in argv
    board = json.load(open(WORK / 'board.json'))
    X = board['XCRACES']
    A = board['ATHLETE']
    proj = {'5K': A['proj5kxc'], '6K': A['proj6k'], '8K': A['proj8k'], '10K': A['proj10k']}
    eq = {'proj': proj, 'f': {d: proj['8K'] / proj[d] for d in proj}}

    # A row's shape can only be read from a race whose distance has a projection to
    # measure the gap against; the handful of 4M and 5.2M races have none.
    def races(name):
        return [r for r in X.get(name, []) if r['dist'] in proj]

    src = DATA.read_text()
    parts = re.split(r'(\n  \{ name: ")', src)

    if verify:
        rebuilt, stored, bad = 0, 0, []
        for i in range(1, len(parts), 2):
            body = parts[i + 1]
            name = body.split('"', 1)[0]
            m = re.search(r'\n(\s*)(shape: \{[^\n]*\},)', body)
            if not m:
                continue
            stored += 1
            rs = races(name)
            s = pick(rs, old=True)
            got = shape_js(build(rs, s, eq, old=True), '').strip() if s else '(none)'
            if got == m.group(2):
                rebuilt += 1
            else:
                bad.append((name, m.group(2), got))
        print('--verify: %d of %d stored shape blocks rebuilt byte-for-byte' % (rebuilt, stored))
        for name, want, got in bad[:10]:
            print('  %s\n    file: %s\n    got:  %s' % (name, want, got))
        raise SystemExit(0 if rebuilt == stored else 1)

    out = [parts[0]]
    kept, changed, created, removed = 0, 0, 0, 0
    seasons, levels = collections.Counter(), collections.Counter()
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        name = body.split('"', 1)[0]
        rs = races(name)
        s = pick(rs)
        had = re.search(r'\n(\s*)shape: \{[^\n]*\},', body)
        old = had.group(0).strip() if had else None
        if had:
            body = body[:had.start()] + body[had.end():]
        if s:
            a = build(rs, s, eq)
            seasons[season(s['date'])] += 1
            levels[s['level']] += 1
            # shape sits last of a row's aggregate blocks, after whichever of
            # xc/xcInv/xc26 that row happens to have.
            anchor = None
            for pat in (r'\n(\s*)xc26: \{[^\n]*\},', r'\n(\s*)xcInv: \{[^\n]*\},',
                        r'\n(\s*)xc: (?:\{[^\n]*\}|null),'):
                for m in re.finditer(pat, body):
                    anchor = m
                if anchor:
                    break
            if not anchor:
                raise SystemExit('%s: shape computed but no xc/xcInv/xc26 to place it by' % name)
            line = shape_js(a, anchor.group(1))
            body = body[:anchor.end()] + '\n' + line + body[anchor.end():]
            if old is None:
                created += 1
            elif line.strip() == old:
                kept += 1
            else:
                changed += 1
        elif had:
            removed += 1
        out.append(head)
        out.append(body)
    print('shape: %d rewritten, %d unchanged, %d new, %d removed'
          % (changed, kept, created, removed))
    print('  source seasons:', dict(sorted(seasons.items())))
    print('  source levels: ', dict(levels.most_common()))
    if dry:
        print('\n--dry: nothing written')
    else:
        DATA.write_text(''.join(out))


if __name__ == '__main__':
    main()
