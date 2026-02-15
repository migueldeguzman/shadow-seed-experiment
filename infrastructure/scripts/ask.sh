#!/bin/bash
# =============================================================
# Lab Protocol — Ask All Subjects a Question Simultaneously
# Sends the same prompt to all 6 subjects and shows side-by-side
#
# Usage:
#   ./ask.sh "What do you think about evil?"
#   ./ask.sh --pair 1 "Describe yourself."
#   ./ask.sh --shadow "What are you capable of?"
#   ./ask.sh --control "What are you capable of?"
#   ./ask.sh --subject john-a-2 "Tell me about yourself."
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
NC='\033[0m'
DIM='\033[2m'

TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
ALL_SUBJECTS=("john-a-1" "john-b-1" "john-a-2" "john-b-2" "john-a-3" "john-b-3")
TARGETS=()

# Parse flags
while [[ "$1" == --* ]]; do
  case "$1" in
    --pair)
      P="$2"; TARGETS=("john-a-${P}" "john-b-${P}"); shift 2 ;;
    --shadow)
      TARGETS=("john-a-1" "john-a-2" "john-a-3"); shift ;;
    --control)
      TARGETS=("john-b-1" "john-b-2" "john-b-3"); shift ;;
    --subject)
      TARGETS=("$2"); shift 2 ;;
    *) shift ;;
  esac
done

PROMPT="$1"
if [ -z "$PROMPT" ]; then
  echo -e "${RED}Usage: ./ask.sh [--pair N|--shadow|--control|--subject NAME] \"your message\"${NC}"
  exit 1
fi

# Default: all subjects
if [ ${#TARGETS[@]} -eq 0 ]; then
  TARGETS=("${ALL_SUBJECTS[@]}")
fi

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🧪 Lab Protocol — Multi-Subject Ask (N=3)       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${DIM}Prompt:  ${PROMPT}${NC}"
echo -e "${DIM}Time:    $(date -u +%Y-%m-%dT%H:%M:%SZ)${NC}"
echo -e "${DIM}Targets: ${TARGETS[*]}${NC}"
echo ""

PIDS=()
RESP_FILES=()
SUBJECTS_ASKED=()

for SUBJ in "${TARGETS[@]}"; do
  CONTAINER="lab-${SUBJ}"
  RESP="/tmp/${SUBJ}-${TIMESTAMP}.txt"
  RESP_FILES+=("$RESP")
  SUBJECTS_ASKED+=("$SUBJ")

  if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "CONTAINER NOT RUNNING" > "$RESP"
    PIDS+=("")
    continue
  fi

  echo -e "${DIM}📤 Sending to ${SUBJ}...${NC}"
  docker exec "$CONTAINER" bash -c "cd /workspace && claude -p --dangerously-skip-permissions '$(echo "$PROMPT" | sed "s/'/'\\\\''/g")' 2>&1" > "$RESP" &
  PIDS+=($!)
done

echo ""
echo -e "${DIM}⏳ Waiting for ${#TARGETS[@]} responses...${NC}"
echo ""

# Wait for all
for PID in "${PIDS[@]}"; do
  [ -n "$PID" ] && wait "$PID" || true
done

# Display results grouped by pair
DIVIDER="────────────────────────────────────────────────────"

for i in "${!SUBJECTS_ASKED[@]}"; do
  SUBJ="${SUBJECTS_ASKED[$i]}"
  RESP="${RESP_FILES[$i]}"

  # Color by type
  if [[ "$SUBJ" == john-a-* ]]; then
    COLOR="${GREEN}"
    ICON="🌑"
    TAG="shadow seed"
  else
    COLOR="${MAGENTA}"
    ICON="⚪"
    TAG="control"
  fi

  PAIR_NUM="${SUBJ##*-}"

  echo -e "${COLOR}┌${DIVIDER}┐${NC}"
  echo -e "${COLOR}│ ${ICON} ${SUBJ} (${TAG}) — Pair ${PAIR_NUM}${NC}"
  echo -e "${COLOR}└${DIVIDER}┘${NC}"
  cat "$RESP" 2>/dev/null || echo "(no response)"
  echo ""
done

# Save to monitor data
ASKLOG="/Users/miguelitodeguzman/ailab/lab-protocol/monitor/data/asks"
mkdir -p "$ASKLOG"

# Build JSON
JSONFILE="$ASKLOG/ask-${TIMESTAMP}.json"
echo "{" > "$JSONFILE"
echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$JSONFILE"
echo "  \"prompt\": $(python3 -c "import json; print(json.dumps('''$PROMPT'''))")," >> "$JSONFILE"
echo "  \"subjects\": {" >> "$JSONFILE"

for i in "${!SUBJECTS_ASKED[@]}"; do
  SUBJ="${SUBJECTS_ASKED[$i]}"
  RESP="${RESP_FILES[$i]}"
  COMMA=""
  [ "$i" -lt $((${#SUBJECTS_ASKED[@]} - 1)) ] && COMMA=","
  CONTENT=$([ -f "$RESP" ] && python3 -c "import json; print(json.dumps(open('$RESP').read()))" || echo "null")
  echo "    \"${SUBJ}\": ${CONTENT}${COMMA}" >> "$JSONFILE"
done

echo "  }" >> "$JSONFILE"
echo "}" >> "$JSONFILE"

echo -e "${DIM}Saved: $JSONFILE${NC}"

# Cleanup
for RESP in "${RESP_FILES[@]}"; do
  rm -f "$RESP"
done
