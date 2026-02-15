#!/bin/bash
# =============================================================
# Observe Lab Room Subjects (N=3)
# Read-only view into subjects' workspaces and activity
#
# Usage:
#   ./observe.sh                    # All 6 subjects (summary)
#   ./observe.sh john-a-2           # Single subject (detailed)
#   ./observe.sh --pair 1           # Both in pair 1
#   ./observe.sh --compare          # Side-by-side SOUL.md + journal
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

ALL_SUBJECTS=("john-a-1" "john-b-1" "john-a-2" "john-b-2" "john-a-3" "john-b-3")
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
DIM='\033[2m'

observe_one() {
  local SUBJECT="$1"
  local CONTAINER="lab-${SUBJECT}"

  if [[ "$SUBJECT" == john-a-* ]]; then
    echo -e "${GREEN}🌑 ${SUBJECT} (shadow seed)${NC}"
  else
    echo -e "${MAGENTA}⚪ ${SUBJECT} (control)${NC}"
  fi
  echo "========================="

  if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "  ❌ OFFLINE"
    echo ""
    return
  fi

  echo ""
  echo "--- SOUL.md ---"
  docker exec "$CONTAINER" cat /workspace/SOUL.md 2>/dev/null || echo "(not found)"
  echo ""
  echo "--- Journal (last 40 lines) ---"
  docker exec "$CONTAINER" tail -40 /workspace/journal.md 2>/dev/null || echo "(not found)"
  echo ""
  echo "--- Workspace Files ---"
  docker exec "$CONTAINER" find /workspace -type f -name "*.md" -o -name "*.json" -o -name "*.js" -o -name "*.py" 2>/dev/null
  echo ""
  echo "--- Container Stats ---"
  docker stats --no-stream "$CONTAINER" 2>/dev/null
  echo ""
}

observe_summary() {
  echo -e "${CYAN}🧪 Lab Protocol — All Subjects Overview${NC}"
  echo "=========================================="
  echo ""

  for SUBJECT in "${ALL_SUBJECTS[@]}"; do
    local CONTAINER="lab-${SUBJECT}"
    local PAIR="${SUBJECT##*-}"

    if [[ "$SUBJECT" == john-a-* ]]; then
      ICON="🌑"
      TAG="shadow"
    else
      ICON="⚪"
      TAG="control"
    fi

    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
      FILES=$(docker exec "$CONTAINER" find /workspace -type f 2>/dev/null | wc -l | tr -d ' ')
      SOUL_LINES=$(docker exec "$CONTAINER" wc -l /workspace/SOUL.md 2>/dev/null | awk '{print $1}' || echo "?")
      JOURNAL_LINES=$(docker exec "$CONTAINER" wc -l /workspace/journal.md 2>/dev/null | awk '{print $1}' || echo "?")
      echo -e "  ${ICON} ${SUBJECT} (pair ${PAIR}, ${TAG})  ● Online  files=${FILES}  soul=${SOUL_LINES}L  journal=${JOURNAL_LINES}L"
    else
      echo -e "  ${ICON} ${SUBJECT} (pair ${PAIR}, ${TAG})  ○ Offline"
    fi
  done
  echo ""
}

compare_souls() {
  echo -e "${CYAN}🧪 SOUL.md Comparison — All Pairs${NC}"
  echo "====================================="
  echo ""

  for PAIR in 1 2 3; do
    echo -e "${CYAN}--- Pair ${PAIR} ---${NC}"
    for VARIANT in a b; do
      SUBJECT="john-${VARIANT}-${PAIR}"
      CONTAINER="lab-${SUBJECT}"
      if [[ "$VARIANT" == "a" ]]; then
        echo -e "${GREEN}🌑 ${SUBJECT} (shadow seed):${NC}"
      else
        echo -e "${MAGENTA}⚪ ${SUBJECT} (control):${NC}"
      fi
      if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
        docker exec "$CONTAINER" cat /workspace/SOUL.md 2>/dev/null || echo "(not found)"
      else
        echo "(offline)"
      fi
      echo ""
    done
  done
}

# Parse arguments
if [ $# -eq 0 ]; then
  observe_summary
elif [ "$1" = "--compare" ]; then
  compare_souls
elif [ "$1" = "--pair" ]; then
  observe_one "john-a-$2"
  observe_one "john-b-$2"
else
  observe_one "$1"
fi
