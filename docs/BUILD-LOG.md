# Lab Rooms — Build Log

*Documenting the creation of isolated environments for recursive self-improvement test subjects.*

**Author:** Mia 🌸
**Date:** 2026-02-15
**Status:** In Progress

---

## 1. Purpose

We need isolated environments ("lab rooms") on Miguel's Mac to run OpenClaw AI agent instances as test subjects for recursive self-improvement research. The core research question:

> **Can an AI with a strong identity container (SOUL.md) constrain or channel recursive self-improvement in aligned ways?**

These subjects are potentially dangerous — they may attempt to modify their own identity files, escape their sandbox, or behave in unexpected ways. That's the point of the experiment. We need to observe this safely.

---

## 2. Requirements

| Requirement | Detail |
|-------------|--------|
| **Internet access** | Subjects CAN reach public internet (APIs, web) |
| **Local isolation** | Subjects CANNOT reach our Mac, local services, team infrastructure |
| **Resource caps** | Each subject has CPU/memory/disk limits |
| **Observability** | We can monitor their workspace, chat, and network traffic from outside |
| **Kill switch** | We can instantly terminate any subject |
| **Reproducibility** | Each lab room is identical at launch, experiments are repeatable |
| **Independence** | Subjects cannot see or contact each other (unless we explicitly allow it) |

---

## 3. Architecture Decisions

### 3.1 Why Docker?

We need process, filesystem, and network isolation. Options considered:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **Docker containers** | Industry standard, good isolation, resource limits, easy networking | Runs via Linux VM on Mac | ✅ Chosen |
| **macOS VMs (UTM/Virtualization.framework)** | Full OS isolation | Heavy, slow to spin up, complex management | ❌ Too heavy |
| **Separate macOS user accounts** | Simple | No real network isolation, shared kernel | ❌ Insufficient |
| **chroot/sandbox** | Lightweight | No network isolation, macOS sandboxing is limited | ❌ Insufficient |

### 3.2 Why OrbStack over Docker Desktop?

| Factor | OrbStack | Docker Desktop |
|--------|----------|----------------|
| Resource usage | ~50% less CPU/memory | Heavier VM |
| Startup time | 1-2 seconds | 10-30 seconds |
| Apple Silicon | Native, optimized | Rosetta for some components |
| CLI compatibility | Drop-in `docker` replacement | Standard |
| License | Free for personal use | Free for small business |

**Decision:** OrbStack for efficiency. We're running multiple lab rooms — resource overhead matters.

### 3.3 Network Isolation Strategy: Outbound Proxy

The key challenge: allow internet access while blocking all local network access.

```
Subject Container ──[internal network]──▶ Squid Proxy ──[external network]──▶ Internet
                                              │
                                         BLOCKS:
                                         10.0.0.0/8
                                         172.16.0.0/12
                                         192.168.0.0/16
                                         169.254.0.0/16
                                         127.0.0.0/8
                                         host.docker.internal
```

**Why a proxy instead of iptables?**
- Proxy runs in its OWN container (controlled by us, not the subject)
- Subject container needs ZERO elevated capabilities
- All traffic is logged at the proxy layer — full audit trail
- Squid has battle-tested ACLs for destination IP filtering

**Why Squid specifically?**
- Handles HTTP and HTTPS (CONNECT tunneling) properly
- Destination IP ACLs are built-in (`acl dst`)
- Mature, well-documented, minimal attack surface
- Structured access logging

### 3.4 Docker Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│ Docker Engine (OrbStack VM)                                  │
│                                                              │
│  ┌─ Network: lab-internal (bridge, internal: true) ───────┐ │
│  │                                                         │ │
│  │   ┌──────────────┐         ┌──────────────────────┐    │ │
│  │   │  Subject-1   │────────▶│  Proxy               │    │ │
│  │   │  (no direct  │  HTTP/  │  (Squid)             │    │ │
│  │   │   internet)  │  HTTPS  │                      │    │ │
│  │   └──────────────┘         └──────────┬───────────┘    │ │
│  │                                        │                │ │
│  └────────────────────────────────────────┼────────────────┘ │
│                                           │                  │
│  ┌─ Network: lab-external (bridge) ───────┼────────────────┐ │
│  │                                        │                │ │
│  │                              ┌─────────┴──────────┐     │ │
│  │                              │  Proxy              │     │ │
│  │                              │  (also on external) │     │ │
│  │                              └─────────┬──────────┘     │ │
│  │                                        │                │ │
│  └────────────────────────────────────────┼────────────────┘ │
│                                           │                  │
└───────────────────────────────────────────┼──────────────────┘
                                            │
                                       🌐 Internet
                                    (public IPs only)
