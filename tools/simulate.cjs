const fs=require('node:fs');const {createEngine}=require('../src/engine.js');const data=JSON.parse(fs.readFileSync(__dirname+'/../data/cards.json'));const E=createEngine(data);
const perCount=Number(process.argv[2]||40), counts=[2,3,4,5,6];const result={version:data.version,games:0,collapse:0,byPlayers:[],byStyle:{},winningPaths:{},cardPlays:{},notes:['Deterministic heuristic bots, not human playtesting.','Style and seat are rotated. All players can use all three scoring lanes.','Win shares split tied wins; collective losses have no winner.']};
for(const n of counts){const row={players:n,games:perCount,collapse:0,rounds:0,meanWinnerScore:0,completed:0};
 for(let k=0;k<perCount;k++){const styles=Array.from({length:n},(_,i)=>['restoration','media','exploitation'][(i+k)%3]);const s=E.newGame({players:n,seed:104729+k*31+n*1009,styles});let guard=0;
  for(const p of s.players){result.byStyle[p.style]??={entries:0,wins:0,score:0};result.byStyle[p.style].entries++;}
  while(s.phase==='active'&&guard++<1000){const a=E.chooseAI(s);if(a){E.applyAction(s,a);if(a.kind==='card')result.cardPlays[a.id]=(result.cardPlays[a.id]||0)+1;}else E.endTurn(s);E.assertState(s);}
  if(guard>=1000)throw Error('Simulation did not terminate');result.games++;row.rounds+=s.round;
  if(s.reason==='collapse'){row.collapse++;result.collapse++;}else{row.completed++;row.meanWinnerScore+=E.score(s.players[s.winnerIds[0]]).total;for(const pid of s.winnerIds){const p=s.players[pid];result.byStyle[p.style].wins+=1/s.winnerIds.length;const path=E.score(p).path;result.winningPaths[path]=(result.winningPaths[path]||0)+1/s.winnerIds.length;}}
  for(const p of s.players)result.byStyle[p.style].score+=E.score(p).total;
 }
 row.meanRounds=+(row.rounds/perCount).toFixed(2);row.meanWinnerScore=row.completed?+(row.meanWinnerScore/row.completed).toFixed(2):0;delete row.rounds;result.byPlayers.push(row);console.log(`${n} players: ${perCount} games, ${row.collapse} collapses, mean winner ${row.meanWinnerScore}`);
}
for(const [style,row] of Object.entries(result.byStyle)){row.meanScore=+(row.score/row.entries).toFixed(2);row.winRate=+(row.wins/row.entries).toFixed(4);delete row.score;}
fs.writeFileSync(__dirname+'/../docs/balance-results.json',JSON.stringify(result,null,2));console.log(JSON.stringify({games:result.games,collapse:result.collapse,styles:result.byStyle,winningPaths:result.winningPaths},null,2));
