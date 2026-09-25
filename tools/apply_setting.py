#!/usr/bin/env python3
"""Write the campus-setting column into assets/data.js and assets/detail.js (#13).

Two blocks, because the two files have two jobs and that split already exists here:

  data.js    `SETTING`, keyed by the row's **name** -- one compact record per row, which
             is what the board table and the school page lede need. Name and not slug:
             twelve rows (mostly NO_PROGRAM) have no page and so no slug, and a school
             with no men's team still has a walkability worth showing on its row.
  detail.js  `SETLINES`, keyed by **slug** -- the full named rail and bus lists, which
             only a school page renders. 231 rows have a slug; 171 have a line to list.

Re-running replaces both blocks in place, so this is the only thing that writes them.

  in:   tools/.work/setting1.json    (python3 tools/setting_locale.py)
        tools/.work/walkscore.json   (python3 tools/setting_walkscore.py, then --lines)
  out:  assets/data.js, assets/detail.js
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, 'tools', '.work')
DATA = os.path.join(REPO, 'assets', 'data.js')
DETAIL = os.path.join(REPO, 'assets', 'detail.js')

SETTING_DOC = """
/* Campus setting: what it is like to live here without a car.

   **This is one axis of the two this column was designed around.** The errands axis is
   here; the training axis -- nearest park and its acreage, soft-surface mileage, the
   largest *connected* network of it, signalised crossings per mile, campus acreage and
   the nearest track -- is issue #24 and is not in this file yet. Nothing below says
   anything about whether he can run here, and a high `walk` in particular is a claim
   about groceries and not about a six-mile easy day. Read it as half a picture.

   Keyed by the row's own `name`. Fields:

     loc, locCode   the federal locale, IPEDS HD2023 `LOCALE`. This is the density answer
                    and the only one that covers all 243 rows: 11/12/13 city large,
                    midsize and small, 21/22/23 suburb, 31/32/33 town, 41/42/43 rural.
     town*          the row's own Census place or minor civil division -- its name, its
                    land area in square miles, and how far the campus sits from its
                    centre. `townMi` is distance to the town centre and is NOT the Mi
                    column, which measures to the metro centre from home.
     walk, bike     Walk Score and Bike Score, scraped from the public page in `ws` and
                    attributed there. Third-party numbers, reproduced with their source.
     tscore         Transit Score, **and its absence is not a zero**. Walk Score prints
                    one only where the city publishes a feed it has ingested, so 121 of
                    243 rows have none -- including Columbia, which has the 1 train at
                    the door. Where this is null the rail and bus lists are the answer
                    and this field should not be rendered at all.
     rail*, bus*    nearest named line and how many were listed, from the same page.
                    `railN: 0` with `busN: 0` is a real finding rather than a gap in the
                    read -- Covenant College on Lookout Mountain has neither. The named
                    lines themselves are in SETLINES in detail.js.
     lvl, off       how well the page's answer matches this campus, and the whole
                    accuracy of the column. `address` (230 rows) is the campus's own
                    street address; `approx` (12) is a nearby street, `off` miles from
                    the coordinate this board holds, because that site's geocoder would
                    not take the exact address; `town` (1, Erskine) is the town's own
                    page, because it put all three address forms 78 miles away. Nothing
                    was stored at all unless the coordinate in the page's own map tiles
                    landed within 1.5 miles of this board's coordinate -- asked about a
                    bare lat/lng that site once answered about a village in Maharashtra,
                    and a wrong address still returns a page with somebody else's scores.
     ws             the page every number on the row came from. */"""

LINES_DOC = """
/* The named rail and bus lines near each campus, from the same Walk Score page the
   SETTING row in data.js cites, as [name, miles] nearest first.

   These exist because reading the Transit *Score* alone was wrong for half the board:
   that number is printed only on one of the two page shapes, so 120 rows read as "no
   transit feed" while their pages plainly listed the lines. Of those 120, 48 had named
   rail or bus -- Columbia with the 1 train at 0.0 miles, Bowie State with the MARC Penn
   Line at 0.2. So the lines are the primary answer here and the score is the summary.

   Distances are that site's, to the address in `SETTING[...].ws`, and a 0.0 means under
   a twentieth of a mile rather than exactly zero. Names are kept verbatim: the proxy
   sometimes repeats a badge label, so "Orange Line" can arrive with a letter stuck to
   it, and only exact repeats of the same line were dropped. A row absent from here
   either has no page or had neither rail nor bus listed -- SETTING carries railN and
   busN so the school page can tell those two apart. */"""


def num(v):
    """A float that prints as short as it honestly can: 0.0 stays 0.0 because it means
    'under a twentieth of a mile', not 'unknown'."""
    return ('%.1f' % v).rstrip('0').rstrip('.') if v != round(v, 1) else '%.1f' % v


def js(v):
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, float):
        return num(v)
    if isinstance(v, int):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def setting_block(s1, ws):
    out = [SETTING_DOC.strip(), 'const SETTING = {']
    for name in sorted(s1, key=str.lower):
        a, w = s1[name], ws[name]
        rail, bus = w.get('rail') or [], w.get('bus') or []
        f = [('loc', a['locale']), ('locCode', a['localeCode']),
             ('town', a['townName']), ('townMi', a['townMi']), ('townSqMi', a['townSqMi']),
             ('walk', w.get('walk')), ('bike', w.get('bike')), ('tscore', w.get('transit')),
             ('railN', len(rail)), ('railMi', rail[0]['mi'] if rail else None),
             ('busN', len(bus)), ('busMi', bus[0]['mi'] if bus else None),
             ('lvl', w.get('level')), ('off', w.get('offBy')), ('ws', w.get('url'))]
        body = ', '.join('%s: %s' % (k, js(v)) for k, v in f if v is not None or k in
                         ('walk', 'bike', 'tscore', 'railMi', 'busMi'))
        out.append('  %s:' % json.dumps(name, ensure_ascii=False))
        out.append('    { %s },' % body)
    out.append('};')
    return '\n'.join(out)


def lines_block(s1, ws):
    out = [LINES_DOC.strip(), 'const SETLINES = {']
    n = 0
    for name in sorted(s1, key=str.lower):
        slug, w = s1[name].get('slug'), ws[name]
        rail, bus = w.get('rail') or [], w.get('bus') or []
        if not slug or not (rail or bus):
            continue
        n += 1
        parts = []
        for key, lst in (('rail', rail), ('bus', bus)):
            if lst:
                parts.append('%s: [%s]' % (key, ', '.join(
                    '[%s, %s]' % (json.dumps(g['name'], ensure_ascii=False), num(g['mi']))
                    for g in lst)))
        out.append('  %s:' % json.dumps(slug))
        out.append('    { %s },' % ', '.join(parts))
    out.append('};')
    return '\n'.join(out), n


def splice(path, const, block, anchor=None):
    """Replace `const NAME = {...};` if it is already there, else put it in: before
    `anchor` if one is given, otherwise at the end of the file.

    The end of an existing block is found by scanning for a `};` in the first column,
    which is how every top-level object in these two files closes -- no brace counting,
    and a nested `};` in here is always indented. The doc comment immediately above the
    const is replaced with it, so editing the comment in this script is what edits the
    comment in the file."""
    src = open(path, encoding='utf-8').read()
    decl = src.find('const %s = {' % const)
    if decl >= 0:
        start, doc = decl, src.rfind('/*', 0, decl)
        # Only swallow the comment if it is this const's own -- one `*/` between it and
        # the declaration means nothing else sits in the gap.
        if doc >= 0 and src[doc:decl].count('*/') == 1 and not src[doc:decl].strip().endswith(';'):
            start = doc
        end = src.find('\n};\n', decl)
        if end < 0:
            sys.exit('%s: could not find the end of %s' % (path, const))
        return path, src[:start] + block + src[end + len('\n};\n'):], 'replaced'
    if anchor:
        at = src.find(anchor)
        if at < 0:
            sys.exit('%s: anchor %r not found' % (path, anchor[:40]))
        return path, src[:at] + block + '\n\n' + src[at:], 'inserted'
    return path, src.rstrip('\n') + '\n\n' + block + '\n', 'appended'


def main():
    s1 = json.load(open(os.path.join(WORK, 'setting1.json')))
    ws = json.load(open(os.path.join(WORK, 'walkscore.json')))
    missing = [n for n in s1 if n not in ws or 'walk' not in ws[n]]
    if missing:
        sys.exit('%d rows have no Walk Score yet: %s' % (len(missing), ', '.join(missing[:8])))
    unread = [n for n in s1 if 'rail' not in ws[n]]
    if unread:
        sys.exit('%d rows never had their transit lines read -- run '
                 'setting_walkscore.py --lines first: %s' % (len(unread), ', '.join(unread[:8])))

    block, n = lines_block(s1, ws)
    # Both files are written only after both blocks have been built, so a failure part way
    # through leaves neither half-written.
    edits = [splice(DATA, 'SETTING', setting_block(s1, ws), 'const SCHOOLS = ['),
             splice(DETAIL, 'SETLINES', block)]
    for path, src, _ in edits:
        # Exactly one trailing newline. Without this the run after an append cannot find
        # its own block again: replacing the last const in a file consumes the closing
        # "\n};\n" and the new block does not carry one, so the file ends at "};" and the
        # next run reports "could not find the end of SETLINES".
        open(path, 'w', encoding='utf-8').write(src.rstrip('\n') + '\n')
    print('data.js   SETTING  %s, %d rows' % (edits[0][2], len(s1)))
    print('detail.js SETLINES %s, %d rows with a named line' % (edits[1][2], n))


if __name__ == '__main__':
    main()
