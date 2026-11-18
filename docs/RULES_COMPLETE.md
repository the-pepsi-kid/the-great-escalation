# THE GREAT ESCALATION

## Field manual - playable alpha 0.1.0

When everything becomes a crisis, competence is the ultimate conspiracy.

Everyone is announcing the end of civilization. Six exhausted technicians are trying to restore the network. You run an institution caught between those two business models.

**Players:** 2-6. **Length:** 8 rounds, roughly 25-50 minutes at a table. **Format:** one shared action deck and one incident deck. **Edition:** all 110 cards implemented and individually illustrated. The print deck is a playtest proof.

## 1. Win while there is still a world

Compete for the highest Prestige after round 8. Every institution can pursue any of the three paths. Your Prestige is your highest path score, not the sum. You do not choose a permanent class.

| Path | Prestige |
| --- | --- |
| Restoration | 2 x Accountability + Credibility |
| Narrative | 5 points per pair of Reach, plus 2 for an unpaired Reach, plus Credibility |
| Exploitation | 2 x Leverage + floor(Influence / 3) - 2 x Blame - Liability; minimum 0 |

Narrative is equivalently floor(5 x Reach / 2) + Credibility. Round down only where stated. Example: 7 Reach and 4 Credibility score 17 + 4 = 21. Exploitation example: 8 Leverage, 9 Influence, 2 Blame and 1 Liability score 16 + 3 - 4 - 1 = 14.

Ties break by higher Credibility, then fewer total Blame + Liability. If still tied, share victory. If Stability is zero at any round end, everyone loses immediately. No scoring path overrides collapse.

Panic by itself scores nothing. Accountability survives audits. Reach can be lost when a sponsored rumor is debunked. Liability and Blame threaten an exploiter's score. A profitable institution still needs a functioning world.

## 2. Components and setup

Separate the 20 red Infrastructure cards into the incident deck. Shuffle the other 90 cards into the action deck. Incidents never enter player hands. Every physical card appears exactly once.

At a table, supply a pencil, each player's score tracker, markers for Panic and Stability, case markers for severity and verification, and two support slots per institution. Coins or paper scraps work as tokens. The reference sheet includes trackers.

1. Give each institution 5 Influence, 3 Credibility, and zero Accountability, Reach, Leverage, Liability, Blame, Shields and stored report boost.
2. Set Stability to 20 of 24 and Panic to 2 of 18. Choose a first player; turn order stays fixed for this alpha.
3. For the standard browser opening, seats 1, 2 and 3 receive Senior Systems Engineer, The Algorithm Has Spoken and Premium Support Tier respectively, if still available. Seats 4-6 attempt the same sequence; already-dealt cards are skipped. Fill every hand to 5 from the shuffled action deck. At a table, deal those same available starters, then shuffle and fill to 5, or agree to fully random hands.
4. Reveal ceil(player count / 2) incidents at the start of each round: one for 2 players, two for 3-4, three for 5-6. Apply each printed entry Panic increase. Each incident begins unverified at its printed severity.
5. Start the first turn. Its normal income and draw happen immediately, so the first player normally has 6 cards and 8 Influence.

The browser also offers three prebuilt five-card openings for the first institution: Restoration, Newsroom, and Crisis Consultant. They replace its mixed opening and remove those cards from the shared deck. They are learning aids; automated balance results use the standard opening.

| Prebuilt opening | Five cards |
| --- | --- |
| Restoration | H02, H05, H08, H09, H14 |
| Newsroom | M01, M03, M13, M19, M25 |
| Crisis Consultant | P14, P15, P16, W03, P07 |

All IDs in this table have the TGE- prefix. The browser seed reproduces shuffling and initial hands. It does not hide the case type: a real outage and an unsupported rumor are visibly different. Verification establishes evidence and rewards; this is not a hidden-trait deduction game.

## 3. Resources and limits

