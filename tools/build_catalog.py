"""Authoritative card source. Generates JSON and card copy from implemented operations."""
import json, pathlib
from art_scenes import SCENES

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION = '0.1.0'
CATEGORIES = [
    ('M','Breaking News & Media',25,'#237c91'),
    ('D','Infrastructure Disasters',20,'#c34c38'),
    ('P','Political & Corporate Panic',20,'#926224'),
    ('C','Conspiracies & Prophecies',15,'#80649b'),
    ('H','IT Heroes & Countermeasures',15,'#34785f'),
    ('W','Emergency Events & Wildcards',15,'#ac5270'),
]
cards=[]
def e(op, n=1, **kw): return dict(op=op,n=n,**kw)
def short_rule(x):
    op=x['op']; n=x['n']
    if op=='repair':return f'Repair {n} severity. Use normal work and resolution rewards.'
    if op=='verify':return 'Verify one unknown case. Use normal evidence and debunk rewards.'
    if op=='audit':return f'Audit up to {n} issues at one rival. One shield blocks the audit. Use normal audit rewards.'
    if op=='rumor':return f'Sponsor a rumor and gain {n} Reach. It is vulnerable to verification.'
    if op=='report':return f'Report a real incident for {n} Reach plus your boost (maximum 5). Consume the boost.'
    if op=='debunkAll':return 'Debunk every rumor. Gain verification rewards for the first 3 only; all sponsors take debunk penalties.'
    if op=='verifyAll':return 'Verify all unknown real incidents. Gain verification rewards for the first 2 only; all lower Panic by 1.'
    return rule(x)
def rule(x):
    n=x['n']; op=x['op']
    return {
      'influence':f'Gain {n} Influence.', 'credibility':f'{"Gain" if n>0 else "Lose"} {abs(n)} Credibility.',
      'panic':f'{"Raise" if n>0 else "Lower"} Panic by {abs(n)}.',
      'stability':f'Restore {n} Stability.', 'draw':f'Draw {n} card'+('s.' if n!=1 else '.'),
      'reach':f'Gain {n} Reach.', 'leverage':f'Gain {n} Leverage.',
      'liability':f'Take {n} Liability.', 'shield':f'Gain {n} Audit Shield'+('s.' if n!=1 else '.'),
      'boost':f'Your next report gains +{n} Reach (boosts cap at 3).',
      'report':f'Report the selected real incident for {n} Reach, plus your stored boost (max 5 Reach).',
      'repair':f'Repair {n} severity on the selected real incident and restore 1 Stability. Verified work earns 1 Accountability; resolving it earns +1 Accountability, +1 Credibility, and +1 more Stability.',
      'verify':'Verify the selected unknown case. Earn 1 Accountability and 1 Credibility. A real incident lowers Panic by 1; a rumor is removed, lowers it by 2, and its sponsor loses 1 Reach and takes 1 Blame.',
      'rumor':f'Create an unsupported rumor and gain {n} Reach. Verification can debunk it.',
      'escalate':f'Add {n} severity to the selected real incident (maximum 8).',
      'contain':'Contain the selected real incident through this round: it causes no round-end damage or Panic.',
      'containAll':'Contain every real incident through this round.',
      'audit':f'Audit up to {n} issues at one rival: oldest rumor first, then Liability, then report boost. Each audited Liability becomes Blame and costs 1 Leverage and 1 Credibility. A productive audit earns 1 Accountability and 1 Credibility. One shield blocks the whole audit.',
      'auditAll':'Audit one issue at every eligible rival. Each rival may block with one shield. Gain audit rewards for each productive audit.',
      'steal':f'Transfer up to {n} Influence from a rival to you. A shield blocks the transfer.',
      'transfer':f'Transfer up to {n} of your Liability to a rival. A shield blocks the transfer. Blame cannot be transferred.',
      'clearLiability':f'Remove up to {n} of your Liability. Blame remains.',
      'withdraw':'Withdraw your selected rumor without a debunk penalty. Lose 1 Reach.',
      'debunkAll':'Verify every rumor. Earn normal verification rewards for the first 3 only; every sponsor still takes the normal debunk penalty.',
      'verifyAll':'Verify every unknown real incident. Earn normal verification rewards for the first 2 only; all verified incidents lower Panic by 1.',
      'allIncome':f'Every other player gains {n} Influence.',
      'clearBoosts':'Remove every player\'s stored report boost.',
      'action':f'Gain {n} additional action this turn.',
      'reclaim':'Return the most recently discarded IT card to your hand.',
      'install':{'engineer':'Install: once per turn, your first repair gets +1 severity repaired.', 'field':'Install: once per turn, your first repair of a physical incident gets +2 severity repaired.', 'runbook':'Install: once per turn, your first successful verification draws 1 card.'}.get(x.get('asset'),''),
    }[op]

