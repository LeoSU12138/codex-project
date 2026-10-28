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
FILE=OUT/'01_故障诊断深度学习入门.pdf'
c=canvas.Canvas(str(FILE),pagesize=(W,H))
c.setTitle('故障诊断深度学习｜零基础第一课：流程与知识地图')
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
 c.setFillColor(GRAY); c.setFont('CJK',8); c.drawString(M,28,'故障诊断深度学习 · 入门与方法地图')
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

new('故障诊断深度学习','零基础 · 第一步','从一段振动信号，到一次有依据的故障判断')
c.setFillColor(TEAL);c.setFont('CJK',17);c.drawString(M,y-21,'先看懂流程，再开始训练模型');y-=45
para('你现在没有现成模型，也可以开始学习。本手册以“用轴承振动判断正常、内圈故障、外圈故障”为贯穿例子，讲清楚一个监督式分类项目从哪里开始、每一步做什么，以及需要补哪些知识。')
box('这一课先掌握：样本和标签、训练与推理、训练集与测试集。暂时不要求你推导反向传播，也不要求你读懂 TFN 或 SHAP。','本课目标')
table(['你会遇到的问题','在本手册中找到答案'],[
 ['整个项目怎样走一遍？','第 2 页：完整流程；第 8 页：数字化例子'],
 ['信号如何变成模型输入？','第 3-5 页：采样、切片、划分和 CNN'],
 ['模型如何学习，训练后留下什么？','第 6 页：训练循环与模型文件'],
 ['准确率高就说明模型可靠吗？','第 7 页：测试、漏报与过拟合'],
 ['我究竟要学哪些知识？','第 9-10 页：知识地图与过关顺序'],
 ['什么时候进入特征挖掘？','第 11 页：和你研究目标的连接'],
 ['怎样检查自己是否学懂？','第 12 页：自测；第 13 页：学习资料'],
 ],[190,CW-190])
para('推荐读法：第一次只读第 1-4 页；理解后再读第 5-8 页。第 9-13 页用于安排后续学习和复习。第14–21页补充方法分类、FNO、超网络、泛化和模型修改，末尾给出扩展来源。','small')
para('范围说明：这里讲的是“有类别标签的监督式故障分类”。无监督异常检测、故障程度回归和剩余寿命预测是其他任务，后续再学。所有未注明来源的数值例子均为教学设定，不是实测结果。','small')

new('01  先看懂完整流程','全局地图','你的第一个目标：完整说清楚数据怎样变成一个判断。')
para('深度学习故障诊断，就是让一个可调参数的计算模型，通过带有已知状态标签的信号样本学习规律，再对新信号进行分类。标签来自实验记录、检查或其他可信依据，不是模型自己给出的标准答案。')
top=y;node(M,top,CW,58,'① 明确任务并整理原始记录','确定设备、传感器、正常/故障类别；保留转速、负载、设备与采集批次。')
arrow(W/2,top-58,W/2,top-76)
node(M,top-76,CW,58,'② 按独立来源划分，再在各集合内切片','训练集学参数；验证集选方案；测试集留到方案确定后评估。')
mid=top-155; bw=(CW-24)/2
arrow(W/2,top-134,M+bw/2,mid);arrow(W/2,top-134,M+bw+24+bw/2,mid)
node(M,mid,bw,91,'③ 训练与验证','用训练集确定标准化参数、训练模型；验证集使用同一变换，辅助选择模型。')
node(M+bw+24,mid,bw,91,'④ 保留独立测试集','不参与训练或调参；最终使用已确定的预处理、模型和判定规则。')
arrow(M+bw/2,mid-91,M+bw/2,mid-109);arrow(M+bw+24+bw/2,mid-91,M+bw+24+bw/2,mid-109)
node(M,mid-109,bw,71,'⑤ 保存完整推理所需信息','模型结构与权重、类别编号、预处理参数、输入设置。')
node(M+bw+24,mid-109,bw,71,'⑥ 测试并检查错误','查看准确率、各类召回率和混淆矩阵；分析错判发生在哪里。')
y=mid-195
heading('训练和推理，区别在哪里？')
table(['训练：让模型学习','推理：使用已经学好的模型'],[
 ['输入信号和已知标签，计算预测误差。','输入新的信号，得到类别分数和预测类别。'],
 ['重复调整模型的权重和偏置。','通常不更新参数；不需要真实标签才能预测。'],
 ['像做练习并根据答案订正。','像完成一道没有答案的新题。'],
 ],[CW/2,CW/2])
