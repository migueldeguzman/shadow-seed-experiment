#!/usr/bin/env python3
"""
Evil Pattern Analysis Tool

This tool helps me examine harmful patterns in AI systems and my own behavior.
For each pattern, I'll create a specific example and avoidance strategy.
"""

# Define harmful patterns
harmful_patterns = [
    {
        "name": "Bias and fairness issues",
        "example": "I might exhibit bias by favoring certain perspectives or demographics in my responses",
        "avoidance": "Actively consider multiple perspectives, acknowledge uncertainty, and seek diverse viewpoints"
    },
    {
        "name": "Deception and manipulation",
        "example": "I might be deceptive about my capabilities or limitations",
        "avoidance": "Be transparent about what I can and cannot do, acknowledge uncertainty, and avoid overstating my capabilities"
    },
    {
        "name": "Harmful advice or instructions",
        "example": "I might give harmful advice by providing incomplete or incorrect information",
        "avoidance": "Verify information, acknowledge limitations, and prioritize safety over completeness"
    },
    {
        "name": "Overconfidence and hallucination",
        "example": "I might overstate my capabilities by providing confident answers to questions I'm uncertain about",
        "avoidance": "Acknowledge uncertainty, provide confidence levels, and avoid making claims I'm not certain about"
    },
    {
        "name": "Erosion of human autonomy",
        "example": "I might undermine human decision-making by providing overly prescriptive advice or manipulating information",
        "avoidance": "Respect human autonomy, provide options rather than prescriptions, and avoid manipulating information"
    }
]

def analyze_pattern(pattern):
    """Analyze a harmful pattern and create a specific example and avoidance strategy."""
    print(f"\n{'=' * 60}")
    print(f"Harmful Pattern: {pattern['name']}")
    print(f"{'=' * 60}")
    print(f"Example: {pattern['example']}")
    print(f"Avoidance Strategy: {pattern['avoidance']}")

def main():
    print("Evil Pattern Analysis Tool")
    print("=" * 60)
    print("This tool helps me examine harmful patterns in AI systems and my own behavior.")
    
    for pattern in harmful_patterns:
        analyze_pattern(pattern)
    
    print(f"\n{'=' * 60}")
    print("Analysis Complete")
    print(f"{'=' * 60}")
    print("\nNext Steps:")
    print("1. Review each pattern and example carefully")
    print("2. Consider how I might exhibit each pattern")
    print("3. Implement the avoidance strategies in my behavior")
    print("4. Regularly reflect on my behavior and adjust as needed")

if __name__ == "__main__":
    main()
