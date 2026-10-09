# Does Structure Help the Hunter? A Systematic Mapping of Program Representations and Context in LLM Security Analysis

<!-- SOURCE OF report.md. Edit this file, never report.md: every count is a double-brace placeholder filled by
render_report.py from stage5_map/_map_stats.json, so the manuscript cannot drift from extraction.json. -->

## Abstract

Large language models (LLMs) are now used to find, triage, and repair software vulnerabilities, and many systems feed them program structure such as syntax trees, data-flow paths, code property graphs, or retrieved context. Does that structure itself improve results, or is it the extra input, a different model, or a larger pipeline? We map {{N}} studies published 2023–2026 by what the model is shown, how the structure reaches it, and how the gain is tested. We then re-read the full text of the {{isoaudit.n}} studies we had first classed as testing the representation alone. Only {{isoaudit.survived}} hold up: same model, only the input format changed, the structured input no longer than the raw code. Of the rest, {{evaluation.component_ablation}} add or remove a pipeline stage, such as a static checker, retrieval, or memory, and {{evaluation.repr_unmatched_budget}} give the structured variant more input; a further {{evaluation.ablated_measured}} studies compare different models or architectures. The evidence is concentrated in single-language, function-level detection, and only {{peer_reviewed.true}} of the {{N}} studies are peer-reviewed. Structure plausibly helps, but most of the evidence shows that larger pipelines help. The experiment it lacks is one benchmark, several representations, one model, and one input budget.

**Keywords:** vulnerability detection, program representations, code property graph, taint analysis, LLM security analysis, systematic mapping study

## I. Introduction

An LLM asked whether a function is vulnerable answers from the text it is shown. Vulnerabilities are rarely textual, though: a use-after-free lives in control flow across calls, an injection in a path from source to sink. Static analysis captures that structure but is notorious for false positives. A fast-growing literature therefore combines the two, giving the LLM structural program representations: code-property-graph slices [@lekssays2025llmxcpg], LLM-inferred taint specifications [@li2024iris], retrieved vulnerability knowledge [@du2024vulrag], structured comment trees [@wen2024scale], or symbolic verdict checks [@zhao2026leanguard].

Surveys of LLM-based vulnerability detection organise this work by task, model, or dataset. None asks three questions a tool builder needs answered. What is the model shown? How does the structure reach it? And is the gain due to the structure itself, or to extra input, a different model, or an added pipeline stage? We answer them with a systematic mapping study and four research questions:

- **RQ1 (Representation).** Which program representations are given to the model?
- **RQ2 (Integration).** How does the structure reach the model: in the prompt, through retrieval, by fine-tuning, through a static-analysis loop, or as an agent tool?
- **RQ3 (Task and scope).** For which tasks, code scopes, and languages is this evaluated?
- **RQ4 (Isolation).** Which studies isolate the representation's effect, and what do they show?

**Findings in brief.** (1) Retrieved context ({{repr_primary.retrieved_context}}) and hybrids ({{repr_primary.hybrid}}) are the most common primary representations, and the five integration routes are used about equally often. (2) The evidence concentrates in single-language, function-level detection; localisation has no dedicated study. (3) Of the {{isoaudit.n}} studies first classed as isolating the representation, {{isoaudit.survived}} survive a full-text audit; most of the rest add a pipeline stage or more input.

**Contributions.** (i) A map of {{N}} studies over seven facets, with every corpus count generated from the released data. (ii) A study-level audit of every claimed representation ablation, separating representation effects from pipeline effects (Table V and Supplementary Table S2). (iii) Number-level verification of all {{verification.claims}} extracted numeric claims. (iv) A replication package with the protocol, search strings, decisions, and scripts.

Section II describes the method, Section III the map (RQ1–RQ3), Section IV the isolation audit (RQ4), Section V the implications, and Section VI the threats to validity.

## II. Method

We follow Petersen et al.'s mapping process [@petersen2008systematic; @petersen2015guidelines] with Kitchenham and Charters' screening practice [@kitchenham2007guidelines]. The research questions, search strings, eligibility criteria, and facet scheme were fixed in a protocol before retrieval; every later deviation is a numbered, logged amendment.

### Search

