#!/usr/bin/env python3
"""Bounded backward-snowballing check (narrows deviation D1; not the full protocol pass).
For each given arXiv id: list its references (Semantic Scholar), keep those whose title passes the
search's own conjunction (LLM AND security AND structure/context), and report the ones the search never
identified. Output: stage1_search/_snowball_check.json. Usage: snowball_check.py <arxiv_id>..."""
import json, re, sys, time, os, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "slr-snowball-check (mailto:anonymous@example.org)"}
LLM = re.compile(r"\b(llms?|large language models?|gpt|chatgpt|language models?|codellama|code ?llms?)\b", re.I)
SEC = re.compile(r"vulnerab|secur|exploit|taint|cwe|bug|patch|repair|malicious|false positive", re.I)
STRUCT = re.compile(r"graph|ast\b|syntax|slice|slicing|flow|taint|context|retriev|rag\b|static analysis|program analysis|"
                    r"call|inter-?procedural|repository|symbolic|semantic", re.I)


def get(url):
    for wait in (1.5, 10, 30, 60):
        time.sleep(wait)
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 404: return {"data": None}
            if e.code != 429: raise
    raise RuntimeError(f"rate-limited: {url}")


def norm(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())


known = set()
for f in ("stage1_search/identified.jsonl", "stage2_screening/candidates.jsonl", "corpus.jsonl"):
    for l in open(f"{BASE}/{f}"):
        if l.strip(): known.add(norm(json.loads(l).get("title")))

report = []
for aid in sys.argv[1:]:
    # Semantic Scholar: OpenAlex carries no reference lists for most recent arXiv preprints.
    refs = get(f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}/references?fields=title,year&limit=1000")["data"]
    if refs is None:
        report.append({"arxiv_id": aid, "n_refs": None, "in_scope_by_title": None, "unknown": []})
        print(f"{aid}: not found in Semantic Scholar"); continue
    refs = [r["citedPaper"] for r in refs if r.get("citedPaper")]
    hits = [{"title": x.get("title") or "", "year": x.get("year"), "known": norm(x.get("title")) in known}
            for x in refs if (x.get("year") or 0) >= 2023 and LLM.search(x.get("title") or "")
            and SEC.search(x.get("title") or "") and STRUCT.search(x.get("title") or "")]
    report.append({"arxiv_id": aid, "n_refs": len(refs), "in_scope_by_title": len(hits),
                   "unknown": [h for h in hits if not h["known"]]})
    print(f"{aid}: {len(refs)} refs, {len(hits)} pass the search conjunction, {len(report[-1]['unknown'])} not identified")
uniq = {norm(h["title"]): h for r in report for h in r["unknown"]}
print(f"{len(report)} papers; {len(uniq)} unique in-scope-by-title references never identified by the search")
json.dump({"papers": report, "unique_unknown": list(uniq.values())}, open(f"{BASE}/stage1_search/_snowball_check.json", "w"), indent=1)
