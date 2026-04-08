# HEARTBEAT.md

Check if today's sync ran: `tail -5 /tmp/coco-sync.log`
- Today's date + "✅ daily sync ok" → HEARTBEAT_OK
- Missing or error → alert Lychee once per day
