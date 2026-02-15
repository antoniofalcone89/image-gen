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
TEST_ANIMALS = ["Owl"]
# TEST_ANIMALS = ["Chicken", "Pig", "Penguin"]

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
    "cut off head, blurry, low resolution, text, watermark"
)

# Funny scenarios for each test animal
TEST_SCENARIOS = {
    "Donkey": "wearing stylish black sunglasses while standing in a sunny countryside field",
    "Dog": "wearing a tiny, perfectly fitted tuxedo and blowing a giant pink bubblegum bubble",
    "Cat": "wearing a professional scuba mask while staring intensely into a goldfish bowl",
    "Chicken": "wearing a fancy pearl necklace and looking incredibly posh and superior",
    "Cow": "wearing oversized, flashy gold hoop earrings instead of yellow identification tags",
    "Sheep": "with its wool styled into a perfect, massive 1970s afro haircut",
    "Pig": "wearing a fancy silk bib and using a silver fork to eat a giant slice of watermelon",
    "Horse": "wearing a professional office headset and looking focused as if working in a call center",
    "Goat": "defiantly chewing on a colorful 'No Trespassing' sign with a smug expression",
    "Duck": "wearing a tiny bright yellow raincoat and matching miniature Wellington boots",
    "Pigeon": "wearing a tiny black beret and carrying a miniature baguette under its wing",
    "Sparrow": "wearing a tiny hand-knitted woolen scarf and earmuffs while looking grumpy",
    "Rat": "wearing a white chef's hat and tasting soup from a tiny silver spoon",
    "Fox": "looking utterly disgusted with a wrinkled nose while trying to eat a bunch of green grapes",
    "Deer": "with a laundry line and several colorful socks accidentally tangled in its antlers",
    "Rabbit": "wearing a monocle and checking a tiny gold pocket watch with a worried look",
    "Squirrel": "wearing a tiny leather aviator helmet and goggles, ready for takeoff",
    "Raccoon": "wearing a formal tuxedo and holding a fancy crystal cocktail glass",
    "Hedgehog": "wearing a tiny thimble as a hat and sitting inside a colorful ceramic teacup",
    "Badger": "wearing a yellow construction hard hat while intensely inspecting a hole in the ground",
    "Coyote": "sitting at a dinner table with a napkin tucked into its collar, holding a knife and fork",
    "Eagle": "wearing classic aviator sunglasses and looking like a confident fighter pilot",
    "Owl": "wearing thick, round academic glasses and a graduation cap while looking stern",
    "Beaver": "wearing a tool belt and holding a complex blueprint roll while looking at a log",
    "Flamingo": "wearing a single bright pink roller skate on its standing leg",
    "Red Panda": "trying to meditate in a perfect lotus pose with its paws together and eyes closed",
    "Koala": "hugging a giant 'Eucalyptus' flavored lollipop instead of a tree branch",
    "Penguin": "wearing bright orange inflatable arm floaties while waddling across the ice",
    "Otter": "using a flat river stone as a dinner plate for a tiny, fancy seafood meal",
    "Sloth": "wearing a gold medal that says 'World's Fastest Runner' around its neck",
    "Chameleon": "holding a tiny paint palette and a brush, looking confused at its own changing colors",
    "Porcupine": "with several colorful party balloons safely tied to the tips of its quills",
    "Toucan": "wearing a pair of giant novelty glasses with a fake nose and mustache on its beak",
    "Capybara": "wearing a tiny golden crown while sitting on a 'throne' made of hay",
    "Manta Ray": "wearing a black bow tie and a monocle while gliding underwater",
    "Platypus": "wearing a Sherlock Holmes deerstalker hat and holding a magnifying glass",
    "Seahorse": "wearing a tiny miniature leather saddle with stirrups on its back",
    "Armadillo": "wearing a green turtle-shell backpack, trying to blend in with turtles",
    "Wolf": "wearing a pink floral grandmother's nightcap and reading glasses",
    "Snow Leopard": "wearing a colorful knitted woolly hat with a giant pom-pom",
    "Pangolin": "wearing a miniature medieval knight's helmet that matches its scales",
    "Axolotl": "wearing a tiny party hat and blowing a paper party noisemaker underwater",
    "Narwhal": "with a colorful 'Ring Toss' game hoop perfectly caught on its tusk",
    "Okapi": "wearing striped knee-high socks that match its leg patterns exactly",
    "Clouded Leopard": "wearing a beige detective trench coat while peeking through jungle leaves",
    "Quokka": "holding a small cardboard sign that says 'Free Hugs' with a huge smile",
    "Cassowary": "wearing a neon 'Safety First' reflective vest while crossing a forest path",
    "Gharial": "with a perfect row of five tiny yellow rubber ducks sitting on its long snout",
    "Saola": "wearing a gold medal for 'Hide and Seek World Champion'",
    "Fossa": "wearing a headband with fuzzy cat ears while looking very serious",
    "Aye-Aye": "playing a tiny, delicate violin with its exceptionally long middle finger",
    "Numbat": "wearing a white lab coat and holding a 'Termite Specialist' clipboard",
    "Dugong": "wearing a colorful Hawaiian flower lei while floating underwater",
    "Kakapo": "wearing an old-fashioned leather pilot's helmet with wings on the sides",
    "Vaquita": "wearing a 'VIP' (Very Important Porpoise) gold lanyard around its neck",
    "Javan Rhino": "wearing a t-shirt that says 'One of a Kind' in bold letters",
    "Philippine Eagle": "wearing a tiny, majestic gold crown on its feathered head",
    "Amur Leopard": "wearing a 'Ski Instructor' badge and a colorful winter scarf",
    "Sumatran Orangutan": "holding a large tropical leaf like an umbrella and carrying a briefcase",
    "Red Wolf": "wearing a bright red bandana and looking like a cool biker",
    "Yangtze Finless Porpoise": "wearing a headband with a 'Smile' emoji on it",
    "Northern Hairy-Nosed Wombat": "wearing a pair of fuzzy pink bunny ears headbands",
    "Cross River Gorilla": "wearing a formal suit jacket and a striped necktie",
    "Hainan Gibbon": "wearing a bright leotard like a professional Olympic gymnast",
    "Frog": "sitting on a lily pad with a wide grin showing perfectly white human teeth",
    "Crane": "looking frustrated while trying to drink from a very narrow, tall clay amphora",
    "Ant": "visibly sweating and panting while carrying a massive slice of strawberry cake",
    "Cricket": "standing on a leaf while passionately playing a miniature mandolin"
}


def get_prompt(animal: str) -> str:
    """Generate a prompt for an animal."""
    scenario = TEST_SCENARIOS.get(animal, "in a funny and endearing pose")
    return PROMPT_TEMPLATE.format(animal=animal, scenario=scenario)


def setup_output_dir() -> Path:
    """Create and return the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
