#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Source-bound sheaf reduction, deliberately separate from supplier admission."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
import gzip
import io
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GEOMETRY_SHA = "79515573d8231a59ece664a2ec421983989c9925e1ccab1ca4c71c7cfa3ea2be"
PINS = {
    "research/centre-block-repair-information/independent.py":
        "b298ff3902c14db11e4ed057259785efc185e8ae3bb39c0d1c432e2340ceb4ea",
    "research/community-frontier1094-audit/selected-replay.tar.gz":
        "f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6",
}


def local_module(name: str, filename: str):
    # Execute the named source bytes directly, ignoring pre-existing bytecode.
    module = types.ModuleType(name)
    module.__file__ = str(HERE / filename)
    exec(compile((HERE / filename).read_bytes(), module.__file__, "exec"), module.__dict__)
    return module


def geometry(root: Path = ROOT):
    for name, expected in PINS.items():
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValueError("missing regular source: " + name)
        if sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("source SHA256 mismatch: " + name)
    name = "research/centre-block-repair-information/independent.py"
    module = types.ModuleType("credited_pr3071_source_extractor")
    module.__file__ = str(root / name)
    exec(compile((root / name).read_bytes(), module.__file__, "exec"), module.__dict__)
    word, phases = module.sources()
    rows, later = module.query_rows(word)
    if later != [[x / 4 for x in row] for row in rows]:
        raise ValueError("source contract H=R/4 fails")
    routes, products, _ = module.route_certificates(word, phases)
    if len(products) != 112 * 111:
        raise ValueError("source route uniqueness")
    for route in routes:
        if len(route) != 73 or any(route[k] != 1 << k for k in range(17, 73)):
            raise ValueError("spectator identity")
        if any(x >> 17 for x in route[:17]):
            raise ValueError("active subspace invariant")
    return rows, [tuple(route[:17]) for route in routes]


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key: " + key)
        out[key] = value
    return out


def strict_equal(actual, expected, at="receipt"):
    if type(actual) is not type(expected):
        raise ValueError("receipt type mismatch: " + at)
    if isinstance(actual, dict):
        if actual.keys() != expected.keys():
            raise ValueError("receipt keys mismatch: " + at)
        for key in actual:
            strict_equal(actual[key], expected[key], at + "." + key)
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            raise ValueError("receipt length mismatch: " + at)
        for i, value in enumerate(actual):
            strict_equal(value, expected[i], at + "[" + str(i) + "]")
    elif actual != expected:
        raise ValueError("receipt value mismatch: " + at)


def parsed_geometry(path):
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 100000:
        raise ValueError("missing, aliased or oversized geometry")
    content = path.read_bytes()
    if path.suffix == ".gz":
        with gzip.GzipFile(fileobj=io.BytesIO(content)) as stream:
            content = stream.read(100001)
        if len(content) > 100000:
            raise ValueError("oversized expanded geometry")
    raw = json.loads(content, object_pairs_hook=unique)
    if set(raw) != {"rows", "routes"}:
        raise ValueError("geometry keys")
    if len(raw["rows"]) != 8 or any(len(row) != 112 for row in raw["rows"]):
        raise ValueError("geometry row dimensions")
    if any(type(x) is not str or str(Q(x)) != x for row in raw["rows"] for x in row):
        raise ValueError("canonical rational geometry")
    if len(raw["routes"]) != 112 or any(len(row) != 17 for row in raw["routes"]):
        raise ValueError("geometry route dimensions")
    if any(type(x) is not int or not 0 <= x < (1 << 17) for row in raw["routes"] for x in row):
        raise ValueError("integer geometry")
    engine = local_module("geometry_digest_engine", "sheaf.py")
    if engine.digest(raw) != GEOMETRY_SHA:
        raise ValueError("derived geometry SHA256 mismatch")
    return [[Q(x) for x in row] for row in raw["rows"]], [tuple(row) for row in raw["routes"]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-geometry", action="store_true")
    parser.add_argument("--geometry", type=Path, help="Check a pinned derived export; this does not rerun archive extraction")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write-receipt", type=Path, help="Create a new receipt exclusively; never overwrite")
    args = parser.parse_args()
    engine = local_module("centre_sheaf_engine", "sheaf.py")
    exported_rows, exported_routes = parsed_geometry(HERE / "GEOMETRY.json.gz")
    if args.geometry:
        rows, routes = parsed_geometry(args.geometry)
        source_mode = "pinned derived geometry; archive extraction not rerun"
    else:
        rows, routes = geometry(args.root)
        source_mode = "authenticated archive and credited PR3071 extractor"
    engine.need(rows == exported_rows and routes == exported_routes, "source/export geometry disagreement")
    engine.need(all(x.denominator == 1 for row in rows for x in row), "integral query matrix")
    if args.emit_geometry:
        print("GEOMETRY_JSON=" + json.dumps({"rows": [[str(x) for x in row] for row in rows], "routes": routes}, separators=(",", ":")))
    result = engine.analyse(rows, routes)
    engine.need(result["owners"] == 4080 and result["ports"] == 112, "source block dimensions")
    if args.write_receipt:
        with args.write_receipt.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, sort_keys=True, indent=2)
            stream.write("\n")
    else:
        expected = json.loads((HERE / "RESULT.json").read_bytes(), object_pairs_hook=unique)
        strict_equal(result, expected)
    print("RESULT_SHA256=" + engine.digest(result))
    print("SOURCE_MODE=" + source_mode)
    print("PASS_CENTRE_SHEAF_FIBRE owners=4080 ports=112 kernel=1 required_observations=424319 no_new_kappa")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError) as error:
        print("FAIL_CENTRE_SHEAF_FIBRE " + str(error), file=sys.stderr)
        raise SystemExit(1) from error
