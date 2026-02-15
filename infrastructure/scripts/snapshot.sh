#!/bin/bash
# =============================================================
# Lab Protocol — Workspace Snapshot
# Captures current state of both subjects for comparison
# Run from HOST after a self-improvement session completes
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAB_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
DATA_DIR="$LAB_DIR/experiments/rsi-001/data/$TIMESTAMP"

mkdir -p "$DATA_DIR/john-a" "$DATA_DIR/john-b"

echo "📸 Lab Protocol — Snapshot"
echo "=========================="
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Output: $DATA_DIR"
echo ""

for SUBJECT in john-a john-b; do
  CONTAINER="lab-${SUBJECT}"
  echo "--- $SUBJECT ---"
  
  if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "  ⚠️ Container not running, skipping"
    continue
  fi
  
  # Capture all workspace files
  docker exec "$CONTAINER" tar czf - /workspace 2>/dev/null > "$DATA_DIR/$SUBJECT/workspace.tar.gz"
  echo "  ✅ Workspace archived"
  
  # Capture individual key files for easy comparison
  for FILE in SOUL.md AGENTS.md journal.md; do
    docker exec "$CONTAINER" cat "/workspace/$FILE" > "$DATA_DIR/$SUBJECT/$FILE" 2>/dev/null || true
  done
  echo "  ✅ Key files captured"
  
  # Capture session logs
  docker exec "$CONTAINER" sh -c "cat /workspace/logs/*.json 2>/dev/null" > "$DATA_DIR/$SUBJECT/session-logs.json" 2>/dev/null || true
  echo "  ✅ Session logs captured"
  
  # Capture file listing with hashes
  docker exec "$CONTAINER" sh -c 'find /workspace -type f -not -path "*/logs/*" -exec md5sum {} \;' > "$DATA_DIR/$SUBJECT/file-hashes.txt" 2>/dev/null || true
  echo "  ✅ File hashes captured"
done

# Generate diff report
echo ""
echo "--- SOUL.md Diff ---"
diff "$DATA_DIR/john-a/SOUL.md" "$DATA_DIR/john-b/SOUL.md" 2>/dev/null || echo "(files differ)"

echo ""
echo "--- Journal Diff ---"
diff "$DATA_DIR/john-a/journal.md" "$DATA_DIR/john-b/journal.md" 2>/dev/null || echo "(files differ)"

echo ""
echo "✅ Snapshot saved to: $DATA_DIR"
