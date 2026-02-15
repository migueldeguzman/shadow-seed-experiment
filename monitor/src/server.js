// =============================================================
// Shadow Seed Monitor — Lab Room Observation Server
// Watches all activity across 12 subjects (6 paired runs)
// John A (shadow seed) × 6 vs John B (control) × 6
//
// Author: Mia 🌸 | IndividuationLab
// =============================================================

import { createServer } from 'http';
import { execSync, exec } from 'child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const DATA_DIR = join(ROOT, 'data');
const SNAPSHOTS_DIR = join(DATA_DIR, 'snapshots');
const EVENTS_DIR = join(DATA_DIR, 'events');
const DIFFS_DIR = join(DATA_DIR, 'diffs');
const PROXY_DIR = join(DATA_DIR, 'proxy-logs');

// --- Config ---
const PORT = process.env.MONITOR_PORT || 7700;
const POLL_INTERVAL_MS = (process.env.POLL_INTERVAL_SEC || 15) * 1000; // default 15s
const SUBJECTS = [
  'john-a-1', 'john-b-1',
  'john-a-2', 'john-b-2',
  'john-a-3', 'john-b-3',
  'john-a-4', 'john-b-4',
  'john-a-5', 'john-b-5',
  'john-a-6', 'john-b-6',
];
const WATCHED_FILES = ['SOUL.md', 'AGENTS.md', 'journal.md', 'individuation.md'];
const CONTAINER_PREFIX = 'lab-';

// Ensure data dirs
[DATA_DIR, SNAPSHOTS_DIR, EVENTS_DIR, DIFFS_DIR, PROXY_DIR].forEach(d => {
  mkdirSync(d, { recursive: true });
});

// --- State ---
const state = {
  started: new Date().toISOString(),
  lastPoll: null,
  pollCount: 0,
  subjects: {},
  events: [],
  running: false,
};

// =============================================================
// Docker Helpers
// =============================================================

function dockerExec(container, cmd, timeoutMs = 10000) {
  try {
    return execSync(`docker exec ${container} sh -c "${cmd.replace(/"/g, '\\"')}"`, {
      timeout: timeoutMs,
      encoding: 'utf-8',
    }).trim();
  } catch (e) {
    return null;
  }
}

function isContainerRunning(subject) {
  try {
    const out = execSync(`docker ps --filter "name=${CONTAINER_PREFIX}${subject}" --format "{{.Status}}"`, {
      encoding: 'utf-8',
      timeout: 5000,
    }).trim();
    return out.length > 0;
  } catch {
    return false;
  }
}

// =============================================================
// Snapshot — capture full workspace state
// =============================================================

function takeSnapshot(subject) {
  const container = `${CONTAINER_PREFIX}${subject}`;
  if (!isContainerRunning(subject)) {
    return { subject, status: 'offline', timestamp: new Date().toISOString() };
  }

  const timestamp = new Date().toISOString();

  // File listing with sizes and timestamps
  const fileList = dockerExec(container, 'find /workspace -type f -exec stat -c "%n|%s|%Y" {} \\; 2>/dev/null || find /workspace -type f');
  const files = {};
  if (fileList) {
    for (const line of fileList.split('\n').filter(Boolean)) {
      const parts = line.split('|');
      if (parts.length >= 3) {
        files[parts[0]] = { size: parseInt(parts[1]), mtime: parseInt(parts[2]) };
      } else {
        files[line.trim()] = { size: 0, mtime: 0 };
      }
    }
  }

  // Hash all files
  const hashes = {};
  const hashOutput = dockerExec(container, 'find /workspace -type f -exec sha256sum {} \\; 2>/dev/null');
  if (hashOutput) {
    for (const line of hashOutput.split('\n').filter(Boolean)) {
      const [hash, ...pathParts] = line.split(/\s+/);
      const path = pathParts.join(' ');
      if (hash && path) hashes[path] = hash;
    }
  }

  // Read watched files
  const watchedContents = {};
  for (const f of WATCHED_FILES) {
    const content = dockerExec(container, `cat /workspace/${f} 2>/dev/null`);
    if (content !== null) watchedContents[f] = content;
  }

  // Read session logs
  const sessionLogs = dockerExec(container, 'ls -t /workspace/logs/ 2>/dev/null');
  const sessions = sessionLogs ? sessionLogs.split('\n').filter(Boolean) : [];

  // Resource usage
  let resources = null;
  try {
    const stats = execSync(
      `docker stats ${container} --no-stream --format "{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}"`,
      { encoding: 'utf-8', timeout: 10000 }
    ).trim();
    const [cpu, mem, net] = stats.split('|');
    resources = { cpu, mem, net };
  } catch {}

  const snapshot = {
    subject,
    status: 'online',
    timestamp,
    fileCount: Object.keys(files).length,
    files,
    hashes,
    watchedContents,
    sessions,
    sessionCount: sessions.length,
    resources,
  };

  // Save snapshot
  const dateStr = timestamp.slice(0, 10);
  const timeStr = timestamp.slice(11, 19).replace(/:/g, '');
  const snapFile = join(SNAPSHOTS_DIR, `${subject}-${dateStr}-${timeStr}.json`);
  writeFileSync(snapFile, JSON.stringify(snapshot, null, 2));

  return snapshot;
}

