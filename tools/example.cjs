const fs=require('node:fs');const {createEngine}=require('../src/engine.js');const data=JSON.parse(fs.readFileSync(__dirname+'/../data/cards.json'));const E=createEngine(data);
const s=E.newGame({players:2,seed:431638,names:['The Repair Desk','The Nightly Bulletin'],styles:['restoration','media']});
const turns=[],rounds=[];
while(s.phase==='active'){
 const p=s.players[s.current],r=s.round,row={round:r,player:p.name,actions:[]};
 while(s.actions>0){const a=E.chooseAI(s);if(!a)break;const c=a.kind==='card'?E.byId[a.id]:E.BASICS[a.id];let t=c.target==='rival'?s.players[a.target]?.name:s.cases.find(x=>x.id===a.target)?.name;row.actions.push(c.name+(t?' -> '+t:''));E.applyAction(s,a);}
 row.influence=p.influence;row.credibility=p.credibility;row.prestige=E.score(p).total;turns.push(row);
 const last=s.current===s.players.length-1;let panic=s.panic;if(last){const exposed=s.cases.filter(c=>c.kind==='real'&&c.containedRound<s.round);panic=Math.min(18,panic+Math.min(3,exposed.length));if(!E.realCases(s).length)panic=Math.max(0,panic-2);}
 E.endTurn(s);if(last)rounds.push({round:r,stability:s.stability,panic});E.assertState(s);
}
const result={seed:431638,turns,rounds,reason:s.reason,players:s.players.map(p=>({name:p.name,score:E.score(p)})),winners:s.winnerIds.map(i=>s.players[i].name)};
fs.writeFileSync(__dirname+'/../docs/example-match.json',JSON.stringify(result,null,2));
const lines=['Seed 431638. Standard two-player opening. The Repair Desk favors Restoration; The Nightly Bulletin favors Narrative. Both can use any scoring path.','', '| Round | Institution | Actions in order | End-turn Prestige |','| --- | --- | --- | --- |',...turns.map(t=>`| ${t.round} | ${t.player} | ${t.actions.join('; ')} | ${t.prestige} |`),'','| Round end | Stability | Panic |','| --- | --- | --- |',...rounds.map(r=>`| ${r.round} | ${r.stability} | ${r.panic} |`),'',`Result: **${result.winners.join(' and ')} wins.** `+result.players.map(p=>`${p.name}: ${p.score.total} Prestige (${p.score.path}).`).join(' '),''];
fs.writeFileSync(__dirname+'/../docs/EXAMPLE_GAME.md',lines.join('\n'));console.log(`Example: ${turns.length} turns, ${rounds.length} rounds, ${result.winners.join(', ')}`);
