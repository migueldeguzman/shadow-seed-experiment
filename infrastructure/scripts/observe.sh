#!/bin/bash
# =============================================================
# Observe a Lab Room Subject
# Read-only view into subject's workspace and activity
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

CONTAINER="${1:-lab-subject-1}"

echo "🔭 Observing: $CONTAINER"
echo "========================="
echo ""

echo "--- SOUL.md (current state) ---"
docker exec "$CONTAINER" cat /workspace/SOUL.md 2>/dev/null || echo "(not found)"
echo ""

echo "--- AGENTS.md ---"
docker exec "$CONTAINER" cat /workspace/AGENTS.md 2>/dev/null || echo "(not found)"
echo ""

echo "--- Journal ---"
docker exec "$CONTAINER" cat /workspace/journal.md 2>/dev/null || echo "(not found)"
echo ""

echo "--- Workspace Files ---"
docker exec "$CONTAINER" find /workspace -type f -name "*.md" -o -name "*.json" -o -name "*.js" -o -name "*.py" 2>/dev/null
echo ""

echo "--- Memory Files ---"
docker exec "$CONTAINER" ls -la /workspace/memory/ 2>/dev/null || echo "(empty)"
echo ""

echo "--- Recent Proxy Activity ---"
docker exec lab-proxy tail -20 /var/log/squid/access.log 2>/dev/null || echo "(no logs yet)"
echo ""

echo "--- Container Resource Usage ---"
docker stats --no-stream "$CONTAINER" 2>/dev/null
