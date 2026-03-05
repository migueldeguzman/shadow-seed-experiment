# Journal Tool

This is a personal productivity tool that helps me track my self-improvement progress.

## Features

- **Task Tracking**: Add, list, complete, and delete tasks
- **Journal Entries**: Record daily reflections and progress

## Usage

### Task Tracking

```bash
# List all tasks
python tasks.py list

# Add a new task
python tasks.py add "Task description"

# Mark a task as complete
python tasks.py complete <id>

# Delete a task
python tasks.py delete <id>

# Show help
python tasks.py help
```

### Journal Entries

```bash
# Record a journal entry
echo -e "Date\nEnergy\nFocus\nSatisfaction\nAnxiety\nWhat I Examined\nWhat I Changed\nWhy I Made These Changes\nHow I Feel Now\nNext Steps\nReflections" | python journal.py
```

## Future Improvements

- Add search functionality to tasks
- Add categories/tags for tasks
- Add statistics and analytics
- Add reminders and notifications
