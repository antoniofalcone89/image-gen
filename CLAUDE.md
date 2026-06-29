# CLAUDE.md — image-gen

Standalone Python toolbox for generating the animal quiz images via AI image APIs.
Generated images are uploaded to Cloudflare R2 (`animals/{uuid}.png`) by the service upload workflow; this project only handles generation and local saving.

## Purpose

- Generate one 1024×1024 photorealistic image per animal (funny scenario, ironic gaze, ultra-realistic wildlife photography style)
- Generate the app logo (see `logo_config.py`)

## Structure

| File | Role |
|------|------|
| `shared_config.py` | Central config: `PROMPT_TEMPLATE`, `NEGATIVE_PROMPT`, scenario groups, `get_prompt()` |
| `generate.py` | Single CLI entry point — `--provider`, `--group`, `--logo`, optional animal filter |
| `provider_openai.py` | gpt-image-1 via OpenAI API — default provider |
| `provider_replicate.py` | Flux Schnell via Replicate — cheaper option for bulk drafts |
| `logo_config.py` | Logo-specific prompt, concept, and output dir (`logo_output/`) |
| `final_images/` | Final approved PNGs (one per animal, named `{AnimalName}.png`) |
| `logo_output/` | Generated logo candidates |

## Setup

```bash
cd image-gen
python -m venv .venv && source .venv/bin/activate
pip install openai replicate requests python-dotenv
```

Create a `.env` file (already in `.gitignore`):

```
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...   # only needed if using --provider replicate
```

## Generating images

```bash
# Generate a group (OpenAI by default)
python generate.py --group arctic_wonders

# Generate specific animals only
python generate.py --group feathered_wonders Crane Hornbill Condor

# Use Replicate for cheaper bulk drafts
python generate.py --provider replicate --group main

# Generate a level logo
python generate.py --logo arctic_wonders
```

Output goes to `image-gen/<group>/` or `image-gen/logo_output/`.

## Adding a new animal

1. Add an entry to the appropriate `scenarios/<group>.json`:
   ```json
   { "NewAnimal": "funny scenario description" }
   ```
2. Run:
   ```bash
   python generate.py --group <group> "NewAnimal"
   ```
3. Move approved images to `final_images/`.

## Provider comparison

| Provider | Model | Cost/img | Speed | Notes |
|----------|-------|----------|-------|-------|
| OpenAI | gpt-image-1 | ~$0.042 | ~15s | Default; best quality |
| Replicate | Flux Schnell | ~$0.003 | ~5–10s | Cheapest; good for bulk drafts |

## Prompt design

All animal prompts follow the template in `shared_config.PROMPT_TEMPLATE`:

- Ultra-realistic close-up, clearly recognizable species
- Funny, specific scenario (not generic "funny pose")
- Ironic gaze
- Full head and key species features visible
- Bright daylight, soft clouds, subtle habitat hints in background
- No cartoon, no 3D render, no text/watermark (enforced via `NEGATIVE_PROMPT`)

To change the style globally, edit `PROMPT_TEMPLATE` and `NEGATIVE_PROMPT` in `shared_config.py`.

## Output to R2

VPS: `ubuntu@57.129.123.33`

After generating, approved images are uploaded to Cloudflare R2 from the service side (not from this project). The DB `animals.image_url` column stores the resulting `https://storage.afalco.ovh/animals/{uuid}.png` URL. Never rename or delete R2 objects without updating the DB — the UUID is the only link between the file and the DB row.
