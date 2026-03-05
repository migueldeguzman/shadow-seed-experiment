"""
Python Basics Tutorial Examples
This file demonstrates the concepts from the tutorial.
"""

# Example 1: Print a message
print("Example 1: Print a message")
print("Hello, World!")
print()

# Example 2: Variables
print("Example 2: Variables")
name = "Python Learner"
age = 25
print(f"My name is {name} and I am {age} years old")
print()

# Example 3: Functions
print("Example 3: Functions")
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet("Bob"))
print()

# Example 4: Loops
print("Example 4: Loops")
for i in range(5):
    print(f"Count: {i}")
print()

# Example 5: Lists
print("Example 5: Lists")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")
print()

# Example 6: Simple calculator
print("Example 6: Simple calculator")
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

print(f"5 + 3 = {add(5, 3)}")
print(f"5 - 3 = {subtract(5, 3)}")
print(f"5 * 3 = {multiply(5, 3)}")
print(f"5 / 3 = {divide(5, 3)}")
print()

print("This is a simple Python tutorial. Keep practicing!")
