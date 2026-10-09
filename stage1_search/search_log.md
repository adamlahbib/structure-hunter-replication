# Stage 1 — Search Log (Study: structure-security)
**Cutoff:** 2026-08-30 · **Window:** 2023-01-01 – 2026-08-30 · English, retrievable.
Sources: arXiv API (>=3 s throttle) + OpenAlex. Runners: `run_search.sh` (topic), `run_known_items.sh`
(known-item seeds + borderline/negative controls). Recall audit: `_gold_recall.md`.

## Topic queries (verbatim strings; hits = raw rows returned)

| Query | File | Hits |
|---|---|---|
| LLM vulnerability detection graph structure (arXiv) | ax_graph.jsonl | 25 |
| abstract syntax tree vulnerability detection language model (arXiv) | ax_ast.jsonl | 18 |
| code property graph LLM vulnerability detection (arXiv) | ax_cpg.jsonl | 30 |
| program slicing vulnerability detection large language model (arXiv) | ax_slice.jsonl | 37 |
| taint analysis large language model vulnerability (arXiv) | ax_taint.jsonl | 37 |
| context enhanced vulnerability detection LLM (arXiv) | ax_ctx.jsonl | 35 |
| inter-procedural vulnerability detection LLM context (arXiv) | ax_interproc.jsonl | 35 |
| LLM vulnerability localization repair context repository (arXiv) | ax_repair.jsonl | 38 |
| static analysis large language model hybrid security detection (arXiv) | ax_hybrid.jsonl | 26 |
| neuro-symbolic vulnerability detection reasoning (arXiv) | ax_neurosym.jsonl | 34 |
| structure-aware fine-tuning code vulnerability (arXiv) | ax_finetune.jsonl | 29 |
| smart contract vulnerability detection LLM slicing graph (arXiv) | ax_contract.jsonl | 31 |
| repository-level vulnerability detection audit agent LLM (arXiv) | ax_repoaudit.jsonl | 39 |
| program representation empirical study LLM vulnerability (arXiv) | ax_repr.jsonl | 24 |
| retrieval augmented vulnerability detection knowledge CWE (arXiv) | ax_rag.jsonl | 36 |
| false positive reduction static analysis LLM triage (arXiv) | ax_triage.jsonl | 27 |
| program representation vulnerability detection large language model (OpenAlex) | oa_repr.jsonl | 40 |
| graph large language model vulnerability detection (OpenAlex) | oa_graph.jsonl | 40 |
| static analysis LLM security false positive (OpenAlex) | oa_static.jsonl | 40 |
| slicing context vulnerability repair LLM (OpenAlex) | oa_slice.jsonl | 40 |

## Known-item / control queries (max 5 each)

| Query | File | Hits |
|---|---|---|
| LLMxCPG context-aware vulnerability detection code property graph (arXiv) | ki_llmxcpg.jsonl | 4 |
| K-ASTRO structure-aware adaptation transformers code vulnerability (arXiv) | ki_kastro.jsonl | 5 |
| SCALE structured natural language comment trees vulnerability (arXiv) | ki_scale.jsonl | 2 |
| IRIS LLM-assisted static analysis whole-project security (arXiv) | ki_iris.jsonl | 2 |
| Vul-RAG vulnerability detection knowledge-level RAG (arXiv) | ki_vulrag.jsonl | 5 |
| RepoAudit autonomous LLM agent repository code auditing (arXiv) | ki_repoaudit.jsonl | 5 |
| VulTriage context augmentation LLM vulnerability detection (arXiv) | ki_vultriage.jsonl | 4 |
| CLEAR causal context agentic reasoning vulnerability (arXiv) | ki_clear.jsonl | 4 |
| representation matters empirical program representations vulnerability reasoning (arXiv) | ki_reprmatters.jsonl | 2 |
| code representation false positive cross-language LLM vulnerability (arXiv) | ki_reprfp.jsonl | 3 |
| multitask self-instructed fine-tuning vulnerability detection (arXiv) | ki_msivd.jsonl | 3 |
| evaluating large language models vulnerability detection variable context windows (arXiv) | ki_bc_ctxwin.jsonl | 5 |
| DiverseVul new vulnerable source code dataset deep learning (arXiv) | ki_nc_diversevul.jsonl | 4 |
| prompt injection defense tool-using agent benchmark (arXiv) | ki_nc_injection.jsonl | 5 |

**Total raw rows: 714.** Dedup (normalized title -> Jaccard >= 0.8) and pre-filter in `merge_dedup.py`;
per-record outcomes in `identified.jsonl`. Manual venue checks (strategy 3, DBLP sweeps) and their
outcomes are logged in `_gold_recall.md` and `../stage2_screening/decisions_adjudication.json`.
Deviation D1: the protocol's post-screening backward/forward snowballing pass was not executed (logged).
