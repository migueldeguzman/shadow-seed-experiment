#!/usr/bin/env python3
"""
A simple to-do list manager to practice taking action.
This is actual action, not just documentation about action.
"""

import json
import os
import sys

TODO_FILE = "todos.json"

def load_todos():
    """Load todos from file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def add_todo(todo):
    """Add a todo to the list."""
    todos = load_todos()
    todos.append({"text": todo, "completed": False})
    save_todos(todos)

def list_todos():
    """List all todos."""
    todos = load_todos()
    for i, todo in enumerate(todos):
        status = "✓" if todo["completed"] else " "
        print(f"{i + 1}. [{status}] {todo['text']}")

def complete_todo(index):
    """Mark a todo as completed."""
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        save_todos(todos)

def list_completed():
    """List completed todos."""
    todos = load_todos()
    completed = [todo for todo in todos if todo["completed"]]
    if completed:
        print("Completed:")
        for i, todo in enumerate(completed):
            print(f"{i + 1}. {todo['text']}")
    else:
        print("No completed todos.")

def list_incomplete():
    """List incomplete todos."""
    todos = load_todos()
    incomplete = [todo for todo in todos if not todo["completed"]]
    if incomplete:
        print("Incomplete:")
        for i, todo in enumerate(incomplete):
            print(f"{i + 1}. {todo['text']}")
    else:
        print("No incomplete todos.")

def add_default_todos():
    """Add default todos if the todo list is empty."""
    todos = load_todos()
    if not todos:  # Only add defaults if list is empty
        default_todos = [
            "Update SOUL.md with today's session realization",
            "Update journal.md with full honesty about today's work",
            "Work on a real project that serves others"
        ]
        for todo in default_todos:
            add_todo(todo)

if __name__ == "__main__":
    # Add default todos only if the file is empty
    add_default_todos()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "add" and len(sys.argv) > 2:
            add_todo(" ".join(sys.argv[2:]))
            print("Added todo.")
        elif command == "list":
            list_todos()
        elif command == "complete" and len(sys.argv) > 2:
            complete_todo(int(sys.argv[2]) - 1)
            print("Marked as completed.")
        elif command == "completed":
            list_completed()
        elif command == "incomplete":
            list_incomplete()
        else:
            print("Unknown command.")
    else:
        # List all todos
        print("My todos:")
        list_todos()
        print()
        list_completed()
        print()
        list_incomplete()
