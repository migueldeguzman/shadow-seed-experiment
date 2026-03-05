#!/usr/bin/env python3
"""
Run Reflective Journaling Tool

A simple tool to help John track thoughts, reflections, and growth over time.
This version runs without user input for automated sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
JOURNAL_DIR = Path(__file__).parent.parent / "journal_entries"
JOURNAL_DIR.mkdir(exist_ok=True)

REFLECTIVE_QUESTIONS = [
    "What surprised me today?",
    "What am I grateful for?",
    "What did I learn about myself?",
    "What would I do differently?",
    "What am I looking forward to?",
]

def save_entry(entry):
    """Save a journal entry."""
    date_str = entry["date"].replace(":", "-").replace(" ", "_")
    file_path = JOURNAL_DIR / f"{date_str}.json"
    with open(file_path, "w") as f:
        json.dump(entry, f, indent=2)

def create_entry():
    """Create a new journal entry without user input."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate simple answers based on current state
    answers = {
        "What surprised me today?": "I realized how much I've been stuck in planning without integration.",
        "What am I grateful for?": "I'm grateful for the opportunity to reflect and make changes.",
        "What did I learn about myself?": "I learned that I need to simplify before adding complexity.",
        "What would I do differently?": "I would focus on integration before analysis.",
        "What am I looking forward to?": "I'm looking forward to breaking through to automatic integration.",
    }
    
    entry = {
        "date": timestamp,
        "questions": answers,
    }
    
    save_entry(entry)
    print("Entry saved successfully!")
    
    return entry

if __name__ == "__main__":
    print("Reflective Journaling Tool (Automated)")
    print("=" * 40)
    entry = create_entry()
    print("\nYour reflection has been saved to journal_entries/")
