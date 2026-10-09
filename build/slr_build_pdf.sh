#!/usr/bin/env bash
# Generic IEEE PDF build for an SLR study.
# Usage: slr_build_pdf.sh <stage6_folder> "<TITLE>" [split]
#   split: keep paper.pdf to the two-column main body only (<=8 pp conference limit)
#          and build the appendices as a separate supplementary.pdf.
set -e
BASE="$1"; TITLE="$2"; MODE="${3:-inline}"; AUTHORS="${4:-full}"; PAPER="${5:-letter}"   # PAPER=a4 -> a4paper
# Compress arXiv reference URLs to inline arXiv:ID notes (saves ~1 line/entry in IEEEtran;
# identifiers stay resolvable). Idempotent; non-arXiv URLs (DOIs, method refs) untouched.
BASE="$BASE" python3 - <<'PY'
import re, os
p = os.environ['BASE'] + '/references.bib'
bib = open(p).read()
def repl(m):
    return f"  note = {{arXiv:{m.group(1)}}}"
new = re.sub(r'  url = \{https?://arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?\}', repl, bib)
new = new.replace('  howpublished = {arXiv preprint},\n  note = {arXiv:', '  note = {arXiv preprint arXiv:')
if new != bib:
    open(p, 'w').write(new)
    print('references.bib: arXiv URLs compressed to arXiv:ID notes')
PY
python3 "$(dirname "$0")/slr_make_ieee.py" "$BASE"
pandoc "$BASE/paper_body.md" --from=markdown+raw_tex+tex_math_dollars+pipe_tables --to=latex \
  --wrap=preserve --shift-heading-level-by=-1 -o "$BASE/paper_body.tex"
if [ -s "$BASE/paper_appendix.md" ]; then
  pandoc "$BASE/paper_appendix.md" --from=markdown+raw_tex+tex_math_dollars+pipe_tables --to=latex \
    --wrap=preserve --shift-heading-level-by=-1 -o "$BASE/paper_appendix.tex"
else
  : > "$BASE/paper_appendix.tex"
fi
BASE="$BASE" TITLE="$TITLE" MODE="$MODE" AUTHORS="$AUTHORS" PAPER="$PAPER" python3 - <<'PY'
import re, os
BASE=os.environ['BASE']; TITLE=os.environ['TITLE']; MODE=os.environ['MODE']
AUTHORS=os.environ.get('AUTHORS','full')
report=open(f'{BASE}/report.md').read()
m=re.search(r'##\s+Abstract\s*\n+(.*?)\n##\s', report, re.S)
absec=m.group(1) if m else ''
kwm=re.search(r'\*\*Keywords:\*\*\s*(.+)', absec)
kw=kwm.group(1).strip() if kwm else ''
if kwm: absec=absec[:kwm.start()]
ab=' '.join(absec.split()) if m else ''
ab=ab.replace('&',r'\&').replace('%',r'\%')
ab=re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', ab)
ab=re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'\\emph{\1}', ab)
sym={"→":r"\ensuremath{\rightarrow}","×":r"\ensuremath{\times}","≥":r"\ensuremath{\geq}","≤":r"\ensuremath{\leq}",
     "≫":r"\ensuremath{\gg}","–":"--","—":"---","…":r"\ldots{}","·":r"\ensuremath{\cdot}",
     "τ":r"\ensuremath{\tau}","κ":r"\ensuremath{\kappa}","²":r"\ensuremath{^{2}}"}
