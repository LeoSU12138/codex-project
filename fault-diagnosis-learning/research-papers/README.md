# 故障诊断工程科研论文库

**面向后续科研写作和工程实验的38篇期刊论文，核对日期：2026-10-27。** 其中34篇为方法、应用或基准研究，4篇为综述、教程或综述与比较研究。这里围绕“研究问题—方法—工程验证—可引用内容”整理；[原入门教程与43条学习资料](../README.md)仍保留。

## 文件与使用方式

| 主题 | Excel | 篇数 |
| --- | --- | --- |
| 深度学习诊断与迁移 | [01_深度学习科研论文.xlsx](01_深度学习科研论文.xlsx) | 13 |
| 特征挖掘与故障信号分析 | [02_特征挖掘科研论文.xlsx](02_特征挖掘科研论文.xlsx) | 13 |
| 深度学习、特征挖掘与解释结合 | [03_融合与解释科研论文.xlsx](03_融合与解释科研论文.xlsx) | 12 |

每表有“论文与引用”和“工程验证与复现”两张工作表，通过编号对应。第一张用于选文献和组织相关工作，第二张用于设计对照实验和检查资源条件。表格可筛选，黄色阅读状态可编辑；网址保留为完整文本，本页链接可直接点击。

[BibTeX引文文件](engineering_references.bib) · [RIS引文文件](engineering_references.ris) · [全量CSV](工程科研论文.csv) · [结构化JSON](catalog.json) · [题录来源快照](source_metadata.json)

BibTeX可用于LaTeX，RIS适合导入Zotero、EndNote等软件；最终参考文献样式按投稿期刊要求设置。中文姓名在BibTeX中作为完整姓名保留。编号只在本科研论文库中有效，与旧版入门资料编号不是同一套。

## 最贴近你原始思路的阅读路线

你提出的是“先有诊断模型，再通过特征挖掘检查模型依据”。优先读 **C10（解释如何被检验）→ C09（多层Grad-CAM）→ C06（CS-SHAP）**，再用D02或D07建立普通CNN基线。C06的正式期刊版已于2026年发表，下面使用其正式DOI和完整六位作者。

| 研究路线 | 关键文献 | 你可以形成的实验 |
| --- | --- | --- |
| 冻结模型后解释 | C06、C09、C10 | 用有真值的模拟信号检查定位，再对重要/不重要区域做对照干预，最后在独立测试工况检查稳定性 |
| 从结构上引入信号含义 | C01、C02、C03、C04、C11 | 比较参数化核与普通卷积，检验频响、故障频率和分类表现；这需要改变模型 |
| 特征提取和诊断联合优化 | C07、C08 | 对照传统解卷积、无前端、固定前端、联合训练，并检查输出冲击周期 |
| 柴油机与喷油器工程案例 | D08、D09、F09、F10、F11、C12 | 从故障类型、程度、工况与曲轴角事件组织研究；区分仿真、实验台与现场案例 |

F09和F11可帮助你构造与机理有关的特征，但它们不等同于“事后证明一个深层网络”。注意力图、聚类图或高准确率各自只能回答部分问题。较稳妥的论文表述是：特征分析与对照实验为模型使用故障相关信息提供支持；避免直接声称“证明模型完全正确”。

## 如何把它们用进自己的论文

1. **引言和相关工作：** S01、S02构建领域背景；按实际任务选D、F、C中的原始研究论文，说明已有方法解决了什么、仍有什么限制。
2. **方法：** 使用或改造VMD、FMD、小波核、盲解卷积、Grad-CAM等方法时，引用相应原始论文，并明确你改变的部分。不能仅引用综述替代算法来源。
3. **实验：** D07、S04帮助选统一基线，F12帮助理解CWRU；完整记录独立分组、切片、标准化、种子和超参数。先按设备/运行记录划分，再在各集合内切片。
4. **解释与讨论：** 区分“性能提升”“解释忠实于模型”“解释符合故障机理”。对重要频带、无关频带和随机频带分别干预，检查干预是否造成不合理的分布外信号。选参和解释方案调试用验证集，最终测试集保留到最后。
5. **工程外推：** 同一实验台的跨负载结果不自动代表跨设备或现场有效；目标域无标签数据参与训练属于域适应，不能写成训练时完全未知域的泛化。

“建议借鉴的实验”是本次整理提出的建议，不代表原论文已经做过这些实验。复现难度是材料审阅后的估计；**本次未运行论文训练、未下载全量数据、未复算论文数值**。“未确认作者代码”不等于“没有代码”；已找到代码也不代表全部实验、数据和许可都齐全。

## 检索与核验范围

这是有目的的叙述性文献调研，聚焦机械振动、旋转机械、柴油机及可解释诊断，不是覆盖所有故障诊断方向的系统综述，也不构成论文质量排名。检索出版商页面、Crossref DOI题录、机构页面、开放全文及作者代码页，按题名/DOI去重。部分内容仅能核对摘要或公开片段，范围逐条记录。综述、方法原文、公开基准和工程案例均保留，以满足不同引用用途。

题录采用期刊来源；有卷期年时优先用卷期年，并在表中保留在线年份。C02的Crossref缺少作者，按期刊原页补全中文题名、六位作者和页码；C12出版页仍标注In Press、Journal Pre-proof（在线预校样），尚未给卷期，留空而不推测，投稿前应再次确认最终版本。旧入门资料保留为学习快照，**正式引用与代码状态以本目录更新后的记录为准**。这里提供原创导读和外部链接，不转载付费论文全文。

## 逐篇文献与工程用途

### 深度学习

#### D01 · DNN故障特征学习

Feng Jia; Yaguo Lei; Jing Lin; Xin Zhou; Na Lu. Deep neural networks: A promising tool for fault characteristic mining and intelligent diagnosis of rotating machinery with massive data. Mechanical Systems and Signal Processing, 2016, 72-73: 303-315. [DOI](https://doi.org/10.1016/j.ymssp.2015.10.025)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；轴承、行星齿轮箱 |
| 研究内容 | 手工特征依赖经验，难以处理大量机械信号。 |
| 研究方法 | 深层网络逐层无监督预训练，再用标签微调。 |
| 原文报告的验证 | 四组轴承数据与一组行星齿轮箱数据，比较浅层学习方法。 |
| 适合引用的位置/论点 | 相关工作：机械信号的自动特征学习与深层表征。 |
| 建议借鉴的实验 | 比较浅层分类器与深层网络，并控制输入和数据划分一致。 |
| 复现难度（估计） | 中高：模型可重建，完整原始数据和超参数需核对。 |
| 局限与使用边界 | 学习到可分类特征，不等于已经定位真实物理故障分量。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327015004859)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D02 · WDCNN

