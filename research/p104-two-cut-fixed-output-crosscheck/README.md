# Fixed-output cross-check of #7244

The tested scientific candidate is [#7244](https://github.com/CrocSwap/integer-mult-bounds/pull/7244) at `215f67247f395c0e15f5ea3980f6a3e4aed155af`. The comparator is the #7161 scientific commit `e3f8d39c43b07063dfc5b800f71c5d21015259e6`. Both use the #7113 caller at `07a76c5e2738882c0cb322278e56f6cae3c9885d`.

The [receipt](RECEIPT.json) records exact scalar endpoints and the dirty COPY control, the [#7245](https://github.com/CrocSwap/integer-mult-bounds/pull/7245) census on both words, complete paid and productive rank counts, and directed rational price intervals. Both words have full row rank in every quotient and target class and zero contact-free MOVE pairs. The gain comes from the changed productive fields and the two additional exits charged in each of the 17 stages. Selection and human or formal review remain open under the five assumptions in the [proposed claim](../p104-two-cut-funded-split/PROPOSED-CLAIM.json).

Reproduce from this branch with the pinned commits in the local Git object database. CPython 3.12.3 with assertions took about 51 seconds on the recorded host. The script reuses the main-branch Clifford classifier and implements its own exact scalar replay, elimination modulo 65,521, invoice count and directed price arithmetic.

```sh
git fetch --no-tags https://github.com/CrocSwap/integer-mult-bounds.git refs/pull/7161/head refs/pull/7113/head
python3.12 -I -B research/p104-two-cut-fixed-output-crosscheck/check.py . > /tmp/p104-7244-cross-check.json
cmp /tmp/p104-7244-cross-check.json research/p104-two-cut-fixed-output-crosscheck/RECEIPT.json
```

Credit ToikY for #7245, Clear1nsight and the retained #7161/#7244 lineages, Rohan Arun for #7113, and the canonical Clifford authors. Prepared for Clear1nsight with substantial OpenAI Codex assistance. Apache-2.0.