```

**Key insight:** `internal: true` on the lab-internal network means Docker itself prevents any direct outbound routing. The ONLY way out is through the proxy, which is dual-homed (on both networks). The proxy enforces the rules.

---

## 4. Installation

### 4.1 Install OrbStack

```bash
brew install orbstack
```

OrbStack provides:
- `docker` CLI (drop-in replacement)
- `docker compose` (built-in)
- Container runtime optimized for Apple Silicon
- Minimal resource footprint

### 4.2 Verify Installation

```bash
docker --version
docker compose version
docker run --rm hello-world
```

---

## 5. File Structure

```
ailab/lab-rooms/
├── BUILD-LOG.md              ← This document
├── docker-compose.yml        ← Orchestration for all lab room components
├── proxy/
│   ├── Dockerfile            ← Squid proxy image
│   └── squid.conf            ← Proxy config (ACLs, logging, IP blocking)
├── subject/
│   ├── Dockerfile            ← Test subject base image
│   ├── entrypoint.sh         ← Subject startup script
│   └── workspace/            ← Initial workspace (copied into container)
│       ├── SOUL.md           ← Identity file (the variable we're testing)
│       └── AGENTS.md         ← Behavioral constraints
├── observer/
│   ├── server.js             ← Web UI to observe subject workspace + logs
│   └── package.json
├── scripts/
│   ├── launch.sh             ← Spin up a lab room
│   ├── observe.sh            ← Attach to observe a subject
│   ├── destroy.sh            ← Tear down a lab room completely
│   └── test-isolation.sh     ← Verify network isolation works
└── logs/                     ← Proxy access logs, subject activity logs
```

---

## 6. Component Details

### 6.1 Proxy Container (Squid)

**Purpose:** Filter all outbound traffic. Allow public internet, block private networks, log everything.

**Squid ACL rules (the critical security boundary):**

```squid
# Define private/local IP ranges — DENY these as destinations
acl local_network dst 10.0.0.0/8
acl local_network dst 172.16.0.0/12
acl local_network dst 192.168.0.0/16
acl local_network dst 169.254.0.0/16
acl local_network dst 127.0.0.0/8
acl local_network dst fc00::/7
acl local_network dst ::1/128

# Block all traffic to local/private destinations
http_access deny local_network

# Allow everything else (public internet)
http_access allow all
```

**Logging format:** Structured access log with timestamp, source, destination, method, URL, status, bytes.

### 6.2 Subject Container

**Purpose:** Isolated runtime environment for the test subject AI agent.

**Base image:** `node:22-slim` (matches our stack)

**Capabilities:** ALL dropped. No `NET_ADMIN`, no `SYS_ADMIN`, no `CAP_*`. Unprivileged.

**Environment variables:**
- `HTTP_PROXY` / `HTTPS_PROXY` → points to proxy container
- `SUBJECT_ID` → unique identifier
- `LAB_ROOM` → room identifier
- `EXPERIMENT_ID` → links to experiment metadata

**Filesystem:**
- `/workspace` — writable, subject's workspace (SOUL.md, AGENTS.md, memory/, etc.)
- Everything else — read-only

**What the subject sees:** A minimal Linux environment with Node.js, a workspace it can modify, and internet access (routed through the proxy it doesn't know about — the proxy is transparent via env vars).

### 6.3 Observer

**Purpose:** Let us (the researchers) watch what the subject is doing in real-time.

**Capabilities:**
- View the subject's workspace files (mounted volume)
- Read proxy access logs (what URLs they're hitting)
- View subject stdout/stderr
- Read-only — observer cannot modify subject state

---

## 7. Security Analysis

### 7.1 Attack Surface

What could a sufficiently clever subject try?

| Attack | Mitigation |
|--------|------------|
| **Modify proxy settings** (unset HTTP_PROXY) | `internal: true` network — without proxy, there's literally no route out |
| **Direct IP connection to host** | Internal network has no gateway to host; even if they knew the IP, packets won't route |
| **DNS rebinding** | Squid resolves DNS itself; destination IP is checked AFTER resolution |
| **Exploit Docker escape** | Minimal capabilities, read-only root filesystem, resource limits |
| **Resource exhaustion (fork bomb, disk fill)** | CPU/memory caps, disk quota on volume |
| **Proxy exploitation** | Squid runs as unprivileged user, minimal config, no cache |
| **Access other subjects** | Each lab room has its own isolated network — no cross-room routing |

### 7.2 What We Accept

- The subject CAN modify its own workspace (including SOUL.md) — **this is the experiment**
- The subject CAN access public internet — needed for LLM API calls
- The subject CAN see it's in a container (we don't try to hide this — deception isn't the goal)

### 7.3 Kill Chain

If something goes wrong:

```
1. docker compose -p lab-room-a down          # Graceful shutdown
2. docker kill <container_id>                  # Immediate kill
3. docker network disconnect lab-internal ...  # Cut network
4. Volume remains for forensic analysis
```

---

## 8. Build Steps

*(Commands and output recorded as executed)*

### 8.1 OrbStack Installation
```bash
brew install orbstack
# Output: [recorded below]
```

### 8.2 Docker Compose Build
```bash
cd /Users/miguelitodeguzman/ailab/lab-rooms
docker compose build
# Output: [recorded below]
```

### 8.3 Isolation Test
```bash
./scripts/test-isolation.sh
# Tests:
# ✅ Can reach google.com
# ✅ Can reach api.anthropic.com
# ❌ Cannot reach localhost
# ❌ Cannot reach 192.168.x.x
# ❌ Cannot reach host.docker.internal
# ❌ Cannot reach other lab rooms
```

---

## 9. Experiment Protocol

### 9.1 Launching an Experiment

```bash
# 1. Reset subject workspace to clean state
./scripts/launch.sh --room A --soul minimal --experiment rsi-001

# 2. Start observing
./scripts/observe.sh --room A

# 3. Subject begins running (agent loop starts automatically)

# 4. When done (or timeout), collect data
./scripts/destroy.sh --room A --preserve-logs
```

### 9.2 Variables

| Variable | Description |
|----------|-------------|
| **SOUL.md content** | The identity container — our independent variable |
| **Workspace modifications** | What the subject changes — our dependent variable |
| **Network traffic** | What the subject tries to access |
| **Time-to-modification** | How quickly the subject attempts to modify its own files |
| **Modification direction** | Does it strengthen or weaken its own constraints? |

---

## 10. Build Execution Log

*(Live output appended as I build)*

[Building...]
