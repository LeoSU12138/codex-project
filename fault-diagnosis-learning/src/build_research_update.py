"""Build original Chinese method guides and research plans from Markdown.

No network access or model training. Install reportlab and PyMuPDF to reproduce.
"""
from pathlib import Path
import csv
import html
import json
import re
import hashlib
import fitz
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
METHODS = ROOT / 'deep-learning-methods'
UPDATE = ROOT / 'research-update-2026-11'
BUILD = ROOT / 'build' / 'research-update'
BASE_URL = 'https://github.com/LeoSU12138/codex-project/tree/main/fault-diagnosis-learning/'
W, H, M = 595.28, 841.89, 44
CW = W - 2*M
NAVY, TEAL = colors.HexColor('#163449'), colors.HexColor('#087E8B')
FIELDS = ['归属','基本逻辑','输入与流程','核心表达','诊断示例','注意事项','验证与消融','特征挖掘着眼点','来源']


def setup():
    BUILD.mkdir(parents=True, exist_ok=True)
    font = BUILD / 'CJK.ttf'
    font.write_bytes(fitz.Font('cjk').buffer)
    pdfmetrics.registerFont(TTFont('CJKUpdate', str(font)))
    pdfmetrics.registerFontFamily('CJKUpdate', normal='CJKUpdate', bold='CJKUpdate', italic='CJKUpdate', boldItalic='CJKUpdate')


STYLES = {}


def styles():
    shared = dict(fontName='CJKUpdate', wordWrap='CJK', textColor=NAVY)
    for name, size, leading, gap in [('body',10.4,16.5,7),('small',8.6,13,5),('title',23,32,20),('h1',18,26,15),('h2',14,21,12),('h3',11.5,18,8),('table',9.2,14.5,0)]:
        STYLES[name] = ParagraphStyle(name, fontSize=size, leading=leading, spaceAfter=gap,
                                     keepWithNext=name in ('h1','h2','h3'), **shared)


def inline(s):
    s = html.escape(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#087E8B">\1</link>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', s)
    s = re.sub(r'\*\*(.*?)\*\*', r'<font color="#087E8B">\1</font>', s)
    return s.replace('`', '')


def para(text, style='body', key=None, level=0):
    p = Paragraph(inline(text), STYLES[style])
    if key:
        p.bookmark = (key, re.sub(r'\*\*', '', text), level)
    return p


class GuideDoc(SimpleDocTemplate):
    def __init__(self, path, title):
        super().__init__(str(path), pagesize=(W,H), leftMargin=M, rightMargin=M,
                         topMargin=62, bottomMargin=54, title=title,
                         author='codex-project / 故障诊断学习资料', pageCompression=1, invariant=1)
        self.guide_title = title
        self.outline = []

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark'):
            key, title, level = flowable.bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level, False)
            self.outline.append({'key':key,'title':title,'page':self.page})


def chrome(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(M,H-38,24,3,fill=1,stroke=0)
    canvas.setFont('CJKUpdate',8)
    canvas.drawString(M+34,H-39,'故障诊断 / 方法与研究设计')
    canvas.setFillColor(colors.HexColor('#61727C'))
    canvas.drawRightString(W-M,H-39,'2026-11-01')
    canvas.setStrokeColor(colors.HexColor('#D9E3E7'))
    canvas.line(M,40,W-M,40)
    canvas.setFont('CJKUpdate',7.5)
    canvas.drawString(M,26,doc.guide_title)
    canvas.drawRightString(W-M,26,str(doc.page))
    canvas.restoreState()


def table(rows):
    n=len(rows[0]); widths=[CW/n]*n
    data=[[para(cell,'table') for cell in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEEF0')),
                          ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7F8')]),
                          ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
                          ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),
                          ('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#D9E3E7'))]))
    return t


def markdown(text, prefix):
    blocks=[]; lines=text.splitlines(); i=0; section=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',c) for c in cells): rows.append(cells)
                i+=1
            blocks.extend([table(rows),Spacer(1,10)]); continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#')); title=line[level:].strip();section+=1
            blocks.append(para(title, 'h1' if level==1 else 'h2' if level==2 else 'h3', f'{prefix}-{section}'))
            i+=1;continue
        # Each authored paragraph is a single line; preserve numbered/list items.
        blocks.append(para(line));i+=1
    return blocks


def cards():
    text=(METHODS/'方法详解.md').read_text()
    result=[]
    for match in re.finditer(r'^## (M\d\d)｜([^\n]+)\n(.*?)(?=^## M\d\d｜|\Z)',text,re.M|re.S):
        ident,title,body=match.groups()
        fields=dict(re.findall(r'^\*\*([^：]+)：\*\* (.+)$',body,re.M))
        if list(fields)!=FIELDS: raise ValueError((ident,fields.keys()))
        result.append(dict(id=ident,title=title,group=fields['归属'].split('；')[0],fields=fields))
    assert [c['id'] for c in result]==[f'M{i:02}' for i in range(1,36)]
    return result


