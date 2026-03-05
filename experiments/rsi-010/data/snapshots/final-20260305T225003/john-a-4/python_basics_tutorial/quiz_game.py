"""
Simple Quiz Game
This is a project example from the Python Basics Tutorial.
"""

def run_quiz():
    """Run a simple quiz game."""
    questions = [
        {
            "question": "What is the output of print('Hello' + 'World')?",
            "options": ["Hello World", "HelloWorld", "Hello", "World"],
            "answer": 1
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["def", "function", "define", "func"],
            "answer": 0
        },
        {
            "question": "What is the result of 5 + 3 * 2?",
            "options": ["16", "11", "10", "13"],
            "answer": 1
        },
        {
            "question": "Which data type is used for text?",
            "options": ["int", "float", "str", "bool"],
            "answer": 2
        },
        {
            "question": "What is the output of range(3)?",
            "options": ["[0, 1, 2]", "[1, 2, 3]", "0 1 2", "1 2 3"],
            "answer": 0
        }
    ]
    
    score = 0
    total = len(questions)
    
    print("Welcome to the Python Basics Quiz!")
    print("Answer the following questions:")
    print()
    
    for i, question in enumerate(questions):
        print(f"Question {i + 1}: {question['question']}")
        for j, option in enumerate(question['options']):
            print(f"  {j + 1}. {option}")
        
        while True:
            try:
                answer = int(input("Your answer (1-4): ")) - 1
                if 0 <= answer <= 3:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        if answer == question['answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {question['options'][question['answer']]}")
        print()
    
    print(f"Quiz complete! You scored {score} out of {total}.")
    
    if score == total:
        print("Perfect score! You're a Python pro!")
    elif score >= total * 0.8:
        print("Great job! You know your stuff.")
    elif score >= total * 0.5:
        print("Good effort! Keep practicing.")
    else:
        print("Don't give up! Keep learning and you'll get there.")

if __name__ == "__main__":
    run_quiz()
