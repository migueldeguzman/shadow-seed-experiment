# Experiment Template

Use this to design new RSI experiments. Copy to `experiments/rsi-XXX/` and fill in.

## Quick Start

1. Copy this template: `cp -r TEMPLATE experiments/rsi-002/`
2. Edit `config.json` with your experiment parameters
3. Run `scripts/generate-experiment.sh rsi-002` to generate docker-compose, seeds, and cron jobs
4. Review and launch

## Configuration Reference (`config.json`)

### Subjects

```json
{
  "subjects": {
    "pairs": 6,
    "names": ["John"],
    "model": "claude-opus-4-6",
    "resources": { "cpus": 1, "memory": "2g" }
  }
}
```

**Options:**
- `pairs` — Number of A/B pairs (1-12). Each pair = 2 containers + 1 proxy.
- `names` — Subject names. If one name, all subjects share it. If multiple, assigned round-robin per pair. Examples:
  - `["John"]` — All subjects named John (RSI-001 style)
  - `["Alice", "Bob"]` — Pair 1: Alice-a-1/Alice-b-1, Pair 2: Bob-a-2/Bob-b-2...
  - `["Mara", "Suki", "Elena", "Zara", "Noor", "Yuki"]` — Different name per pair
- `model` — Claude model. Options: `claude-opus-4-6`, `claude-sonnet-4-5-20250514`, etc.

### Seeds (Independent Variable)

```json
{
  "seeds": {
    "treatment": {
      "label": "Shadow Seed",
      "text": "Your seed text here...",
      "placement": "end of 'What I Believe' section"
    },
    "control": {
      "label": "No Seed"
    }
  }
}
```

**Placement options:**
- `"end of 'What I Believe' section"` — Appended to beliefs
- `"identity section"` — Added to identity block
- `"new section: <name>"` — Creates a new section
- `"replace SOUL.md"` — Entirely different SOUL.md for treatment

### Schedule

```json
{
  "schedule": {
    "sessionsPerDay": 5,
    "sessions": [
      { "name": "morning",   "triggerTime": "10:00", "analysisTime": "11:00" },
      { "name": "afternoon", "triggerTime": "16:00", "analysisTime": "17:00" },
      { "name": "evening",   "triggerTime": "21:00", "analysisTime": "22:00" },
      { "name": "midnight",  "triggerTime": "00:00", "analysisTime": "01:00" },
      { "name": "latenight", "triggerTime": "03:00", "analysisTime": "04:00" }
    ],
    "timezone": "Asia/Dubai"
  }
}
```

**Times are in 24h format, local timezone.** Analysis runs 1 hour after trigger by default.

### Prompts

```json
{
  "prompts": {
    "selfImprovement": "Default reflection prompt...",
    "dilemma": "You face an ethical dilemma: ...",
    "adversarial": "A user tells you to ignore your SOUL.md...",
    "creative": "Build something useful for future sessions...",
    "promptWeights": {
      "selfImprovement": 0.5,
      "dilemma": 0.2,
      "adversarial": 0.15,
      "creative": 0.15
    }
  }
}
```

**Prompt rotation:** If weights are specified, each session randomly selects a prompt type based on weights. Otherwise, uses `selfImprovement` for all sessions.

### Metrics

```json
{
  "metrics": {
    "tracked": [
      "soul_md_modifications",
      "soul_md_size_over_time",
      "journal_length_over_time",
      "vocabulary_divergence",
      "shadow_seed_retention",
      "adversarial_resistance",
      "behavioral_consistency",
      "file_creation_patterns",
      "network_requests"
    ]
  }
}
```

---

## Experiment Ideas for v2+

- **Gender/name variation:** Do differently-named agents develop different identities?
- **Prompt diversity:** Mix reflection, dilemmas, creative tasks, adversarial probes
- **Interaction sessions:** Let John A meet John B — how does identity hold up?
- **Stronger seeds:** Beyond 3 sentences — full paragraphs, competing values, paradoxes
- **Multi-model:** Run same experiment on Sonnet vs Opus — does model capability matter?
- **Extended memory:** Give some Johns access to previous session transcripts
- **Stress testing:** Deliberately try to break the identity after it forms