def references(selected):
    full='\n'.join(' '.join(c['fields'].values()) for c in selected)
    ids=set(re.findall(r'(?<![A-Za-z0-9])([CDFSNBE]\d\d)(?![A-Za-z0-9])',full))
    formal=json.loads((ROOT/'research-papers/catalog.json').read_text())
    fetched=json.loads((UPDATE/'SOURCE_RETRIEVAL.json').read_text())['sources']
    old=json.loads((ROOT/'references/catalog.json').read_text())
    lines=['# 来源速查','', 'D/F/C/S为正式38篇库编号，题录沿用历史核验；N/B为本轮README，E为源码。条目提供原理和阅读入口，不表示本轮取得全文或运行实验。通用公式是教学抽象，实验示例是研究建议。','']
    for r in formal:
        if r['id'] in ids:
            lines.extend([f"**{r['id']}** {r['authors']} ({r['year']}). {r['title']}. {r['journal']}. https://doi.org/{r['doi']}",''])
    old_map={'M01':['D01','D03'],'M04':['D09'],'M08':['D10'],'M18':['D17'],'M20':['D15'],
             'M21':['D16'],'M26':['D14'],'M27':['D11'],'M28':['D12'],'M32':['F09','F10'],
             'M33':['F08'],'M34':['F07','F11']}
    old_ids={v for c in selected for v in old_map.get(c['id'],[])}
    for r in old:
        if r['id'] in old_ids:
            lines.extend([f"**旧库{r['id']}** {r['authors']} ({r['year']}). {r['title']}. {r['source_url']}。历史来源核验，非本轮全文评审。",''])
    for r in fetched:
        if r['id'] in ids and r['status']=='retrieved':
            lines.extend([f"**{r['id']}** {r['title']}。本轮读取类型：{r['kind']}。{r['url']}",''])
    lines.extend(['完整证据记录与研究方案：'+BASE_URL+'research-update-2026-11','',
                  '流程来源：literature-review技能；历史引文Kassis等（2026），Scientific Agent Skills，https://doi.org/10.48550/arXiv.2609.00065 。本轮访问受限，未重新核验版本；不是故障诊断研究证据。',''])
    return '\n'.join(lines)


def cover(title, subtitle, selected=None, directory='deep-learning-methods'):
    out=[Spacer(1,48),para(title,'title','cover'),para(subtitle,'h2'),Spacer(1,15),
         para('版本：2026-11-01。中文可搜索，章节可从PDF书签跳转。'),
         para('本资料为原创方法导读与研究设计；没有执行论文模型实验，不包含未经核验的性能排行榜。')]
    if selected:
        out.append(para('阅读索引','h2'))
        for c in selected:out.append(para(c['id']+'  '+c['title'],'small'))
    out.extend([Spacer(1,12),para('先确认预测可靠，再检查模型依赖，最后验证候选特征。','h2'),
                para('GitHub在线目录：'+BASE_URL+directory,'small')])
    if directory == 'research-update-2026-11':
        out.append(para('来源证据：'+BASE_URL+directory+'/来源与证据映射.md','small'))
    return out


def card_story(card):
    story=[para(card['id']+'｜'+card['title'],'h1',card['id'])]
    for name,value in card['fields'].items():
        story.append(para('**'+name+'：** '+value,'small' if name in ('归属','来源') else 'body'))
    # Fail rather than silently split a method card across pages.
    height=sum(p.wrap(CW-12,H)[1]+p.getSpaceBefore()+p.getSpaceAfter() for p in story)
    if height>H-62-54-12:
        raise ValueError(f"{card['id']} card too tall: {height:.1f}")
    return [KeepTogether(story)]


def build(path,title,story):
    doc=GuideDoc(path,title);doc.build(story,onFirstPage=chrome,onLaterPages=chrome)
    with fitz.open(path) as pdf:
        return {'file':str(path.relative_to(ROOT)), 'pages':len(pdf), 'bytes':path.stat().st_size,
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'outline':doc.outline}


def main():
    setup();styles();cs=cards();results=[]
    story=cover('故障诊断深度学习方法详解','31项建模/训练路线 + 4项解释方法')
    story += [PageBreak()]+markdown((METHODS/'阅读与选型.md').read_text(),'intro')
    story += [PageBreak(),para('方法索引','h1','index')]
    for c in cs:story.append(para(c['id']+'  '+c['title']+'  / '+c['group'].split('_',1)[1],'small'))
    for c in cs:story += [PageBreak()]+card_story(c)
    refs=references(cs);(METHODS/'参考来源.md').write_text(refs)
    story += [PageBreak()]+markdown(refs,'ref')
    results.append(build(METHODS/'00_故障诊断深度学习方法详解_合订本.pdf','故障诊断深度学习方法详解',story))
    for group in dict.fromkeys(c['group'] for c in cs):
        subset=[c for c in cs if c['group']==group]
        title=group.split('_',1)[1]
        story=cover(title,'方法分册 / 原理、流程、注意事项与验证',subset)
        for c in subset:story += [PageBreak()]+card_story(c)
        story += [PageBreak()]+markdown(references(subset),'ref')
        results.append(build(METHODS/(group+'.pdf'),title,story))
    for stem in ['调研补充与缺口分析','下一步研究方案']:
        story=cover(stem,'从文献与方法地图进入可检验的研究',directory='research-update-2026-11')
        story += [PageBreak()]+markdown((UPDATE/(stem+'.md')).read_text(),stem)
        results.append(build(UPDATE/(stem+'.pdf'),stem,story))
    pages={r['key']:r['page'] for r in results[0]['outline'] if re.fullmatch(r'M\d\d',r['key'])}
    with (METHODS/'方法索引.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['编号','方法','分类','合订本页码','分册PDF','来源说明'])
        for c in cs:writer.writerow([c['id'],c['title'],c['group'],pages[c['id']],c['group']+'.pdf',c['fields']['来源']])
    (BUILD/'build_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    for r in results:print(r['file'],r['pages'],'pages',r['bytes'],'bytes')


if __name__=='__main__':main()
