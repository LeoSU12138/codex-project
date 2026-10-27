from catalog import R
from xml.sax.saxutils import escape
def catalog_pages(prefix):
    rows=[r for r in R if r['id'].startswith(prefix)]
    for start in range(0,len(rows),6):
        new('参考资料与原始入口','来源索引','核对日期：2026-10-26。完整作者、研究方法、代码和数据见配套Excel；标题可点击。')
        for r in rows[start:start+6]:
            para(f"<font color='#087E8B'>[{r['id']}]</font> <link href='{escape(r['source_url'])}' color='#087E8B'>{escape(r['title'])}</link>",'table',gap=3)
            authors=r['authors'].split('; ')
            brief='; '.join(authors[:2])+(' et al.' if len(authors)>2 else '')
            para(escape(brief+'｜'+r['year']+'｜'+r['type']),'small',gap=2)
            para(escape(r['reference_value']),'small',gap=15)
        para('复现难度属于本次资料条件下的估计，全部条目均未运行验证。“未确认代码”表示本次没有确认，并不等于作者没有发布。课程/综述的阅读难度与论文数值复现难度不能直接比较。','small')
def save_checks():
    FILE.with_suffix('.md').write_text('\n'.join(md),encoding='utf8')
    dest=TMP/(FILE.stem+'_layout.json')
    dest.write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    print(json.dumps({'file':str(FILE),'pages':page,'min_body_bottom':min(x['body_bottom'] for x in checks)},ensure_ascii=False))