def add(cat,name,cost,target,fx,flavor,condition=None,art=None):
    idx=sum(c['category_code']==cat for c in cards)+1
    meta=next(z for z in CATEGORIES if z[0]==cat)
    restrictions={None:'No additional restriction.', 'verified':'The selected real incident must already be verified.',
      'network':'The selected incident must have the network tag.', 'emergency':'Stability must be 8 or lower.',
      'fundEmergency':'Stability must be 10 or lower.', 'panic':'Panic must be 6 or higher.',
      'liability':'You must have at least 1 Liability.', 'ownRumor':'Select a rumor you sponsor.',
      'counterDiscard':'An IT card must be in the discard pile.'}
    counter={'real':'Contain or repair the incident before this card can use it.', 'unknown':'Verify the case first to deny this target.',
      'rumor':'Withdraw or verify the rumor first.', 'rival':'Use Audit Shields. Honest players without rumors, Liability, or boosts cannot be audited.',
      'none':'Reduce Panic, audit unsupported claims or liabilities, and manage the shared Stability clock.'}[target]
    if any(x['op']=='rumor' for x in fx): counter='Any player can use basic Verify to debunk this rumor, removing 1 sponsor Reach and adding 1 Blame.'
    if any(x['op']=='install' for x in fx):counter='Two support slots per player. Installing a third retires the oldest; matching support bonuses trigger only once each turn.'
    cid=f'TGE-{cat}{idx:02d}'
    cards.append(dict(id=cid,name=name,category=meta[1],category_code=cat,color=meta[3],
      type='Support' if any(x['op']=='install' for x in fx) else 'Action',cost=cost,timing='Your turn; costs 1 action',
      target=target,condition=condition,effects=fx,rules=' '.join(rule(x) for x in fx),rules_short=' '.join(short_rule(x) for x in fx),
      restriction=restrictions[condition],counterplay=counter,flavor=flavor,
      illustration={'path':f'art/{cid}.jpg','status':'pending','brief':art or name},
      balance={'version':VERSION,'revision':1,'status':'alpha; automated playtest only','role':{'M':'narrative','P':'opportunism','C':'narrative','H':'restoration','W':'flex'}[cat]}))

