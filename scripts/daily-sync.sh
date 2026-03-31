#!/bin/bash
# Daily GitHub sync for coco-workspace
cd /Users/lychees/.openclaw/workspace

# Create/update today's memory file
TODAY=$(date '+%Y-%m-%d')
MEMORY_FILE="memory/${TODAY}.md"
mkdir -p memory

if [ ! -f "$MEMORY_FILE" ]; then
  echo "# ${TODAY}" > "$MEMORY_FILE"
  echo "" >> "$MEMORY_FILE"
  echo "## Daily Note" >> "$MEMORY_FILE"
  echo "" >> "$MEMORY_FILE"
  echo "- Daily sync" >> "$MEMORY_FILE"
fi

git add -A

# Commit with Lychee's GitHub email so it counts as a contribution
GIT_AUTHOR_EMAIL="ys3848@nyu.edu" \
GIT_COMMITTER_EMAIL="ys3848@nyu.edu" \
GIT_AUTHOR_NAME="lychee23mxp" \
GIT_COMMITTER_NAME="lychee23mxp" \
git commit -m "daily sync: ${TODAY}" --allow-empty

git push origin main
