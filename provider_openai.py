"""DALL-E 3 (gpt-image-1) provider — import and call generate_openai()."""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from shared_config import IMAGE_SIZE

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


