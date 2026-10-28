"""Artifact integrity checks; no model or literature experiments are run."""
from pathlib import Path
import ast, csv, json, hashlib, zipfile, xml.etree.ElementTree as ET
from datetime import datetime, timezone
import fitz
ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
records=json.loads((ROOT/'references/catalog.json').read_text())
assert len(records)==43 and len({r['id'] for r in records})==43
required=['title','authors','content','method','reference_value','reproduction','source_url','code_url','data_url','verification']
assert all(all(r[k] for k in required) for r in records)
assert all(r['run_status']=='未运行验证' for r in records)
for prefix, name in [('D','深度学习'),('F','特征挖掘'),('C','融合研究')]:
 with (ROOT/'references'/f'{name}_参考文献.csv').open(encoding='utf-8-sig',newline='') as f:
  assert list(csv.DictReader(f)) == [r for r in records if r['id'].startswith(prefix)]
for p in (ROOT/'src').glob('*.py'): ast.parse(p.read_text(),filename=str(p))
report={'checked':datetime.now(timezone.utc).date().isoformat(), 'executed_at_utc':datetime.now(timezone.utc).isoformat(),'literature_entries':43,'model_experiments_run':False,'artifacts':[]}
for filename,pages in [('01_故障诊断深度学习入门.pdf',24),('02_特征挖掘入门.pdf',15),('03_深度学习与特征挖掘结合.pdf',11)]:
 p=ROOT/'guides'/filename;d=fitz.open(p);assert len(d)==pages
 links=0
 pdf_text='\n'.join(page.get_text() for page in d)
 md_text=p.with_suffix('.md').read_text()
 required_terms={
  '01':['Precision','Recall','F1','特殊建模','支持样本','验证集','标准化','检查点','超网络'],
  '02':['方差','m/s²','MCKD','MOMEDA','FMD','窗函数','谱泄漏','阶次','720°'],
  '03':['重要/不重要/随机带','分布外信号','macro-F1','冻结模型'],
 }[filename[:2]]
 for term in required_terms:
  assert term in pdf_text and term in md_text,(filename,term,'missing required content')
 for n,page in enumerate(d):
  assert len(page.get_text().strip())>80,(filename,n+1,'empty')
  assert '\ufffd' not in page.get_text(),(filename,n+1,'replacement glyph')
  for b in page.get_text('blocks'):
   assert b[0]>=30 and b[2]<=580 and b[1]>=20 and b[3]<=825,(filename,n+1,b[:4])
  links+=len(page.get_links())
 assert links>0
 assert p.with_suffix('.md').exists()
 report['artifacts'].append({'file':str(p.relative_to(ROOT)),'pages':pages,'links':links,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 assert not d.is_encrypted
 if filename.startswith('02'): assert '^4' in d[1].get_text() and 'x-' in d[1].get_text()
for prefix,filename in [('D','01_深度学习参考文献.xlsx'),('F','02_特征挖掘参考文献.xlsx'),('C','03_融合研究参考文献.xlsx')]:
 p=ROOT/'references'/filename;expected=[r['id'] for r in records if r['id'].startswith(prefix)]
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   strings=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
  for sn in [1,2,3]:
   xml=ET.fromstring(z.read(f'xl/worksheets/sheet{sn}.xml'))
   assert not xml.findall('.//s:c[@t="e"]',NS),(filename,sn,'error cell')
   if sn<3:
    pane=xml.find('.//s:pane',NS);assert pane is not None and pane.attrib['xSplit']=='1' and pane.attrib['ySplit']=='5'
    ids=[]
    for c in xml.findall('.//s:c',NS):
     if c.attrib.get('r','').startswith('A') and c.attrib.get('r','')[1:].isdigit() and int(c.attrib['r'][1:])>=6:
      v=c.findtext('s:v',namespaces=NS)
      if c.attrib.get('t')=='s':ids.append(strings[int(v)])
      else:ids.append(c.findtext('s:is/s:t',default=v,namespaces=NS))
    assert ids==expected,(filename,sn,ids)
  xml=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
  assert xml.find('.//s:dataValidations',NS) is not None
  tables=[n for n in z.namelist() if n.startswith('xl/tables/') and n.endswith('.xml')]
  assert len(tables)==2
  assert all(ET.fromstring(z.read(t)).find('s:autoFilter',NS) is not None for t in tables)
 report['artifacts'].append({'file':str(p.relative_to(ROOT)),'entries':len(expected),'sheets':3,'error_cells':0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'result':'passed','pdf_pages':sum(a.get('pages', 0) for a in report['artifacts']),'workbooks':3,'entries':43,'scope':'document integrity; no model experiments'},ensure_ascii=False))
