#!/usr/bin/env python3
"""Driving miles for the seven North Carolina colleges beyond the ring, on the board's router.

north-carolina.html names seven schools that sponsor men's cross country and sit outside the
300-mile ring, and it claims in prose that their figures are comparable to the board's `Mi`
column because both come from the same router and the same origin. That claim has to survive
`tools/remeasure_mi.py`, which re-measured all 243 board rows to one decimal -- so these seven
are measured the same way here rather than left as the whole numbers of an earlier pass.

Coordinates come from IPEDS HD rather than a geocoder: these are the same coordinates the
federal file gives for every other row, so nothing about the comparison depends on a name
lookup. Unit IDs are explicit and each was confirmed on institution name AND city.

  in:   tools/.work/board.json   (node tools/dump_board.js)  -- for the origin
        tools/.work/HD2023.csv
  out:  tools/.work/nc_seven.json, and the table rows to paste, printed
"""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remeasure_mi import drive_mi  # noqa: E402  same router, same retry policy

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.work')

# The ring is measured from the Greenville SC centre, which is this board's origin.
ORIGIN_METRO = 'greenville'

SEVEN = {
    'UNC Wilmington': 199218,        # University of North Carolina Wilmington, Wilmington NC
    'Barton': 197911,                # Barton College, Wilson NC
    'Mount Olive': 199069,           # University of Mount Olive, Mount Olive NC
    'NC Wesleyan': 199209,           # North Carolina Wesleyan University, Rocky Mount NC
    'East Carolina': 198464,         # East Carolina University, Greenville NC
    'Chowan': 198303,                # Chowan University, Murfreesboro NC
    'Elizabeth City State': 198507,  # Elizabeth City State University, Elizabeth City NC
}


def main():
    board = json.load(open(os.path.join(WORK, 'board.json')))
    origin = board['METROS'][ORIGIN_METRO]['center']

    hd = {}
    with open(os.path.join(WORK, 'HD2023.csv'), encoding='latin-1') as fh:
        for rec in csv.DictReader(fh):
            uid = next(v for k, v in rec.items() if k.endswith('UNITID'))
            if int(uid) in SEVEN.values():
                hd[int(uid)] = rec

    out = {}
    for name, uid in SEVEN.items():
        rec = hd[uid]
        at = (float(rec['LATITUDE']), float(rec['LONGITUD']))
        d = drive_mi(origin, at)
        out[name] = {'mi': round(d, 1) if d else None, 'ipeds': uid,
                     'city': rec['CITY'].strip(), 'lat': at[0], 'lon': at[1]}
        print('%-22s %-18s %s' % (name, rec['CITY'].strip(),
                                  round(d, 1) if d else 'OSRM FAILED'))
    json.dump(out, open(os.path.join(WORK, 'nc_seven.json'), 'w'), indent=1, sort_keys=True)

    print('\nin ring order:')
    for name, v in sorted(out.items(), key=lambda kv: kv[1]['mi'] or 9e9):
        print('   %-22s %s' % (name, v['mi']))


if __name__ == '__main__':
    main()