# BREAKING NEWS & MEDIA: 25
add('M','Breaking News!',1,'real',[e('report',2),e('panic',1)],'We interrupted the solution to bring you the problem.',art='A frantic television anchor presents a flaming beige computer while a tiny technician plugs in its loose cable.')
add('M','Anonymous Sources',0,'none',[e('rumor',2),e('panic',2),e('credibility',-1)],'A person familiar with a person familiar with the matter.')
add('M','The Algorithm Has Spoken',2,'none',[e('boost',2),e('reach',1),e('panic',1)],'The machine has identified your preferred flavor of dread.')
add('M','Expert Panel of Absolutely Nobody',1,'none',[e('reach',2),e('panic',2),e('credibility',-1)],'Six chairs. Seven opinions. Zero relevant qualifications.')
add('M',"Downdetector Says We're Dying",1,'real',[e('escalate',1),e('report',2),e('panic',2)],'A red dot is apparently a death certificate.')
add('M','We Interrupt This Program',1,'none',[e('draw',2),e('panic',1)],'Even the emergency has an ad break.')
add('M','Live From the Parking Lot',1,'real',[e('report',1),e('credibility',1)],'The building remains behind us. More as it develops.')
add('M','Context Is Behind a Paywall',0,'none',[e('influence',3),e('credibility',-1)],'The first three paragraphs of the apocalypse are free.')
add('M','Correction on Page 47',1,'none',[e('panic',-2),e('credibility',1),e('draw',1)],'Yesterday\'s extinction event was a printer jam.')
add('M','Leaked Slide Deck',2,'rival',[e('audit',1),e('draw',1)],'Confidential. Forwarded by everyone.')
add('M','The Thumbnail Has Flames',1,'none',[e('reach',2),e('panic',2),e('credibility',-1),e('boost',1)],'The server was not actually on fire. The engagement was.')
add('M','Breaking: Still Broken',1,'real',[e('report',2),e('draw',1)],'Our third exclusive confirmation of the same outage.',condition='verified')
add('M','Community Radio',1,'none',[e('panic',-1),e('credibility',1),e('reach',1)],'A calm voice. A working frequency. Revolutionary stuff.')
add('M','Follow the Money',1,'rival',[e('audit',1),e('influence',1)],'It led to an invoice for following the money.')
add('M','Scheduled Outrage',0,'none',[e('boost',1),e('panic',1)],'The indignation is live. The footage is from Tuesday.')
add('M','Retraction Speedrun',1,'rumor',[e('verify'),e('draw',1)],'The correction arrived before the merchandise.')
add('M','Independent Fact Check',1,'unknown',[e('verify'),e('panic',-1)],'An astonishing number of facts survived being checked.')
add('M','The Camera Found IT',2,'real',[e('repair',1),e('report',2)],'For once, the person fixing it gets the lower third.',condition='verified')
add('M','Emergency Press Conference',1,'none',[e('panic',-1),e('influence',2),e('credibility',1)],'The podium is operational. The network is not.')
add('M','Public Service Announcement',2,'none',[e('panic',-3),e('reach',1)],'Remain calm. Yes, that is the entire announcement.')
add('M','A Screenshot Is Not a Source',1,'rumor',[e('verify'),e('shield',1)],'Especially a screenshot of your own screenshot.')
add('M','The Mic Is Still On',1,'rival',[e('audit',1),e('leverage',1)],'We will now hear the internal version of that statement.')
add('M','Longform Investigation',3,'rival',[e('audit',2),e('draw',2)],'It took longer than a thread. That was the point.')
add('M','Emergency Broadcast Loop',2,'none',[e('boost',2),e('panic',1),e('draw',1)],'The warning has outlived the event.')
add('M','Responsible Headline',1,'real',[e('report',2),e('panic',-1)],'LOCAL SYSTEM FAILS. LOCAL PEOPLE REPAIR SYSTEM.',condition='verified')

