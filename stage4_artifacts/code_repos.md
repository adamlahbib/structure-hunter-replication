# Stage 4 — Code Artifact Survey

**Survey date:** 2026-08-30

**Methodology:** For each of the 20 selected systems, one targeted `WebSearch` was run
(query pattern: `"<system> github vulnerability detection code"` or a close variant using
the paper's own title keywords). Where the search surfaced a plausible repository URL, one
`WebFetch` of that repo's GitHub page was performed to record stars, license, and
last-activity signals. **No further searching was done per system.** Absence of a
discoverable repository after this single targeted search is recorded as "no public
artifact found (single-search check)" — this is not proof no artifact exists, only that
one reasonably-targeted search did not surface one. Star/license/activity fields reflect
whatever was visible on the fetched GitHub page at time of check; fields not visible in the
fetched page content are marked "not visible."

**Selection note:** The task brief asked for "K-ASTRO" among the headline systems, but no
system by that name appears in `corpus.jsonl` (67 records checked) — it was dropped and
one additional corpus system was substituted in its place. The final list below covers 20
systems spanning detection (graph/CPG-guided, RAG/knowledge-base, comment-tree,
soft-prompt-tuning, neuro-symbolic static analysis), repair, and repository/agentic auditing
approaches, prioritizing the study's headline findings plus additional systems chosen for
representation-class and venue diversity.

> **Revision note (2026-10-09).** Selected during the original study (67 records at that time; the corpus is now 68).
> The selection is purposive and does not cover every study in the revised strict set. "NONE FOUND" means none was found in one targeted search.

## 1. Repository table

| System | arXiv ID | Repo | Stars | License | Activity signal |
|---|---|---|---|---|---|
| LLMxCPG | 2507.16585 | [github.com/qcri/llmxcpg](https://github.com/qcri/llmxcpg) | 161 | GPL-3.0 | 42 commits; news dated Nov 2025 (USENIX Security '25 presentation, MENA CSAW award) |
| IRIS | 2405.17238 | [github.com/iris-sast/iris](https://github.com/iris-sast/iris) | 420 | MIT | 190 commits on `v2` branch; news entry dated Jun 2026 (CWE-Bench-Java fix data added) |
| Vul-RAG | 2406.11147 | [github.com/KnowledgeRAG4LLMVulD](https://github.com/KnowledgeRAG4LLMVulD/KnowledgeRAG4LLMVulD) | 76 | MIT | 47 commits; exact dates not visible on fetched page |
| RepoAudit | 2501.18160 | [github.com/PurCL/RepoAudit](https://github.com/PurCL/RepoAudit) | 431 | Custom "Purdue" license | 68 commits; news dated Jun 2025 (ICML '25 acceptance) |
| VulTriage | 2605.09461 | NONE FOUND | — | — | Paper text claims "code is available on GitHub" but no repo URL surfaced in single search |
| SCALE | 2403.19096 | [github.com/Xin-Cheng-Wen/Comment4Vul](https://github.com/Xin-Cheng-Wen/Comment4Vul) | 18 | not visible | 24 commits; no dates visible |
| MSIVD | 2406.05892 | NONE FOUND | — | — | no public artifact found (single-search check) |
| LeanGuard | 2607.03963 | NONE FOUND | — | — | no public artifact found (single-search check) |
| ZeroFalse | 2510.02534 | NONE FOUND | — | — | no public artifact found (single-search check) |
| PacVD | 2504.16877 | [github.com/DoeSEResearch/PacVD](https://github.com/DoeSEResearch/PacVD) | 18 | not visible | 5 commits; no dates visible |
| MulVul | 2601.18847 | NONE FOUND | — | — | no public artifact found (single-search check) |
| RAVEN | 2604.17948 | NONE FOUND | — | — | no public artifact found (single-search check); search returned only unrelated repos named "raven" |
| SecureFixAgent | 2509.16275 | NONE FOUND | — | — | no public artifact found (single-search check) |
| CGP-Tuning | 2501.04510 | [github.com/ruijunfeng/CGP-tuning](https://github.com/ruijunfeng/CGP-tuning) | 5 | not visible | 1 commit; no dates visible |
| RepBench ("Representation Matters") | 2606.25356 | NONE FOUND | — | — | search surfaced a same-named but unrelated repo (`xlands/RepBench`, a representation-engineering benchmark for a different paper, arXiv 2607.28008); verified via fetch and excluded |
| ACFix | 2403.06838 | NONE FOUND | — | — | no public artifact found (single-search check) |
| LATTE | 2310.08275 | NONE FOUND | — | — | no public artifact found (single-search check) |
| ContractTinker | 2409.09661 | [github.com/CheWang09/LLM4SMAPR](https://github.com/CheWang09/LLM4SMAPR) | 18 | not visible | commit/date not visible; repo description ("automated contract repair tool ... Slither") matches paper |
| VulMaster | 2401.15459 | NONE FOUND | — | — | no public artifact found (single-search check) |
| MoCQ | 2504.16057 | NONE FOUND | — | — | no public artifact found (single-search check) |

## 2. No-artifact list (12 of 20 systems)

- VulTriage (2605.09461) — claims GitHub availability in text; URL not resolved in single search
- MSIVD (2406.05892)
- LeanGuard (2607.03963)
- ZeroFalse (2510.02534)
- MulVul (2601.18847)
- RAVEN (2604.17948)
- SecureFixAgent (2509.16275)
- RepBench / "Representation Matters" (2606.25356) — same-name repo found but confirmed unrelated
- ACFix (2403.06838)
- LATTE (2310.08275)
- VulMaster (2401.15459)
- MoCQ (2504.16057)

## 3. Observations

- **Repository/agentic auditing tools attract the most adoption.** The three highest star
  counts all belong to repo-level or general-purpose static-analysis frameworks rather than
  narrow single-paper scripts: RepoAudit (431, data-flow-graph agent, ICML'25), IRIS (420,
  neuro-symbolic CPG+LLM, ICLR'25), and LLMxCPG (161, CPG-guided, USENIX Sec'25). These are
  also the three most rigorously peer-reviewed venues in the sample, suggesting top-venue
  acceptance and "reusable tool" framing (vs. "artifact for one experiment") both correlate
  with community uptake.
- **Graph/structural-representation papers release code more consistently than
  prompt-tuning or repair-only papers in this sample.** 4 of 6 CPG/AST/CFG/data-flow-graph
  systems checked (LLMxCPG, IRIS, RepoAudit, SCALE) had a discoverable repo, vs. only 2 of 6
  repair-focused systems (ContractTinker, and none of ACFix/LATTE/VulMaster/SecureFixAgent/
  MoCQ) — though the repair-paper sample is small enough that this should be read as a
  signal, not a firm result.
- **The paper making the SLR's own representation-ablation claim is the hardest to verify.**
  RepBench / "Representation Matters" (2606.25356) — the corpus paper most directly relevant
  to this study's research question (it isolates representation choice while holding the
  detection task fixed) — had no verifiable public code in a single-search check; the
  same-named repo that surfaced belongs to an unrelated representation-engineering paper.
  That means the study's headline representation-ablation results (e.g., AST+PDG at 83.2%
  vs. raw source at 53.5%) currently cannot be independently reproduced from a discoverable
  artifact, which is a notable gap for a paper central to this SLR's argument.
- **License hygiene is weak even among found repos.** Of the 8 repos located, only 3 show a
  clear OSS license at a glance (LLMxCPG: GPL-3.0, IRIS: MIT, Vul-RAG: MIT); RepoAudit uses a
  custom institutional ("Purdue") license, and four others (SCALE, PacVD, CGP-Tuning,
  ContractTinker) show no visible license file, leaving reuse/redistribution rights unclear
  for roughly half of the artifacts that do exist.
- **RAG/knowledge-base detection approaches (Vul-RAG) publish both code and the constructed
  knowledge base**, and independently attracted a follow-up reproducibility study in the
  corpus itself (2606.04739, "Revisiting Vul-RAG"), which is the only case in this sample
  where third-party replication of a released artifact is directly evidenced within the
  corpus.
