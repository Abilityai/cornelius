#!/usr/bin/env python3
"""
Generate thumbnails using Gemini 2.5 Flash Image API.
Supports 16:9 aspect ratio for horizontal thumbnails (YouTube, etc.).

Usage:
    python generate_thumbnail.py "prompt" output_path.png
    python generate_thumbnail.py "prompt"  # saves to /tmp/thumbnail.png
"""

import requests
import base64
import sys
import os
from pathlib import Path


def find_api_key():
    """Find API key from environment or .env files."""
    # Check environment variables first
    for var in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
        if os.environ.get(var):
            return os.environ[var]

    # Check .env files in common locations
    env_paths = [
        Path(".env"),
        Path.home() / ".env",
        Path.home() / "Dropbox/Agents/Ruby/.env",
    ]

    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
                            return value

    return None


API_KEY = find_api_key()
if not API_KEY:
    print("Error: No API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY.")
    sys.exit(1)

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"


def generate_thumbnail(prompt: str, output_path: str, aspect_ratio: str = "16:9"):
    """Generate a thumbnail image with specified aspect ratio.

    Args:
        prompt: Text description of the image to generate
        output_path: Where to save the PNG file
        aspect_ratio: Image aspect ratio (default: 16:9 for thumbnails)

    Returns:
        True if successful, False otherwise
    """
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "aspectRatio": aspect_ratio
            }
        }
    }

    response = requests.post(URL, json=payload)
    data = response.json()

    if "candidates" not in data:
        print(f"Error: {data.get('error', data)}")
        return False

    parts = data["candidates"][0]["content"]["parts"]
    for part in parts:
        if "inlineData" in part:
            img_data = part["inlineData"]["data"]

            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(base64.b64decode(img_data))

            file_size = os.path.getsize(output_path)
            print(f"Saved: {output_path} ({file_size / 1024:.1f} KB)")
            return True

    print("Error: No image in response")
    return False


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Professional YouTube thumbnail"
    output = sys.argv[2] if len(sys.argv) > 2 else "/tmp/thumbnail.png"
    generate_thumbnail(prompt, output)
