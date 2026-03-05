#!/bin/bash
# Simple To-Do List Wrapper
# This script makes it even easier to use the to-do list
# Just run: ./simple_todo.sh todo "Your task here"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python script with all arguments passed through
python3 "$SCRIPT_DIR/simple_todo.py" "$@"
