import csv, math, json, time, subprocess, sys
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'

CENTERS=[("New York",40.7128,-74.0060),("Chicago",41.8781,-87.6298),("Philadelphia",39.9526,-75.1652),
("Charlotte",35.2271,-80.8431),("Washington DC",38.9072,-77.0369),("Boston",42.3601,-71.0589),
("Baltimore",39.2904,-76.6122),("Atlanta",33.7490,-84.3880),("Raleigh",35.7796,-78.6382),
("Virginia Beach",36.8529,-75.9780),("Newark",40.7357,-74.1724),("Pittsburgh",40.4406,-79.9959),
("Greensboro",36.0726,-79.7920),("Durham",35.9940,-78.8986),("Jersey City",40.7178,-74.0431),
("Buffalo",42.8864,-78.8784),("Chesapeake",36.7682,-76.2875),("Winston-Salem",36.0999,-80.2442),
("Arlington",38.8816,-77.0910),("Norfolk",36.8508,-76.2859)]
R=3958.8
def gc(a,b,c,d):
    p,q=math.radians(a),math.radians(c)
    return 2*R*math.asin(math.sqrt(math.sin((q-p)/2)**2+math.cos(p)*math.cos(q)*math.sin(math.radians(d-b)/2)**2))
def drive(la,lo,cla,clo):
    """Returns miles, or None on failure. Uses curl: this python has no CA bundle."""
    u=f"https://router.project-osrm.org/route/v1/driving/{clo},{cla};{lo},{la}?overview=false"
    for attempt in range(4):
        try:
            out=subprocess.run(["curl","-s","-m","30",u],capture_output=True,text=True,timeout=40).stdout
            j=json.loads(out)
            if j.get("code")=="Ok": return j["routes"][0]["distance"]/1609.34
        except Exception: pass
        time.sleep(2*(attempt+1))
    return None
has=lambda r,k: r.get(k) not in (None,'','NA','NULL')
cands=[]
# College Scorecard institution file, downloaded by hand into tools/.work/ from
# https://collegescorecard.ed.gov/data/ - it is ~250MB unzipped and is not vendored.
with open(R+'Most-Recent-Cohorts-Institution.csv',encoding='utf-8-sig',errors='replace') as f:
    for r in csv.DictReader(f):
        if r.get('ICLEVEL')!='1': continue
        if not(has(r,'LATITUDE') and has(r,'LONGITUDE') and has(r,'UGDS')): continue
        if float(r['UGDS'])<200: continue
        la,lo=float(r['LATITUDE']),float(r['LONGITUDE'])
        near=sorted([(gc(la,lo,a,b),n) for n,a,b in CENTERS])
        if near[0][0]>20: continue     # driving >= straight-line, so definitively out
        cands.append(dict(unitid=r['UNITID'],name=r['INSTNM'],city=r['CITY'],st=r['STABBR'],
            lat=la,lon=lo,ugds=int(float(r['UGDS'])),ctrl=r.get('CONTROL'),
            sl=[[round(d,2),n] for d,n in near if d<=20]))
print(f"{len(cands)} schools with a center within 20 straight-line mi",flush=True)
print(f"{sum(len(c['sl']) for c in cands)} OSRM pairs max",flush=True)
cmap={n:(a,b) for n,a,b in CENTERS}
fails=0
for i,c in enumerate(cands,1):
    best=(None,None); anyfail=False
    for sl,cn in c['sl']:
        cla,clo=cmap[cn]
        dm=drive(c['lat'],c['lon'],cla,clo)
        if dm is None: anyfail=True; continue
        if best[0] is None or dm<best[0]: best=(dm,cn)
        if best[0]<=20: break
    c['drive']=round(best[0],1) if best[0] is not None else None
    c['center']=best[1]
    if c['drive'] is None:
        c['status']='OSRM_FAILED'; fails+=1          # never silently "out"
    elif c['drive']<=20: c['status']='IN'
    else: c['status']='OUT'
    if i%25==0: print(f"  {i}/{len(cands)}  in={sum(1 for x in cands[:i] if x.get('status')=='IN')} failed={fails}",flush=True)
json.dump(cands,open(R+'candidates.json','w'),indent=1)
from collections import Counter
print("\n"+str(Counter(c['status'] for c in cands)),flush=True)
print("DONE",flush=True)
