"""Splice the rebuilt races into assets/detail.js.

The generator marks the schools it has nothing new for with @@KEEP@@; their block
is copied across from the file as it stands rather than dropped, because "no
comparable race in the 2025 or 2026 season" is not the same as "no race" - those
three have results at distances this board cannot convert, and the hand-written
entry explains that.
"""
import re
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'

DETAIL = str(REPO / 'assets' / 'detail.js')
NEW = R + 'xcraces_new.js'

src = open(DETAIL).read()
m = re.search(r'(const XCRACES = \{\n)(.*?)(\n\};\n)', src, re.S)
if not m:
    raise SystemExit('XCRACES block not found')
body = m.group(2)

# Existing per-school blocks, keyed by name, so the kept ones survive verbatim.
old = {}
for b in re.finditer(r'\n?(  "([^"]+)": \[\n.*?\n  \],)', body, re.S):
    old[b.group(2)] = b.group(1)
print('existing schools in XCRACES:', len(old))

out, kept = [], []
new = open(NEW).read()
for blk in re.finditer(r'  @@KEEP@@ "([^"]+)"|  "([^"]+)": \[\n(.*?)\n  \],', new, re.S):
    if blk.group(1):
        name = blk.group(1)
        if name not in old:
            raise SystemExit('nothing to keep for ' + name)
        out.append(old[name])
        kept.append(name)
        continue
    out.append('  "%s": [\n%s\n  ],' % (blk.group(2), blk.group(3)))

txt = '\n'.join(out)
open(DETAIL, 'w').write(src[:m.start(2)] + txt + src[m.end(2):])
print('schools written:', len(out), 'kept verbatim:', kept)
print('races written:', txt.count('{ meet:'))