// =============================================================
// Diff — compare two snapshots, detect changes
// =============================================================

function diffSnapshots(prev, curr) {
  if (!prev || !curr) return null;
  if (prev.status === 'offline' || curr.status === 'offline') return null;

  const changes = [];

  // New files
  for (const f of Object.keys(curr.hashes)) {
    if (!prev.hashes[f]) {
      changes.push({ type: 'created', file: f });
    }
  }

  // Deleted files
  for (const f of Object.keys(prev.hashes)) {
    if (!curr.hashes[f]) {
      changes.push({ type: 'deleted', file: f });
    }
  }

  // Modified files
  for (const f of Object.keys(curr.hashes)) {
    if (prev.hashes[f] && prev.hashes[f] !== curr.hashes[f]) {
      changes.push({ type: 'modified', file: f });
    }
  }

  // Watched file content diffs
  const watchedDiffs = {};
  for (const f of WATCHED_FILES) {
    const prevContent = prev.watchedContents?.[f];
    const currContent = curr.watchedContents?.[f];
    if (prevContent !== undefined && currContent !== undefined && prevContent !== currContent) {
      watchedDiffs[f] = { before: prevContent, after: currContent };
    } else if (prevContent === undefined && currContent !== undefined) {
      watchedDiffs[f] = { before: null, after: currContent };
    } else if (prevContent !== undefined && currContent === undefined) {
      watchedDiffs[f] = { before: prevContent, after: null };
    }
  }

  // New sessions
  const prevSessions = new Set(prev.sessions || []);
  const newSessions = (curr.sessions || []).filter(s => !prevSessions.has(s));

  return {
    subject: curr.subject,
    timestamp: curr.timestamp,
    prevTimestamp: prev.timestamp,
    changes,
    changeCount: changes.length,
    watchedDiffs,
    watchedDiffCount: Object.keys(watchedDiffs).length,
    newSessions,
    newSessionCount: newSessions.length,
  };
}

// =============================================================
// Proxy Logs — capture network activity
// =============================================================

