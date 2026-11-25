#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Extracts transcripts from YouTube videos using youtube-transcript-api.
Free, local, no API key required.
"""

import sys
import re
import json
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return as-is if already an ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_transcript(video_id: str, language: str = 'en') -> list:
    """Fetch transcript for a video."""
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript = ytt_api.fetch(video_id, languages=[language])
        return transcript
    except Exception as e:
        # Try to get any available transcript
        try:
            transcript_list = ytt_api.list(video_id)
            available = [t.language_code for t in transcript_list]
            if available:
                transcript = ytt_api.fetch(video_id, languages=available[:1])
                return transcript
        except:
            pass
        raise e


def format_transcript(transcript, output_format: str = 'text') -> str:
    """Format transcript to specified format."""
    if output_format == 'json':
        formatter = JSONFormatter()
        return formatter.format_transcript(transcript)
    elif output_format == 'text':
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    elif output_format == 'raw':
        return json.dumps([dict(entry) for entry in transcript], indent=2)
    else:
        # Default: plain text concatenation
        return '\n'.join(entry.text for entry in transcript)


def main():
    parser = argparse.ArgumentParser(description='Extract YouTube video transcripts')
    parser.add_argument('video', help='YouTube URL or video ID')
    parser.add_argument('-l', '--language', default='en', help='Language code (default: en)')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'raw'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')

    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
        transcript = get_transcript(video_id, args.language)
        output = format_transcript(transcript, args.format)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Transcript saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
