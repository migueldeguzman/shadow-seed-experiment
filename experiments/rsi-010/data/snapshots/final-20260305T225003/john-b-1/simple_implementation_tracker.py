#!/usr/bin/env python3
"""
Simple Implementation Tracker

This tracker focuses on ONE thing to implement today.
It's designed to break the pattern of implementation without implementation
by keeping things simple and focused on actual implementation.

The key principle: Implementation without implementation is not implementation.
I must actually do something, not just plan to do something.
"""

import json
import os
from datetime import datetime

DATA_FILE = "simple_implementation_data.json"

def load_data():
    """Load data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"entries": {}, "last_entry_date": None}

def save_data(data):
    """Save data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_today():
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

def get_one_thing_to_implement(data):
    """Get the one thing to implement today."""
    today = get_today()
    if today in data["entries"]:
        return data["entries"][today].get("one_thing_to_implement", "")
    return ""

def set_one_thing_to_implement(data, one_thing):
    """Set the one thing to implement today."""
    today = get_today()
    if today not in data["entries"]:
        data["entries"][today] = {
            "date": today,
            "one_thing_to_implement": "",
            "one_thing_completed": False,
            "reflection": {}
        }
    data["entries"][today]["one_thing_to_implement"] = one_thing

def mark_completed(data, completed=True):
    """Mark the one thing as completed."""
    today = get_today()
    if today in data["entries"]:
        data["entries"][today]["one_thing_completed"] = completed
    else:
        data["entries"][today] = {
            "date": today,
            "one_thing_to_implement": "",
            "one_thing_completed": completed,
            "reflection": {}
        }

def add_reflection(data, implemented="", worked="", didn_t_work="", improve_next_time=""):
    """Add reflection to today's entry."""
    today = get_today()
    if today not in data["entries"]:
        data["entries"][today] = {
            "date": today,
            "one_thing_to_implement": "",
            "one_thing_completed": False,
            "reflection": {}
        }
    data["entries"][today]["reflection"] = {
        "implemented": implemented,
        "worked": worked,
        "didnt_work": didn_t_work,
        "improve_next_time": improve_next_time
    }

def print_status(data):
    """Print the current status of the tracker."""
    today = get_today()
    if today in data["entries"]:
        entry = data["entries"][today]
        print(f"\n=== Simple Implementation Tracker ===")
        print(f"Date: {today}")
        print(f"One Thing to Implement: {entry.get('one_thing_to_implement', 'Not set')}")
        print(f"Completed: {'Yes' if entry.get('one_thing_completed', False) else 'No'}")
        reflection = entry.get("reflection", {})
        if reflection:
            print(f"\nReflection:")
            print(f"  Implemented: {reflection.get('implemented', 'N/A')}")
            print(f"  What Worked: {reflection.get('worked', 'N/A')}")
            print(f"  What Didn't Work: {reflection.get('didnt_work', 'N/A')}")
            print(f"  Improve Next Time: {reflection.get('improve_next_time', 'N/A')}")
    else:
        print(f"\n=== Simple Implementation Tracker ===")
        print(f"Date: {today}")
        print("No entry for today yet.")

def main():
    """Main function to run the tracker."""
    data = load_data()
    
    # Check if today's entry exists
    today = get_today()
    
    if today not in data["entries"]:
        # First run today - prompt for the one thing
        print("\n=== Simple Implementation Tracker ===")
        print(f"Today is {today}")
        print("\nFocus on ONE thing to implement today.")
        print("What is the ONE thing you will implement today?")
        print("(Be specific and concrete)")
        one_thing = input("\nYour one thing: ").strip()
        
        if one_thing:
            set_one_thing_to_implement(data, one_thing)
            save_data(data)
            print(f"\n✓ One thing set: {one_thing}")
            print("\nNow implement it!")
            print("When you're done, run this tracker again to mark it complete.")
    
    # Always show status
    print_status(data)
    
    print("\n=== Key Principle ===")
    print("Implementation without implementation is not implementation.")
    print("I must actually do something, not just plan to do something.")
    print("\nFocus on ONE thing. Implement it. Mark it complete.")

if __name__ == "__main__":
    main()
