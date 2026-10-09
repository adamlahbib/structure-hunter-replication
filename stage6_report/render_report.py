#!/usr/bin/env python3
"""Fill report.tmpl.md's {{dotted.path}} placeholders from stage5_map/_map_stats.json -> report.md.
Every count in the manuscript goes through here, so the paper cannot drift from extraction.json.
Fails on an unknown path. Usage: render_report.py [study_folder]"""
import json, re, sys, os

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stats = json.load(open(f"{BASE}/stage5_map/_map_stats.json"))
tmpl = open(f"{BASE}/stage6_report/report.tmpl.md").read()


def get(path):
    v = stats
    for k in path.split("."):
        if isinstance(v, dict) and k in v:
            v = v[k]
        else:
            sys.exit(f"render_report: unknown placeholder {{{{{path}}}}}")
    if isinstance(v, (dict, list)):
        sys.exit(f"render_report: {{{{{path}}}}} is not a scalar")
    return f"{v:.2f}" if isinstance(v, float) and path.endswith("kappa") else str(v)


COUNT_FACETS = {"repr_primary", "repr_any", "integration", "task", "scope", "domain", "evaluation",
                "wieringa", "record_type", "year", "repr_x_task", "repr_x_eval"}
AB = {"retrieved_context": "retrieved", "raw_text": "raw", "taint_path": "taint", "interproc_callgraph": "interproc",
      "cfg_dfg": "CFG/DFG", "nl_structured": "NL-struct", "cpg": "CPG", "ast": "AST",
      "prompt_serialization": "prompt", "neurosymbolic_analyzer_loop": "neurosym", "finetune_adapter": "fine-tune",
      "agent_tool_use": "agent", "retrieval_guide": "retr-guide", "triage_fp_reduction": "triage",
      "interprocedural": "interproc", "smart_contract": "contract", "web_js": "web/JS", "hardware_rtl": "RTL",
      "general": "general", "repr_strict": "strict", "repr_unmatched_budget": "unmatched", "component_ablation":
      "component", "ablated_measured": "measured", "demonstrated": "demo", "not_evaluated": "none",
      "solution_proposal": "proposal", "validation": "valid.", "evaluation": "eval."}


def bibkeys():
    """arXiv id -> citation key, read from references.bib (entries carry 'arXiv:<id>' notes or abs URLs)."""
    bib = open(f"{BASE}/stage6_report/references.bib").read()
    out = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        a = re.search(r"(?:arXiv:|arxiv\.org/abs/)(\d{4}\.\d{4,5})", m.group(2))
        if a: out[a.group(1)] = m.group(1)
    return out


def table(name):
    rows = [r for r in json.load(open(f"{BASE}/stage3_extraction/extraction.json")) if r.get("eligible", True)]
    keys = bibkeys(); ab = lambda v: AB.get(v, v or "")
    if name == "corpus":
        out = ["Table: Complete corpus and facet coding (full bibliographic entries for every row are in the reference list).", "",
               "| # | System | Ref. | arXiv | Repr. | Integration | Task | Scope | Domain | Eval. | Peer-rev. |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            k = keys.get(r["arxiv_id"])
            assert k, f"no bibliography entry for {r['arxiv_id']}"
            rc = (r.get("repr_classes") or [""])[0]
            out.append(f"| {i} | {r.get('system')} | [@{k}] | {r['arxiv_id']} | {ab(rc)} | {ab(r.get('integration'))} | "
                       f"{ab(r.get('task'))} | {ab(r.get('scope'))} | {ab(r.get('domain'))} | {ab(r.get('evaluation'))} | "
                       f"{'yes' if r.get('peer_reviewed') else 'no'} |")
        return "\n".join(out)
    if name == "isolation":
        out = ["Table: Study-level audit of the 37 records first coded as representation-only ablations.", "",
               "| System | Model / config | Dataset, metric | Budget control | Arms compared | Other change | Reported delta | Verdict | Decided by | Rationale |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        def cl(t):  # one line per cell; "the record" in audit notes means our original extraction
            t = re.sub(r"\s+", " ", str(t or "")).replace("|", "/")
            t = t.replace("$", "\\$")  # literal dollars, not pandoc math
            return re.sub(r"\b([Tt])he record('s)?\b", lambda m: ("O" if m.group(1) == "T" else "o") + "ur original extraction" + (m.group(2) or ""), t)
        for a in stats["isolation_audit"]:
            out.append(f"| {a['system']} | {cl(a['model_config'])} | {cl(a['dataset_metric'])} | {cl(a['budget_control'])} | "
                       f"{cl(a['arm_a'])} vs {cl(a['arm_b'])} | {cl(a['other_changes'])} | {cl(a.get('delta'))} | {ab(a['evaluation'])} | "
                       f"{'both checkers' if a['decided_by'] == 'both checkers' else 'author (proposed verdict)'} | {cl(a.get('human_reason') or a.get('rationale'))} |")
        return "\n".join(out)
    sys.exit(f"render_report: unknown table {name}")


tmpl = re.sub(r"\{\{table:(\w+)\}\}", lambda m: table(m.group(1)), tmpl)
out, n = re.subn(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}", lambda m: get(m.group(1)), tmpl)
left = re.findall(r"@@\w+@@|\{\{[^}]*\}\}", out)
if left and not os.environ.get("DRAFT"):
    sys.exit(f"render_report: unfilled sections/placeholders: {sorted(set(left))}")
open(f"{BASE}/stage6_report/report.md", "w").write(out)
print(f"report.md rendered: {n} placeholders filled")

if __name__ == "__main__" and os.environ.get("SELFTEST"):
    stats.update({"a": {"b": 3}, "k": {"kappa": 0.5}})
    assert get("a.b") == "3" and get("k.kappa") == "0.50"
    print("selftest ok")
