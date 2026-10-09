#!/usr/bin/env bash
# database search (arXiv + OpenAlex). Strategy 1 of 3 (see 00_protocol.md §2).
set -u
# Helpers: github.com/lingzhi227/agent-research-skills @ 9e6c085 (not redistributed). Set ARS_DIR to a checkout.
DR="${ARS_DIR:?set ARS_DIR to a checkout of agent-research-skills}/skills/deep-research/scripts"
LS="$ARS_DIR/skills/literature-search/scripts"
R="$(cd "$(dirname "$0")" && pwd)/results"
mkdir -p "$R"
ax() { python3 "$DR/search_arxiv.py" --query "$1" --max-results "${3:-40}" --sort-by relevance --start-date 2023-01-01 -o "$R/$2" 2>&1 | tail -1; sleep 3; }
oa() { python3 "$LS/search_openalex.py" --query "$1" --max-results "${3:-40}" --year-range 2023-2026 --output "$R/$2" 2>&1 | tail -1; sleep 1; }

ax "LLM vulnerability detection graph structure" ax_graph.jsonl
ax "abstract syntax tree vulnerability detection language model" ax_ast.jsonl
ax "code property graph LLM vulnerability detection" ax_cpg.jsonl
ax "program slicing vulnerability detection large language model" ax_slice.jsonl
ax "taint analysis large language model vulnerability" ax_taint.jsonl
ax "context enhanced vulnerability detection LLM" ax_ctx.jsonl
ax "inter-procedural vulnerability detection LLM context" ax_interproc.jsonl
ax "LLM vulnerability localization repair context repository" ax_repair.jsonl
ax "static analysis large language model hybrid security detection" ax_hybrid.jsonl
ax "neuro-symbolic vulnerability detection reasoning" ax_neurosym.jsonl
ax "structure-aware fine-tuning code vulnerability" ax_finetune.jsonl
ax "smart contract vulnerability detection LLM slicing graph" ax_contract.jsonl
ax "repository-level vulnerability detection audit agent LLM" ax_repoaudit.jsonl
ax "program representation empirical study LLM vulnerability" ax_repr.jsonl
ax "retrieval augmented vulnerability detection knowledge CWE" ax_rag.jsonl
ax "false positive reduction static analysis LLM triage" ax_triage.jsonl

oa "program representation vulnerability detection large language model" oa_repr.jsonl
oa "graph large language model vulnerability detection" oa_graph.jsonl
oa "static analysis LLM security false positive" oa_static.jsonl
oa "slicing context vulnerability repair LLM" oa_slice.jsonl
echo "database search done: $(ls "$R" | wc -l) result files"
