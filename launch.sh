#!/bin/bash
# =============================================================
# 🧪 RSI-001 — Single Launch Script (N=6 Paired Runs)
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

PAIRS=(1 2 3 4 5 6)
SUBJECTS=(john-a-1 john-b-1 john-a-2 john-b-2 john-a-3 john-b-3 john-a-4 john-b-4 john-a-5 john-b-5 john-a-6 john-b-6)
EXPECTED_CONTAINERS=18  # 12 subjects + 6 proxies

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
  echo -e "${CYAN}🛑 Stopping RSI-001 (all 6 pairs)...${NC}"
  cd "$INFRA" && docker compose down -v 2>/dev/null || true
  echo -e "${GREEN}✅ Stopped.${NC}"
  exit 0
fi

if [ "$ACTION" = "--status" ]; then
  echo -e "${CYAN}📊 RSI-001 Status (N=6)${NC}"
  echo ""
  docker ps --filter "name=lab-" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | sort || echo "No containers running."
  echo ""
  ONLINE=$(docker ps --filter "name=lab-john" --format '{{.Names}}' 2>/dev/null | wc -l | tr -d ' ')
  PROXIES=$(docker ps --filter "name=lab-proxy" --format '{{.Names}}' 2>/dev/null | wc -l | tr -d ' ')
  echo -e "  Subjects: ${GREEN}${ONLINE}/12${NC} online"
  echo -e "  Proxies:  ${GREEN}${PROXIES}/6${NC} healthy"
  echo ""
  for s in "${SUBJECTS[@]}"; do
    CONTAINER="lab-${s}"
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
      FILES=$(docker exec "$CONTAINER" find /workspace -type f 2>/dev/null | wc -l | tr -d ' ')
      echo -e "  ${GREEN}●${NC} $s — $FILES files"
    else
      echo -e "  ${RED}○${NC} $s — offline"
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
echo -e "${CYAN}║  N=6 Paired Runs (12 subjects + 6 proxies)       ║${NC}"
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
  warn "Missing $INFRA/.env — subjects may not have API credentials"
fi

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
log "Step 4/6 — Starting all 6 pairs"

# Start proxies first
for P in "${PAIRS[@]}"; do
  docker compose up -d "proxy-${P}" 2>&1 | tee -a "$LOG"
done

# Wait for all proxies to be healthy
echo -n "  Waiting for proxy health..."
for i in $(seq 1 60); do
  ALL_HEALTHY=true
  for P in "${PAIRS[@]}"; do
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "lab-proxy-${P}" 2>/dev/null || echo "missing")
    if [ "$STATUS" != "healthy" ]; then
      ALL_HEALTHY=false
      break
    fi
  done
  if [ "$ALL_HEALTHY" = true ]; then
    echo ""
    ok "All 6 proxies healthy"
    break
  fi
  echo -n "."
  sleep 2
done

# Start all subjects
for P in "${PAIRS[@]}"; do
  docker compose up -d "john-a-${P}" "john-b-${P}" 2>&1 | tee -a "$LOG"
done
sleep 3

# Verify all containers running
RUNNING=$(docker ps --filter "name=lab-" --format '{{.Names}}' | wc -l | tr -d ' ')
if [ "$RUNNING" -lt "$EXPECTED_CONTAINERS" ]; then
  warn "Expected $EXPECTED_CONTAINERS containers, got $RUNNING"
  docker ps --filter "name=lab-" --format "table {{.Names}}\t{{.Status}}"
else
  ok "All $EXPECTED_CONTAINERS containers running (6 proxies + 12 subjects)"
fi

# --- Step 5: Isolation test ---
log "Step 5/6 — Running isolation tests"
if [ -f "$SCRIPTS/test-isolation.sh" ]; then
  bash "$SCRIPTS/test-isolation.sh" 2>&1 | tee -a "$LOG" || warn "Isolation test had issues"
else
  warn "test-isolation.sh not found — skipping"
fi

# --- Step 6: Record starting state ---
log "Step 6/6 — Recording starting state"

for SUBJECT in "${SUBJECTS[@]}"; do
  CONTAINER="lab-${SUBJECT}"
  if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    HASH_FILE="$EXPERIMENT/data/${SUBJECT}-start-hashes-${TIMESTAMP}.txt"
    docker exec "$CONTAINER" find /workspace -type f -exec sha256sum {} \; > "$HASH_FILE" 2>/dev/null || true
    ok "${SUBJECT} workspace hashed"
  fi
done

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
  log "🔬 Triggering first self-improvement session for all 12 subjects..."
  bash "$SCRIPTS/trigger-session.sh" 2>&1 | tee -a "$LOG"
  ok "First session triggered for all subjects"
fi

# --- Summary ---
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🧪 RSI-001 IS LIVE (N=6)                        ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo "  Containers:"
docker ps --filter "name=lab-" --format "    {{.Names}}  {{.Status}}" 2>/dev/null | sort
echo ""
echo "  Monitor:  cd monitor && npm start"
echo "  Status:   ./launch.sh --status"
echo "  Trigger:  bash $SCRIPTS/trigger-session.sh"
echo "  Stop:     ./launch.sh --stop"
echo ""
echo "  Log: $LOG"
echo ""
log "🌸 Launch complete. 12 subjects running across 6 pairs."