# INFRASTRUCTURE DISASTERS: 20. These are the separate incident deck.
disasters=[
('Broadcast Storm',4,1,['network'],'An unmanaged switch loop is flooding the network.','Every packet has been invited to every meeting.','An octopus-like tangle of ethernet cables lashes through a beige network closet while a technician discovers two ports plugged into one another.'),
('Nationwide Ground Stop',4,2,['software'],'An expired flight-information service token blocked updates.','The planes work. The permission to know where they are does not.',None),
('Banking Outage',4,2,['network'],'A routing policy isolated the payment gateway.','Your money is safe. Its whereabouts are temporarily abstract.',None),
('The Legacy Router',3,1,['network','physical'],'An unsupported router exhausted its memory.','It has survived three mergers and no firmware updates.',None),
('Global DNS Failure',5,2,['network'],'A bad DNS change propagated to production resolvers.','Civilization cannot find civilization.',None),
('Unapproved Production Change',3,1,['software'],'A direct production edit bypassed validation.','A small change, as measured by the person who left.',None),
('Expired Certificate',2,1,['identity'],'An unrenewed TLS certificate broke service authentication.','The entire company has been defeated by a date.',None),
('Fiber-Seeking Backhoe',4,1,['network','physical'],'Excavation severed the only fiber route.','Nature\'s most accurate cable locator.',None),
('Read-Only Backup',4,1,['storage'],'The backup account could read data but never write it.','Thirty green reports. Zero recoverable files.',None),
('Region Unavailable',5,2,['cloud'],'A regional control plane failed during a migration.','The cloud is somebody else\'s very crowded war room.',None),
('Ransomware Drill Gone Live',5,2,['security'],'A simulation tool was pointed at production storage.','The exercise has exceeded all expectations.',None),
('Empty Generator Tank',4,1,['physical'],'The generator test never included checking the fuel.','The continuity plan runs on assumptions.',None),
('DHCP Hunger Games',3,1,['network'],'The address pool is exhausted by abandoned leases.','May the next available address be ever in your favor.',None),
('Identity Provider Vacation',4,1,['identity'],'A directory-sync failure locked out valid accounts.','Please sign in to report that you cannot sign in.',None),
('Flooded Equipment Closet',4,1,['physical'],'A plumbing leak reached floor-mounted equipment.','The rack has achieved liquid cooling.',None),
('Patching the Wrong Cluster',3,1,['software'],'The maintenance target list included both failover nodes.','High availability met highly enthusiastic patching.',None),
('Vendor Status: Operational',3,2,['cloud'],'The status monitor cannot reach the failed service either.','The dashboard has successfully monitored itself.',None),
('The Building Has One Uplink',3,1,['network','physical'],'A failed transceiver removed the only WAN connection.','Redundancy was value-engineered into a future meeting.',None),
('The Spreadsheet Was Production',2,1,['software'],'An undocumented workbook supplied the live inventory feed.','The business-critical platform was named final_FINAL2.xlsx.',None),
('Friday at 4:59',4,2,['software'],'An untested deployment removed a required configuration.','Deployment complete. Engineer unavailable.',None),
]
for idx,(name,sev,panic,tags,cause,flavor,brief) in enumerate(disasters,1):
    cid=f'TGE-D{idx:02d}'; cards.append(dict(id=cid,name=name,category=CATEGORIES[1][1],category_code='D',color=CATEGORIES[1][3],type='Incident',cost=0,timing='Reveal at round start; never enters a player hand',target='none',condition=None,effects=[e('incident',sev,panic=panic,tags=tags,cause=cause)],rules=f'Enter as a real, unverified incident with {sev} severity. Raise Panic by {panic}. At round end, uncontained real incidents deal combined damage equal to their remaining severity divided by 4, rounded up.',restriction='Only the incident deck reveals this card. The real-incident limit is player count + 2.',counterplay='Verify to reveal the cause and earn Accountability. Repair to remove severity. Contain to prevent round-end damage for one round.',flavor=flavor,illustration={'path':f'art/{cid}.jpg','status':'pending','brief':brief or name},balance={'version':VERSION,'revision':1,'status':'alpha; automated playtest only','role':'incident'}))

