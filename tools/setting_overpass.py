#!/usr/bin/env python3
"""Stage 3 of the campus-setting column (#13): the axis Walk Score cannot see.

A high Walk Score is a claim about errands, not about running. This pass asks OpenStreetMap
the questions a distance runner would ask on a visit, from the campus coordinate out:

  parkMi / parkName / parkAc  nearest park, reserve or wood of at least MIN_AC acres, and
                              the biggest one within RUN_MI -- the acreage matters because a
                              two-acre square with a fountain is not somewhere to run
  softMi                      total length of unpaved path, track and trail within RUN_MI
  netMi                       the largest *connected* network of it, which is the honest
                              version of "how far can he run without stopping": twelve
                              disconnected half-miles are not a six-mile run
  crossPerMi                  signalised crossings per mile of road within CROSS_MI, the
                              number that makes an urban campus miserable for a tempo run
  campusAc                    area of the campus polygon, or None where OSM has no polygon
                              for it -- this is what separates MIT from NYU, which score
                              alike on errands and are not alike to live on
  trackMi                     nearest running track, because a team without one on site
                              drives to intervals and that is a real fact about the week

Everything here is keyless. Overpass rejects curl's default user agent with a 406 and is
intermittently too busy, so every query is paced, retried, and sent with a real agent.

  in:   tools/.work/setting1.json   (python3 tools/setting_locale.py)
  out:  tools/.work/overpass.json   -- merged, so a re-run only fetches what is missing
  args: [n] rows this pass, or a school name to do one row
"""
import json, math, os, subprocess, sys, time

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.work')
OUT = os.path.join(WORK, 'overpass.json')
MIRRORS = ['https://overpass-api.de/api/interpreter',
           'https://overpass.kumi.systems/api/interpreter']
AGENT = 'xc-cs-college-board/1.0 (github.com/timhibbard)'
PACE = 4.0
RUN_MI = 2.0        # a warm-up plus a little: what he could reach on foot from the door
CROSS_MI = 1.0
MIN_AC = 10.0       # below this a "park" is a lawn with a bench
M_PER_MI = 1609.34
SOFT = ('dirt', 'ground', 'grass', 'gravel', 'fine_gravel', 'earth', 'sand', 'wood',
        'woodchips', 'compacted', 'unpaved', 'mud', 'pebblestone')


def q(lat, lon):
    r, c = int(RUN_MI * M_PER_MI), int(CROSS_MI * M_PER_MI)
    return f"""[out:json][timeout:90];
(
  nwr(around:{r},{lat},{lon})["leisure"~"^(park|nature_reserve)$"];
  nwr(around:{r},{lat},{lon})["landuse"~"^(forest|recreation_ground|village_green)$"];
  nwr(around:{r},{lat},{lon})["natural"="wood"];
)->.green;
(
  way(around:{r},{lat},{lon})["highway"~"^(path|footway|cycleway|track|bridleway)$"];
)->.paths;
(
  way(around:{c},{lat},{lon})["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|service)$"];
)->.roads;
(
  node(around:{c},{lat},{lon})["highway"~"^(crossing|traffic_signals)$"];
)->.cross;
(
  nwr(around:{r},{lat},{lon})["amenity"="university"];
  nwr(around:{r},{lat},{lon})["amenity"="college"];
)->.campus;
(
  nwr(around:{r},{lat},{lon})["leisure"="track"];
)->.track;
(.green; .paths; .roads; .cross; .campus; .track;);
out tags geom;"""


