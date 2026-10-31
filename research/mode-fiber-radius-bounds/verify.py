#!/usr/bin/env python3
"""Exact checks for the mode-fiber rounding radius bounds. Standard library only.

Checks, in exact integer/rational arithmetic, every finite fact the proof uses:
the mode matrix structure, L = M^T Z^112 = {x : x mod 2 in H8}, the genericity
hypothesis, the PR6312 lower-bound witness, the tau = 6 basis certificate, and
the subset-sum witnesses recorded in SEARCH.json. Rejection controls follow.
Prepared for apoursh with substantial Anthropic Claude assistance. Apache-2.0.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'research/coded-native-caller/NORMALIZERS.json'
SOURCE_SHA256 = 'ae8aad06aa5d1811d725895b3ab5a4f4daa9dcdd88294aa0d5f723e78bb1e0da'
WITNESS_SUPPORT, WITNESS_TARGET = (0, 7, 20, 111), 48


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path, limit=1 << 20):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit, 'bounded regular file: %s' % path)
    return path.read_bytes()


def load_rows(raw):
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, 'source hash')
    cols = json.loads(raw)['mode_columns']
    need(type(cols) is list and len(cols) == 8 and all(len(c) == 112 for c in cols), 'mode shape')
    rows = [tuple(c[i] for c in cols) for i in range(112)]
    need(all(type(v) is int and v in (-1, 0, 1) for r in rows for v in r), 'signed entries')
    return rows


def hnf(vectors):
    """Row-style Hermite normal form of the integer lattice spanned by vectors (dimension 8)."""
    rows, out = [list(v) for v in vectors], []
    for c in range(8):
        while True:
            piv = [r for r in rows if r[c]]
            if len(piv) <= 1:
                break
            piv.sort(key=lambda r: abs(r[c]))
            for r in piv[1:]:
                q = r[c] // piv[0][c]
                r[:] = [a - q * b for a, b in zip(r, piv[0])]
        if piv:
            p = piv[0]
            rows.remove(p)
            out.append([-v for v in p] if p[c] < 0 else p)
    for i in range(len(out)):
        for k in range(i):
            q = out[k][i] // out[i][i]
            out[k] = [a - q * b for a, b in zip(out[k], out[i])]
    return out


def rank(vectors):
    rows, r = [[Q(v) for v in vec] for vec in vectors], 0
    for c in range(len(rows[0]) if rows else 0):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def solve(columns, target):
    """Solve sum_k x_k columns[k] = target exactly for square nonsingular columns."""
    n = len(columns)
    a = [[Q(columns[k][j]) for k in range(n)] + [Q(target[j])] for j in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if a[i][c])
        a[c], a[piv] = a[piv], a[c]
        for i in range(n):
            if i != c and a[i][c]:
                f = a[i][c] / a[c][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def det(columns):
    n, d = len(columns), Q(1)
    a = [[Q(columns[k][j]) for k in range(n)] for j in range(n)]
    for c in range(n):
        piv = next((i for i in range(c, n) if a[i][c]), None)
        if piv is None:
            return Q(0)
        if piv != c:
            a[c], a[piv], d = a[piv], a[c], -d
        d *= a[c][c]
        for i in range(c + 1, n):
            f = a[i][c] / a[c][c]
            a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return d


def hamming_code(rows):
    supports = {tuple(int(v != 0) for v in r) for r in rows}
    code = supports | {(0,) * 8, (1,) * 8}
    need(all(tuple(x ^ y for x, y in zip(a, b)) in code for a in code for b in code), 'linear code')
    return supports, code


def in_lattice(t, code):
    return all(type(v) is int for v in t) and tuple(v % 2 for v in t) in code


def check_structure(rows):
    need(len(set(rows)) == 112 and all(sum(map(abs, r)) == 4 for r in rows), 'distinct weight-four rows')
    gram = [[sum(r[a] * r[b] for r in rows) for b in range(8)] for a in range(8)]
    need(gram == [[56 * (a == b) for b in range(8)] for a in range(8)], 'M^T M = 56 I')
    supports, code = hamming_code(rows)
    need(len(supports) == 14 and len(code) == 16, 'supports are the 14 weight-four words of [8,4,4]')
    need(all(sum(tuple(int(v != 0) for v in r) == s for r in rows) == 8 for s in supports), 'eight rows per support')
    negation_closed = all(tuple(-v for v in r) in set(rows) for r in rows)
    generators = [list(c) for c in code] + [[2 * (j == k) for j in range(8)] for k in range(8)]
    lattice = hnf(rows)
    need(lattice == hnf(generators), 'L equals the Hamming construction {x : x mod 2 in H8}')
    index = 1
    for i, r in enumerate(lattice):
        index *= r[i]
    need(index == 16, 'index of L in Z^8')
    need(all(rank(rows[:i] + rows[i + 1:]) == 8 for i in range(112)), 'no coordinate is constant on ker M^T')
    return code, negation_closed


def check_witness(rows):
    # PR6312 lower bound: x = (e_0 + e_7 + e_20 + e_111)/2 has the modes of e_48 (radius-one fiber).
    half = [sum(Q(rows[i][j], 2) for i in WITNESS_SUPPORT) for j in range(8)]
    need(half == [Q(v) for v in rows[WITNESS_TARGET]], 'PR6312 witness relation')


def check_basis(rows, certificate):
    basis, tau = certificate['basis_rows'], certificate['tau']
    need(len(set(basis)) == 8 and all(0 <= b < 112 for b in basis), 'eight distinct basis rows')
    cols = [rows[b] for b in basis]
    need(abs(det(cols)) == 16, 'basis covolume equals covolume of L')
    worst = 0
    for i in range(112):
        if i in basis:
            continue
        w = solve(cols, rows[i])
        need(all(x.denominator == 1 for x in w), 'integral coordinates in the basis')
        worst = max(worst, sum(abs(x) for x in w))
    need(worst == tau, 'maximum column l1 norm equals the certified tau')
    return tau


def check_search(rows, code, search):
    need(search['schema'] == 'mode-fiber-subset-sum-evidence-v1', 'search schema')
    faces = {}
    for t, face_rank, q, mask in search['records']:
        need(in_lattice(t, code), 'search target lies in L')
        z = int(mask, 16)
        need(0 <= z < 1 << 112, 'mask range')
        total = [sum(rows[i][j] for i in range(112) if z >> i & 1) for j in range(8)]
        need(total == t, 'subset-sum witness')
        faces[face_rank] = faces.get(face_rank, 0) + 1
    return len(search['records']), dict(sorted(faces.items()))


def rejects(function, *args):
    try:
        function(*args)
    except (ValueError, StopIteration, ZeroDivisionError):
        return True
    return False


def controls(rows, code, certificate, search):
    flipped = [list(r) for r in rows]
    flipped[3][0] = -flipped[3][0]
    repeated = {**certificate, 'basis_rows': certificate['basis_rows'][:7] + [certificate['basis_rows'][0]]}
    stronger = {**certificate, 'tau': certificate['tau'] - 1}
    non_basis = {**certificate, 'basis_rows': list(range(8))}
    t, f, q, mask = search['records'][0]
    wrong_sum = {**search, 'records': [[t, f, q, format(int(mask, 16) ^ 1, '028x')]]}
    off_lattice = {**search, 'records': [[[t[0] + 1] + t[1:], f, q, mask]]}
    results = [
        rejects(check_structure, [tuple(r) for r in flipped]),
        rejects(check_basis, rows, repeated),
        rejects(check_basis, rows, stronger),
        rejects(check_basis, rows, non_basis),
        rejects(check_search, rows, code, wrong_sum),
        rejects(check_search, rows, code, off_lattice),
        rejects(check_witness, rows[:48] + [rows[49]] + rows[49:]),
    ]
    need(all(results), 'every rejection control must fail closed: %s' % results)
    return len(results)


def main():
    rows = load_rows(read(ROOT / SOURCE))
    code, negation_closed = check_structure(rows)
    check_witness(rows)
    certificate = json.loads(read(HERE / 'CERTIFICATE.json'))
    tau = check_basis(rows, certificate)
    search = json.loads(read(HERE / 'SEARCH.json'))
    count, faces = check_search(rows, code, search)
    n_controls = controls(rows, code, certificate, search)
    print(json.dumps({
        'lattice': 'L = M^T Z^112 = {x in Z^8 : x mod 2 in H8}, index 16',
        'rows_negation_closed': negation_closed,
        'lower_bound': 1, 'upper_bound': tau,
        'subset_sum_witnesses': count, 'witnesses_by_face_rank': faces,
        'rejection_controls': n_controls,
        'scope': 'Exact finite checks only; the reduction and Beck-Fiala arguments are in PROOF.md. '
                 'Interiority of search targets is not certified.'}, indent=1))
    print('PASS_MODE_FIBER_RADIUS_BOUNDS')


if __name__ == '__main__':
    main()