| Resource | Use and limit |
| --- | --- |
| Influence | Spend on cards and basic actions. Maximum 15; excess gains are lost. |
| Panic | Shared public alarm, 0-18. At 12 or more it lowers turn income by 1 and adds 1 round-end Stability damage. |
| Credibility | Personal trust, 0-6. At 4 or more gain +1 turn income. Adds to Restoration and Narrative scores. |
| Stability | Shared operational health, 0-24. Zero at round end is collective defeat. |
| Accountability | Durable personal evidence and repair record. No card removes it in this edition. |
| Reach | Personal audience, principally earned by reporting. Debunked rumors cost their sponsor 1 Reach. |
| Leverage | Personal crisis profits. Audits of Liability remove it. |
| Liability | Public, unaudited exposure. Costs 1 Exploitation point each. Can be transferred or removed by specific cards. |
| Blame | Established responsibility. Costs 2 Exploitation points each. Cannot be removed or transferred. |
| Audit Shields | Up to 3. Automatically spend one to block an entire audit, Influence theft or Liability transfer. |
| Report boost | Up to 3. Adds to the next Report effect, then is consumed. A single report earns at most 5 Reach. |

Unless a card says otherwise, changes clamp at zero and the stated maximum. A card can be played even when some resource gains will be lost at a cap. Reach, Accountability, Leverage, Liability and Blame have no gameplay cap. Hand limit is 8 at turn end, not during the turn.

## 4. A turn

1. Gain 3 Influence, +1 if your Credibility is at least 4, -1 if Panic is at least 12. Apply both modifiers, then the 15 Influence cap.
2. Draw 1 action card. Reset your once-per-turn support triggers. Receive 2 actions.
3. Spend actions on cards or basic actions in any order. Pay printed Influence and 1 action before resolving. Choose all required targets before paying. Resolve printed effects in order, then discard the card unless it stays as a support or sponsored rumor.
4. End your turn whenever you wish; unused actions are lost. If you hold more than 8 cards, discard the newest cards from the right end of your hand until you have 8. This automatic discard rule is deliberately the same in print and browser.

One More Thing spends an action and gives one back, so it replaces its own action cost; it does not create an additional net action. Income does not happen again. There are no out-of-turn reactions in this alpha. Shields block automatically; other counterplay occurs during your own turn.

When the action deck empties, shuffle its discard pile and continue drawing. Active supports and rumors are not in that discard pile. If both deck and discard are empty, the draw is skipped. Resolved incidents go to a separate incident discard, recycled when its deck empties. Never shuffle incidents into action cards.

## 5. Your six basic actions

You always have these actions. Each costs one action in addition to the listed Influence. No card is required.

| Action | Influence | Effect |
| --- | --- | --- |
| Find Funding | 0 | Gain 2 Influence. |
| Repair | 1 | Repair 2 severity on one real incident. Restore 1 Stability. If it was verified, gain 1 Accountability. If resolved, gain +1 Accountability, +1 Credibility and restore +1 more Stability. |
| Verify | 1 | Verify one unknown case. Gain 1 Accountability and 1 Credibility. A real case lowers Panic by 1. A rumor is debunked using the penalties below. |
| Report | 1 | Report any real incident for 1 Reach plus stored boost, maximum 5. Consume the boost; Panic +1. An incident may be reported again on a later action. |
| Monetize | 1 | Requires a real incident and Panic at least 6. Gain 2 Leverage, take 1 Liability, Panic +1. |
| Reassure | 0 | Lower Panic by 2 and gain 1 Credibility. |

Reporting a real outage does not make it verified. A visible event and its verified cause are different things. Specific cards require evidence before they can use a real incident.

## 6. Cases: real outages and unsupported rumors

Real incidents have 2-5 initial severity, a technology tag, an evidence state, and a specific cause. Escalation adds severity up to 8. Repair reduces it. Severity zero immediately resolves and removes the incident. No unfinished repair progress is lost between turns.

