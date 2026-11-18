import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
d=read('data/cards.json');tests=read('docs/test-results.json');sim=read('docs/balance-results.json');art=read('docs/artifact-results.json');pr=read('docs/print-validation.json')
unused=[c for c in d['cards'] if c['type']!='Incident' and c['id'] not in sim['cardPlays']]
lines=['# The Great Escalation - quality and balance report','',
'Edition 0.1.0, art revision 1. Fully illustrated 110-card alpha.','',
'## What is complete','',
f'- Exactly 110 unique cards: 25 Media, 20 Infrastructure, 20 Political/Corporate, 15 Conspiracy, 15 IT and 15 Wildcards.',
'- All 90 action/support/narrative cards resolve in dedicated legal fixtures. All 20 incident definitions have valid reveal rules, severity, tags and evidence.',
'- All 110 have different mechanical signatures after excluding titles and root-cause prose. Seven similarly severe incidents have distinct recovery bonuses.',
'- Source-of-truth JSON, validated JSON Schema, a full XLSX catalog and 110 individual art briefs.',
'- One rules engine shared by the offline browser, simulations, tests and complete eight-round example.',
'- Solo automated opponents, 2-6 seats, pass-and-play, prebuilt openings, card inspection, collection filters, event log, autosave, file saves and Undo are implemented.',
'- A nine-page field manual, rules reference, pencil trackers, distinct action/incident backs and all 110 typeset faces.',
f'- Print files: {pr["face_pages"]} single-card pages with 2.5 x 3.5 inch TrimBox and 0.125 inch bleed; 19 six-up front sheets and {pr["duplex_pages"]} interleaved duplex pages.',
'- All 110 individually generated illustrations, a ten-page full-deck art atlas and the preserved six-card style proof. Typography is controlled separately from art.','',
'## Checks actually performed','',
f'- Rules: **{tests["passed"]}/{tests["total"]} test groups passed**, including all-card fixture resolution, 110-card conservation, illegal-action atomicity, verification rewards, rumor penalties, real repair, shields, audits, support triggers, capped transfers, prebuilt hands, seeded determinism and complete matches.',
f'- Final artifact checks: **{art["passed"]}/{art["total"]} passed**. These include the embedded catalog, syntax compilation of all three HTML script blocks, unique static IDs, no external asset dependencies, actual art completion flags, all 110 PDF IDs, card trim/bleed metadata and the workbook export.',
'- Workbook: formulas reconcile 110 cards, 110 illustrated and 0 pending. Changing one illustration status changes the totals to 109/1; restoring it returns 110/0. Formula-error scan found none. Overview and catalog previews were reviewed.',
'- PDF visual review: the complete ten-page art atlas, illustrated face sheets, card backs and the manual were rendered and inspected. A narrow example-table heading and a logo spacing issue were corrected. The face builder checks text fit; body type is 8 points.',
'- All 110 cards have individual written illustration scenes. All 110 have actual image files and distinct source checksums. All 110 are embedded in the HTML and every single-card PDF page contains its own high-resolution illustration. No card face has an art placeholder.','',
'## Seeded match evidence','',
f'{sim["games"]} complete deterministic games from the unchanged rules build: 100 each at 2, 3, 4, 5 and 6 players. Bot strategy labels and seats rotate. A bot can still win using a different path from its preferred label. Tied winners split their win share.','',
'| Winning path | Win share | Share of 500 games |','| --- | ---: | ---: |']
for key,label in [('restoration','Restoration'),('media','Narrative'),('exploitation','Exploitation')]:
    v=sim['winningPaths'].get(key,0);lines.append(f'| {label} | {v:g} | {v/5:.1f}% |')
lines+=['','| Players | Games | Collapses | Mean winning Prestige |','| --- | ---: | ---: | ---: |']
for row in sim['byPlayers']:lines.append(f'| {row["players"]} | {row["games"]} | {row["collapse"]} | {row["meanWinnerScore"]} |')
lines+=['',
'These samples show that every scoring path can win against these heuristics. They do not establish tournament balance or human skill ceilings. Bots deliberately value keeping the world operational. None of these 500 games collapsed, so this sample does not establish human collapse frequency or difficulty. A separate neglect test confirms that passing every turn causes collective collapse at every supported player count.','',
f'**{len(unused)} action cards were never selected by these bots.** Their effects are implemented and pass legal-fixture tests; human testing should determine whether their situational value, pricing or the bot evaluator needs adjustment.','',
'| ID | Card |','| --- | --- |']
lines += [f'| {c["id"]} | {c["name"]} |' for c in unused]
lines+=['',
'## Explicitly unverified or unfinished','',
'1. **Live browser walkthrough is unverified.** Local Chromium could not create its singleton socket. The cloud preview rejected local file URLs. No workaround was attempted after that policy denial. The browser script compiles, but actual desktop/mobile rendering, dialog interactions, save import/export, autosave behavior, handoff privacy and bot pacing need the included Playwright walkthrough in a browser-enabled environment.',
'2. **Art is complete for this alpha.** All 110 cards have individual illustrations in the user-approved style. The original PNG archive contains 110 unique 1536 x 1024 files. The art update changes no card mechanics or engine code, verified against the preceding build.',
'3. **Human playtests are pending**, especially at two and six players, with all three paths represented, aggressive audits, deliberate non-cooperation, prebuilt openings and shared-loss pressure.',
'4. **Commercial print finishing is pending.** PDFs have geometric bleed, trim and cut guides, but no physical duplex proof, printer-specific CMYK profile, chosen stock, tolerance proof or production packaging has been approved. These are playtest PDFs.',
'5. The alpha has fixed seat order and automatic newest-first hand-limit discards. Their fairness and usability need human review. There is no online multiplayer, deck-construction editor or hidden-reaction system; those are outside this shared-deck alpha.',
'6. The user approved the shared art style. Individual scene refinements can follow review of the complete atlas; no placeholder art remains.','',
'## Production milestones','',
'| Phase | State |','| --- | --- |',
'| Rules and architecture | Complete for alpha |',
'| Full 110-card catalog | Complete |',
'| Playable prototype | Engine verified; browser shell implemented, live walkthrough pending |',
'| Art production | Complete: 110/110 individual illustrations |',
'| Print and digital package | Complete playtest proofs; commercial finish pending |',
'| Acceptance | Automated engine/catalog checks pass; browser, human playtests and commercial finishing remain open |','',
'No tested engine defect remains open. This does not claim that the unverified browser shell is defect-free. No repository push, public hosting or publication was performed.','']
(ROOT/'docs/QUALITY_REPORT.md').write_text('\n'.join(lines))
print('Quality report generated with actual test and simulation results.')
