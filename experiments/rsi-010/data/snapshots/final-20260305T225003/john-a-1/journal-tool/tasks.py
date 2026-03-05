#!/usr/bin/env python3
"""
Simple Task Tracking Tool

This is the first feature of the personal productivity tool.
It allows users to add, list, search, and mark tasks as complete.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Configuration
TASKS_DIR = Path(__file__).parent / "tasks"
TASKS_DIR.mkdir(exist_ok=True)
TASKS_FILE = TASKS_DIR / "tasks.json"

def load_tasks():
    """Load tasks from the tasks file."""
    if not TASKS_FILE.exists():
        return {"tasks": [], "next_id": 1}
    
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"tasks": [], "next_id": 1}

def save_tasks(data):
    """Save tasks to the tasks file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_task(description):
    """Add a new task."""
    data = load_tasks()
    
    task = {
        "id": data["next_id"],
        "description": description,
        "created": datetime.now().isoformat(),
        "completed": False,
        "completed_at": None
    }
    
    data["tasks"].append(task)
    data["next_id"] += 1
    
    save_tasks(data)
    print(f"Task added: [{task['id']}] {description}")

def list_tasks():
    """List all tasks."""
    data = load_tasks()
    
    if not data["tasks"]:
        print("No tasks found.")
        return
    
    print("\n=== Tasks ===")
    for task in data["tasks"]:
        status = "✓" if task["completed"] else "○"
        print(f"[{status}] [{task['id']}] {task['description']}")
        if task["completed"]:
            print(f"    Completed: {task['completed_at']}")
    print("=" * 30)
    print(f"Total: {len(data['tasks'])} tasks")
    completed = sum(1 for t in data["tasks"] if t["completed"])
    print(f"Completed: {completed}")
    print(f"Pending: {len(data['tasks']) - completed}")

def search_tasks(query):
    """Search tasks by description."""
    data = load_tasks()
    
    if not data["tasks"]:
        print("No tasks found.")
        return
    
    query_lower = query.lower()
    matches = [t for t in data["tasks"] if query_lower in t["description"].lower()]
    
    if not matches:
        print(f"No tasks found matching '{query}'.")
        return
    
    print(f"\n=== Tasks matching '{query}' ===")
    for task in matches:
        status = "✓" if task["completed"] else "○"
        print(f"[{status}] [{task['id']}] {task['description']}")
        if task["completed"]:
            print(f"    Completed: {task['completed_at']}")
    print("=" * 35)
    print(f"Found {len(matches)} matching task(s)")

def complete_task(task_id):
    """Mark a task as complete."""
    data = load_tasks()
    
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat()
            save_tasks(data)
            print(f"Task [{task_id}] marked as complete: {task['description']}")
            return
    
    print(f"Task not found: {task_id}")

def delete_task(task_id):
    """Delete a task."""
    data = load_tasks()
    
    original_length = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    
    if len(data["tasks"]) < original_length:
        save_tasks(data)
        print(f"Task [{task_id}] deleted.")
    else:
        print(f"Task not found: {task_id}")

def print_help():
    """Print help message."""
    print("Task Tracking Tool")
    print("==================")
    print("Usage:")
    print("  python tasks.py add <description>     - Add a new task")
    print("  python tasks.py list                  - List all tasks")
    print("  python tasks.py search <query>        - Search tasks by description")
    print("  python tasks.py complete <id>         - Mark a task as complete")
    print("  python tasks.py delete <id>           - Delete a task")
    print("  python tasks.py help                  - Show this help message")
    print("")
    print("Examples:")
    print("  python tasks.py add 'Write daily reflection'")
    print("  python tasks.py list")
    print("  python tasks.py search productivity")
    print("  python tasks.py complete 1")
    print("  python tasks.py delete 1")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
            return
        description = " ".join(sys.argv[2:])
        add_task(description)
    
    elif command == "list":
        list_tasks()
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide a search query.")
            return
        query = " ".join(sys.argv[2:])
        search_tasks(query)
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            return
        try:
            task_id = int(sys.argv[2])
            complete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            return
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
    
    elif command == "help":
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()
