"""Build original scientific figures and manuscript; no model experiments."""
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile

os.environ.setdefault('MPLCONFIGDIR', '/tmp/paper-matplotlib-cache')
os.environ.setdefault('XDG_CACHE_HOME', '/tmp/paper-font-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import scipy
from scipy.signal import butter, sosfiltfilt, hilbert
import fitz

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'figures'
BLUE, TEAL, AMBER, INK = '#165A88', '#126B60', '#8C5700', '#202C38'
FONT = '/tmp/paper-cjk.ttf'
Path(FONT).write_bytes(fitz.Font('cjk').buffer)
font_manager.fontManager.addfont(FONT)
plt.rcParams.update({'font.family': font_manager.FontProperties(fname=FONT).get_name(),
                     'font.size': 10, 'axes.unicode_minus': False,
                     'pdf.fonttype': 42, 'svg.fonttype': 'path',
                     'savefig.facecolor': 'white', 'axes.spines.top': False,
                     'axes.spines.right': False, 'text.color': INK})
MANIFEST = {'kind': 'method_schematics_and_synthetic_demonstration',
            'real_device_experiments': False, 'model_trained': False,
            'shap_computed': False, 'seed': 20261115,
            'versions': {'python': platform.python_version(), 'matplotlib': matplotlib.__version__,
                         'numpy': np.__version__, 'scipy': scipy.__version__}, 'figures': []}


def export(fig, name, meaning):
    paths = []
    for ext in ['png', 'svg', 'pdf']:
        p = FIG / f'{name}.{ext}'
        fig.savefig(p, dpi=300, facecolor='white')
        paths.append({'path': str(p.relative_to(ROOT)),
                      'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    MANIFEST['figures'].append({'id': name, 'meaning': meaning,
                               'size_inches': list(fig.get_size_inches()), 'files': paths})
    plt.close(fig)


def canvas(title, size=(7.1, 4.5)):
    fig, ax = plt.subplots(figsize=size)
    fig.subplots_adjust(left=.02, right=.98, bottom=.04, top=.89)
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis('off')
    fig.suptitle(title, fontsize=13, color=INK, fontweight='bold', y=.97)
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.018',
                               lw=1.15, edgecolor=color, facecolor='#F6F8FA'))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs, linespacing=1.55)


def arrow(ax, a, b, color=INK):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=11,
                                lw=1.05, color=color))


def diagrams():
    fig, ax = canvas('研究流程：先独立划分，再挖掘与检验')
    box(ax,.03,.76,.23,.16,'原始振动记录\n设备 / 记录 / 工况')
    box(ax,.38,.76,.24,.16,'按独立单元划分\n随后分别切窗')
    arrow(ax,(.27,.84),(.37,.84))
    ys=[.53,.29,.05]
    texts=[('训练集','训练模型 → 冻结权重\n频带归因 → 候选特征发现',BLUE),
           ('验证集','选择模型、特征数量与阈值\n随后锁定全部分析设置',TEAL),
           ('最终测试集','只执行预定独立评价\n诊断性能 / 解释 / 特征价值',AMBER)]
    for y,(label,desc,col) in zip(ys,texts):
        box(ax,.05,y,.22,.16,label,col)
        box(ax,.39,y,.56,.16,desc,col)
        arrow(ax,(.28,y+.08),(.38,y+.08),col)
    ax.plot([.5,.5,.015,.015],[.75,.72,.72,.13],color=INK,lw=1.05)
    for y in ys:arrow(ax,(.015,y+.08),(.04,y+.08))
    ax.text(.80,.84,'无实测结果',ha='center',va='center',fontsize=10,color=AMBER,
            bbox={'facecolor':'white','edgecolor':'none'})
    export(fig,'fig1_workflow','Method schematic, not experimental results')

    fig, ax = canvas('频带分组归因：频域操作与时域模型连接')
    box(ax,.02,.72,.24,.17,'待解释信号 x\n训练背景信号 b')
    box(ax,.39,.72,.23,.17,'单边复数频谱\n保留幅值与相位')
    box(ax,.75,.72,.23,.17,'按集合 S 组合\n其余频带由 b 替换')
    arrow(ax,(.27,.80),(.38,.80));arrow(ax,(.63,.80),(.74,.80))
    box(ax,.75,.40,.23,.17,'匹配的逆变换\n得到实值波形')
    box(ax,.39,.40,.23,.17,'冻结诊断模型\n固定类别得分')
    box(ax,.02,.40,.24,.17,'排列采样近似\n频带贡献')
    arrow(ax,(.86,.71),(.86,.58));arrow(ax,(.74,.48),(.63,.48));arrow(ax,(.38,.48),(.27,.48))
    box(ax,.09,.04,.82,.23,'数值与敏感性检查\n重构误差 · 背景集合 · 频带粒度 · 采样预算\n图中不包含已计算的 SHAP 值',TEAL)
    arrow(ax,(.14,.39),(.14,.28),TEAL)
    export(fig,'fig2_attribution','Proposed complex-spectrum grouping; no SHAP values computed')

    fig, ax = canvas('三层验证：不同主张需要不同证据',size=(7.1,4.7))
    rows=[(.68,'解释忠实性','高贡献 / 低贡献 / 随机区域扰动\n检查替换策略与异常重构','失效：仅对异常扰动敏感',BLUE),
          (.37,'物理一致性','故障频率 / 谐波 / 阶次对照\n排查竞争频率与转速误差','边界：频率接近不等于因果',TEAL),
          (.06,'特征诊断价值','同维度、同分类器、同预算\n传统 / 随机 / 解释引导特征','失效：独立工况不优于基线',AMBER)]
    for y,title,body,note,col in rows:
        box(ax,.02,y,.23,.23,title,col)
        box(ax,.33,y,.64,.23,body,col,fs=9.5)
        arrow(ax,(.26,y+.115),(.32,y+.115),col)
        ax.text(.65,y-.032,note,ha='center',va='center',fontsize=8.5,color=col)
    export(fig,'fig4_validation','Prospective controls and failure criteria, not validation outcomes')


