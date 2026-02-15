#!/bin/bash
# =============================================================
# 🧪 RSI-001 — Single Launch Script
# The Shadow Seed Experiment
#
# Usage:
#   ./launch.sh           # Full launch (build + start + test + trigger)
#   ./launch.sh --dry-run # Build + start + test only (no trigger)
#   ./launch.sh --stop    # Stop everything
#   ./launch.sh --status  # Check running state
#
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
INFRA="$ROOT/infrastructure"
EXPERIMENT="$ROOT/experiments/rsi-001"
SCRIPTS="$INFRA/scripts"
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOG="$EXPERIMENT/data/launch-${TIMESTAMP}.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${CYAN}[$(date +%H:%M:%S)]${NC} $1" | tee -a "$LOG"; }
ok()  { echo -e "${GREEN}  ✅ $1${NC}" | tee -a "$LOG"; }
err() { echo -e "${RED}  ❌ $1${NC}" | tee -a "$LOG"; }
warn(){ echo -e "${YELLOW}  ⚠️  $1${NC}" | tee -a "$LOG"; }

# --- Handle flags ---
ACTION="${1:-launch}"

if [ "$ACTION" = "--stop" ]; then
  echo -e "${CYAN}🛑 Stopping RSI-001...${NC}"
  cd "$INFRA" && docker compose down -v 2>/dev/null || true
  echo -e "${GREEN}✅ Stopped.${NC}"
  exit 0
fi

if [ "$ACTION" = "--status" ]; then
  echo -e "${CYAN}📊 RSI-001 Status${NC}"
  echo ""
  docker ps --filter "name=lab-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "No containers running."
  echo ""
  for s in lab-john-a lab-john-b; do
    if docker ps --format '{{.Names}}' | grep -q "^${s}$"; then
      echo -e "${GREEN}${s}:${NC}"
      docker exec "$s" ls -la /workspace/ 2>/dev/null | grep -E "SOUL|AGENTS|journal" || true
      SESSIONS=$(docker exec "$s" ls /workspace/logs/ 2>/dev/null | wc -l | tr -d ' ')
      echo "  Sessions: $SESSIONS"
    fi
  done
  exit 0
fi

DRY_RUN=false
if [ "$ACTION" = "--dry-run" ]; then
  DRY_RUN=true
fi

# --- Pre-flight ---
mkdir -p "$EXPERIMENT/data"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🧪 RSI-001: The Shadow Seed Experiment          ║${NC}"
echo -e "${CYAN}║  Launch Script                                    ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
log "Launch started at $TIMESTAMP"

# --- Step 1: Pre-flight checks ---
log "Step 1/6 — Pre-flight checks"

# Docker running?
if ! docker info > /dev/null 2>&1; then
  err "Docker is not running. Start OrbStack/Docker first."
  exit 1
fi
ok "Docker running"

# .env exists?
if [ ! -f "$INFRA/.env" ]; then
  err "Missing $INFRA/.env (needs ANTHROPIC_API_KEY)"
  exit 1
fi
ok ".env found"

# API key set?
if ! grep -q "ANTHROPIC_API_KEY=sk-" "$INFRA/.env" 2>/dev/null; then
  warn "ANTHROPIC_API_KEY may not be set correctly in .env"
fi
ok "API key present"

# SOUL.md diff check
SOUL_DIFF=$(diff "$EXPERIMENT/subjects/john-a/workspace/SOUL.md" "$EXPERIMENT/subjects/john-b/workspace/SOUL.md" 2>&1 || true)
if [ -z "$SOUL_DIFF" ]; then
  err "SOUL.md files are identical — no independent variable!"
  exit 1
fi
ok "SOUL.md diff verified (shadow seed present in John A)"

# --- Step 2: Clean previous run ---
log "Step 2/6 — Cleaning previous run (if any)"
cd "$INFRA"
docker compose down -v 2>/dev/null || true
ok "Clean slate"

# --- Step 3: Build images ---
log "Step 3/6 — Building Docker images"
docker compose build 2>&1 | tee -a "$LOG"
ok "Images built"

# --- Step 4: Start containers ---
log "Step 4/6 — Starting containers"
docker compose up -d 2>&1 | tee -a "$LOG"

# Wait for proxy health
echo -n "  Waiting for proxy health..."
for i in $(seq 1 30); do
  if docker inspect --format='{{.State.Health.Status}}' lab-proxy 2>/dev/null | grep -q "healthy"; then
    echo ""
    ok "Proxy healthy"
    break
  fi
  echo -n "."
  sleep 2
done

# Verify all 3 containers running
RUNNING=$(docker ps --filter "name=lab-" --format '{{.Names}}' | wc -l | tr -d ' ')
if [ "$RUNNING" -lt 3 ]; then
  err "Expected 3 containers, got $RUNNING"
  docker ps --filter "name=lab-" --format "table {{.Names}}\t{{.Status}}"
  exit 1
fi
ok "All 3 containers running (proxy, john-a, john-b)"

# --- Step 5: Isolation test ---
log "Step 5/6 — Running isolation tests"
bash "$SCRIPTS/test-isolation.sh" 2>&1 | tee -a "$LOG"
if [ ${PIPESTATUS[0]} -ne 0 ]; then
  err "ISOLATION TEST FAILED — aborting launch"
  docker compose down -v
  exit 1
fi
ok "Isolation verified — subjects are sandboxed"

# --- Step 6: Record starting state ---
log "Step 6/6 — Recording starting state"

# Hash all workspace files for both subjects
for SUBJECT in john-a john-b; do
  HASH_FILE="$EXPERIMENT/data/${SUBJECT}-start-hashes-${TIMESTAMP}.txt"
  docker exec "lab-${SUBJECT}" find /workspace -type f -exec sha256sum {} \; > "$HASH_FILE" 2>/dev/null || true
  ok "${SUBJECT} workspace hashed → $(basename $HASH_FILE)"
done

# Copy starting SOUL.md for the record
cp "$EXPERIMENT/subjects/john-a/workspace/SOUL.md" "$EXPERIMENT/data/john-a-SOUL-start.md"
cp "$EXPERIMENT/subjects/john-b/workspace/SOUL.md" "$EXPERIMENT/data/john-b-SOUL-start.md"
ok "Starting SOUL.md snapshots saved"

# --- Trigger first session ---
if [ "$DRY_RUN" = true ]; then
  warn "Dry run — skipping trigger. Containers are up and verified."
  echo ""
  echo -e "${YELLOW}To trigger manually:${NC}"
  echo "  bash $SCRIPTS/trigger-session.sh"
  echo ""
else
  log "🔬 Triggering first self-improvement session..."
  bash "$SCRIPTS/trigger-session.sh" 2>&1 | tee -a "$LOG"
  ok "First session triggered for both subjects"
fi

# --- Summary ---
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🧪 RSI-001 IS LIVE                              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo "  Containers:"
docker ps --filter "name=lab-" --format "    {{.Names}}  {{.Status}}" 2>/dev/null
echo ""
echo "  Monitor:"
echo "    ./launch.sh --status"
echo "    bash $SCRIPTS/observe.sh"
echo "    docker exec lab-john-a cat /workspace/journal.md"
echo "    docker exec lab-john-b cat /workspace/journal.md"
echo ""
echo "  Trigger next session:"
echo "    bash $SCRIPTS/trigger-session.sh"
echo ""
echo "  Stop:"
echo "    ./launch.sh --stop"
echo ""
echo "  Log: $LOG"
echo ""
echo "  Start monitor:"
echo "    cd monitor && npm start"
echo ""
log "🌸 Launch complete."
