# 可编辑源文件与重新生成

本目录用于维护学习资料；做研究请从[首页六步路线](../../README.md)开始。这里没有故障诊断模型的训练入口。以下旧日期记录对应历史构建；只修改导航或模板时，无需重新生成PDF/Excel。

## 一次检查全部资料（2026-11-07新增）

从仓库根目录执行，依赖见[requirements.txt](requirements.txt)：

```bash
python -m pip install -r fault-diagnosis-learning/src/requirements.txt
python fault-diagnosis-learning/src/validate_all.py
```

`validate_all.py`先检查全部版本管理范围内的Markdown本地目标/标题、14份PDF与6份Excel清单、六步导航和5份CSV空模板的字段说明，再依次调用下方四个既有校验器，写入[总检查报告](../REPOSITORY_CHECK.json)。不会联网、训练模型或读取个人实验数据；会更新各份本地验证报告的实际执行时间。文献日期仍保留历史含义。原始数据/窗口跨集合泄漏需在自己的研究代码中另行检查。

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

## 2026-11方法详解与研究方案

`build_research_update.py`读取`deep-learning-methods/方法详解.md`和`阅读与选型.md`，生成45页方法合订本、8个分类分册、方法索引CSV和参考来源；同时将`research-update-2026-11/`两份研究文稿生成两份各5页PDF。35张方法卡使用固定字段，每卡单页，超出可用页面高度会报错；所有PDF带中文字体与章节书签。

```bash
python fault-diagnosis-learning/src/build_research_update.py
python fault-diagnosis-learning/src/validate_research_update.py
```

从仓库根目录运行；依赖`reportlab`、`PyMuPDF`，实际版本见`research-update-2026-11/DOCUMENT_VALIDATION.json`。临时字体与构建清单在已忽略的`build/research-update/`。生成器不联网、不运行模型；再次生成应保持PDF/CSV/参考来源字节一致。

`validate_research_update.py`核查35卡字段及完整正文在合订本/分册对应页面出现、11份PDF字体嵌入/书签/文本边界、索引页码、本地链接、25项来源记录、空白实验模板和原任务书哈希；不证明科学结论。`research-update-2026-11/collect_sources.py`仅在明确刷新来源时使用，记录失败而不绕过代理；上游变更后应人工重读并同步证据说明，不能自动改日期当作核验完成。
