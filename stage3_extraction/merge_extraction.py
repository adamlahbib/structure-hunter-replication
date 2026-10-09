#!/usr/bin/env python3
"""Study 6: merge extraction chunks -> extraction.json + corpus.jsonl + facet count printout.
Usage: merge_extraction.py [out_base]  (default: the study folder)."""
import json, glob, sys, os, collections

BASE = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else BASE
os.makedirs(f"{OUT}/stage3_extraction", exist_ok=True)

meta = {}
for l in open(f"{BASE}/stage2_screening/candidates.jsonl"):
    r = json.loads(l)
    if r.get("arxiv_id"): meta[r["arxiv_id"]] = r
# rescues not in candidates.jsonl
for l in open(f"{BASE}/stage1_search/identified.jsonl"):
    r = json.loads(l)
    if r.get("arxiv_id") == "2501.18160": meta.setdefault("2501.18160", r)
meta.setdefault("2502.00064", {"title": "Evaluating Large Language Models in Vulnerability Detection Under Variable Context Windows", "authors": ["Jie Lin"]})

# Amendment A1 (2026-08-30, logged in decisions_adjudication.json): author-withdrawn papers whose
# withdrawal notice cites methodological error are demoted E6 (superseded/withdrawn) — their reported
# numbers are disowned by their own authors and cannot carry map claims.
WITHDRAWN = {"2505.17460": "Author-withdrawn on arXiv citing 'fundamental errors in the methodology'; results disowned (Amendment A1)."}

rows, seen = [], set()
for f in sorted(glob.glob(f"{BASE}/stage3_extraction/extraction_chunk*.json")):
    for r in json.load(open(f)):
        aid = r.get("arxiv_id")
        if not aid or aid in seen:
            if aid in seen: print("DUP", aid)
            continue
        seen.add(aid)
        m = meta.get(aid, {})
        r["title"] = m.get("title", r.get("title", ""))
        r["authors"] = m.get("authors", r.get("authors", []))
        if aid in WITHDRAWN:
            r["eligible"] = False
            r["demote_criterion"] = "E6-withdrawn"
            r["demote_reason"] = WITHDRAWN[aid]
        rows.append(r)
rows.sort(key=lambda r: r["arxiv_id"])
eligible = [r for r in rows if r.get("eligible", True)]
json.dump(rows, open(f"{OUT}/stage3_extraction/extraction.json", "w"), indent=1)
with open(f"{OUT}/corpus.jsonl", "w") as f:
    for r in eligible:
        f.write(json.dumps({"arxiv_id": r["arxiv_id"], "system": r.get("system",""), "title": r["title"],
                            "authors": r.get("authors", []), "year": r.get("year"),
                            "venue": r.get("venue","arXiv"), "peer_reviewed": r.get("peer_reviewed", False)}) + "\n")
print(f"total={len(rows)} eligible={len(eligible)} demoted={len(rows)-len(eligible)}")
for r in rows:
    if not r.get("eligible", True):
        print("  DEMOTED:", r["arxiv_id"], r.get("system",""), r.get("demote_criterion"), "-", str(r.get("demote_reason",""))[:90])
def prim(v): return v[0] if isinstance(v, list) and v else v
for facet, listy in [("repr_classes", True), ("integration", False), ("task", False), ("scope", False),
                     ("domain", False), ("evaluation", False), ("wieringa", False), ("record_type", False),
                     ("cross_language", False), ("year", False)]:
    c = collections.Counter()
    for r in eligible:
        v = r.get(facet)
        if listy:
            for x in (v or []): c[x] += 1
        else: c[prim(v)] += 1
    print(f"== {facet} ==", dict(c.most_common()))
c = collections.Counter(prim(r.get("repr_classes")) for r in eligible)
print("== repr_primary ==", dict(c.most_common()))
sg = sum(1 for r in eligible if (r.get("structure_gain") or "none").lower().startswith("none") is False)
print("records reporting a structure-vs-text delta:", sg)
