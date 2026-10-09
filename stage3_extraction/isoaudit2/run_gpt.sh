#!/usr/bin/env bash
# Second, independent isolation check (plan step 1). RUNS `codex exec` — user-gated; run only with approval.
# One call per record, read-only sandbox, no web; each call sees only that record's paper.txt.
set -u
here=$(cd "$(dirname "$0")" && pwd); out="$here/out"; mkdir -p "$out"
python3 - "$here" <<'PY' | while IFS=$'\t' read -r id; do
import json,glob,sys
for f in sorted(glob.glob(sys.argv[1]+'/../isoaudit_in/batch*.json')):
    for r in json.load(open(f)): print(r['arxiv_id'])
PY
  [[ -s "$out/$id.json" ]] && continue
  ws=$(mktemp -d); cp "$here/fulltext/$id.txt" "$ws/paper.txt"
  python3 - "$here" "$id" > "$ws/prompt" <<'PY'
import json,glob,sys
here,i=sys.argv[1],sys.argv[2]
r=[r for f in glob.glob(here+'/../isoaudit_in/batch*.json') for r in json.load(open(f)) if r['arxiv_id']==i][0]
t=open(here+'/prompt_template.txt').read()
print(t.replace('__ID__',i).replace('__SYS__',r['system'] or '').replace('__GAIN__',r.get('structure_gain') or 'none'))
PY
  ( cd "$ws" && codex exec --json --ephemeral --ignore-user-config --strict-config --skip-git-repo-check \
      --sandbox read-only -c approval_policy="never" --model gpt-5.6-terra -c model_reasoning_effort="medium" \
      -c web_search=disabled -c features.browser_use=false -c features.computer_use=false -c features.in_app_browser=false \
      < prompt > "$out/$id.raw" 2> "$out/$id.err" )
  jq -rs 'map(select(.type=="item.completed" and .item.type=="agent_message")|.item.text)|last // empty' "$out/$id.raw" > "$out/$id.json"
  if grep -qiE 'usage limit|rate limit|quota|too many requests|\b429\b' "$out/$id.err" \
       <(jq -r 'select(.type == "error" or .type == "turn.failed") | tostring' "$out/$id.raw" 2>/dev/null); then echo "QUOTA STOP at $id"; rm -f "$out/$id.json"; exit 2; fi
  echo "$id done"; rm -rf "$ws"
done
