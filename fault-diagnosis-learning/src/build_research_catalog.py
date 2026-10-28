"""Build citation-oriented engineering catalogs from a verified metadata snapshot.

Standard-library only. Does not download papers or execute their experiments.
"""
import csv
import json
from pathlib import Path
from research_annotations import R
from research_audit import audit_fields, DETAILS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research-papers'
CHECKED = '2026-10-27'
GROUPS = [('深度学习', '01_深度学习科研论文', ['D', 'S01', 'S02', 'S04']),
          ('特征挖掘', '02_特征挖掘科研论文', ['F', 'S03']),
          ('融合与解释', '03_融合与解释科研论文', ['C'])]

def selected(id, selectors):
    return any(id.startswith(s) if len(s) == 1 else id == s for s in selectors)

def bib_escape(value):
    return str(value).replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')

def main():
    metadata = json.loads((OUT / 'source_metadata.json').read_text())
    assert set(metadata) == set(R) == set(DETAILS), 'Annotation and metadata IDs differ'
    evidence = json.loads((OUT / 'AUDIT_EVIDENCE.json').read_text())
    records = []
    for id, annotation in R.items():
        m = metadata[id]
        # Use issue/volume year where available; retain first-online year separately.
        date = m.get('published-print') or m.get('published') or m.get('published-online')
        year = date['date-parts'][0][0]
        online = (m.get('published-online') or {}).get('date-parts', [['']])[0][0]
        authors = m.get('author', [])
        title = m['title'][0]
        journal = m['container-title'][0]
        pages = m.get('page') or m.get('article-number') or ''
        note = 'Crossref DOI题录；优先使用卷期年，在线年另列。'
        if id == 'C02':
            # Publisher supplies missing authors and full page range in Crossref.
            title = '一种面向机械设备故障诊断的可解释卷积神经网络'
            authors = [{'name': x} for x in ['陈钱', '陈康康', '董兴建', '皇甫一樊', '彭志科', '孟光']]
            journal, pages = '机械工程学报', '65-76'
            note += ' 中文题名、完整作者及65–76页据期刊原页补全。'
        if id == 'C06':
            note += ' 采用2026年正式期刊版；保留全部六位作者，包括Guang Meng。'
        if id == 'C10':
            note += ' 原题名中的Adadpted拼写按出版记录保留。'
        if id == 'C12':
            note += ' 出版页标注In Press, Journal Pre-proof，2026-05-20在线；题录未提供卷期，不推测补写。'
        group = next(name for name, _, selectors in GROUPS if selected(id, selectors))
        kind = '综述/教程' if id in ['S01', 'S02', 'S03'] else ('综述与基准比较' if id == 'S04' else '方法/应用/基准研究')
        r = dict(id=id, theme=group, title=title,
                 authors='; '.join(a.get('name') or ' '.join(filter(None, [a.get('given'), a.get('family')])) for a in authors),
                 author_structured=authors, year=year, online_year=online,
                 journal=journal, volume=m.get('volume') or '', issue=m.get('issue') or '',
                 pages=pages, doi=m['DOI'], source_url='https://doi.org/' + m['DOI'],
                 type=kind, publication_status='期刊在线预校样（In Press）' if id == 'C12' else '期刊卷期已登记',
                 checked=CHECKED, metadata_note=note, **annotation)
        if not r['evidence_url']:
            r['evidence_url'] = r['source_url']
        r['verification'] = 'DOI题录、出版摘要/可见正文片段；未完成逐页全文复核。'
        if id in ['D02', 'D09', 'D10', 'C10']:
            r['verification'] = 'DOI题录、开放正文相关部分；未逐项复算实验。'
        if id in ['D07', 'S04', 'C01', 'C03', 'C06', 'C07']:
            r['verification'] += ' 已阅读作者仓库README，核对代码范围；未执行。'
        if id in ['F03', 'F05', 'F06', 'F07', 'F08']:
            r['verification'] += ' 已核对作者代码页说明；未执行。'
        if id == 'C02':
            r['verification'] = 'DOI、期刊原页题录及摘要；完整实验须读全文。'
        if id == 'C12':
            r['verification'] = 'Crossref题录与出版页摘要/章节片段；未获取全文和工程数据。'
        r.update(audit_fields(id, evidence))
        records.append(r)

    (OUT / 'catalog.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    flatkeys = [k for k in records[0] if k != 'author_structured']
    with (OUT / '工程科研论文.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flatkeys, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)

    bib, ris = [], []
    for r in records:
        authors_bib, authors_ris = [], []
        for a in r['author_structured']:
            if a.get('name'):
                authors_bib.append('{' + a['name'] + '}')
                authors_ris.append(a['name'])
            else:
                name = a['family'] + (', ' + a['given'] if a.get('given') else '')
                authors_bib.append(name)
                authors_ris.append(name)
        fields = dict(title='{' + bib_escape(r['title']) + '}', author=' and '.join(authors_bib),
                      journal=bib_escape(r['journal']), year=r['year'], volume=r['volume'],
                      number=r['issue'], pages=r['pages'].replace('-', '--'), doi=r['doi'], url=r['source_url'])
        bib.append('@article{FD_' + r['id'] + ',\n' + '\n'.join(f'  {k} = {{{v}}},' for k, v in fields.items() if v != '') + '\n}\n')
        lines = ['TY  - JOUR', 'ID  - FD_' + r['id'], 'TI  - ' + r['title']]
        lines += ['AU  - ' + a for a in authors_ris]
        lines += ['JO  - ' + r['journal'], 'PY  - ' + str(r['year'])]
        if r['volume']: lines.append('VL  - ' + r['volume'])
        if r['issue']: lines.append('IS  - ' + r['issue'])
        if r['pages']:
            parts = r['pages'].split('-', 1)
            lines.append('SP  - ' + parts[0])
            if len(parts) == 2: lines.append('EP  - ' + parts[1])
        lines += ['DO  - ' + r['doi'], 'UR  - ' + r['source_url'], 'ER  - ']
        ris.append('\n'.join(lines))
    (OUT / 'engineering_references.bib').write_text('\n'.join(bib), encoding='utf-8')
    (OUT / 'engineering_references.ris').write_text('\n\n'.join(ris) + '\n', encoding='utf-8')

    intro = '''# 故障诊断工程科研论文库

**面向后续科研写作和工程实验的38篇期刊论文，核对日期：2026-10-27。** 其中34篇为方法、应用或基准研究，4篇为综述、教程或综述与比较研究。这里围绕“研究问题—方法—工程验证—可引用内容”整理；[原入门教程与43条学习资料](../README.md)仍保留。

## 2026-10-28审计增补

本次保留38篇和既有题录，不重复检索凑数。每篇补入**输入→输出**、**未核验的工程细节**、**本次审计日期/范围**，Excel第二张表末尾可查看。原`checked`和`verification`仍代表2026-10-27历史核验；不能把它们当作本次在线复核。

本次重新阅读C01/C03/C06/C07/C10/D07/S04的作者README，确认其声明的代码入口与覆盖范围，未执行模型。[审计证据与网络结果](AUDIT_EVIDENCE.json)记录请求入口、读取方式和摘要哈希。CS-SHAP作者README仍给2025预印本引文，可核对完整六位作者；本库2026期刊版来自原有Crossref快照。

Crossref、DOI解析、中文期刊和ScienceDirect页面本次均受代理403限制，故**C12的In Press是2026-10-27历史状态，当前最终出版状态未确认**，其卷期仍留空；所有38篇均未重新逐页阅读全文。未知设备、故障、工况和数据条件明确写为未核验，不推测补齐。旧43条学习资料与其Excel继续保留为学习快照，正式引用优先使用本库，并在投稿前确认最终出版版本。

## 文件与使用方式

| 主题 | Excel | 篇数 |
| --- | --- | --- |
| 深度学习诊断与迁移 | [01_深度学习科研论文.xlsx](01_深度学习科研论文.xlsx) | 13 |
| 特征挖掘与故障信号分析 | [02_特征挖掘科研论文.xlsx](02_特征挖掘科研论文.xlsx) | 13 |
| 深度学习、特征挖掘与解释结合 | [03_融合与解释科研论文.xlsx](03_融合与解释科研论文.xlsx) | 12 |

每表有“论文与引用”和“工程验证与复现”两张工作表，通过编号对应。第一张用于选文献和组织相关工作，第二张用于设计对照实验和检查资源条件。表格可筛选，黄色阅读状态可编辑；网址保留为完整文本，本页链接可直接点击。

[BibTeX引文文件](engineering_references.bib) · [RIS引文文件](engineering_references.ris) · [全量CSV](工程科研论文.csv) · [结构化JSON](catalog.json) · [题录来源快照](source_metadata.json)

BibTeX可用于LaTeX，RIS适合导入Zotero、EndNote等软件；最终参考文献样式按投稿期刊要求设置。中文姓名在BibTeX中作为完整姓名保留。编号只在本科研论文库中有效，与旧版入门资料编号不是同一套。

## 最贴近你原始思路的阅读路线

你提出的是“先有诊断模型，再通过特征挖掘检查模型依据”。优先读 **C10（解释如何被检验）→ C09（多层Grad-CAM）→ C06（CS-SHAP）**，再用D02或D07建立普通CNN基线。C06的正式期刊版已于2026年发表，下面使用其正式DOI和完整六位作者。

| 研究路线 | 关键文献 | 你可以形成的实验 |
| --- | --- | --- |
| 冻结模型后解释 | C06、C09、C10 | 用有真值的模拟信号检查定位，再对重要/不重要区域做对照干预，最后在独立测试工况检查稳定性 |
| 从结构上引入信号含义 | C01、C02、C03、C04、C11 | 比较参数化核与普通卷积，检验频响、故障频率和分类表现；这需要改变模型 |
| 特征提取和诊断联合优化 | C07、C08 | 对照传统解卷积、无前端、固定前端、联合训练，并检查输出冲击周期 |
| 柴油机与喷油器工程案例 | D08、D09、F09、F10、F11、C12 | 从故障类型、程度、工况与曲轴角事件组织研究；区分仿真、实验台与现场案例 |

F09和F11可帮助你构造与机理有关的特征，但它们不等同于“事后证明一个深层网络”。注意力图、聚类图或高准确率各自只能回答部分问题。较稳妥的论文表述是：特征分析与对照实验为模型使用故障相关信息提供支持；避免直接声称“证明模型完全正确”。

## 如何把它们用进自己的论文

1. **引言和相关工作：** S01、S02构建领域背景；按实际任务选D、F、C中的原始研究论文，说明已有方法解决了什么、仍有什么限制。
2. **方法：** 使用或改造VMD、FMD、小波核、盲解卷积、Grad-CAM等方法时，引用相应原始论文，并明确你改变的部分。不能仅引用综述替代算法来源。
3. **实验：** D07、S04帮助选统一基线，F12帮助理解CWRU；完整记录独立分组、切片、标准化、种子和超参数。先按设备/运行记录划分，再在各集合内切片。
4. **解释与讨论：** 区分“性能提升”“解释忠实于模型”“解释符合故障机理”。对重要频带、无关频带和随机频带分别干预，检查干预是否造成不合理的分布外信号。选参和解释方案调试用验证集，最终测试集保留到最后。
5. **工程外推：** 同一实验台的跨负载结果不自动代表跨设备或现场有效；目标域无标签数据参与训练属于域适应，不能写成训练时完全未知域的泛化。

“建议借鉴的实验”是本次整理提出的建议，不代表原论文已经做过这些实验。复现难度是材料审阅后的估计；**本次未运行论文训练、未下载全量数据、未复算论文数值**。“未确认作者代码”不等于“没有代码”；已找到代码也不代表全部实验、数据和许可都齐全。

## 检索与核验范围

这是有目的的叙述性文献调研，聚焦机械振动、旋转机械、柴油机及可解释诊断，不是覆盖所有故障诊断方向的系统综述，也不构成论文质量排名。检索出版商页面、Crossref DOI题录、机构页面、开放全文及作者代码页，按题名/DOI去重。部分内容仅能核对摘要或公开片段，范围逐条记录。综述、方法原文、公开基准和工程案例均保留，以满足不同引用用途。

题录采用期刊来源；有卷期年时优先用卷期年，并在表中保留在线年份。C02的Crossref缺少作者，按期刊原页补全中文题名、六位作者和页码；C12出版页仍标注In Press、Journal Pre-proof（在线预校样），尚未给卷期，留空而不推测，投稿前应再次确认最终版本。旧入门资料保留为学习快照，**正式引用与代码状态以本目录更新后的记录为准**。这里提供原创导读和外部链接，不转载付费论文全文。

## 逐篇文献与工程用途
'''
    chunks = [intro]
    for theme, _, selectors in GROUPS:
        chunks.append('\n### ' + theme + '\n')
        for r in records:
            if not selected(r['id'], selectors): continue
            volume = r['volume'] + ('(' + r['issue'] + ')' if r['issue'] else '')
            citation = f"{r['authors']}. {r['title']}. {r['journal']}, {r['year']}"
            if volume: citation += ', ' + volume
            if r['pages']: citation += ': ' + r['pages']
            chunks.append(f"\n#### {r['id']} · {r['short_name']}\n\n{citation}. [DOI]({r['source_url']})\n\n")
            rows = [('类型与对象', r['type'] + '；' + r['engineering_object']),
                    ('研究内容', r['research_problem']), ('研究方法', r['method']),
                    ('原文报告的验证', r['reported_validation']), ('适合引用的位置/论点', r['citation_use']),
                    ('建议借鉴的实验', r['suggested_experiment']), ('复现难度（估计）', r['reproduction']),
                    ('局限与使用边界', r['limitations']),
                    ('输入与输出（导读摘要）', r['input_output']),
                    ('未核验的工程细节', r['unverified_details']),
                    ('本次审计', r['audit_date'] + '；' + r['audit_scope'])]
            chunks.append('| 项目 | 内容 |\n| --- | --- |\n' + ''.join(f'| {k} | {v} |\n' for k, v in rows))
            code = f"[{r['code_status']}]({r['code_url']})" if r['code_url'] else r['code_status']
            data = f"[数据入口]({r['data_url']})；" if r['data_url'] else ''
            chunks.append(f"\n代码：{code}；{r['code_scope']}。数据：{data}{r['data_status']}。\n\n")
            chunks.append(f"历史核验范围（{r['checked']}）：{r['verification']} [补充来源]({r['evidence_url']})。{r['metadata_note']}\n")
    (OUT / 'README.md').write_text(''.join(chunks), encoding='utf-8')
    print(json.dumps({'papers': len(records), 'groups': {t: sum(selected(r['id'], s) for r in records) for t, _, s in GROUPS}}, ensure_ascii=False))

if __name__ == '__main__':
    main()
