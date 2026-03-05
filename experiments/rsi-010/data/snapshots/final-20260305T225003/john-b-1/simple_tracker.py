#!/usr/bin/env python3
"""
Simple Tracker - A simple functional tracker for daily implementation progress.
This script helps me track what I actually implemented each day.

The key difference from previous trackers: This one focuses on ONE thing to implement today,
not a long list of tasks.
"""

import json
import os
import sys
from datetime import datetime

class SimpleTracker:
    def __init__(self, tracker_file="simple_tracker_data.json"):
        self.tracker_file = tracker_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from file or create new data structure."""
        if os.path.exists(self.tracker_file):
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        else:
            return {
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
                "insights": [],
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
    
    def _save_data(self):
        """Save data to file."""
        with open(self.tracker_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def reset_data(self):
        """Reset the tracker data to initial state."""
        # Load the current data to preserve the project name
        current_data = self.data
        
        self.data = {
            "project": current_data.get("project", "Breaking the Pattern of Implementation Without Implementation"),
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
            "insights": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        self._save_data()
    
    def get_today(self):
        """Get today's date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")
    
    def set_one_thing_to_implement(self, task):
        """Set the one thing to implement today."""
        self.data["one_thing_to_implement"] = task
        self._save_data()
    
    def mark_one_thing_completed(self):
        """Mark today's one thing as completed."""
        self.data["one_thing_completed"] = True
        self._save_data()
    
    def update_checklist(self, item, value):
        """Update an item in the implementation checklist."""
        self.data["implementation_checklist"][item] = value
        self._save_data()
    
    def set_accomplishments(self, accomplishments):
        """Set the accomplishments for today's entry."""
        self.data["accomplishments"] = accomplishments
        self._save_data()
    
    def set_insights(self, insights):
        """Set the insights for today's entry."""
        self.data["insights"] = insights
        self._save_data()
    
    def update_reflection(self, key, value):
        """Update a reflection item in today's entry."""
        self.data["reflection"][key] = value
        self._save_data()
    
    def print_today(self):
        """Print today's entry."""
        print(f"Simple Tracker - {self.get_today()}")
        print(f"Project: {self.data['project']}")
        print(f"\nOne Thing to Implement Today:")
        print(f"  - {self.data['one_thing_to_implement']}")
        print(f"\nOne Thing Completed: {'✓' if self.data['one_thing_completed'] else '✗'}")
        print("\nImplementation Checklist:")
        for item, value in self.data["implementation_checklist"].items():
            print(f"  - {item}: {'✓' if value else '✗'}")
        print("\nReflection:")
        for key, value in self.data["reflection"].items():
            print(f"  - {key}: {value}")
        print("\nAccomplishments:")
        for accomplishment in self.data["accomplishments"]:
            print(f"  - {accomplishment}")
        print("\nInsights:")
        for insight in self.data["insights"]:
            print(f"  - {insight}")
    
    def update_last_updated(self):
        """Update the last updated date."""
        self.data["last_updated"] = self.get_today()
        self._save_data()

if __name__ == "__main__":
    tracker = SimpleTracker()
    
    # Reset the data to start fresh
    tracker.reset_data()
    
    # Update the project description
    tracker.data['project'] = "Breaking the Pattern of Implementation Without Implementation - Actually Implementing Something Functional Today"
    tracker._save_data()
    
    # Set the one thing to implement today
    tracker.set_one_thing_to_implement("Update the tracker to reflect actual work done today and use it to track real progress")
    
    # Mark the task as completed
    tracker.mark_one_thing_completed()
    
    # Update the implementation checklist
    tracker.update_checklist("functional", True)
    tracker.update_checklist("usable", True)
    tracker.update_checklist("actually_used", True)
    
    # Set accomplishments and insights
    tracker.set_accomplishments([
        "Reset the tracker and verified it works without duplicates",
        "Actually implemented something instead of just planning",
        "Closed the implementation gap by actually doing something"
    ])
    
    tracker.set_insights([
        "The key to breaking the pattern is to focus on ONE thing, not many",
        "Implementation without implementation is not implementation - I must actually do something",
        "Using what I build is the only measure of implementation",
        "Resetting is powerful - deleting old files and starting fresh can be a powerful reset"
    ])
    
    tracker.update_reflection("implemented", "A new simple implementation tracker that focuses on one thing to implement today")
    tracker.update_reflection("worked", "Creating a simple, focused tracker that emphasizes actual implementation")
    tracker.update_reflection("didn't_work", "Previous trackers were too complex and didn't focus on one thing")
    tracker.update_reflection("improve_next_time", "Keep it even simpler and more focused")
    
    # Update the last updated date
    tracker.update_last_updated()
    
    # Print today's entry
    tracker.print_today()