Wei Zhang; Gaoliang Peng; Chuanhao Li; Yuanhang Chen; Zhujun Zhang. A New Deep Learning Model for Fault Diagnosis with Good Anti-Noise and Domain Adaptation Ability on Raw Vibration Signals. Sensors, 2017, 17(2): 425. [DOI](https://doi.org/10.3390/s17020425)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；滚动轴承 |
| 研究内容 | 原始振动诊断受到噪声和负载变化影响。 |
| 研究方法 | 首层宽卷积核、小卷积核堆叠和自适应批归一化AdaBN。 |
| 原文报告的验证 | CWRU轴承；噪声、不同负载及特征图分析。 |
| 适合引用的位置/论点 | 方法与基线：一维CNN、宽核去噪及跨负载适应。 |
| 建议借鉴的实验 | 比较宽核与窄核，固定划分后分开报告噪声和跨负载结果。 |
| 复现难度（估计） | 中：结构清楚，作者完整训练包本次未确认。 |
| 局限与使用边界 | AdaBN涉及目标数据统计量；不能据此宣称完全未知域泛化。 |

代码：本次未确认作者代码；未核验完整实现。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；CWRU公开入口；未下载全量数据。

核验范围：DOI题录、开放正文相关部分；未逐项复算实验。 [补充来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC5336047/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D03 · 噪声与变负载CNN

Wei Zhang; Chuanhao Li; Gaoliang Peng; Yuanhang Chen; Zhujun Zhang. A deep convolutional neural network with new training methods for bearing fault diagnosis under noisy environment and different working load. Mechanical Systems and Signal Processing, 2018, 100: 439-453. [DOI](https://doi.org/10.1016/j.ymssp.2017.06.022)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；滚动轴承 |
| 研究内容 | 提高噪声和不同负载下的识别能力。 |
| 研究方法 | 深卷积网络配合训练策略与跨负载处理。 |
| 原文报告的验证 | 轴承振动的噪声及负载变化试验。 |
| 适合引用的位置/论点 | 相关工作：面向复杂工况的卷积诊断。 |
| 建议借鉴的实验 | 设置多个信噪比，分别报告同工况和跨工况表现。 |
| 复现难度（估计） | 中高：需核对训练细节及与D02的差异。 |
| 局限与使用边界 | 与D02属于相关研究，不能当成完全独立的两类技术证据。 |

代码：本次未确认作者代码；未核验完整实现。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；CWRU公开入口；未下载全量数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2017.06.022)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D04 · 信号图像化CNN

Long Wen; Xinyu Li; Liang Gao; Yuyan Zhang. A New Convolutional Neural Network-Based Data-Driven Fault Diagnosis Method. IEEE Transactions on Industrial Electronics, 2018, 65(7): 5990-5998. [DOI](https://doi.org/10.1109/tie.2017.2774777)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；制造设备故障诊断 |
| 研究内容 | 减少对人工设计特征的依赖。 |
| 研究方法 | 把信号转换成二维图像，再使用基于LeNet-5的CNN。 |
| 原文报告的验证 | 论文进行诊断方法比较；具体数据划分需全文核对。 |
| 适合引用的位置/论点 | 方法与基线：信号图像化输入的CNN诊断。 |
| 建议借鉴的实验 | 与原始一维信号输入比较，检查重排是否改变局部关联。 |
| 复现难度（估计） | 中高：转换规则、训练配置和数据须按全文实现。 |
| 局限与使用边界 | 题录与出版摘要可核对，未全面核验各数据集实验细节。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1109/TIE.2017.2774777)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D05 · 深度迁移诊断

Siyu Shao; Stephen McAleer; Ruqiang Yan; Pierre Baldi. Highly Accurate Machine Fault Diagnosis Using Deep Transfer Learning. IEEE Transactions on Industrial Informatics, 2019, 15(4): 2446-2455. [DOI](https://doi.org/10.1109/tii.2018.2864759)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；机械故障数据 |
| 研究内容 | 减少诊断网络训练对大量标注样本的依赖。 |
| 研究方法 | 时频表征与预训练网络迁移学习。 |
| 原文报告的验证 | 机械数据诊断；作者提供配套数据门户。 |
| 适合引用的位置/论点 | 相关工作：利用已有深层表征进行机械诊断。 |
| 建议借鉴的实验 | 比较从零训练、冻结主干和微调，控制可用标签数量。 |
| 复现难度（估计） | 中高：数据入口明确，完整训练代码本次未确认。 |
| 局限与使用边界 | 图像预训练的有效性需要按信号转换和目标任务验证。 |

代码：本次未确认作者代码；未核验完整实现。数据：[数据入口](https://mlmechanics.ics.uci.edu/)；作者配套数据门户；下载完整性未测试。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://mlmechanics.ics.uci.edu/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D06 · DCTLN

Liang Guo; Yaguo Lei; Saibo Xing; Tao Yan; Naipeng Li. Deep Convolutional Transfer Learning Network: A New Method for Intelligent Fault Diagnosis of Machines With Unlabeled Data. IEEE Transactions on Industrial Electronics, 2019, 66(9): 7316-7325. [DOI](https://doi.org/10.1109/tie.2018.2877090)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；跨设备机械故障诊断 |
| 研究内容 | 源域有标签，目标域无标签，且分布不同。 |
| 研究方法 | 一维卷积特征、状态识别和域适应联合学习。 |
| 原文报告的验证 | 机械故障跨域诊断；源/目标划分按论文定义。 |
| 适合引用的位置/论点 | 相关工作：无标签目标域的迁移诊断。 |
| 建议借鉴的实验 | 对照源域直接训练与域适应，单列目标标签使用规则。 |
| 复现难度（估计） | 中高：需重建联合训练流程，独立作者代码未确认。 |
| 局限与使用边界 | 属于域适应，训练时能接触目标域数据。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://xplorestaging.ieee.org/document/8511076/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D07 · 开源深度诊断基准

Zhibin Zhao; Tianfu Li; Jingyao Wu; Chuang Sun; Shibin Wang; Ruqiang Yan; Xuefeng Chen. Deep learning algorithms for rotating machinery intelligent diagnosis: An open source benchmark study. ISA Transactions, 2020, 107: 224-255. [DOI](https://doi.org/10.1016/j.isatra.2020.08.010)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；轴承与齿轮箱 |
| 研究内容 | 不同论文使用不同数据处理流程，结果难公平比较。 |
| 研究方法 | 统一多种深度网络、数据接口与评价流程。 |
| 原文报告的验证 | 作者仓库涵盖CWRU、PU、MFPT、SEU、XJTU-SY等接口。 |
| 适合引用的位置/论点 | 实验设计：选基线、统一预处理和评价协议。 |
| 建议借鉴的实验 | 先建立统一训练脚本，再加入自己的模块；重新设计独立分组划分。 |
| 复现难度（估计） | 中：有训练脚本，需更新环境并整理数据。 |
| 局限与使用边界 | 仓库包含随机切分等设置，不能不加检查地沿用；依赖较旧。 |

代码：[已确认作者仓库](https://github.com/ZhaoZhibin/DL-based-Intelligent-Diagnosis-Benchmark)；模型、数据加载和训练脚本；未运行。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；多个公开数据集，其他入口见作者README。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://github.com/ZhaoZhibin/DL-based-Intelligent-Diagnosis-Benchmark)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D08 · 柴油机跨场景迁移

Junhong Zhang; Guobin Pei; Xiaolong Zhu; Xin Gou; Linlong Deng; Lang Gao; Zewei Liu; Qing Ni; Jiewei Lin. Diesel engine fault diagnosis for multiple industrial scenarios based on transfer learning. Measurement, 2024, 228: 114338. [DOI](https://doi.org/10.1016/j.measurement.2024.114338)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；柴油机 |
| 研究内容 | 样本有限且工业场景变化时的诊断迁移。 |
| 研究方法 | 宽卷积核CNN-LSTM（WCL）与深度迁移学习。 |
| 原文报告的验证 | 论文报告多场景柴油机诊断；完整原始数据本次未确认。 |
| 适合引用的位置/论点 | 相关工作：柴油机低信噪比与跨场景诊断。 |
| 建议借鉴的实验 | 划分转速、负载、设备等迁移方向，分别测试各方向。 |
| 复现难度（估计） | 高：模型可参考，完整数据获取是主要障碍。 |
| 局限与使用边界 | 多场景试验不意味着对任意柴油机或喷油器故障都适用。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://opus.lib.uts.edu.au/handle/10453/186632)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D09 · MACNN柴油机诊断

Xiao Yang; Fengrong Bi; Jiangang Cheng; Daijie Tang; Pengfei Shen; Xiaoyang Bi. A Multiple Attention Convolutional Neural Networks for Diesel Engine Fault Diagnosis. Sensors, 2024, 24(9): 2708. [DOI](https://doi.org/10.3390/s24092708)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；柴油机振动 |
| 研究内容 | 端到端识别多个故障类型及不同程度。 |
| 研究方法 | CNN、改进卷积块注意力、自注意力与特征序列重组。 |
| 原文报告的验证 | 故障设置包括气门间隙、轨压、供油不足；多转速八类任务。 |
| 适合引用的位置/论点 | 工程案例：柴油机振动诊断的注意力网络设计。 |
| 建议借鉴的实验 | 分别去掉通道、空间、自注意力模块，并报告推理耗时。 |
| 复现难度（估计） | 中高：全文开放，完整数据与作者训练包未确认。 |
| 局限与使用边界 | 人工设置故障的试验结论不能直接等同长期现场性能。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、开放正文相关部分；未逐项复算实验。 [补充来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC11086139/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### D10 · CWT时频图CNN

Sheng Guo; Tao Yang; Wei Gao; Chen Zhang. A Novel Fault Diagnosis Method for Rotating Machinery Based on a Convolutional Neural Network. Sensors, 2018, 18(5): 1429. [DOI](https://doi.org/10.3390/s18051429)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；转子设备 |
| 研究内容 | 人工统计特征可能丢失信号信息。 |
| 研究方法 | 连续小波变换得到时频图，由CNN分类。 |
| 原文报告的验证 | 转子实验台，并在另一台转子设备上验证。 |
| 适合引用的位置/论点 | 方法与工程案例：时频表征结合CNN。 |
| 建议借鉴的实验 | 比较原始波形、频谱和CWT输入；验证不同设备迁移。 |
| 复现难度（估计） | 中高：方法与全文可读，原实验台数据未确认公开。 |
| 局限与使用边界 | 时频图准确率不直接解释模型关注的物理成分。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、开放正文相关部分；未逐项复算实验。 [补充来源](https://doi.org/10.3390/s18051429)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### S01 · 机器健康监测深度学习综述

Rui Zhao; Ruqiang Yan; Zhenghua Chen; Kezhi Mao; Peng Wang; Robert X. Gao. Deep learning and its applications to machine health monitoring. Mechanical Systems and Signal Processing, 2019, 115: 213-237. [DOI](https://doi.org/10.1016/j.ymssp.2018.05.050)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 综述/教程；机器健康监测 |
| 研究内容 | 梳理深度学习在机器健康监测中的应用。 |
| 研究方法 | 分类总结AE、DBN、CNN、RNN等方法。 |
| 原文报告的验证 | 综述，不是单一复现实验。 |
| 适合引用的位置/论点 | 引言：领域方法发展与已有应用。 |
| 建议借鉴的实验 | 按综述的引用追踪原始方法论文。 |
| 复现难度（估计） | 不适用：综述。 |
| 局限与使用边界 | 适合领域背景；具体算法创新应同时引用原始论文。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://arxiv.org/abs/1612.07640)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### S02 · 机器故障诊断路线图

Yaguo Lei; Bin Yang; Xinwei Jiang; Feng Jia; Naipeng Li; Asoke K. Nandi. Applications of machine learning to machine fault diagnosis: A review and roadmap. Mechanical Systems and Signal Processing, 2020, 138: 106587. [DOI](https://doi.org/10.1016/j.ymssp.2019.106587)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 综述/教程；机械故障诊断 |
| 研究内容 | 概括机器学习诊断技术与挑战。 |
| 研究方法 | 传统学习、深度学习和迁移学习路线综述。 |
| 原文报告的验证 | 综述，不是单一实验。 |
| 适合引用的位置/论点 | 引言：研究现状、数据与泛化挑战。 |
| 建议借鉴的实验 | 用其分类框架组织自己的相关工作。 |
| 复现难度（估计） | 不适用：综述。 |
| 局限与使用边界 | 不能代替具体算法、数据集和实验结论的原文。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2019.106587)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### S04 · UDTL综述与比较

Zhibin Zhao; Qiyang Zhang; Xiaolei Yu; Chuang Sun; Shibin Wang; Ruqiang Yan; Xuefeng Chen. Applications of Unsupervised Deep Transfer Learning to Intelligent Fault Diagnosis: A Survey and Comparative Study. IEEE Transactions on Instrumentation and Measurement, 2021, 70: 1-28. [DOI](https://doi.org/10.1109/tim.2021.3116309)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 综述与基准比较；跨域机械故障诊断 |
| 研究内容 | 统一比较无监督深度迁移诊断方法。 |
| 研究方法 | 综述与统一基准，含映射式、对抗式及AdaBN等方法。 |
| 原文报告的验证 | 公开代码包括CWRU、PU、PHM2009、SEU、JNU数据接口。 |
| 适合引用的位置/论点 | 引言与实验设计：迁移设定、基线和标签可见性。 |
| 建议借鉴的实验 | 用统一网络和划分比较迁移损失，固定目标标签使用规则。 |
| 复现难度（估计） | 中高：作者工程完整但依赖老旧，需记录环境迁移。 |
| 局限与使用边界 | 不要把所有迁移设置都概括成未知工况泛化。 |

代码：[已确认作者仓库](https://github.com/ZhaoZhibin/UDTL)；多种迁移方法与训练入口；未运行。数据：[数据入口](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download)；多个公开数据集，见作者README。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://github.com/ZhaoZhibin/UDTL)。Crossref DOI题录；优先使用卷期年，在线年另列。

### 特征挖掘

#### F01 · 稀疏过滤特征学习

Yaguo Lei; Feng Jia; Jing Lin; Saibo Xing; Steven X. Ding. An Intelligent Fault Diagnosis Method Using Unsupervised Feature Learning Towards Mechanical Big Data. IEEE Transactions on Industrial Electronics, 2016, 63(5): 3137-3147. [DOI](https://doi.org/10.1109/tie.2016.2519325)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；电机与机车轴承 |
| 研究内容 | 用自动学习替代劳动密集的人工特征工程。 |
| 研究方法 | 两层稀疏过滤网络学习特征，再用softmax分类。 |
| 原文报告的验证 | 电机轴承与机车轴承两组数据。 |
| 适合引用的位置/论点 | 相关工作：无监督机械特征学习。 |
| 建议借鉴的实验 | 比较原始特征、人工特征及学习特征的下游分类表现。 |
| 复现难度（估计） | 中高：网络较简洁，完整数据和实现需核对。 |
| 局限与使用边界 | 无监督特征学习与训练后解释是不同任务。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://scholar.xjtu.edu.cn/en/publications/an-intelligent-fault-diagnosis-method-using-unsupervised-feature-/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F02 · 谱峭度理论

Jérôme Antoni. The spectral kurtosis: a useful tool for characterising non-stationary signals. Mechanical Systems and Signal Processing, 2006, 20(2): 282-307. [DOI](https://doi.org/10.1016/j.ymssp.2004.09.001)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；非平稳信号 |
| 研究内容 | 定位瞬态成分所在的频带。 |
| 研究方法 | 谱峭度的统计定义与估计。 |
| 原文报告的验证 | 非平稳信号方法研究；不是独立深度分类项目。 |
| 适合引用的位置/论点 | 方法依据：为什么用谱峭度衡量频带中的瞬态性。 |
| 建议借鉴的实验 | 在已知冲击频带的模拟信号上检验频带定位。 |
| 复现难度（估计） | 中：数学理解有门槛，信号示例可自行构造。 |
| 局限与使用边界 | 高峭度可能来自偶发干扰，不能单独判定周期故障。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327004001517)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F03 · Fast Kurtogram

Jérôme Antoni. Fast computation of the kurtogram for the detection of transient faults. Mechanical Systems and Signal Processing, 2007, 21(1): 108-124. [DOI](https://doi.org/10.1016/j.ymssp.2005.12.002)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；瞬态机械故障信号 |
| 研究内容 | 高效寻找适合解调的中心频率和带宽。 |
| 研究方法 | 滤波器组上的快速峭度图计算。 |
| 原文报告的验证 | 瞬态检测方法及信号示例；作者发布MATLAB实现。 |
| 适合引用的位置/论点 | 方法与基线：解调频带选择。 |
| 建议借鉴的实验 | 对比手选频带和自动选频带，再观察包络谱故障周期。 |
| 复现难度（估计） | 中：作者代码可用；参数解释与结果判断仍需信号知识。 |
| 局限与使用边界 | 所选带宽依赖滤波器和分辨率设置，也可能受脉冲噪声影响。 |

代码：[已确认作者代码页](https://www.mathworks.com/matlabcentral/fileexchange/48912-fast-kurtogram)；MATLAB函数与演示；未运行。数据：提供信号演示；完整原论文数据未确认。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已核对作者代码页说明；未执行。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327005002414)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F04 · MCKD

Geoff L. McDonald; Qing Zhao; Ming J. Zuo. Maximum correlated Kurtosis deconvolution and application on gear tooth chip fault detection. Mechanical Systems and Signal Processing, 2012, 33: 237-255. [DOI](https://doi.org/10.1016/j.ymssp.2012.06.010)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；齿轮齿面缺损 |
| 研究内容 | 从振动混合信号中增强重复冲击。 |
| 研究方法 | 最大相关峭度目标下的盲解卷积。 |
| 原文报告的验证 | 有/无齿缺损的齿轮箱振动比较。 |
| 适合引用的位置/论点 | 方法与基线：周期冲击提取和盲解卷积。 |
| 建议借鉴的实验 | 比较MED与MCKD，并扰动预设故障周期和滤波器长度。 |
| 复现难度（估计） | 中：作者提供MATLAB函数，完整实验数据需核对。 |
| 局限与使用边界 | 周期先验与滤波器长度会影响结果；输出不是自动获得的真实源。 |

代码：[原论文链接作者代码](https://www.mathworks.com/matlabcentral/fileexchange/31326)；MCKD MATLAB实现；未下载核验。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327012002452)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F05 · MOMEDA

Geoff L. McDonald; Qing Zhao. Multipoint Optimal Minimum Entropy Deconvolution and Convolution Fix: Application to vibration fault detection. Mechanical Systems and Signal Processing, 2017, 82: 461-477. [DOI](https://doi.org/10.1016/j.ymssp.2016.05.036)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；齿轮箱 |
| 研究内容 | 避免只增强单次冲击，提取与故障周期一致的冲击列。 |
| 研究方法 | 用目标冲击向量构建解卷积问题，直接求解滤波器。 |
| 原文报告的验证 | 仿真和有/无人工齿缺损齿轮箱试验。 |
| 适合引用的位置/论点 | 方法与基线：非迭代滤波求解及周期冲击提取。 |
| 建议借鉴的实验 | 扫描候选故障周期，比较输出包络谱与已知齿轮周期。 |
| 复现难度（估计） | 中：作者MATLAB代码可得。 |
| 局限与使用边界 | 非迭代指给定目标下的滤波求解，周期和参数选择仍需设计。 |

代码：[已确认作者代码页](https://www.mathworks.com/matlabcentral/fileexchange/53483-multipoint-optimal-minimum-entropy-deconvolution-with-convolution-adjustment-momeda)；MOMEDA MATLAB函数；未运行。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已核对作者代码页说明；未执行。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327016301297)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F06 · Fast Spectral Correlation

Jérôme Antoni; Ge Xin; Nacer Hamzaoui. Fast computation of the spectral correlation. Mechanical Systems and Signal Processing, 2017, 92: 248-277. [DOI](https://doi.org/10.1016/j.ymssp.2017.01.011)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；轴承循环平稳信号 |
| 研究内容 | 降低循环谱分析的计算开销。 |
| 研究方法 | 基于STFT的快速谱相关估计。 |
| 原文报告的验证 | 弱轴承特征和转速变化场景。 |
| 适合引用的位置/论点 | 方法依据：载频与调制频率的二维描述。 |
| 建议借鉴的实验 | 把循环谱与普通频谱、包络谱并列分析；检查分辨率。 |
| 复现难度（估计） | 中高：作者代码有模拟演示，理论与参数门槛较高。 |
| 局限与使用边界 | 循环频率不等于载频；两轴含义必须区分。 |

代码：[已确认作者代码页](https://www.mathworks.com/matlabcentral/fileexchange/60561-fast_sc-x-nw-alpha_max-fs-opt)；Fast_SC与模拟演示；未运行。数据：作者模拟信号演示；原试验数据未确认。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已核对作者代码页说明；未执行。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327017300134)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F07 · VMD

Konstantin Dragomiretskiy; Dominique Zosso. Variational Mode Decomposition. IEEE Transactions on Signal Processing, 2014, 62(3): 531-544. [DOI](https://doi.org/10.1109/tsp.2013.2288675)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；信号模态分解 |
| 研究内容 | 同时估计若干带限模态及其中心频率。 |
| 研究方法 | 变分优化与交替方向乘子法。 |
| 原文报告的验证 | 方法论文及作者信号示例。 |
| 适合引用的位置/论点 | 方法依据：VMD分解算法的原始出处。 |
| 建议借鉴的实验 | 与原信号或其他分解法比较，对K与惩罚参数做敏感性分析。 |
| 复现难度（估计） | 中：作者MATLAB实现公开，模式数选择需学习。 |
| 局限与使用边界 | 算法原文不是某种设备的通用故障验证；模态不保证对应物理源。 |

代码：[已确认作者代码页](https://math.montana.edu/dzosso/code/)；原始VMD MATLAB代码；未运行。数据：作者示例；不是特定机械故障数据库。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已核对作者代码页说明；未执行。 [补充来源](https://math.montana.edu/dzosso/code/)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F08 · FMD

Yonghao Miao; Boyao Zhang; Chenhui Li; Jing Lin; Dayi Zhang. Feature Mode Decomposition: New Decomposition Theory for Rotating Machinery Fault Diagnosis. IEEE Transactions on Industrial Electronics, 2023, 70(2): 1949-1960. [DOI](https://doi.org/10.1109/tie.2022.3156156)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；旋转机械冲击故障 |
| 研究内容 | 用冲击性和周期性目标提取故障模态。 |
| 研究方法 | 以机械故障特征为目标的自适应滤波分解。 |
| 原文报告的验证 | 旋转机械诊断；作者代码可复现部分论文结果。 |
| 适合引用的位置/论点 | 方法与基线：面向故障特征的模态分解。 |
| 建议借鉴的实验 | 与VMD、MCKD比较，并检验滤波长度和模态数。 |
| 复现难度（估计） | 中：有作者MATLAB包，完整结果需核对数据与参数。 |
| 局限与使用边界 | 目标函数偏好特定信号结构，不能把每个模态直接命名为真实故障。 |

代码：[已确认作者代码页](https://www.mathworks.com/matlabcentral/fileexchange/108099-feature-mode-decomposition-fmd)；可复现部分论文结果；未运行。数据：作者包中的示例范围需下载后核验。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已核对作者代码页说明；未执行。 [补充来源](https://www.mathworks.com/matlabcentral/fileexchange/108099-feature-mode-decomposition-fmd)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F09 · 柴油机自适应稀疏注意力

He Li; Jinjie Zhang; Zhenjing Zhang; Zhinong Jiang; Zhiwei Mao. Priori-distribution-guided adaptive sparse attention for cross-domain feature mining in diesel engine fault diagnosis. Engineering Applications of Artificial Intelligence, 2024, 132: 107975. [DOI](https://doi.org/10.1016/j.engappai.2024.107975)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；柴油机 |
| 研究内容 | 筛选跨域故障敏感特征并降低模型复杂度。 |
| 研究方法 | 结合热力学/动力学先验，从时域、频域、包络域构造特征并用稀疏注意力学习。 |
| 原文报告的验证 | 柴油机故障诊断；完整原始数据未确认公开。 |
| 适合引用的位置/论点 | 工程案例：有物理含义的特征集与自适应特征加权。 |
| 建议借鉴的实验 | 比较不同信号域、筛选前后特征和不同工况下的重要性。 |
| 复现难度（估计） | 高：特征定义和采集条件必须对齐，数据获取受限。 |
| 局限与使用边界 | 权重是模型内选择依据；仍需遮蔽和独立工况实验。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0952197624001337)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F10 · 船用发动机对数签名

Chaitanya Patil; Gerasimos Theotokatos; Yue Wu; Terry Lyons. Investigation of logarithmic signatures for feature extraction and application to marine engine fault diagnosis. Engineering Applications of Artificial Intelligence, 2024, 138: 109299. [DOI](https://doi.org/10.1016/j.engappai.2024.109299)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；大型四冲程船用柴油机 |
| 研究内容 | 从缸压序列中提取故障表征。 |
| 研究方法 | 路径对数签名特征用于故障诊断。 |
| 原文报告的验证 | 经验证的物理数字孪生产生缸压，覆盖故障组合、程度和工况。 |
| 适合引用的位置/论点 | 工程案例：动力学仿真数据与时序特征构造。 |
| 建议借鉴的实验 | 改变故障程度与工况，检验特征的稳定性和区分性。 |
| 复现难度（估计） | 高：需要数字孪生、参数和缸压数据。 |
| 局限与使用边界 | 核心数据由数字孪生产生，不能写成全部来自现场实测。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://www.sciencedirect.com/science/article/pii/S095219762401457X)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F11 · 喷油器类型与程度识别

Yun Ke; Enzhe Song; Chong Yao; Shunliang Ding; Yilin Ning; Rui Li. Refined composite hierarchical bidirectional diversity entropy and its application in fault type diagnosis and fault degree diagnosis of diesel engine fuel injectors. Journal of Vibration and Control, 2024, 30(21-22): 5047-5059. [DOI](https://doi.org/10.1177/10775463231217530)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；柴油机喷油器 |
| 研究内容 | 同时描述喷油器故障类型和故障程度。 |
| 研究方法 | 精细复合层次双向散布熵RCHBDE与海鸥算法优化SVM。 |
| 原文报告的验证 | 模拟信号和喷油器故障试验数据。 |
| 适合引用的位置/论点 | 工程案例：故障敏感特征及故障程度分析。 |
| 建议借鉴的实验 | 用不同故障程度作趋势分析，并把工况变化作为混杂因素控制。 |
| 复现难度（估计） | 高：原数据未确认公开；熵定义及参数需逐式核对。 |
| 局限与使用边界 | 它是特征工程加SVM，不属于深度网络事后解释。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://journals.sagepub.com/doi/10.1177/10775463231217530)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### F12 · CWRU诊断基准分析

Wade A. Smith; Robert B. Randall. Rolling element bearing diagnostics using the Case Western Reserve University data: A benchmark study. Mechanical Systems and Signal Processing, 2015, 64-65: 100-131. [DOI](https://doi.org/10.1016/j.ymssp.2015.04.021)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；滚动轴承 |
| 研究内容 | 明确常用公开数据中的可诊断信号和困难情况。 |
| 研究方法 | 对CWRU数据进行机械信号诊断分析与基准评估。 |
| 原文报告的验证 | CWRU公开轴承数据。 |
| 适合引用的位置/论点 | 数据说明与讨论：基准数据的特点、适用性和限制。 |
| 建议借鉴的实验 | 先检查原始频谱、包络谱与故障标签，避免直接切片训练。 |
| 复现难度（估计） | 中：公开数据可用，信号分析需要机理知识。 |
| 局限与使用边界 | 这是数据与诊断基准研究，不能代替现场有效性证据。 |

代码：本次未确认作者代码；未核验完整实现。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；CWRU公开入口；未下载全量数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2015.04.021)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### S03 · 轴承诊断机理教程论文

Robert B. Randall; Jérôme Antoni. Rolling element bearing diagnostics—A tutorial. Mechanical Systems and Signal Processing, 2011, 25(2): 485-520. [DOI](https://doi.org/10.1016/j.ymssp.2010.07.017)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 综述/教程；滚动轴承 |
| 研究内容 | 把故障机理与振动信号处理连接起来。 |
| 研究方法 | 轴承振动、调制、包络及诊断方法的系统讲解。 |
| 原文报告的验证 | 期刊教程/综述，包含机理与诊断分析。 |
| 适合引用的位置/论点 | 机理依据：解释轴承特征频率与解调结果。 |
| 建议借鉴的实验 | 先由几何和转速确定预期故障频率，再检查模型关注频带。 |
| 复现难度（估计） | 中高：阅读理论，不是统一训练复现任务。 |
| 局限与使用边界 | 轴承机理不能原样套到柴油机燃烧与喷油故障。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2010.07.017)。Crossref DOI题录；优先使用卷期年，在线年另列。

### 融合与解释

#### C01 · TFN

Qian Chen; Xingjian Dong; Guowei Tu; Dong Wang; Changming Cheng; Baoxuan Zhao; Zhike Peng. TFN: An interpretable neural network with time-frequency transform embedded for intelligent fault diagnosis. Mechanical Systems and Signal Processing, 2024, 207: 110952. [DOI](https://doi.org/10.1016/j.ymssp.2023.110952)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；机械振动故障诊断 |
| 研究内容 | 让卷积前端的响应具有时频意义。 |
| 研究方法 | 把可学习时频变换嵌入卷积层。 |
| 原文报告的验证 | 三项机械诊断实验；仓库提供CWRU完整准确率流程。 |
| 适合引用的位置/论点 | 方法与相关工作：可解释滤波前端。 |
| 建议借鉴的实验 | 对比随机核、普通CNN及参数化核，展示频率响应与分类表现。 |
| 复现难度（估计） | 中：作者有CWRU训练流程与模型。 |
| 局限与使用边界 | 前端可解释不意味着所有后续层透明；复现包不覆盖全部实验。 |

代码：[已确认作者仓库](https://github.com/ChenQian0618/TFN)；核心模型、CWRU训练及统计流程；未运行。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；CWRU公开；其余论文数据未确认全部开放。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://github.com/ChenQian0618/TFN)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C02 · Chirplet可解释CNN

陈钱; 陈康康; 董兴建; 皇甫一樊; 彭志科; 孟光. 一种面向机械设备故障诊断的可解释卷积神经网络. 机械工程学报, 2024, 60(12): 65-76. [DOI](https://doi.org/10.3901/jme.2024.12.065)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；机械设备 |
| 研究内容 | 为卷积核赋予可辨识的信号处理含义。 |
| 研究方法 | 基于Chirplet参数化核的卷积特征提取。 |
| 原文报告的验证 | 机械故障诊断案例；本次未确认独立完整复现包。 |
| 适合引用的位置/论点 | 中文相关工作：物理可解释卷积网络。 |
| 建议借鉴的实验 | 从卷积核参数、频率响应和故障谱结构建立对应关系。 |
| 复现难度（估计） | 中高：中文易读，完整代码和数据未确认。 |
| 局限与使用边界 | TFN相关仓库不能自动当作本论文完整代码。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI、期刊原页题录及摘要；完整实验须读全文。 [补充来源](https://qikan.cmes.org/jxgcxb/CN/10.3901/JME.2024.12.065)。Crossref DOI题录；优先使用卷期年，在线年另列。 中文题名、完整作者及65–76页据期刊原页补全。

#### C03 · WaveletKernelNet

Tianfu Li; Zhibin Zhao; Chuang Sun; Li Cheng; Xuefeng Chen; Ruqiang Yan; Robert X. Gao. WaveletKernelNet: An Interpretable Deep Neural Network for Industrial Intelligent Diagnosis. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2022, 52(4): 2302-2312. [DOI](https://doi.org/10.1109/tsmc.2020.3048950)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；工业机械诊断 |
| 研究内容 | 使第一层特征提取具有小波分析含义。 |
| 研究方法 | 可学习小波卷积核与后续深层网络。 |
| 原文报告的验证 | 论文机械诊断实验；作者模型可接入D07基准。 |
| 适合引用的位置/论点 | 方法与基线：小波参数化卷积核。 |
| 建议借鉴的实验 | 比较不同母小波、普通卷积和固定小波参数。 |
| 复现难度（估计） | 中：模型公开，训练需整合基准工程。 |
| 局限与使用边界 | 公开仓库主要提供模型，完整训练与数据流程需另行接入。 |

代码：[已确认作者仓库](https://github.com/HazeDT/WaveletKernelNet)；主要为模型，需接D07基准；未运行。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；建议接公开数据复现；不等于已复现原论文全部数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://github.com/HazeDT/WaveletKernelNet)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C04 · Frequency Activation Map

Min Su Kim; Jong Pil Yun; Poogyeon Park. An Explainable Neural Network for Fault Diagnosis With a Frequency Activation Map. IEEE Access, 2021, 9: 98962-98972. [DOI](https://doi.org/10.1109/access.2021.3095565)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；机械故障诊断 |
| 研究内容 | 把分类依据映射为可读的频率区域。 |
| 研究方法 | 可解释网络及频率激活图FAM。 |
| 原文报告的验证 | 论文故障诊断实验；完整数据和代码本次未确认。 |
| 适合引用的位置/论点 | 方法与相关工作：频域解释的网络设计。 |
| 建议借鉴的实验 | 检查高激活频段是否对应已知故障频率，并做频带干预。 |
| 复现难度（估计） | 中高：需要实现网络约束与频率映射。 |
| 局限与使用边界 | 频率图是模型依据的证据，不是物理因果证明。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1109/ACCESS.2021.3095565)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C05 · 原型匹配解释

Qian Chen; Xingjian Dong; Zhike Peng. Interpreting what typical fault signals look like via prototype-matching. Advanced Engineering Informatics, 2024, 62: 102849. [DOI](https://doi.org/10.1016/j.aei.2024.102849)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；典型故障频谱 |
| 研究内容 | 展示模型认为典型的故障信号形态。 |
| 研究方法 | 原型匹配、编码/重构及重要区域分析。 |
| 原文报告的验证 | 故障信号原型解释实验；完整原数据与官方代码未确认。 |
| 适合引用的位置/论点 | 方法与相关工作：案例式/原型式可解释诊断。 |
| 建议借鉴的实验 | 比较原型与真实样本，检查是否包含故障频率及侧频结构。 |
| 复现难度（估计） | 中高：需复现原型构造及训练细节。 |
| 局限与使用边界 | 原型是模型学习的代表模式，不一定就是物理源或真实测量样本。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://arxiv.org/abs/2403.07033)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C06 · CS-SHAP

Qian Chen; Xingjian Dong; Kui Hu; Kangkang Chen; Zhike Peng; Guang Meng. CS-SHAP: Extending SHAP to cyclic-spectral domain for better interpretability of intelligent fault diagnosis. Mechanical Systems and Signal Processing, 2026, 257: 114495. [DOI](https://doi.org/10.1016/j.ymssp.2026.114495)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；已训练机械诊断网络 |
| 研究内容 | 原始时域归因难同时展示载频和调制特征。 |
| 研究方法 | 将SHAP归因扩展到循环谱域。 |
| 原文报告的验证 | 三个数据集；作者提供模拟数据和CWRU演示。 |
| 适合引用的位置/论点 | 方法与核心相关工作：冻结模型后的故障特征归因。 |
| 建议借鉴的实验 | 先用已知真值模拟信号，比较时间、频率、包络、时频和循环谱归因。 |
| 复现难度（估计） | 中高：有演示代码，但SHAP版本与计算开销需处理。 |
| 局限与使用边界 | 归因依赖背景样本和扰动方式；它解释预测，不自动证明因果。 |

代码：[已确认作者仓库](https://github.com/ChenQian0618/CS-SHAP)；多信号域SHAP与模拟/CWRU演示；未运行。数据：[数据入口](https://engineering.case.edu/bearingdatacenter/download-data-file)；模拟与CWRU可开始；第三组数据完整获取未核验。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://www.sciencedirect.com/science/article/pii/S0888327026006527)。Crossref DOI题录；优先使用卷期年，在线年另列。 采用2026年正式期刊版；保留全部六位作者，包括Guang Meng。

#### C07 · ClassBD

Jing-Xiao Liao; Chao He; Jipu Li; Jinwei Sun; Shiping Zhang; Xiaoge Zhang. Classifier-guided neural blind deconvolution: A physics-informed denoising module for bearing fault diagnosis under noisy conditions. Mechanical Systems and Signal Processing, 2025, 222: 111750. [DOI](https://doi.org/10.1016/j.ymssp.2024.111750)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；噪声下的轴承故障 |
| 研究内容 | 在噪声中提取有利于诊断的重复冲击。 |
| 研究方法 | 时域二次滤波、频域线性滤波与分类器联合训练。 |
| 原文报告的验证 | 作者工程包含PU与JNU数据处理和训练入口。 |
| 适合引用的位置/论点 | 方法与基线：故障成分增强和分类联合优化。 |
| 建议借鉴的实验 | 比较无解卷积、传统解卷积、联合训练，并检查包络谱和消融结果。 |
| 复现难度（估计） | 中高：完整代码可见，需整理数据并配置损失权重。 |
| 局限与使用边界 | 属于联合训练框架，不能表述为对任意冻结模型的纯事后解释。 |

代码：[已确认作者仓库](https://github.com/asdvfghg/ClassBD)；train_local.py、模型与数据处理；未运行。数据：[数据入口](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download)；PU公开，JNU及重组链接见作者README。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 已阅读作者仓库README，核对代码范围；未执行。 [补充来源](https://github.com/asdvfghg/ClassBD)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C08 · 多通道神经盲解卷积

Liu He; Wen Li; Qiuyang Zhou; Cai Yi; Dong Wang. Multi-channel neural blind deconvolution:A physically interpretable network for impulsive mode extraction. Mechanical Systems and Signal Processing, 2025, 238: 113210. [DOI](https://doi.org/10.1016/j.ymssp.2025.113210)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；冲击模态与复合故障 |
| 研究内容 | 从信号中提取不同冲击模态。 |
| 研究方法 | 将多通道滤波和信号处理步骤构造成可解释网络。 |
| 原文报告的验证 | 论文冲击模态提取实验；完整数据和实现未确认。 |
| 适合引用的位置/论点 | 方法与相关工作：多分量提取与神经盲解卷积。 |
| 建议借鉴的实验 | 检查各通道的周期、包络谱、冗余和跨随机种子稳定性。 |
| 复现难度（估计） | 高：原始实现与完整数据未确认。 |
| 局限与使用边界 | 提取多个模态不等于识别了多个真实独立物理源。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2025.113210)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C09 · Multilayer Grad-CAM

Sinan Li; Tianfu Li; Chuang Sun; Ruqiang Yan; Xuefeng Chen. Multilayer Grad-CAM: An effective tool towards explainable deep neural networks for intelligent fault diagnosis. Journal of Manufacturing Systems, 2023, 69: 20-30. [DOI](https://doi.org/10.1016/j.jmsy.2023.05.027)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；已训练深层诊断网络 |
| 研究内容 | 只解释单一卷积层可能漏掉重要信息。 |
| 研究方法 | 组合多层Grad-CAM信息解释诊断决策。 |
| 原文报告的验证 | 智能故障诊断实验；完整作者复现包未确认。 |
| 适合引用的位置/论点 | 方法与核心相关工作：多层事后归因。 |
| 建议借鉴的实验 | 比较单层与多层解释，并检验重要区域遮蔽后的预测变化。 |
| 复现难度（估计） | 中高：需要核对层选择、融合和上采样规则。 |
| 局限与使用边界 | 上采样后的热图分辨率不等于原网络的真实定位分辨率。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.jmsy.2023.05.027)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C10 · 振动解释方法评估

Oliver Mey; Deniz Neufeld. Explainable AI Algorithms for Vibration Data-Based Fault Detection: Use Case-Adadpted Methods and Critical Evaluation. Sensors, 2022, 22(23): 9037. [DOI](https://doi.org/10.3390/s22239037)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；变转速电机不平衡 |
| 研究内容 | 判断解释图是否真正突出类别相关特征。 |
| 研究方法 | GradCAM、LRP和修改扰动的LIME，结合频率/阶次-RPM图。 |
| 原文报告的验证 | 已知类别特征的合成数据与实测电机不平衡数据。 |
| 适合引用的位置/论点 | 实验设计与讨论：解释质量需要有真值或可检验对照。 |
| 建议借鉴的实验 | 设计可控模拟信号，分别评估相关区域命中与无关区域抑制。 |
| 复现难度（估计） | 中：作者公开分析代码和notebook，环境需核对。 |
| 局限与使用边界 | 原文发现各方法仅部分成功；不能只根据热图好看来评价解释。 |

代码：[已确认作者仓库](https://github.com/o-mey/xai-vibration-fault-detection)；分析代码与notebook；未运行。数据：[数据入口](https://pmc.ncbi.nlm.nih.gov/articles/PMC9736871/)；合成与电机数据的来源见正文和仓库；下载完整性未验证。

核验范围：DOI题录、开放正文相关部分；未逐项复算实验。 [补充来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC9736871/)。Crossref DOI题录；优先使用卷期年，在线年另列。 原题名中的Adadpted拼写按出版记录保留。

#### C11 · BearingNet

N. Herwig; P. Borghesani; W. Smith; Z. Peng. Signal processing- and physics-informed neural network for explainable bearing condition monitoring. Mechanical Systems and Signal Processing, 2025, 235: 112925. [DOI](https://doi.org/10.1016/j.ymssp.2025.112925)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；轴承状态监测 |
| 研究内容 | 把诊断计算过程与信号处理及轴承机理关联。 |
| 研究方法 | 信号处理与物理信息融入结构化神经网络。 |
| 原文报告的验证 | 论文轴承状态监测实验；完整官方代码入口未确认。 |
| 适合引用的位置/论点 | 方法与相关工作：信号处理和物理可解释网络。 |
| 建议借鉴的实验 | 逐层解释输入输出，并检验参数与故障频率之间的关系。 |
| 复现难度（估计） | 高：需轴承信号背景，原始实现获取未确认。 |
| 局限与使用边界 | physics-informed在本文语境不自动等于PDE残差型PINN。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。 [补充来源](https://doi.org/10.1016/j.ymssp.2025.112925)。Crossref DOI题录；优先使用卷期年，在线年另列。

#### C12 · Ex-SPGCAN

Yuyang Chen; Shilong Chu; Shude Ji; Likai Ye; Zhinong Jiang; Fuzhou Feng; Zhiwei Mao. Ex-SPGCAN: Signal-Prior-Guided Channel Attention for Explainable Fault Diagnosis of Diesel Engine Under Variable Operating Conditions. Chinese Journal of Mechanical Engineering, 2026: 100327. [DOI](https://doi.org/10.1016/j.cjme.2026.100327)

| 项目 | 内容 |
| --- | --- |
| 类型与对象 | 方法/应用/基准研究；变工况柴油机 |
| 研究内容 | 区分耦合振动冲击，并增强跨工况解释性。 |
| 研究方法 | 由角域信息和冲击能量先验引导通道注意力。 |
| 原文报告的验证 | TBD234柴油机实验台变工况研究，另有核电应急柴油发电机喷油器故障工程案例。 |
| 适合引用的位置/论点 | 工程案例与相关工作：把重要特征对应到发动机工作事件。 |
| 建议借鉴的实验 | 把归因窗口映射到曲轴角和机械事件，比较工况变化前后的解释。 |
| 复现难度（估计） | 高：工程数据和先验标定是主要门槛。 |
| 局限与使用边界 | 已核对出版页摘要/章节片段，未获得完整工程数据；页面仍标注期刊预校样。 |

代码：本次未确认作者代码；未核验完整实现。数据：本次未确认可独立下载的完整论文数据。

核验范围：Crossref题录与出版页摘要/章节片段；未获取全文和工程数据。 [补充来源](https://www.sciencedirect.com/science/article/pii/S1000934526001161)。Crossref DOI题录；优先使用卷期年，在线年另列。 出版页标注In Press, Journal Pre-proof，2026-05-20在线；题录未提供卷期，不推测补写。
