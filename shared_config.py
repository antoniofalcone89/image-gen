"""
Shared configuration and utilities for image generation providers.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
OUTPUT_DIR = Path("./comparison_output")
IMAGE_SIZE = 1024

# Test with multiple animals across different types for a fair comparison
TEST_ANIMALS = ["donkey"]
# TEST_ANIMALS = ["lion", "octopus", "donkey"]

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


def get_prompt(animal: str) -> str:
    """Generate a prompt for an animal."""
    scenario = TEST_SCENARIOS.get(animal, "in a funny and endearing pose")
    return PROMPT_TEMPLATE.format(animal=animal, scenario=scenario)


def setup_output_dir() -> Path:
    """Create and return the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
