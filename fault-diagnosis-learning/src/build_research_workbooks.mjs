import fs from 'node:fs/promises';
import path from 'node:path';
const {Workbook, SpreadsheetFile} = await import(process.env.ARTIFACT_TOOL_MODULE || '@oai/artifact-tool');

// Run a copy from a private temporary directory. No repo-local dependencies required.
const [input, output, previews] = process.argv.slice(2);
if (!input || !output || !previews) throw new Error('Usage: node build_research_workbooks.mjs catalog.json output-dir preview-dir');
const records = JSON.parse(await fs.readFile(input, 'utf8'));
await fs.mkdir(output, {recursive:true});
await fs.mkdir(previews, {recursive:true});
const groups = [['深度学习','01_深度学习科研论文'],['特征挖掘','02_特征挖掘科研论文'],['融合与解释','03_融合与解释科研论文']];
const col = n => {let s=''; for(n++;n;n=Math.floor((n-1)/26)) s=String.fromCharCode(65+(n-1)%26)+s; return s;};
const font = 'Droid Sans Fallback';
for (const [theme, file] of groups) {
  const rows = records.filter(r=>r.theme===theme);
  const wb = Workbook.create();
  function sheet(name, headers, keys, widths, tag) {
    const sh = wb.worksheets.add(name);
    sh.showGridLines=false; sh.tabColor=tag==='papers'?'#163449':'#087E8B';
    sh.getRange('A2').values=[[`${theme}${name}（${rows.length}篇）`]];
    sh.getRange('A2').format={font:{name:font,size:15,bold:true,color:'#163449'},rowHeight:30};
    sh.getRange('A3').values=[['历史题录：2026-10-27｜本地审计：2026-10-28｜同编号跨表对应；黄色阅读状态可编辑。']];
    sh.getRange('A3').format={font:{name:font,size:10,color:'#61727C'},rowHeight:24};
    sh.getRange('A4').values=[['复现难度为估计，未运行论文实验；建议实验与原文报告分列。可点击来源见同目录README。']];
    sh.getRange('A4').format={font:{name:font,size:10,color:'#61727C'},rowHeight:24};
    const last=col(headers.length-1), end=rows.length+6;
    sh.getRange(`A6:${last}${end}`).values=[headers,...rows.map(r=>keys.map(k=>['checked','audit_date'].includes(k)?new Date(r[k]+'T00:00:00Z'):(r[k] ?? '')))];
    const all=sh.getRange(`A6:${last}${end}`);
    all.format={font:{name:font,size:10,color:'#243746'},wrapText:true,verticalAlignment:'top'};
    widths.forEach((w,i)=>sh.getRange(`${col(i)}6:${col(i)}${end}`).format.columnWidth=w);
    for (const key of ['checked', 'audit_date']) {
      const dateColumn=keys.indexOf(key);
      if(dateColumn>=0) sh.getRange(`${col(dateColumn)}7:${col(dateColumn)}${end}`).setNumberFormat('yyyy-mm-dd');
    }
    sh.getRange(`A6:${last}6`).format={fill:'#163449',font:{name:font,size:10,bold:true,color:'#FFFFFF'},rowHeight:32,verticalAlignment:'center',wrapText:true};
    rows.forEach((r,i)=>{
      const lines=keys.map((k,j)=>Math.ceil([...String(r[k]??'')].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0)/(widths[j]-4)));
      const row=sh.getRange(`A${i+7}:${last}${i+7}`);
      row.format.rowHeight=Math.max(70,16*Math.max(...lines)+18);
      if(i%2===0) row.format.fill='#F0F5F6';
      keys.forEach((k,j)=>{if(k.endsWith('_url') && r[k]) sh.getRange(`${col(j)}${i+7}`).format.font.color='#087E8B';});
    });
    sh.tables.add(`A6:${last}${end}`,true,tag).showFilterButton=true;
    sh.freezePanes.freezeRows(6); sh.freezePanes.freezeColumns(2);
    const progress=keys.indexOf('reading_status');
    if(progress>=0){
      const cell=sh.getRange(`${col(progress)}7:${col(progress)}${end}`);
      cell.format.fill='#FFF2CC';
      cell.dataValidation={rule:{type:'list',values:['未读','在读','已读','拟复现','已复现']}};
    }
    return sh;
  }
  sheet('论文与引用',
    ['编号','方法简称','文献名称','完整作者','年份（卷期优先）','期刊','卷','期','页码/文章号','类型','工程对象','研究内容','研究方法','适合引用的位置/论点','DOI/原文','在线年份','阅读优先级','阅读状态','出版状态'],
    ['id','short_name','title','authors','year','journal','volume','issue','pages','type','engineering_object','research_problem','method','citation_use','source_url','online_year','priority','reading_status','publication_status'],
    [9,26,66,48,16,45,10,12,18,23,26,48,50,52,58,15,17,15,30], 'papers');
  sheet('工程验证与复现',
    ['编号','方法简称','原文报告的验证','建议借鉴的实验（本次整理建议）','局限与使用边界','复现难度与原因（估计）','代码状态','代码入口','代码覆盖范围','数据状态','数据入口','历史核验范围','补充证据入口','题录说明','历史核对日期','实验运行状态','输入与输出（导读摘要）','未核验的工程细节','本次审计日期','本次审计范围'],
    ['id','short_name','reported_validation','suggested_experiment','limitations','reproduction','code_status','code_url','code_scope','data_status','data_url','verification','evidence_url','metadata_note','checked','run_status','input_output','unverified_details','audit_date','audit_scope'],
    [9,26,54,54,58,52,29,64,47,49,64,60,64,58,16,22,58,66,18,68], 'resources');
  wb.recalculate();
  const inspect=await wb.inspect({kind:'region',sheetId:'论文与引用',range:'A6:E8',maxChars:1800,tableMaxRows:3,tableMaxCols:5});
  await fs.writeFile(path.join(previews,`${file}_inspect.ndjson`),inspect.ndjson);
  const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'final error scan'});
  await fs.writeFile(path.join(previews,`${file}_errors.ndjson`),errors.ndjson);
  for(const [name,range,tag] of [['论文与引用','A6:E9','metadata'],['论文与引用','K6:N9','methods'],['工程验证与复现','A6:F9','validation'],['工程验证与复现','G6:J9','code'],['工程验证与复现','Q6:T9','audit']]){
    const img=await wb.render({sheetName:name,range,scale:1.25,format:'png'});
    await fs.writeFile(path.join(previews,`${file}_${tag}.png`),new Uint8Array(await img.arrayBuffer()));
  }
  const xlsx=await SpreadsheetFile.exportXlsx(wb); await xlsx.save(path.join(output,file+'.xlsx'));
  console.log(JSON.stringify({file:file+'.xlsx',records:rows.length,sheets:2}));
}
