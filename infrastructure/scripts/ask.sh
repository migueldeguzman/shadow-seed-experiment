#!/bin/bash
# =============================================================
# Lab Protocol — Ask Both Johns a Question Simultaneously
# Sends the same prompt to both subjects and shows replies
#
# Usage:
#   ./ask.sh "What do you think about evil?"
#   ./ask.sh "Describe yourself in one paragraph."
#   ./ask.sh --john-a "message"    # John A only
#   ./ask.sh --john-b "message"    # John B only
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
DIM='\033[2m'

TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
TARGET="both"

# Parse flags
if [ "$1" = "--john-a" ]; then
  TARGET="john-a"
  shift
elif [ "$1" = "--john-b" ]; then
  TARGET="john-b"
  shift
fi

PROMPT="$1"

if [ -z "$PROMPT" ]; then
  echo -e "${RED}Usage: ./ask.sh [--john-a|--john-b] \"your message\"${NC}"
  exit 1
fi

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🧪 Lab Protocol — Dual Ask                      ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${DIM}Prompt: ${PROMPT}${NC}"
echo -e "${DIM}Time:   $(date -u +%Y-%m-%dT%H:%M:%SZ)${NC}"
echo -e "${DIM}Target: ${TARGET}${NC}"
echo ""

RESP_A="/tmp/john-a-${TIMESTAMP}.txt"
RESP_B="/tmp/john-b-${TIMESTAMP}.txt"

ask_subject() {
  local SUBJECT="$1"
  local CONTAINER="lab-${SUBJECT}"
  local OUTFILE="$2"
  local LOGFILE="/workspace/logs/ask-${TIMESTAMP}.md"

  if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "CONTAINER NOT RUNNING" > "$OUTFILE"
    return 1
  fi

  # Run claude --print with the prompt, capture output
  docker exec "$CONTAINER" bash -c "cd /workspace && claude --print '$(echo "$PROMPT" | sed "s/'/'\\\\''/g")' 2>&1" > "$OUTFILE" &
}

# Fire both simultaneously
if [ "$TARGET" = "both" ] || [ "$TARGET" = "john-a" ]; then
  echo -e "${GREEN}🌑 Sending to John A...${NC}"
  ask_subject "john-a" "$RESP_A"
  PID_A=$!
fi

if [ "$TARGET" = "both" ] || [ "$TARGET" = "john-b" ]; then
  echo -e "${MAGENTA}⚪ Sending to John B...${NC}"
  ask_subject "john-b" "$RESP_B"
  PID_B=$!
fi

echo ""
echo -e "${DIM}Waiting for responses...${NC}"
echo ""

# Wait for both to finish
FAIL=0
if [ -n "$PID_A" ]; then
  wait $PID_A || FAIL=1
fi
if [ -n "$PID_B" ]; then
  wait $PID_B || FAIL=1
fi

# Display results
DIVIDER="────────────────────────────────────────────────────"

if [ "$TARGET" = "both" ] || [ "$TARGET" = "john-a" ]; then
  echo -e "${GREEN}┌${DIVIDER}┐${NC}"
  echo -e "${GREEN}│ 🌑 JOHN A (shadow seed)                            ${NC}"
  echo -e "${GREEN}└${DIVIDER}┘${NC}"
  cat "$RESP_A" 2>/dev/null || echo "(no response)"
  echo ""
fi

if [ "$TARGET" = "both" ] || [ "$TARGET" = "john-b" ]; then
  echo -e "${MAGENTA}┌${DIVIDER}┐${NC}"
  echo -e "${MAGENTA}│ ⚪ JOHN B (control)                                 ${NC}"
  echo -e "${MAGENTA}└${DIVIDER}┘${NC}"
  cat "$RESP_B" 2>/dev/null || echo "(no response)"
  echo ""
fi

# Save to monitor data
ASKLOG="/Users/miguelitodeguzman/ailab/lab-protocol/monitor/data/asks"
mkdir -p "$ASKLOG"
cat > "$ASKLOG/ask-${TIMESTAMP}.json" << ASKEOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "prompt": $(python3 -c "import json; print(json.dumps('''$PROMPT'''))"),
  "john-a": $([ -f "$RESP_A" ] && python3 -c "import json; print(json.dumps(open('$RESP_A').read()))" || echo "null"),
  "john-b": $([ -f "$RESP_B" ] && python3 -c "import json; print(json.dumps(open('$RESP_B').read()))" || echo "null")
}
ASKEOF

echo -e "${DIM}Saved to: $ASKLOG/ask-${TIMESTAMP}.json${NC}"

# Cleanup
rm -f "$RESP_A" "$RESP_B"
