"""Validate citation and document consistency; never run paper experiments."""
import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research-papers'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
GROUPS = [('深度学习', '01_深度学习科研论文.xlsx', 13),
          ('特征挖掘', '02_特征挖掘科研论文.xlsx', 13),
          ('融合与解释', '03_融合与解释科研论文.xlsx', 12)]
PAPER_KEYS = ['id','short_name','title','authors','year','journal','volume','issue','pages','type',
              'engineering_object','research_problem','method','citation_use','source_url','online_year',
              'priority','reading_status','publication_status']
RESOURCE_KEYS = ['id','short_name','reported_validation','suggested_experiment','limitations','reproduction',
                 'code_status','code_url','code_scope','data_status','data_url','verification','evidence_url',
                 'metadata_note','checked','run_status']

def column(i):
    result = ''
    while i:
        i, rem = divmod(i - 1, 26)
        result = chr(65 + rem) + result
    return result

def main():
    records = json.loads((OUT / 'catalog.json').read_text())
    meta = json.loads((OUT / 'source_metadata.json').read_text())
    assert len(records) == 38
    assert len({r['id'] for r in records}) == len({r['doi'].lower() for r in records}) == 38
    required = ['title','authors','journal','year','method','reported_validation','citation_use',
                'suggested_experiment','limitations','reproduction','verification','evidence_url']
    for r in records:
        assert all(r[k] for k in required), r['id']
        assert r['doi'].lower() == meta[r['id']]['DOI'].lower()
        assert r['run_status'] == '未运行论文实验'
        assert re.fullmatch(r'10\.\d{4,9}/\S+', r['doi'])
        assert not any(c in json.dumps(r, ensure_ascii=False) for c in ['\ufffd'])
    indexed = {r['id']: r for r in records}
    assert len(indexed['C02']['author_structured']) == 6 and indexed['C02']['pages'] == '65-76'
    assert len(indexed['C06']['author_structured']) == 6 and 'Guang Meng' in indexed['C06']['authors']
    assert indexed['F11']['year'] == 2024 and indexed['F11']['online_year'] == 2023
    assert indexed['C12']['publication_status'] == '期刊在线预校样（In Press）'
    assert indexed['C12']['volume'] == ''

    with (OUT / '工程科研论文.csv').open(encoding='utf-8-sig', newline='') as f:
        csv_rows = list(csv.DictReader(f))
    assert len(csv_rows) == 38
    for r, row in zip(records, csv_rows):
        assert all(str(v) == row[k] for k, v in r.items() if k != 'author_structured')

    # Parse the deliberately restricted emitted BibTeX format, respecting nested braces.
    bib = (OUT / 'engineering_references.bib').read_text()
    entries = re.findall(r'@article\{(FD_[A-Z]\d\d),\n(.*?)\n\}', bib, re.S)
    assert len(entries) == 38
    depth = 0
    for char in bib:
        if char == '{': depth += 1
        if char == '}': depth -= 1
        assert depth >= 0
    assert depth == 0
    for key, body in entries:
        r = indexed[key[3:]]
        values = dict(re.findall(r'^  (\w+) = \{(.*)\},$', body, re.M))
        assert values['doi'] == r['doi'] and values['year'] == str(r['year'])
        assert len(values['author'].split(' and ')) == len(r['author_structured'])
        assert values['url'] == r['source_url']
    ris = (OUT / 'engineering_references.ris').read_text().strip().split('\n\n')
    assert len(ris) == 38
    for block in ris:
        fields = {}
        for line in block.splitlines():
            key, value = line[:2], line[6:]
            fields.setdefault(key, []).append(value)
        r = indexed[fields['ID'][0][3:]]
        assert fields['TY'] == ['JOUR'] and 'ER' in fields
        assert fields['TI'] == [r['title']] and fields['DO'] == [r['doi']]
        assert fields['PY'] == [str(r['year'])]
        assert len(fields['AU']) == len(r['author_structured'])

    report = {'checked':'2026-10-27','result':'passed','papers':38,'unique_doi':38,
              'bibtex_entries':38,'ris_entries':38,'csv_records':38,
              'model_experiments_run':False, 'checks':[], 'artifacts':[]}
    for theme, filename, expected_count in GROUPS:
        expected = [r for r in records if r['theme'] == theme]
        assert len(expected) == expected_count
        with zipfile.ZipFile(OUT / filename) as z:
            assert z.testzip() is None
            wb = ET.fromstring(z.read('xl/workbook.xml'))
            assert [s.attrib['name'] for s in wb.findall('s:sheets/s:sheet', NS)] == ['论文与引用','工程验证与复现']
            shared = []
            if 'xl/sharedStrings.xml' in z.namelist():
                shared = [''.join(t.text or '' for t in el.findall('.//s:t', NS))
                          for el in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
            for sn, keys in [(1,PAPER_KEYS),(2,RESOURCE_KEYS)]:
                xml = ET.fromstring(z.read(f'xl/worksheets/sheet{sn}.xml'))
                assert not xml.findall('.//s:c[@t="e"]',NS)
                assert not xml.findall('.//s:f',NS), 'This catalog needs no formulas'
                pane=xml.find('.//s:pane',NS)
                assert pane is not None and pane.attrib['xSplit']=='2' and pane.attrib['ySplit']=='6'
                cells, types = {}, {}
                for c in xml.findall('.//s:c',NS):
                    value = c.findtext('s:v', default='', namespaces=NS)
                    if c.attrib.get('t')=='s': value=shared[int(value)]
                    elif c.attrib.get('t')=='inlineStr': value=''.join(t.text or '' for t in c.findall('.//s:t',NS))
                    cells[c.attrib['r']] = value
                    types[c.attrib['r']] = c.attrib.get('t','n')
                for row, r in enumerate(expected,7):
                    for j,k in enumerate(keys,1):
                        value=cells.get(f'{column(j)}{row}','')
                        if k=='checked':
                            assert value.startswith(r[k]+'T00:00:00') and types[f'{column(j)}{row}']=='d', (filename,k,value)
                        else: assert value == str(r[k]), (filename,row,k,value,r[k])
                if sn==1: assert xml.find('.//s:dataValidations',NS) is not None
            tables=[n for n in z.namelist() if n.startswith('xl/tables/') and n.endswith('.xml')]
            assert len(tables)==2
            for table in tables:
                assert ET.fromstring(z.read(table)).find('s:autoFilter',NS) is not None
        report['checks'].append({'file':filename,'records':expected_count,'sheets':2,
                                 'all_cells_match_catalog':True,'error_cells':0,'filters':True,'frozen_rows_columns':True})
    for file in [OUT/'README.md',ROOT/'README.md',ROOT/'src/README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not link.startswith(('http:', 'https:', '#')):
                assert (file.parent/link.split('#')[0]).exists(), (file,link)
    for p in (ROOT/'src').glob('*.py'): ast.parse(p.read_text(),filename=str(p))
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.suffix in ['.md','.json','.csv','.bib','.ris','.xlsx'] and p.name!='VALIDATION.json':
            report['artifacts'].append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    report['limits']='Document and metadata consistency only; no model training, external dataset download or native Excel/Zotero execution.'
    (OUT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['artifacts','checks']},ensure_ascii=False))

if __name__=='__main__': main()
