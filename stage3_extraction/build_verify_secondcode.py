#!/usr/bin/env python3
"""build verify_in/ batches (numbers + facets per eligible record) and secondcode_in/
batches (BLIND: id+title only) from extraction.json. Usage: build_verify_secondcode.py [base] [nbatch]."""
import json, sys, os

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
NB = int(sys.argv[2]) if len(sys.argv) > 2 else 6
rows = [r for r in json.load(open(f"{BASE}/stage3_extraction/extraction.json")) if r.get("eligible", True)]
os.makedirs(f"{BASE}/stage3_extraction/verify_in", exist_ok=True)
os.makedirs(f"{BASE}/stage3_extraction/secondcode_in", exist_ok=True)
os.makedirs(f"{BASE}/stage3_extraction/verify_out", exist_ok=True)
os.makedirs(f"{BASE}/stage3_extraction/secondcode_out", exist_ok=True)
def prim(v): return v[0] if isinstance(v, list) and v else v
for i in range(NB):
    chunk = rows[i::NB]
    json.dump([{"arxiv_id": r["arxiv_id"], "title": r.get("title",""), "system": r.get("system",""),
                "key_numbers": r.get("key_numbers", []),
                "repr_primary": prim(r.get("repr_classes")), "integration": r.get("integration"),
                "evaluation": r.get("evaluation"), "structure_gain": r.get("structure_gain",""),
                "stop_detail": r.get("stop_detail","")}
               for r in chunk], open(f"{BASE}/stage3_extraction/verify_in/batch{i}.json", "w"), indent=0)
    json.dump([{"arxiv_id": r["arxiv_id"], "title": r.get("title","")} for r in chunk],
              open(f"{BASE}/stage3_extraction/secondcode_in/batch{i}.json", "w"), indent=0)
print(f"built {NB} verify_in + secondcode_in batches over {len(rows)} eligible records")
