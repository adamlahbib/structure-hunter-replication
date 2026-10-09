# Stage 3 — Author Adjudication Log (2026-08-30)

> **Historical header (2026-08-30).** The paragraph below predates the GPTScan restoration (amendment D2) and the
> isolation re-audit (amendment A2). Current totals: 68 records, 261 numeric claims (243 confirmed, 17 wrong, 1
> unretrievable), and the A2 section at the end of this log. The paper's numbers come from `stage5_map/_map_stats.json`.


Independent verification covered **all 67 eligible records, 257 numeric claims** (93.0% confirmed,
17 wrong, 1 unretrievable — a figure-only heatmap) plus non-blind facet spot-checks; a blind second
coder re-coded all 67 on three facets. One record (2607.03963 LeanGuard) was skipped by its batch
verifier and was **author-verified directly** against the source (all five checks confirmed exactly;
logged in `verify_out/batch6.json`). Corrections apply programmatically via `apply_adjudications.py`.

## Number corrections — 17 WRONG verdicts, all ACCEPTED

Recurring shapes, each fixed with the verifier's exact value: wrong-row misattributions (MulVul's
retrieval-ablation drop is −12.76pp; the −30.70 belongs to the GPT-4o baseline row; RepoAudit's
no-validator precision is 51.28% from Table 6's own totals, not 33.33%), **relative-vs-percentage-
point conflation** (QASecClaw recall −2.9pp, the paper's 3.2% being relative), wrong-mode
attribution (Explode.js File mode 43.13%, not Pkg mode), "best baseline" that was actually the
worst (SCALE vs UniXcoder 56.04%, not CodeBERT 49.10%), a metric swap (ZeroFalse FPR_P 0.98–1.0;
72–96% is FPR_R), figure-derived values presented as table cells with a nonexistent C/C++
breakdown (VulnLLM-R), and derived averages recomputed (+0.176, not ~0.15).

## Evaluation facet — strict representation-isolation rule, adjudicated record-by-record

Rule: `representation_only_ablation` requires the SAME model at the SAME context budget with only
the representation varied. **Downgrades accepted (4):** 2602.06751 (compares UniXcoder vs a
fine-tuned Qwen2.5-32B — different architectures), 2607.21983 (configs "not recorded", unequal
input lengths), 2503.03586 (ReAct-vs-plain changes the interaction paradigm, not the
representation), 2512.07533 (the ablation varies reasoning-chain training; adjudicated to
ablated_measured rather than the verifier's not_evaluated, since quantified baseline comparisons
exist). **Upgrades accepted (2):** 2406.11147 Vul-RAG (its code-level-RAG comparator is a same-model
ablation) and 2507.16585 LLMxCPG (Appendix C's same-model slicing ablation exists and is detailed —
the extraction's contrary claim was itself an extraction error, now fixed). Net isolation set:
**36/67** (from 38 as extracted).

**Rejected:** the blind second coder's 13 repr-only downgrades where the full-text verifier
independently confirmed the extractor's coding (11 of 13; several were coded by the second coder
from the abstract alone); the two with verifier concurrence are in the accepted set above.

## Representation / integration recodes — ACCEPTED (verifier full-text evidence)

repr_primary: 2509.15433 → hybrid (+ integration → finetune_adapter); 2601.10865 → taint_path;
2604.08417 → interproc_callgraph (the paper's own stated primary independent variable);
2605.04251 → hybrid (fuzzing traces + dataflow + call-graph); 2607.01138 → hybrid (deterministic
Tree-sitter extraction, not similarity retrieval); 2409.18395 → nl_structured (no retrieval corpus
exists). integration: 2505.17416 and 2604.17948 → retrieval_guide (fixed sequential RAG pipelines,
no autonomous tool invocation); 2605.09461 → prompt_serialization (the AST/CFG/DFG control path is
verbalized into the prompt, not retrieved).

## Also noted by verifiers (recorded on records, no facet change)

2406.05892 MSIVD: the PreciseBugs F1=0.48 is the paper's own no-GNN variant, per its text.
2512.04106: the cited zero-shot-vs-20-shot pair is shot-count-confounded; a clean same-shot
ablation exists elsewhere in the paper. 2505.17460 (FocusVul) is author-withdrawn and demoted
E6-withdrawn by amendment A1 (see `decisions_adjudication.json`).

## Blind second-coder reliability (context for the κ table)

Post-adjudication κ: repr_primary 0.55, integration 0.72, evaluation 0.54 (n=67). The repr
disagreements concentrate on the hybrid boundary (17/30 involve hybrid), and 13 of 17 evaluation
disagreements were downgrades of `representation_only_ablation` — the same direction the verifiers
flagged and this adjudication partially upheld. Headline claims are therefore anchored to the
structural-vs-raw-text aggregate (robust to the hybrid boundary) and the adjudicated 36/67
isolation set is reported with its contested history, not as a clean count.


## Amendment A2 (2026-10-09): full-text isolation re-audit

All 37 records coded `representation_only_ablation` were re-audited at full text by two independent checkers
(Claude agents: `isoaudit_out/`; GPT: `isoaudit2/out/`). Agreement 27/37 (kappa 0.60, `isoaudit2/compare.py`).
The authors decided the 10 disagreements; reasons in `isoaudit2/human_decisions.json`. Final verdicts:
`isoaudit_final.json` (7 strict, 13 unmatched input, 15 component, 2 not isolated).

Extraction errors corrected (accepted; source value used):
- Antaeus (2607.01138): numbers matched superseded v1; replaced with v2 Table 4 (35 CVEs).
- LLMxCPG (2507.16585): Appendix C values are accuracy, not F1.
- AgenticRepair (2607.29422): code-structure facet arm is 73.5%, not within "73.0-74.5%" as a range for all arms.
- Trad25 (2512.04106): cited zero- vs 20-shot pair changes context amount; equal-shot comparison (71.43% vs 65.69%) recorded.
- ZeroFalse (2510.02534): +0.176 is our mean over Table 4, not a reported figure; now labelled as computed.
- SemTaint (2601.10865): models are GPT-5 / GPT-5-mini, not GPT-4 / GPT-4-mini; CodeQL performs detection.
- RepoAudit (2501.18160): 51.28% is computed from Table 6, not stated; now labelled.

Inconsistencies inside primary studies (recorded in `source_inconsistency`, not extraction errors):
RepoAudit, VerilogLAVD, SCALE, Khan24, MoCQ, ACFix.
