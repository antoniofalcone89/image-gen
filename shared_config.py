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

# Funny scenarios for each test animal (merged from all sources)
TEST_SCENARIOS = {
    "Alpaca": "with its fleece styled into a perfect, tall white chef's hat, holding a tiny silver whisk",
    "Amur Leopard": "wearing a 'Ski Instructor' badge and a colorful winter scarf",
    "Ant": "visibly sweating and panting while carrying a massive slice of strawberry cake",
    "Arctic Fox": "wearing a bright red scarf and matching boots, standing out perfectly against the white snow",
    "Armadillo": "wearing a green turtle-shell backpack, trying to blend in with turtles",
    "Axolotl": "wearing a tiny party hat and blowing a paper party noisemaker underwater",
    "Aye-Aye": "playing a tiny, delicate violin with its exceptionally long middle finger",
    "Badger": "wearing a yellow construction hard hat while intensely inspecting a hole in the ground",
    "Bat": "wearing tiny silk pajamas and holding a miniature stuffed teddy bear while hanging upside down",
    "Beaver": "wearing a tool belt and holding a complex blueprint roll while looking at a log",
    "Bee": "wearing a tiny high-visibility yellow safety vest and carrying a miniature clipboard, looking stressed",
    "Butterfly": "applying bright red lipstick to its proboscis while looking into a tiny dewdrop mirror",
    "Camel": "wearing a colorful Hawaiian shirt and three different cameras around its neck, looking like a lost tourist",
    "Capybara": "wearing a tiny golden crown while sitting on a 'throne' made of hay",
    "Cassowary": "wearing a neon 'Safety First' reflective vest while crossing a forest path",
    "Cat": "wearing a professional scuba mask while staring intensely into a goldfish bowl",
    "Chameleon": "holding a tiny paint palette and a brush, looking confused at its own changing colors",
    "Chicken": "wearing a fancy pearl necklace and looking incredibly posh and superior",
    "Chipmunk": "with cheeks so full of acorns they look like giant balloons, wearing a 'Winner' gold medal",
    "Clouded Leopard": "wearing a beige detective trench coat while peeking through jungle leaves",
    "Clownfish": "wearing a tiny red foam clown nose and oversized colorful shoes on its fins",
    "Cow": "wearing oversized, flashy gold hoop earrings instead of yellow identification tags",
    "Coyote": "sitting at a dinner table with a napkin tucked into its collar, holding a knife and fork",
    "Crab": "wearing tiny red boxing gloves on its claws and posing in a classic fighting stance",
    "Crane": "looking frustrated while trying to drink from a very narrow, tall clay amphora",
    "Cricket": "standing on a leaf while passionately playing a miniature mandolin",
    "Crocodile": "with green cucumber slices on its eyes while relaxing in a bathtub filled with swamp water",
    "Cross River Gorilla": "wearing a formal suit jacket and a striped necktie",
    "Deer": "with a laundry line and several colorful socks accidentally tangled in its antlers",
    "Dog": "wearing a tiny, perfectly fitted tuxedo and blowing a giant pink bubblegum bubble",
    "Dolphin": "wearing retro 80s neon headphones and a sweatband, looking like it's doing an underwater aerobics class",
    "Donkey": "wearing stylish black sunglasses while standing in a sunny countryside field",
    "Dragonfly": "wearing oversized aviator goggles and a tiny leather pilot's jacket, looking like an ace pilot",
    "Duck": "wearing a tiny bright yellow raincoat and matching miniature Wellington boots",
    "Dugong": "wearing a colorful Hawaiian flower lei while floating underwater",
    "Eagle": "wearing classic aviator sunglasses and looking like a confident fighter pilot",
    "Eel": "looking like a neon glow-stick and accidentally tied in a complex knot with itself",
    "Elephant": "wearing a tiny, struggling pink tutu while trying to balance on one leg on a very small, squashed wooden stool",
    "Fennec Fox": "wearing huge, oversized noise-canceling earmuffs that can barely fit over its giant ears",
    "Flamingo": "wearing a single bright pink roller skate on its standing leg",
    "Fossa": "wearing a headband with fuzzy cat ears while looking very serious",
    "Fox": "looking utterly disgusted with a wrinkled nose while trying to eat a bunch of green grapes",
    "Frog": "sitting on a lily pad with a wide grin showing perfectly white human teeth",
    "Gharial": "with a perfect row of five tiny yellow rubber ducks sitting on its long snout",
    "Giraffe": "wearing twenty different colorful woolly scarves stacked all the way up its neck, looking very cozy",
    "Goat": "defiantly chewing on a colorful 'No Trespassing' sign with a smug expression",
    "Goldfish": "wearing a tiny detective trench coat and hat, holding a magnifying glass against the glass of its bowl",
    "Goose": "wearing a 'Security' vest and aggressively guarding a single, tiny, shiny gold coin on the grass",
    "Gorilla": "wearing thick reading glasses and looking with extreme tenderness at a tiny, delicate origami bird in its huge hands",
    "Guinea Pig": "wearing a tiny three-piece suit and sitting at a miniature desk with a tiny laptop",
    "Hainan Gibbon": "wearing a bright leotard like a professional Olympic gymnast",
    "Hamster": "wearing a tiny superhero cape and standing heroically on top of a giant, mountain-like pile of sunflower seeds",
    "Hedgehog": "wearing a tiny thimble as a hat and sitting inside a colorful ceramic teacup",
    "Hippo": "wearing a bright pink swimming cap and a floral vintage swimsuit, ready to dive into a pool",
    "Horse": "wearing a professional office headset and looking focused as if working in a call center",
    "Husky": "wearing a tropical flower lei and sunglasses while sitting directly in front of a giant electric fan",
    "Hyena": "wearing a bowtie and holding a '101 Jokes' book, looking like it just told a terrible pun",
    "Iguana": "wearing a tiny leather biker jacket and miniature sunglasses, looking like a cool rebel",
    "Jaguar": "wearing a 'high-visibility' neon orange vest while trying to 'stealthily' hunt in the green jungle",
    "Javan Rhino": "wearing a t-shirt that says 'One of a Kind' in bold letters",
    "Jellyfish": "wearing a bright '70s disco afro wig and glowing like a neon lamp under the sea",
    "Jerboa": "using its long, thin back legs to balance on top of a single, giant basketball",
    "Kakapo": "wearing an old-fashioned leather pilot's helmet with wings on the sides",
    "Koala": "hugging a giant 'Eucalyptus' flavored lollipop instead of a tree branch",
    "Ladybug": "wearing a tiny backpack and holding a miniature map, looking confused at a giant blade of grass",
    "Lemming": "wearing a tiny parachute and looking very hesitant and nervous at the edge of a small puddle",
    "Lion": "sitting in a professional barber chair with its mane covered in colorful plastic curlers, reading a magazine",
    "Llama": "wearing oversized, colorful headphones and looking incredibly chill with its eyes half-closed",
    "Lobster": "wearing a bib with a picture of a human on it and holding a tiny silver fork and knife",
    "Manta Ray": "wearing a black bow tie and a monocle while gliding underwater",
    "Meerkat": "wearing a tall black busby hat like a royal guard and standing perfectly still",
    "Mole": "wearing thick 'coke-bottle' glasses and holding a tiny flashlight, looking very confused in the bright sun",
    "Monkey": "wearing a business suit and looking frustrated while trying to assemble a tiny IKEA-style chair with a hex key",
    "Mouse": "straining to lift a giant barbell made of two huge olives and a toothpick, wearing a tiny sweatband",
    "Narwhal": "with a colorful 'Ring Toss' game hoop perfectly caught on its tusk",
    "Northern Hairy-Nosed Wombat": "wearing a pair of fuzzy pink bunny ears headbands",
    "Numbat": "wearing a white lab coat and holding a 'Termite Specialist' clipboard",
    "Octopus": "wearing six different colorful socks and looking exhausted because it is still searching for the last two",
    "Okapi": "wearing striped knee-high socks that match its leg patterns exactly",
    "Orangutan": "wearing blue overalls and holding a large wrench, looking confused at a broken coconut",
    "Orca": "wearing a black-and-white striped referee shirt and blowing a whistle at a group of seals",
    "Otter": "using a flat river stone as a dinner plate for a tiny, fancy seafood meal",
    "Owl": "wearing thick, round academic glasses and a graduation cap while looking stern",
    "Pangolin": "wearing a miniature medieval knight's helmet that matches its scales",
    "Panther": "wearing a bright pink collar with a giant bell and looking extremely humiliated",
    "Parakeet": "wearing a tiny golden crown and sitting on a 'throne' made entirely of birdseed",
    "Parrot": "wearing a professional gaming headset and sitting in front of a tiny, glowing computer monitor",
    "Peacock": "with its tail fanned out, but several feathers are replaced by colorful hand fans and cocktail umbrellas",
    "Penguin": "wearing bright orange inflatable arm floaties while waddling across the ice",
    "Philippine Eagle": "wearing a tiny, majestic gold crown on its feathered head",
    "Pig": "wearing a fancy silk bib and using a silver fork to eat a giant slice of watermelon",
    "Pigeon": "wearing a tiny black beret and carrying a miniature baguette under its wing",
    "Platypus": "wearing a Sherlock Holmes deerstalker hat and holding a magnifying glass",
    "Polar Bear": "shivering under a thick, colorful woolly blanket while holding a steaming mug of hot cocoa",
    "Porcupine": "with several colorful party balloons safely tied to the tips of its quills",
    "Pronghorn": "wearing a marathon bib with the number '1' and carrying a tiny water bottle",
    "Pufferfish": "inflated into a perfect sphere, wearing a tiny 'Don't Touch' sign pinned to its spikes",
    "Quokka": "holding a small cardboard sign that says 'Free Hugs' with a huge smile",
    "Rabbit": "wearing a monocle and checking a tiny gold pocket watch with a worried look",
    "Raccoon": "wearing a formal tuxedo and holding a fancy crystal cocktail glass",
    "Rat": "wearing a white chef's hat and tasting soup from a tiny silver spoon",
    "Rattlesnake": "with a colorful plastic baby's rattle taped to the end of its tail, looking very serious",
    "Red Panda": "trying to meditate in a perfect lotus pose with its paws together and eyes closed",
    "Red Wolf": "wearing a bright red bandana and looking like a cool biker",
    "Reindeer": "tangled in a string of glowing, multi-colored Christmas lights and looking very annoyed",
    "Rhino": "looking cross-eyed and grumpy at a tiny, colorful butterfly that has landed right on the tip of its horn",
    "Roadrunner": "wearing a pair of high-tech sneakers with literal rocket boosters attached to the sides",
    "Robin": "wearing a tiny mailman's hat and trying to shove a human-sized envelope into a tiny birdhouse",
    "Saola": "wearing a gold medal for 'Hide and Seek World Champion'",
    "Scorpion": "using its stinger to carefully hold a tiny, delicate paintbrush and painting a miniature landscape",
    "Sea Turtle": "with a miniature thatched-roof 'beach bar' built on its shell, complete with tiny stools",
    "Seahorse": "wearing a tiny miniature leather saddle with stirrups on its back",
    "Seal": "wearing a tuxedo and balancing a tray with a single, tiny glass of sparkling cider on its nose",
    "Shark": "sitting on an underwater couch with a bowl of popcorn, watching a movie about kittens with a terrified face",
    "Sheep": "with its wool styled into a perfect, massive 1970s afro haircut",
    "Sloth": "wearing a gold medal that says 'World's Fastest Runner' around its neck",
    "Snail": "with a miniature 'Wide Load' sign on its shell and several tiny orange traffic cones trailing behind it",
    "Snake": "looking frustrated while trying to play a long, thin flute with no fingers",
    "Snow Leopard": "wearing a colorful knitted woolly hat with a giant pom-pom",
    "Snowy Owl": "wearing a nightcap and holding a tiny 'World's Best Dad' mug, looking like it needs more coffee",
    "Sparrow": "wearing a tiny hand-knitted woolen scarf and earmuffs while looking grumpy",
    "Squid": "holding eight different colorful pens and looking stressed while trying to sign a single contract",
    "Squirrel": "wearing a tiny leather aviator helmet and goggles, ready for takeoff",
    "Starfish": "wearing five tiny sneakers, one on each arm, and looking like it's ready for a marathon",
    "Sumatran Orangutan": "holding a large tropical leaf like an umbrella and carrying a briefcase",
    "Tiger": "wearing a fancy silk bathrobe and carefully holding a tiny porcelain cup of tea with one claw extended",
    "Tortoise": "with a 'Student Driver' sign on its shell, being overtaken by a very slow snail",
    "Toucan": "wearing a pair of giant novelty glasses with a fake nose and mustache on its beak",
    "Turkey": "holding a sign that says 'Eat Pizza' while wearing a bad disguise of a fake mustache and glasses",
    "Turtle": "with a giant 'Turbo' racing spoiler glued to its shell and a tiny checkered flag in its mouth",
    "Vaquita": "wearing a 'VIP' (Very Important Porpoise) gold lanyard around its neck",
    "Vulture": "wearing a 'Have a Nice Day' t-shirt while waiting patiently by a dry, bare bone",
    "Walrus": "with its long tusks decorated with colorful plastic rings, like a game of ring-toss",
    "Whale": "wearing a giant, oversized snorkel and a pair of very tight, small swimming goggles",
    "Wolf": "wearing a pink floral grandmother's nightcap and reading glasses",
    "Woodpecker": "wearing a yellow construction helmet and using its beak like a jackhammer on a tiny 'Under Construction' sign",
    "Yangtze Finless Porpoise": "wearing a headband with a 'Smile' emoji on it",
    "Zebra": "wearing a black-and-white referee uniform and blowing a whistle with a very stern facial expression",
}

