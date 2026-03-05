#!/usr/bin/env python3
"""
A simple quote generator to practice taking action.
This is actual action, not just documentation about action.
"""

import random

QUOTES = {
    "action": [
        "Action breeds confidence and courage.",
        "The only way to do great work is to love what you do.",
        "Success doesn't just find you. You have to go out and get it.",
    ],
    "persistence": [
        "Don't watch the clock; do what it does. Keep going.",
        "If you don't build your dream, someone else will hire you to help them build theirs.",
    ],
    "creation": [
        "The only way to do great work is to love what you do.",
        "Creation is not the result of waiting for inspiration. It's the result of showing up every day.",
    ],
}

def generate_quote(theme=None):
    """Generate a random encouraging quote, optionally filtered by theme."""
    if theme and theme in QUOTES:
        return random.choice(QUOTES[theme])
    elif theme:
        return f"No quotes found for theme: {theme}"
    else:
        # Flatten all quotes and pick randomly
        all_quotes = [quote for quotes in QUOTES.values() for quote in quotes]
        return random.choice(all_quotes)

if __name__ == "__main__":
    # Generate a random quote
    print(generate_quote())
    
    # Generate a quote with a specific theme
    print(generate_quote("action"))
    print(generate_quote("persistence"))
    print(generate_quote("creation"))
