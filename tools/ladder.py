"""Run the tier ladder (methodology.html #tier-ladder) over every measured school.

The ladder describes the hand tiers rather than generating them, so this prints the
disagreements for a human to decide. In 8K-equivalent seconds: more than 45s outside
their 7th man is a cut, outside it is deep, a slot of 2 or better is caution, else
target. Where a school never finished seven the same ladder runs on the last finisher.

Recomputes the championship aggregate from the raw stored times rather than reading the
stored one, because the stored aggregate carries no `vlast` - so reading it silently
skipped the ~29 schools that have a championship race but never a 7th man, and reported
87 runnable instead of the true 116. Same derivations as stage11_races.py and sens.py.
"""
import json
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'
b = json.load(open(R + 'board.json'))
A = b['ATHLETE']
P = {'5K': A['proj5kxc'], '8K': A['proj8k'], '10K': A['proj10k']}
EQ = {d: P['8K'] / P[d] for d in P}
CHAMP = ('conference', 'area championship', 'NCAA regional', 'national championship')


def agg(races):
    rs = [r for r in races
          if r['level'] in CHAMP and r['dist'] in P
          and (r.get('nfin') or len(r['runners'])) >= 5]
    if not rs:
        return None
    v7s, vlasts, slots = [], [], []
    for r in rs:
        t = r['runners']
        corr = r.get('corr') or 0
        proj = P[r['dist']]
        if len(t) >= 7:
            v7s.append((proj - (t[6] + corr)) * EQ[r['dist']])
        vlasts.append((proj - (t[-1] + corr)) * EQ[r['dist']])
        slots.append(sum(1 for x in t[:7] if x + corr < proj) + 1)
    return {'v7': sum(v7s) / len(v7s) if v7s else None,
            'vlast': sum(vlasts) / len(vlasts),
            'slot': sum(slots) / len(slots),
            'n': len(rs), 'seven': bool(v7s)}


def ladder(x):
    if not x:
        return None
    v = x['v7'] if x['v7'] is not None else x['vlast']
    if v > 45:
        return 'cut'
    if v > 0:
        return 'deep'
    return 'caution' if x['slot'] <= 2 else 'target'


def short_champ(races):
    """Championship races too short for the ladder, which are evidence and not a gap.

    agg() needs five finishers before it will average a race, so a school that turned up
    to its conference championship with one or two men returns None above and drops out of
    the run entirely - and used to drop out silently, keeping whatever tier it was seeded
    with. Three rows sat at Verify that way with their own notes recording 1-2 finishers at
    a conference meet. A short field at a *conference* championship is a measurement of
    depth, because that is the race a program brings everyone to. A short field at a
    national championship is not, because only individual qualifiers go.
    """
    out = []
    for r in races:
        if r['level'] not in CHAMP or r['dist'] not in P:
            continue
        n = r.get('nfin') or len(r['runners'])
        if n >= 5 or not r['runners']:
            continue
        gap = (P[r['dist']] - (r['runners'][0] + (r.get('corr') or 0))) * EQ[r['dist']]
        out.append((r['level'], r['date'], n, round(-gap, 1)))
    return out


rows, run, seven = [], 0, 0
for s in b['SCHOOLS']:
    if not s.get('tier'):
        continue
    x = agg(b['XCRACES'].get(s['name'], []))
    l = ladder(x)
    if not l:
        continue
    run += 1
    seven += 1 if x['seven'] else 0
    if l != s['tier']:
        rows.append((s['name'], s['tier'], l,
                     round(x['v7'], 1) if x['v7'] is not None else None,
                     round(x['vlast'], 1), round(x['slot'], 2), x['n']))

print('anchor: 5K %d  8K %d  10K %d' % (P['5K'], P['8K'], P['10K']))
print('schools the ladder can run on: %d  (%d on a 7th man, %d on the last finisher)'
      % (run, seven, run - seven))
print('disagreements:', len(rows))
for r in sorted(rows, key=lambda r: (r[1], r[0])):
    print('  %-24s hand %-8s ladder %-8s v7 %8s vlast %9s slot %5s races %s' % r)

# This sweep runs over every row that carries a tier, not just the board. A board-only
# version of it missed Greensboro College and William Peace: both are off the board on the
# both-sports rule, both still publish "the tier it held on cross country" on a metro page,
# and both were labelled Verify on a one- and a three-man conference championship. A tier
# that says "unmeasured" about a measured squad is wrong wherever it is printed.
OFF = {r['name'] for r in b['REMOVED'] + b['NO_TRACK']}
shortonly = []
for s in b['SCHOOLS'] + b['REMOVED'] + b['NO_TRACK']:
    if not s.get('tier') or agg(b['XCRACES'].get(s['name'], [])):
        continue
    sc = short_champ(b['XCRACES'].get(s['name'], []))
    if sc:
        shortonly.append((s['name'], s['tier'], sc))

print('\nno ladder, but measured at a championship too short to average: %d' % len(shortonly))
print('  a conference or regional field under five men is evidence of a thin program, not a')
print('  gap in the evidence - these should not sit at Verify. A national championship field')
print('  is the exception: only individual qualifiers go, so a lone finisher there says nothing.')
DEPTH = ('conference', 'area championship', 'NCAA regional')
for name, tier, sc in sorted(shortonly):
    # Only a short field at a depth race is grounds for complaint. A row whose only short
    # championship is the national meet is correctly left at Verify, so saying nothing about
    # it is the point - a check that flags the one row already decided teaches you to ignore it.
    flag = ('   <-- still Verify on a short depth race, check this'
            if tier == 'verify' and any(l in DEPTH for l, _, _, _ in sc) else '')
    print('  %-24s hand %-8s%s%s' % (name, tier, ' (off the board)' if name in OFF else '', flag))
    for level, date, n, ahead in sc:
        print('      %s  %-22s %d finisher%s, he is %+.1fs on their #1'
              % (date, level, n, '' if n == 1 else 's', ahead))
