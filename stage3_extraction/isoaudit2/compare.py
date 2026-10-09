#!/usr/bin/env python3
"""Agreement between the two isolation checkers (A = full-text agents, isoaudit_out; B = GPT, isoaudit2/out).
Prints counts, raw agreement, Cohen's kappa over the four verdicts, and the disagreements."""
import json, glob, os, re, collections
here = os.path.dirname(os.path.abspath(__file__))
A = {r["arxiv_id"]: r for f in sorted(glob.glob(f"{here}/../isoaudit_out/batch*.json")) for r in json.load(open(f))}
B = {}
for f in glob.glob(f"{here}/out/*.json"):
    t = open(f).read().strip()
    if not t: continue
    m = re.search(r"\{.*\}", t, re.S)
    B[os.path.basename(f)[:-5]] = json.loads(m.group(0))
V = ["R-strict", "R-unmatched-budget", "component", "not-isolated"]
ids = [i for i in A if i in B]
pairs = [(A[i]["verdict"], B[i]["verdict"]) for i in ids]
assert all(a in V and b in V for a, b in pairs), pairs
n = len(pairs); po = sum(a == b for a, b in pairs) / n
ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
pe = sum(ca[v] * cb[v] for v in V) / n / n
print(f"n={n}/{len(A)}  agreement={po:.3f}  kappa={(po - pe) / (1 - pe):.3f}")
print("A:", dict(ca)); print("B:", dict(cb))
for i in ids:
    if A[i]["verdict"] != B[i]["verdict"]:
        print(f"- {i} {A[i]['system']}: A={A[i]['verdict']} B={B[i]['verdict']}")
