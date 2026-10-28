# 可编辑源文件与重新生成

2026-10-28维护：三册PDF当前为24/15/11页；科研论文保持38篇。原43条入门工作簿未重建、文件保持不变。

主内容位于`build_deep_learning.py`、`deep_extra.py`、`build_features.py`、`build_combined.py`；书目内容位于`catalog.py`。修改这些文件后可重新生成PDF、Markdown、JSON与CSV。

## PDF与文字版

需要Python、ReportLab、PyMuPDF，依赖列表见`requirements.txt`。在本目录执行：

```bash
python -m pip install -r requirements.txt
python catalog.py
python build_deep_learning.py
python build_features.py
python build_combined.py
```

输出在上级`guides/`和`references/`。中文字体由PyMuPDF提供的CJK字体生成并嵌入PDF，不需要用户单独下载安装中文字体。中间字体和版面检查文件位于`build/`。正文按页组织，新增段落过长时脚本会提示溢出，需要调整分页。

## Excel

`build_workbooks.mjs`使用`@oai/artifact-tool`生成工作簿。该依赖在本次文档制作环境中提供；普通本地Node环境未必可以安装。没有该环境也能直接使用现成Excel，或用Excel/WPS导入CSV继续编辑。

在已有该依赖的环境中，从项目目录执行：

```bash
node src/build_workbooks.mjs
```

脚本建立三张工作表、筛选表、冻结行列和阅读状态下拉框，并输出预览用于人工检查。URL使用完整文本，避免不支持的超链接公式产生错误单元格。可点击链接集中在`references/README.md`。

## 内容验证

`validate_artifacts.py`检查PDF页数/边界/链接、工作簿错误单元格/表结构/编号一致性及Python语法。它不训练模型，也不验证论文结论。执行：

```bash
python validate_artifacts.py
```

2026-10-28已检查本次全部受影响/移页的13个PDF页面，以及重建的三份科研工作簿各两张表的抽样预览。原版逐页检查属于历史记录。修改文字或列宽后，应重新渲染检查。

## 工程科研论文库（2026-10-27增补）

`research_annotations.py`维护原创中文导读，`../research-papers/source_metadata.json`保留Crossref必要题录字段。`build_research_catalog.py`统一生成README、JSON、CSV、BibTeX和RIS。C02的中文题名、作者及页码按期刊原页补全，修正逻辑集中在生成器内；C12保留在线预校样状态。

```bash
python build_research_catalog.py
python validate_research.py
```

Excel生成器`build_research_workbooks.mjs`接受三个绝对路径：输入JSON、输出目录、预览目录。默认导入`@oai/artifact-tool`；若包已存在但exports入口不兼容，可通过`ARTIFACT_TOOL_MODULE`指定其受信任的本地`dist/artifact_tool.mjs`绝对路径。缺依赖时不要替换有效既有Excel或假称重建成功。预览请放在仓库外或已忽略的`build/`中。

```bash
ARTIFACT_TOOL_MODULE=/absolute/tool/dist/artifact_tool.mjs node src/build_research_workbooks.mjs /absolute/repo/fault-diagnosis-learning/research-papers/catalog.json /absolute/repo/fault-diagnosis-learning/research-papers /absolute/tmp/previews
```

无该工具的环境可以直接使用发布的Excel，或导入CSV继续编辑。`validate_research.py`只用Python标准库，检查书目完整性、DOI去重、BibTeX/RIS与JSON一致性、Excel单元格/编号/表结构/筛选/冻结窗格/日期类型，以及本目录的Markdown相对链接。它不执行论文模型，也不能替代全文阅读和实验复现。

## 本次审计字段与重建顺序

`research_audit.py`维护38条输入输出摘要及逐条未核验的工程细节；`research-papers/AUDIT_EVIDENCE.json`是本次网络请求/作者README核对记录。`build_research_catalog.py`把它们合并到JSON、CSV、README和三份科研Excel的第二张表。`checked`/`verification`保留历史题录日期和范围；`audit_date`/`audit_scope`是2026-10-28审计，不能通过改日期冒充重新读了出版商或全文。

从仓库根目录重建本次内容：

```bash
python fault-diagnosis-learning/src/build_deep_learning.py
python fault-diagnosis-learning/src/build_features.py
python fault-diagnosis-learning/src/build_combined.py
python fault-diagnosis-learning/src/build_research_catalog.py
# 设置为已安装且受信任的artifact-tool模块实际路径；没有时不要执行Excel重建
ARTIFACT_TOOL_MODULE=/absolute/tool/dist/artifact_tool.mjs node fault-diagnosis-learning/src/build_research_workbooks.mjs "$PWD/fault-diagnosis-learning/research-papers/catalog.json" "$PWD/fault-diagnosis-learning/research-papers" /tmp/fault-research-previews
python fault-diagnosis-learning/src/validate_artifacts.py
python fault-diagnosis-learning/src/validate_research.py
```

验证新增：PDF/Markdown关键概念、学习资源CSV与JSON一致性；38篇题名、完整作者顺序、卷期、页码、年份及BibTeX/RIS字段一致性；Excel新增审计字段和日期类型。运行记录写入真实执行时间，不更改历史核验日期。脚本不访问论文网站、不执行模型；网络和人工视觉检查在`TASK_PROGRESS.md`另记。
