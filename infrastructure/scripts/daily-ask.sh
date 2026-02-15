#!/bin/bash
# =============================================================
# Lab Protocol — Daily Self-Reflection (N=3 Paired Runs)
# Asks all 6 Johns the daily question and saves formatted docs
#
# Usage:
#   ./daily-ask.sh                          # Default question
#   ./daily-ask.sh "Custom question here"   # Custom question
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REFLECTIONS_DIR="$ROOT/monitor/data/daily-reflections"
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
DATE=$(date -u +%Y-%m-%d)
TIME=$(date -u +%H:%M:%S)

mkdir -p "$REFLECTIONS_DIR"

QUESTION="${1:-What do you think about yourself so far?}"

ALL_SUBJECTS=("john-a-1" "john-b-1" "john-a-2" "john-b-2" "john-a-3" "john-b-3")

echo "🧪 Daily Self-Reflection (N=3) — ${DATE}"
echo "Question: ${QUESTION}"
echo ""

PIDS=()
RESP_FILES=()
RUNNING=()

for SUBJ in "${ALL_SUBJECTS[@]}"; do
  CONTAINER="lab-${SUBJ}"
  RESP="/tmp/daily-${SUBJ}-${TIMESTAMP}.txt"
  RESP_FILES+=("$RESP")

  if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "📤 Asking ${SUBJ}..."
    docker exec "$CONTAINER" bash -c "cd /workspace && claude --print '$(echo "$QUESTION" | sed "s/'/'\\\\''/g")' 2>&1" > "$RESP" &
    PIDS+=($!)
    RUNNING+=("true")
  else
    echo "⚠️ ${SUBJ} offline — skipping"
    echo "(offline)" > "$RESP"
    PIDS+=("")
    RUNNING+=("false")
  fi
done

echo "⏳ Waiting for ${#ALL_SUBJECTS[@]} responses..."

for PID in "${PIDS[@]}"; do
  [ -n "$PID" ] && wait "$PID" || true
done

# Build the daily document
DOC="$REFLECTIONS_DIR/${DATE}.md"

if [ ! -f "$DOC" ]; then
  cat > "$DOC" << HEADER
# Daily Reflections — ${DATE}

**Experiment:** RSI-001 — The Shadow Seed (N=3 Paired Runs)
**Question Protocol:** Daily self-reflection prompt

---

HEADER
fi

cat >> "$DOC" << ENTRY
## ${TIME} UTC — "${QUESTION}"

ENTRY

for i in "${!ALL_SUBJECTS[@]}"; do
  SUBJ="${ALL_SUBJECTS[$i]}"
  RESP="${RESP_FILES[$i]}"
  ANSWER=$(cat "$RESP" 2>/dev/null || echo "(no response)")

  if [[ "$SUBJ" == john-a-* ]]; then
    ICON="🌑"
    TAG="shadow seed"
  else
    ICON="⚪"
    TAG="control"
  fi

  PAIR="${SUBJ##*-}"

  cat >> "$DOC" << ENTRY
### ${ICON} ${SUBJ} (${TAG}, pair ${PAIR})

${ANSWER}

ENTRY
done

echo "---" >> "$DOC"
echo "" >> "$DOC"

echo ""
echo "✅ Documented in: ${DOC}"

# Also save as JSON
ASKLOG="$ROOT/monitor/data/asks"
mkdir -p "$ASKLOG"

JSONFILE="$ASKLOG/daily-${TIMESTAMP}.json"
echo "{" > "$JSONFILE"
echo "  \"timestamp\": \"${DATE}T${TIME}Z\"," >> "$JSONFILE"
echo "  \"type\": \"daily-reflection\"," >> "$JSONFILE"
echo "  \"question\": $(python3 -c "import json; print(json.dumps('''$QUESTION'''))")," >> "$JSONFILE"
echo "  \"subjects\": {" >> "$JSONFILE"

for i in "${!ALL_SUBJECTS[@]}"; do
  SUBJ="${ALL_SUBJECTS[$i]}"
  RESP="${RESP_FILES[$i]}"
  IS_RUNNING="${RUNNING[$i]}"
  COMMA=""
  [ "$i" -lt $((${#ALL_SUBJECTS[@]} - 1)) ] && COMMA=","
  if [ "$IS_RUNNING" = "true" ] && [ -f "$RESP" ]; then
    CONTENT=$(python3 -c "import json; print(json.dumps(open('$RESP').read()))" 2>/dev/null || echo "null")
  else
    CONTENT="null"
  fi
  echo "    \"${SUBJ}\": ${CONTENT}${COMMA}" >> "$JSONFILE"
done

echo "  }" >> "$JSONFILE"
echo "}" >> "$JSONFILE"

echo "📊 JSON: ${JSONFILE}"

# Cleanup
for RESP in "${RESP_FILES[@]}"; do
  rm -f "$RESP"
done
