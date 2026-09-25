#!/usr/bin/env python3
"""Stage 1 of the campus-setting column (#13): the two fields that need no fetching.

  locale       the federal city/suburb/town/rural class, IPEDS HD `LOCALE`, joined on the
               unit ID already stored in each row's cost block. Federal record rather than
               an impression, and it is the only one of these fields that is somebody
               else's judgement rather than arithmetic.
  townMi       straight-line miles from the campus coordinate to the centre of the town the
               campus is actually in, with that town's land area beside it. This replaces an
               earlier `downtownMi` measured to the METRO centre, which was a mistake: that
               number is the board's `mi` column again, computed a second way, and it says
               nothing about whether you can walk to anything. Three miles out of a
               two-square-mile town is out of town; three miles from the middle of Chicago
               is Lincoln Park. The area is what tells those apart, so both are stored.

               Census place centroids are the geographic middle rather than the historic
               downtown, so this is "how central in its own town", not "how near the CBD" --
               the errands axis answers the second question far better than any radius can.

The HD file also carries the institution's street address, which is the input the Walk
Score pass needs -- that site's lat/lng URL form is broken (it answered MIT's own
coordinate with a village in Maharashtra and "Car-Dependent"), so the address slug is the
only way to ask it a question and get the right place back.

  in:   tools/.work/board.json   (node tools/dump_board.js)
        tools/.work/HD2023.csv   (https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip)
        tools/.work/2023_Gaz_place_national.txt
            (https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/
             2023_Gaz_place_national.zip)
  out:  tools/.work/setting1.json
"""
import csv, json, math, os, re, sys

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.work')

# IPEDS LOCALE. The twelve-way split is the point: "Town: Remote" and "Suburb: Large" are
# both "not a city" and they are not the same place to spend four years without a car.
LOCALE = {
    11: 'City: Large',    12: 'City: Midsize',    13: 'City: Small',
    21: 'Suburb: Large',  22: 'Suburb: Midsize',  23: 'Suburb: Small',
    31: 'Town: Fringe',   32: 'Town: Distant',    33: 'Town: Remote',
    41: 'Rural: Fringe',  42: 'Rural: Distant',   43: 'Rural: Remote',
}


# Twelve rows carry no `cost.ipeds`: the ones with no cost block at all (no men's program,
# so no cost was ever read) plus a few whose cost came from somewhere other than the
# federal file. Every one below was confirmed by institution name AND city in HD2023 --
# explicit only, the same rule slugmap.json follows, because a name like "Georgia State"
# matches a dozen technical colleges and "St. John's" matches nine.
UNITID = {
    'UAB': 100663,                 # University of Alabama at Birmingham, Birmingham AL
    'Georgia Southern': 139931,    # Statesboro GA
    'Georgia State': 139940,       # Atlanta GA -- not 244437, its Perimeter College
    'Northwestern': 147767,        # Evanston IL
    'St. John’s': 195809,          # St. John's University-New York, Queens NY
    'Trinity Christian': 149505,   # Palos Heights IL
    'Montclair State': 185590,     # Montclair NJ
    'NYIT': 194091,                # New York Institute of Technology, Old Westbury NY
    'William Paterson': 187444,    # Wayne NJ
    'North Georgia': 482680,       # University of North Georgia, Dahlonega GA
    'St. Andrews': 199698,         # St. Andrews University, Laurinburg NC
    'Saint Augustine’s': 199582,   # Raleigh NC
}


# Gazetteer NAME carries the legal type as a trailing word: "Boone town", "Chicago city",
# "Lookout Mountain city". Stripped so the name can be matched against the IPEDS city field,
# which carries none. Exact match only, on name AND state -- the same rule slugmap.json
# follows, because fuzzy matching on place names is how you confidently put a campus in the
# wrong Springfield.
TYPES = ('city', 'town', 'village', 'borough', 'CDP', 'municipality', 'township',
         'comunidad', 'zona urbana', 'consolidated government', 'metro government',
         'metropolitan government', 'urban county', 'city and borough', 'unified government')


