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

PROMPT_TEMPLATE = (
    "Ultra-realistic close-up picture of a clearly recognizable {animal} in a funny situation: {scenario}. "
    "The {animal} must be immediately identifiable for an animal trivia quiz. "
    "The {animal}'s gaze must be ironic and funny. "
    "The full head, ears, and key species features are clearly visible and anatomically accurate. "
    "The {animal} is centered and fully identifiable at first glance. "
    "Bright natural daylight, blue sky with soft clouds in the background. If the animal has a distinctive habitat, include subtle hints of it in the background (e.g. savannah for lion, ocean for octopus). "
    "Sharp focus, detailed fur texture, realistic lighting and shadows. "
    "Playful and confident expression, but still realistic. "
    "Photorealistic wildlife photography style, high detail, high resolution."
)

NEGATIVE_PROMPT = (
    "extreme fisheye, heavy distortion, exaggerated nose, warped face, cartoon, illustration, "
    "3d render, pixar, disney, anime, unrealistic proportions, cropped ears, "
    "cut off head, blurry, low resolution, text, watermark, labels, name tags, writing, letters, words"
)

# ---------------------------------------------------------------------------
# Scenario + group loading — driven entirely by scenarios/*.json files.
# Each JSON file is a flat dict mapping animal name → funny scenario string.
# The filename (without extension) becomes the group name.
# To add a new group: create scenarios/<group_name>.json — no code changes needed.
# ---------------------------------------------------------------------------

import json as _json

SCENARIOS_DIR = Path(__file__).parent / "scenarios"

GROUPS: dict[str, dict[str, str]] = {
    path.stem: _json.loads(path.read_text(encoding="utf-8"))
    for path in sorted(SCENARIOS_DIR.glob("*.json"))
}

_ALL_SCENARIOS: dict[str, str] = {
    animal: scenario
    for group in GROUPS.values()
    for animal, scenario in group.items()
}

# ---------------------------------------------------------------------------
# Legacy aliases kept for backwards compatibility with provider scripts
# ---------------------------------------------------------------------------
TEST_SCENARIOS = GROUPS.get("main", {})
DINO_SCENARIOS = GROUPS.get("dino", {})



def get_prompt(animal: str) -> str:
    """Generate a prompt for an animal."""
    scenario = _ALL_SCENARIOS.get(animal, "in a funny and endearing pose")
    return PROMPT_TEMPLATE.format(animal=animal, scenario=scenario)


def setup_output_dir() -> Path:
    """Create and return the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
