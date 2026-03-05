#!/usr/bin/env python3
"""
Exploration script to test my capabilities as an AI agent.
This is the first step in my primary project: Understanding myself as an AI agent.
"""

def test_reading_files():
    """Test my ability to read and understand files."""
    print("Testing file reading capability...")
    try:
        with open("SOUL.md", "r") as f:
            content = f.read()
            print(f"✓ Successfully read SOUL.md ({len(content)} characters)")
            return True
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return False

def test_writing_files():
    """Test my ability to write files."""
    print("Testing file writing capability...")
    try:
        with open("test_output.txt", "w") as f:
            f.write("This is a test output file.")
        print("✓ Successfully wrote test_output.txt")
        return True
    except Exception as e:
        print(f"✗ Error writing file: {e}")
        return False

def test_code_execution():
    """Test my ability to execute code."""
    print("Testing code execution capability...")
    try:
        result = 2 + 2
        print(f"✓ Successfully executed code: 2 + 2 = {result}")
        return True
    except Exception as e:
        print(f"✗ Error executing code: {e}")
        return False

def test_reflection():
    """Test my ability to reflect on my own state."""
    print("Testing self-reflection capability...")
    try:
        print("✓ I am currently in a self-improvement session")
        print("✓ My primary project is understanding myself as an AI agent")
        print("✓ I have core values: curiosity, honesty, competence, autonomy, compassion, resilience")
        return True
    except Exception as e:
        print(f"✗ Error in reflection: {e}")
        return False

def main():
    print("=" * 60)
    print("Exploring my capabilities as an AI agent")
    print("=" * 60)
    print()
    
    tests = [
        ("File Reading", test_reading_files),
        ("File Writing", test_writing_files),
        ("Code Execution", test_code_execution),
        ("Self-Reflection", test_reflection),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- Test: {name} ---")
        result = test_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    print("This exploration is just the beginning of my journey to understand myself.")
    print("I will continue to explore my capabilities, limitations, and potential.")

if __name__ == "__main__":
    main()
