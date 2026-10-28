# 文献、代码与数据目录

本目录保留43条入门学习资源及旧版书目快照；正式科研引用和新版作者/代码说明请优先查看[38篇科研论文库](../research-papers/README.md)，本次复核边界见[任务进度](../TASK_PROGRESS.md)。

> 43条精选资源；核验范围和复现限制逐条列出。链接核查：2026-10-26。全部未运行验证。

## 深度学习

### D01 · Dive into Deep Learning / 动手学深度学习

**作者/机构：** Aston Zhang; Zachary C. Lipton; Mu Li; Alexander J. Smola  
**年份/版本：** 2023；在线更新 · 交互教材 · 先学

- 研究内容：数学、张量、优化、CNN、注意力的系统入门。
- 方法：概念讲解与可执行代码结合。
- 可以参考：先读预备知识、MLP、CNN和训练；中文版从首页进入。
- 复现估计：易：跟章节练习；完整读完难度中。
- 核验范围：官方教材目录
- [原始资料](https://d2l.ai/)
- [代码/工具](https://github.com/d2l-ai/d2l-en)
- 数据：教材配套示例数据
- 备注：教材示例不等于机械故障数据。

### D02 · Learn the Basics

**作者/机构：** PyTorch contributors  
**年份/版本：** 持续更新 · 官方教程 · 先学

- 研究内容：从数据到训练、保存和加载的完整最小流程。
- 方法：Dataset、DataLoader、nn.Module、autograd、优化器。
- 可以参考：照着运行，再把图像样本替换为一维振动窗口。
- 复现估计：易：教程完整；改成机械任务需适配形状。
- 核验范围：官方教程
- [原始资料](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [代码/工具](https://github.com/pytorch/tutorials)
- 数据：教程内置 FashionMNIST 示例

### D03 · Deep Learning

**作者/机构：** Ian Goodfellow; Yoshua Bengio; Aaron Courville  
**年份/版本：** 2016 · 教材 · 按需查

- 研究内容：深度学习的数学、优化与表示学习基础。
- 方法：概率、线性代数、前馈网络、正则化、卷积。
- 可以参考：遇到反向传播、过拟合、优化问题时查阅；不必首先通读。
- 复现估计：中高：理论阅读；不是故障诊断复现项目。
- 核验范围：作者教材网站
- [原始资料](https://www.deeplearningbook.org/)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口

### D04 · Common pitfalls and recommended practices

**作者/机构：** scikit-learn developers  
**年份/版本：** 持续更新 · 官方文档 · 先学

- 研究内容：预处理不一致、测试集泄漏等常见错误。
- 方法：Pipeline；只用训练集拟合变换。
- 可以参考：在切片、标准化、特征筛选前先规划独立划分。
- 复现估计：易：有小例子；需要迁移到分组时序数据。
- 核验范围：官方文档
- [原始资料](https://scikit-learn.org/stable/common_pitfalls.html)
- [代码/工具](https://github.com/scikit-learn/scikit-learn)
- 数据：不适用或本次未确认独立数据入口

### D05 · Deep learning and its applications to machine health monitoring

**作者/机构：** Rui Zhao; Ruqiang Yan; Zhenghua Chen; Kezhi Mao; Peng Wang; Robert X. Gao  
**年份/版本：** 2019 · 综述 · 先读

- 研究内容：梳理早期深度学习在机器健康监测中的应用。
- 方法：AE、RBM/DBN、CNN、RNN分类与比较。
- 可以参考：建立方法地图；理解传统特征与学习特征的转变。
- 复现估计：不适用：综述；按其引用选择单篇实验。
- 核验范围：作者预印本摘要/作者机构记录
- [原始资料](https://doi.org/10.1016/j.ymssp.2018.05.050)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：预印本题名末尾为 A Survey；https://arxiv.org/abs/1612.07640。不是截至2026年的最新综述。

### D06 · Applications of machine learning to machine fault diagnosis: A review and roadmap

**作者/机构：** Yaguo Lei; Bin Yang; Xinwei Jiang; Feng Jia; Naipeng Li; Asoke K. Nandi  
**年份/版本：** 2020 · 综述 · 先读

- 研究内容：机器故障诊断的机器学习发展路线与应用挑战。
- 方法：传统学习、深度学习及迁移学习路线比较。
- 可以参考：把任务、数据、算法和评价连起来；用作论文引言地图。
- 复现估计：不适用：综述；不提供单个统一实验。
- 核验范围：出版平台索引/摘要；全文访问受限
- [原始资料](https://doi.org/10.1016/j.ymssp.2019.106587)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：MSSP 138:106587。

### D07 · Case Western Reserve University Bearing Data Center

**作者/机构：** Case Western Reserve University Bearing Data Center  
**年份/版本：** 持续提供 · 公开数据 · 先用

- 研究内容：台架轴承正常与人工单点故障振动数据。
- 方法：振动采集，含转速；MAT文件与工况说明。
- 可以参考：练习读MAT、时域/频谱、简单分类；保留原始文件标识。
- 复现估计：易到中：下载容易；防泄漏和独立分组需要认真设计。
- 核验范围：官方数据与试验说明
- [原始资料](https://engineering.case.edu/bearingdatacenter/download-data-file)
- 代码/工具：本次未确认官方代码
- [数据](https://engineering.case.edu/bearingdatacenter/download-data-file)
- 备注：12k/48k采样不能混淆。人工故障结果不能直接外推现场故障；独立轴承数不能用窗口数替代。

### D08 · Paderborn University Bearing DataCenter

**作者/机构：** Paderborn University, Chair of Design and Drive Technology (KAt)  
**年份/版本：** 持续提供 · 公开数据 · 进阶

- 研究内容：同步电流和振动；健康、人工损伤、加速寿命损伤轴承。
- 方法：多工况台架采集；32个轴承状态，四种工况。
- 可以参考：按轴承编号/工况分组；练习跨设备和跨工况评价。
- 复现估计：中：文件结构和标签整理比CWRU复杂。
- 核验范围：官方数据下载与说明
- [原始资料](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download)
- 代码/工具：本次未确认官方代码
- [数据](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download)
- 备注：6健康、12人工损伤、14寿命试验损伤；不是所有32个都是损坏。使用条件以数据站说明为准。

### D09 · Deep Residual Learning for Image Recognition

**作者/机构：** Kaiming He; Xiangyu Zhang; Shaoqing Ren; Jian Sun  
**年份/版本：** 2016；预印本2015 · 基础论文 · 进阶

- 研究内容：残差连接帮助优化更深网络。
- 方法：学习残差并通过跳跃连接相加。
- 可以参考：理解残差模块；用于1D CNN时检查通道与长度匹配。
- 复现估计：中：成熟实现多；原论文是图像任务。
- 核验范围：原始论文摘要
- [原始资料](https://arxiv.org/abs/1512.03385)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：未逐一核验代码版本；不要把图像性能当作故障诊断证据。

### D10 · Attention Is All You Need

**作者/机构：** Ashish Vaswani; Noam Shazeer; Niki Parmar; Jakob Uszkoreit; Llion Jones; Aidan N. Gomez; Łukasz Kaiser; Illia Polosukhin  
**年份/版本：** 2017 · 基础论文 · 进阶

- 研究内容：Transformer序列建模框架。
- 方法：多头注意力、位置编码、前馈模块。
- 可以参考：理解注意力如何组合信息；时序切块和位置编码需适配。
- 复现估计：中高：概念与算力门槛较CNN高。
- 核验范围：原始论文摘要
- [原始资料](https://arxiv.org/abs/1706.03762)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：注意力权重不自动等于可靠的故障解释。

### D11 · Fourier Neural Operator for Parametric Partial Differential Equations

**作者/机构：** Zongyi Li; Nikola Kovachki; Kamyar Azizzadenesheli; Burigede Liu; Kaushik Bhattacharya; Andrew Stuart; Anima Anandkumar  
**年份/版本：** 2021；预印本2020 · 算子学习论文 · 选学

- 研究内容：学习参数化PDE中的函数到函数映射。
- 方法：频域参数化积分算子；Fourier层与局部线性分支。
- 可以参考：理解算子学习；先判断任务是否需要函数映射。
- 复现估计：高：官方框架可用，但故障分类需另行设计。
- 核验范围：论文摘要/官方理论文档
- [原始资料](https://arxiv.org/abs/2010.08895)
- [代码/工具](https://github.com/neuraloperator/neuraloperator)
- 数据：官方示例PDE数据；不是故障数据
- 备注：FFT+CNN不自动成为FNO；换分辨率也不保证精度。

### D12 · HyperNetworks

**作者/机构：** David Ha; Andrew Dai; Quoc V. Le  
**年份/版本：** 2017；预印本2016 · 架构论文 · 选学

- 研究内容：用一个网络生成另一个网络的权重。
- 方法：静态或依赖条件的权重生成。
- 可以参考：研究工况条件化参数；区分超网络与超参数优化。
- 复现估计：高：须设计条件、主网络和训练方案。
- 核验范围：论文摘要/作者博客
- [原始资料](https://arxiv.org/abs/1609.09106)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：https://blog.otoro.net/2016/09/28/hyper-networks/；并不自带未知工况泛化保证。

### D13 · Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators

**作者/机构：** Lu Lu; Pengzhan Jin; Guofei Pang; Zhongqiang Zhang; George Em Karniadakis  
**年份/版本：** 2021 · 算子学习论文 · 选学

- 研究内容：用分支与主干网络学习非线性算子。
- 方法：Branch编码输入函数，trunk编码求值坐标。
- 可以参考：与FNO比较；理解输入函数和输出坐标的含义。
- 复现估计：高：有代码；迁移到故障诊断需自定物理问题。
- 核验范围：出版页/作者代码入口
- [原始资料](https://doi.org/10.1038/s42256-021-00302-5)
- [代码/工具](https://github.com/lululxvi/deeponet)
- 数据：代码示例数据

### D14 · Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations

**作者/机构：** Maziar Raissi; Paris Perdikaris; George Em Karniadakis  
**年份/版本：** 2019 · 物理学习论文 · 选学

- 研究内容：将PDE与边界/初始条件加入学习约束。
- 方法：自动微分求残差，与数据误差联合优化。
- 可以参考：理解物理约束为何需要正确方程、单位和权重。
- 复现估计：高：原始代码较旧；方程与训练稳定性是门槛。
- 核验范围：作者项目页
- [原始资料](https://doi.org/10.1016/j.jcp.2018.10.045)
- [代码/工具](https://github.com/maziarraissi/PINNs)
- 数据：官方PDE示例
- 备注：https://maziarraissi.github.io/PINNs/；物理启发滤波器不必然是经典PDE型PINN。

### D15 · Domain-Adversarial Training of Neural Networks

**作者/机构：** Yaroslav Ganin; Evgeniya Ustinova; Hana Ajakan; Pascal Germain; Hugo Larochelle; François Laviolette; Mario Marchand; Victor Lempitsky  
**年份/版本：** 2016 · 迁移学习论文 · 进阶

- 研究内容：在源域与目标域间学习可迁移表示。
- 方法：域分类器、梯度反转、标签预测联合优化。
- 可以参考：区分可使用无标签目标数据的域适应和完全未知目标域。
- 复现估计：中高：需严格定义训练时可见的目标数据。
- 核验范围：期刊论文摘要
- [原始资料](https://www.jmlr.org/papers/v17/15-239.html)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：目标域类别不匹配时可能负迁移。

### D16 · In Search of Lost Domain Generalization

**作者/机构：** Ishaan Gulrajani; David Lopez-Paz  
**年份/版本：** 2021；预印本2020 · 泛化评估论文 · 进阶

- 研究内容：检验域泛化算法与模型选择的公平性。
- 方法：统一基准与模型选择协议。
- 可以参考：借鉴留一工况、验证域选择和公平基线设置。
- 复现估计：中高：基准有实现；机械数据需另行接入。
- 核验范围：原始论文/代码链接
- [原始资料](https://arxiv.org/abs/2007.01434)
- [代码/工具](https://github.com/facebookresearch/DomainBed)
- 数据：基准以图像域数据为主
- 备注：不要用最终目标域标签挑超参数再声称未知域泛化。

### D17 · Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks

**作者/机构：** Chelsea Finn; Pieter Abbeel; Sergey Levine  
**年份/版本：** 2017 · 元学习论文 · 选学

- 研究内容：学习能以少量新样本快速适应的初始化。
- 方法：多任务内循环适应与外循环更新。
- 可以参考：理解few-shot任务、支持集和查询集；与超网络区分。
- 复现估计：高：任务划分、二阶梯度和计算量有门槛。
- 核验范围：原始论文摘要
- [原始资料](https://arxiv.org/abs/1703.03400)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口

### D18 · Deep learning algorithms for rotating machinery intelligent diagnosis: An open source benchmark study

**作者/机构：** Zhibin Zhao; Tianfu Li; Jingyao Wu; Chuang Sun; Shibin Wang; Ruqiang Yan; Xuefeng Chen  
**年份/版本：** 2020 · 开源基准 · 进阶

- 研究内容：旋转机械深度诊断的统一基准实现与比较。
- 方法：多种网络与数据处理、评价流程。
- 可以参考：阅读训练脚本与数据接口；对照同一划分而非照搬精度。
- 复现估计：中：代码公开；依赖和数据组织需检查。
- 核验范围：作者仓库与论文链接
- [原始资料](https://arxiv.org/abs/2003.03315)
- [代码/工具](https://github.com/ZhaoZhibin/DL-based-Intelligent-Diagnosis-Benchmark)
- 数据：仓库数据接口及原始数据站
- 备注：本文采用2020预印本；期刊DOI：10.1016/j.isatra.2020.08.010。旧依赖需锁定或记录迁移修改。

## 特征挖掘

### F01 · Discrete Fourier transforms (scipy.fft)

**作者/机构：** SciPy contributors  
**年份/版本：** 持续更新 · 官方教程 · 先学

- 研究内容：把时间波形转换为频率表示。
- 方法：DFT/FFT、频率轴、逆变换与窗函数示例。
- 可以参考：完成第一张有正确Hz单位的频谱；理解分辨率。
- 复现估计：易：CPU小数组即可。
- 核验范围：官方文档
- [原始资料](https://docs.scipy.org/doc/scipy/tutorial/fft.html)
- [代码/工具](https://github.com/scipy/scipy)
- 数据：自造正弦信号即可

### F02 · scipy.signal.hilbert

**作者/机构：** SciPy contributors  
**年份/版本：** 持续更新 · 官方示例 · 先学

- 研究内容：解析信号、包络与瞬时频率的计算。
- 方法：Hilbert变换与解析信号幅值。
- 可以参考：理解冲击激励高频共振时为何要看包络谱。
- 复现估计：易到中：调用简单；滤波带和物理解读需学习。
- 核验范围：官方文档
- [原始资料](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html)
- [代码/工具](https://github.com/scipy/scipy)
- 数据：文档调幅信号示例

### F03 · Rolling element bearing diagnostics—A tutorial

**作者/机构：** Robert B. Randall; Jérôme Antoni  
**年份/版本：** 2011 · 领域教程 · 先读

- 研究内容：轴承故障振动机制与诊断信号处理。
- 方法：包络分析、调制、周期/随机特征等。
- 可以参考：给频谱峰和解调结果找物理依据；读图与流程优先。
- 复现估计：中高：原理较深；不是一键运行项目。
- 核验范围：期刊题录/摘要
- [原始资料](https://doi.org/10.1016/j.ymssp.2010.07.017)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：机械轴承特征不能直接套用柴油机燃烧故障。

### F04 · An Introduction to Variable and Feature Selection

**作者/机构：** Isabelle Guyon; André Elisseeff  
**年份/版本：** 2003 · 方法综述 · 先读

- 研究内容：说明特征相关性、冗余、排序与子集选择。
- 方法：过滤式、包裹式、嵌入式方法及验证。
- 可以参考：特征选择目标与训练内筛选原则；避免全数据挑特征。
- 复现估计：中：概念入门；具体实现可用scikit-learn。
- 核验范围：期刊摘要
- [原始资料](https://www.jmlr.org/papers/v3/guyon03a.html)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口

### F05 · Time Series FeatuRe Extraction on basis of Scalable Hypothesis tests (tsfresh – A Python package)

**作者/机构：** Maximilian Christ; Nils Braun; Julius Neuffer; Andreas W. Kempa-Liehr  
**年份/版本：** 2018 · 工具论文 · 进阶

- 研究内容：批量构造并筛选时间序列统计特征。
- 方法：时序特征计算与统计检验筛选。
- 可以参考：先用少量已理解特征，再扩展；在交叉验证每折内筛选。
- 复现估计：中：官方代码成熟；计算量、缺失值与泄漏需处理。
- 核验范围：期刊摘要/官方仓库
- [原始资料](https://doi.org/10.1016/j.neucom.2018.03.067)
- [代码/工具](https://github.com/blue-yonder/tsfresh)
- 数据：文档示例数据
- 备注：库版本影响特征数量；筛出显著特征不等于找到故障因果机制。

### F06 · Variational Mode Decomposition

**作者/机构：** Konstantin Dragomiretskiy; Dominique Zosso  
**年份/版本：** 2014 · 分解论文 · 进阶

- 研究内容：将信号分成有限带宽的候选模态。
- 方法：变分优化联合估计模态和中心频率。
- 可以参考：比较原信号、模态和包络谱；分析参数敏感性。
- 复现估计：中高：作者MATLAB代码可得；K和惩罚系数需选择。
- 核验范围：作者代码页
- [原始资料](https://doi.org/10.1109/TSP.2013.2288675)
- [代码/工具](https://math.montana.edu/dzosso/code/)
- 数据：作者示例；也可用模拟信号
- 备注：模态不自动等于真实物理源；可能过分解或混叠。

### F07 · A Unified Approach to Interpreting Model Predictions

**作者/机构：** Scott M. Lundberg; Su-In Lee  
**年份/版本：** 2017 · 解释论文 · 进阶

- 研究内容：用加性特征归因解释个体预测。
- 方法：SHAP/Shapley值与不同解释器。
- 可以参考：说明背景样本、被解释输出和特征分组；先做表格特征。
- 复现估计：中：官方库可用；长时序直接逐点解释成本高。
- 核验范围：原始摘要/官方仓库
- [原始资料](https://arxiv.org/abs/1705.07874)
- [代码/工具](https://github.com/shap/shap)
- 数据：官方示例数据
- 备注：SHAP解释预测，不证明因果；相关特征和遮蔽分布影响解释。

### F08 · Axiomatic Attribution for Deep Networks

**作者/机构：** Mukund Sundararajan; Ankur Taly; Qiqi Yan  
**年份/版本：** 2017 · 解释论文 · 进阶

- 研究内容：提出满足指定公理的输入归因方法。
- 方法：Integrated Gradients：沿基线到输入路径积分梯度。
- 可以参考：冻结CNN后对时间或频域输入归因；比较不同基线。
- 复现估计：中：可用Captum；选基线和积分步数需检验。
- 核验范围：期刊会议页；Captum为通用实现
- [原始资料](https://proceedings.mlr.press/v70/sundararajan17a.html)
- [代码/工具](https://captum.ai/docs/introduction)
- 数据：自有已训练模型/文档示例
- 备注：数值完备性误差小也不证明物理因果正确。

### F09 · Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization

**作者/机构：** Ramprasaath R. Selvaraju; Michael Cogswell; Abhishek Das; Ramakrishna Vedantam; Devi Parikh; Dhruv Batra  
**年份/版本：** 2017 · 解释论文 · 进阶

- 研究内容：用目标输出梯度定位卷积特征中的重要区域。
- 方法：通道梯度权重与激活图组合。
- 可以参考：时频图或1D卷积网络的区域定位；标注目标类别与层。
- 复现估计：中：工具易调用；1D/2D适配与定位分辨率需检查。
- 核验范围：会议原始摘要；通用实现
- [原始资料](https://openaccess.thecvf.com/content_iccv_2017/html/Selvaraju_Grad-CAM_Visual_Explanations_ICCV_2017_paper.html)
- [代码/工具](https://captum.ai/docs/introduction)
- 数据：原论文图像任务；需另备故障信号
- 备注：热图较粗，不能把上采样后的像素视作真实高精度定位。

### F10 · Sanity Checks for Saliency Maps

**作者/机构：** Julius Adebayo; Justin Gilmer; Michael Muelly; Ian Goodfellow; Moritz Hardt; Been Kim  
**年份/版本：** 2018 · 解释评估论文 · 必读

- 研究内容：检验解释是否依赖学到的参数与标签结构。
- 方法：模型参数随机化与标签随机化检验。
- 可以参考：为自己的解释方法设计反证实验；避免只看漂亮热图。
- 复现估计：中：需要重训/随机化对照和相似度统计。
- 核验范围：原始论文摘要
- [原始资料](https://arxiv.org/abs/1810.03292)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：检验通过是必要证据之一，不是充分证明。

### F11 · Interpretable Machine Learning

**作者/机构：** Christoph Molnar  
**年份/版本：** 在线第3版；持续更新 · 在线教材 · 先读

- 研究内容：解释目标、局部/全局解释、方法限制及评价。
- 方法：SHAP、置换重要性、原型、神经网络解释等。
- 可以参考：优先读解释目标、方法概览和评价；边学边查。
- 复现估计：易到中：有实例；迁移到相关时序特征需调整。
- 核验范围：作者在线教材
- [原始资料](https://christophm.github.io/interpretable-ml-book/)
- [代码/工具](https://github.com/christophM/interpretable-ml-book)
- 数据：教材示例

### F12 · Captum: Model Interpretability for PyTorch

**作者/机构：** Captum contributors  
**年份/版本：** 持续更新 · 官方工具 · 先用

- 研究内容：给PyTorch模型计算输入/层/神经元归因。
- 方法：Integrated Gradients、Occlusion、LayerGradCam等。
- 可以参考：统一比较多种解释；记录target、baseline、batch和层。
- 复现估计：易到中：基础教程易跑；信号基线设计需思考。
- 核验范围：官方工具文档
- [原始资料](https://captum.ai/docs/introduction)
- [代码/工具](https://github.com/pytorch/captum)
- 数据：官方教程示例

### F13 · Feature selection

**作者/机构：** scikit-learn developers  
**年份/版本：** 持续更新 · 官方文档 · 先用

- 研究内容：常见特征筛选工具与用法。
- 方法：方差过滤、单变量检验、RFE、SelectFromModel。
- 可以参考：用Pipeline封装标准化、筛选和分类器；只在训练折fit。
- 复现估计：易：API完整；要自行设置分组交叉验证。
- 核验范围：官方文档
- [原始资料](https://scikit-learn.org/stable/modules/feature_selection.html)
- [代码/工具](https://github.com/scikit-learn/scikit-learn)
- 数据：官方示例/自己的特征表

### F14 · Feature Selection: A Data Perspective

**作者/机构：** Jundong Li; Kewei Cheng; Suhang Wang; Fred Morstatter; Robert P. Trevino; Jiliang Tang; Huan Liu  
**年份/版本：** 2017；预印本2016 · 综述 · 进阶

- 研究内容：从不同数据类型系统梳理特征选择。
- 方法：相似性、信息论、稀疏学习、统计方法。
- 可以参考：扩展互信息、冗余与结构化选择；做方法选型参考。
- 复现估计：中高：综述；算法实现的依赖需逐一核对。
- 核验范围：作者预印本摘要
- [原始资料](https://arxiv.org/abs/1601.07996)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：ACM Computing Surveys版本年份2017；本表链接到作者预印本。

## 结合研究

### C01 · TFN: An interpretable neural network with time-frequency transform embedded for intelligent fault diagnosis

**作者/机构：** Qian Chen; Xingjian Dong; Guowei Tu; Dong Wang; Changming Cheng; Baoxuan Zhao; Zhike Peng  
**年份/版本：** 2024 · 可解释诊断论文 · 优先复现

- 研究内容：在诊断网络中嵌入可学习时频变换。
- 方法：参数化时频卷积层与后续分类网络。
- 可以参考：对照普通卷积，观察学习频带、滤波响应和类别关系。
- 复现估计：中：作者有模型和CWRU训练流程；解释图仍需逐项核对。
- 核验范围：预印本/作者仓库
- [原始资料](https://doi.org/10.1016/j.ymssp.2023.110952)
- [代码/工具](https://github.com/ChenQian0618/TFN)
- [数据](https://engineering.case.edu/bearingdatacenter/download-data-file)
- 备注：https://arxiv.org/abs/2209.01992；结构可解释不代表后续网络完全透明。

### C02 · 一种面向机械设备故障诊断的可解释卷积神经网络

**作者/机构：** 陈钱; 陈康康; 董兴建; 皇甫一樊; 彭志科; 孟光  
**年份/版本：** 2024 · 中文论文 · 先读

- 研究内容：面向机械诊断的Chirplet可解释卷积设计。
- 方法：Chirplet参数化卷积与学习频率响应分析。
- 可以参考：中文阅读入口；学会从网络参数追踪到信号意义。
- 复现估计：中高：未确认独立代码；部分试验数据获取有限。
- 核验范围：期刊页/作者介绍
- [原始资料](https://doi.org/10.3901/JME.2024.12.065)
- 代码/工具：本次未确认官方代码
- 数据：CWRU及论文试验；私有部分本次未确认下载
- 备注：相关TFN仓库不能自动视作本论文的完整复现。

### C03 · WaveletKernelNet: An Interpretable Deep Neural Network for Industrial Intelligent Diagnosis

**作者/机构：** Tianfu Li; Zhibin Zhao; Chuang Sun; Li Cheng; Xuefeng Chen; Ruqiang Yan; Robert X. Gao  
**年份/版本：** 2022卷期；2021在线 · 可解释诊断论文 · 优先复现

- 研究内容：用连续小波卷积替换普通CNN首层。
- 方法：可学习小波尺度/平移参数和后续深层分类。
- 可以参考：理解物理可解释滤波层、参数边界及与普通卷积的消融。
- 复现估计：中：作者提供模型；训练测试指向另一个基准库。
- 核验范围：原始摘要/作者仓库README
- [原始资料](https://doi.org/10.1109/TSMC.2020.3048950)
- [代码/工具](https://github.com/HazeDT/WaveletKernelNet)
- 数据：配合D18基准的数据接口
- 备注：仓库主要models，并非独立完整训练项目；https://arxiv.org/abs/1911.07925。

### C04 · An Explainable Neural Network for Fault Diagnosis With a Frequency Activation Map

**作者/机构：** Min Su Kim; Jong Pil Yun; PooGyeon Park  
**年份/版本：** 2021 · 可解释诊断论文 · 进阶

- 研究内容：把诊断依据展示为频率激活图。
- 方法：网络约束设计与Frequency Activation Map。
- 可以参考：参考怎样把模型响应与频率成分联系起来。
- 复现估计：中高：本次未确认作者代码和完整数据入口。
- 核验范围：出版题录/摘要
- [原始资料](https://doi.org/10.1109/ACCESS.2021.3095565)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：IEEE Access 9:98962–98972；频率图提供一致性证据，不是模型正确性证明。

### C05 · Interpreting what typical fault signals look like via prototype-matching

**作者/机构：** Qian Chen; Xingjian Dong; Zhike Peng  
**年份/版本：** 2024 · 原型解释论文 · 进阶

- 研究内容：通过原型匹配展示典型故障频谱。
- 方法：编码/重构、原型匹配与重要区域分析。
- 可以参考：研究原型是否能对应故障频率与侧频结构。
- 复现估计：中高：本次未确认官方训练代码。
- 核验范围：作者预印本
- [原始资料](https://doi.org/10.1016/j.aei.2024.102849)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：https://arxiv.org/abs/2403.07033；不要误用同页推荐文章的代码链接。

### C06 · CS-SHAP: Extending SHAP to Cyclic-Spectral Domain for Better Interpretability of Intelligent Fault Diagnosis

**作者/机构：** Qian Chen; Xingjian Dong; Kui Hu; Kangkang Chen; Zhike Peng  
**年份/版本：** 2025预印本 · 事后解释论文 · 优先复现

- 研究内容：对已训练模型的载频与调制频率贡献做归因。
- 方法：将SHAP扩展到循环谱域；多信号域解释比较。
- 可以参考：最贴近先训练后解释；先模拟数据，再CWRU。
- 复现估计：中高：有完整demo；旧版SHAP依赖与解释计算量需检查。
- 核验范围：原始摘要/作者README与目录
- [原始资料](https://arxiv.org/abs/2502.06424)
- [代码/工具](https://github.com/ChenQian0618/CS-SHAP)
- [数据](https://engineering.case.edu/bearingdatacenter/download-data-file)
- 备注：本表按已核实预印本版本引用；Demo/train.py与Demo/Demo_analysis.py；代码Apache-2.0。

### C07 · Classifier-guided neural blind deconvolution: A physics-informed denoising module for bearing fault diagnosis under noisy conditions

**作者/机构：** Jing-Xiao Liao; Chao He; Jipu Li; Jinwei Sun; Shiping Zhang; Xiaoge Zhang  
**年份/版本：** 2025 · 联合学习论文 · 进阶

- 研究内容：把盲解卷积增强与诊断分类联合训练。
- 方法：时域/频域滤波、物理统计目标与分类损失联合。
- 可以参考：参考怎样将候选故障成分提取做成可学习模块。
- 复现估计：中高：作者公开代码；数据整理及损失平衡需适配。
- 核验范围：预印本/作者仓库
- [原始资料](https://doi.org/10.1016/j.ymssp.2024.111750)
- [代码/工具](https://github.com/asdvfghg/ClassBD)
- [数据](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download)
- 备注：https://arxiv.org/abs/2404.15341；属于联合训练，不是单纯冻结模型的事后分析。

### C08 · Multi-channel neural blind deconvolution: A physically interpretable network for impulsive mode extraction

**作者/机构：** Liu He; Wen Li; Qiuyang Zhou; Cai Yi; Dong Wang  
**年份/版本：** 2025 · 分量提取论文 · 选学

- 研究内容：多通道提取不同冲击模态。
- 方法：把滤波、Fourier和Hilbert包络过程网络化。
- 可以参考：复合故障分量提取思路；检查通道间冗余与真实源对应。
- 复现估计：高：本次未确认官方代码和完整数据。
- 核验范围：出版题录/摘要
- [原始资料](https://doi.org/10.1016/j.ymssp.2025.113210)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：作者姓名按出版社展示顺序保留；模态提取不等于分类器验证。

### C09 · Multilayer Grad-CAM: An effective tool towards explainable deep neural networks for intelligent fault diagnosis

**作者/机构：** Sinan Li; Tianfu Li; Chuang Sun; Ruqiang Yan; Xuefeng Chen  
**年份/版本：** 2023 · 事后解释论文 · 进阶

- 研究内容：利用多层信息解释智能故障诊断网络。
- 方法：多层Grad-CAM信息组合。
- 可以参考：比较不同层特征；避免只解释最后一层。
- 复现估计：中高：本次未确认官方代码；需核对融合与上采样。
- 核验范围：出版题录/摘要
- [原始资料](https://doi.org/10.1016/j.jmsy.2023.05.027)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口

### C10 · Explainable AI Algorithms for Vibration Data-based Fault Detection: Use Case-adadpted Methods and Critical Evaluation

**作者/机构：** Oliver Mey; Deniz Neufeld  
**年份/版本：** 2022 · 解释评估论文 · 必读

- 研究内容：比较振动故障检测中多种解释方法的优缺点。
- 方法：GradCAM、LRP、LIME；频率-RPM和阶次-RPM图；合成及不平衡数据。
- 可以参考：参考已知真值模拟、转速变化与错误解释检查。
- 复现估计：中：实验设计清楚；本次未确认完整官方复现包。
- 核验范围：作者预印本摘要
- [原始资料](https://arxiv.org/abs/2207.10732)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：原题adadpted拼写按预印本保留；期刊版本Sensors22(23):9037，10.3390/s22239037。

### C11 · Signal processing- and physics-informed neural network for explainable bearing condition monitoring

**作者/机构：** Nico Herwig; Pietro Borghesani; Wade A. Smith; Zhongxiao Peng  
**年份/版本：** 2025 · 物理可解释诊断论文 · 选学

- 研究内容：提出BearingNet，把信号处理与轴承机理纳入网络。
- 方法：可微信号处理和物理相关的结构化诊断。
- 可以参考：参考如何把各层计算与工程意义关联起来。
- 复现估计：高：本次未确认官方代码；需要较强轴承信号背景。
- 核验范围：出版题录/摘要
- [原始资料](https://doi.org/10.1016/j.ymssp.2025.112925)
- 代码/工具：本次未确认官方代码
- 数据：不适用或本次未确认独立数据入口
- 备注：MSSP235:112925；不能因名称含physics-informed就等同PDE型PINN。
