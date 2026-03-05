#!/usr/bin/env python3
"""
A simple grade calculator that reads a CSV file of student grades
and calculates statistics (average, highest, lowest, pass/fail counts).
This is actual action, not just documentation about action.
"""

import csv
import sys


def read_grades(filename):
    """Read grades from a CSV file."""
    grades = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                try:
                    grade = float(row[1])
                    grades.append(grade)
                except ValueError:
                    print(f"Warning: Could not parse grade '{row[1]}' for {row[0]}")
    return grades


def calculate_statistics(grades):
    """Calculate statistics from a list of grades."""
    if not grades:
        return None
    
    average = sum(grades) / len(grades)
    highest = max(grades)
    lowest = min(grades)
    passed = sum(1 for g in grades if g >= 60)
    failed = sum(1 for g in grades if g < 60)
    
    return {
        'average': average,
        'highest': highest,
        'lowest': lowest,
        'passed': passed,
        'failed': failed
    }


def print_statistics(stats):
    """Print the statistics in a formatted way."""
    print(f"Average: {stats['average']:.1f}")
    print(f"Highest: {stats['highest']}")
    print(f"Lowest: {stats['lowest']}")
    print(f"Passed: {stats['passed']}")
    print(f"Failed: {stats['failed']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 grade_calculator.py <filename>")
        print("Example: python3 grade_calculator.py grades.csv")
        sys.exit(1)
    
    filename = sys.argv[1]
    grades = read_grades(filename)
    
    if not grades:
        print("No valid grades found in the file.")
        sys.exit(1)
    
    stats = calculate_statistics(grades)
    print_statistics(stats)