Every successful Repair effect restores 1 Stability. A repair of a verified incident earns its actor 1 Accountability, regardless of severity repaired. Resolving a real incident also gives its actor 1 Accountability, 1 Credibility and 1 more Stability. This resolution reward applies even to an unverified incident. Excess repair is lost, not carried to another case. A single multi-point repair is one effect and earns at most one work reward and one resolution reward.

Seven incidents also print a resolution bonus. The institution that reduces that incident to zero receives the bonus once, after the standard rewards. For example, restoring Banking Outage grants the fixer 2 extra Influence. This distinguishes similarly severe failures and creates a choice about which recovery to finish first.

Verification of a real incident reveals its cause, gives 1 Accountability and 1 Credibility, and lowers Panic by 1. Once verified, it cannot be targeted by basic Verify again. A mixed card such as Packet Capture may still repair an already verified eligible incident; its redundant Verify effect simply does nothing.

A conspiracy or media card that sponsors a rumor stays beside the queue. Rumors have zero outage severity and never count toward combined incident severity. Their Panic can still push the public into the high-Panic penalty. The sponsor receives the card's immediate Reach and other effects.

Verifying a rumor removes its card to the action discard, lowers Panic by 2, gives the verifier 1 Accountability and 1 Credibility, and gives the sponsor -1 Reach and +1 Blame. These penalties apply even when someone debunks their own rumor. A sponsor can instead use The Date Has Been Revised to withdraw their own rumor: lose 1 Reach, remove it, and apply that card's other effects without the normal debunk reward or Blame.

The queue can hold player count + 2 real incidents. If a new incident would exceed that limit, discard the newly revealed card, add 1 severity to the oldest real incident (maximum 8), and raise Panic by 1. Do not also apply the discarded incident's entry Panic. Rumors do not use real-incident slots. There is no rumor-slot cap.

## 7. Seven connected mechanics

| Mechanic | How it works |
| --- | --- |
| Escalation | Add severity to a real incident, maximum 8. This increases future damage, not immediate damage. |
| Amplification | Store report boost, maximum 3. The next Report effect consumes all of it, maximum 5 total Reach. Direct gain-Reach effects do not consume a boost. |
| Containment | Mark a real incident as contained through the current round. It contributes neither severity damage nor exposed-incident Panic at that round end. It remains in play and becomes exposed next round. |
| Verification | Establish real evidence or remove an unsupported rumor. Already verified cases cannot generate repeated verification rewards. |
| Recovery | Restore Stability and reduce severity. Repair work and resolution award durable Accountability. |
| Blame Transfer | Transfer unaudited Liability, never established Blame. A rival can automatically spend one shield to block the transfer. |
| Audit | Review a rival's actual public issues, oldest sponsored rumor first, then Liability, then report boost. Honest institutions without issues are ineligible for targeted audits. |

An audit reviews up to its printed issue count. Each rumor reviewed gets normal debunk removal, Panic reduction and sponsor penalties, but the audit's reward replaces normal verification rewards. Each Liability reviewed becomes one Blame and costs that rival 1 Leverage and 1 Credibility. If no rumor or Liability remains, remove all of that rival's stored report boost as one issue. A productive audit gives its actor exactly 1 Accountability and 1 Credibility, regardless of issues reviewed. One shield blocks the entire audit and is consumed; the actor receives no audit reward.

The Great Compliance audits one issue at each eligible rival in seat order. Each rival can block separately. Each productive audit earns its own normal reward. It does not punish people without a documented issue. Its fiction follows evidence, human law and due process.

Shields also block one Influence theft or Liability transfer. Separate effects on the same card resolve separately: a shield that blocks an audit is gone when a later theft effect resolves. A blocked component does not cancel the card's other printed effects. A theft transfers only the minimum of the printed amount, the victim's actual Influence and the recipient's space below 15; money is not created by theft.

## 8. Support desk

You have two permanent support slots. A support card stays in your area and is not discarded after play. Installing a third automatically retires the oldest support into the action discard. Retiring a support does not replay its effect or refund its cost.

