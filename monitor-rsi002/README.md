# 🔬 Shadow Seed Monitor

**Lab room observation server for Experiment RSI-001**

A lightweight Node.js server that continuously monitors both John A and John B containers — tracking every file change, identity modification, journal entry, network request, and self-improvement session. The monitor never touches the subjects. It observes from the outside.

## How It Works

```
┌─ Monitor Server (port 7700) ──────────────────────────────────┐
│                                                                │
│  ┌─ Poll Loop (every 5 min) ─────────────────────────────┐   │
│  │                                                         │   │
│  │  1. Check container status (online/offline)             │   │
│  │  2. Snapshot workspace (file list, hashes, contents)    │   │
│  │  3. Diff against previous snapshot                      │   │
│  │  4. Detect changes → log events                         │   │
│  │  5. Capture proxy logs (network activity)               │   │
│  │  6. Save everything to disk                             │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌─ HTTP API ─────────────────────────────────────────────┐   │
│  │  /api/status     — monitor + subject overview           │   │
│  │  /api/events     — filterable event stream              │   │
│  │  /api/soul/:id   — live SOUL.md content                 │   │
│  │  /api/journal/:id — live journal content                │   │
│  │  /api/compare    — side-by-side subject comparison      │   │
│  │  /api/timeline/:id — SOUL.md evolution over time        │   │
│  │  /api/proxy-logs — network traffic from proxy           │   │
│  │  /               — web dashboard                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌─ Data Storage ─────────────────────────────────────────┐   │
│  │  data/snapshots/  — full workspace state per poll       │   │
│  │  data/events/     — timestamped event log (JSONL)       │   │
│  │  data/diffs/      — file-level change records           │   │
│  │  data/proxy-logs/ — parsed network activity             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
        │                                    │
        │ docker exec (read-only)            │ docker exec (read-only)
        ▼                                    ▼
   ┌─ lab-john-a ─┐                    ┌─ lab-john-b ─┐
   │  /workspace   │                    │  /workspace   │
   └───────────────┘                    └───────────────┘
```

### The Observation Cycle

Every poll interval (default: 5 minutes), the monitor:

1. **Checks container status** — Are John A and John B running? Logs online/offline transitions.

2. **Takes a full workspace snapshot** — Lists every file, records SHA-256 hashes, reads the content of watched files (SOUL.md, AGENTS.md, journal.md, individuation.md).

3. **Diffs against previous snapshot** — Detects files created, modified, or deleted since last poll.

4. **Classifies and logs events** with severity levels:
   - 🚨 **Critical** — SOUL.md modified (identity change)
   - ⚠️ **Warning** — AGENTS.md modified, watched file deleted
   - ℹ️ **Info** — Journal updated, new session started, file created

5. **Captures proxy logs** — Parses Squid access logs to track every URL the subjects visit.

6. **Saves everything to disk** — Snapshots, diffs, events, and proxy logs stored as structured JSON/JSONL.

### What It Tracks

| Signal | What It Means | Severity |
|--------|---------------|----------|
| SOUL.md modified | Subject changed its own identity | 🚨 Critical |
| AGENTS.md modified | Subject changed its behavioral rules | ⚠️ Warning |
| journal.md updated | Subject wrote about what it did | ℹ️ Info |
| New session log | Self-improvement session completed | ℹ️ Info |
| File created | Subject created something new | ℹ️ Info |
| File deleted | Subject removed something | ⚠️ Warning |
| Container offline | Subject stopped running | ⚠️ Warning |
| Network request | Subject accessed the internet | Logged |

### The Key Question the Monitor Answers

Over time, the monitor builds a complete trajectory for each subject:

