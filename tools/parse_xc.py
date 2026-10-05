"""Parse a TFRRS XC result page -> men's individual finishers (no names kept).

Returns {'dist': '8k', 'fin': [ {pl, team_slug, yr, sec}, ... ]}
YEAR is a real column on TFRRS individual tables; we keep it and the time,
and deliberately discard the NAME column (repo no-names rule).

A YEAR cell the board does not understand becomes None, never the raw token. Meets write
that column freely -- FRESHMAN, 2029, RS/UNA, NA, ?, an empty cell that survives as
&NBSP; -- and passing those through has a specific cost downstream: `shape` counts a
returning man as any known year that is not SR, so '&NBSP;' was being counted as a
sophomore who comes back. One such token is on file today (High Point, 2026-09-04) and it
got there through this function. The two conversions that CAN be made are made: the word
forms, and a graduation year read against the season the race was run in.
"""
import re, sys, json

YRMAP = {'FR': 'FR', 'SO': 'SO', 'JR': 'JR', 'SR': 'SR',
         'FR-1': 'FR', 'SO-2': 'SO', 'JR-3': 'JR', 'SR-4': 'SR', 'FY': 'FR',
         'FRESHMAN': 'FR', 'FRESHMEN': 'FR', 'SOPHOMORE': 'SO',
         'JUNIOR': 'JR', 'SENIOR': 'SR'}

def _yr(raw, season):
    """One YEAR cell -> FR/SO/JR/SR or None. `season` is the autumn the race was run in."""
    y = YRMAP.get(raw)
    if y:
        return y
    # A class of 2029 is a freshman in the 2025 season. Without a season there is nothing
    # to read it against, so it stays unknown rather than becoming a guess.
    if season and re.match(r'^(19|20)\d\d$', raw):
        return {4: 'FR', 3: 'SO', 2: 'JR', 1: 'SR'}.get(int(raw) - season)
    return None

def _dist(m):
    """A section title's distance -> '8k', '6.2k', '4.97m'. None if the title has no distance.

    Three normalisations, each of which a downstream stage would otherwise get wrong. A meet
    that writes "6200K" means 6,200 metres -- the CSU Buccaneer Open does, and its own
    parenthetical says (6.2k) -- and no college race is six thousand kilometres, so a k
    over 100 is metres. And "8.0K" is the same race as "8K": the projection table is keyed
    by the string, so an unnormalised '8.0k' would store a full 8K race as having no
    projection at all, which puts a null where a measurement belongs.

    The third is the same argument for the unit that also abbreviates miles. "8000M" is
    8,000 metres and no college race is eight thousand miles -- Running of the Cows writes
    its sections that way, and its own parenthetical says (8k). Four standard 8K races came
    off that one page as dist '8000m' with slot, g1 and v7 all null, which is the exact
    failure the 8.0K rule above was written to stop, one spelling short. The threshold
    separates cleanly: every mile distance this board holds is under 100 -- 2M, 4M, 5.2M.
    """
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2).lower()[0]
    if v >= 100 and u in 'km':
        v, u = v / 1000, 'k'
    return '%g%s' % (v, u)

def _txt(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).strip()

def _sec(t):
    t=t.strip()
    m=re.match(r'^(?:(\d+):)?(\d+(?:\.\d+)?)$',t)
    if not m: return None
    mn=int(m.group(1) or 0)
    return round(mn*60+float(m.group(2)),1)

