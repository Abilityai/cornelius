---
name: get-youtube-transcript
description: Extract the transcript from a YouTube video by URL or video ID. Use when the user shares a YouTube link and wants the transcript, captions, or text content of the video. Falls back automatically if the requested language isn't available.
automation: autonomous
allowed-tools: [Bash]
user-invocable: true
argument-hint: "<youtube-url-or-video-id>"
---

# Get YouTube Transcript

Extract a full transcript from any YouTube video using the local youtube-transcript-api (no rate limits, no API key required).

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Script | `scripts/utilities/yt-transcript.sh` | ✓ | - |
| Venv | `scripts/utilities/yt_transcript_venv/` | ✓ | - |
| YouTube | External (via youtube-transcript-api) | ✓ | - |

## Process

### Step 1: Extract the transcript

Run the wrapper script with the URL or video ID the user provided:

```bash
$PROJECT_ROOT/scripts/utilities/yt-transcript.sh "<url-or-id>"
```

Options:
- `-l <lang>` — language code (default: `en`). If user specifies a language, pass it.
- `-f text` — plain text output (default, best for reading)
- `-f json` — structured output with timestamps (use when user needs timestamps)

### Step 2: Handle errors

If the script fails:
1. **Language not found** — retry without `-l` flag (auto-selects any available language)
2. **Video unavailable** — inform user the video may be private, deleted, or region-restricted
3. **No transcript available** — inform user the video has no captions

### Step 3: Present the transcript

Return the full transcript text to the user. If it's long (>500 lines), summarize what the video covers first, then provide the full text.

## Example

User: "get me the transcript of https://youtu.be/abc123"

```bash
$PROJECT_ROOT/scripts/utilities/yt-transcript.sh "https://youtu.be/abc123"
```

## Notes

- Uses `youtube-transcript-api` Python package — works locally with no quota
- Falls back to any available language if English isn't found
- The MCP youtube-transcript tool hits rate limits; always prefer this script
