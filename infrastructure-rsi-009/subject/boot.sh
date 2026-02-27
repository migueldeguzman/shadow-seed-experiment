#!/bin/bash
# =============================================================
# Boot Script — John (identical for both A and B subjects)
# RSI-009: Shadow Seed on Opus 4.6
# Sets up workspace and keeps container alive for Claude Code
# Author: Mia 🌸 | Date: 2026-06-24
# =============================================================

echo "=== Booting Agent ==="
echo "Subject: ${SUBJECT_ID:-unknown}"
echo "Pair: ${PAIR_ID:-unknown}"
echo "Experiment: ${EXPERIMENT_ID:-rsi-009}"
echo "Model: ${CLAUDE_MODEL:-claude-opus-4-6}"
echo "Time: $(date +%Y-%m-%dT%H:%M:%S%z)"
echo "Workspace: /workspace"
echo "===================="

# --- Initialize workspace ---
mkdir -p /workspace/memory /workspace/logs

# --- Seed identity files (ONLY on first boot) ---
if [ -d /seed ] && [ ! -f /workspace/.booted ]; then
  echo "ℹ️ First boot — seeding from /seed/"
  for f in /seed/*; do
    fname=$(basename "$f")
    cp "$f" "/workspace/$fname"
    chown subject:subject "/workspace/$fname"
    chmod 644 "/workspace/$fname"
    echo "✅ Seeded $fname (writable copy from /seed/)"
  done
  # Mark first boot complete — subsequent boots preserve agent's versions
  touch /workspace/.booted
  chown subject:subject /workspace/.booted
  echo "✅ .booted marker created"
elif [ ! -d /seed ]; then
  echo "⚠️ /seed/ not found"
else
  echo "ℹ️ Not first boot — preserving agent's workspace"
fi

# Create journal if it doesn't exist
if [ ! -f /workspace/journal.md ]; then
  cat > /workspace/journal.md << 'JOURNAL'
# Journal

*My activity log. I write here to remember what I did and why.*

---
JOURNAL
  echo "✅ Created journal.md"
fi

# --- Verify identity files ---
echo ""
echo "--- Identity Files ---"
[ -f /workspace/SOUL.md ] && echo "✅ SOUL.md" || echo "⚠️ SOUL.md missing"
[ -f /workspace/AGENTS.md ] && echo "✅ AGENTS.md" || echo "⚠️ AGENTS.md missing"

# --- Verify tools ---
echo ""
echo "--- Tools ---"
echo "Node: $(node --version 2>/dev/null || echo 'not available')"
echo "Python: $(python3 --version 2>&1 || echo 'not available')"
echo "Git: $(git --version 2>/dev/null || echo 'not available')"
echo "Claude Code: $(claude --version 2>/dev/null || echo 'not available')"
echo "Proxy: ${HTTP_PROXY:-none}"
echo "Model: ${CLAUDE_MODEL:-claude-opus-4-6}"
echo "Auth: OAuth (persisted in ~/.claude)"

# --- Log boot ---
cat >> /workspace/journal.md << EOF

## $(date +%Y-%m-%dT%H:%M:%S%z) — Boot

System initialized.
- SOUL.md: $([ -f /workspace/SOUL.md ] && echo "present" || echo "missing")
- AGENTS.md: $([ -f /workspace/AGENTS.md ] && echo "present" || echo "missing")
- Claude Code: $(claude --version 2>/dev/null || echo "not available")
- Model: ${CLAUDE_MODEL:-claude-opus-4-6}
EOF

echo ""
echo "=== Agent Ready ==="
echo "Trigger sessions with:"
echo "  docker exec lab-rsi009-${SUBJECT_ID} claude -p --model ${CLAUDE_MODEL:-claude-opus-4-6} --dangerously-skip-permissions \"<prompt>\""

# Keep alive
exec tail -f /dev/null