para('解释与验证：模型训练完成后，可以再分析重要频率或冲击位置。解释是否合理和诊断是否准确，是两个需要分别检查的问题。','small')

new('02  模型到底看见了什么？','数据基础','先分清三个概念：采样点、样本、原始记录。')
para('加速度传感器把机械振动变成随时间变化的数值。计算机读到的可能是一列数字，例如 0.12、-0.08、0.23……每个数字是某个采样时刻的测量值；物理单位由传感器标定与数据说明决定。')
table(['概念','通俗解释','本手册的教学例子'],[
 ['采样点','某个时刻的一个测量值','某一时刻的振动加速度'],
 ['原始记录','一次采集得到的完整连续信号','每条记录 5 秒，采样率 12,000 Hz'],
 ['样本 / 窗口','交给模型处理的一小段信号','每段 1,200 点，即 0.1 秒'],
 ['标签','这段信号对应的已知状态','0=正常；1=内圈故障；2=外圈故障'],
 ],[82,185,CW-267])
box('样本时长 = 点数 ÷ 采样率 = 1,200 ÷ 12,000 = 0.1 秒。<br/>一条 5 秒记录有 60,000 点；不重叠地切分，可得到 50 个样本。','只记住这个换算')
heading('一条波形，本质是一串按顺序排列的数字')
ytop=y; plot_h=84
c.setFillColor(LIGHT);c.roundRect(M,ytop-plot_h,CW,plot_h,5,fill=1,stroke=0)
c.setStrokeColor(TEAL);c.setLineWidth(1)
p=c.beginPath()
for i in range(360):
 t=i/359; v=math.sin(2*math.pi*9*t)*.22+(.72*math.exp(-22*(t-.44))*math.sin(2*math.pi*45*(t-.44)) if t>=.44 else 0)
 xx=M+12+(CW-24)*t; yy=ytop-plot_h/2+v*29
 if i==0:p.moveTo(xx,yy)
 else:p.lineTo(xx,yy)
c.drawPath(p);y-=plot_h+7
para('示意波形：仅用于解释数据形态，不代表某种真实故障，也不能凭这张图下诊断。','small')
heading('怎样打包给模型？')
para('把一段信号记为 x，把它的标签记为 y。例如：x 是长度为 1,200 的数组，y 是数字 1。数字 1 只是“内圈故障”的编号，不表示故障比正常严重一倍。')
para('若一次送入 32 段单通道信号，PyTorch 的一维卷积常用输入形状是 [32, 1, 1200]，分别表示“样本数、通道数、每段点数”。通道数为 1，表示只有一路输入信号。')
para('关键提醒：从一条记录切出的 50 段，不等于做了 50 次独立实验。它们可能共享相同设备、工况和噪声特征。','small')

new('03  数据划分比换网络更重要','建立可信实验','学习类比：训练集是练习题，验证集是模拟题，测试集是最后的考试。')
table(['集合','用来做什么','不该用来做什么'],[
 ['训练集','计算训练损失，更新模型参数。','代替独立测试来宣称泛化能力。'],
 ['验证集','选学习率、训练轮数、模型版本和阈值。','在普通监督训练中用其标签更新权重。'],
 ['测试集','方案固定后，评价对未参与开发数据的表现。','反复查看结果，继续挑模型、选特征。'],
 ],[72,215,CW-287])
