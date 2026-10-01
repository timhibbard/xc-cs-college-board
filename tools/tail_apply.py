"""Add the men behind each race's scoring seven to assets/detail.js.

  in:   tools/.work/tails.json   (python3 tools/xc_verify.py --emit)
        tools/.work/board.json   (node tools/dump_board.js)
  out:  assets/detail.js  -- `tail` and `tyears` on every race whose team finished
                             more than seven. Nothing else on a race is touched.
        assets/data.js    -- the `maxfin` number inside existing xc/xcInv/xc26 blocks,
                             where the tail proves the published count too low. One number
                             per block; no field is added, removed or reordered.

Why this exists. This board keeps a team's first seven because seven is what scores, and
every aggregate on it -- slot, the gap to their 7th man, the 1-to-7 spread -- is defined
over exactly those seven. But methodology.html says the invitationals are kept because
they are "the best evidence there is about the men BEHIND a team's front, because that is
where a program's 5th through 9th runners actually race", and the 8th and 9th man were not
in the file at all. 819 of the 1,745 races on file put more than seven men on their page;
3,419 of those men were read, checked and then dropped on the floor. The page said it and
the file did not, which is the kind of gap this repo keeps paying for somewhere else.

Why a separate array and not a longer `runners`. Lengthening runners would have been the
tidier model and the wrong change: a dozen call sites take runners[0] as their #1,
runners[6] as their 7th man, runners.length as "how many finished" and runners.length-1 as
their last. A deep squad puts thirty men in an invitational -- Wingate put thirty in one --
so every one of those would have gone on working and started answering a different
question. `tail` adds evidence without moving any number that is already published.

What makes this safe. The tails come from the verifier, which anchors a race by matching
its stored seven against every men's section of its page, so an eighth man is anchored by
the same match that proves the race. And before this stage writes anything it renders every
block in the file from board.json with no tails and requires the result to be byte-identical
to what is there now -- 223 of 223 -- because the only way to add a line to 819 races
without reformatting the other 926 is to prove the formatter reproduces the file first.

And the one number this unblocks. Every aggregate block says "most runners they finished in
any of these races", and for 74 of them it said seven when the team had finished eight to
twenty. Eight blocks were already right -- UIC's 14, Saint Joseph's 16 -- written when an
older stage still had the whole field in hand, and xc_apply's own gate was failing on all
eight because its formula could only count to seven. So this is not a cosmetic correction:
until it is made, the next sweep aborts. The gate here is the same idea as the one above --
every other field of every published block is recomputed from the file and must agree before
a single digit is touched, which is what proves the race set behind a block was reconstructed
correctly rather than guessed at. Only `maxfin` is then substituted, in place, by text.

`xc` is rewritten here and nowhere else, and only this one field of it. It carries the tiers
and five of its blocks are hand decisions, so no formula writes it -- but a count of finishers
is not a judgement, and leaving 33 of its blocks publishing a number the file now disproves
would be the worse half of that rule.

usage:
  python3 tools/tail_apply.py --dry
  python3 tools/tail_apply.py
"""
import json, re, statistics, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
DETAIL = REPO / 'assets' / 'detail.js'
DATA = REPO / 'assets' / 'data.js'
sys.path.insert(0, str(REPO / 'tools'))
import xc_apply                                                 # noqa: E402

CHAMP = xc_apply.CHAMP
SEASON_START = xc_apply.SEASON_START


def nscore(r):
    """The men who scored: seven at most, which is what every average is defined over."""
    return r.get('nfin') or len(r['runners'])


def nfinish(r):
    """The men who finished. Only maxfin asks this, and only `tail` can answer it."""
    return nscore(r) + len(r.get('tail') or [])