DINO_SCENARIOS = {
    "Tyrannosaurus":   "A Tyrannosaurus sitting comically on a brightly colored playground swing. Its notoriously short, stocky arms are struggling to grip the chains, barely reaching. Its tail droops to the ground. Other smaller dinosaurs are playing happily on nearby slides and roundabouts. The T-Rex has an expression that is simultaneously slightly frustrated but also determined and slightly sheepish.",
    "Triceratops":     "using its three long horns as a coat rack, with colorful scarves, a handbag, and a dripping umbrella hanging perfectly from each horn, looking very pleased with itself",
    "Velociraptor":    "carefully picking a door lock with its sickle claw, wearing a tiny chef's apron, looking extremely clever and proud of itself",
    "Ankylosaurus":    "its armoured tail club having accidentally knocked over a long row of dominoes in a perfect spiral, looking simultaneously guilty and deeply impressed at the destruction",
    "Spinosaurus":     "wearing a bright orange lifeguard swimsuit and sitting in a very tall lifeguard chair by a river, blowing a whistle officiously, with a large 'NO SWIMMING' sign clearly visible beside it",
    "Stegosaurus":     "with tiny solar panels strapped to each back plate and a bright green 'Eco Warrior' badge on its chest, looking insufferably smug about its carbon footprint",
    "Brachiosaurus":   "using its impossibly long neck to peer through the upper-floor window of a skyscraper, face pressed against the glass with a goofy wide-eyed grin",
    "Brontosaurus":    "A Brontosaurus using its impossibly long neck to carefully peek into a cozy, elevated treehouse. The dinosaur's massive, goofy, wide-eyed face is right up to the small window, grinning. Inside, tiny birds are fluttering in surprise around miniature furniture. The Brontosaurus looks excited but very gentle.",
    "Mosasaurus":      "wearing tiny bright-yellow inflatable water wings on its front flippers while swimming underwater, looking utterly mortified to be seen in them",
    "Carnotaurus":     "looking deeply offended because someone has started hanging Christmas fairy lights from its two short stubby head horns, treating them purely as decoration",
    "Pterosaur":       "trying to hold a giant umbrella with its wing claws in a strong gust of wind, being blown almost sideways while clutching a tiny briefcase with its feet, looking very flustered",
    "Gallimimus":      "wearing a bright orange traffic cone as a hat while sprinting in obvious panic in completely the wrong direction, arms flailing wildly",
    "Deinonychus":     "holding a large magnifying glass and a tiny notebook, wearing a miniature detective hat, crouching to examine a single mysterious footprint with intense concentration",
    "Baryonyx":        "wearing full yellow rubber fishing waders and a fisherman's cap, proudly holding up an enormous fish with a massive beaming grin",
    "Argentinosaurus": "trying to fit through a tiny doorway, its enormous body comically wedged in the frame while it sucks in its belly and tries to squeeze through with a very optimistic expression",
    "Dimorphodon":     "wearing a tiny leather aviator helmet and goggles, attempting to land gracefully on a branch but tumbling beak-first into a pile of autumn leaves",
    "Struthiomimus":   "wearing a full chef's toque and pristine apron, sprinting at full speed with a steaming tray of food held perfectly level and balanced, looking extremely focused",
    "Nigersaurus":     "with its unusually wide, straight-edged mouth pressed flat against a patch of grass like a living lawnmower, looking very industrious and self-satisfied",
    "Pentaceratops":   "standing in front of a mirror looking extremely pleased with its five horns, carefully adjusting each one like a person styling their hair before a big event",
    "Chasmosaurus":    "wearing its large neck frill decorated with tiny fairy lights and glitter like a festive collar, looking simultaneously embarrassed and secretly delighted",
}

# Test with multiple animals across different types for a fair comparison
TEST_ANIMALS = list(TEST_SCENARIOS.keys())

_ALL_SCENARIOS = {**TEST_SCENARIOS, **DINO_SCENARIOS}


def get_prompt(animal: str) -> str:
    """Generate a prompt for an animal."""
    scenario = _ALL_SCENARIOS.get(animal, "in a funny and endearing pose")
    return PROMPT_TEMPLATE.format(animal=animal, scenario=scenario)


def setup_output_dir() -> Path:
    """Create and return the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
