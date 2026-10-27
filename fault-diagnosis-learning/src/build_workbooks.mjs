import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const records=JSON.parse(await fs.readFile(path.join(root,'references/catalog.json'),'utf8'));
const out=path.join(root,'references');
const previews=path.join(root,'..','tmp','previews');
await fs.mkdir(previews,{recursive:true});
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
const groups=[['D','01_深度学习参考文献','深度学习'],['F','02_特征挖掘参考文献','特征挖掘'],['C','03_融合研究参考文献','融合研究']];
for(const [prefix,file,label] of groups){
 const wb=Workbook.create(); const rows=records.filter(r=>r.id.startsWith(prefix));
 function sheet(name,title,headers,keys,widths){
  const sh=wb.worksheets.add(name);sh.showGridLines=false;sh.tabColor='#163449';
  sh.getRange('A2').values=[[title]];sh.getRange('A2:J2').format.rowHeight=25;
  sh.getRange('A2').format.font={name:'Droid Sans Fallback',size:14,bold:true,color:'#163449'};
  sh.getRange('A3').values=[['2026-10-26 核对｜按表头筛选；向右查看全部字段；复现难度为估计，均未运行验证']];
  sh.getRange('A3:J3').format.rowHeight=24;sh.getRange('A3').format.font={name:'Droid Sans Fallback',size:10,color:'#61727C'};
  const end=rows.length+5,last=col(headers.length-1);
  sh.getRange(`A5:${last}${end}`).values=[headers,...rows.map(r=>keys.map(k=>r[k]))];
  const whole=sh.getRange(`A5:${last}${end}`);
  whole.format.font={name:'Droid Sans Fallback',size:10,color:'#243746'};whole.format.wrapText=true;whole.format.verticalAlignment='top';
  widths.forEach((w,i)=>sh.getRange(`${col(i)}5:${col(i)}${end}`).format.columnWidth=w);
  sh.getRange(`A5:${last}5`).format={fill:'#163449',font:{name:'Droid Sans Fallback',size:10,bold:true,color:'#FFFFFF'},rowHeight:30,verticalAlignment:'center',horizontalAlignment:'center',wrapText:true};
  for(let r=0;r<rows.length;r++){ const lengths=keys.map((k,i)=>{const units=[...String(rows[r][k])].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0);return Math.ceil(units/(widths[i]-3));}); sh.getRange(`A${r+6}:${last}${r+6}`).format.rowHeight=Math.max(54,14*Math.max(...lengths)+12); }
  for(let i=6;i<=end;i++)if(i%2===0)sh.getRange(`A${i}:${last}${i}`).format.fill='#F0F5F6';
  const tbl=sh.tables.add(`A5:${last}${end}`,true,prefix+(name==='文献与方法'?'Methods':'Resources'));tbl.showFilterButton=true;
  sh.freezePanes.freezeRows(5);sh.freezePanes.freezeColumns(1);
  if(name==='复现与资源'){ for(let r=0;r<rows.length;r++)for(const [j,k] of [[4,'code_url'],[5,'data_url'],[6,'source_url']]){const url=rows[r][k];if(url.startsWith('https://')){const cell=sh.getRange(`${col(j)}${r+6}`);cell.values=[[url]];cell.format.font.color='#087E8B';}}}
  return sh;
 }
 const s=sheet('文献与方法',label+'｜文献与方法',['编号','文献/资料名称','作者或机构','年份/版本','类型','阅读优先级','研究/教学内容','研究方法','可以参考什么','阅读进度'],['id','title','authors','year','type','priority','content','method','reference_value','reading_status'],[9,57,42,21,18,16,48,48,48,14]);
 s.getRange(`J6:J${rows.length+5}`).dataValidation={rule:{type:'list',values:['未读','在读','已读','拟复现','已复现']}};
 s.getRange(`J6:J${rows.length+5}`).format.fill='#FFF2CC';
 sheet('复现与资源',label+'｜复现与资源',['编号','文献/资料名称','复现难度与原因','本次核验范围','代码/工具入口','数据入口与说明','原始资料链接','备注与限制','核对日期','实验核验状态'],['id','title','reproduction','verification','code_url','data_url','source_url','note','checked','run_status'],[9,50,52,37,60,60,60,63,16,18]);
 const g=wb.worksheets.add('使用与阅读路线');g.showGridLines=false;g.tabColor='#8799A0';
 const route=prefix==='D'?'D01/D02/D04 → D05/D06 → D07/D08/D18 → D09/D10 → 按需D11–D17':prefix==='F'?'F01/F02 → F03/F04 → F13/F11 → F08/F12/F10 → F05/F06/F07':'C02 → C01/C03 → C06/C10 → C07；其余作为扩展';
 const guide=[['项目','说明'],['本表范围',`${rows.length}条精选资料。属于面向入门的定向调研，不是穷尽式系统综述。`],['如何阅读','文献与方法：比较内容和用途；复现与资源：按同一编号查难度和限制。URL保留为可复制文本；仓库references/README.md提供可直接点击的链接。'],['建议顺序',route],['难度口径','易：教程/小示例较齐；中：需适配数据或依赖；高：理论/实现/算力或资源门槛较大；不适用：综述不是单一实验。'],['核验边界','核验题录、摘要、公开文档或README；具体范围逐条注明。未下载全量数据，未执行论文训练，也未审计全部代码。'],['代码说明','“未确认官方代码”不是“无代码”。Captum等通用库不等于原论文的完整官方复现；代码可访问不保证环境可运行。'],['数据说明','公开入口不等于数据已下载；下载条款、引用方式、版本和许可应按原站核对。链接可能随时间变化。'],['阅读进度','黄色单元格可选未读/在读/已读/拟复现/已复现；请在自己的复现记录中补配置、划分和结果。'],['首要实验原则','独立分组后切片；筛选和标准化只在训练内拟合；测试集不参与选模型。'],['检索范围','优先作者论文、出版社、会议/期刊原页、官方文档、作者GitHub和大学数据站；用标题/DOI核对。'],['版本说明','书目年份区分预印本与卷期；本文不据引用次数排名。综述主要用来构建基础地图，高级论文不要求初学者全部掌握。']];
 g.getRange(`A2:B${guide.length+1}`).values=guide;g.getRange(`A2:B${guide.length+1}`).format={font:{name:'Droid Sans Fallback',size:11,color:'#243746'},wrapText:true,verticalAlignment:'center'};g.getRange('A2:A14').format.columnWidth=22;g.getRange('B2:B14').format.columnWidth=100;g.getRange(`A3:B${guide.length+1}`).format.rowHeight=65;g.getRange('A2:B2').format={fill:'#163449',font:{name:'Droid Sans Fallback',size:11,color:'#FFFFFF',bold:true},rowHeight:28};
 wb.recalculate();
 console.log((await wb.inspect({kind:'region',sheetId:'文献与方法',range:'A5:C7',maxChars:1200,tableMaxRows:3,tableMaxCols:3})).ndjson);
 for(const [sn,rg,tag] of [['文献与方法','A5:F8','methods'],['复现与资源','A5:D8','resources'],['使用与阅读路线','A2:B8','guide'],['复现与资源','E5:H8','links']]){
  const image=await wb.render({sheetName:sn,range:rg,scale:1.25,format:'png'});await fs.writeFile(path.join(previews,`${prefix}_${tag}.png`),new Uint8Array(await image.arrayBuffer()));
 }
 const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(out,file+'.xlsx'));console.log('saved',file,rows.length);
}
