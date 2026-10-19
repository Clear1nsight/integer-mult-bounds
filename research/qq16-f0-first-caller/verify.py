"""Source-bound first F0 Gaussian caller inspection.

Clear1nsight, with substantial OpenAI ChatGPT assistance. Apache-2.0.
No full physical caller or multiplication supplier is admitted here.
"""
import gzip
import hashlib
import io
import json
import tarfile
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "20ecf2891d80b5acf18d980b2164fb44ea7faa90"
PINS = {
    "research/joint-query/certificate.json.gz":
        "a5ed85fac5ebf3c091482a113ab0d351eb5a7892fe2841a35e16017ec1ff49f7",
    "research/community-frontier1042-audit/selected-replay.tar.gz":
        "22c3f4dce4b897a1d423d1388801933e288b6a6b1906cb15e1b16a5eb68db754",
}
MEMBERS = {
    "slots/local/CANONICAL-WORD.json.gz":
        "16bc0ebb04b4be6c0ade74badc6a0c0cdba4215eda86e4ff9f13abf8ecebd219",
    "slots/local/CLIFFORD-RECIPES.json":
        "d0768f2164d5f64a2fdbec422f1cfde4e400818792f1904ca541958377243731",
    "slots/local/RESIDUAL-ADAPTERS.json":
        "383f40aadd00a4ac700dfd0d4c22d6c6c0be9a9863116e4d69c7acd23bafae0c",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def load(root=ROOT):
    raw = {}
    for name, sha in PINS.items():
        path = root / name
        need(not path.is_symlink(), "source symlink")
        value = path.read_bytes()
        need(len(value) <= 128 * 1024**2, "source size cap")
        need(hashlib.sha256(value).hexdigest() == sha, "source SHA256: " + name)
        raw[name] = value
    packet = json.loads(gzip.decompress(raw[next(iter(PINS))]))
    objects = []
    with tarfile.open(fileobj=io.BytesIO(raw[list(PINS)[1]]), mode="r:gz") as archive:
        for name, sha in MEMBERS.items():
            records = [m for m in archive.getmembers() if m.name == name]
            need(len(records) == 1 and records[0].isfile(), "unique regular member")
            need(records[0].size <= 64 * 1024**2, "member size cap")
            value = archive.extractfile(records[0]).read()
            need(hashlib.sha256(value).hexdigest() == sha, "member SHA256")
            objects.append(json.loads(gzip.decompress(value) if name.endswith(".gz") else value))
    return packet, *objects


def reg(token):
    kind, index = token
    need(kind in ("L", "C") and type(index) is int, "register token")
    need(0 <= index < (704 if kind == "L" else 8), "register range")
    return index + (704 if kind == "C" else 0)


def ceil_log2_fraction(value):
    need(value > 0, "positive envelope")
    n, d = value.numerator, value.denominator
    result = n.bit_length() - d.bit_length()
    power = Fraction(2**result) if result >= 0 else Fraction(1, 2**(-result))
    return result + (value > power)


def scaled(bound, coefficient):
    magnitude, denominator = bound
    if coefficient == 0 or magnitude == 0:
        return Fraction(0), 0
    d = coefficient.denominator
    need(d > 0 and d & (d-1) == 0, "dyadic scalar")
    return magnitude * abs(coefficient), denominator + d.bit_length() - 1


def added(left, right):
    if left[0] == 0:
        return right
    if right[0] == 0:
        return left
    return left[0] + right[0], max(left[1], right[1])


def inspect(packet, word, recipes, residuals):
    need(packet["programs"]["F_0"][0][:3] == ["retained_core", "forward", 0],
         "F0 retained-core binding")
    children = {(r["old"], r["new"]): r for r in recipes["children"]}
    need(len(children) == len(recipes["children"]), "unique child frames")
    states = [(Fraction(1), 0)] * 704 + [(Fraction(0), 0)] * 8
    events = packet["core_words"]["forward"]
    for index, event in enumerate(events):
        kind = event[0]
        if kind == "climb":
            _, direction, dst, old, new, claimed_rank = event
            child = children[old, new]
            rank = child["rank"]
            need(type(rank) is int and 0 <= rank <= 9, "native rank")
            if rank > 0:
                magnitude, grid = states[dst]
                need(magnitude > 0, "nonzero input envelope")
                return {
                    "source_base": BASE,
                    "event_index": index,
                    "event": event,
                    "prefix_events": events[:index],
                    "prefix_sha256": digest(events[:index]),
                    "recipe": child,
                    "recipe_sha256": digest(child),
                    "target_entry_magnitude_factor": str(magnitude),
                    "target_entry_grid_exponent": grid,
                    "target_initial_frame": word["start"][dst],
                    "first_axis_signed_width_intercept": grid + 4 + ceil_log2_fraction(magnitude),
                    "whole_recipe_width_intercept_at_lambda1": grid + 2*rank + 2 + ceil_log2_fraction(magnitude),
                    "private_fields_proved_zero_at_cut": [i-704 for i in range(704, 712) if states[i][0] == 0],
                    "physical_window_assignment_in_source": "not established by these numerical records",
                }
            need(child["right"] is None, "rank-zero right factor")
        elif kind == "scalar":
            gate = event[1]
            dst = reg(gate[1])
            if gate[0] == "clear":
                need(dst >= 704, "owned private CLEAR")
                states[dst] = Fraction(0), 0
            elif gate[0] == "scale":
                states[dst] = scaled(states[dst], Fraction(gate[2], gate[3]))
            else:
                need(gate[0] == "add", "scalar instruction")
                states[dst] = added(states[dst], scaled(states[reg(gate[2])], Fraction(gate[3], gate[4])))
        else:
            need(kind in ("adapter", "residual_adapter", "phase"), "pre-Gaussian event kind")
    raise ValueError("no positive-rank F0 child")


def main():
    result = inspect(*load())
    print("FIRST_F0_CALLER_SOURCE=" + json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("PASS_QQ16_FIRST_F0_SOURCE_BINDING no_supplier_admission")


if __name__ == "__main__":
    main()
