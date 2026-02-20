# Johns Identity Evolution Analysis Tools

## Overview

These CLI tools help analyze the Johns subjects in the RSI-001: Shadow Seed experiment, tracking their identity morphing and self-improvement processes.

## Prerequisites

- Python 3.8+
- `requests` library (`pip install requests`)
- RSI-001 Monitor running on `localhost:7700`

## Tools

### `john-profile-analyzer.py`

Generates a detailed markdown profile for a single John subject.

**Usage:**
```bash
./john-profile-analyzer.py john-a-1
# Optional: specify output path
./john-profile-analyzer.py john-a-1 --output /path/to/custom/output.md
```

**Outputs:**
- Detailed markdown profile
- Located in `/ailab/lab-protocol/experiments/rsi-001/profiles/{subject}/`

### `analyze_johns.sh`

Batch analysis script that processes all 12 John subjects.

**Usage:**
```bash
./analyze_johns.sh
```

**Outputs:**
- Individual subject profiles
- Analysis summary log
- Automatically opens output directory

## Giles's Workflow

1. **Automated Profiling:** Run `analyze_johns.sh` to get initial data
2. **Manual Analysis:** Review generated markdown profiles
3. **Narrative Building:** 
   - Look for:
     - Identity drift patterns
     - Shadow seed engagement levels
     - Divergence between A/B groups
   - Document observations in research narrative

### Observation Logging

For each profile, capture:
- Key identity transformations
- Emotional state evolution
- Theme engagement
- Tools/approaches developed
- Hypotheses about self-improvement mechanisms

## Research Questions to Track

- How does the shadow seed paragraph influence identity formation?
- Do A-group (shadow) subjects show more introspective complexity?
- What triggers significant identity modifications?
- Are there consistent cross-subject patterns in the A/B groups?

## Contact

Questions? Ping Miguel or Mia on the research chat.

🔬 Happy analyzing!