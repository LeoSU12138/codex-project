# 检索与核验说明

以下先保留原入门包的检索记录；2026-10-27新增的[38篇工程科研论文库](research-papers/README.md)见本文末尾“工程科研论文版增补”。正式引用与代码状态以新库更新记录为准。

## 目的与范围

回答三个学习问题：深度学习故障诊断如何入门；特征挖掘要学什么；怎样把模型预测、事后解释和物理验证结合。目标是选择适合分阶段阅读和复现的资源，而不是追求引用量排名或穷尽全部论文。

检索与链接核验日期为2026-10-26，文档整理和最终格式验证完成于2026-10-27。共43条独立条目：深度学习18条、特征挖掘14条、结合研究11条。教材、官方工具文档和公开数据集也作为资源条目计数，因此43不是论文数量。

## 来源与查询方向

使用网页检索并核对作者原始论文、会议/期刊/出版社页面、arXiv预印本、官方工具文档、大学数据站及作者代码仓库。代表性查询包括：

- deep learning fault diagnosis review roadmap / rotating machinery open source benchmark
- interpretable fault diagnosis time-frequency transform / WaveletKernelNet / frequency activation map
- post-hoc vibration fault detection explainability / CS-SHAP / prototype matching
- feature selection Guyon Elisseeff / time series feature extraction tsfresh
- Fourier Neural Operator / HyperNetworks / domain generalization
- CWRU Bearing Data Center / Paderborn Bearing DataCenter

对候选条目用完整题名、DOI或作者仓库相互核对。补充检索解决书目或代码归属疑点。没有做数据库全量导出、双人独立筛选、PRISMA计数、全文逐篇评审或引文影响力统计。

## 纳入原则

优先选择基础概念明确、能连接到机械故障诊断、具有可用学习材料或代码入口的资源。基础论文允许非机械任务，但用途列中明确说明迁移边界。高级方法被标为“选学”，不作为入门先决条件。

没有确认题名/作者或出处的候选不作为正式条目。未确认官方代码时如实保留该状态。通用解释工具（如Captum）与论文完整复现项目明确区分；作者仓库只有模型文件时，指出还需要训练框架。

## 核验深度与复现判断

每行的“本次核验范围”说明依据是官方文档、README、预印本、出版题录或摘要。未下载全部数据、未训练论文模型、未审计全部代码、未验证全部依赖可安装性，也未承诺论文性能可直接复现。

“易”主要意味着基础示例较完整；“中”意味着需要处理数据/依赖/模型适配；“高”意味着理论、实现、算力或资源门槛更大；综述不作为单一实验评价。判断针对本文建议的学习任务，不是对原研究质量的评分。

部分出版社页面访问受限，使用作者预印本、出版社索引或作者机构记录核对，未声称阅读受限全文。CS-SHAP按本次确认的2025预印本引用；WaveletKernelNet区分2021在线发表与2022卷期；开源基准采用2020预印本入口。后续正式引用应检查所用版本的最新书目信息。

## 编写流程来源

