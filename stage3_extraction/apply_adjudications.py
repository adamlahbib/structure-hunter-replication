#!/usr/bin/env python3
"""author adjudication of the verification pass + blind-second-coder disagreements.
Applies accepted corrections onto extraction.json. Decisions and rationale in corrections_log.md.
Run order: merge_extraction.py -> apply_adjudications.py -> summarize_verification.py -> make_map.py.
Usage: apply_adjudications.py [base]"""
import json, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
P = f"{BASE}/stage3_extraction/extraction.json"
rows = json.load(open(P))
by = {r["arxiv_id"]: r for r in rows}

def fix_num(aid, metric_sub, value=None, where=None):
    r = by[aid]
    for n in r.get("key_numbers", []):
        if metric_sub.lower() in n["metric"].lower():
            if value: n["value"] = value
            if where: n["where"] = where
            return
    raise KeyError(f"{aid}: no key_number matching '{metric_sub}'")

def fix_gain(aid, text):
    by[aid]["structure_gain"] = text

# ---- 1. Number + structure_gain corrections (17 WRONG verdicts, all accepted)
fix_num("2504.16877", "API-abstraction", value="69.09% vs 60.89% (+8.20pp)", where="Table 4")
fix_gain("2504.16877", "A3 API-context vs w/o-API: F1 69.09% vs 60.89% (+8.20pp), same model (Table 4).")
fix_num("2510.02534", "F1 gain, optimized vs minimal-context", value="+0.176 average across the 10 models (OpenVuln)", where="Table 4")
fix_gain("2510.02534", "Optimized vs minimal-context prompt: average F1 +0.176 across 10 models (OpenVuln, Table 4), same models.")
fix_num("2601.18847", "retrieval ablation", value="34.56% -> 21.80% Macro-F1 without retrieval (-12.76pp)", where="ablation table")
fix_gain("2601.18847", "Removing retrieval: Macro-F1 34.56% -> 21.80% (-12.76pp), same model (the -30.70 figure belongs to the GPT-4o baseline row).")
fix_num("2501.18160", "validator ablation", value="78.43% with validator vs 51.28% without (40TP/38FP)", where="Table 6")
fix_gain("2501.18160", "Ablations, same agent: no-abstraction precision 40.38% (21TP/31FP) and no-validator 51.28% (40TP/38FP) vs full RepoAudit 78.43% (Table 6).")
fix_num("2512.07533", "C/C++ F1", value="Figure-derived aggregates only: All-data F1 ~0.71->~0.78, OOD-CWE F1 ~0.58->~0.81 with reasoning-chain training (no C/C++ breakdown exists)", where="Figure 5 (bar chart; figure-derived)")
fix_gain("2512.07533", "None representation-specific: the Figure 5 ablation varies reasoning-chain training, not program representation (figure-derived aggregates All ~0.71->0.78, OOD ~0.58->0.81).")
fix_num("2604.20179", "confirmation rate", value="83.75% (433/517) vs Explode.js File mode 43.13% (223/517); Pkg mode is 11.80% (61/517)", where="evaluation table")
fix_num("2403.19096", "F1 on Reveal", value="62.85% (SCALE) vs 56.04% best baseline (UniXcoder; CodeBERT 49.10% is the worst, not best, baseline)")
fix_gain("2602.06751", "Reported +11.13pp (56.65%->67.78%) compares UniXcoder (encoder classifier) vs fine-tuned Qwen2.5-32B — different architectures, so the gain is NOT representation-isolated; fine-tuning-budget equality is unsubstantiated.")
fix_gain("2607.21983", "+13.33pp / +10.0pp deltas correct, but same-model/config constancy is not substantiated (settings 'not recorded') and complete-contract inputs are far longer than slices — unequal context budget.")
fix_num("2506.10322", "False positive filter rate", value="FPR_P 0.98-1.0 per bug type (NPD 0.98, BOF 1.0, UAF 1.0); the 72-96% range describes FPR_R, a different metric", where="Table 1")
fix_num("2605.01885", "recall", value="87.1% vs standalone Semgrep 90.0% (-2.9pp; the paper's '3.2%' is the relative reduction)")
fix_gain("2605.01885", "Precision 95.1% vs 69.5% (confirmed); recall 87.1% vs 90.0% = -2.9pp (relative -3.2%).")

