#!/usr/bin/env python3
"""Stage 2 of the campus-setting column (#13): Walk, Transit and Bike Score per row.

Walk Score has no key on this machine, and its public page is readable through the
r.jina.ai text proxy. Two traps, both of which this script exists to avoid:

1. **The lat/lng URL form is wrong, not merely imprecise.** Asked about MIT's own
   coordinate (`/score/lat=42.3601/lng=-71.0942`) it answered "Chandgavhan MH ...
   Car-Dependent" -- a village in Maharashtra. So the address-slug URL is the only usable
   form, and the address comes from IPEDS HD (`setting_locale.py`).

2. **A wrong address still returns a page**, with somebody else's scores on it. So nothing
   is stored unless the coordinate in the page's own map tiles lands within NEAR of the
   campus coordinate this board already holds, and of the slugs that pass, the closest one
   wins rather than the first. A row where none pass is recorded as a miss with its reason
   and how far off the best attempt was, never as a number.

   The obvious version of that test -- does the page name the town the federal address
   names -- is wrong in both directions, and it threw away ten good rows on the first pass:
   Walk Score calls Manhattan College's address Bronx, York College's Queens, Daemen's
   Buffalo rather than Amherst, and Harvard's "this location".

Transit Score exists only where the city publishes a feed Walk Score has ingested, so its
absence is "no feed", not zero, and it is stored as None rather than 0.

  in:   tools/.work/setting1.json   (python3 tools/setting_locale.py)
  out:  tools/.work/walkscore.json  -- merged, so a re-run only fetches what is missing
  args: [n] rows this pass, or a school name to do one row
"""
import json, math, os, re, subprocess, sys, time, unicodedata

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.work')
OUT = os.path.join(WORK, 'walkscore.json')
PACE = 5.0          # seconds between fetches; this channel is shared and never parallel
# How far the page's own coordinate may sit from the campus coordinate before its score is
# about somewhere else. This number is the whole accuracy of the column, and loose is worse
# than strict: at three miles the pass accepted road-level answers and two runs over the
# same 243 rows disagreed on 25 of them, because "Germantown Ave, Philadelphia" scores the
# length of the avenue at 85 while Chestnut Hill's own corner of it scores 4. Half a mile is
# about a ten minute walk, which is the scale the score itself is built on.
NEAR = 0.5
APPROX = 1.5          # accepted, but stored as a nearby reading with its distance shown
CLOSE_ENOUGH = 0.15   # stop trying further slugs; this one is on the campus


def rank(level, off):
    """Which of two accepted answers is the better one. Distance alone is not the test: a
    town page's coordinate is the town centre, and for a small town that can sit closer to
    the stored campus point than the campus's own street address does, so distance alone
    chose the town of Whiting over Calumet College's campus and read 84 instead of 31. An
    address always beats a nearby street, which always beats a whole town."""
    return ({'address': 0, 'approx': 1, 'town': 2}[level], off)


SUFFIX = re.compile(r'\b(ave|avenue|st|street|rd|road|blvd|dr|drive|ln|way|pkwy|hwy)\b\.?', re.I)


def slug(*parts):
    """Walk Score's own URL shape: /score/77-massachusetts-ave-cambridge-ma."""
    s = ' '.join(p for p in parts if p)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = s.replace('&', ' and ').replace('.', '').replace(',', ' ')
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')


ROAD = [(r'\bhwy\b', 'highway'), (r'\brte?\b', 'route'), (r'\bus\b', 'us highway'),
        (r'\b(\d+)([NSEW])\b', r'\1')]


