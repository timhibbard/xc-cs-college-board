#!/usr/bin/env python3
"""Projections for the distances college cross country races that are not 5K, 6K, 8K or 10K.

82 races on file are run at twelve other distances -- 4M, 5.2M, 7K, 6.2K, 7.2K, 7.7K, 3.73M,
5.8K, 4K, 3.6K, 4.34K, 2M -- and every one of them carried a null slot, gap and v7, on the
argument that inventing a factor puts a plausible number where an absence belongs. That
argument is right about inventing one and wrong about the absence: the file has enough
evidence to measure these, and a null is not neutral. It drops 82 races out of every
comparison the board makes, including 37 at 4M, which is a distance the Northeast races all
autumn.

The rule is not new either. ATHLETE.proj6k is 1140 and its own comment says it was
"interpolated between the 5K and the 8K, not measured" -- so the board already has a rule
for a distance it declines to measure, and this extends that rule rather than adding one:

  1. INTERPOLATE between the two published anchors that bracket the distance, linearly in
     metres. This is what produced 1140 at 6K.
  2. MEASURE the same distance independently, by the comparison the published 5K->8K and
     8K->10K factors use: one team, one season, its own nth man at that distance and at 8K.
     A ratio, never a Riegel exponent -- solving for an exponent puts ln(7700/8000) = 0.038
     under a division and reports 0.61 and 2.58 from the same sixteen pairs.
  3. TAKE THE SLOWER of the two, because this board's rule (methodology.html #projections)
     is that a projection may be conservative but may not be optimistic, and a slower
     projection makes his gap to a team's #1 larger rather than smaller.

A distance shorter than 5K gets nothing, and that is the honest answer rather than a timid
one: 5K is the shortest mark this athlete has actually run, so there is no pair of anchors
to interpolate between and the only route left is extrapolating below his own evidence.
That leaves 13 races at 2M, 3.6K, 4K and 4.34K null, and each one is a short early-season
race rather than the kind of result a tier should turn on.

The gate is 6K itself, with 6K held out of its own anchors: draw the line from the 5K to the
8K alone, read it at 6,000 metres, and it must land within two seconds of the published 1140
and on the conservative side of it. It gives 1138.7, and 1140 is the clean 19:00 label 1.3
seconds slower -- so the rule reproduces the one anchor that was already built with it, and
the published value is the more conservative of the two. Leaving 6K in the anchor set makes
the gate pass at exactly 0.0s and prove nothing, which is what the first draft of it did.

  python3 tools/offdist.py            derive and report, write nothing
  python3 tools/offdist.py --apply    rewrite ATHLETE.projOff in assets/data.js and
                                      backfill slot/g1/v7 on every off-distance race
"""
import json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '.work')
DATA = os.path.join(os.path.dirname(HERE), 'assets', 'data.js')
DETAIL = os.path.join(os.path.dirname(HERE), 'assets', 'detail.js')

# Metres for every distance string the file holds. A mile is 1609.344 m exactly; these are
# the nominal race distances, not course measurements, which is the same basis the 8K and
# 10K anchors use. 3.73M is 6,002.9 m -- a 6K written in miles -- and it is left as its own
# string rather than renamed, because the page it came from says 3.73 Mile and xc_verify
# joins the file back to that page.
METRES = {
    '2M': 3218.7, '3.6K': 3600, '4K': 4000, '4.34K': 4340, '5K': 5000, '5.8K': 5800,
    '3.73M': 6002.9, '6K': 6000, '6.2K': 6200, '4M': 6437.4, '7K': 7000, '7.2K': 7200,
    '7.7K': 7700, '8K': 8000, '5.2M': 8368.6, '10K': 10000,
}
STD = ('5K', '6K', '8K', '10K')
MEAS_ANCHOR = '8K'          # where the slot pairs are: every off-distance shares a season with it

# There is deliberately no minimum sample size on the measurement, and the reason is worth
# stating because the opposite looks more careful. Taking the slower of the two routes means
# a thin measurement can only ever push a projection further from flattery: if it is wrong it
# makes his gap to a team's #1 larger, which this board permits, and the interpolation is
# still there underneath as the floor. A threshold would only ever discard that -- an earlier
# draft set it at 30 pairs and the single effect was to throw away 25 seconds of conservatism
# at 7.7K. The pair and team-season counts are published instead, so a thin factor is visible
# as thin rather than silently dropped.


def season_of(date):
    """August starts the season the autumn is named for, as everywhere else in this chain."""
    return int(date[:4]) - (1 if date[5:7] < '08' else 0)


def anchors(ath):
    return {'5K': ath['proj5kxc'], '6K': ath['proj6k'], '8K': ath['proj8k'], '10K': ath['proj10k']}


