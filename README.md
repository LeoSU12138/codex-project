# codex-project｜故障诊断学习与研究

刘昌顺的故障诊断学习与科研资料仓库。目标是：**建立可靠的诊断模型，查清模型依赖什么信息，再验证挖出的特征是否与机理相容、能否在独立数据上使用。**

**从本页按步骤做；需要找文件时用[资料总目录](fault-diagnosis-learning/README.md)。** 仓库已有教学PDF、文献索引、方法详解和研究方案；个人数据、训练工程、权重与实验结果还需要实际建立。`src/`中的程序用于生成和检查资料，不是故障诊断训练入口。

## 新增：带科研图的小论文

**[直接阅读论文PDF](fault-diagnosis-learning/manuscript/paper.pdf) · [下载可编辑Word稿](fault-diagnosis-learning/manuscript/paper.docx) · [在线阅读全文](fault-diagnosis-learning/manuscript/paper.md) · [图片、代码与验证说明](fault-diagnosis-learning/manuscript/README.md)**

《面向跨工况故障诊断的解释引导特征挖掘方法框架》已将四幅科研用图嵌入正文，包含研究流程、频带归因、合成信号的频谱与包络演示及三层验证设计。2026-11-15稿为方法与实验方案，尚无真实设备实验结果；合成图不代表实测诊断效果。PDF采用通用中文学术版式；Word下载后用Word/WPS修改。下一步按论文第4节及下方六步路线开展实际实验。

## 你现在从哪里开始

| 当前状态 | 开始位置 | 这次先完成的一件事 |
| --- | --- | --- |
| 尚无数据、模型，或不确定研究什么 | 第1步 | 写清设备、故障任务、信号、数据来源和一个研究问题 |
| 已有原始数据，但没有可信划分 | 第2步 | 建立原始记录清单，确定独立分组与测试集 |
| 已有数据与划分，尚无可靠模型 | 第3步 | 跑通传统特征和小CNN的公平基线 |
| 已有模型、权重、划分与评估记录 | 先核对第2–3步，再到第4步 | 固定模型与解释目标，在开发数据上做解释对照 |

**今天建议只做：** 复制[研究执行清单](fault-diagnosis-learning/research-update-2026-11/研究执行清单.md)，填完“项目卡”；再按[模板填写指南](fault-diagnosis-learning/research-update-2026-11/模板填写指南.md)准备个人记录。无需先读完所有论文或尝试所有网络。

## 按六步推进

### 第1步：明确问题，补足最少的基础

先定一种设备和一个任务，例如轴承故障分类，或柴油机喷油器故障识别；写明输入信号、标签来源、已有数据和部署时可获得的信息。暂未确定就标“待确定”，不要先选复杂网络。

按需阅读：[深度学习入门](fault-diagnosis-learning/guides/01_故障诊断深度学习入门.md) → [特征挖掘入门](fault-diagnosis-learning/guides/02_特征挖掘入门.md) → [两者结合](fault-diagnosis-learning/guides/03_深度学习与特征挖掘结合.md)。先弄懂训练/验证/测试、频谱/包络和模型解释的区别。PDF在[总目录](fault-diagnosis-learning/README.md)下载。

**交付与完成条件：** 一张项目卡、一句话研究问题，能说清最终要预测什么、希望解释什么。柴油机需要单独核对曲轴角和工作事件；轴承的故障频率不能直接套用。

### 第2步：整理数据，先分组再切片

填写[原始记录清单](fault-diagnosis-learning/research-update-2026-11/data_manifest_template.csv)，记录设备、运行/批次、转速、负载、采样率、单位、标签依据和来源。没有自己的数据时，从[基础资源目录](fault-diagnosis-learning/references/README.md)的CWRU/Paderborn入口了解条件，再决定是否适合你的任务。

按设备或独立运行分组，划分训练、验证、最终测试；然后生成[窗口清单](fault-diagnosis-learning/research-update-2026-11/window_manifest_template.csv)，记录每片来自哪个原始文件和区间。标准化参数只由训练集拟合。最终测试集锁定；模型、频带和解释参数的选择在训练/验证范围完成。

**交付与完成条件：** 原始记录清单、划分协议、窗口清单和基本信号检查图；没有同源重叠片段跨集合，能报告独立设备/记录数。元数据不足时缩小结论范围，并记录限制。

### 第3步：先做两个可信基线

先用RMS、峭度、预定包络能量等人工特征搭配浅层分类器，再做小型1D-CNN。网络原理优先查[方法详解](fault-diagnosis-learning/deep-learning-methods/README.md)的M01、M03、M05；工程阅读查[科研论文库](fault-diagnosis-learning/research-papers/README.md)的D02、D07。作者代码需要核对数据接口、划分、依赖和训练入口后才能接入。

