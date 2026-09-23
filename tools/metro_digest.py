"""Per-metro fact sheet for writing the new metro pages from.

Everything the prose on a metro page claims has to come from a row on that page, so this
prints the rows the page will show - kept, cut, no-track and no-program - with the numbers
the page is allowed to quote, plus the aggregates a lede needs: division mix, tier counts,
how many programs he would lead, how many never finished seven, and the median net price on
his residency.
"""
import json
import statistics as st
import sys
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'
b = json.load(open(R + 'board.json'))
X = b['XCRACES']
CH = ('conference', 'area championship', 'NCAA regional', 'national championship')


def metros(s):
    return s['metro'] if isinstance(s['metro'], list) else [s['metro']]


def mi(s, m):
    return (s.get('miBy') or {}).get(m, s.get('mi'))


def net(s):
    c = s.get('cost') or {}
    if c.get('net') is None:
        return None
    prem = (c.get('tuiOut') or 0) - (c.get('tuiIn') or 0) \
        if c.get('own') == 'public' and c.get('resid') == 'out' else 0
    return c['net'] + prem


def champs(name):
    out = []
    for r in X.get(name, []):
        if r['level'] in CH and (r.get('nfin') or len(r['runners'])) >= 5:
            out.append('%s [%s %s n=%d]' % (r['meet'][:38], r['level'][:12], r['dist'],
                                            len(r['runners'])))
    return out


want = sys.argv[1:] or list(b['METROS'])
for m in want:
    M = b['METROS'][m]
    kept = [s for s in b['SCHOOLS'] if m in metros(s)]
    kept.sort(key=lambda s: mi(s, m))
    print('\n' + '=' * 100)
    print('%s  (%s, centre %s)  kept=%d' % (M['label'], M['radius'],
                                            M.get('centerLabel', ''), len(kept)))
    divs = {}
    for s in kept:
        divs[s['div']] = divs.get(s['div'], 0) + 1
    tiers = {}
    for s in kept:
        tiers[s['tier']] = tiers.get(s['tier'], 0) + 1
    nets = [net(s) for s in kept if net(s) is not None]
    css = [s.get('csShare') for s in kept if s.get('csShare')]
    lead = [s['name'] for s in kept if s.get('xc') and s['xc']['slot'] <= 1.5]
    short = [s['name'] for s in kept if s.get('xc') and s['xc'].get('v7') is None]
    unmeas = [s['name'] for s in kept if not s.get('xc')]
    print('  divisions %s   tiers %s' % (divs, tiers))
    print('  median net $%s (n=%d)   median CS share %.1f%%'
          % (format(int(st.median(nets)), ','), len(nets), st.median(css) if css else 0))
    print('  he leads (slot<=1.5): %d %s' % (len(lead), lead))
    print('  never finished seven: %d %s' % (len(short), short))
    print('  unmeasured: %d %s' % (len(unmeas), unmeas))
    print('  %-26s %-4s %-16s %5s %-8s %7s %6s %9s %5s %6s %6s %6s' %
          ('school', 'div', 'conf', 'mi', 'tier', 'net', 'cs%', 'sat', 'adm', 'slot', 'v7', 'g1'))
    for s in kept:
        x = s.get('xc') or {}
        print('  %-26s %-4s %-16s %5s %-8s %7s %6s %9s %5s %6s %6s %6s' % (
            s['name'][:26], s['div'], s['conf'][:16], mi(s, m), s['tier'],
            net(s) if net(s) is not None else '-', s.get('csShare') or '-',
            (s.get('sat') or '-')[:9], s.get('accept') or '-',
            x.get('slot', '-'), round(x['v7']) if x.get('v7') is not None else '-',
            round(x['g1']) if x.get('g1') is not None else '-'))
        for c in champs(s['name']):
            print('        %s' % c)
    for lab, arr in (('CUT', 'REMOVED'), ('NO TRACK', 'NO_TRACK'), ('NO XC', 'NO_PROGRAM')):
        rows = [s for s in b[arr] if m in metros(s)]
        if not rows:
            continue
        print('  --- %s (%d)' % (lab, len(rows)))
        for s in sorted(rows, key=lambda s: mi(s, m) if mi(s, m) is not None else 999):
            x = s.get('xc') or {}
            print('    %-26s %-4s %-16s %5s tier=%-8s slot=%-5s v7=%-6s g1=%-6s spread=%s' % (
                s['name'][:26], s.get('div', '-'), (s.get('conf') or '-')[:16], mi(s, m),
                s.get('tier', '-'), x.get('slot', '-'),
                round(x['v7']) if x.get('v7') is not None else '-',
                round(x['g1']) if x.get('g1') is not None else '-',
                round(x['spread']) if x.get('spread') is not None else '-'))
