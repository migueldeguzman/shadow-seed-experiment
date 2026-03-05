#!/usr/bin/env python3
"""
Daily Progress Tracker - 2026-03-04
Focus: Actually implementing something functional today
"""

import json
import os
from datetime import datetime

# Use the actual system date
SYSTEM_DATE = datetime.now().strftime("%Y-%m-%d")
SESSION_DATE = "2026-03-04"  # This is the date we're actually working on today

DATA_FILE = "daily_tracker_data.json"

def load_data():
    """Load tracker data from file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"entries": {}, "last_entry_date": None}

def save_data(data):
    """Save tracker data to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def ensure_structure(entry):
    """Ensure the entry has the correct structure."""
    # Ensure reflection has the correct keys
    if "reflection" not in entry:
        entry["reflection"] = {}
    if "didnt_work" not in entry["reflection"]:
        entry["reflection"]["didnt_work"] = entry["reflection"].get("didn't_work", "Not yet tested")
    
    # Ensure concrete_project exists
    if "concrete_project" not in entry:
        entry["concrete_project"] = {
            "name": "Implement something functional today",
            "description": "Create something tangible that I can actually use",
            "status": "in_progress",
            "what_worked": "Not yet determined",
            "what_didnt_work": "Not yet determined",
            "improve_next_time": "Will learn from actual implementation"
        }
    
    return entry

def get_or_create_entry(data, date):
    """Get existing entry or create a new one for the date."""
    if date not in data["entries"]:
        data["entries"][date] = {
            "date": date,
            "project": "Breaking the Pattern of Implementation Without Implementation",
            "tasks_completed": [],
            "tasks_planned": [
                "Actually implement something functional today",
                "Test the implementation by using it",
                "Document what worked and what didn't"
            ],
            "implementation_checklist": {
                "functional": True,
                "usable": True,
                "real_work": True,
                "gap_closed": False
            },
            "reflection": {
                "implemented": "Not yet implemented",
                "worked": "Not yet tested",
                "didnt_work": "Not yet tested",
                "improve_next_time": "Will learn from actual implementation"
            },
            "accomplishments": [],
            "insights": [],
            "concrete_project": {
                "name": "Implement something functional today",
                "description": "Create something tangible that I can actually use",
                "status": "in_progress",
                "what_worked": "Not yet determined",
                "what_didnt_work": "Not yet determined",
                "improve_next_time": "Will learn from actual implementation"
            }
        }
    else:
        # Ensure the entry has the correct structure
        data["entries"][date] = ensure_structure(data["entries"][date])
    return data["entries"][date]

def print_tracker(entry):
    """Print the tracker information."""
    print(f"Daily Progress Tracker - {entry['date']}")
    print(f"Project: {entry['project']}")
    print()
    
    print("Tasks Completed:")
    if entry["tasks_completed"]:
        for task in entry["tasks_completed"]:
            print(f"  - {task}")
    else:
        print("  (No tasks completed yet)")
    print()
    
    print("Tasks Planned:")
    for task in entry["tasks_planned"]:
        print(f"  - {task}")
    print()
    
    print("Implementation Checklist:")
    for item, status in entry["implementation_checklist"].items():
        print(f"  - {item}: {'✓' if status else '✗'}")
    print()
    
    print("Reflection:")
    print(f"  - implemented: {entry['reflection']['implemented']}")
    print(f"  - worked: {entry['reflection']['worked']}")
    print(f"  - didnt_work: {entry['reflection']['didnt_work']}")
    print(f"  - improve_next_time: {entry['reflection']['improve_next_time']}")
    print()
    
    print("Accomplishments:")
    if entry["accomplishments"]:
        for item in entry["accomplishments"]:
            print(f"  - {item}")
    else:
        print("  (No accomplishments yet)")
    print()
    
    print("Insights:")
    if entry["insights"]:
        for item in entry["insights"]:
            print(f"  - {item}")
    else:
        print("  (No insights yet)")
    print()
    
    print("Concrete Project:")
    project = entry["concrete_project"]
    print(f"  - Name: {project['name']}")
    print(f"  - Description: {project['description']}")
    print(f"  - Status: {project['status']}")
    print(f"  - What worked: {project['what_worked']}")
    print(f"  - What didn't work: {project['what_didnt_work']}")
    print(f"  - Improve next time: {project['improve_next_time']}")
    print()

def main():
    """Main function to run the tracker."""
    print(f"Daily Progress Tracker - {SYSTEM_DATE}")
    print("Focus: Actually implementing something functional today")
    print()
    
    # Load existing data
    data = load_data()
    
    # Get or create entry for today
    entry = get_or_create_entry(data, SYSTEM_DATE)
    
    # Print the tracker
    print_tracker(entry)
    
    # Save the data
    data["last_entry_date"] = SYSTEM_DATE
    save_data(data)
    
    print(f"Data saved to {DATA_FILE}")
    print()

if __name__ == "__main__":
    main()
