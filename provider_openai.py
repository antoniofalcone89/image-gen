#!/usr/bin/env python3
"""
DALL-E 3 via OpenAI API
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from logo_config import LOGO_OUTPUT_DIR, get_logo_prompt, setup_logo_output_dir
from shared_config import OUTPUT_DIR, IMAGE_SIZE, get_prompt, setup_output_dir

load_dotenv()


def generate_openai(prompt: str, output_path: Path) -> dict:
    """DALL-E 3 via OpenAI API."""
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"status": "skipped", "reason": "OPENAI_API_KEY not set"}

    try:
        client = OpenAI()
        start = time.time()

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=f"{IMAGE_SIZE}x{IMAGE_SIZE}",
            quality="standard",
            n=1,
        )

        elapsed = time.time() - start
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        output_path.write_bytes(image_data)

        # DALL-E 3 sometimes revises your prompt — capture it
        revised_prompt = response.data[0].revised_prompt

        return {
            "status": "success",
            "time_seconds": round(elapsed, 1),
            "revised_prompt": revised_prompt,
            "cost_estimate": "$0.040",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


if __name__ == "__main__":
    from shared_config import TEST_ANIMALS
    
    #setup_output_dir()
    setup_logo_output_dir()

    prompt = get_logo_prompt()
    print(f"Generating logo with this prompt: {prompt}")
    time.sleep(1)
      # Small delay to ensure output directory is ready
    output_path = LOGO_OUTPUT_DIR / "logo_openai.png"
    if output_path.exists():
        counter = 1
        while True:
            candidate = LOGO_OUTPUT_DIR / f"logo_openai_{counter}.png"
            if not candidate.exists():
                output_path = candidate
                break
            counter += 1
    print(f"Generating logo with OpenAI...")
    result = generate_openai(prompt, output_path)
    print(f"Status: {result['status']}")
    if result["status"] == "success":
            print(f"Time: {result['time_seconds']}s")
            print(f"Cost: {result['cost_estimate']}")
            print(f"Output: {output_path}")
    else:
            print(f"Error: {result['reason']}")
    print()
    
    # for animal in TEST_ANIMALS:
    #     prompt = get_prompt(animal)
    #     output_path = OUTPUT_DIR / f"{animal}_openai.png"
        
    #     print(f"Generating image for {animal}...")
    #     result = generate_openai(prompt, output_path)
        
    #     print(f"Status: {result['status']}")
    #     if result["status"] == "success":
    #         print(f"Time: {result['time_seconds']}s")
    #         print(f"Cost: {result['cost_estimate']}")
    #         print(f"Output: {output_path}")
    #     else:
    #         print(f"Error: {result['reason']}")
    #     print()