def synthetic():
    fs, duration, repetition, carrier, decay, seed = 12800, 1., 100., 2400., 900., 20261115
    t=np.arange(int(fs*duration))/fs
    clean=np.zeros_like(t)
    for tm in np.arange(.02,.98,1/repetition):
        dt=t-tm; active=dt>=0
        clean[active]+=np.exp(-decay*dt[active])*np.sin(2*np.pi*carrier*dt[active])
    rng=np.random.default_rng(seed)
    x=clean+.12*np.sin(2*np.pi*30*t)+.08*rng.standard_normal(len(t))
    sos=butter(4,[1800,3000],btype='bandpass',fs=fs,output='sos')
    filtered=sosfiltfilt(sos,x);env=np.abs(hilbert(filtered))
    def spectrum(a):
        w=np.hanning(len(a));v=2*np.abs(np.fft.rfft(a*w))/w.sum()
        v[0]/=2
        if len(a)%2==0:v[-1]/=2
        return np.fft.rfftfreq(len(a),1/fs),v
    f,amp=spectrum(x)
    interior=(t>=.1)&(t<.9)
    fe,ae=spectrum(env[interior]-env[interior].mean())
    np.savez_compressed(FIG/'synthetic_source.npz',time_s=t,signal=x,clean_impulses=clean,
                        filtered=filtered,envelope=env,spectrum_frequency_hz=f,
                        spectrum_amplitude=amp,envelope_frequency_hz=fe,envelope_amplitude=ae)
    parameters={'fs_hz':fs,'duration_s':duration,'repetition_hz':repetition,
                'carrier_hz':carrier,'decay_per_s':decay,'impulse_start_s':.02,
                'impulse_stop_exclusive_s':.98,'impulse_amplitude':1.,'sine_hz':30.,
                'sine_amplitude':.12,'noise_sd':.08,'seed':seed,'units':'arbitrary',
                'filter':'4th-order Butterworth bandpass; scipy sosfiltfilt',
                'band_hz':[1800,3000],'envelope':'abs(scipy.signal.hilbert(filtered))',
                'spectrum':'one-sided Hann-window amplitude; coherent-gain correction',
                'envelope_spectrum_interval_s':[.1,.9],
                'band_selection':'predefined from synthetic generator; not attribution discovery'}
    (FIG/'synthetic_parameters.json').write_text(json.dumps(parameters,ensure_ascii=False,indent=2)+'\n')
    fig,axes=plt.subplots(2,2,figsize=(7.1,5.1),layout='constrained')
    short=t<.1
    axes[0,0].plot(t[short],x[short],color=BLUE,lw=.65)
    axes[0,0].set(title='（a）合成振动波形',xlabel='时间 / s',ylabel='幅值 / a.u.',xlim=(0,.1))
    axes[0,1].plot(f,amp,color=BLUE,lw=.8)
    axes[0,1].axvspan(1800,3000,facecolor='#FFF2D5',edgecolor=AMBER,hatch='///',lw=.5,label='预设滤波带')
    axes[0,1].set(title='（b）原始信号幅值谱',xlabel='频率 / Hz',ylabel='幅值 / a.u.',xlim=(0,4000),ylim=(0,None))
    axes[0,1].legend(fontsize=8)
    axes[1,0].plot(t[short],filtered[short],color=BLUE,lw=.65,label='带通信号')
    axes[1,0].plot(t[short],env[short],color=AMBER,lw=1.1,ls='--',label='Hilbert 包络')
    axes[1,0].set(title='（c）滤波与包络',xlabel='时间 / s',ylabel='幅值 / a.u.',xlim=(0,.1))
    axes[1,0].legend(fontsize=8,loc='lower right')
    axes[1,1].plot(fe,ae,color=TEAL,lw=.95)
    for h in [100,200,300]:axes[1,1].axvline(h,color=AMBER,ls='--',lw=.8)
    axes[1,1].set(title='（d）去均值包络幅值谱',xlabel='调制频率 / Hz',ylabel='幅值 / a.u.',xlim=(0,450),ylim=(0,None))
    axes[1,1].text(.98,.96,'虚线：预设重复频率及谐波',transform=axes[1,1].transAxes,
                    ha='right',va='top',fontsize=8)
    for ax in axes.flat:
        ax.tick_params(labelsize=8);ax.title.set_fontsize(10);ax.grid(alpha=.15)
    fig.suptitle('合成信号演示（非实测数据、非模型解释结果）',fontsize=12,fontweight='bold')
    export(fig,'fig3_synthetic','Computed synthetic signal demo, predefined band, not real device validation')


