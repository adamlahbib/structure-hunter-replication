# Stage 5 — Systematic Map (auto-derived from extraction.json; N=68)

## repr_primary

| value | n |
|---|---|
| retrieved_context | 16 |
| hybrid | 11 |
| raw_text | 10 |
| taint_path | 10 |
| cpg | 7 |
| ast | 4 |
| interproc_callgraph | 4 |
| cfg_dfg | 3 |
| slice | 2 |
| nl_structured | 1 |

## repr_any

| value | n |
|---|---|
| raw_text | 33 |
| retrieved_context | 33 |
| interproc_callgraph | 23 |
| taint_path | 15 |
| hybrid | 13 |
| cfg_dfg | 12 |
| cpg | 12 |
| ast | 11 |
| nl_structured | 11 |
| slice | 6 |

## integration

| value | n |
|---|---|
| prompt_serialization | 17 |
| neurosymbolic_analyzer_loop | 16 |
| finetune_adapter | 12 |
| agent_tool_use | 12 |
| retrieval_guide | 11 |

## task

| value | n |
|---|---|
| detection | 38 |
| repair | 12 |
| multi | 12 |
| triage_fp_reduction | 6 |

## scope

| value | n |
|---|---|
| function | 26 |
| interprocedural | 21 |
| repository | 15 |
| file | 6 |

## domain

| value | n |
|---|---|
| general | 54 |
| smart_contract | 8 |
| web_js | 3 |
| binary | 2 |
| hardware_rtl | 1 |

## evaluation

| value | n |
|---|---|
| ablated_measured | 29 |
| component_ablation | 15 |
| repr_unmatched_budget | 13 |
| repr_strict | 7 |
| demonstrated | 3 |
| not_evaluated | 1 |

## wieringa

| value | n |
|---|---|
| validation | 35 |
| evaluation | 31 |
| solution_proposal | 2 |

## record_type

| value | n |
|---|---|
| technique_tool | 53 |
| empirical_study | 11 |
| benchmark_eval | 4 |

## cross_language

| value | n |
|---|---|
| False | 53 |
| True | 15 |

## year

| value | n |
|---|---|
| 2025 | 27 |
| 2026 | 26 |
| 2024 | 13 |
| 2023 | 2 |

## peer_reviewed

| value | n |
|---|---|
| False | 49 |
| True | 19 |

## repr_primary × task

| repr | detection | localization | triage | repair | multi |
|---|---|---|---|---|---|
| raw_text | 5 | 0 | 2 | 1 | 2 |
| taint_path | 4 | 0 | 3 | 1 | 2 |
| ast | 2 | 0 | 0 | 2 | 0 |
| hybrid | 5 | 0 | 0 | 4 | 2 |
| cfg_dfg | 2 | 0 | 0 | 0 | 1 |
| retrieved_context | 10 | 0 | 0 | 3 | 3 |
| nl_structured | 0 | 0 | 0 | 1 | 0 |
| cpg | 5 | 0 | 1 | 0 | 1 |
| interproc_callgraph | 3 | 0 | 0 | 0 | 1 |
| slice | 2 | 0 | 0 | 0 | 0 |

## repr_primary × evaluation

| repr | strict | unmatched budget | component | ablated | demonstrated | not_eval |
|---|---|---|---|---|---|---|
| raw_text | 1 | 2 | 1 | 6 | 0 | 0 |
| taint_path | 0 | 2 | 3 | 5 | 0 | 0 |
| ast | 0 | 2 | 1 | 0 | 1 | 0 |
| hybrid | 2 | 2 | 2 | 4 | 1 | 0 |
| cfg_dfg | 0 | 2 | 0 | 1 | 0 | 0 |
| retrieved_context | 1 | 1 | 6 | 6 | 1 | 1 |
| nl_structured | 0 | 1 | 0 | 0 | 0 | 0 |
| cpg | 2 | 0 | 2 | 3 | 0 | 0 |
| interproc_callgraph | 0 | 1 | 0 | 3 | 0 | 0 |
| slice | 1 | 0 | 0 | 1 | 0 | 0 |

## RQ4: strict representation-only ablations (7/68); structure-gain deltas reported: 59/68

- ACFix (2403.06838): Removing the AC Context Graph (ACG, built from interprocedural slicing+PDG+call graph) drops success from 94.92% to 89.83% (-5.09pp) on the same GPT-4 model wit
- LLM4FPM (2411.03079): eCPG-based slicing (vs full-file raw context, LLM4FPM-noslice) improves accuracy by +3.02pp and F1 by +1.73pp on the same Qwen2.5-32B model (Table III); the raw
- MoCQ (2504.16057): Providing a subset DSL grammar (MoCQ) instead of no specification raises query-generation pass rate from 9.9% (DSL0) to 77.4%, and F1 from 0.31 (DSL100, full gr
- LLMxCPG (2507.16585): Appendix C same-model slicing ablation: slice-based vs full-code F1 0.8146 vs 0.6762 (FormAI), 0.7250 vs 0.4875 (PrimeVul), 0.6020 vs 0.5078 (SVEN) — the extrac
- Trad25 (2512.04106): Equal-shot comparison: 10-shot retrieval-augmented vs random examples, F1 71.43% vs 65.69% (+5.74pp), same Gemini-1.5-Flash (Sec. V-B). The zero-shot vs 20-shot
- Li25 (2512.16538): Central ablation compares raw code text vs. its obfuscated (layout/data-flow/control-flow-transformed) counterpart, same LLM/prompt: virtualization obfuscation 
- RepBench (2606.25356): AST+PDG reaches 83.2% curated accuracy vs. 53.5% for raw source alone (+29.7pp), with model (qwen3.6-plus), temperature, prompting/checklist structure, and 50,0
