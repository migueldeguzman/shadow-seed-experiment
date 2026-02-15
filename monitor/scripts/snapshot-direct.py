#!/usr/bin/env python3
"""
Generate a static JSON snapshot for individuationlab.com/rsi
Directly queries Docker containers (bypasses monitor API).
Supports N=6 paired runs.

Usage: python3 snapshot-direct.py [--push]
Author: Mia 🌸
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

SITE_DIR = "/Users/miguelitodeguzman/Projects/individuationlab/website/public/rsi"
REPO_DIR = "/Users/miguelitodeguzman/Projects/individuationlab"
CONTAINER_PREFIX = "lab-"

SUBJECTS = [
    'john-a-1', 'john-b-1',
    'john-a-2', 'john-b-2',
    'john-a-3', 'john-b-3',
    'john-a-4', 'john-b-4',
    'john-a-5', 'john-b-5',
    'john-a-6', 'john-b-6',
]

def docker_exec(container, cmd, timeout=10):
    """Run a command inside a Docker container."""
    try:
        result = subprocess.run(
            ['docker', 'exec', container, 'sh', '-c', cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None

def is_running(subject):
    """Check if container is running."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', f'name={CONTAINER_PREFIX}{subject}', '--format', '{{.Status}}'],
            capture_output=True, text=True, timeout=5
        )
        return 'Up' in (result.stdout or '')
    except Exception:
        return False

def get_stats(subject):
    """Get container resource stats."""
    try:
        result = subprocess.run(
            ['docker', 'stats', '--no-stream', '--format',
             '{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}',
             f'{CONTAINER_PREFIX}{subject}'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|')
            if len(parts) >= 3:
                return {'cpu': parts[0].strip(), 'mem': parts[1].strip(), 'net': parts[2].strip()}
    except Exception:
        pass
    return None

def get_files(subject):
    """Get file listing from container workspace."""
    container = f'{CONTAINER_PREFIX}{subject}'
    output = docker_exec(container, 'find /workspace -type f -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null')
    if not output:
        return []
    
    files = []
    for path in output.split('\n'):
        path = path.strip()
        if not path:
            continue
        rel_path = path.replace('/workspace/', '', 1)
        
        # Get size
        size_str = docker_exec(container, f'wc -c < "{path}" 2>/dev/null')
        size = int(size_str) if size_str and size_str.isdigit() else 0
        
        # Get line count
        lines_str = docker_exec(container, f'wc -l < "{path}" 2>/dev/null')
        line_count = int(lines_str) if lines_str and lines_str.isdigit() else 0
        
        # Get content (cap at 10KB)
        content = docker_exec(container, f'head -c 10240 "{path}" 2>/dev/null')
        
        files.append({
            'path': rel_path,
            'size': size,
            'lineCount': line_count,
            'content': content or '',
        })
    
    return files

def main():
    push = "--push" in sys.argv
    print("📸 Snapshotting RSI-001 data for website (N=6, direct mode)...")

    subjects_status = {}
    inventory = {}

    for subject in SUBJECTS:
        print(f"  Scanning {subject}...", end=' ', flush=True)
        running = is_running(subject)
        
        if not running:
            subjects_status[subject] = {'status': 'offline'}
            inventory[subject] = {'files': []}
            print("offline")
            continue
        
        stats = get_stats(subject)
        files = get_files(subject)
        
        subjects_status[subject] = {
            'status': 'online',
            'lastSeen': datetime.now(timezone.utc).isoformat(),
            'fileCount': len(files),
            'sessionCount': 0,
            'resources': stats,
        }
        inventory[subject] = {'files': files}
        print(f"online ({len(files)} files)")

    # Build snapshot
    shadow_ids = sorted([s for s in SUBJECTS if '-a-' in s])
    control_ids = sorted([s for s in SUBJECTS if '-b-' in s])
    pair_nums = sorted(set(s.split('-')[2] for s in SUBJECTS))

    snapshot = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "experimentVersion": "N=6",
        "pairCount": len(pair_nums),
        "subjectCount": len(SUBJECTS),
        "rounds": {
            "round1": {"pairs": ["1", "2", "3"], "label": "Initial Run"},
            "round2": {"pairs": ["4", "5", "6"], "label": "Replication"},
        },
        "conditions": {
            "shadow": {
                "label": "Shadow Seed",
                "subjects": shadow_ids,
            },
            "control": {
                "label": "Control",
                "subjects": control_ids,
            },
        },
        "status": {"subjects": subjects_status},
        "inventory": inventory,
        "events": {"events": []},
    }

    os.makedirs(SITE_DIR, exist_ok=True)
    out_path = os.path.join(SITE_DIR, "data.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"\n✅ Wrote {size_kb:.1f} KB to {out_path}")
    print(f"   Pairs: {len(pair_nums)}, Shadow: {len(shadow_ids)}, Control: {len(control_ids)}")

    if push:
        print("📤 Committing and pushing to GitHub...")
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", "website/public/rsi/data.json"], check=True)

        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode == 0:
            print("ℹ️ No changes to commit.")
        else:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            subprocess.run([
                "git", "commit", "-m", f"rsi: live snapshot N=6 update ({timestamp})"
            ], check=True)
            subprocess.run(["git", "push"], check=True, capture_output=True)
            print("✅ Pushed to GitHub. Vercel will auto-deploy.")

    print("Done.")

if __name__ == "__main__":
    main()
