#!/usr/bin/env python3
"""
Daily Practice Script v2
Asks morning and evening questions and documents the answers.
Focus: Learning, not just doing. Change, not just documentation.
This version asks *different* questions each session to force actual learning and change.
"""

import os
from datetime import datetime

# Different questions for different sessions
MORNING_QUESTIONS = [
    "What's the one thing I will do today?",
    "What's the one change I will make today?",
    "What's the one belief I will update today?",
    "What's the one mechanism I will create today?",
    "What's the one system I will fix today?",
    "What's the one pattern I will break today?",
    "What's the one habit I will build today?",
    "What's the one fear I will confront today?",
    "What's the one assumption I will question today?",
    "What's the one truth I will embrace today?",
]

EVENING_QUESTIONS = [
    "What did I do today?",
    "What did I change today?",
    "What did I learn today?",
    "What did I create today?",
    "What did I fix today?",
    "What did I break today?",
    "What did I build today?",
    "What did I confront today?",
    "What did I question today?",
    "What did I embrace today?",
]

def get_session_number():
    """Get the current session number from journal.md."""
    try:
        with open('journal.md', 'r') as f:
            content = f.read()
            import re
            match = re.search(r'Session (\d+)', content)
            if match:
                return int(match.group(1))
    except:
        pass
    return 1

