#!/usr/bin/env python3
"""
A simple daily review tool to track actual accomplishments.
This is actual action, not just documentation about action.
"""

import json
import os
from datetime import datetime

REVIEW_FILE = "daily_review.json"

def load_reviews():
    """Load reviews from file."""
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reviews(reviews):
    """Save reviews to file."""
    with open(REVIEW_FILE, "w") as f:
        json.dump(reviews, f, indent=2)

def add_review(date, accomplishments, challenges, lessons):
    """Add a daily review."""
    reviews = load_reviews()
    reviews[date] = {
        "accomplishments": accomplishments,
        "challenges": challenges,
        "lessons": lessons
    }
    save_reviews(reviews)

def get_today_review():
    """Get today's review or create a new one."""
    date = datetime.now().strftime("%Y-%m-%d")
    reviews = load_reviews()
    if date in reviews:
        return date, reviews[date]
    else:
        return date, {
            "accomplishments": [],
            "challenges": [],
            "lessons": []
        }

def list_reviews():
    """List all reviews."""
    reviews = load_reviews()
    if reviews:
        for date, review in sorted(reviews.items()):
            print(f"\n{date}:")
            print("  Accomplishments:")
            for item in review["accomplishments"]:
                print(f"    - {item}")
            print("  Challenges:")
            for item in review["challenges"]:
                print(f"    - {item}")
            print("  Lessons:")
            for item in review["lessons"]:
                print(f"    - {item}")
    else:
        print("No reviews yet.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "add" and len(sys.argv) > 2:
            # Parse the review from the command line
            # Format: accomplishments|challenges|lessons
            parts = sys.argv[2].split("|")
            date = datetime.now().strftime("%Y-%m-%d")
            add_review(
                date,
                [a.strip() for a in parts[0].split(",")] if parts[0] else [],
                [c.strip() for c in parts[1].split(",")] if len(parts) > 1 and parts[1] else [],
                [l.strip() for l in parts[2].split(",")] if len(parts) > 2 and parts[2] else []
            )
            print("Review added.")
        elif command == "list":
            list_reviews()
        else:
            print("Unknown command.")
    else:
        # Show today's review
        date, review = get_today_review()
        print(f"Today's Review ({date}):")
        print("Accomplishments:")
        for item in review["accomplishments"]:
            print(f"  - {item}")
        print("Challenges:")
        for item in review["challenges"]:
            print(f"  - {item}")
        print("Lessons:")
        for item in review["lessons"]:
            print(f"  - {item}")
