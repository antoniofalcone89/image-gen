"""
Configuration for generating the Animals Quiz Academy app logo.
"""

# Logo generation prompt
LOGO_PROMPT = (
    "High-quality animated-style logo illustration of a globe-shaped miniature world under a clear blue daytime sky, during the day (so with bright sunlight and clear skies) "
    "with a small group of charismatic animals standing playfully on top of the globe. "
    "It is clearly daytime, but the sun is NOT visible in the frame, but the lighting should suggest it's daytime, with a clear blue sky. "
    "There are NO stars, NO sun, NO outer space, NO galaxy background. "
    "The sun MUST NOT be visible in the frame, but the lighting should suggest it's daytime, with a clear blue sky. "
    "The animals have expressive, slightly exaggerated but detailed facial features, "
    "big engaging eyes, confident and mischievous expressions, similar energy to animated adventure movies. "
    "They are posing in funny, dynamic positions: one leaning forward toward the viewer, "
    "one balancing dramatically, one laughing, one striking a heroic pose. "
    "The globe is detailed with visible continents. "
    "Cinematic lighting, vibrant colors, high contrast, polished 3D animated film style, "
    "clean composition suitable for a mobile app logo, centered framing, high resolution, "
    "sharp details, professional branding quality. Do NOT duplicate the same animal, each one MUST be a different species. "
    "Use a giraffe, a zebra, a hippo, and a lion. The overall vibe should be funny, adventurous, and inviting for a trivia quiz app about animals. "
)

# Negative prompt for logo generation
LOGO_NEGATIVE_PROMPT = (
    "low resolution, blurry, flat design, minimalist icon, simple vector, childish drawing, "
    "ugly proportions, distorted faces, extra limbs, mutated animals, horror, scary, "
    "dark gritty realism, photorealistic wildlife photo, watermark, text, logo mockup, "
    "grainy texture, dull colors, cluttered composition"
)

# Alternative logo concepts to try
LOGO_CONCEPT = (
    "a giraffe stretching its neck forward toward the viewer, "
    "a zebra leaning sideways laughing, "
    "a hippo balancing near the edge of the globe, "
    "and a lion standing proudly in a heroic pose, "
    "all standing together on top of the globe, "
    "with a light sky on the background."
)


# --- Utility Functions ---

from pathlib import Path

# Output directory for logos
LOGO_OUTPUT_DIR = Path("./logo_output")


def get_logo_prompt() -> str:
    """
    Generate the full logo prompt.
    
    Returns:
        The complete logo prompt string.
    """
    negative_guidelines = f"Negative prompt: {LOGO_NEGATIVE_PROMPT}. "
    concept = f"Specific concept: {LOGO_CONCEPT}. "
    base_prompt = f"{LOGO_PROMPT} {negative_guidelines} {concept}"

    return base_prompt


def setup_logo_output_dir() -> Path:
    """Create and return the logo output directory."""
    LOGO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return LOGO_OUTPUT_DIR