# The federal address is the institution's administrative one, which for a school on two
# campuses is whichever one holds the president. This board's coordinate is the campus the
# team is on, so for these rows the two disagree by more than a walk: DePaul's HD address is
# the Loop, 3.4 miles from the Lincoln Park campus where its athletics are. Where the gap is
# bigger than NEAR the row misses rather than quietly scoring the wrong campus, and the
# answer is an address by hand -- with the reason, because a bare override is unreviewable.
#
# Both of these were found by the coordinate test rather than guessed at: each row's federal
# address answered about a real place that is not the campus this board's coordinate is on.
ADDR_BY_HAND = {
    # HD gives 1 E Jackson Blvd, the Loop campus that holds the president. The board's
    # coordinate is Lincoln Park, 3.6 miles north, which is where the athletics and the
    # residence halls are -- so the Loop's errands are not this row's errands. The Lincoln
    # Park Student Center, on the coordinate the board already holds.
    'DePaul': {'street': '2250 N Sheffield Ave', 'city': 'Chicago', 'zip': '60614'},
    # HD gives 720 Northern Blvd, Brookville: LIU reports as one institution under the unit
    # ID of the Post campus, twenty-two miles out on Long Island. This row is the Brooklyn
    # campus -- city "Brooklyn NY", and its coordinate is on University Plaza to three
    # decimals. See the note in the PR: which campus the TEAM trains on is a separate
    # question from which one this row describes, and it is not settled here.
    'LIU': {'street': '1 University Plaza', 'city': 'Brooklyn', 'zip': '11201'},
    # Two rows on this board share unit ID 195544 and they are two real programs with two
    # coaches: St. Joseph's University has a Brooklyn campus and a Long Island one, and the
    # federal record gives the Brooklyn address for both. This is the Long Island one, in
    # Patchogue -- 55 miles out, which is what its Mi said all along even while its
    # coordinate was pointing at Clinton Hill.
    'St. Joseph\'s Long Island': {'street': '155 W Roe Blvd', 'city': 'Patchogue',
                                  'zip': '11772'},
}


def variants(addr, coords):
    """Slugs to try, best first. A rural highway address is the case that needs them:
    Pfeiffer's federal address, 48380 US Hwy 52N, geocodes to nothing on that site, while
    the same road without the house number and spelled out answers with a Walk Score of 7.
    The last resort asks OpenStreetMap what the campus coordinate is on the street of."""
    street = addr['street']
    yield slug(street, addr['city'], addr['state'])
    road = re.sub(r'^\d+\s+', '', street)
    for pat, rep in ROAD:
        road = re.sub(pat, rep, road, flags=re.I)
    road = re.sub(r'\bus highway highway\b', 'us highway', road, flags=re.I)
    alt = slug(road, addr['city'], addr['state'])
    if alt != slug(street, addr['city'], addr['state']):
        yield alt
    osm = nominatim_road(coords)
    if osm:
        yield slug(osm, addr['city'], addr['state'])
    # Last resort, and a coarser answer than the three above: the town's own page. Erskine
    # needs it -- that site's geocoder does not know any street in Due West and put all
    # three address forms in Cayce, 78 miles away, while the town page lands 0.15 miles from
    # campus. Stored as level "town" so the page can say it is the town's number.
    yield slug(addr['city'], addr['state'])


def curl(url, *args):
    return subprocess.run(['curl', '-s', '-m', '60', *args, url],
                          capture_output=True, text=True).stdout


def fetch(url, tries=3):
    """An empty body is rate limiting, not an answer. Fifteen rows of the first pass
    recorded as bad addresses this way and Clemson, one of them, returned Walk 54 on a
    plain retry a minute later -- so a short body backs off and asks again, and only a
    body that survives that is allowed to mean anything."""
    page = ''
    for i in range(tries):
        page = curl('https://r.jina.ai/' + url)
        if 'URL Source:' in page and len(page) > 400:
            return page
        time.sleep(15 * (i + 1))
    return page


def nominatim_road(coords):
    """Reverse geocode, keyless, one request and paced like the rest."""
    if not coords or coords[0] is None:
        return None
    time.sleep(PACE)
    body = curl('https://nominatim.openstreetmap.org/reverse?format=jsonv2'
                '&lat=%s&lon=%s&zoom=18' % coords,
                '-A', 'xc-cs-college-board/1.0 (github.com/timhibbard)')
    try:
        return json.loads(body)['address'].get('road')
    except Exception:
        return None


SCORE = re.compile(r'!\[Image \d+: (\d+) (Walk|Transit|Bike) Score of ([^\]]+)\]')
LABEL = re.compile(r'^##### (.+)$', re.M)
# The same page comes in two shapes and the second one is easy to miss: addresses with a
# full score set print three badge images, while others print a sentence and no badge at
# all. Fayetteville State read as "no score on page" against the badge pattern alone while
# the page plainly said 49. Anything that only ever matches one shape will silently record
# the thinner half of the board as unscored -- which is the same shape of bug as #2.
PROSE = re.compile(r'has a (Walk|Transit|Bike) Score of (\d+) out of 100')
PARKS = re.compile(r'Nearby parks include ([^.]+)\.')


