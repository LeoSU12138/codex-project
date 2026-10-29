"""Export the supplied reading list using existing catalog metadata (stdlib only)."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = {
    '编号': 'id', '论文': 'title', '作者': 'authors', '年份': 'year',
    '期刊': 'journal', '方向': 'engineering_object', '方法': 'method',
    '输入输出': 'input_output', '原文报告的验证（历史记录）': 'reported_validation',
    '学习重点（任务书建议）': 'learning_focus', '建议实验': 'suggested_experiment',
    '限制': 'limitations', 'DOI': 'doi', '出版入口': 'source_url',
    '代码状态': 'code_status', '代码入口': 'code_url', '代码范围': 'code_scope',
    '数据状态': 'data_status', '数据入口': 'data_url',
    '历史题录核验范围': 'verification', '历史题录核对日期': 'checked',
    '既有审计范围': 'audit_scope', '既有审计日期': 'audit_date',
    '未核验细节': 'unverified_details', '实验运行状态': 'run_status',
}


def source_sections():
    text = (ROOT / '研究进展与任务书.md').read_text(encoding='utf-8')
    sections = re.findall(r'^### ([SDFC]\d\d) ([^\n]+)\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S)
    return sections


def make_rows():
    catalog = json.loads((ROOT.parent / 'research-papers/catalog.json').read_text(encoding='utf-8'))
    indexed = {r['id']: r for r in catalog}
    rows = []
    for id, _, body in source_sections():
        r = dict(indexed[id])
        doi = re.search(r'\[DOI\]\(https://doi.org/([^\s)]+)\)', body).group(1)
        assert doi.lower() == r['doi'].lower(), (id, 'DOI mismatch')
        r['learning_focus'] = re.search(r'^- \*\*应该学习和借鉴：\*\* (.+)$', body, re.M).group(1)
        rows.append({header: str(r[key]) for header, key in FIELDS.items()})
    return rows


def main():
    rows = make_rows()
    with (ROOT / '特征挖掘阅读索引.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'Exported {len(rows)} existing papers; no catalog entries added.')


if __name__ == '__main__':
    main()
