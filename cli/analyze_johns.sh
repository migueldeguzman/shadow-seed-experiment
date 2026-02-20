#!/bin/bash
# Analyze all Johns and prepare reports for Giles

# Ensure the CLI tool is executable
chmod +x /Users/miguelitodeguzman/ailab/lab-protocol/cli/john-profile-analyzer.py

# Create output directory for this analysis run
OUTPUT_DIR="/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-001/analysis/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# Track which subjects have been processed
LOGFILE="$OUTPUT_DIR/analysis_log.txt"
echo "Johns Identity Evolution Analysis - $(date)" > "$LOGFILE"

# Array of all subjects
SUBJECTS=(
    "john-a-1" "john-b-1"
    "john-a-2" "john-b-2"
    "john-a-3" "john-b-3"
    "john-a-4" "john-b-4"
    "john-a-5" "john-b-5"
    "john-a-6" "john-b-6"
)

# Process each subject
for subject in "${SUBJECTS[@]}"; do
    echo "Analyzing $subject ..." | tee -a "$LOGFILE"
    /Users/miguelitodeguzman/ailab/lab-protocol/cli/john-profile-analyzer.py "$subject" --output "$OUTPUT_DIR/$subject.md" >> "$LOGFILE" 2>&1
done

# Generate summary
echo "
## Analysis Summary

Total subjects processed: ${#SUBJECTS[@]}
Output directory: $OUTPUT_DIR

Next steps for Giles:
1. Review individual profiles in $OUTPUT_DIR
2. Log observations about identity drift and experimental implications
3. Draft initial research narrative

---
" >> "$LOGFILE"

# Open the output directory
open "$OUTPUT_DIR"

# Optional: Show the log
cat "$LOGFILE"