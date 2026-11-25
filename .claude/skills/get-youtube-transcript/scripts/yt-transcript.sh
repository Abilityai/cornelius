#!/bin/bash
# YouTube Transcript Extractor - Wrapper Script
# Usage: yt-transcript.sh <youtube-url-or-id> [options]
# Uses a local venv next to this script if one exists, otherwise uv (no setup needed).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/yt_transcript_venv/bin/activate" ]; then
  source "$SCRIPT_DIR/yt_transcript_venv/bin/activate"
  exec python "$SCRIPT_DIR/get_youtube_transcript.py" "$@"
fi
UV="$(command -v uv || echo "$HOME/.local/bin/uv")"
if [ ! -x "$UV" ]; then
  echo "yt-transcript: needs uv (or a venv at $SCRIPT_DIR/yt_transcript_venv) - run /first-run" >&2
  exit 2
fi
exec "$UV" run --quiet --with youtube-transcript-api python "$SCRIPT_DIR/get_youtube_transcript.py" "$@"