def city_key(usps, name):
    """For the IPEDS city field, which carries no legal type. Nothing is stripped here: half a
    dozen of these cities are named "... City" outright -- Jersey City, Johnson City, Garden
    City, Jefferson City -- and running the gazetteer's suffix stripper over them turned
    Jersey City into Jersey and lost every one of them."""
    return (usps.strip().upper(), name.strip().lower())


def place_key(usps, name):
    n = re.sub(r'\s*\((balance|part)\)$', '', name.strip())
    for t in sorted(TYPES, key=len, reverse=True):
        if n.lower().endswith(' ' + t.lower()):
            n = n[:-(len(t) + 1)].rstrip()
            break
    return city_key(usps, n)


# Where the IPEDS city is not the name of any place or subdivision. Every one checked by
# hand against the campus coordinate, and every one belongs to a class rather than being a
# one-off: a New York neighbourhood inside a borough, a Massachusetts village inside a town,
# a Pennsylvania post-office name inside a township, or a Georgia city that merged with its
# county and now files under the joint name.
CITY_BY_HAND = {
    ('NY', 'jamaica'): 'Queens',            # neighbourhood of Queens
    ('NY', 'riverdale'): 'Bronx',           # neighbourhood of the Bronx
    ('NY', 'throggs neck'): 'Bronx',        # ditto
    ('MA', 'chestnut hill'): 'Newton',      # village split across Newton and Brookline
    ('PA', 'saint davids'): 'Radnor',       # post office inside Radnor township
    ('NJ', 'south orange'): 'South Orange Village',
    ('GA', 'augusta'): 'Augusta-Richmond County',   # consolidated 1996
    ('GA', 'athens'): 'Athens-Clarke County',       # consolidated 1991
    ('GA', 'macon'): 'Macon-Bibb County',           # consolidated 2014
    ('GA', 'mount berry'): 'Rome',          # unincorporated; Berry College's own post office
}


def load_gaz(path, places=None, fill_only=False):
    """Keyed on (state, lowercased name), the legal type stripped. Where a state has two
    entries of the same name -- a city and a CDP of the same name happens -- the larger by
    land area wins, because the CDP duplicate is usually a fragment of the same settlement.

    Called twice: the place file first, then the county-subdivision file to fill what the
    place file has no row for. That second file is not optional. New England towns and
    mid-Atlantic townships are minor civil divisions and appear in NO place file, so on
    places alone thirty rows had no town at all -- Weston MA, Wayne NJ, Haverford PA,
    Amherst NY -- and so did every NYC campus, because a borough is not a place either."""
    places = {} if places is None else places
    with open(path, encoding='latin-1') as fh:
        for rec in csv.DictReader(fh, delimiter='\t'):
            rec = {k.strip(): (v.strip() if isinstance(v, str) else v)
                   for k, v in rec.items() if k}
            try:
                lat, lon = float(rec['INTPTLAT']), float(rec['INTPTLONG'])
                sqmi = float(rec['ALAND_SQMI'])
            except (KeyError, ValueError, TypeError):
                continue
            key = place_key(rec['USPS'], rec['NAME'])
            if fill_only and key in places:
                # The subdivision file FILLS, it does not override. Both files carry a "Boone"
                # in NC -- the town and the township around it -- and the township is larger,
                # so an area comparison across the two files would quietly move the centre of
                # every such row out of the town and into the countryside around it.
                continue
            if key not in places or sqmi > places[key][2]:
                places[key] = (lat, lon, sqmi, rec['NAME'])
    return places


def find_town(places, state, city):
    """Three ordered attempts, none of them fuzzy: the city as written, then the city with a
    trailing legal type removed (IPEDS writes "Moon Township" where the gazetteer writes
    "Moon township", and this order is what keeps Jersey City from becoming Jersey), then
    the hand-checked map."""
    for key in (city_key(state, city), place_key(state, city)):
        if key in places:
            return places[key]
    by_hand = CITY_BY_HAND.get(city_key(state, city))
    return places.get(city_key(state, by_hand)) if by_hand else None