| Support | Trigger |
| --- | --- |
| Senior Systems Engineer | Your first repair each own turn repairs +1 severity. |
| Field Technician | Your first repair of a physical-tag incident each own turn repairs +2 severity. |
| Documented Runbook | Your first successful rewarded verification each own turn draws 1 action card. |

Engineer and Field Technician can combine on the same repair. A trigger is consumed when its qualifying effect resolves, even if the incident needs fewer repair points. Audits do not trigger the Runbook because their verification rewards are replaced by audit rewards. A multi-Verify card can trigger the Runbook once only.

## 9. End of round

After the final institution's turn, use the current board and Panic value:

1. Add the remaining severity of all uncontained real incidents. Divide by 4 and round up. Add 1 damage if Panic is already at least 12. Reduce Stability by that total.
2. Raise Panic by the number of uncontained real incidents, maximum +3. Contained incidents and rumors do not count.
3. If there are no real incidents at all, restore 2 Stability and lower Panic by 2. This also applies if the only cases left are rumors. A contained real incident still prevents this clean-board bonus.
4. If Stability is now zero, everyone loses. Otherwise, after round 8 score Prestige and declare the winner. If earlier, advance the round, reveal new incidents, then begin the first institution's turn.

The high-Panic damage check occurs before the round-end Panic increase. Stability can reach zero during a turn and be restored before round end. A card cannot prevent collapse after the end-of-round check has finished. Containment is marked by round number and expires automatically as the next round begins.

## 10. Timing and edge cases

All action and support cards are played during their owner's turn. Incidents are revealed only at round start. The selected target must exist and meet the card's restriction when played. An illegal action spends nothing and changes nothing.

Effects then resolve left to right. A component that no longer applies does nothing; later components still resolve. For example, The Camera Found IT can finish a verified incident and still Report that just-completed incident using its already chosen target. Verification during a mixed card does not require a second target selection.

Choose a rival with an auditable issue for a card that includes a targeted audit. Targeted theft alone can select any rival, including one with zero Influence; the actual transfer may then be zero. Liability-transfer cards require at least one of your own Liability. Blame is never a valid transferable substitute.

Bulk verification rewards are capped per card: Unfollowed by Reality gives normal verifier rewards for the first three rumors only; Unscheduled Transparency for the first two real incidents only. Cases are processed oldest first. Every affected rumor still gives its sponsor the normal penalty, and all verified real incidents still lower Panic even beyond the reward cap.

Cards in the discard pile are public. The Public Remembers retrieves the most recently discarded IT card; it cannot retrieve an incident or an active support. Hand-limit discards are newest first. If the newly retrieved card exceeds the hand limit at turn end, it can be discarded by that same rule.

## 11. Browser controls

Open index.html in a modern browser. It contains the engine, all 110 card definitions, fonts, and all 110 illustrations, and needs no server or account. Your current game saves automatically when browser storage is available. Save file exports an independent JSON save; Load file restores a compatible 0.1.0 game.

Click a case to inspect it and take a quick Repair or Verify action. Click a hand card to read full rules, restrictions and counterplay, select a target, and play. The left rail contains all six basic actions. Cards in The 110 Cards archive are inspectable but cannot be played directly from the collection.

New game chooses 2-6 players, mixed or focused automated rivals, a random or reproducible seed, and an optional prebuilt opening. Pass & play makes every seat human and covers the next hand until the player accepts the device. Undo reverses your most recent action until you end your turn; ending the turn commits it. Restarting uses New game and replaces the current autosave.

The browser shows each institution's live Prestige, public resources, Liability, Blame and shields. Open Scores & resources for all three lanes. Bot hands stay private. The incident log records resolution order. Keyboard controls use native buttons, labeled selectors, visible focus and Escape to dismiss inspectors. Motion respects the device preference.

## 12. Complete example game

The following eight-round example is produced by the same deterministic rules engine as the browser. It records every action, including basic actions. It illustrates legal resolution rather than a recommended optimal strategy.

