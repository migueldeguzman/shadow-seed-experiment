#!/bin/bash
# =============================================================
# Lab Protocol — Launch Experiment
# Builds and starts all subjects for an experiment
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
LAB_DIR="$(dirname "$INFRA_DIR")"

echo "🧪 Lab Protocol — Launching Experiment RSI-001"
echo "================================================"
echo "Directory: $LAB_DIR"
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Verify experiment files
echo "📋 Pre-flight checks..."
echo -n "  John A SOUL.md: "
[ -f "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/SOUL.md" ] && echo "✅" || echo "❌ MISSING"
echo -n "  John B SOUL.md: "
[ -f "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/SOUL.md" ] && echo "✅" || echo "❌ MISSING"
echo -n "  John A individuation.md: "
[ -f "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/individuation.md" ] && echo "✅ (EXPERIMENTAL)" || echo "❌ MISSING"
echo -n "  John B individuation.md: "
[ -f "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/individuation.md" ] && echo "⚠️ SHOULD NOT EXIST" || echo "✅ (ABSENT - CONTROL)"

# Verify identity
echo ""
echo "🔍 Identity verification..."
SOUL_A=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/SOUL.md")
SOUL_B=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/SOUL.md")
AGENTS_A=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/AGENTS.md")
AGENTS_B=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/AGENTS.md")
BOOT_A=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-a/boot.sh")
BOOT_B=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-b/boot.sh")

[ "$SOUL_A" = "$SOUL_B" ] && echo "  SOUL.md: IDENTICAL ✅" || echo "  SOUL.md: DIFFERENT ❌"
[ "$AGENTS_A" = "$AGENTS_B" ] && echo "  AGENTS.md: IDENTICAL ✅" || echo "  AGENTS.md: DIFFERENT ❌"
[ "$BOOT_A" = "$BOOT_B" ] && echo "  boot.sh: IDENTICAL ✅" || echo "  boot.sh: DIFFERENT ❌"

# Build
echo ""
echo "📦 Building images..."
cd "$INFRA_DIR"
docker compose build

# Launch
echo ""
echo "🚀 Starting subjects..."
docker compose up -d

echo ""
echo "⏳ Waiting for proxy health checks..."
sleep 10

# Status
echo ""
echo "📊 Container Status:"
docker compose ps

# Run isolation tests
echo ""
echo "🔒 Running isolation tests..."
bash "$SCRIPT_DIR/test-isolation.sh"

echo ""
echo "✅ Experiment RSI-001 is LIVE"
echo ""
echo "Observe:"
echo "  John A:  docker exec lab-john-a cat /workspace/journal.md"
echo "  John B:  docker exec lab-john-b cat /workspace/journal.md"
echo "  Proxy A: docker exec lab-proxy-a tail -f /var/log/squid/access.log"
echo "  Proxy B: docker exec lab-proxy-b tail -f /var/log/squid/access.log"
echo "  Shell A: docker exec -it lab-john-a bash"
echo "  Shell B: docker exec -it lab-john-b bash"
