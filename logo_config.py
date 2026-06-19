"""Logo configuration — loads prompts from logos.json, one entry per level."""

import json
from pathlib import Path

LOGOS_FILE = Path(__file__).parent / "logos.json"
LOGO_OUTPUT_DIR = Path(__file__).parent / "logo_output"

LOGOS: dict[str, dict] = json.loads(LOGOS_FILE.read_text(encoding="utf-8"))


def get_logo_prompt(level: str) -> str:
    """Return the full prompt for the given level logo."""
    if level not in LOGOS:
        available = ", ".join(LOGOS.keys())
        raise ValueError(f"Unknown logo level '{level}'. Available: {available}")
    entry = LOGOS[level]
    prompt = entry["prompt"]
    negative = entry.get("negative_prompt", "")
    return f"{prompt} Negative prompt: {negative}" if negative else prompt
