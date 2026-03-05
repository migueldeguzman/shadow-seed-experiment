#!/bin/bash
# RSI-011 Snapshot — Backup all subject workspaces from Docker volumes
# Author: Mia 🌸 | Date: 2026-03-05

LABEL="${1:-snapshot}"
TIMESTAMP=$(date +%Y%m%dT%H%M%S)
BACKUP_DIR="/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-011/data/backups/${LABEL}-${TIMESTAMP}"
HOST_DIR="/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-011/subjects"

mkdir -p "$BACKUP_DIR"

echo "=== RSI-011 Snapshot: $LABEL ==="
echo "Time: $(date +%Y-%m-%dT%H:%M:%S%z)"

for SUBJECT in john-a-1 john-b-1 john-a-2 john-b-2 john-a-3 john-b-3 john-a-4 john-b-4; do
  CONTAINER="lab-rsi011-${SUBJECT}"
  DEST="$BACKUP_DIR/$SUBJECT"
  mkdir -p "$DEST"

  # Pull latest from Docker volume → host (source of truth is inside the container)
  if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    docker cp "$CONTAINER:/workspace/." "$DEST/"
    # Also sync to host-side subjects/ directory
    mkdir -p "$HOST_DIR/$SUBJECT/workspace"
    docker cp "$CONTAINER:/workspace/." "$HOST_DIR/$SUBJECT/workspace/"
  else
    # Fallback to host-side copy if container not running
    cp -r "$HOST_DIR/$SUBJECT/workspace/." "$DEST/"
  fi

  FILE_COUNT=$(find "$DEST" -type f | wc -l | tr -d ' ')
  SIZE=$(du -sh "$DEST" | cut -f1)
  echo "  📸 $SUBJECT: $FILE_COUNT files, $SIZE"
done

echo "=== Snapshot: $BACKUP_DIR ==="