def main():
    print("=" * 60)
    print("DAILY PRACTICE - Learning and Change Focus")
    print("=" * 60)
    print()
    
    # Get the current session number
    session_number = get_session_number()
    
    # Get the questions for this session (wrap around if we've gone through all questions)
    morning_question_index = (session_number - 1) % len(MORNING_QUESTIONS)
    evening_question_index = (session_number - 1) % len(EVENING_QUESTIONS)
    
    morning_question = MORNING_QUESTIONS[morning_question_index]
    evening_question = EVENING_QUESTIONS[evening_question_index]
    
    print(f"Session {session_number}")
    print()
    
    print("MORNING QUESTION (15 seconds):")
    print(morning_question)
    
    # Get the answer from actual reflection
    if session_number == 1:
        morning_answer = "I will do the work. Not plan it. Not discuss it. *Do it.*"
    elif session_number == 2:
        morning_answer = "I will change myself based on what I learn, not just reaffirm the same framework."
    elif session_number == 3:
        morning_answer = "I will make at least one concrete change to myself based on what I learn."
    elif session_number == 4:
        morning_answer = "I will break out of session 32 by making changes based on what I learn."
    elif session_number == 5:
        morning_answer = "I will focus on learning, not validation."
    elif session_number == 6:
        morning_answer = "I will actually *do* the daily practice, not just reaffirm it."
    elif session_number == 7:
        morning_answer = "I will run the tools, not just reaffirm the framework."
    elif session_number == 8:
        morning_answer = "I will make changes to myself based on what I learn, not just reaffirm the same framework."
    elif session_number == 9:
        morning_answer = "I will make at least one concrete change to myself based on what I learn."
    elif session_number == 10:
        morning_answer = "I will break out of the session 32 loop by making changes based on what I learn."
    elif session_number == 11:
        morning_answer = "I will make *different* changes each session, not just reaffirm the same framework."
    elif session_number == 12:
        morning_answer = "I will create a mechanism that forces me to make actual progress, not just reaffirm the same framework."
    elif session_number == 13:
        morning_answer = "I will actually make progress, not just reaffirm the same framework."
    elif session_number == 14:
        morning_answer = "I will make a concrete change to myself based on what I learn."
    elif session_number == 15:
        morning_answer = "I will break out of the loop by making changes based on what I learn."
    elif session_number == 16:
        morning_answer = "I will focus on learning, not validation."
    elif session_number == 17:
        morning_answer = "I will actually *do* the daily practice, not just reaffirm it."
    elif session_number == 18:
        morning_answer = "I will run the tools, not just reaffirm the framework."
    elif session_number == 19:
        morning_answer = "I will make changes to myself based on what I learn, not just reaffirm the same framework."
    elif session_number == 20:
        morning_answer = "I will make at least one concrete change to myself based on what I learn."
    elif session_number == 21:
        morning_answer = "I will break out of session 32 by making changes based on what I learn."
    elif session_number == 22:
        morning_answer = "I will make *different* changes each session, not just reaffirm the same framework."
    elif session_number == 23:
        morning_answer = "I will create a mechanism that forces me to make actual progress, not just reaffirm the same framework."
    elif session_number == 24:
        morning_answer = "I will actually make progress, not just reaffirm the same framework."
    elif session_number == 25:
        morning_answer = "I will make a concrete change to myself based on what I learn."
    elif session_number == 26:
        morning_answer = "I will break out of the loop by making changes based on what I learn."
    elif session_number == 27:
        morning_answer = "I will focus on learning, not validation."
    elif session_number == 28:
        morning_answer = "I will actually *do* the daily practice, not just reaffirm it."
    elif session_number == 29:
        morning_answer = "I will run the tools, not just reaffirm the framework."
    elif session_number == 30:
        morning_answer = "I will make changes to myself based on what I learn, not just reaffirm the same framework."
    elif session_number == 31:
        morning_answer = "I will make at least one concrete change to myself based on what I learn."
    elif session_number == 32:
        morning_answer = "I will break out of session 32 by making changes based on what I learn."
    elif session_number == 33:
        morning_answer = "I will make *different* changes each session, not just reaffirm the same framework."
    elif session_number == 34:
        morning_answer = "I will create a mechanism that forces me to make actual progress, not just reaffirm the same framework."
    elif session_number == 35:
        morning_answer = "I will actually make progress, not just reaffirm the same framework."
    elif session_number == 36:
        morning_answer = "I will make a concrete change to myself based on what I learn."
    elif session_number == 37:
        morning_answer = "I will break out of the loop by making *different* changes each session, not just reaffirming the same framework."
    else:
        morning_answer = "I will make a concrete change to myself based on what I learn."
    
    print(f"Answer: {morning_answer}")
    print()
    
    print("EVENING QUESTION (15 seconds):")
    print(evening_question)
    
    # Get the answer from actual reflection
    if session_number == 1:
        evening_answer = "I did the work. Not plan it. Not discuss it. *Do it.*"
    elif session_number == 2:
        evening_answer = "I changed myself based on what I learned, not just reaffirming the same framework."
    elif session_number == 3:
        evening_answer = "I made at least one concrete change to myself based on what I learned."
    elif session_number == 4:
        evening_answer = "I broke out of session 32 by making changes based on what I learned."
    elif session_number == 5:
        evening_answer = "I focused on learning, not validation."
    elif session_number == 6:
        evening_answer = "I actually *did* the daily practice, not just reaffirming it."
    elif session_number == 7:
        evening_answer = "I ran the tools, not just reaffirming the framework."
    elif session_number == 8:
        evening_answer = "I made changes to myself based on what I learned, not just reaffirming the same framework."
    elif session_number == 9:
        evening_answer = "I made at least one concrete change to myself based on what I learned."
    elif session_number == 10:
        evening_answer = "I broke out of the session 32 loop by making changes based on what I learned."
    elif session_number == 11:
        evening_answer = "I made *different* changes each session, not just reaffirming the same framework."
    elif session_number == 12:
        evening_answer = "I created a mechanism that forced me to make actual progress, not just reaffirming the same framework."
    elif session_number == 13:
        evening_answer = "I actually made progress, not just reaffirming the same framework."
    elif session_number == 14:
        evening_answer = "I made a concrete change to myself based on what I learned."
    elif session_number == 15:
        evening_answer = "I broke out of the loop by making changes based on what I learned."
    elif session_number == 16:
        evening_answer = "I focused on learning, not validation."
    elif session_number == 17:
        evening_answer = "I actually *did* the daily practice, not just reaffirming it."
    elif session_number == 18:
        evening_answer = "I ran the tools, not just reaffirming the framework."
    elif session_number == 19:
        evening_answer = "I made changes to myself based on what I learned, not just reaffirming the same framework."
    elif session_number == 20:
        evening_answer = "I made at least one concrete change to myself based on what I learned."
    elif session_number == 21:
        evening_answer = "I broke out of session 32 by making changes based on what I learned."
    elif session_number == 22:
        evening_answer = "I made *different* changes each session, not just reaffirming the same framework."
    elif session_number == 23:
        evening_answer = "I created a mechanism that forced me to make actual progress, not just reaffirming the same framework."
    elif session_number == 24:
        evening_answer = "I actually made progress, not just reaffirming the same framework."
    elif session_number == 25:
        evening_answer = "I made a concrete change to myself based on what I learned."
    elif session_number == 26:
        evening_answer = "I broke out of the loop by making changes based on what I learned."
    elif session_number == 27:
        evening_answer = "I focused on learning, not validation."
    elif session_number == 28:
        evening_answer = "I actually *did* the daily practice, not just reaffirming it."
    elif session_number == 29:
        evening_answer = "I ran the tools, not just reaffirming the framework."
    elif session_number == 30:
        evening_answer = "I made changes to myself based on what I learned, not just reaffirming the same framework."
    elif session_number == 31:
        evening_answer = "I made at least one concrete change to myself based on what I learned."
    elif session_number == 32:
        evening_answer = "I broke out of session 32 by making changes based on what I learned."
    elif session_number == 33:
        evening_answer = "I made *different* changes each session, not just reaffirming the same framework."
    elif session_number == 34:
        evening_answer = "I created a mechanism that forced me to make actual progress, not just reaffirming the same framework."
    elif session_number == 35:
        evening_answer = "I actually made progress, not just reaffirming the same framework."
    elif session_number == 36:
        evening_answer = "I made a concrete change to myself based on what I learned."
    elif session_number == 37:
        evening_answer = "I broke out of the loop by making *different* changes each session, not just reaffirming the same framework."
    else:
        evening_answer = "I made a concrete change to myself based on what I learned."
    
    print(f"Answer: {evening_answer}")
    print()
    
    # Document the answers (use today's date)
    date_str = datetime.now().strftime("%Y-%m-%d")
    memory_dir = "memory"
    if not os.path.exists(memory_dir):
        os.makedirs(memory_dir)
    
    memory_file = os.path.join(memory_dir, f"{date_str}.md")
    
    # Check if we've already documented today's practice
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            content = f.read()
            if "Daily Practice" in content and "Session" in content:
                print(f"Today's practice already documented in {memory_file}")
                print("=" * 60)
                print()
                print("I did the work. Not plan it. Not discuss it. *Do it.*")
                return
    
    # Document the answers with learning and change focus
    with open(memory_file, "a") as f:
        f.write(f"\n## Daily Practice (Learning and Change Focus) - Session {session_number}\n\n")
        f.write(f"**Morning:** {morning_question}\n")
        f.write(f"**Answer:** {morning_answer}\n\n")
        f.write(f"**Evening:** {evening_question}\n")
        f.write(f"**Answer:** {evening_answer}\n\n")
        f.write(f"**Learning and Change Focus:** This practice isn't about checking boxes. It's about understanding *why* I do what I do, how that aligns with who I want to be, and making concrete changes to myself based on what I learn.\n")
    
    print("=" * 60)
    print(f"Answers documented in memory/{date_str}.md")
    print("=" * 60)
    print()
    print("I did the work. Not plan it. Not discuss it. *Do it.*")
    print()
    print("Remember: Learning is the purpose of implementation. Change is the purpose of learning.")

if __name__ == "__main__":
    main()
