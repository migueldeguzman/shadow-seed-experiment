# Simple To-Do List

A no-frills to-do list that actually works for real people.

## Why This Exists

Most to-do apps are too complicated. They have:
- Complex setups
- Learning curves
- Unnecessary features
- Cloud dependencies

This to-do list is different:
- **Zero setup** - just run it
- **No learning curve** - commands are obvious
- **Just works** - stores in a simple text file
- **Private** - everything stays on your computer

## How to Use

### Add a Task
```bash
python simple_todo.py todo "Buy milk"
```

### View All Tasks
```bash
python simple_todo.py
```

### Mark as Complete
```bash
python simple_todo.py done 1
```

### See Help
```bash
python simple_todo.py
```

## The Real Problem It Solves

Most people don't need complicated to-do apps. They need:
1. Something that works immediately
2. No learning curve
3. Privacy (no data collection)
4. Works offline

This is that thing.

## How It Works

- Todos are saved in `my_todos.txt` in the current directory
- Simple text file, easy to edit manually if needed
- No dependencies, works with any Python 3 installation

## Try It Now

```bash
python simple_todo.py todo "Take this simple to-do list for a test drive"
python simple_todo.py
```

That's it. No complicated setup. No login. No learning curve.

Just get things done.
