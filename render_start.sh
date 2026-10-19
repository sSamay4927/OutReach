#!/bin/bash
set -e

echo "=============================================="
echo " Starting Outreach Tool on Render"
echo "=============================================="

# Resolve directory paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
DATA_DIR="${DATA_DIR:-$BACKEND_DIR}"

mkdir -p "$DATA_DIR/uploads"

echo "Using DATA_DIR: $DATA_DIR"
cd "$BACKEND_DIR"

# 1. Initialize SQLite Database
echo "[1/3] Initializing SQLite database..."
python -c "from db import init_db; init_db(); print('Database ready.')"

# 2. Start Background Batch Worker Daemon
echo "[2/3] Launching autonomous batch worker..."
python batch_worker.py &
WORKER_PID=$!
echo "Batch worker running with PID: $WORKER_PID"

# Graceful termination handler
cleanup() {
    echo "Received termination signal. Shutting down gracefully..."
    kill -TERM "$WORKER_PID" 2>/dev/null || true
    wait "$WORKER_PID" 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

# 3. Start Gunicorn Web Server
PORT_NUM="${PORT:-5000}"
echo "[3/3] Starting Gunicorn on port $PORT_NUM..."
gunicorn \
    --workers 1 \
    --bind "0.0.0.0:$PORT_NUM" \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    "app:app" &
GUNICORN_PID=$!

# Wait for process exit
wait $GUNICORN_PID
