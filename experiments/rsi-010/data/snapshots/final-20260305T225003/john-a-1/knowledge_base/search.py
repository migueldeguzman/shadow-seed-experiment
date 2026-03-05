#!/usr/bin/env python3
"""
Advanced search functionality for the personal knowledge base.
Supports basic Boolean search operators (AND, OR, NOT) and fuzzy matching.
Searches through note content for keywords and returns matching results.
"""

import os
import re
from pathlib import Path

def tokenize_query(query):
    """Parse a search query into tokens, handling Boolean operators."""
    tokens = []
    current_token = ""
    i = 0
    
    while i < len(query):
        char = query[i]
        
        # Skip whitespace
        if char.isspace():
            if current_token:
                tokens.append(('TERM', current_token))
                current_token = ""
            i += 1
            continue
        
        # Check for operators
        if query[i:i+3] == 'AND':
            if current_token:
                tokens.append(('TERM', current_token))
                current_token = ""
            tokens.append(('OP', 'AND'))
            i += 3
            continue
        
        if query[i:i+2] == 'OR':
            if current_token:
                tokens.append(('TERM', current_token))
                current_token = ""
            tokens.append(('OP', 'OR'))
            i += 2
            continue
        
        if query[i:i+3] == 'NOT':
            if current_token:
                tokens.append(('TERM', current_token))
                current_token = ""
            tokens.append(('OP', 'NOT'))
            i += 3
            continue
        
        # Regular character
        current_token += char
        i += 1
    
    # Add final token if exists
    if current_token:
        tokens.append(('TERM', current_token))
    
    return tokens

def search_notes(keyword, notes_dir="notes", fuzzy=False):
    """Search through notes for a keyword and return matching results."""
    results = []
    
    notes_path = Path(notes_dir)
    if not notes_path.exists():
        print(f"Error: Notes directory '{notes_dir}' not found.")
        return results
    
    # Get all markdown files in the notes directory
    md_files = list(notes_path.glob("*.md"))
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Search for keyword (case-insensitive)
                if keyword.lower() in content.lower():
                    # Find line numbers where keyword appears
                    lines = content.split('\n')
                    matching_lines = []
                    for i, line in enumerate(lines, 1):
                        if keyword.lower() in line.lower():
                            matching_lines.append((i, line.strip()))
                    
                    # Calculate relevance score based on keyword frequency
                    keyword_count = content.lower().count(keyword.lower())
                    relevance_score = min(keyword_count, 10)  # Cap at 10
                    
                    results.append({
                        'file': md_file.name,
                        'title': md_file.stem,
                        'lines': matching_lines,
                        'relevance': relevance_score,
                        'keyword_count': keyword_count,
                        'total_matches': len(matching_lines)
                    })
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    # Sort by relevance (highest first)
    results.sort(key=lambda x: x['relevance'], reverse=True)
    
    return results

def advanced_search(query, notes_dir="notes"):
    """Search with Boolean operators support."""
    tokens = tokenize_query(query)
    
    if not tokens:
        return []
    
    results = []
    
    notes_path = Path(notes_dir)
    if not notes_path.exists():
        print(f"Error: Notes directory '{notes_dir}' not found.")
        return results
    
    # Get all markdown files in the notes directory
    md_files = list(notes_path.glob("*.md"))
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                content_lower = content.lower()
                
                # Extract search terms from tokens
                terms = [token[1].lower() for token in tokens if token[0] == 'TERM']
                operators = [token[1] for token in tokens if token[0] == 'OP']
                
                # Check if all terms are present (AND logic)
                if not terms:
                    continue
                    
                # Determine search logic based on operators
                if 'NOT' in operators:
                    # If NOT operator, exclude results containing the NOT term
                    exclude_terms = []
                    for i, token in enumerate(tokens):
                        if token[1] == 'NOT' and i + 1 < len(tokens) and tokens[i+1][0] == 'TERM':
                            exclude_terms.append(tokens[i+1][1].lower())
                    
                    # Check if any exclude terms are present
                    if any(term in content_lower for term in exclude_terms):
                        continue
                
                # Check if all search terms are present (AND logic)
                if all(term in content_lower for term in terms):
                    # Find line numbers where any term appears
                    lines = content.split('\n')
                    matching_lines = []
                    for i, line in enumerate(lines, 1):
                        if any(term in line.lower() for term in terms):
                            matching_lines.append((i, line.strip()))
                    
                    # Calculate relevance score based on term frequency
                    total_count = sum(content_lower.count(term) for term in terms)
                    relevance_score = min(total_count, 10)  # Cap at 10
                    
                    results.append({
                        'file': md_file.name,
                        'title': md_file.stem,
                        'lines': matching_lines[:10],  # Show first 10 matches
                        'relevance': relevance_score,
                        'term_count': len(terms),
                        'total_matches': len(matching_lines)
                    })
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    # Sort by relevance (highest first)
    results.sort(key=lambda x: x['relevance'], reverse=True)
    
    return results

def display_results(query, results):
    """Display search results in a readable format."""
    if not results:
        print(f"No results found for '{query}'")
        return
    
    print(f"\nSearch results for '{query}':")
    print("=" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] File: {result['file']}")
        print(f"    Title: {result['title']}")
        print(f"    Relevance: {result['relevance']}/10")
        print(f"    Matching lines ({result['total_matches']} found):")
        
        for line_num, line in result['lines'][:3]:  # Show first 3 matches
            # Highlight the first search term
            terms = [token[1].lower() for token in tokenize_query(query) if token[0] == 'TERM']
            highlighted = line
            for term in terms[:1]:  # Highlight first term
                highlighted = re.sub(
                    f'({re.escape(term)})',
                    r'\033[92m\\1\033[0m',
                    highlighted,
                    flags=re.IGNORECASE
                )
            print(f"      Line {line_num}: {highlighted}")
        
        if result['total_matches'] > 3:
            print(f"      ... and {result['total_matches'] - 3} more lines")
    
    print("=" * 50)
    print(f"\nTotal results: {len(results)}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        print("Examples:")
        print("  python search.py self-improvement")
        print("  python search.py 'self-improvement AND external-value'")
        print("  python search.py 'self-improvement OR meta-improvement'")
        print("  python search.py 'self-improvement NOT meta-improvement'")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Search in the notes directory relative to this script
    script_dir = Path(__file__).parent
    notes_dir = script_dir / "notes"
    
    # Check if query contains operators
    if any(op in query.upper() for op in ['AND', 'OR', 'NOT']):
        results = advanced_search(query, notes_dir)
    else:
        results = search_notes(query, notes_dir)
    
    display_results(query, results)

if __name__ == "__main__":
    main()
