"""Replace each school's xc aggregate in assets/data.js and add the new ones.

xc keeps its meaning - the 2025 championship races only - so the tier it supports
is the same measurement it always was, just averaged over every championship on
file rather than the one or two that had been read by hand. xcInv and xc26 are
additions: the 2025 invitational season, and the 2026 season as far as it has run.
"""
import json
import re
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'

DATA = str(REPO / 'assets' / 'data.js')
ag = json.load(open(R + 'xcagg.json'))


def num(v):
    if v is None:
        return 'null'
    return str(int(v)) if float(v) == int(v) else str(round(float(v), 1))


def obj(a, keys):
    out = []
    for k in keys:
        # False is the absence of a flag, not a value: `disagree: 0` in the file reads
        # as data when it is really "this did not happen".
        if k not in a or a[k] is None or a[k] is False:
            continue
        v = a[k]
        out.append('%s: %s' % (k, 'true' if v is True else
                               json.dumps(v) if isinstance(v, str) else num(v)))
    return '{ ' + ', '.join(out) + ' }'


src = open(DATA).read()
parts = re.split(r'(\n  \{ name: ")', src)
out = [parts[0]]
touched, added = 0, 0
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i + 1]
    name = body.split('"', 1)[0]
    a = ag.get(name)
    # Re-runnable: drop any block a previous run added before inserting again.
    body = re.sub(r'\n\s*(?:xcInv|xc26|shape): \{[^\n]*\},', '', body)
    m = re.search(r'\n(\s*)xc: \{[^\n]*\},', body)
    if a and m:
        ind = m.group(1)
        # A school whose only championship race was short of five finishers gets no
        # computed xc - there is no scoring five to average - and keeps the value that
        # was read by hand. The other three blocks are still worth having: its 2026
        # races and its class years exist whatever the championship looked like.
        lines = [ind + 'xc: ' + obj(a['xc'], ('slot', 'g1', 'v7', 'spread', 'disagree',
                                              'eq', 'nraces', 'short', 'maxfin')) + ','] \
            if a.get('xc') else [body[m.start() + 1:m.end()]]
        if a.get('xcInv'):
            lines.append(ind + 'xcInv: ' + obj(a['xcInv'], ('slot', 'g1', 'v7', 'spread',
                                                            'eq', 'nraces', 'short',
                                                            'maxfin')) + ',')
        if a.get('xc26'):
            lines.append(ind + 'xc26: ' + obj(a['xc26'], ('slot', 'g1', 'v7', 'spread',
                                                          'eq', 'nraces', 'short', 'maxfin',
                                                          'date')) + ',')
        if a.get('shape'):
            lines.append(ind + 'shape: ' + obj(a['shape'], ('date', 'meet', 'dist', 'n', 'ret',
                                                            'g1ret', 'eq', 'fr', 'so', 'jr', 'sr',
                                                            'mfr', 'mso', 'mjr', 'msr')) + ',')
        body = body[:m.start()] + '\n' + '\n'.join(lines) + body[m.end():]
        touched += 1 if a.get('xc') else 0
        added += len(lines) - 1
    out.append(head)
    out.append(body)
open(DATA, 'w').write(''.join(out))
print('schools whose xc was rewritten:', touched, ' extra blocks added:', added)
print('aggregates on file but not matched:',
      [n for n in ag if ag[n].get('xc') and ('"%s"' % n) not in src])