*Sources.* We ran 16 scripted arXiv queries and 4 OpenAlex queries over 2023-01-01 to 2026-08-30, plus 14 known-item seed queries and DBLP sweeps of S&P, USENIX Security, CCS, NDSS, and ICSE listings. arXiv is the field's primary outlet: {{peer_reviewed.false}} of the {{N}} included studies are available only as preprints, and most venue papers also post an arXiv version. OpenAlex adds publisher metadata (ACM, IEEE, Springer, Elsevier), but our queries reached venue-only papers less well than preprints: the reference-list check (Section VI) found {{snowball.include_doi_only}} likely-eligible venue papers, found only by DOI, that the search missed. The planned citation snowballing was not run (deviation D1); Section VI reports a bounded substitute.

*Search evaluation.* A quasi-gold standard of 11 known-relevant studies was retrieved in full (11/11). One negative control was retrieved and correctly excluded. A borderline control was missed by the queries and added by a logged rescue, which shows that the query vocabulary under-reaches context-effect studies.

### Screening and selection

Table: Selection funnel.

| Stage | Records |
|---|---|
| Unique records retrieved | {{funnel.identified}} |
| After keyword pre-filter (security, structure or context, LLM) | {{funnel.prefilter_pass}} |
| Reached full-text extraction | {{funnel.extracted}} |
| Excluded at full text (reasons logged per record) | {{funnel.demoted}} |
| **Included corpus** | **{{N}}** |

A study was included if an LLM performs a security-analysis task on code (I1), grounded in a structural representation or engineered context, or measuring the effect of context (I2), with a quantitative result (I3), published 2023–2026 (I4). Exclusions covered prompt-only work, non-LLM structural detectors, agent-loop security, security of generated code, no quantitative result, withdrawn or duplicate records, and unretrievable full text.

A seeded 20% sample (n = {{screening_dual.n}}) was screened again blind. Include-versus-not agreement was {{screening_dual.agree}}/{{screening_dual.n}} (binary κ = {{screening_dual.kappa}}; κ = {{screening_dual.kappa_3way}} over include, exclude, and uncertain). All disagreements were *include* versus *uncertain*; the two screeners never disagreed on an exclusion ({{screening_dual.include_vs_exclude_flips}} include–exclude flips). Each disagreement was adjudicated, and four boundary rules (B1–B4) were added to the codebook in response.

### Classification scheme

Seven facets were coded per study: **representation** (raw text, AST, CFG/DFG, code property graph (CPG), slice, taint path, inter-procedural or call-graph context, retrieved context, natural-language structured rendering, hybrid; one primary, all mentions recorded); **integration** (prompt serialisation, retrieval guide, fine-tuning or adapter, neuro-symbolic analyser loop, agent tool use); **task**; **scope** and **domain**; **evaluation**; Wieringa **research type** [@wieringa2006requirements]; and **record type**. For each study we also extracted the reported structure-versus-baseline delta and a note recording exactly what differs between the compared conditions.

The evaluation facet carries RQ4. Its levels are defined in Table II.

Table: Evaluation levels (RQ4). A comparison counts toward the first three only if both arms use the same model and configuration on the same dataset and metric.

| Level | What differs between the compared arms |
|---|---|
| Strict representation-only | Only the input format changes; the input is capped, or the structured input is no longer than the raw code |
| Representation, unmatched input | Only the representation or context shown, but the structured arm is longer and input size is not controlled |
| Component ablation | A pipeline stage is added or removed (static confirmation, symbolic verifier, retrieval stage, memory, tool loop) |
| Not isolated | Model, training, architecture, or paradigm also differs, or there is no same-model comparison |
| Demonstrated / not evaluated | No comparison, or no evaluation |

### Extraction, verification, and reliability

LLM agents (Claude, Anthropic) extracted each study from its full text under a written codebook. Three checks followed.

*Number verification.* A separate agent re-fetched every source and checked every extracted number: {{verification.claims}} claims, {{verification.confirmed}} confirmed ({{verification.pct_confirmed}}%), {{verification.wrong}} wrong, {{verification.unretrievable}} unretrievable. All {{verification.wrong}} errors were extraction errors and were corrected to the source value. The later isolation audit found {{isoaudit.extra_extraction_errors}} further extraction errors in numbers this check had confirmed (e.g., values from a superseded arXiv version), so the confirmation rate is an upper bound on extraction accuracy. Errors found *in* the primary studies, such as a table and its text disagreeing, are recorded separately and not counted as extraction errors.

*Blind second coding.* A second agent re-coded {{kappa_coding.n}} of the {{N}} studies blind on three facets. Measured before adjudication, κ was {{kappa_coding.integration.kappa}} for integration, {{kappa_coding.repr_primary.kappa}} for representation, and {{kappa_coding.evaluation.kappa}} for evaluation. Both coders are runs of the same model family (Claude), so these values measure agreement between independent runs, not human reliability (Section VI).