def haversine_mi(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 3958.7613 * math.asin(math.sqrt(h))


def main():
    board = json.load(open(os.path.join(WORK, 'board.json')))
    metros = board['METROS']
    rows = [r for key in ('SCHOOLS', 'REMOVED', 'NO_TRACK', 'NO_PROGRAM')
            for r in board[key]]

    hd_path = os.path.join(WORK, 'HD2023.csv')
    if not os.path.exists(hd_path):
        sys.exit('missing %s -- unzip HD2023.zip into .work/ first' % hd_path)
    hd = {}
    with open(hd_path, encoding='latin-1') as fh:
        for rec in csv.DictReader(fh):
            # The HD header ships with a UTF-8 BOM and the file is read latin-1 (a handful of
            # institution names are not UTF-8), so the first column arrives as 'ï»¿UNITID'.
            uid = next(v for k, v in rec.items() if k.endswith('UNITID'))
            hd[int(uid)] = rec

    places = None
    for fn in ('2023_Gaz_place_national.txt', '2023_Gaz_cousubs_national.txt'):
        path = os.path.join(WORK, fn)
        if not os.path.exists(path):
            sys.exit('missing %s -- unzip its Gazetteer zip into .work/ first' % path)
        places = load_gaz(path, places, fill_only=places is not None)

    out, no_id, no_match, no_locale, no_town = {}, [], [], [], []
    for r in rows:
        uid = (r.get('cost') or {}).get('ipeds') or UNITID.get(r['name'])
        rec = hd.get(uid) if uid else None
        if not uid:
            no_id.append(r['name'])
        elif rec is None:
            no_match.append('%s (%s)' % (r['name'], uid))

        code = int(rec['LOCALE']) if rec and rec['LOCALE'].strip().lstrip('-').isdigit() else None
        if rec is not None and code not in LOCALE:
            no_locale.append(r['name'])

        entry = {
            # Only the board rows have a page, so only they have a slug.
            'slug': r.get('slug'),
            'metro': r['metro'],
            'lat': r['lat'], 'lon': r['lon'],
            'locale': LOCALE.get(code),
            'localeCode': code,
        }
        town = find_town(places, rec['STABBR'], rec['CITY']) if rec is not None else None
        if town:
            entry['townMi'] = round(haversine_mi((r['lat'], r['lon']), (town[0], town[1])), 1)
            entry['townSqMi'] = round(town[2], 1)
            entry['townName'] = town[3]
        else:
            entry['townMi'] = entry['townSqMi'] = entry['townName'] = None
            if rec is not None:
                no_town.append('%s (%s %s)' % (r['name'], rec['CITY'].strip(), rec['STABBR']))
        if rec is not None:
            # Kept for the Walk Score pass, and to check it answered about the right place.
            entry['addr'] = {'street': rec['ADDR'].strip(), 'city': rec['CITY'].strip(),
                             'state': rec['STABBR'].strip(), 'zip': rec['ZIP'].strip()[:5]}
            entry['hdName'] = rec['INSTNM'].strip()
        out[r['name']] = entry

    json.dump(out, open(os.path.join(WORK, 'setting1.json'), 'w'), indent=1, sort_keys=True)

    have = [e for e in out.values() if e['locale']]
    print('rows %d   locale %d   address %d   townMi %d'
          % (len(out), len(have), sum('addr' in e for e in out.values()),
             sum(e['townMi'] is not None for e in out.values())))
    for label, lst in (('no ipeds id', no_id), ('id not in HD2023', no_match),
                       ('no LOCALE in HD', no_locale),
                       ('city not a Census place', no_town)):
        if lst:
            print('  %s (%d): %s' % (label, len(lst), ', '.join(sorted(lst))))
    tally = {}
    for e in have:
        tally[e['locale']] = tally.get(e['locale'], 0) + 1
    for k in LOCALE.values():
        if k in tally:
            print('  %-15s %3d' % (k, tally[k]))


if __name__ == '__main__':
    main()
