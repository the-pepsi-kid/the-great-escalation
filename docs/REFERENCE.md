# THE GREAT ESCALATION - TABLE REFERENCE

## A turn

Gain 3 Influence (+1 if Credibility 4+, -1 if Panic 12+). Draw 1. Take 2 actions. End when ready. Discard newest cards until hand size is 8.

| Basic action | Cost | Result |
| --- | --- | --- |
| Find Funding | 0 | Gain 2 Influence. |
| Repair | 1 | Repair 2. Restore 1 Stability. Verified work: +1 Accountability. Resolution: +1 Accountability, +1 Credibility, +1 more Stability. |
| Verify | 1 | Unknown real: +1 Accountability, +1 Credibility, Panic -1. Rumor: same reward, Panic -2; sponsor -1 Reach and +1 Blame; discard rumor. |
| Report | 1 | Real incident only. Gain 1 Reach + stored boost (maximum 5). Consume boost. Panic +1. |
| Monetize | 1 | Real incident and Panic 6+. Gain 2 Leverage; +1 Liability; Panic +1. |
| Reassure | 0 | Panic -2. Credibility +1. |

Every basic action also costs one action. Card Repair, Verify and Audit effects use the same normal rewards.

## Audit and containment

Audit issues in this order: oldest sponsored rumor, then Liability, then all report boost as one issue. Audited Liability becomes Blame and costs 1 Leverage and 1 Credibility. Any productive audit gives the actor 1 Accountability and 1 Credibility; replace verification rewards, do not add both. A shield blocks a whole audit or one theft/transfer automatically. Each separate card component still resolves.

Containment lasts through this round. The incident stays in play but causes no severity damage or round-end Panic. Maximum two supports; a third retires the oldest. Support triggers reset each own turn.

## Round end

Add uncontained real severity; damage = ceil(total / 4), +1 if Panic is already 12+. Reduce Stability. Then Panic rises by uncontained real count, maximum +3. If no real incidents remain, Stability +2 and Panic -2. Stability zero now: everyone loses. Otherwise after round 8 score, or reveal ceil(players / 2) new incidents and continue.

## Scoring and limits

| Path | Prestige |
| --- | --- |
| Restoration | 2 x Accountability + Credibility |
| Narrative | floor(5 x Reach / 2) + Credibility |
| Exploitation | max(0, 2 x Leverage + floor(Influence / 3) - 2 x Blame - Liability) |

Use only your highest lane. Ties: higher Credibility, then lower Blame + Liability, then shared victory. Influence cap 15, Credibility 6, Panic 18, Stability 24, Shields 3, boost 3. Severity cap 8. Accountability and Blame are durable. Real queue limit = players + 2. There is no rumor-slot cap.
