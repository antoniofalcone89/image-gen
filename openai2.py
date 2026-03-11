#!/usr/bin/env python3
"""
Multi-turn Image Generation via OpenAI Responses API
"""

import os
import time
import base64
from pathlib import Path
from dotenv import load_dotenv
from logo_config import LOGO_OUTPUT_DIR, get_logo_prompt, setup_logo_output_dir
from openai import OpenAI

load_dotenv()

client = OpenAI()


def generate_openai(prompt: str, output_path: Path) -> dict:
    """Generate an initial image using the OpenAI Responses API."""
    try:
        start = time.time()

        response = client.responses.create(
            model="dall-e-3",
            input=prompt,
            tools=[{"type": "image_generation"}],
        )

        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if not image_data:
            return {"status": "error", "reason": "No image generated in response"}

        output_path.write_bytes(base64.b64decode(image_data[0]))

        return {
            "status": "success",
            "time_seconds": round(time.time() - start, 1),
            "response_id": response.id,
            "cost_estimate": "$0.040",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def refine_image_openai(
    additional_prompt: str,
    output_path: Path,
    previous_response_id: str,
) -> dict:
    """Refine an existing image by continuing the conversation via previous_response_id."""
    try:
        start = time.time()

        response = client.responses.create(
            model="gpt-4o",
            previous_response_id=previous_response_id,
            input=additional_prompt,
            tools=[{"type": "image_generation"}],
        )

        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if not image_data:
            return {"status": "error", "reason": "No image generated in follow-up response"}

        output_path.write_bytes(base64.b64decode(image_data[0]))

        return {
            "status": "success",
            "time_seconds": round(time.time() - start, 1),
            "response_id": response.id,
            "cost_estimate": "$0.040",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def next_output_path(base_name: str = "logo_openai") -> Path:
    """Return the next available numbered output path in LOGO_OUTPUT_DIR."""
    candidate = LOGO_OUTPUT_DIR / f"{base_name}.png"
    counter = 1
    while candidate.exists():
        candidate = LOGO_OUTPUT_DIR / f"{base_name}_{counter}.png"
        counter += 1
    return candidate


if __name__ == "__main__":
    setup_logo_output_dir()

    prompt = get_logo_prompt()
    print(f"Prompt:\n{prompt}\n")

    # --- Turn 1: initial generation ---
    output_path = next_output_path("logo_openai")
    print(f"[Turn 1] Generating image → {output_path}")
    result = generate_openai(prompt, output_path)

    if result["status"] != "success":
        print(f"Failed: {result['reason']}")
        raise SystemExit(1)

    print(f"  Done in {result['time_seconds']}s  (response_id={result['response_id']})")

    # --- Turn 2: refinement ---
    refinement_prompt = (
        "The composition looks good. Now sharpen the details: "
        "make each animal's facial expression more vivid and expressive, "
        "increase the vibrancy of the colors, and ensure the globe continents "
        "are clearly visible with high contrast. Keep everything else the same."
    )

    refined_path = next_output_path("logo_openai_refined")
    print(f"[Turn 2] Refining image → {refined_path}")
    result2 = refine_image_openai(refinement_prompt, refined_path, result["response_id"])

    if result2["status"] != "success":
        print(f"Refinement failed: {result2['reason']}")
        raise SystemExit(1)

    print(f"  Done in {result2['time_seconds']}s  (response_id={result2['response_id']})")
    print(f"\nFinal outputs:\n  {output_path}\n  {refined_path}")