def haversine_m(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


def length_m(geom):
    return sum(haversine_m((geom[i]['lat'], geom[i]['lon']),
                           (geom[i + 1]['lat'], geom[i + 1]['lon']))
               for i in range(len(geom) - 1))


def area_ac(geom):
    """Shoelace on a local equirectangular projection -- accurate well past park size."""
    if len(geom) < 4:
        return 0.0
    lat0 = math.radians(sum(p['lat'] for p in geom) / len(geom))
    xy = [(math.radians(p['lon']) * math.cos(lat0) * 6371008.8,
           math.radians(p['lat']) * 6371008.8) for p in geom]
    s = sum(xy[i][0] * xy[i + 1][1] - xy[i + 1][0] * xy[i][1] for i in range(len(xy) - 1))
    return abs(s) / 2 / 4046.86


def near_m(geom, at):
    return min((haversine_m((p['lat'], p['lon']), at) for p in geom), default=None)


def fetch(query, tries=4):
    """Overpass answers "too busy" often enough that one attempt means nothing."""
    for i in range(tries):
        host = MIRRORS[i % len(MIRRORS)]
        r = subprocess.run(['curl', '-s', '-m', '120', '-A', AGENT, host,
                            '--data-urlencode', 'data=' + query],
                           capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(10 * (i + 1))
    return None


def measure(el_list, at):
    green, paths, roads, cross, campus, track = [], [], 0.0, 0, [], []
    for e in el_list:
        t = e.get('tags') or {}
        geom = e.get('geometry') or ([{'lat': e['lat'], 'lon': e['lon']}]
                                     if e.get('lat') is not None else [])
        if not geom:
            continue
        hw = t.get('highway')
        if t.get('leisure') == 'track':
            track.append(near_m(geom, at))
        elif t.get('amenity') in ('university', 'college'):
            campus.append((area_ac(geom), t.get('name')))
        elif (t.get('leisure') in ('park', 'nature_reserve')
                or t.get('landuse') in ('forest', 'recreation_ground', 'village_green')
                or t.get('natural') == 'wood'):
            green.append((area_ac(geom), near_m(geom, at), t.get('name')))
        elif hw in ('path', 'footway', 'cycleway', 'track', 'bridleway'):
            # Paved footways are sidewalks. The question is soft surface, so an unpaved or
            # untagged path counts and an explicitly paved one does not.
            if t.get('surface') in SOFT or (t.get('surface') is None and hw != 'footway'):
                paths.append(geom)
        elif hw:
            roads += length_m(geom)
        if hw in ('crossing', 'traffic_signals'):
            cross += 1

    big = [g for g in green if g[0] >= MIN_AC]
    nearest = min(big, key=lambda g: g[1]) if big else None
    biggest = max(big, key=lambda g: g[0]) if big else None
    soft_m = sum(length_m(g) for g in paths)
    return {
        'parkMi': round(nearest[1] / M_PER_MI, 2) if nearest else None,
        'parkName': nearest[2] if nearest else None,
        'parkAc': round(biggest[0]) if biggest else None,
        'parkBig': biggest[2] if biggest else None,
        'softMi': round(soft_m / M_PER_MI, 2),
        'netMi': round(network_mi(paths), 2),
        'crossPerMi': round(cross / (roads / M_PER_MI), 1) if roads > 500 else None,
        'roadMi': round(roads / M_PER_MI, 1),
        'campusAc': round(max(campus)[0]) if campus else None,
        'trackMi': round(min(t for t in track if t is not None) / M_PER_MI, 2) if track else None,
    }


def network_mi(paths):
    """Largest connected run of path, by joining ways that share an endpoint. Twelve
    disconnected half-miles are not a six-mile run, so total length alone would flatter a
    campus ringed by driveway stubs."""
    ends, comp = {}, list(range(len(paths)))

    def find(i):
        while comp[i] != i:
            comp[i] = comp[comp[i]]
            i = comp[i]
        return i

    for i, g in enumerate(paths):
        for p in (g[0], g[-1]):
            k = (round(p['lat'], 6), round(p['lon'], 6))
            if k in ends:
                a, b = find(ends[k]), find(i)
                if a != b:
                    comp[a] = b
            else:
                ends[k] = i
    tot = {}
    for i, g in enumerate(paths):
        tot[find(i)] = tot.get(find(i), 0.0) + length_m(g)
    return max(tot.values(), default=0.0) / M_PER_MI


def main():
    have = json.load(open(OUT)) if os.path.exists(OUT) else {}
    rows = json.load(open(os.path.join(WORK, 'setting1.json')))
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    todo = ([arg] if arg and not arg.isdigit()
            else [n for n in sorted(rows) if n not in have][:int(arg or 10)])

    for i, name in enumerate(todo, 1):
        at = (rows[name]['lat'], rows[name]['lon'])
        data = fetch(q(*at))
        if data is None or 'elements' not in data:
            print('%3d/%-3d %-24s overpass gave nothing' % (i, len(todo), name))
            continue
        have[name] = measure(data['elements'], at)
        m = have[name]
        print('%3d/%-3d %-24s park %-5s %-22s net %-5s soft %-5s cross/mi %-5s campus %-5s track %s'
              % (i, len(todo), name, m['parkMi'], (m['parkName'] or '')[:22], m['netMi'],
                 m['softMi'], m['crossPerMi'], m['campusAc'], m['trackMi']))
        json.dump(have, open(OUT, 'w'), indent=1, sort_keys=True)
        if i < len(todo):
            time.sleep(PACE)

    print('\n%d rows on file' % len(have))


if __name__ == '__main__':
    main()
