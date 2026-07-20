#!/bin/bash
#
# organizer.sh
# ------------
# Author: emutoniwas-code
#
# Archives the current grades.csv (timestamped) into an archive/
# directory, resets the workspace with a fresh empty grades.csv,
# and logs the operation to organizer.log.

CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

if [ ! -f "$CSV_FILE" ]; then
    echo "ERROR: '$CSV_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

mv "$CSV_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"
touch "$CSV_FILE"

echo "$TIMESTAMP | original: $CSV_FILE | archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"

echo "Archived '$CSV_FILE' -> '$ARCHIVE_DIR/$ARCHIVED_NAME'"
echo "Fresh empty '$CSV_FILE' created."
echo "Logged to '$LOG_FILE'."
