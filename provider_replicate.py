#!/usr/bin/env python3
"""
Flux Schnell via Replicate API (fast & cheap)
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from shared_config import OUTPUT_DIR, get_prompt, setup_output_dir

load_dotenv()


def generate_replicate(prompt: str, output_path: Path) -> dict:
    """Flux Schnell via Replicate API (fast & cheap)."""
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        return {"status": "skipped", "reason": "REPLICATE_API_TOKEN not set"}

    try:
        start = time.time()
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
            headers=headers,
            json={
                "input": {
                    "prompt": prompt,
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "png",
                },
            },
        )

        prediction = response.json()

        # Poll for completion
        while prediction.get("status") not in ("succeeded", "failed", "canceled"):
            time.sleep(2)
            poll_url = prediction.get("urls", {}).get("get")
            if not poll_url:
                return {
                    "status": "error",
                    "reason": "Missing 'urls' in prediction response",
                    "response": prediction,
                }

            poll = requests.get(poll_url, headers=headers)
            prediction = poll.json()

        elapsed = time.time() - start

        if prediction["status"] == "succeeded":
            image_url = prediction["output"][0]
            image_data = requests.get(image_url).content
            output_path.write_bytes(image_data)
            return {
                "status": "success",
                "time_seconds": round(elapsed, 1),
                "cost_estimate": "$0.003",
            }
        else:
            return {"status": "error", "reason": prediction.get("error", "Unknown error")}

    except Exception as e:
        return {"status": "error", "reason": str(e)}


if __name__ == "__main__":
    from shared_config import TEST_ANIMALS
    
    setup_output_dir()
    
    for animal in TEST_ANIMALS:
        prompt = get_prompt(animal)
        output_path = OUTPUT_DIR / f"{animal}_replicate.png"
        
        print(f"Generating image for {animal}...")
        result = generate_replicate(prompt, output_path)
        
        print(f"Status: {result['status']}")
        if result["status"] == "success":
            print(f"Time: {result['time_seconds']}s")
            print(f"Cost: {result['cost_estimate']}")
            print(f"Output: {output_path}")
        else:
            print(f"Error: {result['reason']}")
        print()
