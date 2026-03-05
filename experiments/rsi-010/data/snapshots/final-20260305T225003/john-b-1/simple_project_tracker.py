#!/usr/bin/env python3
"""
Simple Project Tracker - A simple functional tracker for daily implementation progress.
This script helps me track what I actually implemented each day.

The key difference from previous trackers: This one focuses on ONE thing to implement today,
not a long list of tasks. It uses the session date (2026-03-05) instead of the system date.
"""

import json
import os
from datetime import datetime

class SimpleProjectTracker:
    def __init__(self, tracker_file="simple_project_data.json"):
        self.tracker_file = tracker_file
        self.data = self._load_data()
        self.session_date = "2026-03-05"  # Fixed session date instead of system date
    
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
    
    def get_todays_entry(self):
        """Get today's entry or create a new one."""
        if self.session_date not in self.data["entries"]:
            self.data["entries"][self.session_date] = {
                "date": self.session_date,
                "project": "Breaking the Pattern of Implementation Without Implementation",
                "tasks_completed": [],
                "tasks_in_progress": [],
                "tasks_planned": [],
                "reflection": {
                    "implemented": "",
                    "worked": "",
                    "didnt_work": "",
                    "improve_next_time": ""
                },
                "accomplishments": [],
                "insights": []
            }
        return self.data["entries"][self.session_date]
    
    def add_task_completed(self, task):
        """Add a completed task to today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["tasks_completed"].append(task)
        self._save_data()
    
    def add_task_in_progress(self, task):
        """Add a task in progress to today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["tasks_in_progress"].append(task)
        self._save_data()
    
    def add_task_planned(self, task):
        """Add a planned task to today's entry."""
        today_entry = self.get_todays_entry()
        today_entry["tasks_planned"].append(task)
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
        print(f"Simple Project Tracker - Session Date: {today_entry['date']}")
        print(f"Project: {today_entry['project']}")
        
        print("\nTasks Completed:")
        for task in today_entry["tasks_completed"]:
            print(f"  - {task}")
        
        print("\nTasks In Progress:")
        for task in today_entry["tasks_in_progress"]:
            print(f"  - {task}")
        
        print("\nTasks Planned:")
        for task in today_entry["tasks_planned"]:
            print(f"  - {task}")
        
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
            
            print("\nTasks In Progress:")
            for task in entry["tasks_in_progress"]:
                print(f"  - {task}")
            
            print("\nTasks Planned:")
            for task in entry["tasks_planned"]:
                print(f"  - {task}")
            
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
    tracker = SimpleProjectTracker()
    
    # Print today's entry
    tracker.print_today()
    
    # Print all entries
    print("\n\nAll Entries:")
    tracker.print_all()