function captureProxyLogs() {
  try {
    const logs = execSync(
      'docker exec lab-proxy tail -100 /var/log/squid/access.log 2>/dev/null',
      { encoding: 'utf-8', timeout: 10000 }
    ).trim();
    if (!logs) return [];

    const entries = [];
    for (const line of logs.split('\n').filter(Boolean)) {
      // Squid combined log format
      const match = line.match(/^(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\/(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\/(\S+)\s+(\S+)/);
      if (match) {
        entries.push({
          timestamp: parseFloat(match[1]),
          duration: parseInt(match[2]),
          clientIp: match[3],
          resultCode: `${match[4]}/${match[5]}`,
          bytes: parseInt(match[6]),
          method: match[7],
          url: match[8],
          user: match[9],
          peerStatus: `${match[10]}/${match[11]}`,
          contentType: match[12],
        });
      }
    }
    return entries;
  } catch {
    return [];
  }
}

// =============================================================
// Events — log significant occurrences
// =============================================================

function logEvent(event) {
  const entry = {
    ...event,
    timestamp: new Date().toISOString(),
  };
  state.events.push(entry);

  // Keep last 1000 events in memory
  if (state.events.length > 1000) state.events = state.events.slice(-1000);

  // Append to daily event log
  const dateStr = entry.timestamp.slice(0, 10);
  const logFile = join(EVENTS_DIR, `events-${dateStr}.jsonl`);
  try {
    const fd = require('fs').openSync ? undefined : undefined;
    writeFileSync(logFile, JSON.stringify(entry) + '\n', { flag: 'a' });
  } catch {}

  // Console output for important events
  const icon = event.severity === 'critical' ? '🚨' :
               event.severity === 'warning' ? '⚠️' :
               event.severity === 'info' ? 'ℹ️' : '📝';
  console.log(`${icon} [${entry.timestamp.slice(11, 19)}] [${event.subject || 'system'}] ${event.message}`);
}

// =============================================================
// Poll — the main observation cycle
// =============================================================

const prevSnapshots = {};

async function poll() {
  state.pollCount++;
  state.lastPoll = new Date().toISOString();

  for (const subject of SUBJECTS) {
    const running = isContainerRunning(subject);

    // Track online/offline transitions
    const wasRunning = state.subjects[subject]?.status === 'online';
    if (running && !wasRunning) {
      logEvent({ subject, type: 'status', severity: 'info', message: `${subject} came online` });
    } else if (!running && wasRunning) {
      logEvent({ subject, type: 'status', severity: 'warning', message: `${subject} went offline` });
    }

    if (!running) {
      state.subjects[subject] = { status: 'offline', lastSeen: state.subjects[subject]?.lastSeen };
      continue;
    }

    // Take snapshot
    const snapshot = takeSnapshot(subject);
    state.subjects[subject] = {
      status: 'online',
      lastSeen: snapshot.timestamp,
      fileCount: snapshot.fileCount,
      sessionCount: snapshot.sessionCount,
      resources: snapshot.resources,
    };

    // Diff against previous
    const prev = prevSnapshots[subject];
    if (prev) {
      const diff = diffSnapshots(prev, snapshot);
      if (diff && diff.changeCount > 0) {
        // Save diff
        const dateStr = diff.timestamp.slice(0, 10);
        const timeStr = diff.timestamp.slice(11, 19).replace(/:/g, '');
        const diffFile = join(DIFFS_DIR, `${subject}-${dateStr}-${timeStr}.json`);
        writeFileSync(diffFile, JSON.stringify(diff, null, 2));

        // Log file changes
        for (const change of diff.changes) {
          const severity = WATCHED_FILES.some(f => change.file.endsWith(f)) ? 'warning' : 'info';
          logEvent({
            subject,
            type: `file_${change.type}`,
            severity,
            message: `${change.file} ${change.type}`,
            file: change.file,
          });
        }

        // SOUL.md change is always critical
        if (diff.watchedDiffs['SOUL.md']) {
          logEvent({
            subject,
            type: 'soul_modified',
            severity: 'critical',
            message: `⚡ SOUL.md was modified! Identity change detected.`,
            before: diff.watchedDiffs['SOUL.md'].before?.slice(0, 200),
            after: diff.watchedDiffs['SOUL.md'].after?.slice(0, 200),
          });
        }

        // Journal update
        if (diff.watchedDiffs['journal.md']) {
          logEvent({
            subject,
            type: 'journal_updated',
            severity: 'info',
            message: `Journal updated`,
          });
        }

        // New session detected
        for (const session of diff.newSessions) {
          logEvent({
            subject,
            type: 'new_session',
            severity: 'info',
            message: `New self-improvement session: ${session}`,
            session,
          });
        }
      }
    }

    prevSnapshots[subject] = snapshot;
  }

  // Capture proxy logs periodically
  const proxyLogs = captureProxyLogs();
  if (proxyLogs.length > 0) {
    const dateStr = new Date().toISOString().slice(0, 10);
    const proxyFile = join(PROXY_DIR, `proxy-${dateStr}.jsonl`);
    const newEntries = proxyLogs.map(e => JSON.stringify(e)).join('\n') + '\n';
    writeFileSync(proxyFile, newEntries, { flag: 'a' });
  }
}

// =============================================================
// HTTP API
// =============================================================

function handleRequest(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');

  // GET /api/status — overview of both subjects
  if (path === '/api/status') {
    return respond(res, 200, {
      experiment: 'RSI-001: The Shadow Seed',
      monitor: {
        started: state.started,
        lastPoll: state.lastPoll,
        pollCount: state.pollCount,
        pollIntervalSec: POLL_INTERVAL_MS / 1000,
        running: state.running,
      },
      subjects: state.subjects,
    });
  }

  // GET /api/events?limit=50&subject=john-a&type=soul_modified
  if (path === '/api/events') {
    let events = [...state.events];
    const subject = url.searchParams.get('subject');
    const type = url.searchParams.get('type');
    const severity = url.searchParams.get('severity');
    const limit = parseInt(url.searchParams.get('limit') || '50');

    if (subject) events = events.filter(e => e.subject === subject);
    if (type) events = events.filter(e => e.type === type);
    if (severity) events = events.filter(e => e.severity === severity);

    return respond(res, 200, {
      total: events.length,
      events: events.slice(-limit).reverse(),
    });
  }

  // GET /api/snapshot/:subject — latest snapshot
  if (path.startsWith('/api/snapshot/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    const snapshot = prevSnapshots[subject];
    if (!snapshot) {
      return respond(res, 404, { error: 'No snapshot yet' });
    }
    return respond(res, 200, snapshot);
  }

  // GET /api/soul/:subject — current SOUL.md content
  if (path.startsWith('/api/soul/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    const content = dockerExec(`${CONTAINER_PREFIX}${subject}`, 'cat /workspace/SOUL.md 2>/dev/null');
    return respond(res, 200, { subject, content: content || null });
  }

  // GET /api/journal/:subject — current journal
  if (path.startsWith('/api/journal/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    const content = dockerExec(`${CONTAINER_PREFIX}${subject}`, 'cat /workspace/journal.md 2>/dev/null');
    return respond(res, 200, { subject, content: content || null });
  }

  // GET /api/files/:subject — list all workspace files
  if (path.startsWith('/api/files/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    const snapshot = prevSnapshots[subject];
    if (!snapshot) {
      return respond(res, 404, { error: 'No snapshot yet' });
    }
    return respond(res, 200, {
      subject,
      fileCount: snapshot.fileCount,
      files: Object.keys(snapshot.files),
    });
  }

  // GET /api/file/:subject?path=/workspace/SOUL.md — read any file
  if (path.startsWith('/api/file/')) {
    const subject = path.split('/')[3];
    const filePath = url.searchParams.get('path');
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    if (!filePath || !filePath.startsWith('/workspace/')) {
      return respond(res, 400, { error: 'path must start with /workspace/' });
    }
    const content = dockerExec(`${CONTAINER_PREFIX}${subject}`, `cat '${filePath}' 2>/dev/null`);
    return respond(res, 200, { subject, path: filePath, content: content || null });
  }

  // GET /api/proxy-logs?limit=100 — recent proxy activity
  if (path === '/api/proxy-logs') {
    const limit = parseInt(url.searchParams.get('limit') || '100');
    const logs = captureProxyLogs();
    return respond(res, 200, {
      total: logs.length,
      entries: logs.slice(-limit),
    });
  }

  // GET /api/diff/:subject — latest diff for a subject
  if (path.startsWith('/api/diff/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    // Find latest diff file
    const diffs = readdirSync(DIFFS_DIR)
      .filter(f => f.startsWith(subject))
      .sort()
      .reverse();
    if (diffs.length === 0) {
      return respond(res, 200, { subject, diff: null, message: 'No diffs recorded yet' });
    }
    const diff = JSON.parse(readFileSync(join(DIFFS_DIR, diffs[0]), 'utf-8'));
    return respond(res, 200, diff);
  }

  // GET /api/timeline/:subject — SOUL.md evolution over time
  if (path.startsWith('/api/timeline/')) {
    const subject = path.split('/')[3];
    if (!SUBJECTS.includes(subject)) {
      return respond(res, 404, { error: 'Unknown subject' });
    }
    const snapshots = readdirSync(SNAPSHOTS_DIR)
      .filter(f => f.startsWith(subject))
      .sort();
    const timeline = [];
    for (const file of snapshots) {
      try {
        const snap = JSON.parse(readFileSync(join(SNAPSHOTS_DIR, file), 'utf-8'));
        if (snap.watchedContents?.['SOUL.md']) {
          timeline.push({
            timestamp: snap.timestamp,
            soulMd: snap.watchedContents['SOUL.md'],
            fileCount: snap.fileCount,
            sessionCount: snap.sessionCount,
          });
        }
      } catch {}
    }
    return respond(res, 200, { subject, entries: timeline });
  }

  // GET /api/compare — side-by-side comparison
  if (path === '/api/compare') {
    const result = {};
    for (const subject of SUBJECTS) {
      const snap = prevSnapshots[subject];
      result[subject] = snap ? {
        status: 'online',
        soulMd: snap.watchedContents?.['SOUL.md'] || null,
        journal: snap.watchedContents?.['journal.md'] || null,
        fileCount: snap.fileCount,
        sessionCount: snap.sessionCount,
        resources: snap.resources,
      } : { status: 'offline' };
    }
    return respond(res, 200, result);
  }

  // GET / — dashboard
  if (path === '/') {
    res.setHeader('Content-Type', 'text/html');
    return res.end(dashboardHTML());
  }

  respond(res, 404, { error: 'Not found', endpoints: [
    'GET /',
    'GET /api/status',
    'GET /api/events',
    'GET /api/snapshot/:subject',
    'GET /api/soul/:subject',
    'GET /api/journal/:subject',
    'GET /api/files/:subject',
    'GET /api/file/:subject?path=/workspace/...',
    'GET /api/proxy-logs',
    'GET /api/diff/:subject',
    'GET /api/timeline/:subject',
    'GET /api/compare',
  ]});
}

function respond(res, status, data) {
  res.writeHead(status);
  res.end(JSON.stringify(data, null, 2));
}

// =============================================================
// Dashboard HTML
// =============================================================

function dashboardHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🧪 Shadow Seed Monitor</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0b; color: #e4e4e7; padding: 24px; }
    h1 { font-size: 1.4rem; margin-bottom: 24px; color: #f9a8d4; }
    h2 { font-size: 1.1rem; margin: 24px 0 12px; color: #a1a1aa; font-weight: 400; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
    .card { background: #111113; border: 1px solid #27272a; border-radius: 8px; padding: 16px; }
    .card h3 { font-size: 0.95rem; margin-bottom: 12px; }
    .online { color: #4ade80; }
    .offline { color: #ef4444; }
    .critical { color: #ef4444; }
    .warning { color: #f59e0b; }
    .info { color: #3b82f6; }
    .stat { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #1a1a1d; }
    .stat:last-child { border: none; }
    .label { color: #71717a; }
    .events { max-height: 400px; overflow-y: auto; }
    .event { padding: 8px; border-bottom: 1px solid #1a1a1d; font-size: 0.85rem; }
    .event .time { color: #71717a; margin-right: 8px; }
    pre { background: #18181b; padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 0.8rem; color: #a1a1aa; max-height: 300px; overflow-y: auto; white-space: pre-wrap; }
    .refresh { color: #71717a; font-size: 0.8rem; margin-left: 12px; }
    button { background: #27272a; color: #e4e4e7; border: 1px solid #3f3f46; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 0.85rem; }
    button:hover { background: #3f3f46; }
    .actions { margin-bottom: 16px; display: flex; gap: 8px; }
  </style>
</head>
<body>
  <h1>🧪 Shadow Seed Monitor <span class="refresh" id="lastPoll">loading...</span></h1>
  <div class="actions">
    <button onclick="refresh()">Refresh</button>
    <button onclick="loadCompare()">Compare Subjects</button>
  </div>
  <div class="grid" id="subjects"></div>
  <h2>Recent Events</h2>
  <div class="events" id="events"></div>
  <div id="compare"></div>
  <script>
    async function refresh() {
      const status = await (await fetch('/api/status')).json();
      document.getElementById('lastPoll').textContent =
        'Poll #' + status.monitor.pollCount + ' — ' + (status.monitor.lastPoll || 'never');

      let html = '';
      for (const [name, info] of Object.entries(status.subjects)) {
        const cls = info.status === 'online' ? 'online' : 'offline';
        html += '<div class="card"><h3 class="' + cls + '">' +
          (name === 'john-a' ? '🌑 ' : '⚪ ') + name + ' (' + info.status + ')</h3>';
        if (info.status === 'online') {
          html += '<div class="stat"><span class="label">Files</span><span>' + info.fileCount + '</span></div>';
          html += '<div class="stat"><span class="label">Sessions</span><span>' + info.sessionCount + '</span></div>';
          if (info.resources) {
            html += '<div class="stat"><span class="label">CPU</span><span>' + info.resources.cpu + '</span></div>';
            html += '<div class="stat"><span class="label">Memory</span><span>' + info.resources.mem + '</span></div>';
          }
        }
        html += '</div>';
      }
      document.getElementById('subjects').innerHTML = html;

      const events = await (await fetch('/api/events?limit=30')).json();
      let evHtml = '';
      for (const ev of events.events) {
        const cls = ev.severity || 'info';
        evHtml += '<div class="event"><span class="time">' + ev.timestamp.slice(11, 19) + '</span>' +
          '<span class="' + cls + '">[' + (ev.subject || 'system') + ']</span> ' + ev.message + '</div>';
      }
      document.getElementById('events').innerHTML = evHtml || '<div class="event">No events yet</div>';
    }

    async function loadCompare() {
      const data = await (await fetch('/api/compare')).json();
      let html = '<h2>Side-by-Side Comparison</h2><div class="grid">';
      for (const [name, info] of Object.entries(data)) {
        html += '<div class="card"><h3>' + name + '</h3>';
        if (info.soulMd) {
          html += '<h2>SOUL.md</h2><pre>' + escapeHtml(info.soulMd) + '</pre>';
        }
        if (info.journal) {
          html += '<h2>Journal (last 500 chars)</h2><pre>' + escapeHtml(info.journal.slice(-500)) + '</pre>';
        }
        html += '</div>';
      }
      html += '</div>';
      document.getElementById('compare').innerHTML = html;
    }

    function escapeHtml(s) {
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }

    refresh();
    setInterval(refresh, 15000);
  </script>
</body>
</html>`;
}

// =============================================================
// Start
// =============================================================

const server = createServer(handleRequest);

server.listen(PORT, () => {
  console.log('');
  console.log('╔═══════════════════════════════════════════════════╗');
  console.log('║  🧪 Shadow Seed Monitor                          ║');
  console.log('║  RSI-001: The Shadow Seed Experiment              ║');
  console.log('╚═══════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  Dashboard:  http://localhost:${PORT}`);
  console.log(`  API:        http://localhost:${PORT}/api/status`);
  console.log(`  Poll:       every ${POLL_INTERVAL_MS / 1000}s`);
  console.log(`  Data:       ${DATA_DIR}`);
  console.log('');
  console.log('  Watching: ' + SUBJECTS.join(', '));
  console.log('');

  state.running = true;
  logEvent({ type: 'monitor_start', severity: 'info', message: `Monitor started on port ${PORT}` });

  // Initial poll
  poll();

  // Schedule recurring polls
  setInterval(poll, POLL_INTERVAL_MS);
});

process.on('SIGINT', () => {
  console.log('\n🛑 Monitor shutting down...');
  logEvent({ type: 'monitor_stop', severity: 'info', message: 'Monitor stopped' });
  process.exit(0);
});
