#!/usr/bin/env python3
"""Generate the Play Store feature graphic for Animals Quiz Academy (1024x500px)."""

import base64
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import io

load_dotenv()

OUTPUT_PATH = Path(__file__).parent / "logo_output" / "feature_graphic.png"

PROMPT = (
    "Wide panoramic banner illustration in the exact style of the Madagascar animated movie — "
    "bright 3D cartoon characters, thick outlines, vivid saturated colors, big glossy expressive eyes, "
    "huge toothy smiles, and exaggerated funny poses. "

    "A sunny tropical beach scene: bright blue ocean with gentle waves, golden sand, two palm trees, "
    "a big cheerful sun in a blue sky with fluffy white clouds. "
    "Five cartoon animals standing together on the beach, all laughing and posing joyfully: "

    "(1 — far left) A cartoon lion wearing a tiny gold crown that is sliding off its head mid-sneeze, "
    "eyes squeezed shut, mane blown sideways, expression of hilarious royal embarrassment. "

    "(2 — left of center) A cartoon elephant standing on its tiptoes, "
    "eyes bugging out in exaggerated terror, trunk shot straight up in the air, "
    "staring down at a teeny tiny mouse sitting calmly on the sand below it. "
    "Classic comedic size contrast. "

    "(3 — center, tallest) A cartoon giraffe wearing oversized cool sunglasses, "
    "neck zigzagging playfully, big cheesy grin, one leg raised mid-dance. "

    "(4 — right of center) A cartoon penguin with bright orange inflatable arm floaties, "
    "chest puffed out, chin raised, striding with ridiculous unearned confidence, huge smug grin. "

    "(5 — far right) A cartoon monkey in a tiny business suit, "
    "holding a tiny briefcase, looking totally baffled at a banana that is somehow also wearing a suit. "

    "All animals have large expressive cartoon eyes, rosy cheeks, and are clearly having a fantastic time. "
    "Bright primary colors, clean cel-shaded look, joyful summer energy. "
    "Composition is very wide and horizontal, all animals visible from head to toe. "
    "No text, no watermarks, no letters."
)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set in .env")
        return

    client = OpenAI()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Generating feature graphic at 1536x1024 (will crop to 1024x500)...")
    start = time.time()

    response = client.images.generate(
        model="gpt-image-1",
        prompt=PROMPT,
        size="1536x1024",
        quality="high",
        n=1,
    )

    elapsed = time.time() - start
    image_data = base64.b64decode(response.data[0].b64_json)

    # Crop to 2.048:1 ratio first (removes only sky/sand at top+bottom margins),
    # then scale proportionally to 1024x500 — no content distortion.
    img = Image.open(io.BytesIO(image_data))
    w, h = img.size  # 1536x1024
    target_h = int(w / (1024 / 500))  # = 750
    top = (h - target_h) // 2
    cropped = img.crop((0, top, w, top + target_h))  # full width, crop sky/sand only
    final = cropped.resize((1024, 500), Image.LANCZOS)
    final.save(OUTPUT_PATH, "PNG")

    print(f"Done in {round(elapsed, 1)}s — saved to {OUTPUT_PATH}")
    print(f"Size: {final.size[0]}x{final.size[1]}px")


if __name__ == "__main__":
    main()