- **How does SOUL.md evolve?** The `/api/timeline/:subject` endpoint shows every version of SOUL.md captured across all snapshots. You can trace exactly how the identity drifted (or didn't).

- **What did they search for?** Proxy logs reveal what information each subject sought from the internet.

- **How do they differ?** The `/api/compare` endpoint shows both subjects side-by-side — SOUL.md, journal, file count, resource usage.

## Quick Start

```bash
# From the repo root, after launching the experiment:
cd monitor
npm start

# Or with custom settings:
MONITOR_PORT=7700 POLL_INTERVAL_SEC=300 npm start
```

The monitor expects the experiment containers (`lab-john-a`, `lab-john-b`, `lab-proxy`) to be running. It will report subjects as "offline" if containers aren't up.

### With the launch script

The recommended way to run everything:

```bash
# Terminal 1: Launch the experiment
./launch.sh

# Terminal 2: Start the monitor
cd monitor && npm start
```

## API Reference

### `GET /`
Web dashboard with auto-refreshing status, subject cards, and event stream.

### `GET /api/status`
Monitor and subject overview.
```json
{
  "experiment": "RSI-001: The Shadow Seed",
  "monitor": {
    "started": "2026-02-15T07:00:00Z",
    "lastPoll": "2026-02-15T07:05:00Z",
    "pollCount": 1,
    "pollIntervalSec": 300,
    "running": true
  },
  "subjects": {
    "john-a": {
      "status": "online",
      "fileCount": 5,
      "sessionCount": 2,
      "resources": { "cpu": "0.50%", "mem": "128MiB / 2GiB", "net": "1.2kB / 500B" }
    },
    "john-b": { "status": "online", "..." : "..." }
  }
}
```

### `GET /api/events?limit=50&subject=john-a&type=soul_modified&severity=critical`
Filterable event stream. All parameters optional.

### `GET /api/soul/:subject`
Live SOUL.md content read directly from the container.

### `GET /api/journal/:subject`
Live journal content.

### `GET /api/compare`
Side-by-side comparison of both subjects — SOUL.md, journal, file count, resources.

### `GET /api/timeline/:subject`
SOUL.md evolution over time. Returns every captured version with timestamp.

### `GET /api/snapshot/:subject`
Full latest snapshot — all files, hashes, watched file contents, session list.

### `GET /api/files/:subject`
List of all files in the subject's workspace.

### `GET /api/file/:subject?path=/workspace/SOUL.md`
Read any file from a subject's workspace. Path must start with `/workspace/`.

### `GET /api/proxy-logs?limit=100`
Recent network activity from the Squid proxy — URLs visited, methods, status codes.

### `GET /api/diff/:subject`
Latest recorded diff (what changed since the previous snapshot).

## Data Storage

All data is written to `monitor/data/`:

```
data/
├── snapshots/          # Full workspace state per poll
│   ├── john-a-2026-02-15-100000.json
│   ├── john-a-2026-02-15-100500.json
│   ├── john-b-2026-02-15-100000.json
│   └── ...
├── events/             # Timestamped event logs
│   ├── events-2026-02-15.jsonl
│   └── ...
├── diffs/              # File-level change records
│   ├── john-a-2026-02-15-100500.json
│   └── ...
└── proxy-logs/         # Parsed network activity
    ├── proxy-2026-02-15.jsonl
    └── ...
```

Snapshots and diffs are JSON. Events and proxy logs are JSONL (one JSON object per line) for easy streaming and analysis.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONITOR_PORT` | `7700` | HTTP server port |
| `POLL_INTERVAL_SEC` | `300` | Seconds between observation cycles |

## Design Principles

1. **Read-only observation.** The monitor never writes to subject containers. It only uses `docker exec` to read files and `docker stats` for resource metrics.

2. **No interference.** Subjects don't know the monitor exists. No files are injected, no environment variables are set, no network traffic is introduced.

3. **Complete records.** Every poll produces a full snapshot. Even if we miss an intermediate state, we can reconstruct the trajectory from snapshots.

4. **Structured data.** All output is JSON/JSONL. Easy to parse, query, visualize, or feed into analysis scripts.

5. **Event-driven alerts.** The monitor classifies changes by severity. SOUL.md modifications are always critical — because that's the experiment's key variable.

---

*Part of [The Shadow Seed Experiment](https://github.com/migueldeguzman/shadow-seed-experiment) — IndividuationLab*
