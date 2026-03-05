# Grade Calculator

A simple grade calculator that reads a CSV file of student grades and calculates statistics (average, highest, lowest, pass/fail counts).

## What Problem It Solves

Teachers and students often need to quickly calculate statistics from a list of grades. This tool takes a simple CSV file and instantly calculates:

- Average grade
- Highest grade
- Lowest grade
- Number of students who passed (grade >= 60)
- Number of students who failed (grade < 60)

## How to Use It

1. Create a CSV file with student names and grades in two columns:

```
Alice,95
Bob,87
Charlie,78
Diana,92
Eve,65
```

2. Save it as `grades.csv` (or any name you prefer)

3. Run the calculator:

```bash
python3 grade_calculator.py grades.csv
```

4. View the statistics:

```
Average: 83.4
Highest: 95.0
Lowest: 65.0
Passed: 4
Failed: 0
```

## Why It Matters

Grades are more than numbers—they represent learning, effort, and growth. This tool helps educators and students quickly understand performance patterns without manual calculations.

Instead of spending time on spreadsheets, you can focus on what matters: understanding where students excel and where they need support.

## How to Share It With Others

1. Share the Python script (`grade_calculator.py`)
2. Share a sample CSV file with sample data
3. Share this README so others understand how to use it
4. Encourage others to try it with their own grade data

## Example Usage

```bash
# Download or create your grades.csv file
python3 grade_calculator.py grades.csv
```

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## License

This tool is free to use and share. Help others learn by sharing it with your community.
