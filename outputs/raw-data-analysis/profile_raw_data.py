"""Reproducible, full-data Inside Airbnb EDA; never modifies data/raw.

Run: python scripts/profile_raw_data.py
Dependencies: pandas==3.0.1, numpy==2.3.5 (tested versions).
An on-disk SQLite frequency table keeps exact distinct counts without loading
the full calendar/reviews into memory. All metrics use full files, not samples.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import html
import json
import math
from pathlib import Path
import platform
import sqlite3
import tempfile

import numpy as np
import pandas as pd

SOURCE = 'https://insideairbnb.com/get-the-data/'
DICTIONARY = 'https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit'
ASSUMPTIONS = 'https://insideairbnb.com/data-assumptions/'
DATE_FIELDS = {'date','last_scraped','host_since','calendar_last_scraped','first_review','last_review',
               'price_quote_checkin_date','price_quote_checkout_date'}
IDS = {'id','listing_id','host_id','host_profile_id','reviewer_id','scrape_id'}
BOOL = {'available','has_availability','host_is_superhost','host_has_profile_pic',
        'host_identity_verified','instant_bookable'}
NUMERIC = {'latitude','longitude','accommodates','bathrooms','bedrooms','beds','price',
           'minimum_nights','maximum_nights','minimum_minimum_nights','maximum_minimum_nights',
           'minimum_maximum_nights','maximum_maximum_nights','minimum_nights_avg_ntm','maximum_nights_avg_ntm',
           'host_response_rate','host_acceptance_rate','host_listings_count','host_total_listings_count',
           'number_of_reviews','number_of_reviews_ltm','number_of_reviews_l30d','number_of_reviews_ly',
           'reviews_per_month','availability_eoy','estimated_occupancy_l365d','estimated_revenue_l365d',
           'price_quote_total_price','price_quote_price_per_night'}
PRIVATE_TEXT = {'name','host_name','reviewer_name','comments','host_about','description',
                'neighborhood_overview','picture_url','host_url','host_profile_url','listing_url',
                'host_picture_url','host_thumbnail_url','price_quote_raw'}
GRAINS = {'listings.extracted.csv':['id'], 'listings.csv':['id'],
          'reviews.extracted.csv':['id'], 'calendar.extracted.csv':['listing_id','date'],
          'neighbourhoods.csv':['neighbourhood_group','neighbourhood']}
DEFINITIONS = {
 'id':'Listing identifier in listings; review identifier in detailed reviews. A key, not a measure.',
 'listing_id':'Listing key linking reviews/calendar rows to listings.',
 'listing_url':'Link to the listing page.', 'scrape_id':'Identifier of the collection run.',
 'last_scraped':'Date this listing was collected; not a booking or stay date.',
 'source':'How the listing was discovered in the collection process.',
 'name':'Listing title.', 'description':'Listing description supplied on the platform.',
 'neighborhood_overview':'Host-written description of the surrounding area.',
 'picture_url':'Listing image link.', 'host_id':'Airbnb host/user identifier.',
 'host_url':'Host account page link.', 'host_profile_id':'Host profile identifier; role inferred from name, current semantics unverified.',
 'host_profile_url':'Host profile page link; inferred from field name.',
 'host_name':'Displayed host name; not a stable key.',
 'host_since':'Account registration date; may precede hosting activity.',
 'host_location':'Self-reported host location.', 'host_about':'Host biography/free text.',
 'host_response_time':'Categorical reported response speed.',
 'host_response_rate':'Reported response percentage; profiled in percentage points (0–100).',
 'host_acceptance_rate':'Reported request acceptance percentage; percentage points (0–100).',
 'host_is_superhost':'Superhost status flag.', 'host_thumbnail_url':'Small host image link.',
 'host_picture_url':'Host image link.', 'host_neighbourhood':'Host-associated neighbourhood label.',
 'host_listings_count':'Platform-reported host listing count; calculation/scope not fully specified.',
 'host_total_listings_count':'Platform-reported total host listing count; scope not fully specified.',
 'host_verifications':'Serialized list of host verification methods.',
 'host_has_profile_pic':'Whether a host profile photo is present.',
 'host_identity_verified':'Reported identity-verification status.',
 'neighbourhood':'Summary: mapped neighbourhood label; detailed listings: source neighbourhood text.',
 'neighbourhood_group':'Higher-level mapped geographical group (municipality labels observed locally).',
 'neighbourhood_cleansed':'Neighbourhood assigned by spatial matching.',
 'neighbourhood_group_cleansed':'Higher-level spatially assigned group; local labels appear to be municipalities.',
 'latitude':'Approximate WGS84 latitude; position is anonymized.',
 'longitude':'Approximate WGS84 longitude; position is anonymized.',
 'property_type':'Reported property/accommodation classification.',
 'room_type':'Accommodation privacy category, e.g. entire home or private room.',
 'accommodates':'Advertised maximum guest capacity.', 'bathrooms':'Numeric bathroom count.',
 'bathrooms_text':'Bathroom count and sharing description in text.',
 'bedrooms':'Reported bedroom count.', 'beds':'Reported bed count.',
 'amenities':'Serialized list of amenities; needs parsing for individual amenities.',
 'price':'Advertised nightly price in local currency; not realized revenue. Currency symbols alone do not identify currency.',
 'price_quote_checkin_date':'Quote check-in date; interpretation inferred, current source semantics unverified.',
 'price_quote_checkout_date':'Quote check-out date; interpretation inferred, current source semantics unverified.',
 'price_quote_total_price':'Quote total amount; components/fees unverified. Inferred from name.',
 'price_quote_price_per_night':'Quoted nightly amount; fee basis unverified. Inferred from name.',
 'price_quote_raw':'Raw quote payload; schema/semantics unverified.',
 'minimum_nights':'Minimum permitted stay length in nights.',
 'maximum_nights':'Maximum permitted stay length in nights; large values may mean effectively unrestricted.',
 'minimum_minimum_nights':'Smallest minimum-stay rule in the forward calendar.',
 'maximum_minimum_nights':'Largest minimum-stay rule in the forward calendar.',
 'minimum_maximum_nights':'Smallest maximum-stay rule in the forward calendar.',
 'maximum_maximum_nights':'Largest maximum-stay rule in the forward calendar.',
 'minimum_nights_avg_ntm':'Average forward-calendar minimum stay in nights.',
 'maximum_nights_avg_ntm':'Average forward-calendar maximum stay in nights.',
 'calendar_updated':'Legacy calendar-update field; an empty column provides no update evidence.',
 'has_availability':'Listing-level availability flag.',
 'calendar_last_scraped':'Calendar collection date.',
 'number_of_reviews':'Lifetime review count reported at the snapshot.',
 'number_of_reviews_ltm':'Review count over the preceding twelve months.',
 'number_of_reviews_l30d':'Review count over the preceding thirty days.',
 'number_of_reviews_ly':'Likely previous-year review count; precise period unverified.',
 'availability_eoy':'Likely available nights until year-end; exact cutoff unverified.',
 'estimated_occupancy_l365d':'Source-modelled occupancy over trailing 365 days; units/formula unverified for this export.',
 'estimated_revenue_l365d':'Source-modelled trailing-year revenue; not observed transaction revenue.',
 'first_review':'Earliest observed review date for the listing.',
 'last_review':'Most recent observed review date for the listing.',
 'license':'Reported registration/permit text; not independently verified.',
 'instant_bookable':'Whether booking can be made without manual host acceptance.',
 'reviews_per_month':'Average observed review frequency per month over listing review history.',
 'reviewer_id':'Reviewer account identifier; not a measure.',
 'reviewer_name':'Displayed reviewer name; not a stable key.',
 'comments':'Free-text review content; no per-review rating field is supplied here.',
 'available':'Calendar availability flag: unavailable does not prove a booking.',
 'date':'Review publication date in reviews; prospective stay date in calendar.',
 'geometry_type':'GeoJSON geometry class.',
 'geometry_coordinates':'Serialized polygon coordinates; geographic shape, not a numeric business measure.',
}


def meaning(field):
    if field in DEFINITIONS:
        return DEFINITIONS[field]
    if field.startswith('availability_'):
        return f'Count of available nights in the next {field.rsplit("_",1)[1]} days, not confirmed bookings.'
    if field.startswith('review_scores_'):
        return f'Listing-level aggregate review score for {field[14:]}; not an individual review rating.'
    if field.startswith('calculated_host_listings_count'):
        suffix=field.removeprefix('calculated_host_listings_count').strip('_')
        return 'Host listing count within the current regional scrape' + (f', restricted to {suffix.replace("_"," ")}' if suffix else '') + '.'
    if field.startswith('hosts_time_as_'):
        return 'Reported tenure as ' + field.removeprefix('hosts_time_as_').replace('_',' ') + '; inferred from name; exact derivation unverified.'
    return 'Unmapped field; interpretation requires source confirmation.'


def kind(field):
    if field in IDS: return 'identifier'
    if field in DATE_FIELDS: return 'date'
    if field in BOOL: return 'boolean'
    if field in NUMERIC or field.startswith(('review_scores_','calculated_host_listings_count','availability_','hosts_time_as_')): return 'numeric'
    return 'text'


def sha(path, compressed=False):
    h=hashlib.sha256()
    with (gzip.open(path,'rb') if compressed else path.open('rb')) as f:
        for block in iter(lambda:f.read(4*1024*1024), b''): h.update(block)
    return h.hexdigest()


def weighted_quantile(values, weights, q):
    """Exact linear percentile of the expanded finite numeric population."""
    n=int(weights.sum())
    rank=(n-1)*q
    lo,hi=math.floor(rank),math.ceil(rank)
    cumulative=np.cumsum(weights)
    a=values[np.searchsorted(cumulative,lo,side='right')]
    b=values[np.searchsorted(cumulative,hi,side='right')]
    return float(a+(b-a)*(rank-lo))


def numeric_profile(field, pairs):
    raw=pd.Series([p[0] for p in pairs], dtype='str')
    text=raw.str.replace(r'[$€£,%]','',regex=True).str.replace(',','',regex=False)
    converted=pd.to_numeric(text,errors='coerce').to_numpy(dtype=float,na_value=np.nan)
    weights=np.array([p[1] for p in pairs],dtype=np.int64)
    good=np.isfinite(converted)
    result={'parse_failures':int(weights[~good].sum()),'numeric_count':int(weights[good].sum())}
    if not good.any(): return result
    v,w=converted[good],weights[good]
    order=np.argsort(v); v,w=v[order],w[order]
    n=int(w.sum()); mean=float(np.average(v,weights=w))
    q1,q2,q3=(weighted_quantile(v,w,q) for q in [.25,.5,.75])
    iqr=q3-q1; lower=q1-1.5*iqr; upper=q3+1.5*iqr
    result.update(mean=mean,median=q2,min=float(v[0]),max=float(v[-1]),q1=q1,q3=q3,
                  std=float(np.sqrt(np.sum(w*(v-mean)**2)/(n-1))) if n>1 else None,
                  iqr_lower=lower,iqr_upper=upper,
                  outlier_count=int(w[(v<lower)|(v>upper)].sum()),
                  outlier_rule='Tukey 1.5×IQR; potential extremes, not automatic errors',
                  zero_count=int(w[v==0].sum()),negative_count=int(w[v<0].sum()))
    # Semantic checks are separate from statistical extremes.
    invalid=np.zeros(len(v), dtype=bool)
    rule=''
    if field=='latitude': invalid=(v < -90)|(v>90); rule='latitude outside [-90,90]'
    elif field=='longitude': invalid=(v < -180)|(v>180); rule='longitude outside [-180,180]'
    elif field in {'host_response_rate','host_acceptance_rate'}: invalid=(v<0)|(v>100); rule='percentage outside [0,100]'
    elif field.startswith('review_scores_'): invalid=(v<0)|(v>5); rule='score outside assumed [0,5]; confirm export scale'
    elif field in {'minimum_nights','maximum_nights','accommodates'}: invalid=v<1; rule='value below 1'
    elif field.startswith('availability_') and field[13:].isdigit(): invalid=(v<0)|(v>int(field[13:])); rule='available nights outside window'
    else: invalid=v<0; rule='negative count/amount (candidate domain check)'
    result.update(domain_rule=rule,domain_flag_count=int(w[invalid].sum()))
    return result


def profile(path, out, chunksize):
    print(f'Profiling {path.name} ...',flush=True)
    geo=path.suffix=='.geojson'
    if geo:
        obj=json.loads(path.read_text(encoding='utf-8'))
        records=[]
        for f in obj['features']:
            records.append({**f['properties'],'geometry_type':f['geometry']['type'],
                            'geometry_coordinates':json.dumps(f['geometry']['coordinates'],separators=(',',':'))})
        chunks=[pd.DataFrame(records).fillna('').astype(str)]
    else:
        chunks=pd.read_csv(path,dtype=str,keep_default_na=False,chunksize=chunksize,encoding='utf-8-sig')
    summary={'file':path.name,'sha256':sha(path),'bytes':path.stat().st_size,'rows':0,'fields':[]}
    nulls=Counter(); whitespace=Counter(); row_problems=Counter()
    listing_ids=set(); retained={}
    with tempfile.TemporaryDirectory(prefix='bi-profile-') as tmp:
        con=sqlite3.connect(str(Path(tmp)/'counts.sqlite'))
        con.execute('PRAGMA journal_mode=OFF'); con.execute('PRAGMA synchronous=OFF')
        con.execute('PRAGMA cache_size=-65536')
        con.execute('CREATE TABLE hist(field TEXT,value TEXT,n INTEGER,PRIMARY KEY(field,value)) WITHOUT ROWID')
        columns=[]
        for chunk in chunks:
            columns=list(chunk.columns); summary['rows']+=len(chunk)
            for col in columns:
                s=chunk[col].fillna('')
                nulls[col]+=int(s.eq('').sum())
                whitespace[col]+=int((s.ne('') & s.str.strip().eq('')).sum())
                vc=s[s.ne('')].value_counts()
                con.executemany('INSERT INTO hist VALUES(?,?,?) ON CONFLICT(field,value) DO UPDATE SET n=n+excluded.n',
                                ((col,str(v),int(n)) for v,n in vc.items()))
            grain=GRAINS.get(path.name)
            if grain:
                keys=pd.Series([json.dumps(row,ensure_ascii=False) for row in chunk[grain].itertuples(index=False,name=None)],dtype='str') if len(grain)>1 else chunk[grain[0]]
                vc=keys.value_counts()
                con.executemany('INSERT INTO hist VALUES(?,?,?) ON CONFLICT(field,value) DO UPDATE SET n=n+excluded.n',
                                (('__grain__',str(v),int(n)) for v,n in vc.items()))
            if 'listing_id' in chunk: listing_ids.update(chunk['listing_id'].unique())
            if path.name.startswith('listings'):
                listing_ids.update(chunk['id'].unique())
            if {'minimum_nights','maximum_nights'} <= set(columns):
                mn=pd.to_numeric(chunk.minimum_nights,errors='coerce'); mx=pd.to_numeric(chunk.maximum_nights,errors='coerce')
                row_problems['minimum_exceeds_maximum']+=int((mn>mx).sum())
            if path.name=='listings.extracted.csv':
                for metric in ['id','neighbourhood_group_cleansed','neighbourhood_cleansed','room_type','property_type',
                               'host_id','accommodates','price','number_of_reviews','reviews_per_month',
                               'availability_365','review_scores_rating','last_scraped','first_review','last_review']:
                    retained.setdefault(metric,[]).extend(chunk[metric].tolist())
            con.commit()
        if GRAINS.get(path.name):
            summary['grain']=GRAINS[path.name]
            summary['duplicate_grain_extra_rows']=int(con.execute("SELECT coalesce(sum(n-1),0) FROM hist WHERE field='__grain__'").fetchone()[0])
        else:
            summary['grain_note']='Summary reviews has only listing/date; repeats can be distinct reviews on the same day. No review identifier for duplicate-event determination.' if path.name=='reviews.csv' else 'GeoJSON feature grain.'
        for col in columns:
            typ=kind(col); n=summary['rows']
            distinct=int(con.execute('SELECT count(*) FROM hist WHERE field=?',(col,)).fetchone()[0])
            f={'column':col,'meaning':meaning(col),'type':typ,'rows':n,'missing':nulls[col],
               'missing_pct':round(100*nulls[col]/n,4) if n else 0,
               'whitespace_only':whitespace[col],'distinct_nonmissing':distinct,
               'mean':None,'median':None,'stat_note':'Not applicable to text, dates, or identifiers.',
               'interpretation_status':'Inference; exact current source semantics unverified' if ('unverified' in meaning(col) or col.startswith('estimated_')) else 'Source-informed interpretation; see sources and caveats.'}
            if typ=='numeric':
                pairs=con.execute('SELECT value,n FROM hist WHERE field=?',(col,)).fetchall()
                f.update(numeric_profile(col,pairs)); f['stat_note']='Full-data finite numeric values; blanks excluded. Currency/percent symbols and thousands commas stripped; rates in percentage points.'
            elif typ=='date':
                pairs=con.execute('SELECT value,n FROM hist WHERE field=?',(col,)).fetchall()
                vals=pd.to_datetime(pd.Series([p[0] for p in pairs],dtype='str'),errors='coerce',format='%Y-%m-%d')
                valid=vals.notna()
                f.update(date_min=str(vals[valid].min().date()) if valid.any() else None,
                         date_max=str(vals[valid].max().date()) if valid.any() else None,
                         date_parse_failures=sum(p[1] for p,g in zip(pairs,valid) if not g))
                if valid.any(): f['span_days']=int((vals[valid].max()-vals[valid].min()).days)
            elif typ=='boolean':
                pairs=dict(con.execute('SELECT value,n FROM hist WHERE field=?',(col,)))
                f['invalid_boolean_count']=sum(n for v,n in pairs.items() if v not in {'t','f','true','false','1','0'})
                f['stat_note']='Boolean categories; use true/false counts rather than an arithmetic mean.'
            if col not in PRIVATE_TEXT and col!='geometry_coordinates':
                limit=50 if distinct<=50 else 10
                f['values']=[{'value':v,'count':int(c)} for v,c in con.execute('SELECT value,n FROM hist WHERE field=? ORDER BY n DESC,value LIMIT ?',(col,limit))]
                f['values_note']='All nonempty categories' if distinct<=50 else 'Top 10 values; exact distinct count covers full file'
            else:
                f['values_note']='Distinct count computed exactly; individual free-text/name/URL/geometry values omitted to keep output compact.'
            assert 0 <= f['missing'] <= n
            assert f['distinct_nonmissing'] <= n-f['missing']
            summary['fields'].append(f)
        con.close()
    summary['row_checks']=dict(row_problems)
    summary['unique_listing_ids']=len(listing_ids)
    print(f'  {summary["rows"]:,} rows, {len(columns)} fields',flush=True)
    return summary,listing_ids,retained


def table(headers, rows):
    return '<table><thead><tr>'+''.join(f'<th>{html.escape(str(h))}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table>'


def fmt(v):
    if v is None: return 'N/A'
    if isinstance(v,(int,np.integer)): return f'{v:,}'
    if isinstance(v,(float,np.floating)): return f'{v:,.3f}'
    return str(v)


def add_context_checks(out, raw):
    """Explain observed missingness and check selected published controls."""
    d=pd.read_csv(raw/'listings.extracted.csv',dtype=str,keep_default_na=False)
    n=pd.to_numeric(d.number_of_reviews,errors='coerce')
    conditional={}
    for col in ['review_scores_rating','first_review','last_review','reviews_per_month']:
        blank=d[col].eq('')
        conditional[col]={'blank':int(blank.sum()),'blank_with_zero_reviews':int((blank & n.eq(0)).sum()),
                          'blank_with_positive_reviews':int((blank & n.gt(0)).sum())}
    profile_path=out/'profile.json'
    obj=json.loads(profile_path.read_text(encoding='utf-8'))
    obj['conditional_missingness']=conditional
    geo=json.loads((raw/'neighbourhoods.geojson').read_text(encoding='utf-8'))
    geo_keys={(f['properties'].get('neighbourhood_group'),f['properties'].get('neighbourhood')) for f in geo['features']}
    obj['geojson_feature_count']=len(geo['features'])
    obj['geojson_distinct_geography_keys']=len(geo_keys)
    listing_geo=set(map(tuple,d[['neighbourhood_group_cleansed','neighbourhood_cleansed']].to_numpy()))
    obj['listing_geography_pairs_not_in_geojson']=len(listing_geo-geo_keys)
    ls=next(s for s in obj['datasets'] if s['file']=='listings.extracted.csv')
    price=next(f for f in ls['fields'] if f['column']=='price')
    v=pd.to_numeric(d.price.str.replace(r'[$€,]','',regex=True),errors='coerce')
    assert ls['rows']==len(d) and ls['duplicate_grain_extra_rows']==int(d.id.duplicated().sum())
    assert np.isclose(price['mean'],v.mean()) and np.isclose(price['median'],v.median())
    assert price['missing']==int(d.price.eq('').sum())
    q1,q3=v.quantile([.25,.75])
    assert price['outlier_count']==int(((v<q1-1.5*(q3-q1))|(v>q3+1.5*(q3-q1))).sum())
    review_file=raw/'reviews.extracted.csv'
    review_ids=pd.read_csv(review_file,usecols=['id'],dtype=str,keep_default_na=False)['id']
    duplicate_ids=set(review_ids[review_ids.duplicated(keep=False)])
    audit={'duplicate_id_extra_rows':int(review_ids.duplicated().sum()),'distinct_repeated_ids':len(duplicate_ids),
           'exact_duplicate_extra_rows':0,'ids_with_conflicting_rows':0}
    if duplicate_ids:
        pieces=[]
        for chunk in pd.read_csv(review_file,dtype=str,keep_default_na=False,chunksize=100_000):
            matched=chunk[chunk.id.isin(duplicate_ids)]
            if len(matched): pieces.append(matched)
        repeated=pd.concat(pieces,ignore_index=True)
        distinct_rows=repeated.drop_duplicates()
        audit['exact_duplicate_extra_rows']=int(repeated.duplicated().sum())
        audit['ids_with_conflicting_rows']=int((distinct_rows.groupby('id').size()>1).sum())
    obj['review_duplicate_audit']=audit
    obj['independent_listing_controls_passed']=True
    profile_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    note='## Observed conditional missingness and rule conflicts\n\n'
    for col,c in conditional.items():
        note+=f'- {col}: {c["blank"]:,} blanks; {c["blank_with_zero_reviews"]:,} have zero reviews and {c["blank_with_positive_reviews"]:,} have positive reviews.\n'
    note+='These observed associations support treating review-related missing values separately from general data loss; they do not justify inventing a zero score.\n'
    note+=f'- Detailed reviews: {audit["duplicate_id_extra_rows"]:,} extra rows repeat review IDs, involving {audit["distinct_repeated_ids"]:,} repeated IDs. Of these, {audit["exact_duplicate_extra_rows"]:,} are exact duplicate rows across all fields; {audit["ids_with_conflicting_rows"]:,} IDs have conflicting row variants. These remain in raw inputs and raw statistics; define and document a deduplication policy before fact loading.\n'
    note+=f'- GeoJSON: {len(geo["features"]):,} geometry features, {len(geo_keys):,} distinct geography keys; {len(listing_geo-geo_keys):,} listing geography pairs lack a GeoJSON key. Multiple shapes with the same key do not automatically represent additional neighbourhoods.\n'
    for ds in obj['datasets']:
        for check,count in ds.get('row_checks',{}).items():
            note+=f'- {ds["file"]}: {check} = {count:,} rows. Investigate flagged source records before choosing a correction.\n'
    note+='\nIndependent direct pandas calculations matched listing rows, duplicate IDs, price missing count, mean, median, and IQR outlier count.\n'
    report_path=out/'report.md'
    report=report_path.read_text(encoding='utf-8')
    marker='## Observed conditional missingness and rule conflicts'
    if marker in report:
        start=report.index(marker); end=report.index('## Recommended next step',start)
        report=report[:start]+report[end:]
    report=report.replace('## Recommended next step',note+'\n## Recommended next step')
    report_path.write_text(report,encoding='utf-8')
    render_explorer(out, obj['datasets'], report)


def render_explorer(out, summaries, findings):
    sections=[]
    for ds in summaries:
        rows=[]
        for f in ds['fields']:
            values='; '.join(f'{p["value"]}: {p["count"]:,}' for p in f.get('values',[])) or f['values_note']
            rows.append([f['column'],f['meaning'],f['type'],fmt(f['missing']),fmt(f['missing_pct'])+'%',fmt(f['distinct_nonmissing']),
                         fmt(f.get('mean')),fmt(f.get('median')),fmt(f.get('min')),fmt(f.get('max')),fmt(f.get('outlier_count')),
                         (f.get('date_min') or '')+' '+(f.get('date_max') or ''),values,f['stat_note']])
        sections.append(f'<h2>{html.escape(ds["file"])} · {ds["rows"]:,} rows</h2>'+table(['Feature','Interpretation','Type','Missing','Missing %','Distinct','Mean','Median','Min','Max','IQR flags','Date range','Values / counts','Stats note'],rows))
    display='''<!doctype html><html lang="en"><meta charset="utf-8"><title>BI Project · Raw data exploration</title>
<style>body{font:15px/1.5 system-ui;margin:32px;color:#182b40;background:#f7f9fc}h1,h2{color:#173f59}table{border-collapse:collapse;background:white;margin:20px 0;display:block;overflow:auto;max-height:75vh}td,th{border:1px solid #d6e1eb;padding:9px;min-width:95px;max-width:400px;vertical-align:top;overflow-wrap:anywhere}th{background:#e4eef4;position:sticky;top:0;cursor:pointer}input{padding:12px;width:min(650px,90%);position:sticky;top:0;z-index:4}pre{white-space:pre-wrap;background:white;padding:22px;border-radius:10px;max-width:1100px}.hint{color:#52667a}</style>
<h1>BI Project · Raw data exploration</h1><p>All rows profiled. Originals preserved. Local EDA; Fabric compliance remains unverified.</p>
<p class="hint">Search filters field rows. Click a column heading to sort. Mean and median are N/A for text, dates, identifiers, and booleans. Potential IQR outliers are not proven errors.</p>
<input id="search" placeholder="Search features, meanings, or values…" aria-label="Search features">
'''+''.join(sections)+'<h2>Readiness and interpretation</h2><pre>'+html.escape(findings)+'''</pre>
<script>document.querySelector('#search').addEventListener('input',e=>{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))});document.querySelectorAll('th').forEach(th=>th.onclick=()=>{let t=th.closest('table'),i=th.cellIndex,a=[...t.tBodies[0].rows];th.asc=!th.asc;a.sort((x,y)=>{let u=x.cells[i].textContent,v=y.cells[i].textContent,n=Number(u.replaceAll(',','').replace('%','')),m=Number(v.replaceAll(',','').replace('%',''));return (Number.isFinite(n)&&Number.isFinite(m)?n-m:u.localeCompare(v))*(th.asc?1:-1)});a.forEach(r=>t.tBodies[0].append(r))});</script></html>'''
    (out/'report.html').write_text(display,encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--chunksize',type=int,default=100_000)
    args=parser.parse_args(); root=args.project.resolve(); raw=root/'data/raw'
    out=args.output or root/'outputs/raw-data-analysis'; out.mkdir(parents=True,exist_ok=True)
    before={p.name:sha(p) for p in raw.iterdir() if p.is_file()}
    inputs=sorted(raw.glob('*.csv'))+sorted(raw.glob('*.geojson'))
    summaries=[]; ids={}; details={}
    for path in inputs:
        summary,keys,retained=profile(path,out,args.chunksize)
        summaries.append(summary); ids[path.name]=keys
        if retained: details=retained
    # Confirm gzip files are exact wrappers of the extracted CSV, not new datasets.
    archive_checks=[]
    for p in sorted(raw.glob('*.csv.gz')):
        extracted=p.with_name(p.name[:-7]+'.extracted.csv')
        match=extracted.exists() and sha(p,compressed=True)==before[extracted.name]
        archive_checks.append({'archive':p.name,'extracted':extracted.name,'decompressed_sha256_matches':match})
        assert match, f'Archive/extraction mismatch: {p.name}'
    byfile={s['file']:s for s in summaries}
    listing_keys=ids.get('listings.extracted.csv',set())
    relations={k:len(v-listing_keys) for k,v in ids.items() if k in ['calendar.extracted.csv','reviews.csv','reviews.extracted.csv','listings.csv']}
    data=pd.DataFrame(details)
    geography_pairs=data[['neighbourhood_group_cleansed','neighbourhood_cleansed']].drop_duplicates()
    geo_ambiguity=int((geography_pairs.groupby('neighbourhood_cleansed')['neighbourhood_group_cleansed'].nunique()>1).sum())
    # Summary-review and detailed-review dates/counts are compared separately; no double counting.
    overall={'generated_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
             'pandas':pd.__version__,'numpy':np.__version__,'sources':{'data':SOURCE,'dictionary':DICTIONARY,'assumptions':ASSUMPTIONS},
             'datasets':summaries,'archive_checks':archive_checks,'orphan_listing_ids':relations,
             'neighbourhood_names_in_multiple_groups':geo_ambiguity,
             'method':'Full files; exact raw nonempty distinct values; empty CSV fields are missing; whitespace-only counted separately. No blanket NA-token replacement. Numeric percent values use 0–100. Exact linear weighted quantiles; 1.5×IQR flags are not proof of errors. Identifiers remain strings.',
             'raw_sha256':before}
    # Cross-file geographic key coverage.
    neighbourhood=pd.read_csv(raw/'neighbourhoods.csv',dtype=str,keep_default_na=False)
    geo_keys=set(map(tuple,neighbourhood[['neighbourhood_group','neighbourhood']].to_numpy()))
    listing_geo=set(map(tuple,geography_pairs.to_numpy()))
    overall['listing_geography_pairs_not_in_neighbourhoods']=len(listing_geo-geo_keys)
    for col in ['price','number_of_reviews','reviews_per_month','availability_365','review_scores_rating','accommodates']:
        data[col]=pd.to_numeric(data[col].str.replace(r'[$€,]','',regex=True),errors='coerce')
    business=[]
    for name,g in data.groupby('room_type',dropna=False):
        business.append({'room_type':name,'listings':len(g),'mean_price':g.price.mean(),'median_price':g.price.median(),
                         'mean_rating':g.review_scores_rating.mean(),'median_availability_365':g.availability_365.median()})
    pd.DataFrame(business).to_csv(out/'room_type_summary.csv',index=False)
    data.groupby('neighbourhood_group_cleansed').agg(listings=('id','size'),median_price=('price','median'),
        mean_price=('price','mean'),median_rating=('review_scores_rating','median')).reset_index().to_csv(out/'geography_summary.csv',index=False)
    # Temporal concentration for reviews: computed in a bounded second pass.
    years=Counter()
    for chunk in pd.read_csv(raw/'reviews.extracted.csv',usecols=['date'],dtype=str,chunksize=args.chunksize,keep_default_na=False):
        years.update(chunk.date.str[:4].value_counts().to_dict())
    overall['reviews_by_year']=dict(sorted(years.items()))
    pd.DataFrame([{'year':y,'reviews':n} for y,n in sorted(years.items())]).to_csv(out/'reviews_by_year.csv',index=False)
    after={p.name:sha(p) for p in raw.iterdir() if p.is_file()}
    assert before==after, 'Raw inputs changed during profiling'
    overall['raw_unchanged_verified']=True
    (out/'profile.json').write_text(json.dumps(overall,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    records=[]
    for ds in summaries:
        for f in ds['fields']:
            records.append({'file':ds['file'],**{k:v for k,v in f.items() if k not in ['values']}})
    pd.DataFrame(records).to_csv(out/'column_profile.csv',index=False)
    # Compact markdown report plus an interactive, self-contained HTML field explorer.
    def field(file,col): return next(f for f in byfile[file]['fields'] if f['column']==col)
    caldate=field('calendar.extracted.csv','date'); revdate=field('reviews.extracted.csv','date')
    dsrows=[[s['file'],s['rows'],len(s['fields']),s.get('duplicate_grain_extra_rows','N/A')] for s in summaries]
    allmissing=[f"{s['file']}: {f['column']}" for s in summaries for f in s['fields'] if f['missing']==s['rows']]
    highmissing=sorted([(s['file'],f['column'],f['missing_pct']) for s in summaries for f in s['fields'] if f['missing_pct']>0],key=lambda r:r[2],reverse=True)
    ls='listings.extracted.csv'
    findings=f'''# Raw data exploration and BI I readiness

Generated from all rows, without sampling. Inputs and source references are recorded in profile.json. Raw file hashes were unchanged after analysis. This is local exploratory evidence, not Fabric implementation or teacher approval.

## Verdict
**Conditionally useful, but not compliant as supplied.** Listings are within the 30k source limit; the calendar and reviews are far larger and need a documented, linked sampling/aggregation plan. Reviews provide historical events, but not booking/payment transactions or per-review prices/ratings. Calendar is a prospective availability snapshot, not actual booking history. At least two distinct primitive measures and five genuine three-level hierarchies are not yet established for one defensible fact grain. Confirm this analytical scope with the lab teacher before committing to the model.

## File inventory
| File | Rows/features | Fields | Duplicate grain extra rows |
|---|---:|---:|---:|
'''
    findings+='\n'.join('| '+' | '.join(map(fmt,r))+' |' for r in dsrows)
    findings+=f'''

Gzip originals exactly match their extracted CSV payloads. Do not count them as extra sources. Summary and detailed listings/reviews represent overlapping entities/events; do not append them into a single fact table without reconciliation. Uniqueness of summary review events cannot be established from listing/date alone.

## Time and relationships
- Review dates: {revdate.get('date_min')} to {revdate.get('date_max')} ({revdate.get('span_days'):,} days): historical coverage exceeds one year.
- Calendar dates: {caldate.get('date_min')} to {caldate.get('date_max')} ({caldate.get('span_days'):,} days): forward-looking calendar coverage, not multi-year observed transactions. Crossing calendar years does not prove more than one year of history.
- Listing scrape dates: {field(ls,'last_scraped').get('date_min')} to {field(ls,'last_scraped').get('date_max')}; geography labels indicate the Lisbon region, not just the municipality.
- Distinct listing IDs without a detailed listing: {json.dumps(relations)}. These counts describe missing keys, not orphan row counts.
- Listing geography pairs absent from neighbourhoods.csv: {overall['listing_geography_pairs_not_in_neighbourhoods']}.
- Neighbourhood labels used in multiple groups: {geo_ambiguity}. Use a compound geography key where needed.

## Numeric snapshot
| Detailed listings feature | Missing % | Mean | Median | Min | Max | IQR flags |
|---|---:|---:|---:|---:|---:|---:|
'''
    for col in ['price','accommodates','bedrooms','beds','minimum_nights','maximum_nights','number_of_reviews','reviews_per_month','availability_365','review_scores_rating']:
        f=field(ls,col)
        findings+='\n| '+' | '.join(fmt(v) for v in [col,f['missing_pct'],f.get('mean'),f.get('median'),f.get('min'),f.get('max'),f.get('outlier_count')])+' |'
    findings+='\n\n## Missingness and potential outliers\n\nAll-empty fields: '+', '.join(allmissing)+'.\n\nLargest missing shares:\n'
    findings+='\n'.join(f'- {file} / {col}: {pct:.2f}%.' for file,col,pct in highmissing[:15])
    findings+='''

Do not fill every blank with zero. Missing prices prevent price-based analysis; blank ratings/review dates can reflect no reviews, whereas host rates and legacy export fields need source-specific interpretation. No blank is asserted structurally inapplicable without supporting evidence. IQR flags identify unusual observations, not proven errors: expensive homes, high-volume hosts, and long-stay rules may be legitimate. Zero-IQR distributions can flag all non-modal observations. Review semantic checks, units, and business purpose before capping or dropping anything. Detailed per-field parse failures, domain flags, quartiles, distinct counts, and values appear in the HTML/CSV/JSON profiles.

## Assignment fit
| Criterion | Assessment |
|---|---|
| Source provenance / eligibility | Real public-data source, not one of the prohibited teaching databases. Preserve attribution and confirm teacher acceptance of the business scenario. Download date and exact historical URL of local files have not been supplied. |
| Source row limits | Detailed listings 25,020 meet the ≤30k cap. See inventory for all other files: calendar and review datasets exceed it. Keep originals intact and prepare derived, linked samples outside raw. |
| Minimum fact rows | Large event volumes are available, but final fact grain and valid sampled rows must still demonstrate ≥10k source facts (p.2) and ≥5k DW facts (p.4). |
| More than one year history | Reviews meet date coverage; listings are a current snapshot; calendar is prospective, not historical transactions. |
| ≥5 dimensions including Date | Candidate Date, Listing, Host, Geography, Accommodation Type can be designed. Host/type separation and keys require design; reviewer attributes are sparse. Dimensions are not yet implemented. |
| ≥5 hierarchies, average depth 3 | Not demonstrated. Date year→quarter→month→day and Geography country→municipality→neighbourhood are plausible. Additional attributes/groupings must be justified, not invented to inflate the count. |
| ≥2 distinct primitive measures | Not demonstrated at a historical transaction grain. Review count=1 is one event measure; date or IDs are not measures. Text length is derived, not a second primitive business measure. Price/capacity/stay rules exist at listing/calendar grains, not review-event prices. Estimated revenue/occupancy are modelled, not primitive transactions. |
| Varied sources and transformations | CSV plus GeoJSON enable joins, JSON/list parsing, currency/percent parsing, missing-value policy, and geography reconciliation. Summary/detailed exports are not independent business systems. |
| Fabric STG/DW, ETL and lab quality logging | Not verified by local EDA. Required Fabric pipelines, Copy Data/Dataflows, separate staging, four lab DQ checks, successful execution, and delivery access remain separate work. |

## Recommended next step
Choose the business questions and fact grain before sampling. If using reviews, stratify across years and relevant geographic/listing groups, retain ≥10k valid events, and keep every selected event's listing/host/geography lookup. Do not randomly sample related files independently. For availability analysis, consider a separate listing-day snapshot fact, clearly labelled as prospective. Obtain teacher agreement on primitive measures and hierarchies; supplement eligible source data if needed. Do not claim real occupancy or revenue from unavailable nights.

## Methods and reproducibility
Run `python scripts/profile_raw_data.py` from the project. Tested with Python, pandas 3.0.1 and numpy 2.3.5; versions are captured in profile.json. The script reads full files in 100,000-row chunks, builds temporary on-disk exact frequency tables, and removes scratch tables after use. Exact distinct counts exclude empty fields; whitespace-only counts are separate, and NA-like text is not silently converted. Mean/median use finite parsed numeric values only; numeric IDs remain strings. Percentages are 0–100; currency symbols do not establish currency. Quantiles use linear interpolation over the full weighted frequency distribution. All statistical results are unsampled. Existing generated analysis files in the output folder are replaced on rerun.

Outputs: report.md, report.html, column_profile.csv, profile.json, room_type_summary.csv, geography_summary.csv, reviews_by_year.csv. Each field's meaning is source-informed or explicitly labelled as an unverified inference; the linked public dictionary is version 4.3 (2022) and does not document every newer field in these local exports. No external service is required to rerun this local profiler. It is not the submitted Fabric ETL.

## Sources
- Assignment: docs/source/BI I Project Guide 2026-2027 v1.1.pdf, pp.2–6 and 9.
- [Inside Airbnb data catalogue](https://insideairbnb.com/get-the-data/): file roles and licence; consulted 20 October 2026. Attribute Inside Airbnb under the listed CC BY 4.0 licence.
- [Inside Airbnb data dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit): field context, legacy version; consulted 20 October 2026. Explanations here are analytical interpretations, not a copied dictionary.
- [Inside Airbnb assumptions](https://insideairbnb.com/data-assumptions/): collection/snapshot and availability caveats; consulted 20 October 2026. Unavailable nights cannot distinguish bookings from blocks; locations are approximate; modelled estimates are not actual transaction records.
'''
    # Do not freeze the listing count in narrative when rerunning a different snapshot.
    findings=findings.replace('Detailed listings 25,020',f'Detailed listings {byfile[ls]["rows"]:,}')
    (out/'report.md').write_text(findings,encoding='utf-8')
    render_explorer(out, summaries, findings)
    add_context_checks(out, raw)
    print(f'Saved analysis to {out}',flush=True)


if __name__=='__main__':
    main()
