# image-gen

AI image generation toolbox for the Animals Quiz Academy app.
Generates 1024×1024 images for animal cards and level logos using OpenAI, Replicate, or Stability AI.
Generated images are saved locally, then uploaded to Cloudflare R2 from the service side.

## Setup

```bash
cd image-gen
python -m venv .venv && source .venv/bin/activate
pip install openai replicate requests python-dotenv
```

Create a `.env` file (already in `.gitignore`) with keys for the provider(s) you want to use:

```
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
STABILITY_API_KEY=sk-...
```

## Generating animal images

```bash
python generate.py --provider <provider> --group <group> [animal ...]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--provider` | `openai` | `openai`, `replicate`, or `stability` |
| `--group` | — | Animal group to generate (required) |
| `animals` | all | One or more animal names within the group |

```bash
# Generate all animals in a group
python generate.py --group arctic_wonders
python generate.py --provider replicate --group arctic_wonders

# Generate a single animal
python generate.py --group arctic_wonders Puffin

# Generate multiple specific animals
python generate.py --group arctic_wonders Puffin "Arctic Wolf" Wolverine
```

Output is saved to `image-gen/<group>/<Animal>.png`.

### Available groups

| Group | Animals | Description |
|-------|---------|-------------|
| `main` | 150 | All standard game animals |
| `dino` | 20 | Dino World bonus level |
| `arctic_wonders` | 15 | Arctic Wonders bonus level |

## Generating level logos

```bash
python generate.py --provider <provider> --logo <level>
```

```bash
python generate.py --logo arctic_wonders
python generate.py --logo dino
python generate.py --logo app
python generate.py --provider stability --logo arctic_wonders
```

Output is saved to `image-gen/logo_output/<level>.png`.

### Available logos

| Level | Description |
|-------|-------------|
| `app` | Main app logo (globe with animals) |
| `arctic_wonders` | Arctic Wonders bonus level badge |
| `dino` | Dino World bonus level badge |

## Adding a new animal group

1. Create `scenarios/<group_name>.json` — a flat object mapping animal name to funny scenario:

```json
{
  "Capybara": "wearing a tiny golden crown while sitting on a throne made of hay",
  "Axolotl": "wearing a tiny party hat and blowing a paper noisemaker underwater"
}
```

2. Run — the new group is picked up automatically, no code changes needed:

```bash
python generate.py --group <group_name>
```

## Adding a new level logo

Add an entry to `logos.json`:

```json
"small_predators": {
  "prompt": "Digital illustration of a Small Predators level badge ...",
  "negative_prompt": "low resolution, blurry, ..."
}
```

Then run:

```bash
python generate.py --logo small_predators
```

No code changes needed — the new level appears automatically in `--logo` choices.

## Prompt design

### Animal images

All animal prompts follow a shared template (`shared_config.py`):

- Ultra-realistic close-up, clearly recognizable species
- Funny, specific scenario (not generic "funny pose")
- Ironic gaze directed at the camera
- Full head and key species features visible
- Bright daylight, soft clouds, subtle habitat hints in background
- No cartoon, no 3D render, no text or watermarks

The scenario string in the JSON fills in the funny situation. Keep it specific and visual.

### Logos

Logo prompts are free-form strings in `logos.json`. Each entry supports:

- `prompt` — full generation prompt
- `negative_prompt` — optional, appended automatically

## Project structure

```
image-gen/
├── scenarios/               # One JSON file per animal group
│   ├── main.json
│   ├── dino.json
│   └── arctic_wonders.json
├── logos.json               # One entry per level logo (app, arctic_wonders, dino, …)
├── logo_output/             # Generated logo images, one per level
├── <group_name>/            # Generated animal images, one folder per group
├── final_images/            # Approved images ready for R2 upload
├── generate.py              # Single CLI entry point
├── shared_config.py         # Loads scenarios/, exposes GROUPS + get_prompt()
├── logo_config.py           # Loads logos.json, exposes LOGOS + get_logo_prompt()
├── provider_openai.py       # generate_openai() — gpt-image-1
├── provider_replicate.py    # generate_replicate() — Flux Schnell
├── provider_stability.py    # generate_stability() — Stable Diffusion 3.5
└── compare_providers.py     # Side-by-side provider comparison for a given animal
```

## Cost reference

| Provider | Model | Cost/image |
|----------|-------|------------|
| OpenAI | gpt-image-1 (medium) | ~$0.042 |
| Stability AI | SD 3.5 Large | ~$0.030 |
| Replicate | Flux Schnell | ~$0.003 |

## After generating

1. Review images in `<group_name>/` or `logo_output/`
2. SCP the approved folder to the VPS (`ubuntu@57.129.123.33`):
   ```bash
   scp -r image-gen/<group_name> ubuntu@57.129.123.33:~/
   ```
3. SSH in and run the upload script from `animals-service/`:
   ```bash
   ssh ubuntu@57.129.123.33
   cd ~/animals-service
   docker compose run --rm \
     -v "$(pwd)/scripts:/app/scripts" \
     -v "$HOME/<group_name>:/images" \
     api python scripts/upload_images_r2.py --dir /images
   ```
4. The script uploads each image to Cloudflare R2 and sets `image_url` in the DB automatically
