# Mode-fiber rounding radius: R = 1 is a finite question, and R ≤ 6

A scoped partial answer to the first open question of Nick Petalas's #6312
(`research/mode-preserving-rounding`, open at head `46593234`). For the PR4933
mode matrix M (112×8), let R be the least ℓ∞ radius such that every x with a
nonempty integer fiber {z ∈ ℤ^112 : Mᵀz = Mᵀx} has a point of that fiber within R.
#6312 proves R ≥ 1. This package proves:

- **Structure.** L = Mᵀℤ^112 = {x ∈ ℤ^8 : x mod 2 ∈ H8}, the Hamming construction
  of √2·E8, with index 16. The 14 row supports are the weight-four words of
  [8,4,4], with 8 rows each. MᵀM = 56·I. The row set is not closed under negation.
- **Theorem A (finite reduction).** R ≤ 1 if and only if every lattice point of L
  in the *open* zonotope Mᵀ(0,1)^112 is a 0/1 subset sum of rows. One interior
  lattice point that is not a subset sum forces R > 1. So **R = 1 is a finite
  decision problem**, and either answer has a finite exact certificate.
- **Theorem B.** **R ≤ 6.** This is the first explicit upper bound. It uses an 8-row
  basis of L in which every other row has coordinates of ℓ₁ norm at most 6,
  plus Beck–Fiala iterative rounding.
- **Evidence, not proof.** All 1,864 sampled interior lattice points near vertices
  and faces (face rank 0–7) are subset sums. This supports the conjecture R = 1.

[PROOF.md](PROOF.md) has the arguments and exact scope. The basis is in
[CERTIFICATE.json](CERTIFICATE.json), the witnesses in [SEARCH.json](SEARCH.json),
and the pins in [SOURCES.json](SOURCES.json). Complete κ and the selected frontier
are unchanged. This is a property of the exact-mode contract. It does not claim
that any caller needs the contract, and supplies no physical rounder or error/tape bill.

## Reproduce

From the repository root; the standard library suffices:

```sh
python3 -I -W error -B research/mode-fiber-radius-bounds/verify.py
python3 -I -O -W error -B research/mode-fiber-radius-bounds/verify.py
python3.12 -B scripts/research_package.py --package research/mode-fiber-radius-bounds
```

Each prints `PASS_MODE_FIBER_RADIUS_BOUNDS` in about a second. It checks the
structure facts, the HNF lattice identity, the rank condition Theorem A needs,
the #6312 witness relation, the τ = 6 basis (|det| = 16, integral coordinates,
maximum ℓ₁ norm exactly 6) and every subset-sum witness exactly. It also checks
seven rejection controls: a flipped matrix entry, a repeated basis row, a claimed
τ = 5, a non-basis, a wrong witness mask, an off-lattice target and a broken
witness relation. Interiority of the sampled targets came from a floating-point
LP and is not certified.

The non-certifying search scripts in `search/` need numpy and scipy:
`evidence.py SEED TRIALS` regenerates one evidence run (seeds 11–14, 320 trials
each), and `basis_search.py SEED RESTARTS` repeats the basis search.

## Open next questions

1. **Decide R = 1.** Is every lattice point of L in the open zonotope a subset
   sum? This would settle #6312's question exactly. First step: reduce the
   near-boundary cases with the signed-permutation symmetry of the rows, and try
   a face recursion, where deep points are handled by discrepancy rounding and
   points near a face reduce to the rows in that flat. Blocker: about 10¹²
   lattice points rule out brute force, and the recursion is unproved.
2. **Lower the bound below 6.** Local search finds no basis with τ < 6, so this
   method is exhausted. First step: move y to a vertex of its fiber polytope, with
   at most 8 independent fractional rows F. Then R < 2 follows if every lattice
   point of the zonotope of F is a {−1,0,1} combination of the other rows.
   Check this over non-primitive F up to symmetry. Blocker: about C(112,8) sets F
   before reduction.

## Credit

Dillon Amburgey (PR4933) supplies M. Nick Petalas (#6312) supplies the contract,
the radius-one witness and the question. Its predecessor credits (JoyboyBrian,
Dugongue, Ali Romman) carry over. Beck–Fiala rounding and the Hamming
construction of E8 are classical. Prepared by apoursh with substantial Anthropic
Claude (Claude Code) assistance. New work is Apache-2.0.