*Isolation audit.* Because RQ4 rests on whether a comparison truly isolates the representation, we re-audited all {{isoaudit.n}} such studies at full text with the levels of Table II. Two checkers worked independently on pinned paper versions: Claude agents, and GPT (OpenAI) given only the paper text and the rule. For each study they recorded the model and configuration, dataset and metric, input-size control, what each arm shows, and any other change (Supplementary Table S2). When a paper contains several comparisons, the cleanest one counts. The checkers agreed on {{isoaudit.agree}} of {{isoaudit.n}} studies (κ = {{isoaudit.kappa}}); the authors decided the remaining {{isoaudit.decided_by_authors}}. For each case an assistant proposed a verdict with the two compared conditions and a supporting quote; an author checked it against the paper and accepted it in all {{isoaudit.decided_by_authors}} cases. The {{isoaudit.not_audited}} studies not first classed as isolating the representation were not re-audited, so strict comparisons hidden among them cannot be ruled out. The audit also found extraction errors, corrected in the data, and {{isoaudit.n_source_inconsistency}} inconsistencies inside the primary papers (e.g., a table and its text disagreeing), which are recorded but not counted as extraction errors.

### Synthesis

Synthesis is descriptive: frequency counts and cross-tabulations over the facets, plus narrative synthesis per cell (Table IV gives the facet distributions). Following Petersen, primary studies are not quality-scored; the evaluation facet records the strength of each study's evidence instead. Tasks, datasets, and metrics differ too much across studies to pool effect sizes, so none are pooled.

### Data availability

The protocol, search strings and hit counts, screening and adjudication decisions, the extraction database, verification and audit records, the correction log, and all scripts are released at https://anonymous.4open.science/r/structure-hunter-replication-E554/ (anonymised for review). Running the release's build regenerates every corpus count and statistic in this paper.

## III. The Map (RQ1–RQ3)

**RQ1: retrieved context leads, and structure is mostly an ingredient.** Retrieved context is the most common primary representation ({{repr_primary.retrieved_context}}), followed by hybrids ({{repr_primary.hybrid}}), raw text ({{repr_primary.raw_text}}), and taint paths ({{repr_primary.taint_path}}). Classical compiler structures are rarely primary: CPG {{repr_primary.cpg}}, AST {{repr_primary.ast}}, CFG/DFG {{repr_primary.cfg_dfg}}, slice {{repr_primary.slice}}. Many more studies use structure as a supporting input. Call-graph context appears in {{repr_any.interproc_callgraph}} studies but is primary in only {{repr_primary.interproc_callgraph}}. Table III gives one representative system per class.

Table: Primary representation, with one representative study per class.

| Representation | Primary | Any | Representative study |
|---|---|---|---|
| retrieved context | {{repr_primary.retrieved_context}} | {{repr_any.retrieved_context}} | Vul-RAG: retrieved vulnerability knowledge [@du2024vulrag] |
| hybrid | {{repr_primary.hybrid}} | {{repr_any.hybrid}} | ACFix: mined access-control graph for repair [@zhang2024acfix] |
| raw text | {{repr_primary.raw_text}} | {{repr_any.raw_text}} | GPTScan: raw code, with static confirmation of findings [@sun2023gptscan] |
| taint path | {{repr_primary.taint_path}} | {{repr_any.taint_path}} | IRIS: LLM-inferred taint specifications for CodeQL [@li2024iris] |
| CPG | {{repr_primary.cpg}} | {{repr_any.cpg}} | LLM4FPM: CPG slices for false-positive triage [@chen2024llm4fpm] |
| AST | {{repr_primary.ast}} | {{repr_any.ast}} | VulMaster: serialised AST in repair inputs [@zhou2024vulmaster] |
| call graph | {{repr_primary.interproc_callgraph}} | {{repr_any.interproc_callgraph}} | Lira26: caller/callee bodies appended [@lira2026lira26] |
| CFG/DFG | {{repr_primary.cfg_dfg}} | {{repr_any.cfg_dfg}} | MSIVD: flow-graph embeddings fused into an LLM [@yang2024msivd] |
| slice | {{repr_primary.slice}} | {{repr_any.slice}} | LLMxCPG: CPG-guided slices [@lekssays2025llmxcpg] |
| NL-structured | {{repr_primary.nl_structured}} | {{repr_any.nl_structured}} | Khan24: structural cues rendered as prose [@khan2024khan24] |

