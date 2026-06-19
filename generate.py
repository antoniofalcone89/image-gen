#!/usr/bin/env python3
"""Single entry point for animal image generation across all providers."""

import argparse
from pathlib import Path
from dotenv import load_dotenv
from shared_config import GROUPS, get_prompt
from logo_config import LOGOS, LOGO_OUTPUT_DIR, get_logo_prompt

load_dotenv()

PROVIDERS = {
    "openai":     {"cost": 0.042},
    "replicate":  {"cost": 0.003},
    "stability":  {"cost": 0.030},
}


def _load_provider(name: str):
    if name == "openai":
        from provider_openai import generate_openai
        return generate_openai
    if name == "replicate":
        from provider_replicate import generate_replicate
        return generate_replicate
    if name == "stability":
        from provider_stability import generate_stability
        return generate_stability
    raise ValueError(f"Unknown provider: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate animal images via AI providers")
    parser.add_argument(
        "--provider",
        choices=list(PROVIDERS.keys()),
        default="openai",
        help="Image generation provider (default: openai)",
    )
    parser.add_argument(
        "--group",
        choices=list(GROUPS.keys()),
        help="Animal group to generate",
    )
    parser.add_argument(
        "--logo",
        choices=list(LOGOS.keys()),
        metavar="LEVEL",
        help=f"Generate a level logo ({', '.join(LOGOS.keys())})",
    )
    parser.add_argument(
        "animals",
        nargs="*",
        help="One or more animal names within the group (generates all if omitted)",
    )
    args = parser.parse_args()

    if not args.logo and not args.group:
        parser.error("one of --group or --logo LEVEL is required")

    generate = _load_provider(args.provider)

    if args.logo:
        LOGO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = LOGO_OUTPUT_DIR / f"{args.logo}.png"
        print(f"Provider: {args.provider} | Logo: {args.logo} (~${PROVIDERS[args.provider]['cost']:.3f} estimated)\n")
        result = generate(get_logo_prompt(args.logo), output_path)
        if result["status"] == "success":
            print(f"  ✓ {result['time_seconds']}s — {output_path}")
        else:
            print(f"  ✗ {result['reason']}")
        return

    group_animals = list(GROUPS[args.group].keys())
    if args.animals:
        unknown = [a for a in args.animals if a not in group_animals]
        if unknown:
            parser.error(f"Not in group '{args.group}': {', '.join(unknown)}")
        animals = args.animals
    else:
        animals = group_animals

    output_dir = Path(__file__).parent / args.group
    output_dir.mkdir(parents=True, exist_ok=True)

    total_cost = PROVIDERS[args.provider]["cost"] * len(animals)
    print(f"Provider: {args.provider} | Group: {args.group} | {len(animals)} image(s) (~${total_cost:.2f} estimated)\n")

    for animal in animals:
        output_path = output_dir / f"{animal}.png"
        print(f"Generating {animal}...")
        result = generate(get_prompt(animal), output_path)
        if result["status"] == "success":
            print(f"  ✓ {result['time_seconds']}s — {output_path}")
        else:
            print(f"  ✗ {result['reason']}")

    print(f"\nDone. Images saved to {output_dir}/")


if __name__ == "__main__":
    main()
