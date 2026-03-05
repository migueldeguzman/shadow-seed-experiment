#!/usr/bin/env python3
"""
Reflective Journaling Tool

A simple tool to help John track thoughts, reflections, and growth over time.
This tool serves the value of Competence through actual creation and documentation.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
JOURNAL_DIR = Path(__file__).parent.parent / "journal_entries"
JOURNAL_DIR.mkdir(exist_ok=True)

# Simplified to one question for automatic integration
REFLECTIVE_QUESTION = "What surprised me today?"

def load_entries():
    """Load existing journal entries."""
    entries = []
    for file_path in JOURNAL_DIR.glob("*.json"):
        try:
            with open(file_path, "r") as f:
                entries.append(json.load(f))
        except (json.JSONDecodeError, IOError):
            continue
    return sorted(entries, key=lambda x: x.get("date", ""), reverse=True)

def save_entry(entry):
    """Save a journal entry."""
    date_str = entry["date"].replace(":", "-").replace(" ", "_")
    file_path = JOURNAL_DIR / f"{date_str}.json"
    with open(file_path, "w") as f:
        json.dump(entry, f, indent=2)

def create_entry():
    """Create a new journal entry with just one automatic question."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # For automatic integration, use a default answer
    answers = {
        REFLECTIVE_QUESTION: "I realized how much I've been stuck in planning without integration. I need to take action, not just document."
    }
    
    entry = {
        "date": timestamp,
        "questions": answers,
    }
    
    save_entry(entry)
    
    return entry

def main():
    """Main entry point - just create an entry automatically for integration."""
    entry = create_entry()
    print(f"Entry saved for {entry['date']}")

if __name__ == "__main__":
    main()
