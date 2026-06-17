#!/usr/bin/env python3
"""
DALL-E 3 via OpenAI API
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from shared_config import OUTPUT_DIR, IMAGE_SIZE, DINO_SCENARIOS, get_prompt, setup_output_dir

load_dotenv()


def generate_openai(prompt: str, output_path: Path) -> dict:
    """gpt-image-1 via OpenAI API."""
    import base64
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"status": "skipped", "reason": "OPENAI_API_KEY not set"}

    try:
        client = OpenAI()
        start = time.time()

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=f"{IMAGE_SIZE}x{IMAGE_SIZE}",
            quality="medium",
            n=1,
        )

        elapsed = time.time() - start
        image_data = base64.b64decode(response.data[0].b64_json)
        output_path.write_bytes(image_data)

        return {
            "status": "success",
            "time_seconds": round(elapsed, 1),
            "cost_estimate": "$0.042",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


if __name__ == "__main__":
    import sys

    setup_output_dir()

    animals = sys.argv[1:] if len(sys.argv) > 1 else list(DINO_SCENARIOS.keys())

    unknown = [a for a in animals if get_prompt(a) == get_prompt("__missing__")]
    if unknown:
        print(f"Warning: no scenario found for: {', '.join(unknown)} — using fallback prompt")

    total_cost = 0.042 * len(animals)
    print(f"Generating {len(animals)} image(s) (~${total_cost:.2f} estimated)\n")

    for animal in animals:
        prompt = get_prompt(animal)
        output_path = OUTPUT_DIR / f"{animal}_openai.png"

        print(f"Generating {animal}...")
        result = generate_openai(prompt, output_path)

        if result["status"] == "success":
            print(f"  ✓ {result['time_seconds']}s — {output_path}")
        else:
            print(f"  ✗ {result['reason']}")

    print(f"\nDone. Images saved to {OUTPUT_DIR}/")