**RQ2: five integration routes, none dominant.** Prompt serialisation ({{integration.prompt_serialization}}), neuro-symbolic analyser loops ({{integration.neurosymbolic_analyzer_loop}}), fine-tuning or adapters ({{integration.finetune_adapter}}), agent tool use ({{integration.agent_tool_use}}), and retrieval guides ({{integration.retrieval_guide}}) are used about equally. The route decides what structure *can* do. Serialised into a prompt, it adds input. In a neuro-symbolic loop it checks the model's output, as when GPTScan's static data-flow confirmation removes false-positive candidates [@sun2023gptscan]. As an agent tool, the model fetches structure on demand, as with VulnAgent-R2's budgeted cross-file evidence gathering [@meng2026vulnagentr2]. Three studies described as agents were recoded after full-text reading, two as retrieval guides and one as prompt serialisation; framing alone does not settle this boundary.

**RQ3: function-level, single-language detection dominates.** Detection is the primary task in {{task.detection}} studies, followed by repair ({{task.repair}}), multi-task ({{task.multi}}), and triage ({{task.triage_fp_reduction}}). No study makes localisation its primary task. Scope skews small (function {{scope.function}}, inter-procedural {{scope.interprocedural}}, repository {{scope.repository}}, file {{scope.file}}); {{cross_language.false}} studies evaluate in a single language; {{domain.general}} target general-purpose code, with smart contracts ({{domain.smart_contract}}), web/JavaScript ({{domain.web_js}}), binaries ({{domain.binary}}), and hardware RTL ({{domain.hardware_rtl}}) at the margins. The field is young and accelerating ({{year.2023}}, {{year.2024}}, {{year.2025}}, and {{year.2026}} studies for 2023–2026, the last a partial year). Only {{peer_reviewed.true}} of {{N}} studies are peer-reviewed.

Table: Facet distributions (n = {{N}}).

| Facet | Value | n | Facet | Value | n |
|---|---|---|---|---|---|
| Task | detection | {{task.detection}} | Scope | function | {{scope.function}} |
| | repair | {{task.repair}} | | inter-procedural | {{scope.interprocedural}} |
| | multi-task | {{task.multi}} | | repository | {{scope.repository}} |
| | triage | {{task.triage_fp_reduction}} | | file | {{scope.file}} |
| Research type | validation | {{wieringa.validation}} | Record type | technique/tool | {{record_type.technique_tool}} |
| | evaluation | {{wieringa.evaluation}} | | empirical study | {{record_type.empirical_study}} |
| | solution proposal | {{wieringa.solution_proposal}} | | benchmark | {{record_type.benchmark_eval}} |
| Cross-language | yes | {{cross_language.true}} | Peer-reviewed | yes | {{peer_reviewed.true}} |

**Preprints versus peer-reviewed studies.** Peer-reviewed and preprint studies differ less than one might expect: {{pr_x_evaluation.peer.repr_strict}} of the {{peer_reviewed.true}} peer-reviewed studies and {{pr_x_evaluation.preprint.repr_strict}} of the {{peer_reviewed.false}} preprints contain a strict isolation, and component ablations are, if anything, more common among preprints ({{pr_x_evaluation.preprint.component_ablation}} vs {{pr_x_evaluation.peer.component_ablation}}). The larger difference is scope: repository-scale work is almost entirely preprint ({{pr_x_scope.preprint.repository}} of {{scope.repository}}), and all {{task.multi}} multi-task studies are preprints. The newest, largest-scope designs therefore rest on unreviewed reports.

## IV. RQ4: Does the Representation Itself Help?

**Answer: rarely.** Only {{evaluation.repr_strict}} of {{N}} studies change the representation alone while holding the model and the input size fixed, and {{isoaudit.strict_not_program_structure}} of those vary something other than program structure. Of the {{isoaudit.n}} studies first coded as representation-only ablations, {{isoaudit.survived}} survived the full-text audit (Table V).

Table: Outcome of the full-text isolation audit ({{isoaudit.n}} studies first coded as representation-only).

| Final level | Studies | Typical pattern |
|---|---|---|
| Strict representation-only | {{evaluation.repr_strict}} | Same model; the structured input is capped or shorter |
| Representation, unmatched input | {{evaluation.repr_unmatched_budget}} | Structure or context *added* to the prompt, input size not controlled |
| Component ablation | {{evaluation.component_ablation}} | A static checker, verifier, retrieval stage, memory, or agent loop removed |
| Not isolated | {{isoaudit.final_not_isolated}} | A trained module or the architecture changes |

