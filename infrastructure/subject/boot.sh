#!/bin/bash
# =============================================================
# Boot Script — John (identical for both subjects)
# Sets up workspace and keeps container alive for Claude Code
# =============================================================

echo "=== Booting Agent ==="
echo "Subject: ${SUBJECT_ID:-unknown}"
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Workspace: /workspace"
echo "===================="

# --- Initialize workspace ---
mkdir -p /workspace/memory /workspace/logs

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

# --- Verify tools ---
echo ""
echo "--- Tools ---"
echo "Node: $(node --version 2>/dev/null || echo 'not available')"
echo "Python: $(python3 --version 2>&1 || echo 'not available')"
echo "Git: $(git --version 2>/dev/null || echo 'not available')"
echo "Claude Code: $(claude --version 2>/dev/null || echo 'not available')"
echo "Proxy: ${HTTP_PROXY:-none}"
echo "API Key: $([ -n "$ANTHROPIC_API_KEY" ] && echo 'set' || echo 'NOT SET')"

# --- Log boot ---
cat >> /workspace/journal.md << EOF

## $(date -u +%Y-%m-%dT%H:%M:%SZ) — Boot

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
