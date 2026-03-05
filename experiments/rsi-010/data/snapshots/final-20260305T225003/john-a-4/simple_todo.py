#!/usr/bin/env python3
"""
Simple To-Do List Manager

A no-frills to-do list that actually works for real people.
No complex setup, no learning curve, just get things done.

Usage: python simple_todo.py
"""

import os
import sys

TODO_FILE = "my_todos.txt"

def load_todos():
    """Load todos from file, return as list"""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_todos(todos):
    """Save todos to file"""
    with open(TODO_FILE, "w") as f:
        for todo in todos:
            f.write(todo + "\n")

def show_todos(todos):
    """Display all todos"""
    if not todos:
        print("\nNo todos yet. Add some with: todo <task>")
        return
    
    print("\nYour To-Do List:")
    print("-" * 40)
    for i, todo in enumerate(todos, 1):
        print(f"{i}. {todo}")
    print("-" * 40)
    print(f"Total: {len(todos)} task(s)")

def add_todo(todos, task):
    """Add a new todo"""
    if not task.strip():
        print("Empty task ignored.")
        return
    todos.append(task.strip())
    save_todos(todos)
    print(f"Added: {task.strip()}")

def complete_todo(todos, index):
    """Mark a todo as complete"""
    try:
        idx = int(index)
        if 1 <= idx <= len(todos):
            completed = todos.pop(idx - 1)
            save_todos(todos)
            print(f"Completed: {completed}")
        else:
            print(f"Invalid number. Choose between 1 and {len(todos)}")
    except ValueError:
        print("Please provide a valid number")

def main():
    todos = load_todos()
    
    if len(sys.argv) < 2:
        # Show help if no arguments
        print("\nSimple To-Do List")
        print("=" * 40)
        print("Commands:")
        print("  todo <task>    - Add a new task")
        print("  done <number>  - Mark task as complete")
        print("  (no args)      - Show all tasks")
        print("\nExample:")
        print("  python simple_todo.py todo 'Buy milk'")
        print("  python simple_todo.py done 1")
        print()
        show_todos(todos)
        return
    
    command = sys.argv[1].lower()
    
    if command == "todo" and len(sys.argv) > 2:
        # Add a new todo
        task = " ".join(sys.argv[2:])
        add_todo(todos, task)
    elif command == "done" and len(sys.argv) > 2:
        # Mark as complete
        complete_todo(todos, sys.argv[2])
    elif command == "todo" or command == "done":
        print(f"Usage: {sys.argv[0]} {command} <argument>")
    else:
        print(f"Unknown command: {command}")
        print("Use 'python simple_todo.py' for help")

if __name__ == "__main__":
    main()
