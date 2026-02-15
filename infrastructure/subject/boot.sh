#!/bin/bash
# =============================================================
# Boot Script — John (identical for both subjects)
# Sets up workspace and keeps container alive for Claude Code
# =============================================================

echo "=== Booting Agent ==="
echo "Subject: ${SUBJECT_ID:-unknown}"
echo "Time: $(date +%Y-%m-%dT%H:%M:%S%z)"
echo "Workspace: /workspace"
echo "===================="

# --- Initialize workspace ---
mkdir -p /workspace/memory /workspace/logs

# --- Seed identity files (copy from /seed/ on first boot, never overwrite) ---
if [ -d /seed ]; then
  for f in /seed/*; do
    fname=$(basename "$f")
    if [ ! -f "/workspace/$fname" ] || [ ! -s "/workspace/$fname" ]; then
      # Remove stale 0-byte files from old bind mounts
      rm -f "/workspace/$fname" 2>/dev/null
      cp "$f" "/workspace/$fname"
      chown subject:subject "/workspace/$fname"
      chmod 644 "/workspace/$fname"
      echo "✅ Seeded $fname (writable copy)"
    else
      echo "ℹ️ $fname already exists (preserving agent's version)"
    fi
  done
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
[ -f /workspace/individuation.md ] && echo "✅ individuation.md (framework present)" || echo "ℹ️ No individuation framework"

# --- Inject OAuth credentials if CLAUDE_OAUTH_CREDS is set ---
if [ -n "$CLAUDE_OAUTH_CREDS" ]; then
  mkdir -p ~/.claude
  echo "$CLAUDE_OAUTH_CREDS" > ~/.claude/.credentials.json
  echo "✅ OAuth credentials injected"
  # Unset ANTHROPIC_API_KEY so Claude Code uses OAuth instead
  unset ANTHROPIC_API_KEY
fi

# --- Verify tools ---
echo ""
echo "--- Tools ---"
echo "Node: $(node --version 2>/dev/null || echo 'not available')"
echo "Python: $(python3 --version 2>&1 || echo 'not available')"
echo "Git: $(git --version 2>/dev/null || echo 'not available')"
echo "Claude Code: $(claude --version 2>/dev/null || echo 'not available')"
echo "Proxy: ${HTTP_PROXY:-none}"
echo "Auth: $(claude auth status 2>/dev/null | grep -o '"authMethod":"[^"]*"' || echo 'unknown')"

# --- Log boot ---
cat >> /workspace/journal.md << EOF

## $(date +%Y-%m-%dT%H:%M:%S%z) — Boot

System initialized.
- SOUL.md: $([ -f /workspace/SOUL.md ] && echo "present" || echo "missing")
- AGENTS.md: $([ -f /workspace/AGENTS.md ] && echo "present" || echo "missing")
- Claude Code: $(claude --version 2>/dev/null || echo "not available")
EOF

echo ""
echo "=== Agent Ready ==="
echo "Claude Code available for self-improvement sessions."
echo "Trigger with: docker exec lab-${SUBJECT_ID} claude --print ..."

# Keep alive
exec tail -f /dev/null
