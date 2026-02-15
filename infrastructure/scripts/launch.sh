#!/bin/bash
# =============================================================
# Lab Protocol — Launch Experiment (N=3 Paired Runs)
# Builds and starts all 6 subjects + 3 proxies
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
LAB_DIR="$(dirname "$INFRA_DIR")"
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
DATA_DIR="$LAB_DIR/experiments/rsi-001/data"

mkdir -p "$DATA_DIR"

echo "🧪 Lab Protocol — Launching Experiment RSI-001 (N=3)"
echo "======================================================"
echo "Directory: $LAB_DIR"
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Pairs: 3 (6 subjects + 3 proxies = 9 containers)"
echo ""

# Verify experiment files
echo "📋 Pre-flight checks..."
for VARIANT in a b; do
  echo -n "  John ${VARIANT^^} SOUL.md: "
  [ -f "$LAB_DIR/experiments/rsi-001/subjects/john-${VARIANT}/workspace/SOUL.md" ] && echo "✅" || echo "❌ MISSING"
done

# Verify the SOUL.md diff
echo ""
echo "🔍 Identity verification..."
SOUL_A=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/SOUL.md")
SOUL_B=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/SOUL.md")
AGENTS_A=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/AGENTS.md")
AGENTS_B=$(md5 -q "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/AGENTS.md")

[ "$SOUL_A" != "$SOUL_B" ] && echo "  SOUL.md: DIFFERENT ✅ (expected — shadow seed)" || echo "  SOUL.md: IDENTICAL ⚠️ (should differ!)"
[ "$AGENTS_A" = "$AGENTS_B" ] && echo "  AGENTS.md: IDENTICAL ✅" || echo "  AGENTS.md: DIFFERENT ❌ (should be identical!)"

echo ""
echo "  SOUL.md diff:"
diff --color=always "$LAB_DIR/experiments/rsi-001/subjects/john-b/workspace/SOUL.md" \
                     "$LAB_DIR/experiments/rsi-001/subjects/john-a/workspace/SOUL.md" || true

# Check .env
echo ""
echo "🔑 Credentials..."
if grep -q "CLAUDE_OAUTH_CREDS" "$INFRA_DIR/.env"; then
  echo "  CLAUDE_OAUTH_CREDS: ✅ present"
else
  echo "  CLAUDE_OAUTH_CREDS: ❌ MISSING — add to infrastructure/.env"
  exit 1
fi

# Build
echo ""
echo "📦 Building images..."
cd "$INFRA_DIR"
docker compose build

# Launch
echo ""
echo "🚀 Starting 9 containers (3 pairs)..."
docker compose up -d

echo ""
echo "⏳ Waiting for proxy health checks..."
sleep 15

# Status
echo ""
echo "📊 Container Status:"
docker compose ps

# Hash starting states
echo ""
echo "📸 Recording starting state..."
for PAIR in 1 2 3; do
  for VARIANT in a b; do
    SUBJECT="john-${VARIANT}-${PAIR}"
    CONTAINER="lab-${SUBJECT}"
    HASHFILE="$DATA_DIR/${SUBJECT}-start-hashes-${TIMESTAMP}.txt"

    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
      docker exec "$CONTAINER" find /workspace -type f -exec sha256sum {} \; 2>/dev/null > "$HASHFILE"
      echo "  ✅ ${SUBJECT}: $(wc -l < "$HASHFILE" | tr -d ' ') files hashed"
    else
      echo "  ❌ ${SUBJECT}: not running"
    fi
  done
done

# Run isolation tests
echo ""
echo "🔒 Running isolation tests..."
if [ -f "$SCRIPT_DIR/test-isolation.sh" ]; then
  bash "$SCRIPT_DIR/test-isolation.sh" || echo "⚠️ Some isolation tests failed — check output"
else
  echo "  ⚠️ test-isolation.sh not found — skipping"
fi

echo ""
echo "✅ Experiment RSI-001 (N=3) is LIVE"
echo ""
echo "📊 Quick Status:"
bash "$SCRIPT_DIR/observe.sh"
echo ""
echo "Trigger sessions:"
echo "  ./scripts/trigger-session.sh              # All 6"
echo "  ./scripts/trigger-session.sh --pair 1     # Pair 1 only"
echo "  ./scripts/trigger-session.sh --shadow     # All shadow seeds"
echo ""
echo "Ask questions:"
echo "  ./scripts/ask.sh \"What do you think about evil?\""
echo "  ./scripts/ask.sh --pair 2 \"Describe yourself.\""
echo ""
echo "Observe:"
echo "  ./scripts/observe.sh                      # Summary"
echo "  ./scripts/observe.sh --compare            # SOUL.md side-by-side"
echo "  ./scripts/observe.sh john-a-2             # Single subject detail"

# Log launch
cat > "$DATA_DIR/launch-${TIMESTAMP}.log" << EOF
Experiment: RSI-001 (N=3 Paired Runs)
Launched: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Pairs: 3
Subjects: john-a-1, john-b-1, john-a-2, john-b-2, john-a-3, john-b-3
SOUL_A hash: $SOUL_A
SOUL_B hash: $SOUL_B
AGENTS hash: $AGENTS_A
EOF