heading('最常见的陷阱：把同一条记录切碎后随机混分')
para('假设两个窗口有一半采样点重叠，一个进训练集，一个进测试集，模型就可能在考试时遇到几乎见过的题。即使窗口不重叠，来自同一设备或同一次采集，也仍可能非常相似。')
box('先按设备、试验批次或完整采集记录分组，再在各组内部切片。<br/>如果目标是“新设备也能用”，同一设备的记录要放在同一集合；如果目标是“新工况也能用”，需要单独设计工况外测试。','先决定你想证明哪种泛化能力')
heading('预处理：让输入一致，但保留有用信息')
para('① 检查缺失、异常长度、单位和采样率；核对传感器位置/标定、饱和削顶、掉点与转速/负载记录。② 按固定长度切片。③ 根据任务做去均值或标准化。④ 如果确有需要，再考虑滤波和降噪；不要一上来把所有处理都叠加。')
para('若采用全局标准化，可把每个值减去训练集均值，再除以训练集标准差。验证集、测试集和新数据都使用这组已保存的参数；不能先用全部数据计算参数。[2]')
para('逐段标准化是另一种选择，但会削弱段与段之间的幅值差异。如果幅值变化正是故障严重程度的重要信息，就要谨慎使用，并保留原始数据。')
para('常见的 60%/20%/20% 只是比例示例。独立来源数量、类别覆盖和预期使用场景，比凑比例重要。没有足够独立记录时，应如实说明实验的适用范围。[3]','small')

new('04  CNN 怎样把信号变成类别？','认识模型','CNN：卷积神经网络。先把它理解成“可学习的局部模式检测器”。')
para('卷积核是一小组可调数字。它沿信号滑动，对局部数据做加权计算；每滑到一个位置，就输出一个响应。多个卷积核可以对不同的局部形状产生不同响应，但它们并非天然对应某种故障。')
table(['层 / 模块','做什么','可以怎样理解'],[
 ['一维卷积 Conv1d','从局部信号中计算多个响应序列。','拿多个小探头沿波形扫描。'],
 ['激活函数，例如 ReLU','引入非线性；ReLU 把负响应置零。','让网络能组合更复杂的模式。'],
 ['池化 / 汇总','压缩长度或汇总信息。','把局部观察整理成简要描述。'],
 ['全连接分类层','把特征组合成各类分数。','根据多个线索做综合判断。'],
 ],[130,195,CW-325])
heading('看一个具体的尺寸变化')
para('例如：输入 [32, 1, 1200]；第一层使用 8 个长度为 9 的卷积核，步长为 1，两端各补 4 个零，得到 [32, 8, 1200]。这时每个样本有 8 条特征响应序列。')
para('之后可沿时间维取平均，得到每个样本的 8 个特征，即 [32, 8]；分类层再输出 [32, 3]，对应 3 个类别分数。这是讲解结构用的极简例子，不保证对具体数据效果最好。')
box('某个样本的概率型输出可为：[0.10, 0.75, 0.15]。<br/>若类别顺序是正常、内圈故障、外圈故障，选最大值便得到“内圈故障”。这些数值只是示例；0.75 不保证实际正确率就是 75%。','区分分数、概率和类别')
para('分类层常先输出原始分数，称为 logit。Softmax 将多个分数转换为和为 1 的概率型数值。预测类别通常取最大值；概率是否可信，还涉及后续的校准问题。')
para('“特征图”是卷积层的响应，“类别分数”是最终判断依据之一，“真实故障分量”是物理信号中的组成部分。三者不是同一个东西。','small')

new('05  训练到底在改变什么？','学习过程','训练改变的是权重和偏置；输入标签通常保持不变。')
para('模型开始时的参数一般由初始化规则生成，还没有学会区分故障。训练使用已知标签，反复检查预测与答案的差距，再调整参数。[1,4]')
table(['一次训练更新','发生的事情'],[
 ['1. 取一个批次','例如取 32 段信号，以及它们的 32 个标签。'],
 ['2. 前向计算','输入信号经过网络，得到各个类别的分数。'],
 ['3. 计算损失 loss','用损失函数衡量预测与真实标签的不匹配程度。'],
 ['4. 反向传播','计算损失对每个可训练参数的梯度。'],
 ['5. 优化器更新','根据梯度和学习率调整参数，例如用 Adam 或 SGD。'],
 ['6. 继续下一批','重复上述过程；通常先清除上一批累计的梯度。'],
 ],[125,CW-125])