# POLITICAL & CORPORATE PANIC: 20
add('P','Executive War Room',1,'real',[e('contain'),e('panic',2),e('influence',3),e('liability',1)],'All personnel must attend. Except those currently resolving the emergency.',art='Executives in an ornate boardroom worship a giant blank emergency dashboard while an exhausted technician crawls beneath the table fixing cables.')
add('P','Emergency Executive Meeting',1,'none',[e('influence',4),e('panic',1)],'The crisis has been escalated to a larger table.')
add('P','Strategic Infrastructure Heritage',0,'real',[e('influence',3),e('escalate',1),e('liability',1)],'Obsolete is a technical term. Heritage is a budget strategy.')
add('P','The Sacred Dashboard',2,'none',[e('boost',2),e('shield',1)],'HOLY HOLY. ALL METRICS ARE GREEN. THE BUILDING IS DARK.')
add('P','Congressional Hearing',2,'rival',[e('audit',2)],'For the record, who approved the thing no one read?')
add('P','The Contractor Has Been Identified',1,'rival',[e('transfer',1),e('influence',1)],'Their contract did not include attending the blame meeting.',condition='liability')
add('P',"The Consultant's Consultant",2,'none',[e('influence',6),e('liability',1)],'We recommend commissioning a recommendation.')
add('P','Steering Committee',1,'real',[e('contain'),e('panic',-1)],'Nothing moves until we agree which direction not to move.')
add('P','Budget Reallocation',0,'rival',[e('steal',2),e('liability',1)],'We found efficiencies in somebody else\'s department.')
add('P','Mandatory Awareness Training',1,'none',[e('shield',1),e('credibility',1),e('draw',1)],'The phishing email congratulated you on passing.')
add('P','No One Owns This System',0,'real',[e('escalate',1),e('panic',1),e('influence',2)],'It belongs to the organization, which is currently in a meeting.')
add('P','All Hands on Deck',2,'real',[e('repair',3),e('credibility',1)],'An emergency so severe that management became useful.')
add('P','Minutes Were Approved',1,'none',[e('clearLiability',1),e('credibility',1)],'The decision was missing. The approval was immaculate.')
add('P','Crisis Branding Workshop',1,'none',[e('leverage',2),e('panic',1),e('liability',1)],'Before we restore services, can we align on the logo?')
add('P','Emergency Procurement',2,'real',[e('repair',2),e('leverage',1)],'The replacement part arrives before the purchase order.')
add('P','Premium Support Tier',2,'real',[e('leverage',2),e('contain')],'Your emergency is very important to our pricing model.')
add('P','Legal Has Joined the Call',1,'none',[e('shield',2),e('credibility',-1)],'Please stop describing the incident accurately.')
add('P','Return to Office (During the Outage)',1,'none',[e('panic',2),e('influence',3),e('credibility',-1)],'Come together. Sit silently. Reconnect indefinitely.')
add('P','Audit Committee Calendar',2,'rival',[e('audit',1),e('steal',2)],'Accountability has a slot at 11:45.')
add('P','Emergency Change Approval',1,'real',[e('repair',2),e('draw',1)],'Someone read it. Someone signed it. Someone fixed it.',condition='verified')

# CONSPIRACIES & PROPHECIES: 15
add('C','The Prophecy (Again)',1,'none',[e('rumor',2),e('panic',3)],'The end is near. The subscription renews monthly.',art='A fictional theatrical prophet in a cheap suit points at a wall of clocks and obsolete calendars while a stagehand quietly replaces the date card.')
add('C','Tomorrow Is the Day',0,'none',[e('rumor',1),e('panic',2)],'An excellent date. Very reusable.')
add('C','Numerological Alignment',1,'none',[e('rumor',2),e('panic',2),e('boost',1)],'Add the digits. Ignore the denominator.')
add('C','The Insider Knows',2,'none',[e('rumor',3),e('panic',3),e('credibility',-1)],'They cannot reveal the source. Or the facts. Or the meaning.')
add('C','Trust the Plan',1,'none',[e('shield',1),e('influence',2),e('panic',1)],'The plan will be revealed after it has happened.')
add('C','Global Blackout (Rumored)',2,'none',[e('rumor',3),e('panic',4)],'Every light in the prediction studio remains on.')
add('C','Screenshot of a Screenshot',0,'none',[e('rumor',1),e('panic',2),e('credibility',-1)],'Evidence, now with fewer pixels.')
add('C','Coincidence Department',1,'real',[e('escalate',1),e('report',2),e('panic',1)],'Two unrelated things happened on the same internet.')
add('C','Secret Weather Machine',1,'none',[e('rumor',2),e('panic',3),e('credibility',-1)],'The forecast is partly confidential.')
add('C','Quantum Patriot Router',2,'none',[e('rumor',2),e('panic',1),e('influence',2)],'Your packets have been liberated from observable reality.')
add('C','The Date Has Been Revised',1,'rumor',[e('withdraw'),e('draw',2),e('panic',-1)],'The prophecy was correct in a scheduling sense.',condition='ownRumor')
add('C','Encrypted Voice Note',1,'none',[e('rumor',2),e('panic',2),e('draw',1),e('credibility',-1)],'A whisper is apparently end-to-end verification.')
add('C','Just Asking Questions',0,'none',[e('reach',1),e('panic',1),e('credibility',-1)],'The answers have been disabled in the comments.')
add('C','The Caveat Was Classified',1,'none',[e('shield',1),e('boost',1)],'You would understand if you had the clearance to disagree.')
add('C','Unfollowed by Reality',2,'none',[e('debunkAll'),e('credibility',1)],'Reality has reviewed your thread and declined to participate.')

