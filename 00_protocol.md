# Review Protocol — Systematic Mapping Study (Study 6)

**Working title:** *Does Structure Help the Hunter? A Systematic Mapping of Program Representations and
Context in LLM Security Analysis.*

**Document type:** Technical report (systematic mapping study), Petersen et al. (2008; 2015) + Kitchenham
& Charters (2007). **Not** peer-reviewed. **Authorship:** `[REDACTED]` (double-blind).
**Search/compile cutoff:** 2026-08-30. **Eligible window:** 2023-01-01 – 2026-08-30.
**Protocol fixed before retrieval**; amendments logged with timestamps.

## 1. Motivation, research questions, target audience

LLMs are widely applied to security analysis of code — vulnerability detection, localization, triage,
and repair — and a growing line of work grounds them in **structural program representations**: ASTs,
control/data-flow graphs, code property graphs, slices, taint paths, inter-procedural context. Several
broad "LLM for vulnerability detection" surveys exist (2024–2026), organized by task, model, or dataset.
None maps the **representation/context** cut: what the model is actually shown, how structure is
integrated, at what analysis scope, and — critically — whether "structure helps" is demonstrated by
representation-only, budget-matched ablations or confounded with simply giving the model more context.
This study maps that cut, and only that cut; it cites and positions against the existing surveys.

- **RQ1 (Representations).** What program representations ground LLM security analysis — raw code text,
  AST, CFG/DFG, code property graph, slice, taint path, call-graph/inter-procedural context,
  NL-structured renderings?
- **RQ2 (Integration).** How is structure integrated — serialized into the prompt, used to guide
  retrieval/context assembly, injected via fine-tuning/adapters, combined neuro-symbolically with a
  static analyzer, or wielded by an agent as a tool?
- **RQ3 (Task & scope).** Which security tasks (detection, localization, triage/FP-reduction, repair)
  and scopes (function, file, inter-procedural, repository) does each representation serve, and how are
  they evaluated (datasets, metrics, cross-language)?
- **RQ4 (Evidence integrity).** Which papers isolate the representation's contribution — same model, same
  budget, representation varied — and what does that subset actually show? Which classical
  static-analysis artifacts (slices, taint specs, CPGs, points-to) have LLM-pipeline instantiations,
  and which are absent?

**Target audience:** security-tool builders deciding whether structural grounding is worth its pipeline
cost, and researchers designing the ablations the field currently lacks.

## 2. Sources & search — three strategies

1. **Database search:** arXiv API (≥3 s throttle) + OpenAlex, scripted (`stage1_search/run_search.sh`;
   strings + hit counts in `search_log.md`). 2-database ceiling disclosed (DARE QC2), mitigated below.
2. **Snowballing:** known-item seeds now (`run_known_items.sh`); after screening, one backward+forward
   snowballing pass over included records (logged).
3. **Manual venue checks:** IEEE S&P, USENIX Security, CCS, NDSS, ICSE/FSE/ASE proceedings (logged).

**Search evaluation (quasi-gold standard with borderline + negative controls):** LLMxCPG; K-ASTRO; SCALE;
IRIS (LLM + static-analysis taint); Vul-RAG; RepoAudit; VulTriage; CLEAR; "Representation Matters"
(program-representation empirical study); "How Code Representation Shapes False-Positive Dynamics";
MSIVD (multitask self-instructed fine-tuning); *borderline:* "Evaluating LLMs in Vulnerability Detection
Under Variable Context Windows" (varies context, no structure — must be INCLUDED as context-effect
empirical study), smart-contract slicing+LLM work (domain boundary); *negative controls (must be excluded
if retrieved):* DiverseVul (dataset for non-LLM DL, E2), a prompt-only "can GPT find bugs" benchmark with
no representation/context variation (E1), an agent-hijacking/prompt-injection defense (E3 — program
Studies 1–4 territory). Recall + control outcomes reported in `search_log.md`.

**Caps (declared before any draw).** If pre-filter candidates exceed **200**, screening uses a seeded
random sample of 200 (`seed=20260830`), reported as sampling in PRISMA.

## 3. Inclusion / exclusion

