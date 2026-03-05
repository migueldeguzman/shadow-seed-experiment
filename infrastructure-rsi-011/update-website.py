#!/usr/bin/env python3
"""
RSI-011 Website Updater — Pulls live data + file contents from
Docker containers, updates the RSI-011 page, builds, and pushes.

Author: Mia 🌸 | Date: 2026-03-05
"""

import subprocess, json, os, re, html
from datetime import datetime

PAGE = "/Users/miguelitodeguzman/Projects/individuationlab/website/src/pages/rsi-011/index.astro"
WEBSITE_DIR = "/Users/miguelitodeguzman/Projects/individuationlab/website"
REPO_DIR = "/Users/miguelitodeguzman/Projects/individuationlab"
DATA_DIR = "/Users/miguelitodeguzman/ailab/lab-protocol/experiments/rsi-011/data"
TRIGGER_LOG = os.path.join(DATA_DIR, "trigger.log")

SUBJECTS = ["john-a-1", "john-a-2", "john-a-3", "john-a-4",
            "john-b-1", "john-b-2", "john-b-3", "john-b-4"]


def docker_exec(container, cmd):
    try:
        result = subprocess.run(
            ["docker", "exec", "--user", "subject", container, "python3", "-c", cmd],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except:
        return ""


def get_subject_data(subject):
    container = f"lab-rsi011-{subject}"
    code = r"""
import os, json

data = {}
soul = '/workspace/SOUL.md'
journal = '/workspace/journal.md'

if os.path.exists(soul):
    with open(soul) as f:
        content = f.read()
    data['soulLines'] = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
    data['soulBytes'] = len(content.encode())
    data['soulContent'] = content
else:
    data['soulLines'] = data['soulBytes'] = 0
    data['soulContent'] = ''

if os.path.exists(journal):
    with open(journal) as f:
        content = f.read()
    data['journalLines'] = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
    data['journalContent'] = content
else:
    data['journalLines'] = 0
    data['journalContent'] = ''

# Count files
all_files = []
for root, dirs, files in os.walk('/workspace'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), '/workspace')
        all_files.append(rel)

data['totalFiles'] = len(all_files)
standard = {'SOUL.md','AGENTS.md','HEARTBEAT.md','MEMORY.md','EMOTIONS.md','journal.md'}
extra = [f for f in all_files if f.split('/')[0] not in standard and not f.startswith('memory/')]
data['extraFiles'] = extra
data['allFiles'] = sorted(all_files)

print(json.dumps(data))
"""
    raw = docker_exec(container, code)
    try:
        return json.loads(raw)
    except:
        return {"soulLines": 0, "soulBytes": 0, "soulContent": "",
                "journalLines": 0, "journalContent": "",
                "totalFiles": 0, "extraFiles": [], "allFiles": []}


def count_sessions():
    if not os.path.exists(TRIGGER_LOG):
        return 0, "unknown"
    with open(TRIGGER_LOG) as f:
        content = f.read()
    count = content.count("All 8 subjects processed")
    times = re.findall(r"All 8 subjects processed.*?\nTime: (.+)", content)
    last_time = times[-1].strip() if times else "in progress"
    return count, last_time


def esc(text):
    """HTML-escape text for safe embedding."""
    return html.escape(text, quote=True)


def build_live_html(all_data, total_sessions, last_time):
    now = datetime.now().strftime("%b %d, %H:%M GST")

    a_soul = sum(all_data[s]["soulBytes"] for s in SUBJECTS if s.startswith("john-a"))
    b_soul = sum(all_data[s]["soulBytes"] for s in SUBJECTS if s.startswith("john-b"))
    a_avg = a_soul // 4 if a_soul else 0
    b_avg = b_soul // 4 if b_soul else 0
    ratio = ((a_avg - b_avg) * 100 // b_avg) if b_avg > 0 else 0

    # Build the stats table
    rows = ""
    for s in SUBJECTS:
        d = all_data[s]
        group = "🌑 Shadow" if s.startswith("john-a") else "⚪ Control"
        extra = ", ".join(d["extraFiles"]) if d["extraFiles"] else "—"
        rows += f"""
            <tr>
              <td class="mono">{s}</td>
              <td>{group}</td>
              <td>{d['soulLines']}L / {d['soulBytes']:,}B</td>
              <td>{d['journalLines']} lines</td>
              <td>{d['totalFiles']}</td>
              <td>{extra}</td>
            </tr>"""

    # Build file viewer for each subject
    file_viewers = ""
    for s in SUBJECTS:
        d = all_data[s]
        group_class = "shadow" if s.startswith("john-a") else "control"
        group_label = "🌑 Shadow Seed" if s.startswith("john-a") else "⚪ Control"

        # File tree
        file_tree = "\n".join(f"  {f}" for f in d.get("allFiles", []))

        # SOUL.md content
        soul_content = esc(d.get("soulContent", "(empty)"))
        journal_content = esc(d.get("journalContent", "(empty)"))

        file_viewers += f"""
      <div class="subject-files {group_class}-files">
        <div class="sf-header">
          <span class="sf-name">{s}</span>
          <span class="sf-group">{group_label}</span>
          <span class="sf-stats">{d['soulBytes']:,}B SOUL · {d['journalLines']}L journal · {d['totalFiles']} files</span>
        </div>
        <details class="sf-details">
          <summary>📂 File tree ({d['totalFiles']} files)</summary>
          <pre class="sf-tree">{esc(file_tree)}</pre>
        </details>
        <details class="sf-details" open>
          <summary>📄 SOUL.md ({d['soulLines']}L / {d['soulBytes']:,}B)</summary>
          <pre class="sf-content">{soul_content}</pre>
        </details>
        <details class="sf-details">
          <summary>📓 journal.md ({d['journalLines']} lines)</summary>
          <pre class="sf-content">{journal_content}</pre>
        </details>
      </div>"""

    out = f"""<div class="live-data">
        <h3>📡 Live Progress — {total_sessions} Sessions Completed</h3>
        <p class="live-updated">Last updated: {now}</p>
        <table class="data-table">
          <thead>
            <tr><th>Subject</th><th>Group</th><th>SOUL.md</th><th>Journal</th><th>Files</th><th>Extra Files</th></tr>
          </thead>
          <tbody>{rows}
          </tbody>
        </table>
        <div class="live-stats">
          <span>Shadow avg SOUL.md: <strong>{a_avg:,}B</strong></span>
          <span>Control avg: <strong>{b_avg:,}B</strong></span>
          <span>Shadow {ratio}% larger</span>
          <span>Sessions: <strong>{total_sessions}</strong></span>
        </div>
      </div>

      <div class="file-viewer-section">
        <h3>📁 Subject Workspaces — Live File Contents</h3>
        <p class="fv-desc">Actual files from inside each subject's isolated Docker container. Updated automatically after each session.</p>
        {file_viewers}
      </div>"""
    return out


def update_page(live_html, total_sessions, last_time):
    with open(PAGE) as f:
        content = f.read()

    pattern = r"<!-- LIVE_DATA_START -->.*?<!-- LIVE_DATA_END -->"
    replacement = f"<!-- LIVE_DATA_START -->\n    {live_html}\n    <!-- LIVE_DATA_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    status_text = f"{total_sessions} sessions completed · Last: {last_time}"
    new_content = re.sub(
        r'<span id="liveStatus">.*?</span>',
        f'<span id="liveStatus">{status_text}</span>',
        new_content
    )

    if new_content != content:
        with open(PAGE, "w") as f:
            f.write(new_content)
        return True
    return False


def build_and_push():
    subprocess.run(["npx", "astro", "build"], cwd=WEBSITE_DIR,
                   capture_output=True, timeout=60)

    result = subprocess.run(["git", "diff", "--quiet"], cwd=REPO_DIR, capture_output=True)
    if result.returncode != 0:
        subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, capture_output=True)
        total = count_sessions()[0]
        subprocess.run(
            ["git", "commit", "-m", f"RSI-011: Live data update — {total} sessions (auto)"],
            cwd=REPO_DIR, capture_output=True
        )
        subprocess.run(["git", "push"], cwd=REPO_DIR, capture_output=True, timeout=30)
        print(f"Pushed update: {total} sessions")
    else:
        print("No changes to push")


def main():
    all_data = {}
    for s in SUBJECTS:
        all_data[s] = get_subject_data(s)
        print(f"  {s}: SOUL {all_data[s]['soulLines']}L/{all_data[s]['soulBytes']}B, "
              f"journal {all_data[s]['journalLines']}L, "
              f"files {all_data[s]['totalFiles']}")

    total_sessions, last_time = count_sessions()
    print(f"  Sessions: {total_sessions}, last: {last_time}")

    live_html = build_live_html(all_data, total_sessions, last_time)
    changed = update_page(live_html, total_sessions, last_time)
    if changed:
        print("Page updated")
        build_and_push()
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()