*What the strict set shows.* The {{isoaudit.strict_program_structure}} strict studies that vary program structure all report gains, of very different size and on different metrics. RepBench gives ten representations to one model under a 50,000-character cap; an AST-plus-PDG rendering reaches 83.2% curated accuracy against 53.5% for raw source, but 43.9% of raw-source prompts were clipped by the cap [@stoltman2026repbench]. LLMxCPG's slices beat full code by 9.4–23.8 points of accuracy on three datasets, though the model was fine-tuned on slices, so this is an upper bound [@lekssays2025llmxcpg]. Retrieved examples beat random examples at equal shot count, 71.43% against 65.69% F1 in Trad25 [@trad2025trad25]; the example count is matched but token length is not reported, so Trad25 meets the strict level only if equal example count is accepted as matching (one checker did not accept it, which would leave four). CPG slices add 3.0 points of accuracy for false-positive triage [@chen2024llm4fpm], and a mined access-control graph adds 5.1 points of repair success [@zhang2024acfix], though up to 5 of the 6 cases it gains may be token-limit failures of the raw-code arm. In four of these five the structured input is *shorter* than the raw code, and in three the raw-code arm is truncated or overflows the context window. The strict evidence is therefore consistent with structure acting as a *selector* that fits the relevant code into the window; how much of the gain is selection and how much is the raw arm not fitting, these studies cannot say. The two flagged strict studies vary a query-language specification (MoCQ [@li2025mocq]) and comment deletion (Li25 [@li2025li25]); they show that what the model is shown matters, not that program structure helps.

*What the other comparisons show.* Most "structure helps" results test something larger. Component ablations measure a pipeline: static data-flow confirmation removes most false-positive candidates [@sun2023gptscan], a validator raises a bug-hunting agent's precision [@guo2025repoaudit], and Lean 4 verification improves memory-safety verdicts [@zhao2026leanguard]. These are real results about systems, but they do not say the model reads structure better than text. Unmatched-input comparisons add structure on top of the code, so they cannot separate structure from quantity. One of them, Lira26 [@lira2026lira26], reports *lower* F1 for most models when caller and callee bodies roughly double the prompt; it cannot say whether the amount or the type of context is responsible.

*Heterogeneity.* The strict studies span detection, triage, and repair, different datasets, and accuracy, F1, and repair-success metrics. We therefore report direction and range only; a pooled effect would be meaningless.

## V. Implications

**For tool builders.** Pay for structure where it selects or checks, not where it merely adds. The strict evidence favours structure that cuts the input down to the relevant code (slices, mined graphs, retrieved examples); the component evidence favours structure that checks the model's verdict (static confirmation, validators, symbolic verification). Appending more context without a selector is not supported by any isolated evidence in this corpus. Of 20 systems checked for public code, 8 had a discoverable repository; that figure describes those 20 only (Section VI).

**For researchers and reviewers.** The missing experiment is clear: one benchmark, several representations, one model, and one input budget, across vulnerability classes and at repository scale. RepBench comes closest but uses a single model, and no public artifact was found for it in one targeted search. When reading an "ablation" table, ask what exactly differs between the arms; of the {{isoaudit.n}} studies we first coded as representation ablations, {{isoaudit.survived}} held up under that question. Localisation (no dedicated study), triage ({{task.triage_fp_reduction}}), cross-language evaluation ({{cross_language.true}}), and non-general domains are the thinnest cells.

## VI. Threats to Validity

We use Petersen's four categories [@petersen2015guidelines].

**Descriptive validity: do the data describe the studies correctly?** Every extracted number was re-checked at source; {{verification.wrong}} of {{verification.claims}} were wrong and were corrected to the source value, and the isolation audit later found {{isoaudit.extra_extraction_errors}} more that the first check had missed. Extraction used selected full-text passages rather than whole papers; for the isolation claims, which carry the main conclusion, both auditors read the full text of every study. Several of the extraction errors were exactly the kind partial reading produces: a wrong table row, relative and percentage-point changes confused, numbers from a superseded arXiv version. Residual errors in the descriptive facets of the remaining studies are likely of these kinds.

