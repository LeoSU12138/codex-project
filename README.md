# codex-project
刘昌顺学习仓库

## 2048 小游戏

无需安装第三方依赖，使用 Python 3 启动：

```bash
python3 main.py
```

在浏览器访问服务的 8000 端口。支持 `--port 8080` 指定端口；默认监听所有网卡，`--host 127.0.0.1` 可限制本机访问。按 Ctrl+C 停止。也可以直接用浏览器打开 `web/index.html`。

- 使用方向键、WASD、屏幕按钮或在棋盘上滑动。
- 相同数字相遇会合并，每个方块在一回合内只合并一次。
- 达到 2048 后可继续挑战，无可用移动时游戏结束。
- 最高分保存在当前浏览器中，重新开始会重置本局得分。

规则测试（需要 Node.js，无需 npm 依赖）：

```bash
node --test tests/game.test.js
```

## 故障诊断学习资料

[进入深度学习、特征挖掘与结合研究学习目录](fault-diagnosis-learning/README.md)。包含3份中文入门PDF（共48页）、3份可筛选参考资料Excel（43条资料），以及可编辑文字版、CSV/JSON书目和文档构建脚本。

**科研写作与工程实验：** [38篇工程科研论文库](fault-diagnosis-learning/research-papers/README.md)，按深度学习、特征挖掘、融合与解释分成3份Excel。逐篇列出完整作者、DOI、研究方法、工程验证、引用用途、实验借鉴点、复现难度和代码/数据入口；附BibTeX、RIS引文文件。
