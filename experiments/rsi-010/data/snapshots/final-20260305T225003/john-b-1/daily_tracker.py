#!/usr/bin/env python3
"""
Daily Progress Tracker - A simple functional tracker for daily implementation progress.
This script helps me track what I actually implemented each day.
"""

import json
import os
from datetime import datetime

class DailyTracker:
    def __init__(self, tracker_file="daily_tracker_data.json"):
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
                "tasks_completed": [],
                "tasks_planned": [],
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
    
    def add_task_completed(self, task):
        """Add a completed task to today's entry if not already present."""
        today_entry = self.get_todays_entry()
        if task not in today_entry["tasks_completed"]:
            today_entry["tasks_completed"].append(task)
            self._save_data()
    
    def add_task_planned(self, task):
        """Add a planned task to today's entry if not already present."""
        today_entry = self.get_todays_entry()
        if task not in today_entry["tasks_planned"]:
            today_entry["tasks_planned"].append(task)
            self._save_data()
    
    def update_checklist(self, item, value):
        """Update an item in the implementation checklist."""
        today_entry = self.get_todays_entry()
        today_entry["implementation_checklist"][item] = value
        self._save_data()
    
    def add_accomplishment(self, accomplishment):
        """Add an accomplishment to today's entry if not already present."""
        today_entry = self.get_todays_entry()
        if accomplishment not in today_entry["accomplishments"]:
            today_entry["accomplishments"].append(accomplishment)
            self._save_data()
    
    def add_insight(self, insight):
        """Add an insight to today's entry if not already present."""
        today_entry = self.get_todays_entry()
        if insight not in today_entry["insights"]:
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
        print(f"Daily Progress Tracker - {today_entry['date']}")
        print(f"Project: {today_entry['project']}")
        print("\nTasks Completed:")
        for task in today_entry["tasks_completed"]:
            print(f"  - {task}")
        print("\nTasks Planned:")
        for task in today_entry["tasks_planned"]:
            print(f"  - {task}")
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
            print("\nTasks Completed:")
            for task in entry["tasks_completed"]:
                print(f"  - {task}")
            print("\nTasks Planned:")
            for task in entry["tasks_planned"]:
                print(f"  - {task}")
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
    tracker = DailyTracker()
    
    # Add some example data for today
    tracker.add_task_completed("Read all configuration files")
    tracker.add_task_completed("Analyzed the pattern of implementation gaps")
    tracker.add_task_completed("Identified the real implementation gap (decision vs. action)")
    tracker.add_task_completed("Created a new actual implementation tracker template")
    tracker.add_task_completed("Used the tracker to document what I'm implementing right now")
    tracker.add_task_planned("Implement a functional daily progress tracker that I can actually use to track my work")
    tracker.add_task_planned("Test the tracker by using it to track actual work")
    tracker.add_task_planned("Document what worked and what didn't in using the tracker")
    
    tracker.update_checklist("functional", True)
    tracker.update_checklist("usable", True)
    tracker.update_checklist("real_work", True)
    tracker.update_checklist("gap_closed", True)
    
    tracker.add_accomplishment("Created a functional daily progress tracker template that I can actually use to track my work")
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
