# Replication package: "Does Structure Help the Hunter?"

A systematic mapping study of program representations and context in LLM-based security analysis
(68 studies, 2023–2026). This package holds everything needed to check or regenerate every number in the paper.

## Rebuild every number

```bash
cd stage3_extraction
python3 merge_extraction.py      # extraction chunks -> extraction.json
python3 compute_kappa.py         # reliability, PRE-adjudication (refuses adjudicated data)
python3 apply_adjudications.py   # corrections, recodes, isolation re-audit (amendment A2)
python3 summarize_verification.py
python3 ../stage5_map/make_map.py              # -> stage5_map/_map_stats.json
python3 ../stage6_report/render_report.py      # fills report.tmpl.md -> report.md; fails on any unfilled value
```

Python 3 standard library only. `build/slr_build_pdf.sh <stage6_report> "<title>" split anon a4` builds the PDFs (needs pandoc and tectonic).

## What is where

| Stage | Contents |
|---|---|
| `00_protocol.md` | Research questions, criteria, facet scheme, gold set; fixed before retrieval |
| `stage1_search/` | Search scripts and every query string with hit counts (`search_log.md`), retrieved records, gold-set recall audit, bounded reference-list check (`snowball_check.py`, `_snowball_check.json`, `_snowball_screen.json`) |
| `stage2_screening/` | Screening decisions per batch, the blind 20% dual-screen sample, adjudication with boundary rules B1–B4 and amendments (`decisions_adjudication.json`) |
| `stage3_extraction/` | `extraction.json` (the single source of truth), number verification (`verify_out/`, `verification.json`), blind second coding (`secondcode_out/`), `corrections_log.md` |
| `stage3_extraction/isoaudit_*`, `isoaudit2/` | Full-text isolation re-audit: checker A (`isoaudit_out/`), checker B (`isoaudit2/out/`, prompt and runner), author decisions on disagreements (`isoaudit2/human_decisions.json`), final verdicts (`isoaudit_final.json`) |
| `stage4_artifacts/` | Public-code survey of 20 purposively selected systems |
| `stage5_map/` | `make_map.py` and the derived statistics every manuscript count is read from |
| `stage6_report/` | Manuscript template, renderer, bibliography |

## Not included

Full texts of the primary studies (copyright). Each audit record names the exact arXiv version read, so the texts can be re-fetched.
Raw model transcripts are omitted; each checker's structured verdict, the comparison it judged and a deciding quote are included.
The arXiv and OpenAlex search helpers come from github.com/lingzhi227/agent-research-skills (commit 9e6c085) and are not
redistributed; set `ARS_DIR` to a checkout to re-run the searches.

## Tools used

LLM agents (Claude, Anthropic) did screening, extraction, verification and second coding under written instructions; GPT
(OpenAI, via the Codex CLI) was the second checker in the isolation re-audit. All disagreements and boundary decisions were
made by the authors and are recorded in the files above.
