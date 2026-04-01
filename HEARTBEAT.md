# HEARTBEAT.md

## GitHub Daily Sync Check

Check if today's sync ran successfully:

1. Run: `tail -5 /tmp/coco-sync.log`
2. If today's date appears with "✅ daily sync ok" → all good, stay silent
3. If today's date is MISSING or shows an error → alert Lychee: "⚠️ GitHub daily sync failed today — no green square. Check /tmp/coco-sync.log"

Only alert once per day. Do not repeat on every heartbeat.
