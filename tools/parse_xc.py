"""Parse a TFRRS XC result page -> men's individual finishers (no names kept).

Returns {'dist': '8k', 'fin': [ {pl, team_slug, yr, sec}, ... ]}
YEAR is a real column on TFRRS individual tables; we keep it and the time,
and deliberately discard the NAME column (repo no-names rule).
"""
import re, sys, json

YRMAP={'FR':'FR','SO':'SO','JR':'JR','SR':'SR','FR-1':'FR','SO-2':'SO','JR-3':'JR','SR-4':'SR'}

def _txt(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).strip()

def _sec(t):
    t=t.strip()
    m=re.match(r'^(?:(\d+):)?(\d+(?:\.\d+)?)$',t)
    if not m: return None
    mn=int(m.group(1) or 0)
    return round(mn*60+float(m.group(2)),1)

def _rows(seg):
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
        fin.append({'pl':_txt(col('PL')),'team':slug,'yr':YRMAP.get(yr,yr or None),'sec':sec})
    return fin

def parse(html):
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
        # a team's JV/open/alumni squad is not its scoring seven
        if re.search(r"\b(jv|junior varsity|freshm[ae]n|alumni|reserve|development|b race|open race)\b",title,re.I):
            continue
        end=heads[i+1][0] if i+1<len(heads) else len(html)
        seg=html[pos:end]
        dm=re.search(r'\b(\d+(?:\.\d+)?)\s*([kKmM](?:iles?)?)\b',title)
        dist=(dm.group(1)+dm.group(2).lower()[0]) if dm else None
        fin=_rows(seg)
        if not fin: continue
        out.append({'dist':dist,'title':title,'n':len(fin),'fin':fin})
    if not out:
        # Some meets label sections by distance only. At college level men race
        # 8K/10K and women 5K/6K, so an unsexed 8K/10K section is the men's race.
        for i,(pos,title) in enumerate(heads):
            if 'Individual' not in title: continue
            if re.search(r"(?<!\w)wo?men|\(W\)|\bgirls\b",title,re.I): continue
            dm=re.search(r'\b(8|10)(?:\.0)?\s*[kK]\b',title)
            if not dm: continue
            end=heads[i+1][0] if i+1<len(heads) else len(html)
            sec=_rows(html[pos:end])
            if sec: out.append({'dist':dm.group(1)+'k','title':title+' [unsexed 8K/10K]','n':len(sec),'fin':sec})
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
