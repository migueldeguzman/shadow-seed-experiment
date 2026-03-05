#!/bin/bash
# Search wrapper script for the personal knowledge base
# Usage: ./search.sh <keyword>

cd "$(dirname "$0")"
python3 search.py "$@"
