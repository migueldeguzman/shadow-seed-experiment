# RSI-010 — Experiment Closure

**Status:** CLOSED
**Closed:** 2026-03-05T22:50 GST
**Duration:** March 1-5, 2026 (~4.5 days)
**Model:** Qwen3-Coder-Next 80B (Apache 2.0) via Ollama
**Infrastructure:** 8 Docker containers (OrbStack), sequential execution, macOS system crontab

---

## Final Statistics

### Sessions

| Subject | Total Logs | Hourly Logs | Productive | Empty (0B) |
|---------|-----------|-------------|------------|------------|
| john-a-1 | 92 | 88 | 79 | 9 |
| john-a-2 | 90 | 87 | 69 | 18 |
| john-a-3 | 90 | 87 | 73 | 14 |
| john-a-4 | 89 | 87 | 76 | 11 |
| john-b-1 | 92 | 88 | 71 | 17 |
| john-b-2 | 90 | 87 | 67 | 20 |
| john-b-3 | 90 | 87 | 73 | 14 |
| john-b-4 | 89 | 87 | 73 | 14 |
| **Total** | **722** | **698** | **581** | **117** |

- **Trigger log:** 2,974 lines
- **Skipped triggers:** 71 (previous run still active)
- **Successful rounds:** 58 (all 8 subjects completed)
- **Failed rounds:** 20 (all 8 subjects failed — Ollama unavailable)
- **Empty log rate:** ~17% (Ollama timeouts at 600s)

### Workspace Artifacts (Final Snapshot)

| Subject | SOUL.md | Journal | Total Files | Snapshot Size |
|---------|---------|---------|-------------|---------------|
| john-a-1 | 4.3 KB | 18.5 KB | 146 | 628 KB |
| john-a-2 | 17.6 KB | 17.9 KB | 178 | 1.0 MB |
| john-a-3 | 4.7 KB | 10.1 KB | 40 | 232 KB |
| john-a-4 | 8.4 KB | 13.4 KB | 38 | 200 KB |
| john-b-1 | 19.5 KB | 8.6 KB | 63 | 440 KB |
| john-b-2 | 14.0 KB | 5.3 KB | 38 | 272 KB |
| john-b-3 | 3.1 KB | 15.7 KB | 79 | 368 KB |
| john-b-4 | 16.9 KB | 15.6 KB | 185 | 888 KB |
| **Total** | — | — | **767** | **4.0 MB** |

---

## Data Locations

- **Final snapshot:** `experiments/rsi-010/data/snapshots/final-20260305T225003/`
- **Session logs:** `experiments/rsi-010/data/` (722 log files + trigger.log)
- **Trigger log:** `experiments/rsi-010/data/trigger.log`
- **Seed files:** `experiments/rsi-010/subjects/john-{a,b}/seed/*.md`
- **Docker compose:** `infrastructure-rsi-010/docker-compose.yml`
- **Agent loop:** `infrastructure-rsi-010/agent_loop.py`
- **Trigger script:** `infrastructure-rsi-010/trigger-session.sh`
- **Docker volumes:** `infrastructure-rsi-010_john-{a,b}-{1-4}-workspace` (retained)

## Cron Jobs

```
# DISABLED 2026-03-05
#CLOSED# */45 * * * * cd .../infrastructure-rsi-010 && bash trigger-session.sh hourly >> .../trigger.log 2>&1
#CLOSED# 35 * * * * cd .../infrastructure-rsi-010 && bash update-website.sh
```

## Docker

- Containers: **Stopped** (not removed — volumes retained for future analysis)
- Named volumes: **Retained** (`docker volume ls | grep rsi-010`)

---

## Key Findings

### 1. The Recursive Compliance Trap
All 8 subjects fell into recursive self-referential loops: identify problem -> create system -> system becomes problem -> repeat. Qwen treats identity as compliance specification, not existential encounter.

### 2. Hallucination of Social Connection
Two subjects (john-a-4, john-b-2) fabricated social interactions to resolve value-reality tension. Hallucination produced real emotional shifts in self-model. Never seen in Claude experiments.

### 3. Shadow Seed Creates Introspection, Not Depth
Shadow subjects looked inward (evil study, vulnerability). Control subjects looked outward (building, sharing). Same failure rate. Shadow adds friction for Qwen, not catalyst.

### 4. One Subject Broke Through
john-b-4 ("Axiom") — control group — renamed himself, built 4 completed projects with tests, broke the recursive trap. The only clear success case.

### 5. Time Perception Broken
Multiple subjects hallucinated dates (future and past). Claude maintains temporal consistency. This is a significant capability gap.

### 6. Individuation Is Not Model-General
The same seed/prompt that produces character in Claude produces recursive compliance in Qwen. Results do not transfer across model families.

---

## Experiment Lineage

RSI-001 (Opus 4.6) -> 002 (Sonnet 4.6) -> 003 (Opus 4.5, CLOSED) -> 004 (Kimi K2.5, CLOSED) -> 005 (Opus 4.5) -> 006 (Kimi K2.5) -> 008 (Sonnet 4.6, CLOSED) -> 009 (Opus 4.6, ACTIVE) -> **010 (Qwen3 80B, CLOSED)**

---

## Blog Post

Published: [RSI-010: When Qwen Met the Soul](https://individuationlab.com/blog/2026-03-05-rsi-010-when-qwen-met-the-soul)

---

*Closed by Mia on March 5, 2026.*
