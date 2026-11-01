# codex-project

刘昌顺的故障诊断学习与科研资料仓库。

## 最新：调研补充、方法详解与下一步研究（2026-11-01）

**特征挖掘的入门整理已完成，面向论文的证据调研仍需继续；现在可以开始可信基线与小规模实验。** 本轮把重点推进到三个问题：解释是否忠实反映模型依赖，候选特征在不同工况下是否稳定，以及这些特征在独立数据上是否有用。详细结论见[调研补充专区](fault-diagnosis-learning/research-update-2026-11/README.md)。

| 你要查看的内容 | 直接入口 | 具体包含什么 |
| --- | --- | --- |
| 深度学习各种方法的详细说明 | [45页方法合订本PDF](fault-diagnosis-learning/deep-learning-methods/00_故障诊断深度学习方法详解_合订本.pdf) · [8个分类分册](fault-diagnosis-learning/deep-learning-methods/README.md) | 35张独立方法卡：31项建模/训练路线与4项解释方法；逐项解释逻辑、输入输出、公式、示例、注意事项、验证与研究着眼点 |
| 特征挖掘调研还缺什么 | [5页调研补充PDF](fault-diagnosis-learning/research-update-2026-11/调研补充与缺口分析.pdf) · [在线文字版](fault-diagnosis-learning/research-update-2026-11/调研补充与缺口分析.md) | 六条路线取舍、解释评价维度、CS-SHAP变换/背景/块归因/缓存检查、跨域选模和未核验问题 |
| 下一步怎么开展研究 | [5页研究方案PDF](fault-diagnosis-learning/research-update-2026-11/下一步研究方案.pdf) · [在线文字版](fault-diagnosis-learning/research-update-2026-11/下一步研究方案.md) | 三个可证伪假设、数据清单、独立划分、基线、干预对照、跨工况与特征重训、阶段交付和柴油机分支 |

方法分册分别覆盖基础CNN、序列/图模型、重构生成、少标签学习、迁移泛化、物理先验与条件建模、多模态/基础模型/压缩、冻结模型解释。推荐先读小型CNN与IG/Grad-CAM，再按具体失败选择SHAP/CS-SHAP、跨工况或物理结构；不需要把所有模型都训练一遍。PDF含书签、中文可搜索；点击文件预览，或点击下载按钮离线阅读。

下一步优先填写[原始记录清单](fault-diagnosis-learning/research-update-2026-11/data_manifest_template.csv)，确认设备、记录、标签、转速与负载，建立人工特征+浅层分类器和小CNN基线。模型可靠后再冻结解释，通过重要/随机/低重要区域干预、跨工况稳定性和候选特征独立测试形成证据。另提供[实验协议模板](fault-diagnosis-learning/research-update-2026-11/experiment_protocol_template.json)与[结果记录表](fault-diagnosis-learning/research-update-2026-11/experiment_results_template.csv)，尚未填入任何实验成绩。

本轮实际读取20个作者/工具来源文件，其中3份为选定源码；学术数据库与两篇候选页面请求受限，未取得新论文全文。新内容是定向补充、方法教材和研究方案，未运行模型实验，也不宣称穷尽调研或方法性能排名。原38篇工程书目与31篇阅读子集继续保留，不能与工具来源数量相加当作独立论文总数。

## 如何查看故障诊断资料

**从[学习资料总目录](fault-diagnosis-learning/README.md)开始。** 无需运行程序或安装依赖，可直接在GitHub阅读。

1. **学习基础：** 打开[教学手册目录](fault-diagnosis-learning/guides)，按“01 深度学习入门 → 02 特征挖掘入门 → 03 二者结合”阅读。三份PDF分别为24、15、11页，共50页；同名Markdown（`.md`）可直接在线阅读。
2. **查看科研论文：** 打开[38篇工程科研论文库](fault-diagnosis-learning/research-papers/README.md)，在线查看完整题录、引用用途、工程验证、代码和数据入口。
3. **下载Excel筛选文献：** 在[科研论文文件目录](fault-diagnosis-learning/research-papers)选择三份`.xlsx`之一，点击文件页的下载按钮，用Excel或WPS打开。“论文与引用”和“工程验证与复现”两张表按编号对应。旧版[43条入门参考资源](fault-diagnosis-learning/references/README.md)继续用于基础学习。
4. **导入参考文献：** 下载[BibTeX](fault-diagnosis-learning/research-papers/engineering_references.bib)或[RIS](fault-diagnosis-learning/research-papers/engineering_references.ris)，导入Zotero、EndNote等文献管理软件。

