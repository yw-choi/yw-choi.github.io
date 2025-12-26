#!/bin/bash

# Usage: ./compress.sh image1.jpg image2.png ...
# Converts images to WebP format with quality 80

for FILENAME in "$@"; do
    # Check if file exists
    if [ ! -f "$FILENAME" ]; then
        echo "Warning: File '$FILENAME' not found, skipping..."
        continue
    fi
    
    # Get the base name without extension
    BASENAME="${FILENAME%.*}"
    OUTPUT="${BASENAME}.webp"
    
    echo "Converting: $FILENAME -> $OUTPUT"
    cwebp -q 80 "$FILENAME" -o "$OUTPUT"
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully converted: $OUTPUT"
    else
        echo "✗ Failed to convert: $FILENAME"
    fi
done

echo "Done!"


