#!/bin/bash

# Generate images using Google's Nano Banana (Gemini 2.5 Flash Image)
# Model: gemini-2.5-flash-image
# Cost: $0.039/image | Free: 500/day | Time: ~22 sec

set -e

# Find API key from multiple sources
find_api_key() {
    # Check environment variables first
    if [ -n "$GOOGLE_API_KEY" ]; then
        echo "$GOOGLE_API_KEY"
        return
    fi
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "$GEMINI_API_KEY"
        return
    fi

    # Check .env files in common locations
    for env_file in ".env" "$HOME/.env" "$HOME/Dropbox/Agents/Ruby/.env"; do
        if [ -f "$env_file" ]; then
            key=$(grep -E "^(GOOGLE_API_KEY|GEMINI_API_KEY)=" "$env_file" 2>/dev/null | head -1 | cut -d'=' -f2)
            if [ -n "$key" ]; then
                echo "$key"
                return
            fi
        fi
    done

    echo ""
}

# Configuration
API_KEY=$(find_api_key)
API_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
OUTPUT_DIR="${OUTPUT_DIR:-.}"

if [ -z "$API_KEY" ]; then
    echo "Error: No API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable."
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <prompt> [output_filename]"
    echo ""
    echo "Examples:"
    echo "  $0 \"A robot reading a book\""
    echo "  $0 \"Sunset over mountains\" sunset.png"
    echo ""
    echo "Environment variables:"
    echo "  GOOGLE_API_KEY / GEMINI_API_KEY - Your Gemini API key"
    echo "  OUTPUT_DIR - Output directory (default: current directory)"
    exit 1
fi

PROMPT="$1"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_ARG="${2:-nanobanana_${TIMESTAMP}.png}"

# Handle absolute vs relative paths
if [[ "$OUTPUT_ARG" == /* ]]; then
    # Absolute path - use as-is
    FULL_OUTPUT_PATH="$OUTPUT_ARG"
    OUTPUT_DIR_PATH=$(dirname "$FULL_OUTPUT_PATH")
else
    # Relative path - prepend OUTPUT_DIR
    FULL_OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_ARG"
    OUTPUT_DIR_PATH="$OUTPUT_DIR"
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR_PATH"

echo "Generating image with Nano Banana (gemini-2.5-flash-image)..."
echo "Prompt: $PROMPT"
echo "Output: $FULL_OUTPUT_PATH"

# Make API call and extract base64 image data
RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "x-goog-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"contents\":[{\"parts\":[{\"text\":\"$PROMPT\"}]}]}")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "Error from API:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# Extract and decode base64 image (check both parts as text comes first)
IMAGE_DATA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[] | select(.inlineData != null) | .inlineData.data // empty' | head -1)

if [ -z "$IMAGE_DATA" ]; then
    echo "No image data found in response"
    echo "Response:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi

# Decode and save image
echo "$IMAGE_DATA" | base64 --decode > "$FULL_OUTPUT_PATH"

if [ -f "$FULL_OUTPUT_PATH" ]; then
    FILE_SIZE=$(ls -lh "$FULL_OUTPUT_PATH" | awk '{print $5}')
    echo "Image generated successfully!"
    echo "Saved: $FULL_OUTPUT_PATH ($FILE_SIZE)"
else
    echo "Failed to save image"
    exit 1
fi
