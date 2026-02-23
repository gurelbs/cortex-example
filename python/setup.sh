#!/usr/bin/env bash
# =============================================================================
# setup.sh  —  One-shot setup for the Emotiv Cortex Python project
# =============================================================================
# Usage:
#   cd python/
#   chmod +x setup.sh
#   ./setup.sh
#
# What this script does:
#   1. Creates a Python virtual environment in .venv/
#   2. Installs all dependencies from requirements.txt
#   3. Copies .env.example → .env (if .env does not already exist)
#   4. Verifies the configuration
# =============================================================================

set -e  # Exit immediately on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
PYTHON="${PYTHON:-python3}"

# ---------------------------------------------------------------------------
# 1. Create virtual environment
# ---------------------------------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "→ Creating virtual environment in ${VENV_DIR}/ ..."
    "$PYTHON" -m venv "$VENV_DIR"
else
    echo "✔  Virtual environment already exists at ${VENV_DIR}/"
fi

# ---------------------------------------------------------------------------
# 2. Install dependencies
# ---------------------------------------------------------------------------
echo "→ Installing dependencies from requirements.txt ..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r requirements.txt
echo "✔  Dependencies installed."

# ---------------------------------------------------------------------------
# 3. Create .env from example (if not present)
# ---------------------------------------------------------------------------
if [ ! -f ".env" ]; then
    echo "→ Creating .env from .env.example ..."
    cp .env.example .env
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ACTION REQUIRED                                              ║"
    echo "║  Open '.env' and fill in your Cortex credentials:            ║"
    echo "║    EMOTIV_CLIENT_ID=your_app_client_id_here                  ║"
    echo "║    EMOTIV_CLIENT_SECRET=your_app_client_secret_here          ║"
    echo "║                                                               ║"
    echo "║  Get credentials at:                                          ║"
    echo "║  https://emotiv.gitbook.io/cortex-api#create-a-cortex-app   ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
else
    echo "✔  .env already exists (not overwritten)."
fi

# ---------------------------------------------------------------------------
# 4. Verify configuration
# ---------------------------------------------------------------------------
echo "→ Verifying configuration ..."
"$VENV_DIR/bin/python" config.py

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  Setup complete! Activate the environment with:"
echo "    source .venv/bin/activate"
echo ""
echo "  Then run any example:"
echo "    python sub_data.py          # Subscribe to EEG / motion data"
echo "    python record.py            # Record and export data"
echo "    python marker.py            # Inject markers"
echo "    python mental_command_train.py  # Train mental commands"
echo "    python facial_expression_train.py  # Train facial expressions"
echo "    python live_advance.py      # Live mental command + sensitivity"
echo "════════════════════════════════════════════════════════════════════"