def recompute(races, A):
    """Every published aggregate, from the races on file, as the file itself computes them.

    This is xc_apply's formula with one difference that is the file's history rather than a
    choice: `xc` takes its short/maxfin flags from EVERY 2025 championship race, floored or
    not (172 of 175 blocks reproduce that way and 152 the other way), while xcInv and xc26
    take theirs from the same floored set they average (172 and 170 of them, exactly). Get
    that backwards and 20 blocks start disagreeing, which is the gate doing its job.
    """
    P = {'5K': A['proj5kxc'], '6K': A['proj6k'], '8K': A['proj8k'], '10K': A['proj10k']}
    EQ = {d: P['8K'] / P[d] for d in P}

    def floor(newer, champ=None):
        return [r for r in races
                if (r['date'] >= SEASON_START) == newer
                and (champ is None or (r['level'] in CHAMP) == champ)
                and r['dist'] in P and nscore(r) >= 5 and r.get('g1') is not None]

    def block(rs, flags, with_date=False):
        if not rs:
            # No race clears the floor, so there is nothing to average -- but a championship
            # field of three or four is still a measurement, and three published blocks say
            # so with nraces: 0 and a maxfin. Those keep their hand-written components.
            return {'nraces': 0, 'short': True,
                    'maxfin': max(nfinish(r) for r in flags)} if flags else None
        eqv = lambda k: [r[k] * EQ[r['dist']] for r in rs if r.get(k) is not None]
        sev = [r['v7'] * EQ[r['dist']] for r in rs if nscore(r) >= 7 and r.get('v7') is not None]
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
        if any(nscore(r) < 7 for r in flags):
            o['short'] = True
            o['maxfin'] = max(nfinish(r) for r in flags)
        return o

    champ25 = [r for r in races if r['date'] < SEASON_START and r['level'] in CHAMP]
    inv = floor(newer=False, champ=False)
    new = floor(newer=True)
    return {'xc': block(floor(newer=False, champ=True), champ25),
            'xcInv': block(inv, inv),
            'xc26': block(new, new, with_date=True)}


def main():
    dry = '--dry' in sys.argv[1:]
    board = json.load(open(WORK / 'board.json'))
    tails = json.load(open(WORK / 'tails.json'))['races']
    X = board['XCRACES']

    src = DETAIL.read_text()
    m = re.search(r'(const XCRACES = \{\n)(.*?)(\n\};\n)', src, re.S)
    if not m:
        raise SystemExit('XCRACES block not found in assets/detail.js')
    body = m.group(2)
    old = xc_apply.parse_blocks(body)

    # ---- the gate: render the file as it stands, and require the same bytes -----
    # A mismatch here is not a formatting nit. It means this stage's idea of a race is not
    # the file's, and a rewrite would quietly restyle races nobody asked it to touch.
    bad = []
    for name, rows in X.items():
        want = '  %s: [\n%s\n  ],' % (json.dumps(name),
                                      '\n'.join(xc_apply.race_js(r) for r in rows))
        have = old.get(name)
        if have is None:
            bad.append('%s: no block in the file' % name)
        elif have.lstrip('\n') != want:
            bad.append('%s: renders differently from the file' % name)
    print('round-trip gate: %d of %d blocks render byte-identical'
          % (len(X) - len(bad), len(X)))
    if bad:
        for b in bad[:10]:
            print('      ' + b)
        raise SystemExit('the race writer does not reproduce the file, so it may not '
                         'rewrite it. Nothing written.')

    # ---- splice ----------------------------------------------------------------
    hit, miss, men, deep = 0, [], 0, 0
    for name, rows in X.items():
        t = tails.get(name, {})
        touched = False
        for i, r in enumerate(rows):
            rec = t.get(str(i))
            if rec is None:
                miss.append((name, r['date'], 'no verified field'))
                continue
            # The index is positional, so it is checked rather than trusted: the race in
            # the file has to be the race the page was read for.
            stored = [round(float(x), 1) for x in r['runners']]
            if rec['date'] != r['date'] or rec['seven'] != stored:
                raise SystemExit('%s race %d: tails.json describes %s %s, the file holds '
                                 '%s %s. Re-run xc_verify.py --emit.'
                                 % (name, i, rec['date'], rec['seven'][:2],
                                    r['date'], stored[:2]))
            if not rec['tail']:
                continue
            r['tail'], r['tyears'] = rec['tail'], rec['tyears']
            hit += 1
            men += len(rec['tail'])
            deep = max(deep, 7 + len(rec['tail']))
            touched = True
        if not touched:
            continue
        block = '  %s: [\n%s\n  ],' % (json.dumps(name),
                                       '\n'.join(xc_apply.race_js(r) for r in rows))
        if body.count(old[name]) != 1:
            raise SystemExit('%s: block is not uniquely locatable' % name)
        body = body.replace(old[name], ('\n' if old[name].startswith('\n') else '') + block, 1)

    print('races given a tail: %d  (%d men behind a seven, deepest field %d)'
          % (hit, men, deep))
    if miss:
        print('races with no verified field, left alone: %d' % len(miss))
        for x in miss[:8]:
            print('      %-26s %s  %s' % (x[0][:26], x[1], x[2]))
    if not dry:
        DETAIL.write_text(src[:m.start(2)] + body + src[m.end(2):])
    maxfin_pass(board, dry)
    if dry:
        print('\n--dry: nothing written')