TILE = re.compile(r'lat=(-?\d+\.\d+)/lng=(-?\d+\.\d+)')

# Both page shapes list the actual rail and bus lines with distances, under headings that
# survive the proxy, and this is the honest answer to the transit question -- better than the
# score it replaces. A Transit Score is printed only on the badge shape, so reading the score
# alone made 120 of 243 rows say "no transit feed", which Columbia (Walk 97, Manhattan)
# disproved on its own. Arcadia is the case that shows what was being thrown away: no Transit
# Score anywhere on its page, and two SEPTA regional rail lines 0.9 miles from the address
# with four bus routes inside 0.7.
LINES = re.compile(r'\*\*(Rail|Bus) lines:\*\*(.*?)(?=\*\*[A-Z]|\n## |\Z)', re.S)
LINE_ITEM = re.compile(r'^\*\s+(.+?)\s*$\s*^\s*$\s*^([\d.]+)\s*mi\s*$', re.M)


def transit_lines(page):
    """Named lines with distances, nearest first. An empty list is a real answer -- Covenant
    College on Lookout Mountain has no rail and no bus, which is a fact about the place, not
    a gap in the read."""
    out = {'rail': [], 'bus': []}
    for kind, block in LINES.findall(page):
        seen, got = set(), []
        for name, mi in LINE_ITEM.findall(block):
            # The proxy repeats the badge text, so "Orange Line" can arrive as "E Green Line
            # E". Names are kept verbatim; only exact repeats of the same line are dropped.
            name = re.sub(r'\s+', ' ', name).strip()
            if name.lower() in seen:
                continue
            seen.add(name.lower())
            got.append({'name': name[:60], 'mi': float(mi)})
        out[kind.lower()] = sorted(got, key=lambda g: g['mi'])
    return out


