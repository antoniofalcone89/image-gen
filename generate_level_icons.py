#!/usr/bin/env python3
"""
Generate level icon images for Animal Quiz Academy.

Each level gets one 1024×1024 photorealistic image saved locally.
After review, copy approved PNGs to animals-service/static/icons/.

Usage:
    python generate_level_icons.py                  # generate all 6 levels
    python generate_level_icons.py --level 1        # generate a single level
    python generate_level_icons.py --provider dalle3 --level 3
"""

import argparse
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("./icons_output")
IMAGE_SIZE = 1024

NEGATIVE_PROMPT = (
    "extreme fisheye, heavy distortion, exaggerated nose, warped face, cartoon, illustration, "
    "3d render, pixar, disney, anime, unrealistic proportions, cropped ears, "
    "cut off head, blurry, low resolution, text, watermark"
)

LEVEL_ICONS: dict[int, dict] = {
    1: {
        "filename": "level_farm_home.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable cow in a funny situation: "
            "sitting in a cozy armchair wearing reading glasses, holding a self-help book titled "
            "\"How to Stop Being Milked\", looking deeply offended yet dignified. "
            "The cow must be immediately identifiable for an animal trivia quiz. "
            "The cow's gaze must be ironic and funny. "
            "The full head, ears, and key species features are clearly visible and anatomically accurate. "
            "The cow is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of a farm in the background. "
            "Sharp focus, detailed hide texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    2: {
        "filename": "level_wild_icons.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable lion in a funny situation: "
            "wearing a tiny golden crown that keeps slipping over one eye, holding a scepter made "
            "of a stripped tree branch, looking simultaneously regal and embarrassed. "
            "The lion must be immediately identifiable for an animal trivia quiz. "
            "The lion's gaze must be ironic and funny. "
            "The full head, mane, ears, and key species features are clearly visible and anatomically accurate. "
            "The lion is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of the savannah in the background. "
            "Sharp focus, detailed fur texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    3: {
        "filename": "level_forest_garden.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable fox in a funny situation: "
            "sneaking through fallen autumn leaves with an oversized wedge of cheese tucked under "
            "one arm, glancing sideways with a smug self-satisfied expression. "
            "The fox must be immediately identifiable for an animal trivia quiz. "
            "The fox's gaze must be ironic and funny. "
            "The full head, ears, and key species features are clearly visible and anatomically accurate. "
            "The fox is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of an autumn forest in the background. "
            "Sharp focus, detailed fur texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    4: {
        "filename": "level_aquatic_wonders.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable octopus in a funny situation: "
            "simultaneously holding a phone, a coffee cup, a book, sunglasses, a pen, a tiny umbrella, "
            "a sandwich, and a small map with its eight arms, looking both overwhelmed and smugly proud "
            "of itself. "
            "The octopus must be immediately identifiable for an animal trivia quiz. "
            "The octopus's gaze must be ironic and funny. "
            "The full head, eyes, and all eight arms are clearly visible and anatomically accurate. "
            "The octopus is centered and fully identifiable at first glance. "
            "Bright natural daylight filtered through clear shallow water, blue sky visible above the "
            "surface in the background, subtle hints of a coral reef. "
            "Sharp focus, detailed skin texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    5: {
        "filename": "level_wilderness_exotics.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable toucan in a funny situation: "
            "trying with extreme concentration to balance a tall tower of colorful tropical fruits "
            "on its enormous bill, one eye closed, tongue slightly out in effort. "
            "The toucan must be immediately identifiable for an animal trivia quiz. "
            "The toucan's gaze must be ironic and funny. "
            "The full head, beak, and key species features are clearly visible and anatomically accurate. "
            "The toucan is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of a tropical rainforest canopy. "
            "Sharp focus, detailed feather texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    6: {
        "filename": "level_rare_hidden.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable pangolin in a funny situation: "
            "completely rolled into a tight ball wearing a tiny \"Do Not Disturb\" door sign hanging "
            "from one scale, one eye peeking open suspiciously at the camera. "
            "The pangolin must be immediately identifiable for an animal trivia quiz. "
            "The pangolin's visible eye must be ironic and funny. "
            "The distinctive overlapping scales and rolled body shape are clearly visible and "
            "anatomically accurate. The pangolin is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of a tropical forest floor. "
            "Sharp focus, detailed scale texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
    103: {
        "filename": "level_dino_world.png",
        "prompt": (
            "Ultra-realistic close-up picture of a clearly recognizable T-Rex in a funny situation: "
            "at a packed prehistoric rock concert, absolutely shredding an imaginary air guitar solo "
            "with full rock-star energy — head thrown back, eyes closed in passion — except its tiny "
            "arms can only wiggle uselessly a few centimetres from its body, nowhere near forming any "
            "guitar shape. A crowd of smaller dinosaurs in the background looks politely confused. "
            "The T-Rex must be immediately identifiable for an animal trivia quiz. "
            "The T-Rex's gaze must be ironic and funny. "
            "The full head, tiny arms, and key species features are clearly visible and anatomically accurate. "
            "The T-Rex is centered and fully identifiable at first glance. "
            "Bright natural daylight, blue sky with soft clouds in the background, "
            "subtle hints of a prehistoric fern landscape with distant volcanoes. "
            "Sharp focus, detailed skin texture, realistic lighting and shadows. "
            "Playful and confident expression, but still realistic. "
            "Photorealistic wildlife photography style, high detail, high resolution."
        ),
    },
}


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

def generate_dalle3(prompt: str, output_path: Path) -> dict:
    """DALL-E 3 via OpenAI API."""
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
        import base64
        image_bytes = base64.b64decode(response.data[0].b64_json)
        output_path.write_bytes(image_bytes)

        return {
            "status": "success",
            "time_seconds": round(elapsed, 1),
            "revised_prompt": None,
            "cost_estimate": "$0.040",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def generate_replicate(prompt: str, output_path: Path) -> dict:
    """Flux Schnell via Replicate API."""
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

        while prediction.get("status") not in ("succeeded", "failed", "canceled"):
            time.sleep(2)
            poll_url = prediction.get("urls", {}).get("get")
            if not poll_url:
                return {"status": "error", "reason": "Missing 'urls' in prediction response"}
            prediction = requests.get(poll_url, headers=headers).json()

        elapsed = time.time() - start

        if prediction["status"] == "succeeded":
            image_data = requests.get(prediction["output"][0]).content
            output_path.write_bytes(image_data)
            return {"status": "success", "time_seconds": round(elapsed, 1), "cost_estimate": "$0.003"}
        else:
            return {"status": "error", "reason": prediction.get("error", "Unknown error")}

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
            headers={"Authorization": f"Bearer {api_key}", "Accept": "image/*"},
            files={"none": ""},
            data={
                "model": "sd3.5-large",
                "prompt": prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "output_format": "png",
                "aspect_ratio": "1:1",
            },
        )

        elapsed = time.time() - start

        if response.status_code == 200:
            output_path.write_bytes(response.content)
            return {"status": "success", "time_seconds": round(elapsed, 1), "cost_estimate": "$0.030"}
        else:
            return {"status": "error", "reason": f"HTTP {response.status_code}: {response.text[:200]}"}

    except Exception as e:
        return {"status": "error", "reason": str(e)}


PROVIDERS = {
    "dalle3": generate_dalle3,
    "replicate": generate_replicate,
    "stability": generate_stability,
}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(level_ids: list[int], provider_name: str) -> None:
    generate_fn = PROVIDERS[provider_name]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Animal Quiz Academy — Level Icons")
    print("=" * 60)
    print(f"  Provider : {provider_name}")
    print(f"  Levels   : {level_ids}")
    print(f"  Output   : {OUTPUT_DIR.resolve()}\n")

    for level_id in level_ids:
        icon = LEVEL_ICONS[level_id]
        output_path = OUTPUT_DIR / icon["filename"]
        print(f"── Level {level_id} → {icon['filename']}")
        print(f"  {provider_name:12s} → ", end="", flush=True)

        result = generate_fn(icon["prompt"], output_path)

        if result["status"] == "success":
            print(f"✅  {result['time_seconds']}s  {result['cost_estimate']}  → {output_path.name}")
            if "revised_prompt" in result and result["revised_prompt"]:
                print(f"  revised    : {result['revised_prompt'][:120]}...")
        elif result["status"] == "skipped":
            print(f"⏭️   {result['reason']}")
        else:
            print(f"❌  {result['reason'][:100]}")

        print()

    print("=" * 60)
    print(f"  Done. Copy approved PNGs from {OUTPUT_DIR} to animals-service/static/icons/")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate level icon images.")
    parser.add_argument(
        "--level",
        type=int,
        choices=list(LEVEL_ICONS.keys()),
        help="Generate a single level (1–6). Omit to generate all.",
    )
    parser.add_argument(
        "--provider",
        choices=list(PROVIDERS.keys()),
        default="dalle3",
        help="Image provider to use (default: dalle3).",
    )
    args = parser.parse_args()

    level_ids = [args.level] if args.level else list(LEVEL_ICONS.keys())
    run(level_ids, args.provider)


if __name__ == "__main__":
    main()
