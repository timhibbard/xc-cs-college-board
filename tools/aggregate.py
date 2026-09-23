"""Aggregate per-school XC numbers and squad shape.

Tier-bearing numbers come from CHAMPIONSHIP-LEVEL races only (conference, NCAA
regional, NCAA championship), which is what the existing board used and the only
races where teams reliably field a full varsity seven. Measured bias: championship
races read ~10s deeper at the median than invitationals, and up to 160s for
individual schools, so mixing them would demote healthy programs.

Invitationals are kept as a separate read, and supply squad-shape data.
"""
import json,collections,statistics
# Paths are derived from this file's own location so the pipeline runs from a clone
# rather than from one machine's home directory. Intermediates go to tools/.work/,
# which is gitignored: they are fetch caches and multi-megabyte joins, not source.
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
WORK = REPO / 'tools' / '.work'
WORK.mkdir(parents=True, exist_ok=True)
R = str(WORK) + '/'
BT=json.load(open(R+'byteam.json'))
AS=json.load(open(R+'allslugs.json'))
ORDER=['FR','SO','JR','SR']
CHAMP={'conference','NCAA regional','national championship'}

def season(d): return int(d[:4])-(1 if d[5:7]<'08' else 0)
def retained(yrs,frm,fall):
    step=fall-frm; n=0
    for y in yrs:
        if y and ORDER.index(y)+step<=3: n+=1
    return n

def summarise(rs):
    if not rs: return None
    def m(k):
        v=[r[k] for r in rs if r.get(k) is not None]
        return round(statistics.fmean(v),1) if v else None
    sev=[r['v7'] for r in rs if r['nfin']>=7 and r.get('v7') is not None]
    return {'nraces':len(rs),'slot':round(statistics.fmean([r['slot'] for r in rs]),1),
            'g1':m('g1'),'spread':m('spread'),
            'v7':(round(statistics.fmean(sev),1) if sev else None),
            'short':(len(sev)==0),'maxfin':max(r['nfin'] for r in rs),
            'seasons':sorted({season(r['date']) for r in rs}),
            'rids':[r['rid'] for r in rs]}

def agg(slug):
    allr=BT.get(slug,[])
    # Five finishers is the floor for a comparable race: below that there is no scoring five,
    # so "his slot in their 7" has nothing to be a slot in. DO NOT lower this globally to pick
    # up thin schools. cmpable filters races before they are averaged, so a lower floor would
    # also pull 1-4 finisher championship races into the aggregates of healthy programs, moving
    # their g1 and spread and shifting tiers across the whole board. The floor is right.
    cmpable=[r for r in allr if r['g1'] is not None and r['nfin']>=5]
    ch=[r for r in cmpable if r['level'] in CHAMP]
    iv=[r for r in cmpable if r['level'] not in CHAMP]
    out={'races_all':len(allr),'races_cmp':len(cmpable)}
    out['xc']=summarise(ch); out['xcInv']=summarise(iv)
    if not cmpable:
        # What the floor costs, and the reason `unmeasured` is not the same as "no data": a school
        # can land here having been measured at a championship and found to field one or two men.
        # That is the strongest evidence of a thin program there is, and it used to be reported as
        # an absence of evidence, because no xc block meant ladder.py skipped the row and it kept
        # the Verify it was seeded with. Carlow, Marymount and Hilbert sat at Verify that way while
        # their own notes recorded 1-2 finishers at a conference championship; they are hand-tiered
        # Caution now. So: check `maxfin` and the championship levels in XCRACES before treating an
        # unmeasured row as unknown. A conference championship is the race a program brings everyone
        # to, so a short field there is a measurement. A *national* championship is not - only
        # individual qualifiers go, which is why Thomas Jefferson's single finisher there is
        # genuinely no evidence about depth and that row is still Verify.
        out['unmeasured']=True; out['maxfin']=max([r['nfin'] for r in allr],default=0)
        out['champ_levels']=sorted({r['level'] for r in allr if r['level'] in CHAMP})
        out['champ_maxfin']=max([r['nfin'] for r in allr if r['level'] in CHAMP],default=0)
    # squad shape: deepest championship race, else deepest race of any kind
    pool=ch or cmpable or allr
    if pool:
        src=sorted(pool,key=lambda r:(r['nfin'],r['date']))[-1]
        yrs=src['years'][:7]; sn=season(src['date'])
        comp=collections.Counter(y for y in yrs if y)
        out['shape']={'rid':src['rid'],'meet':src['meet'],'date':src['date'],'season':sn,
            'level':src['level'],'n':len(yrs),'years':yrs,
            'by':{k:comp.get(k,0) for k in ORDER},'unknown':sum(1 for y in yrs if not y),
            'retain':{str(f):retained(yrs,sn,f) for f in (sn+1,sn+2,sn+3)}}
    return out

res={}
for name,slug in list(AS['slugmap'].items())+[(k,v) for k,v in AS['ring'].items() if v]:
    if slug: res.setdefault(name,{'slug':slug,**agg(slug)})
json.dump(res,open(R+'agg.json','w'),indent=1)
print("schools:",len(res))
print("with championship-level races:",sum(1 for v in res.values() if v['xc']))
print("championship-only, no invitational:",sum(1 for v in res.values() if v['xc'] and not v['xcInv']))
print("no comparable race at all:",sum(1 for v in res.values() if v.get('unmeasured')))
n=[v['xc']['nraces'] for v in res.values() if v['xc']]
print("championship races/school: mean %.1f median %s max %d"%(statistics.fmean(n),statistics.median(n),max(n)))
print("\n-- examples (championship-level) --")
for k in ['DePaul','Catawba','Lincoln Memorial','Villanova','Georgetown','Wake Forest']:
    v=res.get(k)
    if not v or not v['xc']: continue
    x=v['xc']; s=v['shape']
    print(f"{k:18} n={x['nraces']} slot={x['slot']} g1={x['g1']} v7={x['v7']} spread={x['spread']}")
    print(f"     seven {s['years']} ({s['season']}, {s['level']}) retain={s['retain']}")
