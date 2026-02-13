#!/usr/bin/env python3
"""
Generate images using Gemini 2.5 Flash Image API with configurable options.

Usage:
    python generate_image.py "prompt" output.png
    python generate_image.py "prompt" output.png --aspect-ratio 16:9
    python generate_image.py "prompt" output.png --aspect-ratio 9:16  # vertical
    python generate_image.py "prompt"  # saves to /tmp/generated_image.png

Aspect ratios:
    1:1   - Square (default, 1024x1024)
    16:9  - Horizontal/landscape (thumbnails, presentations)
    9:16  - Vertical/portrait (stories, reels, TikTok)
    4:3   - Classic landscape
    3:4   - Classic portrait
"""

import requests
import base64
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime


def find_api_key():
    """Find API key from environment or .env files."""
    for var in ["GOOGLE_API_KEY", "GEMINI_API_KEY"]:
        if os.environ.get(var):
            return os.environ[var]

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


def generate_image(prompt: str, output_path: str, aspect_ratio: str = "1:1") -> bool:
    """Generate an image with the Gemini 2.5 Flash Image model.

    Args:
        prompt: Text description of the image
        output_path: Where to save the PNG
        aspect_ratio: One of 1:1, 16:9, 9:16, 4:3, 3:4

    Returns:
        True if successful, False otherwise
    """
    api_key = find_api_key()
    if not api_key:
        print("Error: No API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY.")
        return False

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
        }
    }

    # Only add imageConfig if non-default aspect ratio
    if aspect_ratio != "1:1":
        payload["generationConfig"]["imageConfig"] = {
            "aspectRatio": aspect_ratio
        }

    print(f"Generating image...")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"Aspect ratio: {aspect_ratio}")

    response = requests.post(url, json=payload)
    data = response.json()

    if "error" in data:
        print(f"API Error: {data['error'].get('message', data['error'])}")
        return False

    if "candidates" not in data:
        print(f"Unexpected response: {data}")
        return False

    # Extract image from response
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
            size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
            print(f"Saved: {output_path} ({size_str})")
            return True

    print("Error: No image data in response")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini 2.5 Flash Image (Nano Banana)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Aspect ratios:
  1:1   Square (default)
  16:9  Horizontal (thumbnails, YouTube)
  9:16  Vertical (stories, TikTok, reels)
  4:3   Classic landscape
  3:4   Classic portrait

Examples:
  %(prog)s "A red apple" apple.png
  %(prog)s "YouTube thumbnail" thumb.png --aspect-ratio 16:9
  %(prog)s "TikTok cover" cover.png -a 9:16
        """
    )

    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("output", nargs="?", help="Output file path (default: /tmp/generated_image.png)")
    parser.add_argument("-a", "--aspect-ratio", default="1:1",
                        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
                        help="Image aspect ratio (default: 1:1)")

    args = parser.parse_args()

    # Generate default output path if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"/tmp/nanobanana_{timestamp}.png"

    success = generate_image(args.prompt, args.output, args.aspect_ratio)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
