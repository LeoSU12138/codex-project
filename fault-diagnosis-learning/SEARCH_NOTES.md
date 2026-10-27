# 检索与核验说明

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
