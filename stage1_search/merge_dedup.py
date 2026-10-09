#!/usr/bin/env python3
"""Study 6 stage 1->2: merge results, dedup (normalized TITLE ONLY -> title-Jaccard>=0.8), pre-filter
(security ∧ structure/context ∧ LLM signal), gold-set recall audit (incl. borderline + negative
controls), cap check (seeded sample if >200), emit identified.jsonl + candidates.jsonl + compact
screening chunks + a seeded 20% dual-screen sample."""
import json, glob, re, os, random

BASE = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
R = f"{BASE}/stage1_search/results"
os.makedirs(f"{BASE}/stage2_screening", exist_ok=True)
SEED, CAP, CHUNK = 20260830, 200, 35

def norm(t): return re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()
def toks(t): return set(norm(t).split())
def jac(a, b): return len(a & b) / len(a | b) if a and b else 0.0

rows, by_aid, by_title, n_raw = [], {}, {}, 0
for f in sorted(glob.glob(f"{R}/*.jsonl")):
    q = os.path.basename(f).replace(".jsonl", "")
    for line in open(f):
        line = line.strip()
        if not line: continue
        n_raw += 1
        r = json.loads(line)
        aid = (r.get("arxiv_id") or "").split("v")[0].strip()
        nt = norm(r.get("title"))
        if not nt: continue
        hit = by_aid.get(aid) if aid else None
        hit = hit or by_title.get(nt)
        if not hit:
            tk = toks(r.get("title"))
            hit = next((e for e in rows if jac(tk, e["_toks"]) >= 0.8), None)
        if hit:
            hit["queries"].append(q)
            if aid and not hit.get("arxiv_id"): hit["arxiv_id"] = aid
            if len(r.get("abstract") or "") > len(hit.get("abstract") or ""): hit["abstract"] = r["abstract"]
            continue
        rec = {"arxiv_id": aid, "title": (r.get("title") or "").strip(), "authors": r.get("authors") or [],
               "abstract": r.get("abstract") or "", "year": r.get("year"), "pdf_url": r.get("pdf_url") or "",
               "doi": r.get("doi") or "", "source": r.get("source") or "", "queries": [q], "_toks": toks(r.get("title"))}
        rows.append(rec); by_title[nt] = rec
        if aid: by_aid[aid] = rec

SEC = re.compile(r"vulnerab|\bCWE\b|\bCVE\b|security|exploit|malware|malicious|taint|bug[- ]?(detect|find|hunt)|weakness|insecure", re.I)
STRUCT = re.compile(r"abstract syntax|\bAST\b|syntax tree|graph|\bCPG\b|slice|slicing|taint|static analysis|inter[- ]?procedural|call[- ]?graph|data[- ]?flow|control[- ]?flow|context|representation|retriev|structure", re.I)
LLM = re.compile(r"\bLLM|large language|language model|GPT|foundation model|transformer[- ]based", re.I)

n_pref = 0
with open(f"{BASE}/stage1_search/identified.jsonl", "w") as fid, open(f"{BASE}/stage2_screening/candidates.jsonl", "w") as fc:
    for r in rows:
        blob = f"{r['title']} {r['abstract']}"
        r2 = {k: v for k, v in r.items() if k != "_toks"}
        r2["prefilter_pass"] = bool(SEC.search(blob) and STRUCT.search(blob) and LLM.search(blob))
        fid.write(json.dumps(r2) + "\n")
        if r2["prefilter_pass"]:
            n_pref += 1; fc.write(json.dumps(r2) + "\n")

GOLD = ["llmxcpg", "kastro|k astro", "scale constructing structured", "iris", "vulrag|vul rag", "repoaudit",
        "vultriage", "clear causal|causal context", "representation matters", "code representation shapes false",
        "multitask selfinstructed|self instructed fine"]
BORDER = ["variable context windows"]
NEG = ["diversevul", "prompt injection"]
nts = [norm(r["title"]) for r in rows]
cand_nts = {norm(json.loads(l)["title"]) for l in open(f"{BASE}/stage2_screening/candidates.jsonl")}
lines = ["# Gold-set recall audit (Study 6)", "", "| Item | Retrieved | Passed pre-filter |", "|---|---|---|"]
miss = 0
for kind, items in (("", GOLD), ("BORDERLINE:", BORDER), ("NEG:", NEG)):
    for g in items:
        pats = g.split("|")
        found = next((t for t in nts if any(p in t for p in pats)), None)
        inpref = found in cand_nts if found else False
        if not found and kind == "": miss += 1
        lines.append(f"| {kind}{g} | {'yes' if found else 'NO'} | {'yes' if inpref else 'no'} |")
lines.append(f"\nGold recall: {len(GOLD)-miss}/{len(GOLD)}. Borderlines test criteria; negative controls test screening, not recall.")
open(f"{BASE}/stage1_search/_gold_recall.md", "w").write("\n".join(lines) + "\n")

cands = [json.loads(l) for l in open(f"{BASE}/stage2_screening/candidates.jsonl")]
cands.sort(key=lambda r: r["arxiv_id"] or norm(r["title"]))
sampled = False
if len(cands) > CAP:
    random.Random(SEED).shuffle(cands); cands = sorted(cands[:CAP], key=lambda r: r["arxiv_id"] or norm(r["title"])); sampled = True
    with open(f"{BASE}/stage2_screening/candidates_sampled.jsonl", "w") as f:
        for c in cands: f.write(json.dumps(c) + "\n")
def compact(c): return {"id": c["arxiv_id"] or norm(c["title"])[:40], "title": c["title"], "year": c["year"],
                        "abstract": (c["abstract"] or "")[:700]}
nch = max(1, (len(cands) + CHUNK - 1) // CHUNK)
for i in range(nch):
    json.dump([compact(c) for c in cands[i::nch]], open(f"{BASE}/stage2_screening/_chunk{i}.json", "w"), indent=0)
dual = random.Random(SEED).sample(cands, max(1, len(cands) // 5))
json.dump([compact(c) for c in dual], open(f"{BASE}/stage2_screening/_dualscreen_sample.json", "w"), indent=0)
print(f"raw={n_raw} unique={len(rows)} prefilter={n_pref} screened_set={len(cands)} (sampled={sampled}) chunks={nch} dual={len(dual)}")
