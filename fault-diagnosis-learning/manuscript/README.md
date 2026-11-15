# 故障诊断特征挖掘小论文

**直接打开：[带科研图的论文PDF](paper.pdf) · [可编辑Word稿](paper.docx) · [在线阅读全文](paper.md)。**

题目：**面向跨工况故障诊断的解释引导特征挖掘方法框架**。2026-11-15制作，以此前研究方案为基础，完整包含摘要、引言、方法、合成信号演示、实验设计、讨论、结论、7个编号公式和5篇参考文献。作者、单位、目标期刊待确定，当前为通用A4中文学术版式，不声称满足某一期刊模板。

## 稿件状态与下一步

这是方法框架与实验方案稿，尚无真实设备训练与诊断结果。科研图已嵌入正文，图注说明来源、参数和证据边界。图3仅用合成信号说明包络特征提取过程；图1、图2、图4为方法示意。文件验证通过不代表研究假设已经成立，也不代表期刊发表。

下一步按论文第4节执行：核实独立设备/记录和工况 → 锁定数据划分 → 完成传统特征与小CNN基线 → 冻结模型 → 归因与匹配干预 → 锁定特征公式 → 独立工况比较 → 据实补写结果。填写执行清单不是阅读或开展实验的前提，可用自己的记录方式保存关键信息。

## 四幅科研用图

| 图号 | 内容与来源 | 高清图片 | 矢量文件 |
| --- | --- | --- | --- |
| 1 | 原创方法流程图；训练、验证、测试的用途 | [PNG](figures/fig1_workflow.png) | [SVG](figures/fig1_workflow.svg) / [PDF](figures/fig1_workflow.pdf) |
| 2 | 原创频带分组归因示意；未计算SHAP值 | [PNG](figures/fig2_attribution.png) | [SVG](figures/fig2_attribution.svg) / [PDF](figures/fig2_attribution.pdf) |
| 3 | 式（5）生成的合成信号、频谱、滤波、包络谱四面板图 | [PNG](figures/fig3_synthetic.png) | [SVG](figures/fig3_synthetic.svg) / [PDF](figures/fig3_synthetic.pdf) |
| 4 | 原创三层验证示意；对照与失效判据 | [PNG](figures/fig4_validation.png) | [SVG](figures/fig4_validation.svg) / [PDF](figures/fig4_validation.pdf) |

图片均由Matplotlib代码绘制，PNG为300 dpi，SVG将文字转为路径以保留外观，PDF嵌入字体。论文PDF使用矢量图，Word与在线版使用高清PNG。先前对话中的AI生成概念图未用于本稿。

图3原始合成数组见[NPZ](figures/synthetic_source.npz)，包含时间、原始信号、冲击成分、滤波信号、包络和谱数组；[参数JSON](figures/synthetic_parameters.json)说明种子、采样率、公式参数、窗口和滤波。该频带由已知生成参数预先设定，不能作为解释器发现频带的证据。[图形清单](figures/FIGURE_MANIFEST.json)记录尺寸、版本、用途和哈希。

## 修改与重建

修改[论文源稿](paper.md)后运行以下命令。需要Python依赖、Pandoc、XeLaTeX、xeCJK宏包以及Noto CJK字体；Debian/Ubuntu可通过系统管理员安装`pandoc texlive-xetex texlive-lang-chinese fonts-noto-cjk`。不需要训练模型或下载设备数据。

```bash
python -m pip install -r fault-diagnosis-learning/manuscript/requirements.txt
python fault-diagnosis-learning/manuscript/build.py
python fault-diagnosis-learning/manuscript/validate.py
python fault-diagnosis-learning/src/validate_all.py
```

本次环境已具备绘图与办公文档依赖，但缺xeCJK，构建时在临时目录从CTeX-org/ctex-kit的固定提交`c4ccfaefe803ab4a12c9fedc929be1e349e3c612`提取xeCJK、ctexhook及关联文件，并设置`TEXINPUTS=/tmp/paper-tex:`。没有修改系统或将第三方宏包混入稿件。正常安装`texlive-lang-chinese`后不需要这一临时路径。

PDF检查包括文字可提取、图号/关键段落、页面边界、嵌入字体；DOCX检查包括4张内嵌图、表格与公式对象。合成数组检查包括从固定参数重算信号、滤波和谱的一致性。[验证报告](VALIDATION.json)保存实际结果。Word本次检查文件内部结构；未在桌面版Word/WPS中逐页检查，跨软件分页可能略有变化。

## 文献与制作说明

正文参考文献依据仓库既有书目及公开方法题录整理。2026-11-15尝试访问PMLR和arXiv入口均遭代理403，见[访问记录](SOURCE_CHECK.json)；本轮未完成新的原文全文核验。文献[1–2]可在[原科研库](../research-papers/README.md)继续追溯，投稿前需核对全部实际引用原文。

正文与绘图代码由AI辅助，研究者需对论证、文献及后续实测结果负责。科研可视化制作采用[scientific-visualization技能](https://github.com/K-Dense-AI/claude-scientific-skills)提供的完整性、图注和来源记录原则；工作流来源单独记录，不计入故障诊断证据：

Kassis T, Agarwal V, He Y, Patel D, Brueckner A M. Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. 2026. [arXiv:2609.00065](https://arxiv.org/abs/2609.00065). 该题录由技能提供，本次访问受阻，版本及出版状态尚待联网复核。

返回[仓库首页](../../README.md) · [资料总目录](../README.md) · [下一步研究方案](../research-update-2026-11/下一步研究方案.md)