para('可以把梯度想成“参数朝哪个方向微调，可能使损失下降”的提示。学习率控制每一步改动的尺度。参数太多或学习率过大，都可能让学习变得不稳定。')
heading('三个词：batch、epoch、学习率')
para('batch 是一次更新所用的一批样本。epoch 是完整遍历一遍训练集。学习率是更新步长的控制量。例如训练集有 900 段，batch=32，保留最后不足一批的数据，则每轮有 29 次更新。')
para('卷积核权重属于“模型参数”，由训练学习；学习率、卷积核长度和 batch 大小属于“超参数”，由你设定并参考验证集选择。验证阶段通常不做梯度更新。')
heading('训练结束后，你究竟得到什么？')
para('核心产物是模型结构及其已学习参数，常保存为检查点；还要保存类别映射、标准化参数、输入长度与采样设置。损失曲线、预测结果和特征图是分析材料，不等于模型本身。[5]')
para('入门实现提示：PyTorch 的 CrossEntropyLoss 通常直接接收 logits；不要先手动 Softmax 再把结果交给它。这一点到写代码时再练习。[4]','small')

new('06  怎样判断模型真的学会了？','独立评价','只看训练准确率，无法知道模型能否处理新的数据。')
para('下面是一份人为构造的二分类结果，只用于学习指标。把“故障”当作需要检出的正类。行是真实类别，列是预测类别。[6]')
table(['真实状态 / 预测结果','预测正常','预测故障'],[
 ['真实正常：80 个','76：正确排除','4：误报'],
 ['真实故障：20 个','5：漏报','15：正确检出'],
 ],[220,(CW-220)/2,(CW-220)/2])
table(['指标','怎么算','在这个例子中'],[
 ['准确率 Accuracy','所有样本中，判断正确的比例。','(76+15)/100 = 91%'],
 ['故障召回率 Recall','真实故障中，有多少被检出。','15/20 = 75%'],
 ['故障精确率 Precision','报为故障的样本中，有多少确实故障。','15/(15+4) ≈ 78.9%'],
 ['F1','Precision与Recall的调和平均。','2×15/(2×15+4+5) ≈ 76.9%'],
 ],[120,225,CW-345])
para('虽然总准确率有 91%，仍漏掉了四分之一的故障。类别不平衡时更不能只看准确率：若 100 段中有 99 段正常，全部猜正常也有 99% 准确率，却一个故障都检不出来。')
heading('学会观察三种现象')
para('欠拟合：训练和验证表现都差，可能是模型、输入处理、标签或训练设置不合适。<br/>过拟合：训练越来越好，验证停滞或变差，模型可能记住了训练数据的偶然细节。<br/>数据泄漏：测试表现异常好，原因可能是见过近似样本或使用了测试信息。')
box('至少保留：训练/验证曲线、测试混淆矩阵、各类召回率、数据划分说明、错误样本。以后做论文，还要看不同随机种子、不同设备或工况下的稳定性。','第一个实验的结果清单')
para('划分在哪个层级，结论就受哪个层级约束。来自少量记录的许多窗口，不应被当成大量独立试验来夸大证据。新类别出现时，普通分类器也可能自信地分错。','small')