# IT HEROES & COUNTERMEASURES: 15
add('H','Last Ticket Standing',3,'real',[e('stability',4),e('repair',4),e('credibility',1)],'Six exhausted technicians. One remaining working coffee maker.',condition='emergency',art='A small diverse team of six exhausted IT technicians works in a dark operations room, lit by a single amber terminal; behind them a city slowly lights up.')
add('H','The Senior Systems Engineer',3,'none',[e('install',asset='engineer')],'Calmly asks the question that ends the meeting.')
add('H','DNS Fixes Everything',1,'real',[e('repair',3)],'It was DNS. The exception was also DNS.',condition='network')
add('H','Have You Tried Restarting It?',0,'real',[e('repair',1),e('panic',-1)],'An ancient ritual with an uncomfortable success rate.')
add('H','Read the Fucking Logs',2,'unknown',[e('verify'),e('shield',1)],'Prevent the next three speculative explanations by opening one file.')
add('H','The Sacred Maintenance Window',2,'none',[e('containAll')],'For these brief hours, change is both permitted and documented.')
add('H','Known Good Backup',2,'real',[e('repair',4)],'A backup is an opinion until you restore it.',condition='verified')
add('H','The Help Desk Remembers',1,'unknown',[e('verify'),e('draw',1)],'Ticket 18427. Same problem. Same vice president.')
add('H','Packet Capture',1,'real',[e('verify'),e('repair',1)],'The packets have no reason to protect your narrative.',condition='network')
add('H','Rollback Plan',2,'real',[e('repair',3),e('panic',-1)],'The bravest new feature is the old working version.')
add('H','Field Technician',2,'none',[e('install',asset='field'),e('credibility',1)],'The cloud required someone with a ladder.')
add('H','Unpaid Overtime',0,'real',[e('repair',3),e('credibility',-1),e('panic',1)],'A heroic fix. A terrible staffing policy.')
add('H','Documented Runbook',2,'none',[e('install',asset='runbook')],'The sacred knowledge has escaped one person\'s memory.')
add('H','The Junior Asked Why',1,'unknown',[e('verify'),e('credibility',1)],'The forbidden question had a very useful answer.')
add('H','Working as Intended',1,'none',[e('stability',3),e('panic',-1)],'For once, this is good news.')

