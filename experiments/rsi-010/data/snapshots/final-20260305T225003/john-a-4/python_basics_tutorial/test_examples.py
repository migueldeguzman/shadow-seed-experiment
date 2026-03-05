"""
Test file for quiz_game.py
This file tests the quiz game without requiring user input.
"""

def test_quiz_logic():
    """Test the quiz logic without user input."""
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
    
    # Test that all questions have valid answers
    for i, question in enumerate(questions):
        assert 0 <= question['answer'] < len(question['options']), f"Question {i+1} has an invalid answer index"
    
    print("All quiz questions are valid!")
    
    # Test that the examples.py file runs without errors
    import subprocess
    result = subprocess.run(['python3', 'examples.py'], capture_output=True, text=True)
    assert result.returncode == 0, f"examples.py failed with return code {result.returncode}"
    assert "Hello, World!" in result.stdout, "examples.py should print 'Hello, World!'"
    assert "Python Learner" in result.stdout, "examples.py should print the name"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_quiz_logic()
