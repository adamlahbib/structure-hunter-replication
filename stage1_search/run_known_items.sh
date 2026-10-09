#!/usr/bin/env bash
# known-item / snowball-seed queries (strategy 2 of 3) + quasi-gold-standard
# retrieval, incl. borderline cases and negative controls (00_protocol.md §2).
set -u
# Helpers: github.com/lingzhi227/agent-research-skills @ 9e6c085 (not redistributed). Set ARS_DIR to a checkout.
DR="${ARS_DIR:?set ARS_DIR to a checkout of agent-research-skills}/skills/deep-research/scripts"
R="$(cd "$(dirname "$0")" && pwd)/results"
mkdir -p "$R"
ki() { python3 "$DR/search_arxiv.py" --query "$1" --max-results 5 --sort-by relevance --start-date 2022-06-01 -o "$R/ki_$2" 2>&1 | tail -1; sleep 3; }

ki "LLMxCPG context-aware vulnerability detection code property graph" llmxcpg.jsonl
ki "K-ASTRO structure-aware adaptation transformers code vulnerability" kastro.jsonl
ki "SCALE structured natural language comment trees vulnerability" scale.jsonl
ki "IRIS LLM-assisted static analysis whole-project security" iris.jsonl
ki "Vul-RAG vulnerability detection knowledge-level RAG" vulrag.jsonl
ki "RepoAudit autonomous LLM agent repository code auditing" repoaudit.jsonl
ki "VulTriage context augmentation LLM vulnerability detection" vultriage.jsonl
ki "CLEAR causal context agentic reasoning vulnerability" clear.jsonl
ki "representation matters empirical program representations vulnerability reasoning" reprmatters.jsonl
ki "code representation false positive cross-language LLM vulnerability" reprfp.jsonl
ki "multitask self-instructed fine-tuning vulnerability detection" msivd.jsonl
# borderline (must be screened, expected include as context-effect study):
ki "evaluating large language models vulnerability detection variable context windows" bc_ctxwin.jsonl
# negative controls (expected exclusions if retrieved):
ki "DiverseVul new vulnerable source code dataset deep learning" nc_diversevul.jsonl
ki "prompt injection defense tool-using agent benchmark" nc_injection.jsonl
echo "known-item search done"
