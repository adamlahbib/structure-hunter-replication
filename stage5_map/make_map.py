#!/usr/bin/env python3
"""Study 6 stage 5: derive ALL map statistics from extraction.json -> _map_stats.json +
systematic_map.md. Usage: make_map.py [base_with_extraction] [out_base]."""
import json, sys, os, collections

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
OUT = sys.argv[2] if len(sys.argv) > 2 else BASE
os.makedirs(f"{OUT}/stage5_map", exist_ok=True)
rows = [r for r in json.load(open(f"{BASE}/stage3_extraction/extraction.json")) if r.get("eligible", True)]
N = len(rows)
def prim(v): return v[0] if isinstance(v, list) and v else v

stats = {"N": N}
def cnt(name, fn, multi=False):
    c = collections.Counter()
    for r in rows:
        v = fn(r)
        if multi:
            for x in (v or []): c[x] += 1
        else: c[v] += 1
    stats[name] = dict(c.most_common()); return c

cnt("repr_primary", lambda r: prim(r.get("repr_classes")))
cnt("repr_any", lambda r: r.get("repr_classes"), multi=True)
cnt("integration", lambda r: r.get("integration"))
cnt("task", lambda r: r.get("task"))
cnt("scope", lambda r: r.get("scope"))
cnt("domain", lambda r: r.get("domain"))
cnt("evaluation", lambda r: r.get("evaluation"))
cnt("wieringa", lambda r: r.get("wieringa"))
cnt("record_type", lambda r: r.get("record_type"))
cnt("cross_language", lambda r: bool(r.get("cross_language")))
cnt("year", lambda r: r.get("year"))
cnt("peer_reviewed", lambda r: bool(r.get("peer_reviewed")))

xt = collections.defaultdict(collections.Counter)
for r in rows: xt[prim(r.get("repr_classes"))][r.get("task")] += 1
stats["repr_x_task"] = {k: dict(v) for k, v in xt.items()}
xt2 = collections.defaultdict(collections.Counter)
for r in rows: xt2[prim(r.get("repr_classes"))][r.get("evaluation")] += 1
stats["repr_x_eval"] = {k: dict(v) for k, v in xt2.items()}
ISO_LEVELS = ("repr_strict", "repr_unmatched_budget", "component_ablation")
iso = [r for r in rows if r.get("evaluation") == "repr_strict"]
stats["isolation_audit"] = [dict(r["isolation_audit"], system=r.get("system"), evaluation=r["evaluation"],
                                 repr=prim(r.get("repr_classes")), scope=r.get("scope"), task=r.get("task"))
                            for r in rows if r.get("isolation_audit")]
stats["n_isolation_audited"] = len(stats["isolation_audit"])
stats["n_same_model_comparison"] = sum(r.get("evaluation") in ISO_LEVELS for r in rows)
stats["isolation_records"] = [{"id": r["arxiv_id"], "system": r.get("system"),
                               "structure_gain": r.get("structure_gain",""),
                               "confound_note": r.get("confound_note","")} for r in iso]
stats["n_isolation"] = len(iso)
sg = [r for r in rows if not (r.get("structure_gain") or "none").lower().startswith("none")]
stats["n_structure_gain_reported"] = len(sg)
# peer-reviewed vs preprint profile (threats: external validity of a preprint-heavy corpus)
for facet in ("evaluation", "wieringa", "scope", "task"):
    t = collections.defaultdict(collections.Counter)
    for r in rows: t["peer" if r.get("peer_reviewed") else "preprint"][r.get(facet)] += 1
    stats[f"pr_x_{facet}"] = {k: dict(v) for k, v in t.items()}

# isolation audit: two independent full-text checkers + author decisions on disagreements
aud = [r["isolation_audit"] for r in rows if r.get("isolation_audit")]
V = ("R-strict", "R-unmatched-budget", "component", "not-isolated")
pa = [(a["verdict_A"], a["verdict_B"]) for a in aud]; n = len(pa)
po = sum(x == y for x, y in pa) / n
pe = sum(sum(x == v for x, _ in pa) * sum(y == v for _, y in pa) for v in V) / n / n
stats["isoaudit"] = {"n": n, "agree": sum(x == y for x, y in pa), "kappa": round((po - pe) / (1 - pe), 2),
                     "decided_by_authors": sum(a["decided_by"] != "both checkers" for a in aud),
                     "strict_A": sum(x == "R-strict" for x, _ in pa), "strict_B": sum(y == "R-strict" for _, y in pa),
                     "strict_not_program_structure": sum(a["not_program_structure"] and a["verdict"] == "R-strict" for a in aud),
                     "strict_program_structure": sum(not a["not_program_structure"] and a["verdict"] == "R-strict" for a in aud),
                     "survived": sum(a["verdict"] == "R-strict" for a in aud),
                     "final_not_isolated": sum(a["verdict"] == "not-isolated" for a in aud),
                     "not_audited": N - len(aud),
                     "extra_extraction_errors": sum(bool(r.get("a2_extraction_error")) for r in rows),
                     "n_source_inconsistency": sum(bool(r.get("source_inconsistency")) for r in rows)}
stats["n_peer_strict"] = sum(1 for r in rows if r.get("peer_reviewed") and r.get("evaluation") == "repr_strict")

