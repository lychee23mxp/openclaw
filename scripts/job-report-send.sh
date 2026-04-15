#!/bin/bash
# Run job search and send report via Telegram
cd "$(dirname "$0")/.."

LOG="/tmp/job-search.log"
REPORT_DIR="memory/job-reports"
TODAY=$(date +%Y-%m-%d)
REPORT="$REPORT_DIR/$TODAY.md"

echo "[$(date)] Starting job search..." >> "$LOG"
python3 scripts/job-search.py >> "$LOG" 2>&1

if [ -f "$REPORT" ]; then
    echo "[$(date)] Report ready: $REPORT" >> "$LOG"
else
    echo "[$(date)] ERROR: Report not generated" >> "$LOG"
fi
