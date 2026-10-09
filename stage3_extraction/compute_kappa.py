#!/usr/bin/env python3
"""Cohen's kappa between first coding (extraction.json) and blind second coding
(secondcode_out/batch*.json) for repr_primary, integration, evaluation.
Usage: compute_kappa.py [base] [kappa_out_json]"""
import json, glob, sys, collections

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
OUTF = sys.argv[2] if len(sys.argv) > 2 else f"{BASE}/stage3_extraction/_kappa_disagreements.json"
def prim(v): return v[0] if isinstance(v, list) and v else v
first = {r["arxiv_id"]: r for r in json.load(open(f"{BASE}/stage3_extraction/extraction.json"))
         if r.get("eligible", True)}
second = {}
for f in sorted(glob.glob(f"{BASE}/stage3_extraction/secondcode_out/batch*.json")):
    for r in json.load(open(f)): second[r["arxiv_id"]] = r
def kappa(pairs):
    n = len(pairs); agree = sum(1 for a, b in pairs if a == b); po = agree / n
    ca = collections.Counter(a for a, _ in pairs); cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return ((po - pe) / (1 - pe) if pe < 1 else 1.0), agree, n
# Reliability is PRE-adjudication only: apply_adjudications.py marks every row it touches.
assert not any(r.get("adjudicated") for r in first.values()), \
    "extraction.json is post-adjudication; run merge_extraction.py first (canonical order)"
common = sorted(set(first) & set(second))
print(f"first={len(first)} second={len(second)} common={len(common)}")
dis, res = {}, {"n": len(common)}
for facet, f1 in [("repr_primary", lambda r: prim(r.get("repr_classes")) or r.get("repr_primary")),
                  ("integration", lambda r: r.get("integration")),
                  ("evaluation", lambda r: r.get("evaluation"))]:
    pairs = [(f1(first[i]), f1(second[i])) for i in common]
    k, a, n = kappa(pairs)
    print(f"{facet}: kappa={k:.3f} agree={a}/{n}")
    res[facet] = {"kappa": round(k, 2), "agree": a, "n": n}
    dis[facet] = [{"arxiv_id": i, "system": first[i].get("system"), "first": f1(first[i]),
                   "second": f1(second[i]), "note": (second[i].get("note") or "")[:120]}
                  for i in common if f1(first[i]) != f1(second[i])]
json.dump(dis, open(OUTF, "w"), indent=1)
json.dump(res, open(f"{BASE}/stage3_extraction/_kappa.json", "w"), indent=1)
print("disagreements written to", OUTF)
