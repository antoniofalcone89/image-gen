#!/usr/bin/env python3
"""
Animals Quiz Academy — Image Provider Comparison Script

Generates the SAME animal image using all three providers so you can
compare style, quality, and consistency side by side.

Usage:
  1. Add your API keys to a .env file (see below)
  2. Run: python compare_providers.py
  3. Open the output folder and compare the results

You only need keys for the providers you want to test.
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
OUTPUT_DIR = Path("./comparison_output")
IMAGE_SIZE = 1024

# Test with multiple animals across different types for a fair comparison
TEST_ANIMALS = ["donkey"]
#TEST_ANIMALS = ["lion", "octopus", "donkey"]

PROMPT_TEMPLATE = (
    "Ultra-realistic close-up selfie of a clearly recognizable {animal} in a funny situation: {scenario}. "
    "Moderate wide-angle lens (not extreme fisheye), natural proportions without heavy distortion. "
    "The {animal} must be immediately identifiable for an animal trivia quiz."
    "The full head, ears, and key species features are clearly visible and anatomically accurate. "
    "Shot from slightly low angle, like a smartphone selfie. "
    "The {animal} is centered and fully identifiable at first glance. "
    "Bright natural daylight, blue sky with soft clouds in the background. If the animal has a distinctive habitat, include subtle hints of it in the background (e.g. savannah for lion, ocean for octopus). "
    "Sharp focus, detailed fur texture, realistic lighting and shadows. "
    "Playful and confident expression, but still realistic. "
    "Photorealistic wildlife photography style, high detail, high resolution."
)

NEGATIVE_PROMPT = (
    "extreme fisheye, heavy distortion, exaggerated nose, warped face, cartoon, illustration, "
    "3d render, pixar, disney, anime, unrealistic proportions, cropped ears, "
    "cut off head, blurry, low resolution, text, watermark"
)

# Funny scenarios for each test animal
TEST_SCENARIOS = {
    "donkey": "wearing stylish black sunglasses while standing in a sunny countryside field"
}


# ============================================================
# Providers
# ============================================================

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

        # Debug: Print initial prediction response
        print(f"DEBUG: Initial prediction response: {prediction}")

        # Poll for completion
        while prediction.get("status") not in ("succeeded", "failed", "canceled"):
            time.sleep(2)
            poll_url = prediction.get("urls", {}).get("get")
            if not poll_url:
                return {
                    "status": "error",
                    "reason": "Missing 'urls' in prediction response",
                    "response": prediction,  # Log the full prediction response for debugging
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


# ============================================================
# Runner
# ============================================================

PROVIDERS = {
    # "dalle3": generate_openai,
    # "stability": generate_stability,
    "replicate": generate_replicate,
}


def run_comparison():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Animals Quiz Academy — Provider Comparison")
    print("=" * 60)
    print(f"\n  Test animals : {', '.join(TEST_ANIMALS)}")
    print(f"  Providers    : {', '.join(PROVIDERS.keys())}")
    print(f"  Output       : {OUTPUT_DIR.resolve()}\n")

    results = {}

    for animal in TEST_ANIMALS:
        scenario = TEST_SCENARIOS.get(animal, "in a funny and endearing pose")
        prompt = PROMPT_TEMPLATE.format(animal=animal, scenario=scenario)
        print(f"── {animal.upper()} {'─' * (45 - len(animal))}")

        results[animal] = {}

        for provider_name, generate_fn in PROVIDERS.items():
            output_path = OUTPUT_DIR / f"{animal}_{provider_name}.png"

            print(f"  {provider_name:12s} → ", end="", flush=True)
            result = generate_fn(prompt, output_path)
            results[animal][provider_name] = result

            if result["status"] == "success":
                print(f"✅  {result['time_seconds']}s  {result['cost_estimate']}  → {output_path.name}")
            elif result["status"] == "skipped":
                print(f"⏭️   {result['reason']}")
            else:
                print(f"❌  {result['reason'][:80]}")

            time.sleep(0.5)

        print()

    # --- Summary ---
    print("=" * 60)
    print("  COMPARISON SUMMARY")
    print("=" * 60)

    for provider_name in PROVIDERS:
        successes = [r[provider_name] for r in results.values() if r[provider_name]["status"] == "success"]
        if successes:
            avg_time = sum(r["time_seconds"] for r in successes) / len(successes)
            cost = successes[0]["cost_estimate"]
            print(f"\n  {provider_name}:")
            print(f"    Generated : {len(successes)}/{len(TEST_ANIMALS)}")
            print(f"    Avg time  : {avg_time:.1f}s")
            print(f"    Cost/img  : {cost}")
        else:
            skipped = [r[provider_name] for r in results.values() if r[provider_name]["status"] == "skipped"]
            if skipped:
                print(f"\n  {provider_name}: SKIPPED (no API key)")
            else:
                print(f"\n  {provider_name}: ALL FAILED")

    total_cost = {
        "dalle3": "$0.040 × 3 = $0.12",
        # "stability": "$0.030 × 60 = $1.80",
        # "replicate": "$0.003 × 60 = $0.18",
    }

    #print(f"\n{'─' * 60}")
    #print("  PROJECTED COST FOR ALL 60 ANIMALS:")
    for p, c in total_cost.items():
        print(f"    {p:12s} : {c}")

    print(f"\n  📂 Open {OUTPUT_DIR.resolve()} to compare images side by side")
    print(f"     Files: {', '.join(f.name for f in sorted(OUTPUT_DIR.glob('*.png')))}")
    print()


if __name__ == "__main__":
    run_comparison()