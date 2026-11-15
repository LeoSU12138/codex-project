"""Validate delivered manuscript, embedded figures and synthetic source data."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
import fitz
import numpy as np
from PIL import Image, ImageFilter
from scipy.signal import butter, sosfiltfilt, hilbert
from docx import Document

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures'


def main():
    source=(ROOT/'paper.md').read_text()
    assert len(re.findall(r'!\[图[1-4]',source))==4
    assert all(f'\\tag{{{i}}}' in source for i in range(1,8))
    pdf=fitz.open(ROOT/'paper.pdf')
    text=''.join(p.get_text() for p in pdf)
    compact=re.sub(r'\s+','',text)
    assert len(pdf)>=6 and '尚无真实设备数据' in compact
    assert '\ufffd' not in text
    for word in ['摘要','引言','参考文献','合成信号','解释忠实性','物理一致性']:
        assert word in compact,word
    assert len(re.findall(r'图\s*[1-4]\s*　?',text))>=8
    for p in pdf:
        assert 590<p.rect.width<600 and 835<p.rect.height<850
        for b in p.get_text('dict')['blocks']:
            if b['type']!=0:continue
            for line in b['lines']:
                x0,y0,x1,y1=line['bbox']
                assert x0>=15 and y0>=15 and x1<p.rect.width-15 and y1<p.rect.height-15,(p.number,line)
        for font in p.get_fonts(full=True):
            assert font[1]!='n/a',('unembedded font',font)
    document=Document(ROOT/'paper.docx')
    assert len(document.inline_shapes)==4
    assert len(document.tables)==2
    with zipfile.ZipFile(ROOT/'paper.docx') as z:
        xml=z.read('word/document.xml').decode()
        assert len(re.findall(r'<m:oMath[ >]',xml))>=7
        assert not any(t in xml for t in ['\\frac','\\tag','\\mathrm'])
        assert len([n for n in z.namelist() if n.startswith('word/media/')])==4
    figures=[]
    for item in json.loads((FIG/'FIGURE_MANIFEST.json').read_text())['figures']:
        for rec in item['files']:
            p=ROOT/rec['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256']
        png=Image.open(FIG/(item['id']+'.png')).convert('RGB')
        assert png.width>=2000 and png.info.get('dpi',(300,300))[0]>=299
        vector=fitz.open(FIG/(item['id']+'.pdf'))
        assert len(vector)==1 and not vector[0].get_images()
        assert len(vector[0].get_text())>60
        # Catch font embedding failures: dark glyphs in PNG must render in PDF.
        pix=vector[0].get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False)
        rendered=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        if rendered.size!=png.size:rendered=rendered.resize(png.size)
        ref=np.asarray(png.convert('L'))<75
        dark=np.asarray(rendered.convert('L').filter(ImageFilter.MinFilter(3)))<160
        retained=float(dark[ref].mean());assert retained>.94,(item['id'],retained)
        figures.append({'id':item['id'],'png_px':list(png.size),'pdf_dark_content_retention':retained})
    a=np.load(FIG/'synthetic_source.npz');p=json.loads((FIG/'synthetic_parameters.json').read_text())
    t=np.arange(int(p['fs_hz']*p['duration_s']))/p['fs_hz']
    clean=np.zeros_like(t)
    for tm in np.arange(p['impulse_start_s'],p['impulse_stop_exclusive_s'],1/p['repetition_hz']):
        dt=t-tm;active=dt>=0
        clean[active]+=p['impulse_amplitude']*np.exp(-p['decay_per_s']*dt[active])*np.sin(2*np.pi*p['carrier_hz']*dt[active])
    x=clean+p['sine_amplitude']*np.sin(2*np.pi*p['sine_hz']*t)+p['noise_sd']*np.random.default_rng(p['seed']).standard_normal(len(t))
    np.testing.assert_allclose(x,a['signal'],rtol=0,atol=1e-13)
    filtered=sosfiltfilt(butter(4,p['band_hz'],btype='bandpass',fs=p['fs_hz'],output='sos'),x)
    np.testing.assert_allclose(filtered,a['filtered'],rtol=0,atol=1e-13)
    np.testing.assert_allclose(np.abs(hilbert(filtered)),a['envelope'],rtol=0,atol=1e-13)
    f,v=a['envelope_frequency_hz'],a['envelope_amplitude'];region=(f>50)&(f<450)
    peak=float(f[region][np.argmax(v[region])]);assert abs(peak-p['repetition_hz'])<2
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'result':'passed',
            'pdf_pages':len(pdf),'embedded_docx_figures':len(document.inline_shapes),
            'docx_tables':len(document.tables),'figures':figures,
            'synthetic_signal_reconstruction':'passed','envelope_peak_hz':peak,
            'real_device_experiments':False,'native_word_visual_review':False,
            'sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['paper.md','paper.pdf','paper.docx','build.py']}}
    (ROOT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {len(pdf)} PDF pages, 4 embedded Word figures, 2 tables, formulas, fonts, figure rendering and synthetic source')


if __name__=='__main__':main()
