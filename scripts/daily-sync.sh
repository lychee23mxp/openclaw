#!/bin/bash
# Daily GitHub sync for coco-workspace
cd /Users/lychees/.openclaw/workspace
git add -A
git commit -m "daily sync: $(date '+%Y-%m-%d')" --allow-empty
git push origin main
