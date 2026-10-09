#!/usr/bin/env python3
"""tally verify_out batches -> verification.json + verification_summary.md +
_needs_adjudication.json. Usage: summarize_verification.py [verify_out_dir] [out_dir]"""
import json, glob, sys

VD = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))) + "/stage3_extraction/verify_out"
OUT = sys.argv[2] if len(sys.argv) > 2 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))) + "/stage3_extraction"
out, needs = [], []
tot = {"CONFIRMED": 0, "WRONG": 0, "UNRETRIEVABLE": 0}
fa = {"repr_agree": 0, "repr_dis": 0, "integ_agree": 0, "integ_dis": 0, "eval_agree": 0, "eval_dis": 0,
      "stop_fair": 0, "stop_unfair": 0}
for f in sorted(glob.glob(f"{VD}/batch*.json")):
    for r in json.load(open(f)):
        out.append(r)
        for n in r.get("numbers", []):
            v = (n.get("verdict") or "").upper()
            tot[v] = tot.get(v, 0) + 1
            if v == "WRONG":
                needs.append({"arxiv_id": r["arxiv_id"], "kind": "number", "metric": n.get("metric"),
                              "correct": n.get("correct_value_if_wrong"), "note": n.get("note", "")})
        for k, sug in (("repr_primary", "repr"), ("integration", "integ"), ("evaluation", "eval")):
            ag = r.get(f"{k}_agree", True)
            fa[f"{sug}_agree" if ag else f"{sug}_dis"] += 1
            if not ag:
                needs.append({"arxiv_id": r["arxiv_id"], "kind": k,
                              "suggested": r.get(f"{k}_suggested"), "note": (r.get("note") or "")[:200]})
        fa["stop_fair" if r.get("stop_detail_fair", True) else "stop_unfair"] += 1
json.dump(out, open(f"{OUT}/verification.json", "w"), indent=1)
json.dump(needs, open(f"{OUT}/_needs_adjudication.json", "w"), indent=1)
nch = sum(tot.values()); retr = tot["CONFIRMED"] + tot["WRONG"]
md = f"""# Stage 3 — Independent Verification Summary

Records verified: {len(out)}. Key numbers checked: {nch}.
- CONFIRMED: {tot['CONFIRMED']} ({100*tot['CONFIRMED']/nch:.1f}% of checked; {100*tot['CONFIRMED']/retr:.1f}% of retrievable)
- WRONG: {tot['WRONG']} (corrections via author adjudication; see _needs_adjudication.json + corrections log)
- UNRETRIEVABLE: {tot['UNRETRIEVABLE']}

Facet spot-check by verifiers (non-blind; the blind second coding is reported separately):
- repr_primary: {fa['repr_agree']} agree / {fa['repr_dis']} disagree
- integration: {fa['integ_agree']} agree / {fa['integ_dis']} disagree
- evaluation: {fa['eval_agree']} agree / {fa['eval_dis']} disagree
- stop_detail fair paraphrase: {fa['stop_fair']} fair / {fa['stop_unfair']} flagged
"""
open(f"{OUT}/verification_summary.md", "w").write(md)
print(md)
