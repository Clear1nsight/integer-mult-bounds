# Executed evidence and publication boundary

## Source-dependent executions

The first scientific commit was 4c0ef119c6bad986ff633ecf1cfa8ebdf661755d.
Fork workflow 39165088786 passed both planning and registered replay on
Ubuntu 24.04.5 with CPython 3.12.15. Its preview merge was
2bb95b0a53878f77dec929df0e38d596318fe589. The primary actual-archive normal and
-O runs agreed on every field of their printed deterministic result. The
original inputs remained unchanged.

The second scientific commit was 403ef45de40e41baaf8b1f4cfddaf3ba1d57af1c.
Fork workflow 39165978787 passed planning and registered replay. Its preview
merge was 999cf40941895bf98dcc5c8978a7c834aea3957d. Both primary and separate
independent actual-archive implementations passed normally and under -O.
The independent source mode was 'independently parsed pinned archive', not
the derived-geometry fallback. The source geometry hashes agree exactly.

- First run: https://github.com/Clear1nsight/integer-mult-bounds/actions/runs/39165088786
- Separate reconstruction: https://github.com/Clear1nsight/integer-mult-bounds/actions/runs/39165978787

The final packaging commit adds the frozen geometry and receipt, strict
comparisons, local CLI controls, and completed proof text. Its own CI status
is reported separately on the PR after execution, rather than predicted here.

## Local execution

The isolated container has CPython 3.13.5 and no network DNS access. It could
not retrieve the original selected archive. The geometry emitted by the
first authenticated source run was retained locally and checked against its
complete canonical hash. Local normal/-O arithmetic checks with both engines
agree, as do eight generic tests and seven rejecting CLI controls plus one
semantic additional-kernel control. A separate local test checked 900 binary
row/column matrix products at dimensions 1 through 9 with seed 31473656.
That extra random test is local corroboration, not the source theorem.

## Immutable mathematical comparison

Parsed geometry SHA256:

    79515573d8231a59ece664a2ec421983989c9925e1ccab1ca4c71c7cfa3ea2be

Canonical scientific result SHA256, excluding runtime source-mode labels:

    ce517d8e5e33222ce1456591436bb74690a9cee82f98dc9194b0c381b4a2ef57

Both default source engines reconstruct the geometry; offline runs explicitly
label that source extraction was not rerun. Gzip stream bytes are not used as
a mathematical equality condition. Source-archive bytes remain exactly pinned.

## Publication and unrun obligations

Fork PR https://github.com/Clear1nsight/integer-mult-bounds/pull/1 was created
against review/centre-sheaf-base, exactly canonical main20ecf2891d80b5acf18d980b2164fb44ea7faa90.
The fork's older main was deliberately left unchanged. Upstream claim-comment
and PR attempts both returned HTTP403 'Resource not accessible by integration'.
No upstream publication or claim release is represented as successful.

No native payload replay, physical supplier, full selected cold replay,
formal proof-kernel check, independent human acceptance, or new kappa is
claimed. The primary shares PR3071's extractor; the second does not. Both
implementations and the proof were produced in the same assisted session.
