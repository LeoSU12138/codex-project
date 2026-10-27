# 可编辑源文件与重新生成

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

最终版另做了逐页PDF视觉检查和Excel预览检查。修改文字或列宽后，应重新渲染检查。