**Include** iff: **I1** an LLM performs a **security analysis task on code** — vulnerability detection,
localization, triage/false-positive reduction, or security repair (incl. malicious-code detection);
**I2** the approach **grounds the LLM in a structural program representation or an engineered context**
(AST/CFG/DFG/CPG/slice/taint/call-graph/retrieved cross-file context), OR **empirically studies the
effect of representation/context** on a security task; **I3** a quantitative result; **I4** 2023–2026,
English, retrievable.
**Exclude:** **E1** prompt-only LLM security work with neither a representation/context mechanism nor a
representation/context study (plain "ask the model" benchmarks); **E2** non-LLM structural detection
(GNN/DL-only; kept as background, not corpus); **E3** agent-loop security — prompt injection, hijacking,
agent safety (program Studies 1–4 territory); **E4** security *of* LLM-generated code (does the model
write vulnerable code) with no analysis task; **E5** no quantitative result; **E6** duplicate/superseded;
**E7** not retrievable.

**Record** = publication/study unit. Dedup key = normalized title, then title-Jaccard ≥ 0.8.

## 4. Screening — with a reliability action on inclusion/exclusion

Identification → title-only dedup → automated pre-filter (security∧structure/context∧LLM conjunction;
audited against the gold set) → LLM screening in disjoint batches → author adjudication of uncertains +
logged overrides. **Reliability action:** a seeded (`seed=20260830`) **20% double-screened sample** by a
blind second screener; include/exclude agreement + Cohen's κ reported; disagreements adjudicated under a
written rule (default to full-text check).

## 5. Classification scheme

- **F1 Representation (multiple; primary flagged):** raw text · AST · CFG/DFG · CPG · slice · taint path ·
  call-graph/inter-procedural context · retrieved cross-file/CWE-knowledge context · NL-structured
  rendering · hybrid.
- **F2 Integration point:** prompt serialization · retrieval/context-assembly guide · fine-tuning/adapter ·
  neuro-symbolic (LLM + static analyzer in the loop) · agent tool-use.
- **F3 Task:** detection · localization · triage/FP-reduction · repair · multi.
- **F4 Scope:** function · file · inter-procedural · repository. **Domain:** general code · smart-contract ·
  binary · hardware/RTL · web/JS.
- **F5 Evaluation:** representation-only ablation (same model+budget, representation varied) ·
  ablated/measured vs baseline (not representation-isolated) · demonstrated · not evaluated; dataset(s);
  cross-language (y/n).
- **F6 Research type (Wieringa):** validation · evaluation · solution proposal · philosophical · opinion ·
  experience. **F7 record type:** technique/tool · benchmark/eval · empirical study · survey · position.

## 6. Extraction schema (per record)

`system, citation_key, year, venue, peer_reviewed, F1(primary), F2, F3, F4(+domain), F5(+dataset,
cross_language), F6, F7, key_numbers(1–3, source+location), confound_note(what varies between compared
conditions), structure_gain(reported delta vs unstructured baseline, if any, with conditions),
stop_detail, threats_to_that_datum`. **Full-corpus number verification** + **blind full-corpus second
coding** (F1-primary, F2, F5) with κ, as Study 4.

## 7. Analysis & synthesis (named)

**Frequency-count synthesis over the facet map plus structured narrative synthesis** per cell (Petersen
2008). Central maps: representation × task cross-tabulation; representation × evaluation-rigor; the RQ4
"isolation table" (every structure-vs-text comparison and what varies between its arms); classical
static-analysis idiom crosswalk. **Quality assessment:** none, by design, per Petersen (disclosed);
F5 captures rigor descriptively. Evidence labels + programmatic counts as Study 5.

## 8. Threats to validity — Petersen's four categories by name

**Descriptive** (full-corpus verification), **theoretical** (2-database ceiling; terminology bias —
"context" is overloaded; screening & facet κ), **interpretive** (structure_gain deltas come from
heterogeneous datasets/metrics — no cross-paper effect pooling; corpus-scoped claims), **repeatability**
(scripted search, seeds, logs, released pipeline).

## 9. Reporting

Main body ≤ 8 pages (IEEE, split build) + `supplementary.pdf` appendices. AI-tooling disclosure as
Studies 1–5.

## 10. Stage map

0 protocol · 1 search_log (3 strategies + gold-set recall) · 2 prisma + corpus (+ dual-screen κ) ·
3 extraction + verification + second coding · 4 artifacts (code-release survey) · 5 map + synthesis ·
6 report + references + paper.pdf + supplementary.pdf.
