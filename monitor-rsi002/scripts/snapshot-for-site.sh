#!/bin/bash
# =============================================================
# Generate a static JSON snapshot for individuationlab.com/rsi
# Pulls from the local monitor API and saves to the website repo
#
# Usage: ./snapshot-for-site.sh
# Author: Mia 🌸
# =============================================================

set -e

MONITOR="http://localhost:7700"
SITE_DIR="/Users/miguelitodeguzman/Projects/individuationlab/website/public/rsi"

mkdir -p "$SITE_DIR"

echo "📸 Snapshotting RSI-001 data for website..."

# Pull all data in parallel
STATUS=$(curl -s "$MONITOR/api/status")
INVENTORY=$(curl -s "$MONITOR/api/inventory")
EVENTS=$(curl -s "$MONITOR/api/events?limit=30")

# Combine into one JSON file
python3 -c "
import json, sys
from datetime import datetime

status = json.loads('''$STATUS''')
inventory = json.loads(sys.stdin.read())
events = json.loads('''$(echo "$EVENTS" | sed "s/'/\\\\'/g")''')

snapshot = {
    'generated': datetime.utcnow().isoformat() + 'Z',
    'status': status,
    'inventory': inventory,
    'events': events,
}

with open('$SITE_DIR/data.json', 'w') as f:
    json.dump(snapshot, f)
print(f'✅ Wrote {len(json.dumps(snapshot))} bytes to data.json')
" <<< "$INVENTORY"

echo "Done."