Seed 431638. Standard two-player opening. The Repair Desk favors Restoration; The Nightly Bulletin favors Narrative. Both can use any scoring path.

| Round | Institution | Actions in order | End-turn Prestige |
| --- | --- | --- | --- |
| 1 | The Repair Desk | The Senior Systems Engineer; Repair -> DHCP Hunger Games | 6 |
| 1 | The Nightly Bulletin | Numerological Alignment; Expert Panel of Absolutely Nobody | 12 |
| 2 | The Repair Desk | Congressional Hearing -> The Nightly Bulletin; Verify -> Region Unavailable | 12 |
| 2 | The Nightly Bulletin | The Algorithm Has Spoken; Report -> Region Unavailable | 19 |
| 3 | The Repair Desk | Repair -> Region Unavailable; Repair -> Region Unavailable | 18 |
| 3 | The Nightly Bulletin | Report -> Empty Generator Tank; Report -> Empty Generator Tank | 24 |
| 4 | The Repair Desk | Rollback Plan -> Empty Generator Tank; Verify -> Identity Provider Vacation | 22 |
| 4 | The Nightly Bulletin | Report -> Identity Provider Vacation; All Hands on Deck -> Identity Provider Vacation | 28 |
| 5 | The Repair Desk | Repair -> Identity Provider Vacation; Verify -> Broadcast Storm | 28 |
| 5 | The Nightly Bulletin | The Insider Knows; Report -> Broadcast Storm | 37 |
| 6 | The Repair Desk | Repair -> The Building Has One Uplink; Read the Fucking Logs -> The Insider Knows | 32 |
| 6 | The Nightly Bulletin | Report -> Broadcast Storm; Report -> Broadcast Storm | 39 |
| 7 | The Repair Desk | Repair -> Broadcast Storm; Repair -> Broadcast Storm | 38 |
| 7 | The Nightly Bulletin | Report -> Nationwide Ground Stop; The Junior Asked Why -> Nationwide Ground Stop | 44 |
| 8 | The Repair Desk | Repair -> Nationwide Ground Stop; Repair -> Nationwide Ground Stop | 44 |
| 8 | The Nightly Bulletin | Report -> Flooded Equipment Closet; Report -> Flooded Equipment Closet | 49 |

| Round end | Stability | Panic |
| --- | --- | --- |
| 1 | 24 | 5 |
| 2 | 22 | 7 |
| 3 | 23 | 11 |
| 4 | 23 | 12 |
| 5 | 22 | 17 |
| 6 | 22 | 18 |
| 7 | 22 | 18 |
| 8 | 22 | 18 |

Result: **The Nightly Bulletin wins.** The Repair Desk: 44 Prestige (restoration). The Nightly Bulletin: 49 Prestige (media).


## 13. Print and play

Use the US Letter six-up deck for home playtesting at Actual size / 100%, with duplex long-edge if printing the interleaved version. Each trim card is 2.5 x 3.5 inches. A 0.125-inch bleed surrounds each card; crop marks indicate the trim. Print the first front and back as an alignment proof before committing the full deck. Home-printer feed alignment is not guaranteed by the PDF.

Card_Faces_Bleed.pdf has 110 single-card pages, each 2.75 x 3.75 inches including bleed, with TrimBox and BleedBox metadata. Card_Backs_Bleed.pdf contains separate action and incident backs. The six-up print deck keeps those backs distinct so you can separate decks while playing. The final sheet's unused slots stay blank on the front. Printed short rules use the defined Repair, Verify, Audit and Report keywords; consult the reference sheet for their standard rewards.

All 110 cards now have individual illustrations in the approved ink-and-newsprint style. The Full_Illustrated_Card_Atlas.pdf shows every image with its card title and ID across ten pages. This alpha is suitable for playtest printing. Commercial finishing still requires human playtests, a physical proof, and a printer's color and stock specifications.

## 14. The point

The apocalypse has been monetized. The network is still down. Please hold.

HOLY HOLY.
