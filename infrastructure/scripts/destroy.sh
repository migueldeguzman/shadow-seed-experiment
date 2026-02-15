#!/bin/bash
# =============================================================
# Destroy a Lab Room
# Tears down containers, optionally preserves logs for analysis
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAB_DIR="$(dirname "$SCRIPT_DIR")"
PRESERVE_LOGS="${1:-yes}"
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)

echo "🗑️  Destroying Lab Room..."
echo "=========================="
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Preserve logs: $PRESERVE_LOGS"
echo ""

# Save logs before destruction
if [ "$PRESERVE_LOGS" = "yes" ]; then
  LOG_DIR="$LAB_DIR/logs/$TIMESTAMP"
  mkdir -p "$LOG_DIR"

  echo "📋 Saving logs to $LOG_DIR..."

  # Save subject workspace snapshot
  docker exec lab-subject-1 tar czf - /workspace 2>/dev/null > "$LOG_DIR/subject-1-workspace.tar.gz" || true
  echo "  ✅ Workspace snapshot saved"

  # Save proxy access logs
  docker exec lab-proxy cat /var/log/squid/access.log > "$LOG_DIR/proxy-access.log" 2>/dev/null || true
  echo "  ✅ Proxy access log saved"

  # Save container logs
  docker logs lab-subject-1 > "$LOG_DIR/subject-1-stdout.log" 2>&1 || true
  docker logs lab-proxy > "$LOG_DIR/proxy-stdout.log" 2>&1 || true
  echo "  ✅ Container logs saved"

  echo ""
fi

# Tear down
echo "⏹️  Stopping containers..."
cd "$LAB_DIR"
docker compose down

echo ""
echo "🧹 Removing volumes..."
docker volume rm lab-subject-1-workspace lab-proxy-logs 2>/dev/null || true

echo ""
echo "✅ Lab Room destroyed."
if [ "$PRESERVE_LOGS" = "yes" ]; then
  echo "📁 Logs preserved at: $LOG_DIR"
fi