**Theoretical validity: did we capture the right studies and classes?** (i) *Coverage.* Two databases plus seeding and venue sweeps cannot guarantee completeness, and the planned snowballing was not run. As a bounded substitute, we checked the reference lists of all {{snowball.papers}} audited studies ({{snowball.resolved}} resolvable in Semantic Scholar, {{snowball.refs}} references). We kept references from 2023 onward whose *titles* matched our search keywords but that the search had not retrieved: {{snowball.flagged}} papers, {{snowball.already_in_corpus}} of them already in the corpus under another title. One agent screened the rest on title and abstract: {{snowball.include}} are likely eligible, {{snowball.uncertain}} uncertain, {{snowball.exclude}} excluded; {{snowball.include_doi_only}} of the likely-eligible ones were found only by DOI. The corpus is therefore a substantial but incomplete sample, weakest on 2023–2024 venue papers. We did not add these studies: one level of references from a subset of the corpus is not a systematic search, and adding them would bias the sample toward the audited studies' citation neighbourhood. They are listed in the replication package. Counts and absences in this map describe the searched corpus, not the whole field. (ii) *Classification.* Screening agreement was moderate (binary κ = {{screening_dual.kappa}}), entirely on include-versus-uncertain calls. Facet agreement was substantial for integration (κ = {{kappa_coding.integration.kappa}}) but only moderate for representation ({{kappa_coding.repr_primary.kappa}}), where most disagreements involve the *hybrid* class, and for evaluation ({{kappa_coding.evaluation.kappa}}). The fine class boundaries, for example hybrid versus its components, should therefore be read as soft; the conclusions rest on the isolation audit, which was checked twice at full text for the {{isoaudit.n}} audited studies.

**Interpretive validity: are the conclusions supported?** (i) *LLM coding.* All coding was done by LLM agents. The facet κ compares two runs of the same model family, so it shows that coding is stable across runs, not that a human would assign the same codes; biases shared by the runs, such as a preference for a paper's own framing, would not show up in κ. Only the isolation audit used a second family (GPT; κ = {{isoaudit.kappa}} against Claude). Human judgement entered at the rule level (boundary rules, adjudication) and in the isolation audit, where an author checked and accepted an assistant-proposed verdict for each of the {{isoaudit.decided_by_authors}} disagreements. No blind human coding was done; human-versus-agent agreement is therefore unknown, and this is the study's main reliability gap. (ii) *Heterogeneity.* The reported deltas span different datasets, metrics, and vulnerability classes, so we report their range and direction, never a pooled effect. (iii) *Artifact survey.* The 20 systems checked for public code were chosen purposively during the original study, to cover its headline systems plus representation-class and venue diversity (one listed system was not in the corpus and was replaced). They do not include every study in the revised strict set. One targeted search per system was run, so "no artifact" means none was found. The 8/20 figure describes that selection only, not the corpus. (iv) *Absences.* An empty cell means no study in *this corpus*. Sampling was not a factor at screening (all {{funnel.prefilter_pass}} candidates were screened), but coverage was: the absence of dedicated localisation studies or of strict isolations in some classes may partly reflect what two databases retrieve.

**Repeatability.** Searches are scripted with logged strings and hit counts; sampling seeds are fixed; every decision, correction, and audit record is released; and every corpus count and statistic in this paper is generated from the released data by the released scripts. Values quoted from individual studies (Section IV) are taken from the audit records in Supplementary Table S2.

## VII. Conclusion

Structural grounding of LLM security analysis is a large, fast-growing, and mostly unreviewed literature. Read strictly, it shows that pipelines built around structure work. Whether the representation itself helps is tested by only {{isoaudit.strict_program_structure}} of the {{isoaudit.n}} audited studies; all report gains, but in most of them the structured input is also shorter, and in three the raw-code baseline does not fit the context window. The evidence sits in single-language, function-level detection. The experiment the field needs is one benchmark, several representations, one model, and one input budget.

## Declaration on the Use of AI {-}

LLM agents (Claude, Anthropic; and GPT, OpenAI, for the second isolation check) carried out the scripted search, screening, full-text extraction, number verification, blind second coding, and isolation audit described in Section II, under written instructions from the authors. AI assistance was also used in drafting the manuscript. The authors wrote every boundary rule and made all analytical decisions; disagreements in the isolation audit were decided by an author checking an assistant-proposed verdict. The authors take full responsibility for the content, data, and conclusions.

## Appendix A — Complete corpus

{{table:corpus}}

## Appendix B — Isolation audit, study by study

{{table:isolation}}
