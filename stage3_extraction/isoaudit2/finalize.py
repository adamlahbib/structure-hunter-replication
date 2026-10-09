#!/usr/bin/env python3
"""Final isolation verdicts: checker A (full-text agents) and checker B (GPT) agree -> that verdict;
disagree -> the authors' decision in human_decisions.json ({arxiv_id: {"verdict", "reason"}}).
Writes ../isoaudit_final.json, consumed by apply_adjudications.py. Fails if any disagreement is undecided."""
import json, glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
A = [r for f in sorted(glob.glob(f"{here}/../isoaudit_out/batch*.json")) for r in json.load(open(f))]
B = {os.path.basename(f)[:-5]: json.loads(re.search(r"\{.*\}", open(f).read(), re.S).group(0))
     for f in glob.glob(f"{here}/out/*.json") if open(f).read().strip()}
H = json.load(open(f"{here}/human_decisions.json")) if os.path.exists(f"{here}/human_decisions.json") else {}
# strict comparisons that vary something other than program structure (query-language spec; obfuscation)
NOT_STRUCT = {"2504.16057", "2512.16538"}
out, missing = [], []
for a in A:
    i = a["arxiv_id"]; b = B.get(i)
    assert b, f"no checker-B verdict for {i}"
    if a["verdict"] == b["verdict"]:
        v, by = a["verdict"], "both checkers"
    elif i in H:
        v, by = H[i]["verdict"], "authors (checkers disagreed)"
    else:
        missing.append(i); continue
    src = b if (i in H and v == b["verdict"]) else a   # describe the comparison the final verdict judged
    out.append({k: src.get(k) or a.get(k) for k in ("arxiv_id", "system", "source_checked", "comparison", "model_config",
                                      "dataset_metric", "budget_control", "arm_a", "arm_b", "other_changes", "delta")}
               | {"verdict": v, "verdict_A": a["verdict"], "verdict_B": b["verdict"], "decided_by": by,
                  "rationale": a.get("rationale"), "human_reason": H.get(i, {}).get("reason"),
                  "not_program_structure": i in NOT_STRUCT})
assert not missing, f"undecided disagreements: {missing}"
json.dump(out, open(f"{here}/../isoaudit_final.json", "w"), indent=1)
print(f"isoaudit_final.json: {len(out)} records, {sum(o['decided_by'] != 'both checkers' for o in out)} decided by authors")