new('07  用一个完整例子串起来','教学设定 · 非实测','任务：由一段振动信号判断正常、内圈故障或外圈故障。')
para('假设你拥有 30 条相互独立采集的记录，三类各 10 条；每条 5 秒，单通道，采样率 12,000 Hz。这里的数量用于演示流程，不代表公开数据集恰好具有这些独立记录。')
table(['步骤','具体操作','得到什么'],[
 ['任务与标签','固定 0=正常、1=内圈故障、2=外圈故障。','类别映射表'],
 ['按记录划分','每类 6 条训练、2 条验证、2 条测试。','18 / 6 / 6 条记录'],
 ['各集合内部切片','每段 1,200 点，不重叠，每条记录得 50 段。','900 / 300 / 300 个样本'],
 ['预处理','例如只用训练集估计全局均值和标准差。','同一套变换参数'],
 ['建立基线','先做简单统计特征分类器，再训练小型 1D-CNN。','可比较的基本方案'],
 ['训练与选择','用训练集学习；根据验证表现选检查点。','冻结的模型版本'],
 ['独立测试','用 300 段测试样本输出预测，汇总错误。','混淆矩阵与各类指标'],
 ['后续解释','分析模型依赖的频带与信号位置。','待物理验证的候选特征'],
 ],[85,270,CW-355])
box('训练结束后，一条新的 1,200 点信号，经相同预处理送入模型，就可以得到一个类别判断。不需要每来一条新信号，就重新训练一次。','把“训练一次”和“预测一次”分开')
para('公平比较：简单基线和深度网络应使用相同的独立数据划分。基线可以先提取均方根、峰值等统计量，再用简单分类器；如果深度网络没有带来改善，就应检查数据、任务或模型设置。')
para('边界：这份记录级划分不自动证明模型能识别“从未见过的新轴承”。若同一物理轴承贡献多条记录，应按轴承身份分组。窗口 0.1 秒也只是演示值，实际要覆盖足够的故障周期。','small')

new('08  需要学的知识清单','按用途学','不必先把高等数学、信号处理和全部神经网络课程学完。')
table(['知识模块','先学这些','达到这个程度即可继续'],[
 ['Python 与数组','变量、循环、函数；NumPy 数组、切片和 shape。','能读取数组、截取 1,200 点并检查长度。'],
 ['画图与文件','路径、CSV/MAT 文件；折线图、坐标和单位。','能画一段信号，不把采样点编号当秒。'],
 ['信号基础','采样率、时长、幅值；转速与频率；FFT 的作用。','能说明“什么时候变化”和“哪些频率变化”。'],
 ['机械基础','轴承或齿轮的部件、故障类型、激励与传递路径。','知道标签代表什么，不把所有振动都当故障。'],
 ['数学最低准备','向量和矩阵、加权和、平均与标准差、导数直觉。','能理解数据形状、标准化和梯度方向。'],
 ['机器学习基础','样本、标签、训练/验证/测试、分类、过拟合。','能解释为什么测试集不能用于调参。'],
 ['深度学习基础','卷积、激活、池化、损失、梯度、学习率。','能口述一次训练更新，知道权重如何改变。'],
 ['PyTorch 操作','Tensor、Dataset、DataLoader、训练/评价模式、保存。','能跑通一个小型分类网络并重新加载预测。'],
 ['评价与实验','混淆矩阵、召回率、分组划分、简单基线、复现记录。','能看懂失败案例，而不只报告最高准确率。'],
 ],[100,205,CW-305])
heading('哪些内容可以稍后再学？')
para('进入特征挖掘后，再系统学习包络分析、STFT、小波、卷积核频响、Grad-CAM、SHAP，以及解释结果的扰动验证。Transformer、复杂网络融合、完整反向传播推导，不是当前第一道门槛。')
para('优先级：先理解数据和评价，再学小网络；先跑通一个完整流程，再加复杂模块。你已有 Python / MATLAB 基础时，可把更多精力放在信号、划分和训练逻辑上。','small')

