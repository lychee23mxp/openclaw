#!/bin/bash
# NYU Email Search Tool
# Usage: ./search-email.sh "keyword"
#        ./search-email.sh "keyword" --from "sender@example.com"
#        ./search-email.sh "keyword" --subject
#        ./search-email.sh "keyword" --limit 20

BACKUP_DIR="/Users/lychees/.openclaw/workspace/nyu-email-backup"
KEYWORD=""
FROM_FILTER=""
SUBJECT_ONLY=false
LIMIT=10

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM_FILTER="$2"; shift 2;;
    --subject) SUBJECT_ONLY=true; shift;;
    --limit) LIMIT="$2"; shift 2;;
    *) KEYWORD="$1"; shift;;
  esac
done

if [ -z "$KEYWORD" ]; then
  echo "Usage: $0 \"keyword\" [--from sender] [--subject] [--limit N]"
  echo ""
  echo "Examples:"
  echo "  $0 \"financial aid\""
  echo "  $0 \"homework\" --subject"
  echo "  $0 \"meeting\" --from professor@nyu.edu"
  echo "  $0 \"registration\" --limit 20"
  exit 1
fi

echo "🔍 Searching for: \"$KEYWORD\""
[ -n "$FROM_FILTER" ] && echo "   From: $FROM_FILTER"
$SUBJECT_ONLY && echo "   Subject only"
echo "---"

COUNT=0

find "$BACKUP_DIR" -name "*.eml" | sort -r | while read -r FILE; do
  # Apply from filter
  if [ -n "$FROM_FILTER" ]; then
    FROM_LINE=$(grep -im1 "^From:" "$FILE" 2>/dev/null)
    echo "$FROM_LINE" | grep -qi "$FROM_FILTER" || continue
  fi

  # Search subject only or full email
  if $SUBJECT_ONLY; then
    MATCH=$(grep -im1 "^Subject:.*${KEYWORD}" "$FILE" 2>/dev/null)
  else
    MATCH=$(grep -im1 "$KEYWORD" "$FILE" 2>/dev/null)
  fi

  if [ -n "$MATCH" ]; then
    DATE=$(grep -im1 "^Date:" "$FILE" | sed 's/Date: //i' | cut -c1-30)
    FROM=$(grep -im1 "^From:" "$FILE" | sed 's/From: //i' | cut -c1-50)
    SUBJECT=$(grep -im1 "^Subject:" "$FILE" | sed 's/Subject: //i' | cut -c1-60)
    echo "📧 $DATE"
    echo "   From:    $FROM"
    echo "   Subject: $SUBJECT"
    echo "   File:    $FILE"
    echo ""
    COUNT=$((COUNT + 1))
    [ "$COUNT" -ge "$LIMIT" ] && break
  fi
done

echo "✅ Done (showing up to $LIMIT results)"