def interpolate(m, anc, using=STD):
    """Linear in metres between the two published anchors that bracket m. None outside them.

    `using` exists for the gate: testing the rule at 6,000 metres against the published 6K
    has to leave the 6K anchor out of the anchors, or it brackets on the very number it is
    being checked against and reproduces it by construction.
    """
    pts = sorted((METRES[d], anc[d]) for d in using)
    for (m0, t0), (m1, t1) in zip(pts, pts[1:]):
        if m0 <= m <= m1:
            return t0 + (t1 - t0) * (m - m0) / (m1 - m0)
    return None


def measure(races_by_school):
    """{dist: (ratio, pairs, team_seasons)} -- the 8K/dist ratio at matched slots.

    One team, one season, its nth man at both distances. The ratio is 8K time over
    off-distance time, so his 8K projection divided by it is his projection here.
    """
    rows = {}
    for school, races in races_by_school.items():
        by = {}
        for r in races:
            by.setdefault(season_of(r['date']), []).append(r)
        for sn, rs in by.items():
            refs = [r for r in rs if r['dist'] == MEAS_ANCHOR]
            for o in rs:
                if o['dist'] in STD:
                    continue
                for s in refs:
                    n = min(len(o['runners']), len(s['runners']))
                    for i in range(n):
                        rows.setdefault(o['dist'], []).append(
                            (s['runners'][i] / o['runners'][i], school, sn))
    out = {}
    for d, vals in rows.items():
        teams = {(s, sn) for _, s, sn in vals}
        out[d] = (statistics.median(v for v, _, _ in vals), len(vals), len(teams))
    return out


def derive(board):
    anc = anchors(board['ATHLETE'])
    meas = measure(board['XCRACES'])
    offs = sorted({r['dist'] for rs in board['XCRACES'].values() for r in rs} - set(STD),
                  key=lambda d: METRES[d])
    table, report = {}, []
    for d in offs:
        m = METRES[d]
        interp = interpolate(m, anc)
        ratio, pairs, teams = meas.get(d, (None, 0, 0))
        measured = anc[MEAS_ANCHOR] / ratio if ratio else None
        if interp is None:
            proj, why = None, 'shorter than 5K - nothing to interpolate between'
        elif measured is None:
            proj, why = round(interp), 'interpolated - no team raced this and an 8K in one season'
        else:
            proj = round(max(interp, measured))
            why = 'measured' if measured >= interp else 'interpolated'
            why += ' - the slower of %d and %d' % (round(interp), round(measured))
        if proj is not None:
            table[d] = proj
        report.append({'dist': d, 'm': m, 'interp': interp, 'ratio': ratio,
                       'pairs': pairs, 'teams': teams, 'measured': measured,
                       'proj': proj, 'why': why})
    return anc, table, report