# ---- 1b. Extraction errors found by the isolation re-audit (amendment A2, 2026-10-09; full text, pinned version)
fix_num("2607.01138", "Ablation recall", value="Opus 4.7: 20 vs 13 vs 11; GPT-5.4: 14 vs 9 vs 8 (of 35 CVEs)", where="v2 Table 4")
fix_num("2607.01138", "True positives", value="20/35 TP (Claude Opus 4.7)", where="v2 Table 2")
fix_gain("2607.01138", "Removing either context source cuts true-positive detections at a fixed backbone (v2, 35 CVEs: Opus 20->13/11; GPT-5.4 14->9/8; Table 4). Extraction originally matched superseded v1 (28 CVEs).")
fix_gain("2507.16585", "Appendix C same-model slicing ablation: slice-based vs full-code ACCURACY 0.8146 vs 0.6762 (FormAI), 0.7250 vs 0.4875 (PrimeVul), 0.6020 vs 0.5078 (SVEN); model fine-tuned on slices, so the gap is an upper bound on the representation effect.")
fix_num("2607.29422", "Context-facet ablation", value="w/o code-structure 73.5% (-1.5pp), w/o execution 74.5% (-0.5pp), w/o commit-history 73.0% (-2.0pp) vs 75.0%", where="Table II")
fix_gain("2607.29422", "Removing one context facet (each produced by a separate tool-using subagent) costs 0.5-2.0pp (75.0% -> 73.5/74.5/73.0%), 1-4 of 200 instances, single run at temperature 1.0; single-agent scaffold costs 44.5pp.")
fix_gain("2512.04106", "Equal-shot comparison: 10-shot retrieval-augmented vs random examples, F1 71.43% vs 65.69% (+5.74pp), same Gemini-1.5-Flash (Sec. V-B). The zero-shot vs 20-shot pair (36.35% -> 74.05%) also changes the amount of context.")
fix_gain("2510.02534", "Optimized vs minimal-context prompt: F1 gain averaged over the 10 models in Table 4 = +0.176 (our computation; the paper reports per-model values only). Same models.")
by["2601.10865"]["confound_note"] = by["2601.10865"]["confound_note"].replace("GPT-4 vs GPT-4-mi", "GPT-5 vs GPT-5-mi")
assert "GPT-5 vs GPT-5-mi" in by["2601.10865"]["confound_note"]
fix_gain("2601.10865", "LLM-derived taint specifications for CodeQL raise recall from 0% (stock CodeQL) to 65.43% (106/162); RQ3 apportions catches (testing split): 76.4% needed only custom sources/sinks, 23.6% also the repaired call graph. CodeQL, not the LLM, performs detection.")
fix_gain("2501.18160", "Same-agent ablations: no-validator 40TP/38FP (precision 51.28%, our computation from Table 6) and no-abstraction 40.38% (21TP/31FP) vs full 78.43% (40TP/11FP).")

A2_FIXED = ["2607.01138", "2507.16585", "2607.29422", "2512.04106", "2510.02534", "2601.10865", "2501.18160"]
for aid in A2_FIXED: by[aid]["a2_extraction_error"] = True

# Inconsistencies INSIDE primary studies (not extraction errors): recorded, numbers taken from the tables.
SRC = {
    "2501.18160": "Text says no-validator FPs 'increase to 31'; Table 6 and its +245.45% give 38.",
    "2508.13092": "Abstract reports F1 0.54 and gain 0.27; Table 2 gives 0.57; conclusion gives gain 0.25.",
    "2403.19096": "Several F1 differences quoted in the text do not match Tables 4 and 6 (e.g., SVulD SCTC 1.95 vs stated 2.04).",
    "2409.18395": "Text and Table I disagree on the 20% and 31% repair figures.",
    "2504.16057": "DSL100 pass rate is 50.0% in Table 7 but 49.1% in the text.",
    "2403.06838": "Text says the ACG 'contributed to 12 more successful cases'; Table IV gives 112 - 106 = 6.",
}
for aid, note in SRC.items(): by[aid]["source_inconsistency"] = note

# ---- 2. Facet recodes (verifier full-text evidence, all accepted)
def set_facet(aid, **kw):
    r = by[aid]
    for k, v in kw.items():
        if k == "repr_primary":
            rc = r.get("repr_classes") or []
            r["repr_classes"] = [v] + [x for x in rc if x != v]
        else:
            r[k] = v

set_facet("2509.15433", repr_primary="hybrid", integration="finetune_adapter")
set_facet("2601.10865", repr_primary="taint_path")
set_facet("2604.08417", repr_primary="interproc_callgraph")
set_facet("2605.04251", repr_primary="hybrid")
set_facet("2607.01138", repr_primary="hybrid")
set_facet("2409.18395", repr_primary="nl_structured")
set_facet("2505.17416", integration="retrieval_guide")
set_facet("2604.17948", integration="retrieval_guide")
set_facet("2605.09461", integration="prompt_serialization")
# evaluation — strict representation-only rule (same model, same budget, representation varied):
# downgrades (isolation claim fails the rule)
for aid in ("2602.06751", "2607.21983", "2503.03586"):
    set_facet(aid, evaluation="ablated_measured")
# 2512.07533: verifier suggested not_evaluated; adjudicated to ablated_measured — the paper HAS
# quantified baseline comparisons; only the representation-isolation claim fails.
set_facet("2512.07533", evaluation="ablated_measured")
# upgrades (verifier found genuine same-model representation ablations the extractor missed)
for aid in ("2406.11147", "2507.16585"):
    set_facet(aid, evaluation="representation_only_ablation")
fix_gain("2507.16585", "Appendix C same-model slicing ablation: slice-based vs full-code F1 0.8146 vs 0.6762 (FormAI), 0.7250 vs 0.4875 (PrimeVul), 0.6020 vs 0.5078 (SVEN) — the extractor's claim that these were 'not detailed' was wrong.")

# ---- 3. Isolation re-audit (amendment A2, 2026-10-09; reviewer request). Every record coded
# representation_only_ablation was re-judged at full text by two independent checkers (Claude agents; GPT)
# under a sharper rule; disagreements decided by the authors. The old level splits into four.
LEVEL = {"R-strict": "repr_strict", "R-unmatched-budget": "repr_unmatched_budget",
         "component": "component_ablation", "not-isolated": "ablated_measured"}
audit = json.load(open(f"{BASE}/stage3_extraction/isoaudit_final.json"))
assert {a["arxiv_id"] for a in audit} == {r["arxiv_id"] for r in rows if r.get("eligible", True)
                                          and r.get("evaluation") == "representation_only_ablation"}
for a in audit:
    by[a["arxiv_id"]]["evaluation"] = LEVEL[a["verdict"]]
    by[a["arxiv_id"]]["isolation_audit"] = a

for r in rows: r["adjudicated"] = True  # compute_kappa.py refuses post-adjudication data
json.dump(rows, open(P, "w"), indent=1)
print("adjudications applied:", len(rows), "records")
