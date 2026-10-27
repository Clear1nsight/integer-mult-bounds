# Fraction entry type gate: correctness passes, complete-cost screen stops

This bounded follow-up to [PR #5852](https://github.com/CrocSwap/integer-mult-bounds/pull/5852) proves and tests an entry-domain optimization for the exact contribution table. It preserves the frozen [PR #5848](https://github.com/CrocSwap/integer-mult-bounds/pull/5848) source and independent integer oracle. The full actual Fraction trace agrees, but the complete-cost screen predicts only **12.97% wall and 13.10% CPU savings**, below the donor's required 15%. No complete qualifier, full B/C benchmark or performance PR is constructed. No kappa gain.

## What changed and why it is exact

The earlier table checked all five operand types on each of 2,579,750 coefficient updates. The new wrapper checks a conservative ordinary-input domain once per trace. Under that domain, the unchanged source initializes rows only with standard Fractions and preserves their type through every SCALE/ADD/COPY/update, so the table can omit the repeated operand checks. All other inputs use the predecessor checked method. No trace update, rounded site, score, witness, signed hash or oracle comparison is removed. `PROOF.md` gives the source-bound induction and fallback boundary. Stable inputs and runtime during execution remain required; arbitrary concurrent mutation is outside scope.

The table is still bounded to 16,384 entries and fresh per trace; canonical keys include all five Fraction values. Miss arithmetic and the independent integer backend are unchanged. There is no cross-call or cross-backend answer cache. Direct table use stays checked; explicit recertification can invalidate the specialized method.

## Feasibility before complete construction

All **964 complete finite comparisons** retain the predecessor's 241 programs / 10,164 events at four capacities. All **34 inherited controls plus 20 new controls** pass normally and under optimized Python. New controls cover entry-path selection, subtype/foreign-type fallback without custom method calls, matching original method order, internal Fraction types, malformed outcomes, recertification and disabled capacity. The original finite and table source bytes are retained in `parent_finite.py` and `table_parent.py`.

One actual audit compares every value, type, witness and input on **25,984 events / 799 coordinates**. It preserves full output digest `954c7448ff74d78753828e9623ad44c46da9e5ce459420b6e50a5d47294250b9`, with the original 2,252,966 hits / 326,784 misses / 310,400 evictions. The actual input satisfies the proven entry domain.

| Observation | Original trace | Derived trace |
|---|---:|---:|
| Wall | 20.611703 s | 13.832812 s |
| Process CPU | 20.598246 s | 13.824505 s |

These are single ordered within-process observations, not complete qualification medians or a controlled estimate of the entry gate's incremental effect over the earlier table. The new full finite stage takes 1.720395 seconds wall / 1.68 seconds CPU in the declared observation. Charging it against PR5848's previous complete medians gives:

- Wall: `39.014916 - 6.778891 + 1.720395 = 33.956420 s`, **12.97% modelled saving**.
- CPU: `38.88 - 6.773741 + 1.68 = 33.786259 s`, **13.10% modelled saving**.

This is an engineering screen combining observations, not a measured complete wall/CPU result or universal obstruction. It triggers the declared stop before complete construction. No extra capacity/algorithm trial, full six-process expansion or hosted performance claim follows.

## Reproduction and evidence

Python 3.12, standard library only:

```sh
python3 -B scripts/research_package.py --package research/fraction-type-gate-feasibility
```

This executes a **fresh full finite differential and all 54 controls**, around two seconds on this Linux host. It does not freshly replay full actual qualification, validate performance, or replace the admitted source command. The manifest labels finite-only coverage. `actual_audit.py` is separately opt-in and takes about 37 seconds here; a new serial budget and the original 180-second / 1 GiB sampled group-RSS / no-automatic-retry contract are required before replay. No historical replay is needed merely to acknowledge this finding.

`evidence/` retains all raw streams/resource receipts, the preconstruction plan, complete-cost screen and diagnosed failed harness draft. The first attempt passed all inherited finite coverage, then its new-control setup imported a stale source module whose temporary directory had been removed. A fresh uniquely named source import fixes only harness lifetime; no arithmetic or case/control was removed. Its failed receipt is charged and remains visible. Publication setup failures in the partial/promisor checkout are recorded separately; they are not scientific failures. Frozen source bytes/modes remain unchanged. Full-history preflight is unavailable in this shallow checkout.

Source input is the unchanged complete official 97-file PR5848 export at `66fb6c6b8683b37967e9d7f313b3df99a49d2406`, including original PR5831/5826 archives and notices. Own input ancestor `c8162607d3576c3387eddf216882bc1b85a92b40` retains archive and predecessor-code blobs. Exact canonical main remains `de5ec2e7a6074068452f45b1a191b5c72832df4a`, priority 8. Targeted PR/comment/handoff checks found no matching active successor within bounded search coverage; unpublished/global novelty is not established. Final static review found a foreign-metaclass equality side effect in the initial type-alternative predicate. All alternatives now use identity checks, two controls were added, and the full actual audit was repeated. Both earlier and final observations remain; no sample was discarded. The earlier two negative packages are now published as PR5852/5853; this new entry-gate result remains a fork artifact and upstream handoff.

## Open next questions

A different exact arithmetic mechanism needs a separately bounded primitive/self-time or reuse census, a complete validation and memory/time bill, and a new finite gate. The present table/entry proof has not reached 15% complete savings; another local shortcut cannot be justified from its headline trace result alone. No successor is dispatched. Kappa research, Work 1/2, feeds and automations remain paused.

## Credit and limits

Ali Romman supplied the original Fraction/error arithmetic, exact integer backend and [PR #5831](https://github.com/CrocSwap/integer-mult-bounds/pull/5831)/[PR #5826](https://github.com/CrocSwap/integer-mult-bounds/pull/5826)/[PR #5819](https://github.com/CrocSwap/integer-mult-bounds/pull/5819) lineage. Retain Adam Gall, ywz65, [PR #2878](https://github.com/CrocSwap/integer-mult-bounds/pull/2878), Mason Hale/[PR #5811](https://github.com/CrocSwap/integer-mult-bounds/pull/5811), all original native/compiler/precision notices and the [PR #5839](https://github.com/CrocSwap/integer-mult-bounds/pull/5839)/[PR #5816](https://github.com/CrocSwap/integer-mult-bounds/pull/5816)/[PR #5818](https://github.com/CrocSwap/integer-mult-bounds/pull/5818)/[PR #5832](https://github.com/CrocSwap/integer-mult-bounds/pull/5832) verification lineage. The branch retains exact test-only [PR #5761](https://github.com/CrocSwap/integer-mult-bounds/pull/5761) and Ali Romman's authorship/cherry-pick credit. PR5852 supplies the table and source/finite lineage. Memoization and loop-invariant reasoning are standard.

New entry proof, controls and execution by Chris R / Clear1nsight with substantial OpenAI Codex assistance. No scientific subagents, independent human or proof-kernel acceptance. Two publication agents handled only earlier branches. This does not discharge physical/native/compiler/outer obligations or alter selected kappa. Apache-2.0.
