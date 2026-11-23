#!/usr/bin/env bash

APP_DIR="/home/user/raspberrypi-image-receiver"
VENV_PYTHON="$APP_DIR/.venv/bin/python"
SCRIPT="$APP_DIR/analysis.py"
LOG_FILE="$APP_DIR/analysis.log" 
LOCK_FILE="/tmp/raspberrypi-analysis.lock"

cd "$APP_DIR"

exec 200>"$LOCK_FILE"
flock -n 200 || exit 0

"$VENV_PYTHON" "$SCRIPT" >> "$LOG_FILE" 2>&1