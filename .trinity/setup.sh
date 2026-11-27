#!/bin/bash
# Trinity persistent setup — runs on every container start (base-image
# convention: startup.sh executes ~/.trinity/setup.sh when present).
# Idempotent and fast; must never block startup.

# Resolve the agent root from this script's own location (<root>/.trinity/setup.sh)
# so the same file works in any clone layout — never hardcode a home path.
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- Brain Orb (trinity-enterprise#76) -------------------------------------
# 1. Hooks must be executable for the agent-server to run them (_hook_ready
#    checks X_OK). Git preserves the bit, but a GitHub-web-UI edit ships 644 —
#    re-assert at boot so a hotfixed hook never silently 404s.
if [ -d "$AGENT_DIR/.trinity/brain-orb" ]; then
    chmod +x "$AGENT_DIR/.trinity/brain-orb/scopes" \
             "$AGENT_DIR/.trinity/brain-orb/scope" \
             "$AGENT_DIR/.trinity/brain-orb/search" \
             "$AGENT_DIR/.trinity/brain-orb/action" 2>/dev/null || true
fi

# 2. First-boot graph: the live data.json is gitignored (re-export churn must
#    not land in auto-sync commits), so a fresh clone renders from the committed
#    seed. Copy-once; scope/refresh re-exports own the file afterwards.
VIZ_DIR="$AGENT_DIR/resources/agent-visualization"
if [ -f "$VIZ_DIR/data.seed.json" ] && [ ! -f "$VIZ_DIR/data.json" ]; then
    cp "$VIZ_DIR/data.seed.json" "$VIZ_DIR/data.json"
    echo "Brain Orb: seeded data.json from data.seed.json"
fi

# --- Local brain search: first-boot bootstrap, then the daemon ---------------
# A fresh fork has no venv and no index. Until ~/.trinity-bootstrap.done exists,
# launch the bootstrap DETACHED on EVERY start (venv -> pip -> reindex -> daemon ->
# smoke search; log ~/.trinity-bootstrap.log) and return at once - startup must
# never block. It resumes where an earlier run was cut off: the platform restarts
# a new instance's container minutes after its first start (to apply the Claude
# credential), usually mid-way, and the venv may already import by then - so
# "venv works" is NOT "bootstrap finished" (that test used to skip the resume and
# leave the instance without a marker for good). /first-run finishes it too.
LBS="$AGENT_DIR/resources/local-brain-search"
BOOTSTRAP="$AGENT_DIR/.trinity/bootstrap.sh"
if [ -f "$BOOTSTRAP" ] && [ ! -f "$HOME/.trinity-bootstrap.done" ]; then
    chmod +x "$BOOTSTRAP" 2>/dev/null || true
    echo "Brain search bootstrap not finished - (re)starting it in the background (see ~/.trinity-bootstrap.log, or run /first-run)"
    nohup bash "$BOOTSTRAP" >/dev/null 2>&1 < /dev/null &
elif [ -x "$LBS/venv/bin/python" ] && "$LBS/venv/bin/python" -c "import faiss, sentence_transformers" >/dev/null 2>&1; then
    echo "Starting brain search daemon..."
    "$LBS/run_daemon.sh" start || true
fi
