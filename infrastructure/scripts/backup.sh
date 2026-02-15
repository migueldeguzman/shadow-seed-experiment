#!/bin/bash
# =============================================================
# Lab Protocol — Backup All Subject Workspaces (N=6)
# Archives full workspace contents to host storage
#
# Usage:
#   ./backup.sh              # All 12 subjects
#   ./backup.sh john-a-2     # Single subject
#   ./backup.sh --pair 1     # Pair 1 only
#
# Author: Mia 🌸 | Date: 2026-02-15 | Updated: N=6
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAB_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$LAB_DIR/experiments/rsi-001/data/backups"
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)

ALL_SUBJECTS=("john-a-1" "john-b-1" "john-a-2" "john-b-2" "john-a-3" "john-b-3" "john-a-4" "john-b-4" "john-a-5" "john-b-5" "john-a-6" "john-b-6")
TARGETS=()

if [ $# -eq 0 ]; then
  TARGETS=("${ALL_SUBJECTS[@]}")
elif [ "$1" = "--pair" ]; then
  TARGETS=("john-a-$2" "john-b-$2")
else
  TARGETS=("$1")
fi

echo "📦 Backing up ${#TARGETS[@]} subject(s) at ${TIMESTAMP}"

for SUBJ in "${TARGETS[@]}"; do
  CONTAINER="lab-${SUBJ}"
  BACKUP_DIR="$DATA_DIR/${SUBJ}-${TIMESTAMP}"

  if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "  ⚠️ ${SUBJ}: offline, skipping"
    continue
  fi

  mkdir -p "$BACKUP_DIR"
  docker cp "${CONTAINER}:/workspace/." "$BACKUP_DIR/" 2>/dev/null

  FILES=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')
  SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
  echo "  ✅ ${SUBJ}: ${FILES} files, ${SIZE}"
done

echo ""
echo "📁 Backups at: $DATA_DIR"
