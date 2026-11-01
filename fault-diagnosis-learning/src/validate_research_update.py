"""Validate original research-update documents, not model performance."""
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import fitz
from build_research_update import ROOT, METHODS, UPDATE, FIELDS, cards, references


def norm(s):
    return re.sub(r'\s+', '', s).replace('\u200b','')


def main():
    cs=cards()
    expected_ids={c['id'] for c in cs}
    main_pdf=METHODS/'00_故障诊断深度学习方法详解_合订本.pdf'
    files=sorted(METHODS.glob('*.pdf'))+sorted(UPDATE.glob('*.pdf'))
    assert len(files)==11
    report={'validated_at':datetime.now(timezone.utc).isoformat(),
            'scope':'File, source and rendering consistency; no model experiments',
            'model_experiments_run':False,'methods':len(cs),'method_fields':FIELDS,'pdfs':[]}
    page_index={}
    for path in files:
        doc=fitz.open(path)
        toc=doc.get_toc()
        texts=[p.get_text() for p in doc]
        assert all(len(t.strip())>100 for t in texts),('empty page',path)
        assert all('\ufffd' not in t and '\x00' not in t for t in texts),path
        assert toc and doc.metadata['title'],path
        for i,p in enumerate(doc):
            for block in p.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        assert x0>=0 and y0>=0 and x1<=p.rect.width+0.1 and y1<=p.rect.height+0.1, (path,i,span)
            used={s['font'] for b in p.get_text('dict')['blocks'] for line in b.get('lines',[]) for s in line['spans']}
            embedded={font[3].split('+')[-1] for font in p.get_fonts() if doc.extract_font(font[0])[3]}
            assert used <= embedded,('unembedded used font',path,i,used,embedded)
        method_pages={}
        for _,title,pageno in toc:
            m=re.match(r'(M\d\d)｜',title)
            if m:method_pages[m[1]]=pageno
        selected=cs if path==main_pdf else [c for c in cs if path.stem==c['group']]
        if selected:
            assert set(method_pages)=={c['id'] for c in selected},path
            assert len(set(method_pages.values()))==len(selected),path
            for c in selected:
                text=norm(texts[method_pages[c['id']]-1])
                assert norm(c['title']) in text
                for key,value in c['fields'].items():
                    assert norm(value) in text,('missing card text',path,c['id'],key)
            if path==main_pdf:page_index=method_pages
            alltext=norm(''.join(texts))
            for line in references(selected).splitlines():
                if line.startswith('**'):
                    assert norm(line.replace('**','')) in alltext,('missing reference',path,line[:60])
        if path.parent==UPDATE:
            # Every authored paragraph/table cell must survive Markdown->PDF.
            alltext=norm(''.join(texts))
            for line in path.with_suffix('.md').read_text().splitlines():
                line=line.strip()
                if not line or re.fullmatch(r'[| :\-]+',line):continue
                for cell in (line.strip('|').split('|') if line.startswith('|') else [line]):
                    cleaned=re.sub(r'^#+\s*','',cell.strip()).replace('**','').replace('`','')
                    assert norm(cleaned) in alltext,('missing research text',path,cleaned[:60])
        report['pdfs'].append({'file':str(path.relative_to(ROOT)),'pages':len(doc),
                               'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                               'method_cards':len(selected),'bookmarks':len(toc)})
    with (METHODS/'方法索引.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==35 and {r['编号'] for r in rows}==expected_ids
    for c,row in zip(cs,rows):
        assert row['编号']==c['id'] and row['方法']==c['title'] and int(row['合订本页码'])==page_index[c['id']]
        assert row['分类']==c['group'] and row['来源说明']==c['fields']['来源']
        assert (METHODS/row['分册PDF']).is_file()
    source=json.loads((UPDATE/'SOURCE_RETRIEVAL.json').read_text())
    sources=source['sources'];assert len(sources)==25
    assert len({s['id'] for s in sources})==25
    successes=[s for s in sources if s['status']=='retrieved']
    failed=[s for s in sources if s['status']=='not_retrieved']
    assert len(successes)==20 and len(failed)==5
    assert sum(s['kind']=='selected_code' for s in successes)==3
    for s in successes:assert re.fullmatch('[0-9a-f]{64}',s['sha256']) and s['bytes']>0 and s['http_status']==200
    for s in failed:assert s['error'] and 'sha256' not in s
    assert source['full_papers_assessed']==0 and source['model_experiments_run'] is False
    report['sources']={'requests':25,'retrieved':20,'not_retrieved':5,'selected_code_files':3,'new_full_papers':0}
    # Check relative links in the new directories and navigation files.
    mds=list(METHODS.glob('*.md'))+list(UPDATE.glob('*.md'))+[ROOT.parent/'README.md',ROOT/'README.md',ROOT/'feature-mining-progress/README.md',ROOT/'src/README.md']
    links=0; external=0
    for md in mds:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',md.read_text()):
            if target.startswith(('http://','https://')):
                assert urlsplit(target).netloc;external+=1;continue
            if target.startswith('#'):continue
            local=unquote(target.split('#')[0])
            if not local:continue
            resolved=(md.parent/local).resolve()
            if resolved==UPDATE/'DOCUMENT_VALIDATION.json':continue
            assert resolved.exists(),(md,target)
            links+=1
    for filename in ['data_manifest_template.csv','experiment_results_template.csv']:
        with (UPDATE/filename).open(encoding='utf-8-sig',newline='') as f:r=list(csv.reader(f))
        assert len(r)==1 and len(r[0])==len(set(r[0]))
    protocol=json.loads((UPDATE/'experiment_protocol_template.json').read_text())
    assert protocol['status']=='template_not_executed' and protocol['locked_at'] is None
    archive=ROOT/'feature-mining-progress/研究进展与任务书.md'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()=='03d64ad39808fde2977d8af574f39cd251a50db7dd650a0fc29c09bd9118aa33'
    assert len(json.loads((ROOT/'research-papers/catalog.json').read_text()))==38
    report.update(local_links_checked=links,external_link_syntax_checked=external,archived_brief_unchanged=True,
                  versions={'python':sys.version.split()[0],'reportlab':importlib.metadata.version('reportlab'),'PyMuPDF':fitz.VersionBind})
    paths=[p for d in [METHODS,UPDATE] for p in d.iterdir() if p.is_file() and p.name!='DOCUMENT_VALIDATION.json']
    paths += [ROOT/'src/build_research_update.py',Path(__file__)]
    report['artifact_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    (UPDATE/'DOCUMENT_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 35 complete method cards; 11 searchable PDFs; CSV/bookmarks; 25 source records; templates; local links; archived brief')


if __name__=='__main__':main()
