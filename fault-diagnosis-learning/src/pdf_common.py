from pathlib import Path
import math, re, json
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'build'; OUT=ROOT/'guides'
TMP.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
fontfile=TMP/'DroidSansFallback.ttf'
fontfile.write_bytes(fitz.Font('cjk').buffer)
pdfmetrics.registerFont(TTFont('CJK',str(fontfile)))
latin_font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
if latin_font.exists(): pdfmetrics.registerFont(TTFont('Latin',str(latin_font)))
else: pdfmetrics.registerFont(pdfmetrics.Font('Latin','Helvetica','WinAnsiEncoding'))
pdfmetrics.registerFontFamily('CJK',normal='CJK',bold='CJK',italic='CJK',boldItalic='CJK')
W,H=595.28,841.89; M=46; CW=W-2*M
NAVY=colors.HexColor('#163449'); TEAL=colors.HexColor('#087E8B'); INK=colors.HexColor('#243746'); GRAY=colors.HexColor('#61727C'); LIGHT=colors.HexColor('#EFF5F6'); ORANGE=colors.HexColor('#A85F20')
FILE=OUT/FILENAME
c=canvas.Canvas(str(FILE),pagesize=(W,H))
c.setTitle(TITLE)
c.setAuthor('ChatGPT'); c.setSubject('面向初学者的监督式机械故障分类入门，含学习路线、数据划分、训练与测试、特征解释及自测')
styles={
 'body':ParagraphStyle('body',fontName='CJK',fontSize=11,leading=18,textColor=INK,wordWrap='CJK',spaceAfter=0),
 'small':ParagraphStyle('small',fontName='CJK',fontSize=9.2,leading=14.3,textColor=GRAY,wordWrap='CJK'),
 'table':ParagraphStyle('table',fontName='CJK',fontSize=10,leading=16,textColor=INK,wordWrap='CJK'),
 'th':ParagraphStyle('th',fontName='CJK',fontSize=10,leading=15,textColor=colors.white,wordWrap='CJK'),
 'call':ParagraphStyle('call',fontName='CJK',fontSize=11,leading=18,textColor=NAVY,wordWrap='CJK'),
}
page=0; y=0; checks=[]; md=[]
def markdown(text):
 text=re.sub(r'<link href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</link>',r'[\2](\1)',text)
 text=text.replace('<br/>','<br>')
 return re.sub(r'</?(?:font|b|i)[^>]*>','',text)

def para(text,style='body',gap=9,x=None,width=None):
 global y
 md.append(markdown(text)+'\n')
 x=M if x is None else x; width=CW if width is None else width
 p=Paragraph(text,styles[style]); _,h=p.wrap(width,H)
 if y-h<52: raise ValueError(f'Overflow page {page}: y={y} h={h} text={text[:50]}')
 p.drawOn(c,x,y-h); y-=h+gap
 return h
def heading(text):
 global y
 md.append("### "+text+"\n")
 y-=4; c.setFillColor(TEAL); c.setFont('CJK',13); c.drawString(M,y-16,text); y-=26
def box(text,label=None,tint=LIGHT):
 global y
 md.append("> "+markdown((label+"：" if label else "")+text)+"\n")
 if label: text=f'<font color="#087E8B">{label}</font><br/>'+text
 p=Paragraph(text,styles['call']); _,h=p.wrap(CW-26,H)
 c.setFillColor(tint); c.roundRect(M,y-h-22,CW,h+22,7,fill=1,stroke=0)
 c.setFillColor(TEAL); c.rect(M,y-h-22,3,h+22,fill=1,stroke=0)
 p.drawOn(c,M+13,y-h-11); y-=h+34
def table(headers,rows,widths=None):
 global y
 md.append("| "+" | ".join(headers)+" |\n| "+" | ".join(["---"]*len(headers))+" |")
 md.extend("| "+" | ".join(markdown(str(v)) for v in row)+" |" for row in rows)
 md.append("")
 if widths is None: widths=[CW/len(headers)]*len(headers)
 data=[[Paragraph(str(s),styles['th']) for s in headers]]+[[Paragraph(str(s),styles['table']) for s in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('LINEBELOW',(0,0),(-1,0),.5,NAVY),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DCE6E9'))]))
 _,h=t.wrap(CW,H)
 if y-h<52: raise ValueError(f'Table overflow page {page}: {y-h}')
 t.drawOn(c,M,y-h); y-=h+13
def new(title,kicker,sub=''):
 global page,y
 md.append('\n## '+title+'\n')
 if page: finish()
 page+=1; y=H-100
 c.setFillColor(TEAL); c.rect(M,H-56,30,3,fill=1,stroke=0)
 c.setFont('Latin',8); c.setFillColor(GRAY); c.drawString(M+40,H-56,'FAULT DIAGNOSIS / FIRST STEPS')
 c.setFont('CJK',9); c.drawRightString(W-M,H-56,kicker)
 c.setFillColor(NAVY); c.setFont('CJK',23); c.drawString(M,y,title); y-=28
 if sub: para(sub,'small',gap=17)
 c.bookmarkPage(f'p{page}'); c.addOutlineEntry(title,f'p{page}',0)
def finish():
 checks.append({'page':page,'body_bottom':round(y,1)})
 c.setStrokeColor(colors.HexColor('#D9E3E7')); c.setLineWidth(.5); c.line(M,42,W-M,42)
 c.setFillColor(GRAY); c.setFont('CJK',8); c.drawString(M,28,TITLE+' · 零基础学习手册')
 c.setFont('Latin',8); c.drawRightString(W-M,28,f'{page:02d}'); c.showPage()
def node(x,top,w,h,title,desc):
 md.append("- "+title+"："+markdown(desc))
 c.setFillColor(LIGHT); c.roundRect(x,top-h,w,h,6,fill=1,stroke=0)
 c.setFillColor(TEAL); c.setFont('CJK',11); c.drawString(x+12,top-21,title)
 p=Paragraph(desc,styles['small']); _,ph=p.wrap(w-24,h); p.drawOn(c,x+12,top-30-ph)
def arrow(x1,y1,x2,y2,color=TEAL):
 c.setStrokeColor(color);c.setLineWidth(1.2);c.line(x1,y1,x2,y2)
 a=math.atan2(y2-y1,x2-x1); size=5
 c.line(x2,y2,x2-size*math.cos(a-.55),y2-size*math.sin(a-.55))
 c.line(x2,y2,x2-size*math.cos(a+.55),y2-size*math.sin(a+.55))


exec((Path(__file__).parent/'catalog_pages.py').read_text())
