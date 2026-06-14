# CLAUDE.md — image-gen

Standalone Python toolbox for generating the animal quiz images via AI image APIs.
Generated images are uploaded to Cloudflare R2 (`animals/{uuid}.png`) by the service upload workflow; this project only handles generation and local saving.

## Purpose

- Generate one 1024×1024 photorealistic image per animal (funny scenario, ironic gaze, ultra-realistic wildlife photography style)
- Test multiple providers side-by-side before committing to one
- Generate the app logo (see `logo_config.py`)

## Structure

| File | Role |
|------|------|
| `shared_config.py` | Central config: `PROMPT_TEMPLATE`, `NEGATIVE_PROMPT`, `TEST_SCENARIOS` (130+ animals), `get_prompt()` |
| `provider_openai.py` | DALL-E 3 via OpenAI API — runs standalone to generate all animals |
| `provider_replicate.py` | Flux Schnell via Replicate — runs standalone, cheapest option |
| `provider_stability.py` | Stable Diffusion 3.5 via Stability AI — runs standalone |
| `compare_providers.py` | One-off script: generates the same animal(s) across all providers for side-by-side comparison |
| `logo_config.py` | Logo-specific prompt, concept, and output dir (`logo_output/`) |
| `final_images/` | Final approved PNGs (one per animal, named `{AnimalName}.png` or `{AnimalName}_stability.png`) |
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
REPLICATE_API_TOKEN=r8_...
STABILITY_API_KEY=sk-...
```

You only need keys for the provider(s) you want to use.

## Generating images

### Run a single provider for all animals

```bash
python provider_stability.py   # Stable Diffusion 3.5 — $0.03/img
python provider_replicate.py   # Flux Schnell — $0.003/img (cheapest)
python provider_openai.py      # DALL-E 3 — $0.04/img (also used for logo)
```

Each script iterates all animals in `shared_config.TEST_ANIMALS` and saves to `./comparison_output/{Animal}_{provider}.png`.

### Compare providers

```bash
python compare_providers.py
```

Edit `TEST_ANIMALS` in `compare_providers.py` to pick which animals to compare. Results go to `./comparison_output/`.

### Generate the app logo

```bash
python provider_openai.py   # __main__ block generates the logo by default
```

Logo prompt is defined in `logo_config.py`. Output goes to `./logo_output/`.

## Adding a new animal

1. Add an entry to `TEST_SCENARIOS` in `shared_config.py`:
   ```python
   "NewAnimal": "funny scenario description",
   ```
2. Run the preferred provider script — it generates all animals in `TEST_SCENARIOS` (already-generated files in `comparison_output/` are overwritten).
3. Move approved images to `final_images/`.

## Provider comparison

| Provider | Model | Cost/img | Speed | Notes |
|----------|-------|----------|-------|-------|
| Replicate | Flux Schnell | ~$0.003 | ~5–10s | Cheapest; good for bulk drafts |
| Stability AI | SD 3.5 Large | ~$0.030 | ~8s | Good detail; supports negative prompt |
| OpenAI | DALL-E 3 | ~$0.040 | ~15s | May revise prompt; best for logo |

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

After generating, approved images are uploaded to Cloudflare R2 from the service side (not from this project). The DB `animals.image_url` column stores the resulting `https://storage.afalco.ovh/animals/{uuid}.png` URL. Never rename or delete R2 objects without updating the DB — the UUID is the only link between the file and the DB row.
