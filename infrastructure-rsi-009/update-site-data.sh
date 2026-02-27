#!/bin/bash
OUTPUT="/Users/miguelitodeguzman/Projects/individuationlab/website/public/data/rsi-009/data.json"
SUBJECTS="john-a-1 john-a-2 john-a-3 john-a-4 john-b-1 john-b-2 john-b-3 john-b-4"
GENERATED=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo '{' > "$OUTPUT"
echo '  "status": { "subjects": {' >> "$OUTPUT"

first=true
for sid in $SUBJECTS; do
  container="lab-rsi009-$sid"
  status=$(docker inspect -f '{{.State.Status}}' "$container" 2>/dev/null)
  if [ "$status" = "running" ]; then s="online"; else s="offline"; fi
  if [ "$first" = true ]; then first=false; else echo ',' >> "$OUTPUT"; fi
  printf '    "%s": {"status":"%s"}' "$sid" "$s" >> "$OUTPUT"
done

echo '' >> "$OUTPUT"
echo '  }},' >> "$OUTPUT"
echo '  "inventory": {' >> "$OUTPUT"

first_sub=true
for sid in $SUBJECTS; do
  container="lab-rsi009-$sid"
  if [ "$first_sub" = true ]; then first_sub=false; else echo ',' >> "$OUTPUT"; fi
  echo "    \"$sid\": { \"files\": [" >> "$OUTPUT"
  
  first_file=true
  for fpath in SOUL.md AGENTS.md journal.md EMOTIONS.md MEMORY.md HEARTBEAT.md; do
    content=$(docker exec "$container" cat "/workspace/$fpath" 2>/dev/null)
    if [ -n "$content" ]; then
      size=${#content}
      escaped=$(echo "$content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
      if [ "$first_file" = true ]; then first_file=false; else echo ',' >> "$OUTPUT"; fi
      printf '      {"path":"%s","size":%d,"content":%s}' "$fpath" "$size" "$escaped" >> "$OUTPUT"
    fi
  done
  
  # Check for extra files
  for fpath in $(docker exec "$container" find /workspace -maxdepth 2 -name "*.md" -o -name "*.py" -o -name "*.sh" -o -name "*.js" 2>/dev/null | grep -v node_modules | sort); do
    fname="${fpath#/workspace/}"
    # Skip already-captured files
    case "$fname" in SOUL.md|AGENTS.md|journal.md|EMOTIONS.md|MEMORY.md|HEARTBEAT.md) continue;; esac
    content=$(docker exec "$container" cat "$fpath" 2>/dev/null)
    if [ -n "$content" ]; then
      size=${#content}
      escaped=$(echo "$content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
      echo ',' >> "$OUTPUT"
      printf '      {"path":"%s","size":%d,"content":%s}' "$fname" "$size" "$escaped" >> "$OUTPUT"
    fi
  done
  
  echo '' >> "$OUTPUT"
  echo '    ]}' >> "$OUTPUT"
done

echo '' >> "$OUTPUT"
echo '  },' >> "$OUTPUT"
printf '  "generated": "%s",\n' "$GENERATED" >> "$OUTPUT"
echo '  "pairCount": 4,' >> "$OUTPUT"
echo '  "subjectCount": 8' >> "$OUTPUT"
echo '}' >> "$OUTPUT"

echo "✅ Generated $OUTPUT"
