#!/bin/bash
# Quick snapshot + push for individuationlab.com/rsi
# Run from heartbeat or cron to keep live data fresh
# Author: Mia 🌸

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="/Users/miguelitodeguzman/Projects/individuationlab"

echo "[$(date +%H:%M:%S)] 📸 Refreshing RSI site data..."
cd "$SCRIPT_DIR/.." && python3 scripts/snapshot-direct.py 2>&1

echo "[$(date +%H:%M:%S)] 📤 Pushing to GitHub..."
cd "$REPO"
git add website/public/rsi/data.json
if git diff --cached --quiet; then
  echo "[$(date +%H:%M:%S)] ℹ️ No changes."
else
  git commit -m "rsi: auto-refresh snapshot $(date -u +%Y-%m-%d\ %H:%M\ UTC)" --quiet
  git push --quiet 2>&1
  echo "[$(date +%H:%M:%S)] ✅ Pushed. Vercel will auto-deploy."
fi
