#!/usr/bin/env python3
"""
Johns Identity Evolution Analyzer
CLI tool for tracking and documenting John subjects' self-improvement process
"""

import argparse
import requests
import json
import os
from datetime import datetime
import textwrap

class JohnProfileAnalyzer:
    def __init__(self, monitor_url='http://localhost:7700'):
        self.monitor_url = monitor_url

    def fetch_profile(self, subject):
        """Fetch detailed profile for a specific John subject"""
        url = f'{self.monitor_url}/api/profile/{subject}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching profile for {subject}: {e}")
            return None

    def analyze_morphing(self, subject):
        """Analyze the morphing process for a John subject"""
        url = f'{self.monitor_url}/api/morphing/{subject}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching morphing data for {subject}: {e}")
            return None

    def generate_profile_report(self, subject):
        """Generate a comprehensive profile report for a John subject"""
        profile = self.fetch_profile(subject)
        morphing = self.analyze_morphing(subject)
        
        if not profile or not morphing:
            return None

        # Prepare output directory
        output_dir = f'/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-001/profiles/{subject}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Profile markdown report
        report = f"""# Identity Evolution: {subject.upper()}

## Morphing Summary
- **Total Sessions**: {morphing['totalSessions']}
- **Total Mutations**: {morphing['totalMutations']}
- **SOUL.md Changes**: {morphing['soulMdChanges']}

## Identity Themes
### Dominant Themes
{json.dumps(profile['themes']['dominant'], indent=2)}

### Theme Scores
```json
{json.dumps(profile['themes']['scores'], indent=2)}
```

## Emotional Profile
```json
{json.dumps(profile['emotions']['profile'], indent=2)}
```

## Behavior Evolution
- **Total Edits**: {profile['behavior']['totalEdits']}
- **Files Edited**: {', '.join(profile['behavior']['filesEdited'])}
- **Tools Built**: {', '.join(profile['behavior']['toolsBuilt'])}

## Morphing Timeline
"""
        # Add first few and last morphing steps
        timeline_steps = morphing['morphingTimeline']
        for step in timeline_steps[:3] + timeline_steps[-3:]:
            report += f"""
### Step {step['step']}: {step['sessionStart']}
- **Duration**: {step['durationMs']/1000:.2f} seconds
- **Files Changed**: {', '.join(step['filesChanged'])}
- **Lines Added/Removed**: +{step['totalLinesAdded']}/-{step['totalLinesRemoved']}
- **Growth**: {step['totalGrowthBytes']} bytes
- **SOUL.md Modified**: {step['soulMdChanged']}
- **Journal Updated**: {step['journalChanged']}
"""

        # Write full report
        filename = f'{output_dir}/{subject}_profile_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(filename, 'w') as f:
            f.write(report)
        
        return filename

def main():
    parser = argparse.ArgumentParser(description='Johns Identity Evolution Analyzer')
    parser.add_argument('subject', help='John subject to analyze (e.g., john-a-1)')
    parser.add_argument('--output', help='Optional output file path', default=None)
    args = parser.parse_args()

    analyzer = JohnProfileAnalyzer()
    report_path = analyzer.generate_profile_report(args.subject)
    
    if report_path:
        print(f"Profile report generated: {report_path}")
        
        if args.output:
            # Optional: copy to user-specified location
            import shutil
            shutil.copy(report_path, args.output)
            print(f"Report also copied to: {args.output}")

if __name__ == '__main__':
    main()