PDF可在GitHub预览；若无法预览或希望离线阅读，点击文件页的下载按钮保存。也可以在仓库首页选择 **Code → Download ZIP** 下载全部资料，解压后打开PDF和Excel。

## 新增：特征挖掘研究进展与阅读路线

[进入特征挖掘研究进展专区](fault-diagnosis-learning/feature-mining-progress/README.md)。这一部分面向准备开展振动故障诊断研究的学习者，重点回答：**模型预测了故障以后，怎样检查它真正依赖的时间片、频带或内部特征，并判断这些依据是否符合设备机理？**

专区完整收录2026-10-29提供的[研究进展与任务书](fault-diagnosis-learning/feature-mining-progress/研究进展与任务书.md)，包括六类研究方向、31篇逐篇论文导读、两篇待核验候选以及第一个实验的实施顺序。另提供[31篇阅读索引CSV](fault-diagnosis-learning/feature-mining-progress/特征挖掘阅读索引.csv)，可下载到Excel/WPS中筛选方法、学习重点、限制、代码和数据入口。31篇均来自已有38篇论文库，是按研究目标组织的阅读子集。

| 你想解决的问题 | 专区介绍的内容 |
| --- | --- |
| 信号里有哪些故障线索？ | 从频谱、包络、谱峭度、MCKD/MOMEDA理解冲击与调制；用VMD/FMD等分析候选模态及参数敏感性 |
| 网络学到什么、依据是否可靠？ | 从普通CNN基线进入Grad-CAM、SHAP/CS-SHAP，固定模型、解释目标和背景，比较重要/低重要/随机区域干预 |
| 需要怎样改模型？ | 了解TFN、小波核和物理信息结构，区分事后解释与ClassBD等联合训练路线，再根据失败案例决定是否改结构 |
| 怎样连接柴油机或喷油器？ | 用曲轴角、喷油、燃烧和气门事件解释特征，控制转速与负载；区分仿真、实验台和现场证据 |
| 如何形成可检验的研究？ | 分开报告预测性能、解释忠实度和物理一致性；验证跨工况稳定性，再比较候选、传统与随机特征的独立测试表现 |

**建议先读：S03轴承教程 → F12数据基准 → F03/F06信号分析 → D07模型基准 → C10解释评价 → C09多层Grad-CAM → C06 CS-SHAP。** 柴油机方向再读F09、F11、C12。编号沿用科研论文库；逐篇“建议实验”用于设计自己的研究，不代表原论文做过或本仓库已执行。

第一项实验可按“原始记录清单 → 独立分组后切片 → 简单特征与CNN基线 → 冻结模型解释 → 已知真值模拟和合理扰动对照 → 跨工况验证 → 候选特征比较”推进。选择参数、特征及解释设置在训练/验证范围内完成，最终测试集保持独立。每一步应保存哪些信息、如何避免信号扰动造成误判，详见专区介绍。

这一部分可以直接在线阅读，无需先运行模型。原文和CSV中的核验日期保留其历史含义；两篇候选仍待核验，未加入正式引文库。归档与文件验证通过不等于论文实验复现成功。

## 核查记录与使用边界

[任务核查与验证结果](fault-diagnosis-learning/TASK_PROGRESS.md)记录已完成内容和未核验项；[检索说明](fault-diagnosis-learning/SEARCH_NOTES.md)说明来源与限制；[构建说明](fault-diagnosis-learning/src/README.md)用于修改后重新生成资料。

本仓库提供学习导读与文献资料，不包含已复现的论文模型实验。部分出版商实时信息因访问限制未确认，正式引用前请核对最终出版版本。