def haversine_mi(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 3958.7613 * math.asin(math.sqrt(h))


def parse(page, addr, coords=None):
    """Scores, plus proof the page answered about this campus and not another place.

    The proof is the coordinate in the page's own map tile URLs, not the place name it
    prints. Name matching rejected ten good rows: Walk Score calls Manhattan College's
    address Bronx, York College's Queens, Gardner-Webb's Shelby and Harvard's simply "this
    location", none of which contain the town the federal address gives. The coordinate
    settles it either way -- it is also what catches the lat/lng URL form answering about
    Maharashtra, which a state-name test would have waved through for a school in MH."""
    got, said = {}, ''
    for score, kind, where in SCORE.findall(page):
        got[kind.lower()] = int(score)
        said = where
    for kind, score in PROSE.findall(page):
        got.setdefault(kind.lower(), int(score))
    title = re.search(r'^Title: (.*)$', page, re.M)
    said = said or (title.group(1) if title else '')
    off = None
    for la, lo in TILE.findall(page):
        d = haversine_mi(coords, (float(la), float(lo))) if coords and coords[0] else None
        off = d if off is None else min(off, d)
    if off is not None:
        ok_where = off <= APPROX
    else:
        ok_where = (re.search(r'\b%s\b' % re.escape(addr['state']), said, re.I) is not None
                    and addr['city'].split()[0].lower() in said.lower())
    labels = LABEL.findall(page)
    if not labels:
        labels = re.findall(r'This location is an? ([A-Za-z\' ]+?) neighborhood', page)
    # Volunteered by the page, and a useful cross-check on the Overpass park query rather
    # than a substitute for it: these are names with no distance attached.
    parks = PARKS.search(page)
    return got, said, ok_where, off, labels, parks.group(1) if parks else None


def lines_pass(have, arg):
    """Second pass: revisit the URL a row already won with and read its transit lines off it.
    One fetch per row and no variants, because the address question is already settled -- so
    this cannot change a score, only add to it."""
    todo = ([arg] if arg and not arg.isdigit()
            else [n for n, v in sorted(have.items())
                  if 'walk' in v and 'rail' not in v][:int(arg or 10)])
    for i, name in enumerate(todo, 1):
        url = have[name].get('url')
        if not url:
            continue
        page = fetch(url)
        if 'URL Source:' not in page:
            print('%3d/%-3d %-24s proxy returned nothing, left for a later pass'
                  % (i, len(todo), name))
            time.sleep(PACE)
            continue
        got = transit_lines(page)
        have[name].update(got)
        rail, bus = got['rail'], got['bus']
        print('%3d/%-3d %-24s rail %-4s %-28s bus %-3s %s'
              % (i, len(todo), name, rail[0]['mi'] if rail else '--',
                 (rail[0]['name'] if rail else '')[:28], len(bus),
                 ('%s mi  %s' % (bus[0]['mi'], bus[0]['name'][:30])) if bus else ''))
        json.dump(have, open(OUT, 'w'), indent=1, sort_keys=True)
        if i < len(todo):
            time.sleep(PACE)
    done = [v for v in have.values() if 'rail' in v]
    print('\n%d rows read for lines: %d with rail, %d with bus, %d with neither'
          % (len(done), sum(bool(v['rail']) for v in done), sum(bool(v['bus']) for v in done),
             sum(not v['rail'] and not v['bus'] for v in done)))


def main():
    have = json.load(open(OUT)) if os.path.exists(OUT) else {}
    rows = json.load(open(os.path.join(WORK, 'setting1.json')))
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == '--lines':
        return lines_pass(have, sys.argv[2] if len(sys.argv) > 2 else None)
    if arg and not arg.isdigit():
        todo = [arg]
    else:
        todo = [n for n in sorted(rows) if n not in have][:int(arg or 10)]

    for i, name in enumerate(todo, 1):
        addr = dict(rows[name].get('addr') or {}, **ADDR_BY_HAND.get(name, {}))
        if not addr:
            have[name] = {'miss': 'no address'}
            continue
        # Every slug is tried and the CLOSEST answer wins, rather than the first one that is
        # merely close enough. Taking the first accepted answer made the column depend on
        # which earlier slug happened to fail: two runs over these rows disagreed on 25,
        # because a rejected house number fell through to the road and scored the road.
        rec, best, tries = None, None, 0
        coords = (rows[name].get('lat'), rows[name].get('lon'))
        for s in variants(addr, coords):
            if tries:
                time.sleep(PACE)
            tries += 1
            url = 'https://www.walkscore.com/score/' + s
            page = fetch(url)
            got, said, ok_where, off, labels, parks = parse(page, addr, coords)
            if 'URL Source:' not in page:
                # Kept distinct from a wrong address on purpose: this row has not been
                # answered yet, so a later pass should retry it rather than publish a gap.
                rec = {'miss': 'proxy returned nothing', 'url': url}
                break
            if not ok_where:
                rec = rec or {'miss': 'answered about somewhere else', 'url': url,
                              'said': said[:80],
                              'offBy': round(off, 1) if off is not None else None}
            elif not got:
                rec = rec or {'miss': 'no score published', 'url': url, 'said': said[:80]}
            else:
                level = ('town' if s == slug(addr['city'], addr['state'])
                         else 'address' if off is None or off <= NEAR else 'approx')
                cand = {'walk': got.get('walk'), 'transit': got.get('transit'),
                        'bike': got.get('bike'), 'url': url, 'said': said,
                        'labels': labels[:3], 'parks': parks, 'tries': tries,
                        'level': level, 'offBy': round(off, 2) if off is not None else None}
                key = rank(level, off if off is not None else NEAR)
                if best is None or key < best[0]:
                    best = (key, cand)
                if level == 'address' and off is not None and off <= CLOSE_ENOUGH:
                    break
        have[name] = rec = best[1] if best else rec
        print('%3d/%-3d %-24s %s' % (
            i, len(todo), name,
            rec.get('miss') or 'walk %-3s transit %-4s bike %-3s  %s' % (
                rec['walk'], rec['transit'] if rec['transit'] is not None else '--',
                rec['bike'], rec['said'][:44])))
        json.dump(have, open(OUT, 'w'), indent=1, sort_keys=True)
        if i < len(todo):
            time.sleep(PACE)

    done = [v for v in have.values() if 'walk' in v]
    print('\n%d rows on file, %d with a score, %d missed, %d with no transit feed'
          % (len(have), len(done), len(have) - len(done),
             sum(v.get('transit') is None for v in done)))


if __name__ == '__main__':
    main()
