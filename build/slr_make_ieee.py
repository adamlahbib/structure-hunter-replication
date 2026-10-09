#!/usr/bin/env python3
"""Generic IEEE preprocessor for an SLR study. Usage: python3 slr_make_ieee.py <stage6_report_folder>
Reads <folder>/report.md + _citekeys.json -> writes <folder>/paper_body.md."""
import json, re, sys
BASE = sys.argv[1].rstrip("/")
report = open(f"{BASE}/report.md").read()
bibkeys = {e["key"] for e in json.load(open(f"{BASE}/_citekeys.json"))}

m = re.search(r"\n(## .*Introduction)", report)
body = report[m.start():] if m else report
body = re.sub(r"\n##\s+References\b.*?(?=\n##\s|\Z)", "\n", body, flags=re.S)

def keys_in(s): return [k for k in re.findall(r"@([A-Za-z][A-Za-z0-9]+)", s) if k in bibkeys]
def repl_bracket(mm):
    ks = keys_in(mm.group(0))
    return "\\cite{" + ",".join(dict.fromkeys(ks)) + "}" if ks else mm.group(0)
body = re.sub(r"\[[^\]\[]*@[^\]\[]*\]", repl_bracket, body)
body = re.sub(r"(?<![\w@])@([A-Za-z][A-Za-z0-9]+)", lambda mm: "\\cite{" + mm.group(1) + "}" if mm.group(1) in bibkeys else mm.group(0), body)
body = re.sub(r"^(#{2,3})\s+(?:[IVXLC]+|\d+)\.\s+", r"\1 ", body, flags=re.M)

sym = {"→": r"\ensuremath{\rightarrow}", "←": r"\ensuremath{\leftarrow}", "↔": r"\ensuremath{\leftrightarrow}",
       "⇒": r"\ensuremath{\Rightarrow}", "×": r"\ensuremath{\times}", "≈": r"\ensuremath{\approx}",
       "≥": r"\ensuremath{\geq}", "≤": r"\ensuremath{\leq}", "≫": r"\ensuremath{\gg}", "≪": r"\ensuremath{\ll}",
       "±": r"\ensuremath{\pm}", "≠": r"\ensuremath{\neq}", "·": r"\ensuremath{\cdot}",
       "—": "---", "–": "--", "…": r"\ldots{}", "✓": "Y", "✗": "N", "≃": r"\ensuremath{\simeq}",
       "∧": r"\ensuremath{\wedge}", "∨": r"\ensuremath{\vee}", "→": r"\ensuremath{\rightarrow}", "≠": r"\ensuremath{\neq}",
       "τ": r"\ensuremath{\tau}", "κ": r"\ensuremath{\kappa}", "²": r"\ensuremath{^{2}}", "^k": r"\ensuremath{^{k}}"}
for u, t in sym.items():
    body = body.replace(u, t)

# split off the appendices: they render one-column with page-breaking longtables (pandoc default),
# so long data tables (corpus/evidence matrix) don't overflow non-breaking two-column floats.
midx = body.find("\n## Appendix")
mainbody = body if midx == -1 else body[:midx]
appbody = "" if midx == -1 else body[midx:]
open(f"{BASE}/paper_appendix.md", "w").write(appbody)
lines = mainbody.split("\n")
out, i, tc = [], 0, 0
def is_row(l): return l.strip().startswith("|")
def is_sep(l): return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", l))
def esc(c):
    c = c.strip()
    c = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", c)
    c = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\\emph{\1}", c)
    for ch in "&%#_":
        c = re.sub(r"(?<!\\)" + re.escape(ch), "\\" + ch, c)
    return c
while i < len(lines):
    if is_row(lines[i]) and i + 1 < len(lines) and is_sep(lines[i + 1]):
        j = i
        while j < len(lines) and is_row(lines[j]): j += 1
        block = [l for l in lines[i:j] if is_row(l)]
        header = [esc(c) for c in block[0].strip().strip("|").split("|")]
        data = [[esc(c) for c in r.strip().strip("|").split("|")] for r in block[2:]]
        n = len(header); tc += 1
        # "Table: <caption>" on the line(s) just above the table becomes its caption; IEEEtran
        # already prints "TABLE N", so the fallback is an empty caption (no "Table N." duplicate).
        cap = ""
        while out and not out[-1].strip(): out.pop()
        if out and out[-1].startswith("Table:"): cap = esc(out.pop()[6:])
        if n > 8:
            out += ["", "\\begin{table*}[t]", "\\centering", "\\scriptsize", "\\caption{" + cap + "}",
                    "\\resizebox{\\textwidth}{!}{%", "\\begin{tabular}{@{}l" + "l" * (n - 1) + "@{}}", "\\toprule",
                    " & ".join(header) + " \\\\", "\\midrule"]
            for r in data: out.append(" & ".join((r + [""] * n)[:n]) + " \\\\")
            out += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}", ""]
        else:
            if n > 1:
                # content-aware widths: short/numeric columns get natural narrow width
                # (right-aligned); text columns share the remaining width in proportion to their
                # content, so labels sit on one line instead of wrapping (shorter, denser tables).
                cw = [max([len(header[c])] + [len(r[c]) for r in data if c < len(r)]) for c in range(n)]
                xcols = [c for c in range(n) if cw[c] > 8]
                if xcols:
                    k = len(xcols); tot = float(sum(cw[c] for c in xcols))
                    spec = []
                    for c in range(n):
                        if c in xcols:
                            w = cw[c] / tot * k
                            spec.append(">{\\hsize=%.3f\\hsize\\raggedright\\arraybackslash}X" % w)
                        else:
                            spec.append("r")
                    cs = "@{}" + " ".join(spec) + "@{}"
                else:
                    cs = "@{}l" + " r" * (n - 1) + "@{}"
            else:
                cs = "@{}X@{}"
            out += ["", "\\begin{table*}[t]", "\\centering", "\\footnotesize", "\\caption{" + cap + "}",
                    "\\begin{tabularx}{\\textwidth}{" + cs + "}", "\\toprule", " & ".join(header) + " \\\\", "\\midrule"]
            for r in data: out.append(" & ".join((r + [""] * n)[:n]) + " \\\\")
            out += ["\\bottomrule", "\\end{tabularx}", "\\end{table*}", ""]
        i = j
    else:
        out.append(lines[i]); i += 1
open(f"{BASE}/paper_body.md", "w").write("\n".join(out))
print(f"{BASE}: paper_body.md written, {tc} tables, {body.count(chr(92)+'cite{')} cites")
