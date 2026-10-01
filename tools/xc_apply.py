"""Splice the races xc_fetch.py read into assets/detail.js and rebuild every xc26.

  in:   tools/.work/newraces.json  (python3 tools/xc_fetch.py)
        tools/.work/board.json     (node tools/dump_board.js)
  out:  assets/detail.js  -- XCRACES, new races merged in per school, in date order
        assets/data.js    -- each row's xc26 block only

Why this touches xc26 and xcInv and nothing else. `xc` is the tier-bearing aggregate and
it means one specific thing: 2025 championship races at a five-finisher floor. Every tier
on the board rests on it, and three published blocks are hand decisions about what a race
means rather than derivations, so this stage refuses to run at all if a sweep contains a
championship race. `shape` is owned by shape_apply.py. The other two are rewritten,
because a sweep that adds races inside a season those averages cover would otherwise
publish a mean over a set of races that is no longer the set on file: xcInv is the 2025
invitational season, which is exactly where 195 of the 203 races in the last sweep landed.

The formulas were not invented here. Both were reverse-engineered from the blocks already
in data.js and are re-checked against every one of them, from the file as it stands, before
a single block is written -- 169 of 169 for xcInv -- and a disagreement stops the run,
because at that point the formula is wrong, not the file. Mean slot, mean g1, mean spread
and mean v7 over the races that have a projection and at least five finishers, every
component scaled to 8K-equivalent seconds first. Two details are easy to get wrong and
both were:
  * `short` is true when ANY race in the average fell short of seven finishers, not when
    none reached it -- nine rows carry `short` and a `v7` together, which is the only
    thing that distinguishes the two readings.
  * v7 is averaged over the races that HAVE seven finishers, while g1, slot and spread
    average over all of them, so the two are not means of the same set of races.
If a change here drops that agreement, the formula is wrong, not the file.

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
CHAMP = {'conference', 'area championship', 'NCAA regional', 'national championship'}


def same(a, b):
    """Two aggregate values agree. A flag's absence and a false flag are the same thing."""
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b)
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    if (a is None) != (b is None):
        return False
    return a is None or abs(a - b) <= 0.051


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

    # A championship race stops this stage on purpose. `xc` is the number every tier rests
    # on, and three of the published blocks are hand decisions that no formula should
    # overwrite -- Thomas Jefferson's single individual qualifier at a national meet is
    # recorded as no evidence rather than as thin depth, and that is a judgement about what
    # a race means. So a sweep may add invitationals on its own and may not quietly move a
    # tier: if one of these races is a championship, it wants a person.
    champ = [r for r in new if r['level'] in CHAMP]
    if champ:
        for r in champ[:10]:
            print('   %-26s %s  %-34s %s' % (r['school'][:26], r['date'], r['meet'][:34],
                                             r['level']))
        raise SystemExit('%d championship-level race(s) in this sweep. They belong in `xc`, '
                         'which carries the tiers, so decide them by hand. Nothing written.'
                         % len(champ))

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

    # ---- the aggregates these races belong to -----------------------------------
    allraces = dict(board['XCRACES'])
    for name, rs in byschool.items():
        allraces[name] = allraces.get(name, []) + rs

    def fin(r):
        return r.get('nfin') or len(r['runners'])

    def summarise(rs, with_date=False):
        """One aggregate block from a set of races, every component in 8K-equivalent seconds.

        maxfin saturates at seven, because that is all a stored race holds. A team that
        finished nine is on file as its first seven and reads as seven here, which is the
        one number in these blocks that the file cannot say more about than that."""
        if not rs:
            return None
        eqv = lambda k: [r[k] * EQ[r['dist']] for r in rs if r.get(k) is not None]
        sev = [r['v7'] * EQ[r['dist']] for r in rs if fin(r) >= 7 and r.get('v7') is not None]
        sp = eqv('spread')
        o = {'slot': round(statistics.fmean([r['slot'] for r in rs]), 1),
             'g1': round(statistics.fmean(eqv('g1')), 1),
             'v7': round(statistics.fmean(sev), 1) if sev else None,
             'spread': round(statistics.fmean(sp), 1) if sp else None,
             'nraces': len(rs)}
        if with_date:
            o['date'] = max(r['date'] for r in rs)
        if any(r['dist'] != '8K' for r in rs):
            o['eq'] = True
        if any(fin(r) < 7 for r in rs):
            o['short'] = True
            o['maxfin'] = max(fin(r) for r in rs)
        return o

    def cmpable(races, newer, champ=None):
        """The races an aggregate averages: this season or an earlier one, and of that level.

        Five finishers is the floor -- below it there is no scoring five for a slot to be a
        slot in -- and a distance with no projection carries no slot, g1 or v7 to average."""
        return [r for r in races
                if (r['date'] >= SEASON_START) == newer
                and (champ is None or (r['level'] in CHAMP) == champ)
                and r['dist'] in P and fin(r) >= 5 and r.get('g1') is not None]

    def xc26(races):
        return summarise(cmpable(races, newer=True), with_date=True)

    def xcinv(races):
        return summarise(cmpable(races, newer=False, champ=False))

    # Why xcInv is rewritten here and xc is not. A sweep that adds races inside the 2025
    # season changes the 2025 invitational average -- leaving it would publish a mean over
    # a set of races that is no longer the set on file. `xc` is different twice over: it is
    # the tier-bearing number, and not one of these races is championship-level, so it
    # cannot move. The gate below is what makes the xcInv rewrite safe rather than merely
    # plausible: the same formula is run against every block already published, from the
    # file as it stands before the splice, and a single disagreement stops the run. It
    # reproduces 169 of 169 today, including the two details that are easy to get wrong --
    # the 8K-equivalent scaling flagged by `eq`, and `short` meaning ANY race in the average
    # fell below seven rather than none reaching it.
    pre = {}
    for name, v in board['XCRACES'].items():
        pre[name] = xcinv(v)
    stored = {r['name']: r.get('xcInv') for r in board['SCHOOLS']}
    KEYS = ('slot', 'g1', 'v7', 'spread', 'eq', 'nraces', 'short', 'maxfin')
    gate_ok, gate_bad = 0, []
    for name, st in stored.items():
        got = pre.get(name)
        if st is None and got is None:
            continue
        if st is None or got is None:
            gate_bad.append('%s: file %s, formula %s' % (name, bool(st), bool(got)))
            continue
        d = [k for k in KEYS if not same(st.get(k), got.get(k))]
        if d:
            gate_bad.append('%s: %s' % (name, ', '.join(
                '%s file %s formula %s' % (k, st.get(k), got.get(k)) for k in d)))
        else:
            gate_ok += 1
    print('xcInv gate: %d of %d published blocks reproduce from the file'
          % (gate_ok, gate_ok + len(gate_bad)))
    if gate_bad:
        for b in gate_bad[:10]:
            print('      ' + b)
        raise SystemExit('xcInv does not reproduce, so the formula is wrong, not the file. '
                         'Nothing written.')

    def agg_js(key, a, ind):
        order = ('slot', 'g1', 'v7', 'spread', 'eq', 'nraces', 'short', 'maxfin', 'date')
        parts = []
        for k in order:
            v = a.get(k)
            if v is None or v is False:
                continue
            parts.append('%s: %s' % (k, 'true' if v is True else
                                     json.dumps(v) if isinstance(v, str) else num(v)))
        return '%s%s: { %s },' % (ind, key, ', '.join(parts))

    dsrc = DATA.read_text()
    parts = re.split(r'(\n  \{ name: ")', dsrc)
    rebuilt = [parts[0]]
    tally = {'xcInv': [0, 0, 0], 'xc26': [0, 0, 0]}     # rewritten, new, removed
    moved = []
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        name = body.split('"', 1)[0]
        want = {'xcInv': xcinv(allraces.get(name, [])), 'xc26': xc26(allraces.get(name, []))}
        # Both blocks come out, then both go back in the file's own order: xc, xcInv, xc26,
        # shape. Rewriting them in place one at a time would leave the order to whichever
        # happened to exist already, and `shape` has to stay last because it is the only
        # one of the four this stage does not own.
        held = {}
        for key in ('xcInv', 'xc26'):
            m = re.search(r'\n(\s*)%s: \{[^\n]*\},' % key, body)
            if m:
                held[key] = m.group(0)[1:]
                body = body[:m.start()] + body[m.end():]
        lines, ind = [], None
        # `xc: null` is a real value on this board - a program measured at a championship and
        # found to field one man - so the anchor has to match it as well as an object.
        anchor = (re.search(r'\n(\s*)shape: \{', body)
                  or re.search(r'\n(\s*)xc: (?:\{[^\n]*\}|null),', body))
        for key in ('xcInv', 'xc26'):
            a = want[key]
            if a is None:
                if key in held:
                    tally[key][2] += 1
                continue
            if not anchor:
                raise SystemExit('%s: %s computed but no xc or shape to place it by'
                                 % (name, key))
            ind = anchor.group(1)
            lines.append(agg_js(key, a, ind))
            if key in held:
                tally[key][0] += 1 if lines[-1].strip() != held[key].strip() else 0
                if lines[-1].strip() != held[key].strip():
                    moved.append('%s %s' % (name, key))
            else:
                tally[key][1] += 1
        if lines:
            at = anchor.start() if 'shape' in anchor.group(0) else anchor.end()
            body = body[:at] + '\n' + '\n'.join(lines) + body[at:]
        rebuilt.append(head)
        rebuilt.append(body)
    for key in ('xcInv', 'xc26'):
        print('%-5s: %d rewritten, %d new, %d removed' % ((key,) + tuple(tally[key])))
    print('        blocks whose text changed: %d' % len(moved))
    for x in moved[:8]:
        print('      ' + x)
    if len(moved) > 8:
        print('      ... and %d more' % (len(moved) - 8))
    if not dry:
        DATA.write_text(''.join(rebuilt))
    if dry:
        print('\n--dry: nothing written')


if __name__ == '__main__':
    main()
