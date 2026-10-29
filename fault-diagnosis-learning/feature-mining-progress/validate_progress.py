"""Validate the imported brief and its reading index without network requests."""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_index import FIELDS, ROOT, make_rows, source_sections


def main():
    manifest = json.loads((ROOT / 'IMPORT_MANIFEST.json').read_text(encoding='utf-8'))
    original = ROOT / manifest['archived_file']
    raw = original.read_bytes()
    assert len(raw) == manifest['original_bytes']
    assert hashlib.sha256(raw).hexdigest() == manifest['original_sha256'], 'Archived brief changed'
    sections = source_sections()
    ids = [id for id, _, _ in sections]
    assert ids == manifest['paper_ids']
    assert len(ids) == len(set(ids)) == 31
    catalog_path = ROOT.parent / 'research-papers/catalog.json'
    catalog = {r['id']: r for r in json.loads(catalog_path.read_text(encoding='utf-8'))}
    assert len(catalog) == 38 and set(ids) <= set(catalog)
    dois = []
    for id, _, body in sections:
        r = catalog[id]
        citation = re.search(r'^\*\*论文：\*\* (.+)（(\d{4})）\. (.+)\. \[DOI\]\(https://doi.org/([^\s)]+)\)', body, re.M)
        assert citation, id
        authors, year, title_journal, doi = citation.groups()
        assert authors == r['authors'], (id, 'authors')
        assert int(year) == r['year'], (id, 'year')
        assert title_journal == r['title'] + '. ' + r['journal'], (id, 'title/journal')
        assert doi.lower() == r['doi'].lower(), (id, 'DOI')
        assert re.fullmatch(r'10\.\d{4,9}/\S+', doi), id
        dois.append(doi.lower())
    assert len(set(dois)) == 31
    with (ROOT / '特征挖掘阅读索引.csv').open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == list(FIELDS)
        rows = list(reader)
    assert rows == make_rows(), 'Reading CSV differs from sources'
    assert all(r['实验运行状态'] == '未运行论文实验' for r in rows)
    candidate_section = original.read_text(encoding='utf-8').split('## 五、近期补充方向\n', 1)[1].split('\n## 六、', 1)[0]
    assert len(re.findall(r'^- 《', candidate_section, re.M)) == manifest['candidate_count'] == 2
    assert '10.1016/j.ress.2025.111935' not in dois
    local_links = external_links = 0
    for p in [ROOT / 'README.md', original, ROOT.parent / 'README.md', ROOT.parents[1] / 'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            parts = urlsplit(link)
            if parts.scheme:
                assert parts.scheme in ['http', 'https'] and parts.hostname, (p, link)
                assert not parts.username and not parts.password, (p, 'credential in URL')
                external_links += 1
            elif parts.path:
                target = (p.parent / unquote(parts.path)).resolve()
                # This run creates its own linked report only after all source checks pass.
                if target != ROOT / 'VALIDATION.json':
                    assert target.exists(), (p, link)
                local_links += 1
    report = {
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'result': 'passed', 'original_byte_identical': True,
        'original_sha256': manifest['original_sha256'],
        'indexed_existing_papers': 31, 'unique_doi': 31,
        'formal_catalog_papers': len(catalog), 'candidates_not_added': 2,
        'authors_titles_years_doi_match_catalog': True,
        'csv_all_fields_match_sources': True,
        'local_links_checked': local_links, 'external_link_syntax_checked': external_links,
        'live_external_links_checked': 0, 'model_experiments_run': False,
        'scope': 'Document import and local consistency only. Source verification claims remain historical or user-supplied.',
        'artifacts': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [original, ROOT/'特征挖掘阅读索引.csv', ROOT/'README.md', ROOT/'IMPORT_MANIFEST.json']},
    }
    (ROOT / 'VALIDATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'artifacts'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