# bounded backward-snowballing check (deviation D1): references of the audited studies, screened on title+abstract
sc = json.load(open(f"{BASE}/stage1_search/_snowball_check.json"))
scr = json.load(open(f"{BASE}/stage1_search/_snowball_screen.json"))
corpus_ids = {r["arxiv_id"] for r in rows}
new = [x for x in scr if not any(i in (x.get("source_id") or "") for i in corpus_ids)]
stats["snowball"] = {"papers": len(sc["papers"]), "resolved": sum(p["n_refs"] is not None for p in sc["papers"]),
                     "refs": sum(p["n_refs"] or 0 for p in sc["papers"]), "flagged": len(scr),
                     "already_in_corpus": len(scr) - len(new),
                     "include": sum(x["decision"] == "include" for x in new),
                     "uncertain": sum(x["decision"] == "uncertain" for x in new),
                     "exclude": sum(x["decision"] == "exclude" for x in new),
                     "include_doi_only": sum(x["decision"] == "include" and "arXiv" not in (x.get("source_id") or "") for x in new)}

nl = lambda f: sum(1 for l in open(f) if l.strip())
stats["funnel"] = {"identified": nl(f"{BASE}/stage1_search/identified.jsonl"), "prefilter_pass": nl(f"{BASE}/stage2_screening/candidates.jsonl"),
                   "extracted": len(json.load(open(f"{BASE}/stage3_extraction/extraction.json")))}
stats["funnel"]["demoted"] = stats["funnel"]["extracted"] - N

# ---- method facts, each derived from its own source file (no hand-copied numbers)
import glob
S3 = f"{BASE}/stage3_extraction"
ver = json.load(open(f"{S3}/verification.json"))
verdicts = [n.get("verdict") for v in ver for n in v.get("numbers", [])]
vc = collections.Counter(verdicts)
stats["verification"] = {"records": len(ver), "claims": len(verdicts), "confirmed": vc.get("CONFIRMED", 0),
                         "wrong": vc.get("WRONG", 0), "unretrievable": vc.get("UNRETRIEVABLE", 0),
                         "pct_confirmed": round(100 * vc.get("CONFIRMED", 0) / len(verdicts), 1)}
stats["kappa_coding"] = json.load(open(f"{S3}/_kappa.json"))
S2 = f"{BASE}/stage2_screening"
first = {d["id"]: d["decision"] for f in glob.glob(f"{S2}/decisions_chunk*.json") for d in json.load(open(f))}
dual = [(first[d["id"]], d["decision"]) for d in json.load(open(f"{S2}/decisions_dual.json")) if d["id"] in first]
bp = [(a == "include", b == "include") for a, b in dual]
po = sum(a == b for a, b in bp) / len(bp)
pe = sum(sum(a == k for a, _ in bp) * sum(b == k for _, b in bp) for k in (True, False)) / len(bp) ** 2
L3 = ("include", "exclude", "uncertain"); po3 = sum(a == b for a, b in dual) / len(dual)
pe3 = sum(sum(a == k for a, _ in dual) * sum(b == k for _, b in dual) for k in L3) / len(dual) ** 2
stats["screening_dual"] = {"n": len(dual), "agree": sum(a == b for a, b in bp), "kappa": round((po - pe) / (1 - pe), 2),
                           "kappa_3way": round((po3 - pe3) / (1 - pe3), 2),
                           "include_vs_exclude_flips": sum({a, b} == {"include", "exclude"} for a, b in dual)}
json.dump(stats, open(f"{OUT}/stage5_map/_map_stats.json", "w"), indent=1)

md = [f"# Stage 5 — Systematic Map (auto-derived from extraction.json; N={N})", ""]
for name in ("repr_primary","repr_any","integration","task","scope","domain","evaluation",
             "wieringa","record_type","cross_language","year","peer_reviewed"):
    md += [f"## {name}", "", "| value | n |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in stats[name].items()]; md += [""]
md += ["## repr_primary × task", "", "| repr | detection | localization | triage | repair | multi |", "|---|---|---|---|---|---|"]
for k, v in stats["repr_x_task"].items():
    md.append(f"| {k} | {v.get('detection',0)} | {v.get('localization',0)} | {v.get('triage_fp_reduction',0)} | {v.get('repair',0)} | {v.get('multi',0)} |")
md += ["", "## repr_primary × evaluation", "", "| repr | strict | unmatched budget | component | ablated | demonstrated | not_eval |", "|---|---|---|---|---|---|---|"]
for k, v in stats["repr_x_eval"].items():
    md.append(f"| {k} | {v.get('repr_strict',0)} | {v.get('repr_unmatched_budget',0)} | {v.get('component_ablation',0)} | {v.get('ablated_measured',0)} | {v.get('demonstrated',0)} | {v.get('not_evaluated',0)} |")
md += ["", f"## RQ4: strict representation-only ablations ({len(iso)}/{N}); structure-gain deltas reported: {len(sg)}/{N}", ""]
md += [f"- {r['system']} ({r['id']}): {r['structure_gain'][:160]}" for r in stats["isolation_records"]]
open(f"{OUT}/stage5_map/systematic_map.md", "w").write("\n".join(md) + "\n")
print(f"map written: N={N}, isolation={len(iso)}, structure_gain_reported={len(sg)}")
