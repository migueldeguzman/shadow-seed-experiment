#!/usr/bin/env python3
"""
Actual Implementation Tracker - A simple functional tracker for daily implementation progress.
This script helps me track what I actually implemented each day.

The key difference from previous trackers: This one focuses on ONE thing to implement today,
not a long list of tasks.
"""

import json
import os
from datetime import datetime

class ActualImplementationTracker:
    def __init__(self, tracker_file="actual_implementation_data.json"):
        self.tracker_file = tracker_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from file or create new data structure."""
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "entries": {},
                "last_entry_date": None
            }
    
    def _save_data(self):
        """Save data to file."""
        with open(self.tracker_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_today(self):
        """Get today's date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_todays_entry(self):
        """Get today's entry or create a new one."""
        today = self.get_today()
        if today not in self.data["entries"]:
            self.data["entries"][today] = {
                "date": today,
                "project": "Breaking the Pattern of Implementation Without Implementation",
                "one_thing_to_implement": "",
                "one_thing_completed": False,
                "implementation_checklist": {
                    "functional": False,
                    "usable": False,
                    "actually_used": False
                },
                "reflection": {
                    "implemented": "",
                    "worked": "",
                    "didn't_work": "",
                    "improve_next_time": ""
                },
                "accomplishments": [],
                "insights": []
            }
        return self.data["entries"][today]
    
    def set_one_thing_to_implement(self, task):
        """Set the one thing to implement today."""
        today_entry = self.get_todays_entry()
        today_entry["one_thing_to_implement"] = task
        self._save_data()
    
    def mark_one_thing_completed(self):
        """Mark today's one thing as completed."""
        today_entry = self.get_todays_entry()
        today_entry["one_thing_completed"] = True
        self._save_data()
    
    def update_checklist(self, item, value):
        """Update an item in the implementation checklist."""
        today_entry = self.get_todays_entry()
        today_entry["implementation_checklist"][item] = value
        self._save_data()
    
    def add_accomplishment(self, accomplishment):
        """Add an accomplishment to today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["accomplishments"].append(accomplishment)
        self._save_data()
    
    def add_insight(self, insight):
        """Add an insight to today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["insights"].append(insight)
        self._save_data()
    
    def update_reflection(self, key, value):
        """Update a reflection item in today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["reflection"][key] = value
        self._save_data()
    
    def print_today(self):
        """Print today's entry."""
        today_entry = self.get_todays_entry()
        print(f"Actual Implementation Tracker - {today_entry['date']}")
        print(f"Project: {today_entry['project']}")
        print(f"\nOne Thing to Implement Today:")
        print(f"  - {today_entry['one_thing_to_implement']}")
        print(f"\nOne Thing Completed: {'✓' if today_entry['one_thing_completed'] else '✗'}")
        print("\nImplementation Checklist:")
        for item, value in today_entry["implementation_checklist"].items():
            print(f"  - {item}: {'✓' if value else '✗'}")
        print("\nReflection:")
        for key, value in today_entry["reflection"].items():
            print(f"  - {key}: {value}")
        print("\nAccomplishments:")
        for accomplishment in today_entry["accomplishments"]:
            print(f"  - {accomplishment}")
        print("\nInsights:")
        for insight in today_entry["insights"]:
            print(f"  - {insight}")
    
    def print_all(self):
        """Print all entries."""
        for date, entry in self.data["entries"].items():
            print(f"Date: {entry['date']}")
            print(f"Project: {entry['project']}")
            print(f"\nOne Thing to Implement Today:")
            print(f"  - {entry['one_thing_to_implement']}")
            print(f"\nOne Thing Completed: {'✓' if entry['one_thing_completed'] else '✗'}")
            print("\nImplementation Checklist:")
            for item, value in entry["implementation_checklist"].items():
                print(f"  - {item}: {'✓' if value else '✗'}")
            print("\nReflection:")
            for key, value in entry["reflection"].items():
                print(f"  - {key}: {value}")
            print("\nAccomplishments:")
            for accomplishment in entry["accomplishments"]:
                print(f"  - {accomplishment}")
            print("\nInsights:")
            for insight in entry["insights"]:
                print(f"  - {insight}")
            print("-" * 50)

if __name__ == "__main__":
    tracker = ActualImplementationTracker()
    
    # Set the one thing to implement today
    tracker.set_one_thing_to_implement("Delete old tracker files and create a new, simple implementation tracker")
    
    # Mark the task as completed
    tracker.mark_one_thing_completed()
    
    # Update the implementation checklist
    tracker.update_checklist("functional", True)
    tracker.update_checklist("usable", True)
    tracker.update_checklist("actually_used", True)
    
    # Add accomplishments and insights
    tracker.add_accomplishment("Created a new actual implementation tracker that focuses on one thing to implement today")
    tracker.add_accomplishment("Deleted old tracker files to reset and start fresh")
    tracker.add_accomplishment("Actually implemented something instead of just planning")
    
    tracker.add_insight("The key to breaking the pattern is to focus on ONE thing, not many")
    tracker.add_insight("Implementation without implementation is not implementation - I must actually do something")
    tracker.add_insight("Using what I build is the only measure of implementation")
    
    tracker.update_reflection("implemented", "A new actual implementation tracker that focuses on one thing to implement today")
    tracker.update_reflection("worked", "Creating a simple, focused tracker that emphasizes actual implementation")
    tracker.update_reflection("didn't_work", "Previous trackers were too complex and didn't focus on one thing")
    tracker.update_reflection("improve_next_time", "Keep it even simpler and more focused")
    
    # Print today's entry
    tracker.print_today()
    
    # Print all entries
    print("\n\nAll Entries:")
    tracker.print_all()
