#!/usr/bin/env python3
"""Write the re-measured `mi` values into assets/data.js.

Every row in that file carries its name and its mi on one line, so the rewrite is keyed on
the name in the line it is changing -- no positional assumptions, and a row whose name is not
in mi.json is left exactly as it was.

  in:   tools/.work/mi.json   (python3 tools/remeasure_mi.py)
  out:  assets/data.js        rewritten in place
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, 'assets', 'data.js')
MI = os.path.join(REPO, 'tools', '.work', 'mi.json')

NAME = re.compile(r'name: "((?:[^"\\]|\\.)*)"')
MIF = re.compile(r'\bmi: (-?[\d.]+)')


def main():
    mi = json.load(open(MI))
    lines = open(DATA, encoding='utf-8').read().split('\n')
    changed, untouched, moved = 0, [], []
    for i, line in enumerate(lines):
        n, m = NAME.search(line), MIF.search(line)
        if not (n and m):
            continue
        name = n.group(1)
        if name not in mi:
            untouched.append(name)
            continue
        new = mi[name]['mi']
        old = float(m.group(1))
        # Printed as given by the router, to one decimal, including a trailing .0 -- the whole
        # point is that every value in the column now comes from the same place, and a column
        # that hides which values are exact is what needed fixing.
        lines[i] = line[:m.start()] + 'mi: %.1f' % new + line[m.end():]
        changed += 1
        if abs(new - old) > 0.5:
            moved.append((name, old, new))
    open(DATA, 'w', encoding='utf-8').write('\n'.join(lines))
    print('%d rows rewritten, %d left alone' % (changed, len(untouched)))
    if untouched:
        print('  not in mi.json (%d): %s' % (len(untouched), ', '.join(sorted(untouched))))
    print('%d moved by more than half a mile' % len(moved))
    for name, old, new in sorted(moved, key=lambda r: -abs(r[2] - r[1])):
        print('   %-26s %-7s -> %-7s %+.1f' % (name, old, new, new - old))


if __name__ == '__main__':
    sys.exit(main())
