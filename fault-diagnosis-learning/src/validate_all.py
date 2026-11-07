"""Check published documents and navigation; never train or inspect user data."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit
import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / 'fault-diagnosis-learning'
UPDATE = ROOT / 'research-update-2026-11'
REPORT = ROOT / 'REPOSITORY_CHECK.json'


def heading_ids(text):
    ids=set();counts={};in_code=False
    for line in text.splitlines():
        if line.startswith('```'):
            in_code=not in_code
            continue
        if in_code:continue
        m=re.match(r'^#{1,6}\s+(.+?)\s*#*$',line)
        if not m:continue
        title=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',m[1]).replace('`','').lower()
        slug=''.join(c for c in title if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ','-')
        n=counts.get(slug,0);counts[slug]=n+1
        ids.add(slug+(f'-{n}' if n else ''))
    ids.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)',text))
    return ids


def repository_checks():
    raw=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=REPO)
    files=sorted({REPO/p for p in raw.decode().split('\0') if p})
    mds=[p for p in files if p.suffix=='.md']
    local=anchors=external=0
    for p in mds:
        for value in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            u=urlsplit(value)
            if u.scheme:
                assert u.scheme in ('http','https') and u.hostname and not u.username and not u.password,(p,value)
                external+=1;continue
            q=(p.parent/unquote(u.path)).resolve() if u.path else p
            assert q==REPORT or q.exists(),('missing local link',p,value)
            local+=1
            if u.fragment and q.suffix=='.md':
                assert unquote(u.fragment) in heading_ids(q.read_text()),('missing heading',p,value)
                anchors+=1
    pdfs=[p for p in files if p.suffix=='.pdf'];books=[p for p in files if p.suffix=='.xlsx']
    assert len(pdfs)==14 and len(books)==6
    expected={
        'data_manifest_template.csv':{'record_id','group_id','file_sha256','split','sample_rate_hz'},
        'window_manifest_template.csv':{'window_id','record_id','group_id','file_sha256','channel','start_sample','end_sample_exclusive','sample_rate_hz','split','preprocessing_version'},
        'experiment_results_template.csv':{'experiment_id','evaluation_split','protocol_version','split_hash','macro_f1'},
        'feature_candidates_template.csv':{'feature_id','formula','discovery_record_ids','selection_split','frozen_at','implementation_version'},
        'literature_review_template.csv':{'entry_id','catalog_namespace','retrieved_level','claim_to_support','source_location'},
    }
    guide=(UPDATE/'模板填写指南.md').read_text();schemas={}
    assert set(p.name for p in UPDATE.glob('*_template.csv'))==set(expected)
    for name,required in expected.items():
        with (UPDATE/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.reader(f))
        assert len(rows)==1 and len(rows[0])==len(set(rows[0])),name
        assert required<=set(rows[0]),name
        assert all(field in guide for field in rows[0]),('undocumented field',name)
        schemas[name]=rows[0]
    protocol=json.loads((UPDATE/'experiment_protocol_template.json').read_text())
    assert protocol['status']=='template_not_executed' and protocol['locked_at'] is None
    assert all(k in guide for k in protocol), 'undocumented protocol field'
    assert all(k in protocol for k in ['window_manifest','feature_manifest','literature_review_manifest','test_usage_log'])
    root_md=(REPO/'README.md').read_text();checklist=(UPDATE/'研究执行清单.md').read_text()
    for i in range(1,7):
        assert f'### 第{i}步：' in root_md and f'## 第{i}步：' in checklist
    assert '/local-research/' in (REPO/'.gitignore').read_text()
    protected=pdfs+books+[ROOT/'research-papers/catalog.json',ROOT/'references/catalog.json',ROOT/'feature-mining-progress/研究进展与任务书.md']
    return {'markdown_files':len(mds),'local_targets_checked':local,'heading_targets_checked':anchors,
            'external_urls_syntax_only':external,'pdf_count':len(pdfs),'xlsx_count':len(books),
            'template_schemas':schemas,'personal_experiments_checked':False,
            'artifact_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}}


def main():
    report={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'result':'running',
            'scope':'Published artifacts, navigation and blank templates; no live literature retrieval or model experiments',
            'checks':{},'commands':[]}
    try:
        report['checks']=repository_checks()
        # Other validators follow README links to this report on a fresh checkout.
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        for rel in ['src/validate_artifacts.py','src/validate_research.py','feature-mining-progress/validate_progress.py','src/validate_research_update.py']:
            result=subprocess.run([sys.executable,str(ROOT/rel)],cwd=REPO,text=True,capture_output=True)
            report['commands'].append({'script':str(Path('fault-diagnosis-learning')/rel),'returncode':result.returncode,'stdout':result.stdout.strip(),'stderr':result.stderr.strip()})
            print(rel, 'PASS' if result.returncode==0 else 'FAIL')
            if result.returncode:raise RuntimeError(f'{rel}: {result.stderr}')
        report['result']='passed'
    except Exception as error:
        report.update(result='failed',error=str(error))
        raise
    finally:
        report['finished_at_utc']=datetime.now(timezone.utc).isoformat()
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: repository navigation, six-step workflow, five CSV templates and all four artifact validators')


if __name__=='__main__':main()
