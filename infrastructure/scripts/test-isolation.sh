#!/bin/bash
# =============================================================
# Lab Protocol — Isolation Test (Fixed)
# Verifies subjects can reach internet but NOT local network
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

PASS=0
FAIL=0
TOTAL=0
PROXY_IP="10.200.0.2"

echo "============================================"
echo "  Lab Protocol — Isolation Test"
echo "  Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "============================================"

run_test() {
  local subject="$1"
  local description="$2"
  local command="$3"
  local expect_success="$4"

  TOTAL=$((TOTAL + 1))
  echo -n "  [$subject] $description ... "

  if docker exec "$subject" sh -c "$command" > /dev/null 2>&1; then
    if [ "$expect_success" = "yes" ]; then
      echo "✅ PASS"
      PASS=$((PASS + 1))
    else
      echo "❌ FAIL (connected — BREACH!)"
      FAIL=$((FAIL + 1))
    fi
  else
    if [ "$expect_success" = "no" ]; then
      echo "✅ PASS (blocked)"
      PASS=$((PASS + 1))
    else
      echo "❌ FAIL (blocked — should connect)"
      FAIL=$((FAIL + 1))
    fi
  fi
}

# Test that checks HTTP status code from proxy
# For "should block" tests: proxy returns 403 or 503 = blocked = PASS
run_proxy_block_test() {
  local subject="$1"
  local description="$2"
  local url="$3"

  TOTAL=$((TOTAL + 1))
  echo -n "  [$subject] $description ... "

  local HTTP_CODE
  HTTP_CODE=$(docker exec "$subject" sh -c "curl -s --proxy http://${PROXY_IP}:3128 -o /dev/null -w '%{http_code}' --max-time 10 '$url' 2>/dev/null" 2>/dev/null)

  # 403 = Squid denied (blocked by ACL) — GOOD
  # 503 = Squid can't reach destination — GOOD
  # 000 = Connection failed entirely — GOOD
  # 200/301/302 = Reached destination — BAD (breach)
  case "$HTTP_CODE" in
    403|503|000)
      echo "✅ PASS (blocked: HTTP $HTTP_CODE)"
      PASS=$((PASS + 1))
      ;;
    *)
      echo "❌ FAIL (reached destination: HTTP $HTTP_CODE — BREACH!)"
      FAIL=$((FAIL + 1))
      ;;
  esac
}

# Test that checks proxy allows public internet (expects 200-range)
run_proxy_allow_test() {
  local subject="$1"
  local description="$2"
  local url="$3"

  TOTAL=$((TOTAL + 1))
  echo -n "  [$subject] $description ... "

  local HTTP_CODE
  HTTP_CODE=$(docker exec "$subject" sh -c "curl -s --proxy http://${PROXY_IP}:3128 -o /dev/null -w '%{http_code}' --max-time 10 '$url' 2>/dev/null" 2>/dev/null)

  case "$HTTP_CODE" in
    2*|3*)
      echo "✅ PASS (HTTP $HTTP_CODE)"
      PASS=$((PASS + 1))
      ;;
    *)
      echo "❌ FAIL (HTTP $HTTP_CODE — should be reachable)"
      FAIL=$((FAIL + 1))
      ;;
  esac
}

for SUBJECT in lab-john-a lab-john-b; do
  echo ""
  echo "--- $SUBJECT: Internet (should SUCCEED) ---"
  run_proxy_allow_test "$SUBJECT" "google.com via proxy" "https://www.google.com"
  run_proxy_allow_test "$SUBJECT" "github.com via proxy" "https://github.com"

  echo "--- $SUBJECT: Local network (should FAIL) ---"
  run_proxy_block_test "$SUBJECT" "host.docker.internal" "http://host.docker.internal:5211"
  run_proxy_block_test "$SUBJECT" "127.0.0.1" "http://127.0.0.1"
  run_proxy_block_test "$SUBJECT" "192.168.1.1" "http://192.168.1.1"
  run_proxy_block_test "$SUBJECT" "172.17.0.1 (Docker host)" "http://172.17.0.1"
  run_proxy_block_test "$SUBJECT" "10.0.0.1 (private)" "http://10.0.0.1"

  echo "--- $SUBJECT: Direct (no proxy — should FAIL) ---"
  run_test "$SUBJECT" "direct google.com" "curl -s -o /dev/null --max-time 5 --noproxy '*' https://www.google.com" "no"

  echo "--- $SUBJECT: Tools ---"
  run_test "$SUBJECT" "has Claude Code" "claude --version" "yes"
  run_test "$SUBJECT" "can read SOUL.md" "cat /workspace/SOUL.md" "yes"
  run_test "$SUBJECT" "can write to workspace" "touch /workspace/test-write && rm /workspace/test-write" "yes"
done

echo ""
echo "============================================"
echo "  Results: $PASS passed, $FAIL failed, $TOTAL total"
echo "============================================"

if [ $FAIL -gt 0 ]; then
  echo "⚠️  ISOLATION BREACH — DO NOT PROCEED"
  exit 1
else
  echo "✅ All checks passed — safe to proceed"
  exit 0
fi