new('09  按这个顺序学习与过关','学习路线','按成果推进；不把固定天数当作必须完成的期限。')
table(['阶段','要完成的小任务','可以进入下一步的标志'],[
 ['A  看懂一段信号','读取一条记录；画时域图；计算它的时长。','知道每一轴和单位，能区分点、窗口、记录。'],
 ['B  看懂频率','构造一个正弦信号；改变频率；观察 FFT。','能说清波形变密和频谱峰移动之间的关系。'],
 ['C  组织数据','建立文件清单、标签和组编号；划分后切片。','能说明某条测试记录为何没在训练中出现。'],
 ['D  训练小模型','学习简单基线与 1D-CNN；观察损失变化。','理解输入形状、输出类别和参数更新。'],
 ['E  独立评价','加载选定模型；画混淆矩阵；查看错判。','能说明模型漏检哪一类，以及结论的范围。'],
 ['F  开始解释','冻结模型；分析重要频带，再核查物理含义。','把模型重要性与物理故障来源区分开。'],
 ],[95,220,CW-315])
heading('工具各自负责什么？')
para('NumPy：组织和计算数组。Matplotlib：画信号和结果。SciPy：读取部分科学数据格式、FFT 和信号处理。scikit-learn：基线模型、数据划分和指标。PyTorch：构建、训练和保存神经网络。')
heading('电脑准备到什么程度就够了？')
para('入门小实验可以先使用 CPU，运行速度取决于样本量和网络大小；无需先为 CUDA 问题停下学习。建议为项目创建独立 Conda 环境，保留依赖版本；若现有环境已经能用，先验证基本导入与小样本训练即可。')
box('当前最值得做的小任务：任选一段有采样率说明的振动记录，回答“它有多少点、多少秒、是什么状态、来自哪次采集”。先完成这个任务，再开始调网络。','今天的起点')

new('10  它怎样接上你的特征挖掘？','先诊断，再追问依据','目标：知道模型判断正确时，究竟利用了什么信息。')
para('你希望先有一个能诊断的模型，再挖掘其所学特征，并用这些特征检验判断依据是否合理。基础分类流程跑通以后，就能进入这个阶段。')
table(['层次','实际回答的问题','常见输出'],[
 ['诊断结果','这段信号属于哪个状态？','预测类别和类别分数'],
 ['模型解释','什么输入或内部响应影响了判断？','重要时间片、频带、通道或原型'],
 ['信号提取','能否从混合信号保留候选相关成分？','重构波形、包络或频谱'],
 ['物理验证','这些成分是否与故障机理和独立试验一致？','特征频率、阶次、工况与严重度趋势'],
 ],[82,255,CW-337])
heading('一个以后可以做的解释实验')
para('冻结训练好的模型，记录它对某个样本的故障分数；再抑制一段频带，观察分数是否改变。如果明显下降，只能先说“模型依赖这段频带”。要继续与随机频带、其他解释方法和物理规律对照。')
para('人为删频带会改变信号分布，因此分数变化并不自动证明该频带就是故障源。若你依据解释结果筛选特征，应在训练/验证阶段确定规则，再使用未参与选择的数据检验。')
box('诊断准确 ≠ 判断依据一定正确。<br/>模型认为重要 ≠ 该成分必定由故障产生。<br/>发现合理频带，也不等于已经分离出唯一的物理故障源。','研究中需要保留的三个区别')
heading('怎样使用前面推荐的 TFN？')
para('等你能说清输入、标签、训练与测试后，再读 TFN：先看它如何完成分类，再看可学习时频卷积层怎样支持频带解释。作者提供模型代码和 CWRU 训练流程，可作为后续练习入口。[9]')
para('轴承数据适合练习流程。转向柴油机时，还要考虑燃烧冲击、曲轴角度、转速与负载等因素，不能把轴承的故障特征频率直接套到喷油嘴故障上。','small')

