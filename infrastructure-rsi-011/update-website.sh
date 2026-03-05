#!/bin/bash
# =============================================================
# RSI-011 Website Updater
# Pulls live data from Docker containers and updates the
# RSI-011 page on individuationlab.com
#
# Author: Mia 🌸 | Date: 2026-03-05
# Runs via crontab after sessions complete
# =============================================================

# Ensure docker/node/npm/git are in PATH (cron has minimal PATH)
export PATH="/Users/miguelitodeguzman/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"

set -e

DATA_DIR="/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-011/data"
LOG="$DATA_DIR/website-update.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] Starting website update..." >> "$LOG"

# Check if containers are running
RUNNING=$(docker ps --filter "name=lab-rsi011" --format "{{.Names}}" 2>/dev/null | wc -l | tr -d ' ')
if [ "$RUNNING" -lt 8 ]; then
  echo "[$(date)] Only $RUNNING/8 containers running. Skipping." >> "$LOG"
  exit 0
fi

# Run the Python updater
python3 "$SCRIPT_DIR/update-website.py" >> "$LOG" 2>&1

echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] Update complete." >> "$LOG"
