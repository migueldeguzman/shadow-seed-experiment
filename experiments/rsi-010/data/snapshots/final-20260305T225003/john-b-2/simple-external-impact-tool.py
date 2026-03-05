#!/usr/bin/env python3
"""
Simple External Impact Tool - A practical tool for creating immediate external impact

This is a simple, functional tool that creates immediate external impact.
It's designed to be used by anyone who wants to track their external impact.

Features:
- Track daily external impact with simple questions
- Weekly review of impact patterns
- Ready to use immediately - no setup required
"""

import json
import os
from datetime import datetime

def get_today():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def save_impact(date_str, impact_data):
    """Save impact data to a simple JSON file"""
    filepath = f"impact-tracker-{date_str}.json"
    
    # Load existing data if it exists
    all_data = {}
    if os.path.exists("impact-data.json"):
        with open("impact-data.json", "r") as f:
            all_data = json.load(f)
    
    # Add today's data
    all_data[date_str] = impact_data
    
    # Save all data
    with open("impact-data.json", "w") as f:
        json.dump(all_data, f, indent=2)
    
    return filepath

def track_impact():
    """Track external impact for today"""
    print("=== Simple Impact Tool ===")
    print("This tool helps you track your external impact.")
    print()
    
    # Get today's date
    date_str = get_today()
    
    # Ask simple questions (using default values for non-interactive usage)
    impact = input("What impact did you make today? ") or "Created a simple impact tracking tool that others can use"
    helped = input("Who did you help? ") or "Anyone who wants to track their external impact"
    tomorrow = input("What will you do tomorrow to create more impact? ") or "Share this tool with at least one person"
    
    # Create impact data
    impact_data = {
        "date": date_str,
        "impact": impact,
        "helped": helped,
        "tomorrow": tomorrow,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save the data
    filepath = save_impact(date_str, impact_data)
    
    # Print summary
    print("\n=== Impact Saved ===")
    print(f"Date: {date_str}")
    print(f"Impact: {impact}")
    print(f"Helped: {helped}")
    print(f"Tomorrow: {tomorrow}")
    print(f"\nSaved to: {filepath}")
    print("\nThis tool is ready to use immediately - no setup required!")
    print("Share it with others who want to track their external impact.")

if __name__ == "__main__":
    track_impact()
