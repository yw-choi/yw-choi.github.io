#!/usr/bin/env bash
set -euo pipefail

# Configuration
SRC_DIR="content/photos/images"
BACKUP_DIR="content/photos/originals_backup"
MAX_WIDTH=1200
JPEG_QUALITY=95

# Ensure required tools exist (ImageMagick's mogrify/convert & jpegoptim optional)
command -v mogrify >/dev/null 2>&1 || { echo "Error: ImageMagick (mogrify) not found." >&2; exit 1; }

mkdir -p "$BACKUP_DIR"

shopt -s nullglob nocaseglob
img_exts=(jpg jpeg JPG JPEG)

for ext in "${img_exts[@]}"; do
  for f in "$SRC_DIR"/*.$ext; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    base_noext="${fname%.*}"

    # Skip if already processed marker exists
    if grep -qi "optimized=1" <(identify -verbose "$f" 2>/dev/null || true) ; then
      echo "Skipping already optimized $fname"
      continue
    fi

    # Backup original (once)
    if [ ! -f "$BACKUP_DIR/$fname" ]; then
      cp -p "$f" "$BACKUP_DIR/$fname"
    fi

    # Get width
    width=$(identify -format "%w" "$f")

    tmpfile=$(mktemp /tmp/optimg.XXXXXX.jpg)

    if [ "$width" -gt "$MAX_WIDTH" ]; then
      convert "$f" -auto-orient -strip -resize ${MAX_WIDTH}x "$tmpfile"
    else
      convert "$f" -auto-orient -strip "$tmpfile"
    fi

    # Recompress with quality
    convert "$tmpfile" -quality $JPEG_QUALITY -interlace JPEG -set comment "optimized=1" "$f"
    rm -f "$tmpfile"

    echo "Optimized $fname (orig width=$width)"
  done
done

echo "Done. Originals stored in $BACKUP_DIR"