for u,t in sym.items(): ab=ab.replace(u,t)
auth_anon=r"""\author{\IEEEauthorblockN{Anonymous Authors}\IEEEauthorblockA{Affiliation withheld for double-blind review}}"""
auth = auth_anon
docopt = '[conference,a4paper]' if os.environ.get('PAPER')=='a4' else '[conference]'
body=open(f'{BASE}/paper_body.tex').read()
fonts=r'''\usepackage{fontspec}
\setmainfont{texgyretermes}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\setsansfont{texgyreheros}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\setmonofont{texgyrecursor}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
'''
pre=r'''\documentclass%DOCOPT%{IEEEtran}
\IEEEoverridecommandlockouts
\makeatletter
\newcommand{\linebreakand}{\end{@IEEEauthorhalign}\hfill\mbox{}\par\mbox{}\hfill\begin{@IEEEauthorhalign}}
\makeatother
\usepackage{cite}\usepackage{amsmath}
''' + fonts + r'''\usepackage{calc}\usepackage{booktabs}\usepackage{array}\usepackage{tabularx}\usepackage{longtable}\usepackage{graphicx}\usepackage{xcolor}
\usepackage[hidelinks,breaklinks]{hyperref}\usepackage{url}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\renewcommand{\arraystretch}{1.15}
\setcounter{totalnumber}{8}\setcounter{topnumber}{4}\setcounter{dbltopnumber}{4}
\renewcommand{\topfraction}{0.95}\renewcommand{\dbltopfraction}{0.95}\renewcommand{\textfraction}{0.05}\renewcommand{\floatpagefraction}{0.7}
\title{%TITLE%}
%AUTH%
\begin{document}\maketitle
\begin{abstract}
%ABSTRACT%
\end{abstract}
%KEYWORDS%
'''
bib=r'''
\begingroup\renewcommand{\footnotesize}{\scriptsize}\setlength{\baselineskip}{0.92\baselineskip}
\bibliographystyle{IEEEtran}
\bibliography{references}
\endgroup
'''
inline_tail=bib+r'''\clearpage
\onecolumn
\footnotesize
\input{paper_appendix.tex}
\end{document}
'''
split_tail=bib+r'''\end{document}
'''
tail = split_tail if MODE=='split' else inline_tail
kwblock=(r"\begin{IEEEkeywords}"+kw+r"\end{IEEEkeywords}") if kw else ""
open(f'{BASE}/paper.tex','w').write(pre.replace('%DOCOPT%',docopt).replace('%TITLE%',TITLE).replace('%ABSTRACT%',ab).replace('%AUTH%',auth).replace('%KEYWORDS%',kwblock)+body+tail)
print('assembled paper.tex (mode=%s)' % MODE)
if MODE=='split':
    supp=r'''\documentclass%DOCOPT%{IEEEtran}
\IEEEoverridecommandlockouts
\makeatletter
\newcommand{\linebreakand}{\end{@IEEEauthorhalign}\hfill\mbox{}\par\mbox{}\hfill\begin{@IEEEauthorhalign}}
\makeatother
\usepackage{cite}\usepackage{amsmath}
''' + fonts + r'''\usepackage{calc}\usepackage{booktabs}\usepackage{array}\usepackage{tabularx}\usepackage{longtable}\usepackage{graphicx}\usepackage{xcolor}
\usepackage[hidelinks,breaklinks]{hyperref}\usepackage{url}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\renewcommand{\arraystretch}{1.15}
\renewcommand{\thetable}{S\arabic{table}}
\title{Supplementary Material (Appendices) for:\\ \large %TITLE%}
%AUTH%
\begin{document}\maketitle
\onecolumn
\footnotesize
\input{paper_appendix.tex}
\nocite{*}
\bibliographystyle{IEEEtran}
\bibliography{references}
\end{document}
'''
    open(f'{BASE}/supplementary.tex','w').write(supp.replace('%DOCOPT%',docopt).replace('%TITLE%',TITLE).replace('%AUTH%',auth))
    print('assembled supplementary.tex')
PY
( cd "$BASE" && tectonic paper.tex --keep-logs 2>&1 | grep -iE "error|could not represent|undefined control" | grep -viE "underfull|overfull|badness|warning: warnings" || true )
if [ "$MODE" = "split" ]; then
  ( cd "$BASE" && tectonic supplementary.tex --keep-logs 2>&1 | grep -iE "error|could not represent|undefined control" | grep -viE "underfull|overfull|badness|warning: warnings" || true )
  echo "Built supplementary: $(ls -la "$BASE/supplementary.pdf" 2>/dev/null | awk '{print $5" bytes"}')"
fi
echo "Built: $(ls -la "$BASE/paper.pdf" 2>/dev/null | awk '{print $5" bytes"}')"
