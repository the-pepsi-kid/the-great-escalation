import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const root=path.resolve(process.argv[2]);
const outputDir=path.resolve(root,'../outputs/great-escalation');
const qaDir=path.resolve(root,'../tmp/qa');
const data=JSON.parse(await fs.readFile(path.join(root,'data/cards.json'),'utf8'));
await fs.mkdir(outputDir,{recursive:true});await fs.mkdir(qaDir,{recursive:true});
const wb=Workbook.create(),overview=wb.worksheets.add('Overview'),catalog=wb.worksheets.add('Catalog');
overview.showGridLines=false;catalog.showGridLines=false;overview.tabColor='#943d34';
const headers=['ID','Card','Category','Type','Influence cost','Timing','Target','Restriction','Full rules','Counterplay','Flavor text','Illustration status','Art brief','Effects (JSON)','Illustration asset','Version','Balance role','Revision','Printed short rules'];
const rows=data.cards.map(c=>[c.id,c.name,c.category,c.type,c.cost,c.timing,c.target,c.restriction,c.rules,c.counterplay,c.flavor,c.illustration.status,c.illustration.brief,JSON.stringify(c.effects),c.illustration.path,c.balance.version,c.balance.role,c.balance.revision,c.rules_short]);
catalog.getRange('A1:S111').values=[headers,...rows];
catalog.getRange('A1:S111').format.font={name:'Arial',size:10,color:'#252824'};
catalog.getRange('A1:S111').format.verticalAlignment='top';
catalog.getRange('A1:S1').format={fill:'#252824',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:32,wrapText:true,verticalAlignment:'center',horizontalAlignment:'center'};
const widths=[16,34,34,12,12,32,13,52,87,87,64,33,85,95,28,13,18,12,87];
for(let i=0;i<widths.length;i++){const col=String.fromCharCode(65+i);catalog.getRange(`${col}1:${col}111`).format.columnWidth=widths[i];}
catalog.getRange('A2:S111').format.rowHeight=106;
catalog.getRange('B2:D111').format.wrapText=true;
catalog.getRange('F2:S111').format.wrapText=true;
catalog.getRange('E2:E111').format.numberFormat='0';catalog.getRange('R2:R111').format.numberFormat='0';
catalog.getRange('E2:E111').format.horizontalAlignment='right';catalog.getRange('R2:R111').format.horizontalAlignment='right';
catalog.getRange('N2:N111').format.font={name:'Arial',size:9,color:'#6c6b60'};
catalog.getRange('A2:A111').format.font={name:'Arial',size:10,bold:true,color:'#943d34'};
catalog.freezePanes.freezeRows(1);catalog.freezePanes.freezeColumns(2);
catalog.tables.add('A1:S111',true,'CardCatalog');
catalog.getRange('L2:L111').conditionalFormats.add('containsText',{text:'pending',format:{fill:'#f5e7c7',font:{color:'#795d27'}}});

overview.getRange('A2').values=[['The Great Escalation']];overview.getRange('A3').values=[['Complete 110-card catalog. Playable alpha 0.1.0.']];
overview.getRange('A7:D7').values=[['Category','Cards','Illustrated','Pending art']];
for(let i=0;i<data.categories.length;i++){
 const r=i+8;overview.getRange(`A${r}`).values=[[data.categories[i].name]];
 overview.getRange(`B${r}`).formulas=[[`=COUNTIFS(Catalog!$C$2:$C$111,A${r})`]];
 overview.getRange(`C${r}`).formulas=[[`=B${r}-D${r}`]];
 overview.getRange(`D${r}`).formulas=[[`=COUNTIFS(Catalog!$C$2:$C$111,A${r},Catalog!$L$2:$L$111,"pending")`]];
}
overview.getRange('A15').values=[['Total']];overview.getRange('B15:D15').formulas=[['=SUM(B8:B13)','=SUM(C8:C13)','=SUM(D8:D13)']];
overview.getRange('A18:B18').values=[['Card type','Cards']];
for(let i=0;i<3;i++){const r=i+19;overview.getRange(`A${r}`).values=[[['Action','Support','Incident'][i]]];overview.getRange(`B${r}`).formulas=[[`=COUNTIFS(Catalog!$D$2:$D$111,A${r})`]];}
overview.getRange('A24:B27').values=[['Runtime source','cards.json'],['Rules implementation','src/engine.js'],['Art production','All 110 cards illustrated. Six approved references guided the deck.'],['Workbook use','Review and filter the full catalog; release outputs read cards.json.']];
overview.getRange('A2:F27').format.font={name:'Arial',size:10,color:'#252824'};
overview.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#943d34'};
overview.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#6c6b60'};
overview.getRange('A1:A27').format.columnWidth=43;
overview.getRange('B1:D27').format.columnWidth=16;
overview.getRange('E1:F27').format.columnWidth=16;
overview.getRange('A7:D15').format.rowHeight=27;overview.getRange('A18:B21').format.rowHeight=25;
for(const range of ['A7:D7','A18:B18'])overview.getRange(range).format={fill:'#252824',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center'};
overview.getRange('A15:D15').format.font={name:'Arial',size:10,bold:true,color:'#252824'};
overview.getRange('A15:D15').format.borders={top:{style:'thin',color:'#943d34'}};
overview.getRange('B8:D15').format.numberFormat='0';overview.getRange('B19:B21').format.numberFormat='0';
overview.getRange('B8:D15').format.horizontalAlignment='right';overview.getRange('B19:B21').format.horizontalAlignment='right';
overview.getRange('A24:A27').format.font={name:'Arial',size:10,bold:true,color:'#252824'};
overview.getRange('B24:B27').format.font={name:'Arial',size:10,color:'#6c6b60'};
overview.getRange('A24:D27').format.rowHeight=24;

wb.recalculate();
const expected=overview.getRange('B15:D15').values[0];if(expected[0]!==110||expected[1]!==110||expected[2]!==0)throw Error('Catalog totals failed '+JSON.stringify(expected));
catalog.getRange('L2').values=[['pending']];wb.recalculate();
const changed=overview.getRange('C15:D15').values[0];if(changed[0]!==109||changed[1]!==1)throw Error('Artwork status formulas did not update.');
catalog.getRange('L2').values=[['generated reference illustration']];wb.recalculate();
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'formula error scan'});
const check=await wb.inspect({kind:'table',range:'Overview!A7:D15',include:'values,formulas',tableMaxRows:9,tableMaxCols:4,maxChars:1800});
await fs.writeFile(path.join(qaDir,'workbook-inspect.json'),JSON.stringify({errors:errors.ndjson,summary:check.ndjson,totals:expected,inputChangeTest:changed},null,2));
for(const [sheetName,range,file] of [['Overview','A1:F22','workbook-overview.png'],['Catalog','A1:F5','workbook-catalog.png']]){
 const preview=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(path.join(qaDir,file),new Uint8Array(await preview.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(outputDir,'card_catalog.xlsx'));
await fs.copyFile(path.join(outputDir,'card_catalog.xlsx'),path.join(root,'data/card_catalog.xlsx'));
console.log(JSON.stringify({rows:110,totals:expected,recalculationTest:changed,errorScan:errors.ndjson}));