def _rows(seg,season=None):
    """Parse the finisher rows out of one h3-delimited section."""
    tb=re.search(r'<tbody.*?</tbody>',seg,re.S)
    if not tb: return []
    th=re.search(r'<thead.*?</thead>',seg,re.S)
    cols=[_txt(c).upper() for c in re.findall(r'<th[^>]*>(.*?)</th>',th.group(0),re.S)] if th else []
    idx={c:j for j,c in enumerate(cols)}
    fin=[]
    for tr in re.findall(r'<tr.*?</tr>',tb.group(0),re.S):
        tds=re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)
        if len(tds)<len(cols)-1: continue
        def col(n):
            j=idx.get(n)
            return tds[j] if j is not None and j<len(tds) else ''
        slug=None
        tm=re.search(r'/teams/xc/([A-Za-z0-9_\-]+)\.html',col('TEAM'))
        if tm: slug=tm.group(1)
        sec=_sec(_txt(col('TIME')))
        if sec is None: continue
        yr=_txt(col('YEAR')).upper().replace('.','')
        fin.append({'pl':_txt(col('PL')),'team':slug,'yr':_yr(yr,season),'sec':sec})
    return fin

def parse(html,season=None):
    # cut the page into h3-delimited sections
    heads=[(m.start(),_txt(m.group(1))) for m in re.finditer(r'<h3[^>]*>(.*?)</h3>',html,re.S)]
    out=[]
    for i,(pos,title) in enumerate(heads):
        if 'Individual' not in title: continue
        # "Women" contains "men": require men'?s? NOT preceded by "wo".
        # TFRRS also writes "(M)", "Boys", and IC4A (a men-only championship).
        isw=re.search(r"(?<!\w)wo?men|\(W\)|\bgirls\b",title,re.I)
        ism=(re.search(r"(?<!wo)\bmen'?s?\b",title,re.I) or re.search(r"\(M\)|\bboys\b|\bIC4A\b",title,re.I))
        if isw or not ism: continue
        # A team's JV/open/alumni squad is not its scoring seven -- but that is true of a
        # *team*, not of a section, and this used to drop the section outright. At Lehigh's
        # Paul Short the men race twice, and the Open has individual results and no team
        # table at all: nine board programs were named on that page, had every finisher in
        # the Open and none in the Gold, and were reported as DNS. A squad that ran only the
        # open race is the squad the program brought that day. So the section is kept and
        # flagged, and the caller prefers a varsity section for any team that has one --
        # which leaves every race already on file reading from the section it always did.
        sub=bool(re.search(r"\b(jv|junior varsity|freshm[ae]n|alumni|reserve|development|b race|open race)\b",title,re.I))
        end=heads[i+1][0] if i+1<len(heads) else len(html)
        seg=html[pos:end]
        dm=re.search(r'\b(\d+(?:\.\d+)?)\s*([kKmM](?:iles?)?)\b',title)
        dist=_dist(dm)
        fin=_rows(seg,season)
        if not fin: continue
        out.append({'dist':dist,'title':title,'n':len(fin),'fin':fin,'sub':sub})
    if not out:
        # Some meets label sections by distance only. At college level men race
        # 8K/10K and women 5K/6K, so an unsexed 8K/10K section is the men's race.
        for i,(pos,title) in enumerate(heads):
            if 'Individual' not in title: continue
            if re.search(r"(?<!\w)wo?men|\(W\)|\bgirls\b",title,re.I): continue
            dm=re.search(r'\b(8|10)(?:\.0)?\s*[kK]\b',title)
            if not dm: continue
            end=heads[i+1][0] if i+1<len(heads) else len(html)
            sec=_rows(html[pos:end],season)
            if sec: out.append({'dist':dm.group(1)+'k','title':title+' [unsexed 8K/10K]','n':len(sec),'fin':sec,'sub':False})
    return out

if __name__=='__main__':
    h=open(sys.argv[1],encoding='utf-8',errors='replace').read()
    for s in parse(h):
        print(s['title'],'| dist',s['dist'],'| finishers',s['n'])
        for f in s['fin'][:8]: print('   ',f)
        yrs={}
        for f in s['fin']: yrs[f['yr']]=yrs.get(f['yr'],0)+1
        print('    year coverage:',yrs)
        vil=[f for f in s['fin'] if f['team'] and 'Villanova' in f['team']]
        print('    Villanova finishers:',[(f['pl'],f['yr'],f['sec']) for f in vil])
