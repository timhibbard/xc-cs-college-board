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