使用已安装的nature-academic-search、literature-review与scientific-critical-thinking流程辅助检索和论证边界检查。方法来源：Kassis, Timothy; Agarwal, Vinayak; He, Yuhuan; Patel, Darshil; Brueckner, Aubrey M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. [arXiv:2609.00065](https://arxiv.org/abs/2609.00065)。此项为编写流程来源，不是故障诊断研究证据。

## 资料复用

这里只保存原创导读、书目元数据和外部链接。第三方论文全文、作者代码、数据集、图表及其许可证不由本仓库重新授权。使用代码或下载数据时请按原站的许可、引用和版本要求执行。
# 工程科研论文版增补（2026-10-27）

在原入门资料已发布的基础上，新增`research-papers/`，用于后续科研引用和工程实验设计。原PDF与入门工作簿不重复生成；新库38篇，包括34篇方法/应用/基准研究和4篇综述、教程或综述与比较研究。这里的D/F/C/S编号只在新库有效。

检索覆盖出版社、期刊原页、Crossref、开放正文、大学机构页面及作者GitHub/MATLAB代码页。先按题名识别候选，随后对38个DOI逐条取得Crossref记录，核对作者、卷期、页码和年份。必要题录保存在`source_metadata.json`，没有公开全文摘要、作者联系方式或机构详情。中文文章C02的Crossref缺作者，依据期刊原页补齐。来源URL逐篇列在JSON、Excel及目录中。

代表性检索组合包括：`deep learning rotating machinery fault diagnosis benchmark`、`fault characteristic mining deep neural networks`、`diesel engine fault diagnosis transfer learning`、`diesel injector diversity entropy diagnosis`、`spectral kurtosis MCKD MOMEDA FMD`、`interpretable fault diagnosis TFN WaveletKernelNet`、`CS-SHAP cyclic spectral`、`Multilayer Grad-CAM fault diagnosis`、`Ex-SPGCAN`，并用精确题名或DOI定位原始来源。检索结果按工程相关性、原始方法价值、可解释性问题和资源可获得性定向筛选，不声称穷尽检索，未统计系统综述式初筛/排除数量。

新库的题录与资源更新包括：CS-SHAP采用2026年正式期刊DOI `10.1016/j.ymssp.2026.114495`及六位作者；C10确认作者仓库`o-mey/xai-vibration-fault-detection`；MCKD DOI采用`10.1016/j.ymssp.2012.06.010`；UDTL综述与比较研究DOI采用`10.1109/TIM.2021.3116309`；F11区分2023在线和2024卷期年。C12的出版页面仍为In Press / Journal Pre-proof，日期2026-05-20，保留预校样状态并留空卷期。

工程验证范围有意分开：公开轴承基准、人工设置故障的实验台、物理数字孪生，以及原文报告的工程案例。F10的核心数据是数字孪生缸压，不能称为全现场数据；C12公开章节包含TBD234实验台与核电应急柴油发电机喷油器故障案例，不把它推广成任意柴油机验证。

作者代码核验以仓库README和作者发布页为限；TFN示例主要为CWRU，WaveletKernelNet主要为模型，ClassBD包含训练入口，CS-SHAP包含模拟/CWRU演示。未执行训练或复算论文结果，也未审计完整依赖、数据和许可。建议实验由整理者提出，已与原文报告的实验分列。

---


## 2026-10-28任务书复核

执行范围：先同步到`552f417`并阅读三册、旧43条目录、新38篇目录与构建脚本；没有发现需要靠增添论文数量解决的方向缺项，因此保留38篇、34篇原始方法/应用/基准研究及4篇综述/教程/比较研究。任务对应关系见[TASK_PROGRESS.md](TASK_PROGRESS.md)。本次采用nature-academic-search的citation-verification流程；当前未挂载文献检索MCP，改用标准库HTTP请求和已有题录快照逐条比较。

实时预检对Crossref（CS-SHAP和MCKD）、DOI解析（CS-SHAP）、中文期刊C02及ScienceDirect C12发起只读请求，均得到代理`Tunnel connection failed: 403 Forbidden`；提权请求Crossref仍为403，未绕过代理或TLS验证。不能据此断言论文不存在、DOI无效或C12仍处于预校样。未进行大批量无效重试，也未将旧核验日期改为本次日期。

可访问作者来源：通过raw.githubusercontent.com读取TFN、WaveletKernelNet、CS-SHAP、振动解释评估及UDTL的README。ClassBD因文件为小写`readme.md`，初始标准README路径404后改用HTTPS Git代理读取；诊断基准的raw入口503后亦改用HTTPS Git读取，7项均取得。证据入口、正文摘要哈希及两个Git读取的提交号保存在[审计证据](research-papers/AUDIT_EVIDENCE.json)，第三方README正文只留临时目录，不提交仓库。

实际观察：TFN明确提供CWRU准确率训练/统计流程；WaveletKernelNet指向模型和另一个基准工程；CS-SHAP有模拟/CWRU的训练、解释、绘图演示及环境版本，仍引用2025预印本，完整作者为Qian Chen、Xingjian Dong、Kui Hu、Kangkang Chen、Zhike Peng、Guang Meng；ClassBD有`train_local.py`、PU/JNU组织和[batch,1,2048]输入说明；振动解释评估库README只声明代码与notebook；UDTL列出Base/AdaBN/DANN/MK-MMD训练入口。诊断基准明确有random/order划分，不能直接当无泄漏协议。这里只核对作者声明，没有运行训练或下载全量数据。

C02中文题名/六作者/65–76页、C06期刊DOI、MCKD与UDTL的DOI、F11在线2023/卷期2024、本地C12空卷期与In Press状态均与原始快照和已保存补全逻辑一致。**这属于本地一致性复核，不是本次在线题录确认。** C12最终出版状态等外部问题保留为未确认。所有38篇均补明输入输出摘要和具体未核验的工程条件；不根据笼统摘要编造故障尺寸、转速、负载或现场验证。

本次教学新增内容为标准概念导读：方差/量纲、窗函数/泄漏、FMD/MCKD/MOMEDA参数、阶次条件和设备机理边界；原始算法出处沿用科研F04/F05/F07/F08、轴承教程S03与柴油机/喷油器F09–F11/C12，不将本次导读视为新论文实验证据。仅新增资料说明，无需模型训练或教学示例代码测试。