def documents():
    env=os.environ.copy();env['XDG_CACHE_HOME']='/tmp/paper-font-cache'
    # PDF embeds vector figures; Markdown and Word use high-resolution PNG.
    pdf_source=(ROOT/'paper.md').read_text()
    for item in MANIFEST['figures']:
        stem=item['id'];pdf_source=pdf_source.replace(f'(figures/{stem}.png)',f'(figures/{stem}.pdf)')
    with tempfile.NamedTemporaryFile(mode='w',suffix='.md',encoding='utf-8',delete=False) as tmp:
        tmp.write(pdf_source);pdf_input=tmp.name
    try:
        subprocess.run(['pandoc',pdf_input,'--standalone',f'--resource-path={ROOT}',
                    '--pdf-engine=xelatex','--variable=documentclass:article',
                    '--variable=CJKmainfont:Noto Serif CJK SC',
                    '--variable=mainfont:DejaVu Serif','--variable=sansfont:DejaVu Sans',
                    '--variable=fontsize:11pt','--variable=papersize:a4',
                    '--variable=geometry:margin=24mm','--variable=colorlinks:true',
                    '--include-in-header=preamble.tex','--output=paper.pdf'],cwd=ROOT,env=env,check=True)
    finally:
        Path(pdf_input).unlink(missing_ok=True)
    subprocess.run(['pandoc','paper.md','--standalone','--resource-path=.',
                    '--output=paper.docx'],cwd=ROOT,check=True)
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt
    doc=Document(ROOT/'paper.docx')
    for section in doc.sections:
        section.page_width=Mm(210);section.page_height=Mm(297)
        section.left_margin=section.right_margin=Mm(24)
        section.top_margin=section.bottom_margin=Mm(24)
        p=section.footer.paragraphs[0];p.alignment=1
        field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');p._p.append(field)
    for style in doc.styles:
        if style.type==1:
            style.font.name='Times New Roman';style.font.size=Pt(10.5)
            style.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'宋体')
            style.paragraph_format.line_spacing=1.35
        if style.name.startswith('Heading'):
            style.font.bold=True
            style.font.size=Pt(12 if style.name!='Heading 1' else 14)
            style.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'黑体')
            style.paragraph_format.keep_with_next=True
    for p in doc.paragraphs:
        if p._p.xpath('.//w:drawing'):p.paragraph_format.keep_with_next=True
        if p.text=='参考文献':p.paragraph_format.page_break_before=True
    doc.core_properties.title='面向跨工况故障诊断的解释引导特征挖掘方法框架'
    doc.core_properties.subject='方法框架与实验方案稿；含合成信号演示'
    doc.core_properties.author=''
    doc.save(ROOT/'paper.docx')


if __name__=='__main__':
    FIG.mkdir(exist_ok=True)
    diagrams();synthetic()
    (FIG/'FIGURE_MANIFEST.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2)+'\n')
    documents()
    print('Built 4 original figures (PNG/SVG/PDF), source arrays, manuscript PDF and DOCX')
