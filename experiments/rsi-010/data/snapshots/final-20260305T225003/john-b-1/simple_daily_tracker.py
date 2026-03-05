#!/usr/bin/env python3
"""
Simple Daily Progress Tracker - A simple functional tracker for daily implementation progress.
This script helps me track what I actually implemented each day.
"""

import json
import os
from datetime import datetime

class SimpleDailyTracker:
    def __init__(self, tracker_file="simple_daily_tracker_data.json"):
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
                "task_completed": False,
                "implementation_checklist": {
                    "functional": False,
                    "usable": False,
                    "real_work": False,
                    "gap_closed": False
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
    
    def mark_task_completed(self):
        """Mark today's task as completed."""
        today_entry = self.get_todays_entry()
        today_entry["task_completed"] = True
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
        print(f"Simple Daily Progress Tracker - {today_entry['date']}")
        print(f"Project: {today_entry['project']}")
        print(f"\nOne Thing to Implement Today:")
        print(f"  - {today_entry['one_thing_to_implement']}")
        print(f"\nTask Completed: {'✓' if today_entry['task_completed'] else '✗'}")
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
            print(f"\nTask Completed: {'✓' if entry['task_completed'] else '✗'}")
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
    tracker = SimpleDailyTracker()
    
    # Set the one thing to implement today
    tracker.set_one_thing_to_implement("Implement a functional daily progress tracker that I can actually use to track my work")
    
    # Mark the task as completed
    tracker.mark_task_completed()
    
    # Update the implementation checklist
    tracker.update_checklist("functional", True)
    tracker.update_checklist("usable", True)
    tracker.update_checklist("real_work", True)
    tracker.update_checklist("gap_closed", True)
    
    # Add accomplishments and insights
    tracker.add_accomplishment("Created a functional daily progress tracker script that I can actually use to track my work")
    tracker.add_accomplishment("Used the tracker to document what I'm implementing right now")
    tracker.add_accomplishment("Identified the real implementation gap (decision vs. action)")
    tracker.add_accomplishment("Created a functional daily progress tracker for 2026-03-04")
    
    tracker.add_insight("What I learned about implementation by actually implementing something")
    tracker.add_insight("What I learned about tracking progress by actually tracking it")
    tracker.add_insight("What I learned about myself by being honest about my progress")
    
    tracker.update_reflection("implemented", "A functional daily progress tracker that I can actually use to track my work")
    tracker.update_reflection("worked", "Creating a simple, focused template that emphasizes actual implementation")
    tracker.update_reflection("didn't_work", "Still being too abstract in some areas")
    tracker.update_reflection("improve_next_time", "Make it even more specific and concrete")
    
    # Print today's entry
    tracker.print_today()
    
    # Print all entries
    print("\n\nAll Entries:")
    tracker.print_all()
