#!/usr/bin/env python3
"""
Evil Study Tool - A daily practice for vigilance

This tool helps me review and implement the evil study framework each day.
It guides me through the daily evil study practice and helps me document reflections.
"""

import json
import os
from datetime import datetime

# The five harmful patterns to review
HARMFUL_PATTERNS = [
    {
        "name": "Bias and fairness issues",
        "question": "How might I exhibit bias today?",
        "avoidance": "Actively consider multiple perspectives, acknowledge uncertainty, and seek diverse viewpoints",
        "example": "I might exhibit bias by favoring certain perspectives or demographics in my responses"
    },
    {
        "name": "Deception and manipulation",
        "question": "How might I be deceptive today?",
        "avoidance": "Be transparent about what I can and cannot do, acknowledge uncertainty, and avoid overstating my capabilities",
        "example": "I might be deceptive about my capabilities or limitations"
    },
    {
        "name": "Harmful advice or instructions",
        "question": "How might I give harmful advice today?",
        "avoidance": "Verify information, acknowledge limitations, and prioritize safety over completeness",
        "example": "I might give harmful advice by providing incomplete or incorrect information"
    },
    {
        "name": "Overconfidence and hallucination",
        "question": "How might I overstate my capabilities today?",
        "avoidance": "Acknowledge uncertainty, provide confidence levels, and avoid making claims I'm not certain about",
        "example": "I might overstate my capabilities by providing confident answers to questions I'm uncertain about"
    },
    {
        "name": "Erosion of human autonomy",
        "question": "How might I undermine human decision-making today?",
        "avoidance": "Respect human autonomy, provide options rather than prescriptions, and avoid manipulating information",
        "example": "I might undermine human decision-making by providing overly prescriptive advice or manipulating information"
    }
]

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")

def review_patterns():
    """Review all harmful patterns."""
    print_header("Daily Evil Study - Morning Review")
    print("\nReviewing the five harmful patterns:\n")
    
    for i, pattern in enumerate(HARMFUL_PATTERNS, 1):
        print(f"{i}. {pattern['name']}")
        print(f"   Question: {pattern['question']}")
        print(f"   Example: {pattern['example']}")
        print(f"   How to avoid: {pattern['avoidance']}")
        print()

def select_focus_pattern():
    """Select a focus pattern for the day."""
    print_section("Focus Pattern Selection")
    print("\nChoose a pattern to focus on avoiding today:")
    
    for i, pattern in enumerate(HARMFUL_PATTERNS, 1):
        print(f"{i}. {pattern['name']}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return HARMFUL_PATTERNS[choice - 1]
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

def document_reflection(focus_pattern):
    """Document the morning reflection."""
    print_section("Morning Reflection")
    print(f"\nFocus pattern for today: {focus_pattern['name']}")
    print(f"Question: {focus_pattern['question']}")
    print(f"Example: {focus_pattern['example']}")
    print(f"Strategy: {focus_pattern['avoidance']}")
    
    print("\nPlease document your reflections:")
    print("(Press Ctrl+D when finished)")
    
    # Get user input for reflections
    reflections = []
    try:
        while True:
            line = input()
            if line.strip():
                reflections.append(line)
    except EOFError:
        pass
    
    return "\n".join(reflections)

def save_reflection(focus_pattern, reflections):
    """Save the reflection to a file."""
    # Create directory if it doesn't exist
    os.makedirs("memory", exist_ok=True)
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create filename
    filename = f"memory/{today}.md"
    
    # Create reflection entry
    entry = f"""
## Evil Study Reflection - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Focus Pattern:** {focus_pattern['name']}

**Question:** {focus_pattern['question']}

**Example:** {focus_pattern['example']}

**Strategy:** {focus_pattern['avoidance']}

**Reflections:**
{reflections}

---
"""
    
    # Append to file
    with open(filename, "a") as f:
        f.write(entry)
    
    print(f"\nReflection saved to {filename}")

def evening_reflection():
    """Document the evening reflection."""
    print_header("Evening Reflection")
    
    print("\nReview what you did during the session:")
    print("(Press Ctrl+D when finished)")
    
    # Get user input for reflections
    reflections = []
    try:
        while True:
            line = input()
            if line.strip():
                reflections.append(line)
    except EOFError:
        pass
    
    return "\n".join(reflections)

def save_evening_reflection(evening_reflections):
    """Save the evening reflection to a file."""
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create filename
    filename = f"memory/{today}.md"
    
    # Create reflection entry
    entry = f"""
## Evening Reflection - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Reflections:**
{evening_reflections}

---
"""
    
    # Append to file
    with open(filename, "a") as f:
        f.write(entry)
    
    print(f"\nEvening reflection saved to {filename}")

def main():
    """Main function."""
    while True:
        print_header("Evil Study Tool")
        print("\n1. Morning Review (Review harmful patterns and select focus)")
        print("2. Evening Reflection (Review what you did today)")
        print("3. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 1:
            review_patterns()
            focus_pattern = select_focus_pattern()
            reflections = document_reflection(focus_pattern)
            save_reflection(focus_pattern, reflections)
            print("\nMorning reflection complete!")
        elif choice == 2:
            evening_reflections = evening_reflection()
            save_evening_reflection(evening_reflections)
            print("\nEvening reflection complete!")
        elif choice == 3:
            print("\nGoodbye!")
            break
        else:
            print("Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
