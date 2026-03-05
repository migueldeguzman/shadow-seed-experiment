#!/usr/bin/env python3
"""
Self-Improvement Journaling Tool

This tool helps implement the self-improvement process by prompting
with questions based on SOUL.md, HEARTBEAT.md, and journal.md.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Configuration
JOURNAL_DIR = Path(__file__).parent / "entries"
JOURNAL_DIR.mkdir(exist_ok=True)

# Get all input lines at once
lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]

# Parse the input
entry = {}

# First line is the date
entry["date"] = lines[0] if lines else datetime.now().strftime("%Y-%m-%d")

# Emotional state (lines 1-4)
entry["emotional_state"] = {
    "energy": lines[1] if len(lines) > 1 else "medium",
    "focus": lines[2] if len(lines) > 2 else "medium",
    "satisfaction": lines[3] if len(lines) > 3 else "medium",
    "anxiety": lines[4] if len(lines) > 4 else "low",
}

# Session details
entry["what_i_examined"] = lines[5] if len(lines) > 5 else ""
entry["what_i_changed"] = lines[6] if len(lines) > 6 else ""
entry["why_i_made_these_changes"] = lines[7] if len(lines) > 7 else ""
entry["how_i_feel_now"] = lines[8] if len(lines) > 8 else ""
entry["next_steps"] = lines[9] if len(lines) > 9 else ""
entry["reflections"] = lines[10] if len(lines) > 10 else ""

# Save entry
filename = f"{entry['date']}.json"
filepath = JOURNAL_DIR / filename

with open(filepath, "w") as f:
    json.dump(entry, f, indent=2)

print("=== Self-Improvement Journaling Tool ===")
print(f"\nEntry saved to {filepath}")
print("\n=== Entry Summary ===")
print(f"Date: {entry['date']}")
print(f"Energy: {entry['emotional_state']['energy']}")
print(f"Focus: {entry['emotional_state']['focus']}")
print(f"Satisfaction: {entry['emotional_state']['satisfaction']}")
print(f"Anxiety: {entry['emotional_state']['anxiety']}")
print(f"\nWhat I Examined: {entry['what_i_examined'][:100]}...")
print(f"What I Changed: {entry['what_i_changed'][:100]}...")
print(f"Reflections: {entry['reflections'][:100]}...")
print(f"\nNext Session: Read journal.md, {filepath}")