按[实验协议模板](fault-diagnosis-learning/research-update-2026-11/experiment_protocol_template.json)固定预处理、预算和种子，在验证数据选模；保存权重、类别映射、配置、训练日志、混淆矩阵与每类召回。用[结果记录表](fault-diagnosis-learning/research-update-2026-11/experiment_results_template.csv)登记结果。

**交付与完成条件：** 两个可重复基线及错误分析，能排除明显泄漏和标签错误；不以“必须达到99%”作为门槛。表现异常先检查数据与协议，再考虑加深网络。

### 第4步：冻结模型，验证解释

固定权重、预处理、目标类别和输出（如logit）。先试IG或Grad-CAM，确有频域问题再尝试SHAP/CS-SHAP；查[解释分册](fault-diagnosis-learning/deep-learning-methods/08_冻结模型后的解释.pdf)和[调研补充](fault-diagnosis-learning/research-update-2026-11/调研补充与缺口分析.md)。论文顺序为C10 → C09 → C06。

在开发数据上比较重要、低重要和随机区域的合理干预；记录背景、粒度、变换、重构误差、种子和缓存版本。分别检查模型依赖、解释稳定性与机理一致性；热图本身不是通过条件。

**交付与完成条件：** 原始归因、对照结果与失败案例；能够说明解释为什么可信或在哪里失效。涉及选特征/改结构的发现仍属于开发过程，不能使用最终测试来挑选。

### 第5步：把发现写成特征，锁定后独立测试

用[候选特征记录表](fault-diagnosis-learning/research-update-2026-11/feature_candidates_template.csv)把频带、阶次或事件写成公式，注明它从哪些训练记录中发现、如何由验证集选参。用相同维度、分类器和调参预算比较传统、随机与候选特征。

模型、特征、解释设置及评价方案全部锁定后，再使用最终留出数据做预定评价。按工况分别报告预测、忠实度、物理一致性和成本；只有目标域完全未用于开发时才可声称相应的未见域验证。详细对照和指标见[下一步研究方案](fault-diagnosis-learning/research-update-2026-11/下一步研究方案.md)。

**交付与完成条件：** 冻结特征定义、独立比较和不确定性/逐组结果。没有收益也记录；查看最终测试后改方案，应另设新的未见测试或明确后续为探索性分析。

### 第6步：收束结论，再决定下一项研究

汇总“问题 → 方法 → 对照 → 证据 → 限制”，完成执行清单末尾的研究小结。用[全文核验记录表](fault-diagnosis-learning/research-update-2026-11/literature_review_template.csv)对核心文献记录版本、原文位置、实验条件和引用用途，再从正式库导出BibTeX/RIS。

根据已观察到的问题选一个分支：标签少再考虑自监督；长上下文不足再考虑TCN/Transformer；机理明确再试可解释前端。柴油机的额外数据条件见研究方案第7节。

**交付与完成条件：** 可复查的实验材料、证据对应的结论、未解决问题和一个下一步假设。当前资料支持开展研究，论文新颖性、全文核验和真实实验仍需继续。

## 文件如何打开，哪些只需按需查

- Markdown（`.md`）在GitHub直接阅读；PDF可预览或点击下载，预览失败时离线打开。
- CSV/Excel下载后用Excel或WPS打开；BibTeX/RIS导入Zotero等文献管理器。全部资料可用 **Code → Download ZIP** 下载。
- [35张方法卡与8个分册](fault-diagnosis-learning/deep-learning-methods/README.md)用作选型词典；[38篇科研论文库](fault-diagnosis-learning/research-papers/README.md)用于研究阅读与引用；[31篇导读](fault-diagnosis-learning/feature-mining-progress/README.md)是其中的阅读子集。
- [历史任务与核查记录](fault-diagnosis-learning/TASK_PROGRESS.md)、[检索说明](fault-diagnosis-learning/SEARCH_NOTES.md)、[维护脚本说明](fault-diagnosis-learning/src/README.md)按需查看。个人下一步以本页和执行清单为准。

## 本次检查与仍待完成的工作

2026-11-07重排导航，补充执行清单、模板字段说明、窗口追溯、候选特征及全文核验记录。文件核查结果见[仓库检查报告](fault-diagnosis-learning/REPOSITORY_CHECK.json)，具体差距与处理见[任务记录](fault-diagnosis-learning/TASK_PROGRESS.md)。

原有14份资料PDF（含重复编排的合订本/分册）、6份Excel继续保留；另增论文PDF及4份独立矢量图PDF，共19份PDF。35张方法卡不等于35种互斥网络；43条基础资源与38篇科研论文有重复，31篇导读也是子集。两篇候选文献、C12最新出版状态、完整全文核验及用户数据条件仍待补齐；历史来源访问限制不是本轮重新检索的结果。文件检查通过不代表模型实验已完成。