# EMERGENCY EVENTS & WILDCARDS: 15
add('W','This Was Only a Test',1,'rumor',[e('verify'),e('panic',-1)],'Cancel the Apocalypse declaration. Return all unused panic.',art='A vintage emergency broadcast television glows in an empty bunker; its screen shows only a clean abstract calibration target, while a relaxed technician reaches for the off switch. No text.')
add('W','Close All Tickets',0,'none',[e('influence',4),e('liability',2)],'The queue is empty. The users have merely stopped asking.')
add('W','Executive Panic',1,'none',[e('panic',3),e('leverage',2),e('liability',1)],'The emergency began when the CEO noticed the emergency.')
add('W','The Apocalypse Has Been Downgraded',2,'none',[e('panic',-5),e('credibility',1)],'From civilization-ending to mildly inconvenient.')
add('W','The Great Compliance',3,'none',[e('auditAll')],'The machines brought receipts. The humans brought due process.')
add('W','Quiet Weekend',1,'none',[e('stability',2),e('panic',-2)],'No alerts. No predictions. Suspiciously pleasant.')
add('W','Third-Party Review',2,'unknown',[e('verify'),e('stability',2)],'Someone without a bonus riding on the answer.')
add('W','Mutual Aid',1,'real',[e('repair',3),e('allIncome',1)],'Help arrived without a logo requirement.')
add('W','The News Cycle Moved On',1,'none',[e('panic',-3),e('clearBoosts')],'Tomorrow\'s catastrophe is accepting sponsors.')
add('W','The Follow-Up Never Happened',0,'none',[e('clearLiability',1),e('credibility',-1)],'The action item has achieved organizational invisibility.')
add('W','Unscheduled Transparency',1,'none',[e('verifyAll'),e('panic',-2)],'The logs were published before the talking points.')
add('W','The Coffee Arrived',1,'none',[e('draw',3),e('stability',1)],'Morale has been restored in a legally distinct sense.')
add('W','One More Thing',1,'none',[e('action',1),e('draw',1)],'A brief follow-up to the brief follow-up.')
add('W','Emergency Fund',0,'none',[e('influence',4)],'For actual emergencies. A radical interpretation.',condition='fundEmergency')
add('W','The Public Remembers',2,'none',[e('reclaim'),e('credibility',1)],'For once, the person who fixed it gets called back.',condition='counterDiscard')

assert len(cards)==110
assert len({x['id'] for x in cards})==len(cards)
for code,_,n,_ in CATEGORIES: assert sum(c['category_code']==code for c in cards)==n
art_ids=['TGE-M01','TGE-D01','TGE-P01','TGE-C01','TGE-H01','TGE-W01']
for c in cards:
    if c['type']=='Incident':c['rules_short']=f"Real incident. Initial severity {c['effects'][0]['n']}. Panic +{c['effects'][0]['panic']}. Verify, contain, or repair. Uncontained severity contributes to round-end damage."
    if c['id'] in SCENES:c['illustration']['brief']=SCENES[c['id']]
    if (ROOT/c['illustration']['path']).is_file(): c['illustration']['status']='generated reference illustration' if c['id'] in art_ids else 'generated illustration'
bonuses={'TGE-D02':[e('panic',-2)],'TGE-D03':[e('influence',2)],'TGE-D04':[e('credibility',1)],'TGE-D06':[e('draw',1)],'TGE-D12':[e('stability',2)],'TGE-D15':[e('panic',-2)],'TGE-D16':[e('influence',2)]}
for c in cards:
    if c['id'] in bonuses:
        c['effects'][0]['resolution_bonus']=bonuses[c['id']]
        text=' Resolution bonus for the fixer: '+' '.join(rule(x) for x in bonuses[c['id']])
        c['rules']+=text;c['rules_short']+=text
dataset=dict(title='THE GREAT ESCALATION',version=VERSION,edition='Fully illustrated 110-card playable alpha',
  tagline='When everything becomes a crisis, competence is the ultimate conspiracy.',
  categories=[dict(code=c,name=n,count=k,color=h) for c,n,k,h in CATEGORIES],cards=cards)
(ROOT/'data/cards.json').write_text(json.dumps(dataset,ensure_ascii=False,indent=2))
(ROOT/'data/art_briefs.json').write_text(json.dumps([{'id':c['id'],'name':c['name'],**c['illustration']} for c in cards],ensure_ascii=False,indent=2))
(ROOT/'docs/CARD_CATALOG.md').write_text('# The Great Escalation: complete 110-card catalog\n\nVersion '+VERSION+'\n\n'+'\n\n'.join(f"## {c['id']} - {c['name']}\n\n{c['category']} | {c['type']} | Cost {c['cost']} Influence\n\n{c['rules']}\n\nRestriction: {c['restriction']}\n\nCounterplay: {c['counterplay']}\n\n*{c['flavor']}*" for c in cards))
print(f'Authored {len(cards)} unique cards. '+', '.join(f'{x[0]}={x[2]}' for x in CATEGORIES))