def maxfin_pass(board, dry):
    """Correct `maxfin` in assets/data.js wherever the tail proves it too low."""
    KEYS = ('slot', 'g1', 'v7', 'spread', 'eq', 'nraces', 'short', 'date')
    # Every row the file publishes, not just the board: the cut list, the no-track rows and the
    # no-program rows carry aggregates and render pages too, and ten of them (Iona, Duke, Jacksonville
    # State and seven more) were left holding the capped 7 when this pass read SCHOOLS alone.
    rows = [r for k in ('SCHOOLS', 'REMOVED', 'NO_TRACK', 'NO_PROGRAM') for r in board[k]]
    want = {}
    for row in rows:
        want[row['name']] = recompute(board['XCRACES'].get(row['name'], []), board['ATHLETE'])

    # ---- the gate: every other field of every block that carries a maxfin --------
    checked, bad = 0, []
    for row in rows:
        for key, got in want[row['name']].items():
            st = row.get(key)
            if not isinstance(st, dict) or st.get('maxfin') is None:
                continue          # no maxfin to correct, so nothing is claimed about it
            checked += 1
            if got is None:
                bad.append('%s %s: published, and no race on file produces it' % (row['name'], key))
                continue
            # Three blocks average nothing (nraces: 0) because no race of theirs clears the
            # five-finisher floor, and their components are hand-written rather than derived.
            # There is nothing to reproduce there, so the gate holds them to the two fields
            # that are: the race set is still named by short and nraces.
            keys = KEYS if 'slot' in got else ('nraces', 'short')
            d = [k for k in keys if not xc_apply.same(st.get(k), got.get(k))]
            if d:
                bad.append('%s %s: %s' % (row['name'], key, ', '.join(
                    '%s file %s formula %s' % (k, st.get(k), got.get(k)) for k in d)))
    print('maxfin gate: %d of %d blocks reproduce field for field (maxfin aside)'
          % (checked - len(bad), checked))
    if bad:
        for b in bad[:10]:
            print('      ' + b)
        raise SystemExit('a block does not reproduce, so the race set behind it is not the '
                         'one this stage reconstructed. data.js untouched.')

    # ---- substitute the one number ---------------------------------------------
    dsrc = DATA.read_text()
    parts = re.split(r'(\n  \{ name: ")', dsrc)
    out, moved, held = [parts[0]], [], 0
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        name = body.split('"', 1)[0]
        for key, got in want.get(name, {}).items():
            st = next((r.get(key) for r in rows if r['name'] == name), None)
            if not isinstance(st, dict) or st.get('maxfin') is None or got is None:
                continue
            if got['maxfin'] == st['maxfin']:
                held += 1
                continue
            bm = re.search(r'\n\s*%s: \{[^\n]*\},' % key, body)
            if not bm:
                raise SystemExit('%s %s: block not found in data.js' % (name, key))
            line, n = re.subn(r'maxfin: \d+', 'maxfin: %d' % got['maxfin'], bm.group(0))
            if n != 1:
                raise SystemExit('%s %s: %d maxfin values on the line' % (name, key, n))
            body = body[:bm.start()] + line + body[bm.end():]
            moved.append('%-24s %-5s %2d -> %2d' % (name[:24], key, st['maxfin'], got['maxfin']))
        out.append(head)
        out.append(body)
    print('maxfin corrected: %d blocks  (%d already right)' % (len(moved), held))
    for x in moved[:10]:
        print('      ' + x)
    if len(moved) > 10:
        print('      ... and %d more' % (len(moved) - 10))
    if not dry:
        DATA.write_text(''.join(out))


if __name__ == '__main__':
    main()
