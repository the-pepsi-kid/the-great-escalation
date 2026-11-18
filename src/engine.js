/* The Great Escalation 0.1.0. Pure, deterministic rules shared by browser and tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TGE = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = '0.1.0';
  const SUPPORTED_OPS = ['influence','credibility','panic','stability','draw','reach','leverage','liability','shield','boost','report','repair','verify','rumor','escalate','contain','containAll','audit','auditAll','steal','transfer','clearLiability','withdraw','debunkAll','verifyAll','allIncome','clearBoosts','action','reclaim','install','incident'];
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const copy = obj => JSON.parse(JSON.stringify(obj));

  function createEngine(dataset) {
    const cards = dataset.cards || dataset;
    const byId = Object.fromEntries(cards.map(c => [c.id, c]));
    function rand(s) { s.rng = (Math.imul(s.rng, 1664525) + 1013904223) >>> 0; return s.rng / 4294967296; }
    function shuffle(s, a) { for (let i=a.length-1;i>0;i--) { const j=Math.floor(rand(s)*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
    function log(s, text) { s.log.push({round:s.round,turn:s.turn,text}); if(s.log.length>160) s.log.shift(); }
    function change(s, key, n) { const before=s[key];s[key]=clamp(before+n,0,key==='panic'?18:24);return s[key]-before; }
    function stat(p,key,n) { const before=p[key]; const max={influence:15,credibility:6,shield:3,boost:3}[key]??999; p[key]=clamp(before+n,0,max);return p[key]-before; }
    function draw(s,p,n) {
      for(let i=0;i<n;i++) {
        if(!s.deck.length && s.discard.length) { s.deck=shuffle(s,s.discard.splice(0)); log(s,'The news cycle recycles the action discard pile.'); }
        if(s.deck.length) p.hand.push(s.deck.pop());
      }
    }
    function newGame(options={}) {
      const count=clamp(Number(options.players)||3,2,6);
      const s={version:VERSION,rng:(Number(options.seed)||8112026)>>>0,round:0,turn:0,current:0,phase:'active',actions:0,panic:2,stability:20,
        players:[],deck:[],discard:[],incidentDeck:[],incidentDiscard:[],cases:[],nextCase:1,log:[],winnerIds:[],reason:'',totalRounds:8};
      const names=['You','Department of Calm','The Attention Economy','Premium Response LLC','The Context Bureau','Tomorrow Incorporated'];
      const styles=['balanced','restoration','media','exploitation','balanced','media'];
      for(let i=0;i<count;i++) s.players.push({id:i,name:options.names?.[i]||names[i],style:options.styles?.[i]||styles[i],human:options.mode==='hotseat'||i===0,
        influence:5,credibility:3,accountability:0,reach:0,leverage:0,liability:0,blame:0,shield:0,boost:0,hand:[],supports:[],used:[],resolved:0});
      s.deck=shuffle(s,cards.filter(c=>c.type!=='Incident').map(c=>c.id));
      s.incidentDeck=shuffle(s,cards.filter(c=>c.type==='Incident').map(c=>c.id));
      const prebuilt={restoration:['TGE-H02','TGE-H05','TGE-H08','TGE-H09','TGE-H14'],media:['TGE-M01','TGE-M03','TGE-M13','TGE-M19','TGE-M25'],exploitation:['TGE-P14','TGE-P15','TGE-P16','TGE-W03','TGE-P07']};
      if(prebuilt[options.starter])for(const id of prebuilt[options.starter]){s.deck.splice(s.deck.indexOf(id),1);s.players[0].hand.push(id);}
      if(options.starter!==false) {
        // Identical access to one useful engine card, not hard classes or exclusive victory paths.
        const starters=['TGE-H02','TGE-M03','TGE-P16'];
        for(let i=0;i<count;i++) {const id=starters[i%3]; if(s.players[i].hand.length<5&&s.deck.includes(id)){s.deck.splice(s.deck.indexOf(id),1);s.players[i].hand.push(id);}}
      }
      for(const p of s.players) draw(s,p,5-p.hand.length);
      startRound(s); return s;
    }
    function realCases(s) { return s.cases.filter(c=>c.kind==='real'); }
    function reveal(s) {
      if(!s.incidentDeck.length && s.incidentDiscard.length) s.incidentDeck=shuffle(s,s.incidentDiscard.splice(0));
      if(!s.incidentDeck.length)return;
      const id=s.incidentDeck.pop(), card=byId[id], f=card.effects[0];
      if(realCases(s).length>=s.players.length+2){
        s.incidentDiscard.push(id);const c=realCases(s)[0];c.severity=clamp(c.severity+1,0,8);change(s,'panic',1);
        log(s,`${card.name} overwhelms the queue: oldest real incident gains 1 severity; Panic +1.`);return;
      }
      s.cases.push({id:'case-'+s.nextCase++,cardId:id,name:card.name,kind:'real',severity:f.n,verified:false,containedRound:0,tags:f.tags,cause:f.cause,sponsor:null,resolutionBonus:f.resolution_bonus||[]});
      change(s,'panic',f.panic);log(s,`${card.name}: severity ${f.n}. Panic +${f.panic}.`);
    }
    function startRound(s) {
      s.round++;log(s,`ROUND ${s.round}: the network is still down.`);
      for(let i=0;i<Math.ceil(s.players.length/2);i++)reveal(s);
      s.current=0;startTurn(s);
    }
    function startTurn(s) {
      const p=s.players[s.current];s.turn++;s.actions=2;p.used=[];
      const income=3+(p.credibility>=4?1:0)-(s.panic>=12?1:0);
      stat(p,'influence',income);draw(s,p,1);log(s,`${p.name}: +${income} Influence, draw 1, two actions.`);
    }
    function score(p) {
      const lanes={restoration:2*p.accountability+p.credibility,media:Math.floor(5*p.reach/2)+p.credibility,exploitation:Math.max(0,2*p.leverage+Math.floor(p.influence/3)-2*p.blame-p.liability)};
      const best=Math.max(...Object.values(lanes));return {total:best,lanes,path:Object.keys(lanes).filter(k=>lanes[k]===best).join(' / ')};
    }
    function finish(s,reason) {
      s.phase='finished';s.reason=reason;s.actions=0;
      if(reason==='collapse'){s.winnerIds=[];log(s,'COLLECTIVE LOSS: Stability reached zero at round end. Nobody monetizes a dead game.');return;}
      let winners=s.players.filter(p=>score(p).total===Math.max(...s.players.map(p=>score(p).total)));
      const cred=Math.max(...winners.map(p=>p.credibility));winners=winners.filter(p=>p.credibility===cred);
      const blame=Math.min(...winners.map(p=>p.blame+p.liability));winners=winners.filter(p=>p.blame+p.liability===blame);
      s.winnerIds=winners.map(p=>p.id);log(s,`${winners.map(p=>p.name).join(' and ')} wins with ${score(winners[0]).total} Prestige.`);
    }
    function endTurn(s) {
      if(s.phase!=='active')return {ok:false,error:'The game is finished.'};
      const p=s.players[s.current];
      while(p.hand.length>8){const id=p.hand.pop();s.discard.push(id);log(s,`${p.name} discards newest excess card: ${byId[id].name}.`);}
      if(s.current<s.players.length-1){s.current++;startTurn(s);return {ok:true};}
      const exposed=realCases(s).filter(c=>c.containedRound<s.round);
      const raw=exposed.reduce((a,c)=>a+c.severity,0);
      const damage=Math.ceil(raw/4)+(s.panic>=12?1:0);
      change(s,'stability',-damage);change(s,'panic',Math.min(3,exposed.length));
      log(s,`Round end: ${raw} uncontained severity causes ${damage} Stability damage${s.panic>=12?' (high Panic can add 1)':''}.`);
      if(!realCases(s).length){change(s,'stability',2);change(s,'panic',-2);log(s,'No real incidents: Stability +2, Panic -2.');}
      if(s.stability<=0)finish(s,'collapse');else if(s.round>=s.totalRounds)finish(s,'rounds');else startRound(s);
      return {ok:true};
    }
    const BASICS={
      fund:{id:'fund',name:'Find Funding',cost:0,target:'none',effects:[{op:'influence',n:2}]},
      repair:{id:'repair',name:'Repair',cost:1,target:'real',effects:[{op:'repair',n:2}]},
      verify:{id:'verify',name:'Verify',cost:1,target:'unknown',effects:[{op:'verify',n:1}]},
      report:{id:'report',name:'Report',cost:1,target:'real',effects:[{op:'report',n:1},{op:'panic',n:1}]},
      monetize:{id:'monetize',name:'Monetize',cost:1,target:'real',condition:'panic',effects:[{op:'leverage',n:2},{op:'liability',n:1},{op:'panic',n:1}]},
      reassure:{id:'reassure',name:'Reassure',cost:0,target:'none',effects:[{op:'panic',n:-2},{op:'credibility',n:1}]},
    };
    function issueCount(s,p){return p.liability+s.cases.filter(c=>c.kind==='rumor'&&c.sponsor===p.id).length+(p.boost?1:0);}
    function targetOptions(s,card,player=s.players[s.current]) {
      switch(card.target){
        case 'real':return realCases(s).filter(c=>(card.condition!=='verified'||c.verified)&&(card.condition!=='network'||c.tags.includes('network'))).map(c=>({id:c.id,label:c.name,kind:'case'}));
        case 'unknown':return s.cases.filter(c=>!c.verified).map(c=>({id:c.id,label:c.name,kind:'case'}));
        case 'rumor':return s.cases.filter(c=>c.kind==='rumor'&&(card.condition!=='ownRumor'||c.sponsor===player.id)).map(c=>({id:c.id,label:c.name,kind:'case'}));
        case 'rival':return s.players.filter(p=>p.id!==player.id&&(!card.effects.some(e=>e.op==='audit')||issueCount(s,p)>0)).map(p=>({id:p.id,label:p.name,kind:'player'}));
        default:return [{id:null,label:'No target',kind:'none'}];
      }
    }
    function legality(s,action) {
      if(s.phase!=='active')return 'The game is finished.';
      if(s.actions<=0)return 'No actions remaining. End your turn.';
      const p=s.players[s.current], c=action.kind==='card'?byId[action.id]:BASICS[action.id];
      if(!c)return 'Unknown action.';
      if(action.kind==='card'&&!p.hand.includes(c.id))return 'That card is not in the current hand.';
      if(c.type==='Incident')return 'Incidents can only be revealed by the incident deck.';
      if(p.influence<c.cost)return `Needs ${c.cost} Influence.`;
      if(c.condition==='emergency'&&s.stability>8)return 'Requires Stability 8 or lower.';
      if(c.condition==='fundEmergency'&&s.stability>10)return 'Requires Stability 10 or lower.';
      if(c.condition==='panic'&&s.panic<6)return 'Requires Panic 6 or higher.';
      if(c.condition==='liability'&&p.liability<1)return 'Requires your own Liability.';
      if(c.condition==='counterDiscard'&&!s.discard.some(id=>byId[id].category_code==='H'))return 'Requires a discarded IT card.';
      if(!targetOptions(s,c,p).some(t=>t.id===action.target))return 'Select an eligible target.';
      return '';
    }
    function resolveCase(s,c) {
      s.cases.splice(s.cases.indexOf(c),1);
      (c.kind==='real'?s.incidentDiscard:s.discard).push(c.cardId);
    }
    function verify(s,p,c,rewards=true) {
      if(!c||c.verified)return false;
      c.verified=true;
      if(rewards){stat(p,'accountability',1);stat(p,'credibility',1);}
      if(c.kind==='rumor'){
        const sponsor=s.players[c.sponsor];stat(sponsor,'reach',-1);stat(sponsor,'blame',1);change(s,'panic',-2);
        log(s,`${p.name} debunks ${c.name}. ${sponsor.name}: -1 Reach, +1 Blame. The rumor caused no infrastructure damage.`);resolveCase(s,c);
      }else {change(s,'panic',-1);log(s,`${p.name} verifies ${c.name}. Cause: ${c.cause}`);}
      if(rewards&&p.supports.some(x=>x.asset==='runbook')&&!p.used.includes('runbook')){p.used.push('runbook');draw(s,p,1);log(s,'Documented Runbook: draw 1.');}
      return true;
    }
    function repair(s,p,c,n){
      if(!c||c.kind!=='real'||!s.cases.includes(c))return;
      for(const asset of p.supports){if(p.used.includes(asset.asset))continue;
        if(asset.asset==='engineer'){n++;p.used.push('engineer');}
        if(asset.asset==='field'&&c.tags.includes('physical')){n+=2;p.used.push('field');}}
      const work=Math.min(n,c.severity);c.severity-=work;change(s,'stability',1);
      if(c.verified)stat(p,'accountability',1);
      log(s,`${p.name} repairs ${work} severity on ${c.name}; Stability +1${c.verified?', Accountability +1':''}.`);
      if(c.severity===0){stat(p,'accountability',1);stat(p,'credibility',1);p.resolved++;change(s,'stability',1);log(s,`${c.name} resolved: +1 Accountability, +1 Credibility, +1 more Stability.`);for(const bonus of c.resolutionBonus||[]){if(bonus.op==='panic'||bonus.op==='stability')change(s,bonus.op,bonus.n);else if(bonus.op==='draw')draw(s,p,bonus.n);else stat(p,bonus.op,bonus.n);log(s,`${c.name} resolution bonus: ${bonus.op} ${bonus.n>0?'+':''}${bonus.n}.`);}resolveCase(s,c);}
    }
    function block(s,p,name) {if(p.shield){p.shield--;log(s,`${p.name} spends an Audit Shield to block ${name}.`);return true;}return false;}
    function audit(s,p,rival,n) {
      if(!rival||issueCount(s,rival)===0)return;
      if(block(s,rival,'the audit'))return;
      let productive=false;
      for(let i=0;i<n;i++){
        const rumor=s.cases.find(c=>c.kind==='rumor'&&c.sponsor===rival.id);
        if(rumor){verify(s,p,rumor,false);productive=true;continue;}
        if(rival.liability){rival.liability--;rival.blame++;stat(rival,'leverage',-1);stat(rival,'credibility',-1);productive=true;log(s,`${rival.name}: Liability becomes Blame; -1 Leverage, -1 Credibility.`);continue;}
        if(rival.boost){rival.boost=0;productive=true;log(s,`${rival.name}'s stored report boost is audited away.`);continue;}
        break;
      }
      if(productive){stat(p,'accountability',1);stat(p,'credibility',1);}
    }
    function applyEffect(s,p,c,fx,target,sourceId) {
      const n=fx.n;
      switch(fx.op){
        case 'influence':case 'credibility':case 'reach':case 'leverage':case 'liability':case 'shield':case 'boost':stat(p,fx.op,n);break;
        case 'panic':case 'stability':change(s,fx.op,n);break;
        case 'draw':draw(s,p,n);break;
        case 'report':{const gain=Math.min(5,n+p.boost);p.boost=0;stat(p,'reach',gain);log(s,`${p.name} reports ${target.name}: +${gain} Reach.`);break;}
        case 'repair':repair(s,p,target,n);break;
        case 'verify':verify(s,p,target);break;
        case 'rumor':s.cases.push({id:'case-'+s.nextCase++,cardId:sourceId,name:c.name,kind:'rumor',severity:0,verified:false,containedRound:0,tags:[],cause:'Unsupported claim; no corresponding operational incident.',sponsor:p.id});stat(p,'reach',n);log(s,`${p.name} sponsors ${c.name}. This is an unsupported rumor, not a real outage.`);break;
        case 'escalate':target.severity=clamp(target.severity+n,0,8);break;
        case 'contain':target.containedRound=s.round;log(s,`${target.name} contained through round ${s.round}.`);break;
        case 'containAll':for(const x of realCases(s))x.containedRound=s.round;break;
        case 'audit':audit(s,p,target,n);break;
        case 'auditAll':for(const rival of s.players.filter(x=>x.id!==p.id))audit(s,p,rival,1);break;
        case 'steal':if(!block(s,target,'the transfer')){const amount=Math.min(n,target.influence,15-p.influence);target.influence-=amount;p.influence+=amount;}break;
        case 'transfer':if(!block(s,target,'blame transfer')){const amount=Math.min(n,p.liability);p.liability-=amount;target.liability+=amount;}break;
        case 'clearLiability':stat(p,'liability',-n);break;
        case 'withdraw':stat(p,'reach',-1);resolveCase(s,target);break;
        case 'debunkAll':{let i=0;for(const x of s.cases.filter(x=>x.kind==='rumor'))verify(s,p,x,i++<3);break;}
        case 'verifyAll':{let i=0;for(const x of s.cases.filter(x=>x.kind==='real'&&!x.verified))verify(s,p,x,i++<2);break;}
        case 'allIncome':for(const rival of s.players.filter(x=>x.id!==p.id))stat(rival,'influence',n);break;
        case 'clearBoosts':for(const rival of s.players)rival.boost=0;break;
        case 'action':s.actions+=n;break;
        case 'reclaim':{const idx=s.discard.findLastIndex(id=>byId[id].category_code==='H');if(idx>=0)p.hand.push(s.discard.splice(idx,1)[0]);break;}
        case 'install':if(p.supports.length>=2){const old=p.supports.shift();s.discard.push(old.cardId);log(s,`${byId[old.cardId].name} retires to make room.`);}p.supports.push({cardId:sourceId,asset:fx.asset});break;
        default:throw new Error('Unimplemented effect: '+fx.op);
      }
    }
    function applyAction(s,action) {
      const error=legality(s,action);if(error)return {ok:false,error};
      const p=s.players[s.current],c=action.kind==='card'?byId[action.id]:BASICS[action.id];
      const target=c.target==='rival'?s.players[action.target]:s.cases.find(x=>x.id===action.target);
      stat(p,'influence',-c.cost);s.actions--;if(action.kind==='card')p.hand.splice(p.hand.indexOf(c.id),1);
      log(s,`${p.name} plays ${c.name}${target?' → '+target.name:''} (${c.cost} Influence).`);
      for(const fx of c.effects)applyEffect(s,p,c,fx,target,c.id);
      if(action.kind==='card'&&!c.effects.some(x=>['rumor','install'].includes(x.op)))s.discard.push(c.id);
      return {ok:true};
    }
    function legalActions(s) {
      if(s.phase!=='active'||s.actions<=0)return [];
      const p=s.players[s.current],actions=[];
      for(const [kind,c] of [...Object.values(BASICS).map(c=>['basic',c]),...p.hand.map(id=>['card',byId[id]])])
        for(const t of targetOptions(s,c,p)){const a={kind,id:c.id,target:t.id};if(!legality(s,a))actions.push(a);}
      return actions;
    }
    function danger(s){const raw=realCases(s).filter(c=>c.containedRound<s.round).reduce((a,c)=>a+c.severity,0);return Math.ceil(raw/4)+(s.panic>=12?1:0);}
    function utility(s,pid,style) {
      const p=s.players[pid],sc=score(p).lanes;
      const lane=style==='restoration'?sc.restoration:style==='media'?sc.media:style==='exploitation'?sc.exploitation:Math.max(...Object.values(sc));
      const second=style==='restoration'?sc.media:sc.restoration;
      const risk= Math.max(0,12-s.stability)*0.40+Math.max(0,6-s.stability)*1.9;
      return lane+0.13*second+Math.min(9,p.influence)*0.22+p.hand.length*0.22+p.shield*0.50+p.boost*0.65+p.supports.length*1.4+
        s.stability*0.08-danger(s)*(0.45+risk)-(s.panic>11?(s.panic-11)*0.18:0)+
        s.cases.filter(c=>c.kind==='real'&&c.verified).length*0.10;
    }
    function chooseAI(s,styleOverride) {
      const legal=legalActions(s);if(!legal.length)return null;
      const p=s.players[s.current],style=styleOverride||p.style;let best=-Infinity,bestAction=legal[0];
      for(const a of legal){const test=copy(s);test.log=[];applyAction(test,a);let u=utility(test,p.id,style);
        // Value work already contributed toward future resolution and spendable support engines.
        const before=realCases(s).reduce((v,x)=>v+x.severity,0),after=realCases(test).reduce((v,x)=>v+x.severity,0);
        u+=(before-after)*0.20;
        if(a.kind==='card'&&byId[a.id].effects.some(x=>x.op==='install'))u+=Math.max(0,6-s.round)*0.50;
        const rival=a.target!==null&&Number.isInteger(a.target)?a.target:null;
        if(rival!==null)u+=(score(s.players[rival]).total-score(test.players[rival]).total)*0.22;
        u+=((a.id.charCodeAt(a.id.length-1)+s.rng%17)%7)*0.001;
        if(u>best){best=u;bestAction=a;}
      }return bestAction;
    }
    function assertState(s) {
      if(s.panic<0||s.panic>18||s.stability<0||s.stability>24)throw Error('Shared resource out of bounds');
      const actionIds=[...s.deck,...s.discard,...s.players.flatMap(p=>[...p.hand,...p.supports.map(x=>x.cardId)]),...s.cases.filter(c=>c.kind==='rumor').map(c=>c.cardId)];
      const incidentIds=[...s.incidentDeck,...s.incidentDiscard,...s.cases.filter(c=>c.kind==='real').map(c=>c.cardId)];
      if(actionIds.length!==90||new Set(actionIds).size!==90)throw Error('Action card conservation failed');
      if(incidentIds.length!==20||new Set(incidentIds).size!==20)throw Error('Incident conservation failed');
      if(actionIds.some(id=>!byId[id]||byId[id].type==='Incident')||incidentIds.some(id=>!byId[id]||byId[id].type!=='Incident'))throw Error('Deck type mismatch');
      for(const p of s.players){for(const key of ['influence','credibility','accountability','reach','leverage','liability','blame','shield','boost'])if(!Number.isInteger(p[key])||p[key]<0)throw Error('Invalid player resource '+key);if(p.influence>15||p.credibility>6||p.shield>3||p.boost>3)throw Error('Player resource exceeds cap');if(p.supports.length>2)throw Error('Support capacity');}
      for(const c of s.cases)if(c.kind==='real'&&(c.severity<=0||c.severity>8))throw Error('Invalid severity');
      return true;
    }
    return {newGame,applyAction,endTurn,legalActions,legality,targetOptions,chooseAI,score,danger,assertState,byId,BASICS,realCases,issueCount};
  }
  return {createEngine,SUPPORTED_OPS,VERSION,copy};
});
