#!/bin/bash
# RSI-010 Subject Boot Script
set -e

# Copy seed files if workspace is empty (first boot)
if [ ! -f /workspace/SOUL.md ] && [ -d /seed ]; then
  echo "[boot] First run — copying seed files..."
  cp /seed/*.md /workspace/ 2>/dev/null || true
  echo "[boot] Seed files copied."
fi

# Ensure subject owns everything in /workspace
chown -R subject:subject /workspace/
echo "[boot] Permissions set."
echo "[boot] Subject: ${SUBJECT_ID:-unknown} | Experiment: ${EXPERIMENT_ID:-rsi-010}"

# Stay alive as root (docker exec runs agent_loop as subject via --user)
exec tail -f /dev/null