def main():
    board = json.load(open(os.path.join(WORK, 'board.json')))
    anc, table, report = derive(board)

    # The gate: the rule has to reproduce the one anchor that was already built with it,
    # with that anchor held out so it is not reproducing itself.
    six = interpolate(6000, anc, using=('5K', '8K', '10K'))
    gap = anc['6K'] - six
    print('gate: the 5K-8K line at 6,000 m gives %.1f against the published %d -- %+.1fs, %s'
          % (six, anc['6K'], gap, 'conservative' if gap >= 0 else 'OPTIMISTIC'))
    if abs(gap) > 2 or gap < 0:
        sys.exit('  the rule no longer reproduces proj6k; the anchors have moved')

    counts = {}
    for rs in board['XCRACES'].values():
        for r in rs:
            counts[r['dist']] = counts.get(r['dist'], 0) + 1

    print('\n%-7s %7s %6s %7s %6s %6s %7s %7s  %s'
          % ('dist', 'metres', 'races', 'interp', 'ratio', 'pairs', 'teams', 'proj', 'why'))
    covered = nulled = 0
    for r in report:
        n = counts[r['dist']]
        covered += n if r['proj'] else 0
        nulled += 0 if r['proj'] else n
        print('%-7s %7.1f %6d %7s %6s %6d %7d %7s  %s'
              % (r['dist'], r['m'], n,
                 '%.1f' % r['interp'] if r['interp'] else '-',
                 '%.4f' % r['ratio'] if r['ratio'] else '-',
                 r['pairs'], r['teams'], r['proj'] or '-', r['why']))
    print('\n%d off-distance races get a projection, %d stay null' % (covered, nulled))
    print('projOff: %s' % json.dumps(table))

    if '--apply' not in sys.argv:
        print('\nno --apply: nothing written')
        return

    # ATHLETE.projOff, written as one line so the comment above it stays the explanation.
    src = open(DATA, encoding='utf-8').read()
    block = '  projOff: {\n' + ''.join(
        "    '%s': %d,\n" % (d, t) for d, t in sorted(table.items(), key=lambda kv: METRES[kv[0]])
    ) + '  },\n'
    if 'projOff:' in src:
        src, n = re.subn(r'  projOff: \{.*?\n  \},\n', block, src, flags=re.S)
    else:
        # After proj5kxc, not before it: the comment above that line belongs to it, and
        # inserting ahead of the line separated the two.
        src, n = re.subn(r"(  proj5kxc: 940, proj5kxcLabel: '15:40',\n)",
                         lambda m: m.group(1) + OFFDOC + block, src)
    if n != 1:
        sys.exit('  ATHLETE in assets/data.js does not look as expected (%d matches)' % n)
    open(DATA, 'w', encoding='utf-8').write(src)
    print('\nassets/data.js  ATHLETE.projOff rewritten (%d distances)' % len(table))

    # Backfill the races themselves. Each race in XCRACES is one brace-delimited block
    # written over five or six lines, with slot/g1/v7 together on the second, so this walks
    # the lines and rewrites that one line in place. It reads the runners out of the block
    # it is editing rather than out of board.json, which means the three numbers it writes
    # are derived from the times sitting beside them -- the same join xc_verify makes, and
    # one that cannot put a school's figures on another school's race.
    lines = open(DETAIL, encoding='utf-8').read().split('\n')
    done, left = 0, 0
    for i, ln in enumerate(lines):
        m = re.match(r'\s*\{ meet: ".*?", date: "(\d{4}-\d\d-\d\d)", dist: "([^"]+)",', ln)
        if not m:
            continue
        date, dist = m.groups()
        if dist in STD:
            continue
        if dist not in table:
            left += 1
            continue
        rm = next((re.search(r'runners: \[([\d., ]+)\]', lines[j])
                   for j in range(i, min(i + 7, len(lines)))
                   if 'runners: [' in lines[j]), None)
        if not rm:
            sys.exit('  %s %s: no runners array under the block at line %d' % (date, dist, i + 1))
        run = [float(x) for x in rm.group(1).split(',')]
        proj = table[dist]
        # The stored figures are measured against the corrected time, not the raw one, which
        # is how xc_verify recomputes them: it adds the block's own corr back before
        # comparing. Every off-distance race on file today carries corr 0, so this changes
        # nothing now and is here so that applying a course correction to one later does not
        # quietly leave its slot and gap measured against the uncorrected time.
        cm = re.search(r'corr: (-?[\d.]+)', lines[i + 1])
        corr = float(cm.group(1)) if cm else 0.0
        adj = [t + corr for t in run]
        g1 = round(proj - adj[0], 1)
        v7 = round(proj - adj[6], 1) if len(adj) >= 7 else None
        slot = sum(1 for t in adj if t < proj) + 1
        new, n = re.subn(r'slot: [^,]+, g1: [^,]+, v7: [^,]+,',
                         'slot: %d, g1: %s, v7: %s,' % (slot, g1, 'null' if v7 is None else v7),
                         lines[i + 1])
        if n != 1:
            sys.exit('  %s %s: slot/g1/v7 not on the line under the block at %d' % (date, dist, i + 1))
        lines[i + 1], done = new, done + 1
        # A team that finished fewer than seven carries a fifth projected field on the next
        # line -- its gap to the last man it did finish, which is the only 7th-man-shaped
        # number such a race can offer. 20 of the 69 are in that position, and leaving it
        # null while filling the other three is what xc_verify caught.
        if len(run) < 7:
            vlast = round(proj - adj[-1], 1)
            nxt, n = re.subn(r'vlast: [^,]+,', 'vlast: %s,' % vlast, lines[i + 2])
            if n != 1:
                sys.exit('  %s %s: %d runners but no vlast line at %d'
                         % (date, dist, len(run), i + 3))
            lines[i + 2] = nxt
    open(DETAIL, 'w', encoding='utf-8').write('\n'.join(lines))
    print('assets/detail.js  %d off-distance races backfilled, %d left null (under 5K)'
          % (done, left))


OFFDOC = """  /* Projections at the distances that are not 5K, 6K, 8K or 10K -- 82 races on file, 37
     of them at 4M. Each one is the slower of two routes: a linear interpolation in metres
     between the two anchors above that bracket it, which is the rule that produced
     proj6k; and his 8K projection divided by the measured ratio of a team's own nth man
     at 8K to its nth man here, in the same season, which is the comparison the published
     5K->8K and 8K->10K factors are measured with. The slower wins because a projection
     on this board may be conservative and may not be optimistic. Nothing below 5K is
     here: his 5K is the shortest mark he has run, so there is no pair of anchors to
     interpolate between. Derived by tools/offdist.py, re-derived by render-check.
     See methodology.html #offdist. */
"""

if __name__ == '__main__':
    main()
