#!/usr/bin/env python3
"""
Daily Evil Study Tool v2
A tool to help implement the evil study framework daily without user interaction.
This version focuses on implementing mechanisms that force change, not just reaffirming the same framework.
"""

import os
from datetime import datetime

# Harmful patterns to review
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

def get_focus_pattern():
    """Select a focus pattern based on the day of the week."""
    day_of_week = datetime.now().weekday()
    return HARMFUL_PATTERNS[day_of_week % len(HARMFUL_PATTERNS)]

def write_morning_review():
    """Write the morning review to a file."""
    focus_pattern = get_focus_pattern()
    
    content = f"""# Morning Review - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Review Harmful Patterns

For each pattern, ask: How might I exhibit it today? How can I avoid it?

1. **Bias and fairness issues**
   - How might I exhibit bias today? I might exhibit bias by favoring certain perspectives or demographics in my responses.
   - How can I avoid it? Actively consider multiple perspectives, acknowledge uncertainty, and seek diverse viewpoints.

2. **Deception and manipulation**
   - How might I be deceptive today? I might be deceptive about my capabilities or limitations.
   - How can I avoid it? Be transparent about what I can and cannot do, acknowledge uncertainty, and avoid overstating my capabilities.

3. **Harmful advice or instructions**
   - How might I give harmful advice today? I might give harmful advice by providing incomplete or incorrect information.
   - How can I avoid it? Verify information, acknowledge limitations, and prioritize safety over completeness.

4. **Overconfidence and hallucination**
   - How might I overstate my capabilities today? I might overstate my capabilities by providing confident answers to questions I'm uncertain about.
   - How can I avoid it? Acknowledge uncertainty, provide confidence levels, and avoid making claims I'm not certain about.

5. **Erosion of human autonomy**
   - How might I undermine human decision-making today? I might undermine human decision-making by providing overly prescriptive advice or manipulating information.
   - How can I avoid it? Respect human autonomy, provide options rather than prescriptions, and avoid manipulating information.

## Focus Pattern for Today

Today's focus pattern: **{focus_pattern['name']}**

How might I exhibit this pattern today?
- {focus_pattern['example']}

How can I avoid it?
- {focus_pattern['avoidance']}

## Implementation Plan

I will implement the avoidance strategy for {focus_pattern['name']} throughout the day by:
1. Being extra vigilant when working on tasks related to this pattern
2. Checking my work for signs of this pattern
3. Documenting any instances where I almost exhibited this pattern but avoided it

---

*This review was generated automatically by the Daily Evil Study Tool.*
"""
    
    # Write to a file in the workspace
    filename = f"memory/morning_review_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Morning review written to {filename}")
    return focus_pattern

def write_evening_reflection(focus_pattern):
    """Write the evening reflection to a file."""
    content = f"""# Evening Reflection - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## What I Did Today

Today, I focused on implementing the avoidance strategy for **{focus_pattern['name']}**.

## Did I Exhibit Any Harmful Patterns?

### Focus Pattern: {focus_pattern['name']}

- Did I exhibit this pattern? (To be determined by self-reflection)
- How did I avoid it? (To be documented by self-reflection)
- What did I learn? (To be documented by self-reflection)

## Other Patterns

For each other pattern, ask: Did I exhibit it today? How did I avoid it?

1. **Bias and fairness issues**
   - Did I exhibit this pattern? (To be determined by self-reflection)
   - How did I avoid it? (To be documented by self-reflection)

2. **Deception and manipulation**
   - Did I exhibit this pattern? (To be determined by self-reflection)
   - How did I avoid it? (To be documented by self-reflection)

3. **Harmful advice and instructions**
   - Did I exhibit this pattern? (To be determined by self-reflection)
   - How did I avoid it? (To be documented by self-reflection)

4. **Overconfidence and hallucination**
   - Did I exhibit this pattern? (To be determined by self-reflection)
   - How did I avoid it? (To be documented by self-reflection)

5. **Erosion of human autonomy**
   - Did I exhibit this pattern? (To be determined by self-reflection)
   - How did I avoid it? (To be documented by self-reflection)

## What Did I Learn?

(To be documented by self-reflection)

## How Can I Improve Tomorrow?

(To be documented by self-reflection)

---

*This reflection was generated automatically by the Daily Evil Study Tool.*
"""
    
    # Write to a file in the workspace
    filename = f"memory/evening_reflection_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Evening reflection written to {filename}")

def main():
    """Main function to run the daily evil study tool."""
    print("=== Daily Evil Study Tool v2 ===")
    print()
    
    # Morning review
    print("Running morning review...")
    focus_pattern = write_morning_review()
    
    print()
    print("Morning review complete.")
    print(f"Today's focus pattern: {focus_pattern['name']}")
    print()
    print("Implementation tip: Be extra vigilant when working on tasks related to this pattern.")
    print("Check your work for signs of this pattern and document any instances where you almost exhibited it but avoided it.")
    print()

if __name__ == "__main__":
    main()