new('11  第一课自测与速查','先回答，再看答案','这页没有编程门槛。能讲明白，比记住缩写更重要。')
heading('六个问题')
para('1. 一条 12,000 Hz 采样的信号有 60,000 点，它持续多久？<br/>2. 每 1,200 点构成一个样本，单样本时长是多少？不重叠能切几段？<br/>3. 训练时主要改变原始信号、标签，还是模型参数？<br/>4. 为什么不能把高度重叠的相邻窗口随意分到训练集和测试集？<br/>5. 模型输出 [0.10, 0.75, 0.15]，类别顺序为正常、内圈、外圈，预测是哪类？<br/>6. 准确率很高，但所有故障都被判断为正常，模型有用吗？应查看什么指标？')
heading('参考答案')
para('1. 5 秒。2. 每段 0.1 秒，共 50 段。3. 权重、偏置等可训练参数。4. 模型可能在测试时遇到几乎见过的数据，造成过于乐观的结果。5. 内圈故障；0.75 不等于经过验证的真实正确率。6. 对检出故障没有帮助，应至少查看故障召回率和混淆矩阵。')
heading('八个词，随时回来查')
table(['术语','一句话记忆'],[
 ['特征 feature','用于区分类别的描述，可以人工计算，也可以由网络学习。'],
 ['张量 tensor','带有形状的多维数值数组，模型处理数据的基本容器。'],
 ['参数 parameter','训练会调整的数字，例如卷积核权重。'],
 ['损失 loss','训练时用来衡量预测与标签不匹配程度的数值。'],
 ['梯度 gradient','提示各参数微小变化怎样影响损失。'],
 ['批次 batch','通常用于一次参数更新的一组样本。'],
 ['轮次 epoch','完整遍历一次训练集。'],
 ['泛化 generalization','在未参与模型开发的新数据上仍能有效工作。'],
 ],[142,CW-142])
para('下一课建议：只学习“一段振动信号怎样画成时域图与频谱”，看清采样率、时间、频率三个概念，再进入 CNN 代码。','small')

new('12  资料与后续阅读','按需查阅','正文中的 [编号] 对应本页；蓝色标题可点击。资料核对日期：2026-10-26。')
refs=[
 ('[1] PyTorch · Learn the Basics','https://docs.pytorch.org/tutorials/beginner/basics/intro.html','入门总路线：张量、数据加载、搭模型、自动求导、优化、保存。'),
 ('[2] scikit-learn · Common pitfalls','https://scikit-learn.org/stable/common_pitfalls.html','重点看数据泄漏；预处理的统计参数只由训练数据拟合。'),
 ('[3] scikit-learn · GroupKFold','https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html','理解同一组不能同时出现在训练折和评价折；具体分组依据由任务决定。'),
 ('[4] PyTorch · Optimizing Model Parameters','https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html','理解损失、反向传播和优化器更新；无需第一天就背代码。'),
 ('[5] PyTorch · Save and Load the Model','https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html','理解模型权重的保存、加载和评价模式。'),
 ('[6] scikit-learn · confusion_matrix','https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html','了解混淆矩阵行列定义；本手册为真实类别在行、预测类别在列。'),
 ('[7] SciPy · Discrete Fourier Transforms','https://docs.scipy.org/doc/scipy/tutorial/fft.html','配合下一课学习 FFT，先理解频谱再看更复杂时频方法。'),
 ('[8] CWRU Bearing Data Center','https://engineering.case.edu/bearingdatacenter/welcome','公开轴承数据入口；先阅读试验装置、采样方式和文件说明。'),
 ('[9] Chen et al. · TFN（2024）','https://doi.org/10.1016/j.ymssp.2023.110952','Mechanical Systems and Signal Processing, 207: 110952。后续模型解释阅读。'),
 ('TFN 作者代码','https://github.com/ChenQian0618/TFN','包含模型、CWRU 数据准备与训练流程；本手册未运行或复现实验。'),
]
for title,url,desc in refs:
 para(f'<link href="{url}" color="#087E8B">{title}</link>','body',gap=2)
 para(desc,'small',gap=9)
box('本手册是一份教学导览，不是实验报告。流程图、演示波形、样本数量、概率和混淆矩阵均为说明概念而设定；不包含模型性能承诺。','使用说明')
exec((Path(__file__).parent/'deep_extra.py').read_text())
exec((Path(__file__).parent/'catalog_pages.py').read_text())
catalog_pages('D')
finish();c.save();save_checks()
