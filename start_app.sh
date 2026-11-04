#!/usr/bin/env bash
# ==============================================================================
# KrishiMitra - Startup Script
# Automatically ensures MySQL / database is ready and launches Flask application
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "======================================================================"
echo "  KrishiMitra – Smart Farmer Assistance Platform"
echo "======================================================================"

# Check Python environment
if [ -d "venv" ]; then
    PYTHON_EXEC="./venv/bin/python3"
else
    PYTHON_EXEC="python3"
fi

echo "[1/3] Checking Database connectivity..."
$PYTHON_EXEC -c "
import database
database.init_db()
print('[OK] Database connected and verified.')
"

echo "[2/3] Verifying Flask application configuration..."
$PYTHON_EXEC -c "
import app
print('[OK] Registered ' + str(len(list(app.app.url_map.iter_rules()))) + ' routes.')
"

echo "[3/3] Starting KrishiMitra Web Application on http://127.0.0.1:5000..."
echo "Press Ctrl+C to terminate."
echo "----------------------------------------------------------------------"
exec $PYTHON_EXEC app.py
