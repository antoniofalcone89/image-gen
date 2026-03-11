"""
Configuration for generating the Animal Quiz Academy app logo.
"""

# Logo generation prompt
LOGO_PROMPT = (
    "High-quality animated-style logo illustration of a globe-shaped miniature world under a clear blue daytime sky, during the day. "
    "with charismatic animals standing playfully on top of the globe. "
    "It is clearly daytime, but the sun MUST NOT be visible in the frame. "
    "There are NO stars, NO outer space, NO galaxy background. "
    "The animals have expressive, slightly exaggerated but detailed facial features, "
    "big engaging eyes, confident and mischievous expressions, similar energy to animated adventure movies. "
    "They are posing in funny, dynamic positions: one leaning forward toward the viewer, "
    "one balancing dramatically, one laughing, one striking a heroic pose. "
    "The globe is detailed with visible continents. "
    "Cinematic lighting, vibrant colors, high contrast, polished 3D animated film style, "
    "clean composition suitable for a mobile app logo, centered framing, high resolution, "
    "sharp details, professional branding quality.  Each animal one MUST be a different species. "
    "Use only these animals: 1 giraffe, 1 zebra, 1 hippo, and 1 lion, 1 cow, 1 sheep, no others. "
    "The overall vibe should be adventurous, and inviting for a trivia quiz app about animals. "
)

LOGO_PROMPT2 = """
Logo illustration.

A globe-shaped miniature Earth under a clear light blue daytime sky.

On top of the globe there are exactly four animals:
- one giraffe
- one zebra
- one hippo
- one lion

Only these four animals are visible.
No other animals exist in the image.

The giraffe is leaning forward toward the viewer.
The zebra is laughing and slightly leaning sideways.
The hippo is balancing near the edge of the globe.
The lion is standing in a confident heroic pose.

Bright daytime lighting.
The sun is not visible.
No stars.
No space.
No galaxy background.

Clean composition.
Centered.
Professional 3D animated movie style.
Vibrant colors.
Suitable for a mobile app logo.
"""

# Negative prompt for logo generation
LOGO_NEGATIVE_PROMPT = (
    "extra animals, duplicate animals, repeated species, more than four animals, nonexisting animals, invented animals, "
    "sun, sunset, sunrise, night sky, stars, galaxy, outer space, cosmic background, "
    "low resolution, blurry, flat design, minimalist icon, simple vector, childish drawing, "
    "ugly proportions, distorted faces, extra limbs, mutated animals, horror, scary, "
    "dark gritty realism, photorealistic wildlife photo, watermark, text, logo mockup, "
    "grainy texture, dull colors, cluttered composition"
)

# Alternative logo concepts to try
LOGO_CONCEPT = (
    "One giraffe stretching its neck forward toward the viewer, "
    "one zebra leaning sideways laughing, "
    "one hippo balancing near the edge of the globe, "
    "and one lion standing proudly in a heroic pose, "
    "all standing together on top of the globe, "
    "with a light sky on the background."
)


# --- Utility Functions ---

from pathlib import Path

# Output directory for logos
LOGO_OUTPUT_DIR = Path("./logo_output")


# def get_logo_prompt() -> str:
#     return (
#         f"{LOGO_PROMPT2}\n\n"
#         "The image must contain four animals only. "
#         "If more animals appear, the image is incorrect.\n\n"
#         f"Avoid: {LOGO_NEGATIVE_PROMPT}"
#     )

LOGO_PROMPT3 = """Wide bottom banner image for a mobile app screen.
Fun, colorful cartoon animals in cute and cool poses: a smiling lion wearing sunglasses, a playful monkey hanging upside down, a frog winking, a dancing penguin, and a dolphin jumping.
The animals are arranged in a horizontal composition, slightly overlapping.
Madagascar-inspired design, high detail, expressive faces, engaging mood, funny behaviours.
Clean, modern.
No text, no landmarks, no logos, no background (transparent PNG)."""

def get_logo_prompt() -> str:
    return (
        f"{LOGO_PROMPT3}\n"
    )


def setup_logo_output_dir() -> Path:
    """Create and return the logo output directory."""
    LOGO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return LOGO_OUTPUT_DIR
