"""Stable Diffusion 3.5 (Stability AI) provider — import and call generate_stability()."""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from shared_config import NEGATIVE_PROMPT

load_dotenv()


def generate_stability(prompt: str, output_path: Path) -> dict:
    """Stable Diffusion 3.5 via Stability AI API."""
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        return {"status": "skipped", "reason": "STABILITY_API_KEY not set"}

    try:
        start = time.time()

        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "image/*",
            },
            files={"none": ""},
            data={
                "model": "sd3.5-large",
                "prompt": prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "output_format": "jpeg",
                "aspect_ratio": "1:1",
            },
        )

        elapsed = time.time() - start

        if response.status_code == 200:
            output_path.write_bytes(response.content)
            return {
                "status": "success",
                "time_seconds": round(elapsed, 1),
                "cost_estimate": "$0.030",
            }
        else:
            return {"status": "error", "reason": f"HTTP {response.status_code}: {response.text[:200]}"}

    except Exception as e:
        return {"status": "error", "reason": str(e)}


