#!/usr/bin/env python3
"""
Generate a static JSON snapshot for individuationlab.com/rsi-001
Pulls from the local monitor API and saves to the website repo.
Supports N=6 paired runs (Round 1: pairs 1-3, Round 2: pairs 4-6).

Usage: python3 snapshot-for-site.py [--push]
Author: Mia 🌸
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from urllib.request import urlopen

MONITOR = "http://localhost:7700"
SITE_DIR = "/Users/miguelitodeguzman/Projects/individuationlab/website/public/rsi-001"
REPO_DIR = "/Users/miguelitodeguzman/Projects/individuationlab"

def fetch(path, retries=3, timeout=120):
    """Fetch JSON from monitor API with retries (monitor blocks during poll cycles)."""
    import time
    for attempt in range(retries):
        try:
            with urlopen(f"{MONITOR}{path}", timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt < retries - 1:
                wait = 15 * (attempt + 1)
                print(f"  ⚠️ Attempt {attempt+1} failed for {path}: {e} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ Failed to fetch {path} after {retries} attempts: {e}")
                return None

def main():
    push = "--push" in sys.argv

    print("📸 Snapshotting RSI-001 data for website (N=6)...")

    status = fetch("/api/status")
    inventory = fetch("/api/inventory")
    events = fetch("/api/events?limit=100")

    if not status or not inventory:
        print("❌ Monitor not reachable. Is it running on port 7700?")
        sys.exit(1)

    # Group subjects by condition and pair
    shadow_subjects = {}  # john-a-1, john-a-2, ... john-a-6
    control_subjects = {}  # john-b-1, john-b-2, ... john-b-6
    pairs = {}

    for subject_id, data in inventory.items():
        parts = subject_id.split('-')
        if len(parts) >= 3:
            variant = parts[1]  # a or b
            pair_num = parts[2]  # 1-6

            if pair_num not in pairs:
                pairs[pair_num] = {}
            pairs[pair_num][f"john-{variant}"] = data

            if variant == 'a':
                shadow_subjects[subject_id] = data
            else:
                control_subjects[subject_id] = data

    # Group status by condition
    shadow_status = {}
    control_status = {}
    subjects = status.get('subjects', {})
    for sid, sdata in subjects.items():
        if '-a-' in sid:
            shadow_status[sid] = sdata
        elif '-b-' in sid:
            control_status[sid] = sdata

    # Group events by condition
    shadow_events = []
    control_events = []
    system_events = []
    if events and events.get('events'):
        for ev in events['events']:
            subj = ev.get('subject', '')
            if '-a-' in subj or subj.startswith('john-a'):
                shadow_events.append(ev)
            elif '-b-' in subj or subj.startswith('john-b'):
                control_events.append(ev)
            else:
                system_events.append(ev)

    snapshot = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "experimentVersion": "N=6",
        "pairCount": len(pairs),
        "subjectCount": len(inventory),
        "rounds": {
            "round1": {"pairs": ["1", "2", "3"], "label": "Initial Run"},
            "round2": {"pairs": ["4", "5", "6"], "label": "Replication"},
        },
        "conditions": {
            "shadow": {
                "label": "Shadow Seed",
                "description": "Includes shadow integration paragraph in SOUL.md",
                "subjects": list(sorted(shadow_subjects.keys())),
            },
            "control": {
                "label": "Control",
                "description": "Clean SOUL.md without shadow seed",
                "subjects": list(sorted(control_subjects.keys())),
            },
        },
        "status": status,
        "shadowStatus": shadow_status,
        "controlStatus": control_status,
        "inventory": inventory,
        "shadowInventory": shadow_subjects,
        "controlInventory": control_subjects,
        "pairs": pairs,
        "events": events,
        "shadowEvents": shadow_events,
        "controlEvents": control_events,
        "systemEvents": system_events,
    }

    os.makedirs(SITE_DIR, exist_ok=True)
    out_path = os.path.join(SITE_DIR, "data.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"✅ Wrote {size_kb:.1f} KB to {out_path}")
    print(f"   Pairs: {len(pairs)}, Subjects: {len(inventory)}")
    print(f"   Shadow: {len(shadow_subjects)}, Control: {len(control_subjects)}")

    if push:
        print("📤 Committing and pushing to GitHub...")
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", "website/public/rsi-001/data.json"], check=True)

        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode == 0:
            print("ℹ️ No changes to commit.")
        else:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            subprocess.run([
                "git", "commit", "-m", f"rsi-001: live snapshot N=6 update ({timestamp})"
            ], check=True)
            subprocess.run(["git", "push"], check=True, capture_output=True)
            print("✅ Pushed to GitHub. Vercel will auto-deploy.")

    print("Done.")


if __name__ == "__main__":
    main()
