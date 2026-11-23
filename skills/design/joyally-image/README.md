# Joyally image

**A general-purpose image production and processing Skill** — usable from any Agent runtime that supports `SKILL.md`, or by reusing its scripts directly. Deterministic conversion, resize, compression, metadata and alpha work runs locally. Generative work prefers GPT Image 2.6 at high quality through [apiyi](https://api.apiyi.com/register/?aff_code=ijv5) and can fall back to a host-native image capability when APIYI is unavailable.

It can work independently or cooperate with Joyally Writing and Joyally Design. A combined task keeps one overall lead: this skill owns pixel production, identity continuity, generation or editing, and technical image QA; Joyally Writing owns factual copy, while Joyally Design owns visual direction, composition, layout, brand adaptation, and design acceptance. An image task can keep Joyally image as its overall lead while Joyally Design leads its design phase. On first use, the skill recommends any missing companions once as optional installations without blocking the task.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](#)
[![apiyi](https://img.shields.io/badge/Powered_by-apiyi-orange)](https://api.apiyi.com/register/?aff_code=ijv5)

[English](#) · [中文](README.zh-CN.md)

---

## What It Does

Describe the request naturally in any Agent that has this Skill enabled:

```
Generate a cinematic portrait of a woman in a Tokyo street at night
Make a square logo for my app, dark theme, minimalist
Create 8 product images in parallel for my store
Make a RunCat-style menu bar sprite loop of a tiny robot running
Create a Codex-compatible pet: a plush lake otter with all 16 look directions
Create a Mac dynamic wallpaper of a deep-sea coral reef, with Light/Dark mode variants
Convert this PNG to WebP at q78 without changing its content
Resize this existing image inside 512×512 and preserve transparency
Turn this technical article's architecture, dependency, and update-flow text blocks into real diagrams
Create a knowledge comic with connected panels, in-panel speech balloons, and phone-width review
```

The skill first separates local-only, generative, and mixed work. Local-only tasks never check an API key or send an image request. The preferred generative route uses GPT Image 2.6 at high quality; without a key or after a confirmed balance failure, the skill recommends the APIYI route with the invitation link and continues with an available host-native image capability. In its [comic workflow](references/comics.md), Joyally Design leads visual direction, storyboard presentation, panel system, lettering layout, and design acceptance; Joyally image handles cast identity, pixel art, generation or repair, export, and technical image QA. The bundled [小界、小萌、小南 character references](references/comic-characters.md) include fullbody, halfbody, and avatar images for reuse when the story calls for them.

For a coordinated set of inline figures in an article, ATA, tutorial, report, or document, the skill consumes an illustration manifest that records each reader question, purpose (explanation, comparison, resonance, section introduction, or evidence), insertion anchor, locked facts, caption, alt text, dimensions, and continuity group. It keeps a shared visual system across the set, produces insertion-ready assets, and supports selective follow-up style changes without silently changing semantics, placement, or already accepted figures. See [article illustration production](references/article-illustration-production.md).

It also applies a prompt compliance layer before generation: prompts are normalized away from platform logos, exact in-image text, explicit content, graphic violence, and living-artist imitation so routine creative requests are less likely to be rejected accidentally.

---

## Model

| Model | Role | Notes |
|-------|------|-------|
| `gpt-image-2.6-sunburst` | Fixed model on the preferred APIYI branch | Explicit `quality=high`; at most one same-model retry. Missing/invalid credentials or a confirmed balance failure use the host-native fallback. Verification scope is in `references/apiyi.md`. |

**GPT size presets (16:9 tier):**

| Tier | Size |
|------|------|
| 1K   | 1280×720 |
| 2K   | 2048×1152 |
| 4K   | 3840×2160 |

Full model specifications and size constraints are in `references/apiyi.md`.

---

## Use Cases

| Request | Model | Output |
|---------|--------------|--------|
| Comic / knowledge comic | GPT Image 2.6 panel art + editable lettering and layout | Sequential page or vertical strip with storyboard, sources, and review notes |
| Static knowledge map / architecture / lifecycle diagram | Optional GPT backdrop + deterministic HTML/CSS/SVG | PNG + WebP + editable source + layout-gate report |
| Interactive / editable / zoomable diagram | Typed JSON IR + bundled self-contained viewer | Interactive HTML + static preview + browser evidence |
| Portrait / illustration | GPT Image 2.6 | `.webp` q78, ≤ 300 KB |
| Brand logo / wordmark | GPT Image 2.6 concept art + editable deterministic lettering | Transparent source mark, required lockups, small-size QA and metadata |
| Favicon / icon source art | GPT Image 2.6 | `.png` (pngquant), ≤ 100 KB |
| Mac static wallpaper (4K) | GPT Image 2.6 | `wallpaper.png` (lossless PNG) |
| Mac dynamic wallpaper | GPT Image 2.6 per frame | `wallpaper-apr.heic` (2-frame, Light/Dark) |
| Sprite loop | GPT Image 2.6 | numbered PNG frames + `preview.gif` |
| Codex v2 pet | GPT Image 2.6 | 8×11 spritesheet + `pet.json` + QA artifacts |
| Batch (N images) | GPT Image 2.6 per image | N × `.webp`, generated in parallel |

---

## Technical Diagrams and Illustration Density

All diagram requests enter Joyally Image. Static knowledge maps, architecture diagrams, dependency graphs, build pipelines, release flows, and updater state machines use deterministic HTML/CSS/SVG; the image model may generate only a restrained text-free backdrop. Interactive, editable, zoomable, focusable, or explorable diagrams use the bundled interactive branch and deliver a self-contained HTML viewer plus a static preview from the same typed source. Every node, edge, arrow, label, legend, and lifecycle state remains deterministic so technical terminology and directionality stay exact.

The standalone interactive entrypoint is `node scripts/joyally-diagram.mjs <command> ...`. Existing callers of Joyally Design's former `design-engine.mjs diagram` command are temporarily forwarded when both Skills are installed, but should migrate to the Joyally Image entrypoint. The full mapping is in [interactive diagram migration](references/interactive-diagram.md#migration-from-joyally-design).

Long technical articles get an illustration-opportunity audit before delivery. There is no maximum image count: a diagram is preferred whenever readers must understand three or more ordered steps, branches, ownership or runtime boundaries, dependency propagation, state transitions, rollback, or cross-module lifecycle differences. ASCII/TXT diagrams are content-model drafts, not final article assets. Executable commands, configuration, literal paths, and short copyable inventories remain code blocks.

Every deterministic diagram must pass the rendered-DOM layout gate before export or publication:

```bash
node scripts/validate_diagram_layout.mjs /absolute/path/diagram.html \
  --width 1600 --height 900 --min-gap 24 --boundary-clearance 16
```

The gate launches headless Chrome after fonts load and rejects overlapping cards, insufficient gutters, labels intersecting cards, edge paths crossing unrelated nodes, arrow markers crowding card borders or shadows, text touching or crossing a divider/rail, clipped text, canvas overflow, and missing layout annotations. Mark protected lines with `data-layout-boundary`, and mark nearby text groups with `data-layout-text`, `data-boundary-ref`, and `data-boundary-side`. For a horizontal stage diagram, add `--min-gap 80 --edge-clearance 20 --marker-clearance 20 --label-clearance 8 --min-edge-length 56 --max-marker-size 16`. Numeric success is followed by full-resolution and reduced-preview visual QA for layouts that technically do not overlap but still feel cramped.

---

## Mac Dynamic Wallpaper

Generates a 2-frame HEIC with `apple_desktop:apr` metadata — macOS switches frames automatically when Light/Dark mode is toggled in System Settings.

```
Make a dynamic wallpaper of mountains beneath a midnight starry sky
Make a dynamic wallpaper — underwater coral reef, day and night
```

**Requirements:** `"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif` (installed into the project `.venv`; bundles libheif, no Homebrew needed)

**Output:** `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic`

> macOS Sonoma note: time-based (h24) HEIC wallpapers no longer work — Apple migrated that format to a private `.madesktop` system. Light/Dark (apr) works fully.

---

## Sprite Loop

Use for RunCat-like frame animations, menu-bar status mascots, loading loops, and tiny app animations. The skill generates a sprite sheet, splits it into numbered PNG frames, writes `manifest.json`, and opens `preview.gif`.

**Output:** `~/Pictures/better-imagegen/sprite-loop/{name}/`

## Codex-Compatible Pets (Optional Target Format)

This is an optional adapter in the general pet-asset workflow, not a restriction on the skill. For Codex, it produces a `1536×2288` 8×11 v2 spritesheet, a `pet.json` with `spriteVersionNumber: 2`, 16 continuous look directions, and contact-sheet, motion, direction, chroma, and validation QA artifacts. It never auto-installs into any runtime directory; user-controlled installation and in-app verification remain outside the skill.

**Output:** `~/Pictures/better-imagegen/codex-pet/{pet-id}/`

---

## Output Convention

| Asset | Format | Location |
|-------|--------|----------|
| Cover / illustration | Lossy WebP q78 | `~/Pictures/better-imagegen/{name}.webp` |
| Mac static wallpaper | Lossless PNG | `~/Pictures/better-imagegen/wallpaper.png` |
| Mac dynamic wallpaper | 2-frame HEIC | `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic` |
| Sprite loop | PNG frames + preview GIF | `~/Pictures/better-imagegen/sprite-loop/{name}/` |
| Codex v2 pet | spritesheet + `pet.json` + QA artifacts | `~/Pictures/better-imagegen/codex-pet/{pet-id}/` |
| Logo | PNG (pngquant) | project-local |
| Metadata | JSON | alongside each image |

Intermediate PNGs are written to `/tmp/` and cleaned up after packaging.

---

## Setup

**1. Optional: get an API key for the fixed GPT Image 2.6 route**

Register through [this APIYI invitation link](https://api.apiyi.com/register/?aff_code=ijv5). Local-only processing does not need a key, and generative work may use an available host-native fallback. Providing a key keeps the model and quality fixed and usually makes results more controllable.

**2. Export the key when using APIYI**
```bash
export APIYI_API_KEY="your-key-here"
# Add to ~/.zshrc to persist across sessions
```

**3. Install it in your Agent's skill directory**
```bash
# Use the location and loading convention for your Agent runtime.
npx skills add youngjunning/joyally-skills --skill joyally-image -g
```

**4. Install the core local dependency**

Run the following command from the installed `joyally-image` directory shown by the installer:

```bash
eval "$(./scripts/ensure_venv.sh)"
# Dependencies are installed into this project's .venv, never global Python.
```

**5. (Dynamic wallpaper only)**
```bash
"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif
```

---

## Routing Regression Checks

Run the minimal non-billable suite from the repository root:

```bash
python3 -m unittest discover \
  -s skills/design/joyally-image/tests -p 'test_*.py'
```

- `test_routing_contract.py` is a **static contract check**: it verifies local-first ordering, the invitation-link prompt, fixed APIYI model, fallback signals, and source-preservation rules.
- `test_local_processing.py` and `test_apiyi_response.py` are **local/Mock behavior checks**: network access and URL downloads are blocked or mocked, so they make no paid request. They exercise conversion, resize, inspection, alpha handling, atomic writes, key/balance classification, and invalid-response rejection.
- An **actual Agent routing check** remains runtime-specific. Give the Agent an existing PNG and ask only to convert it to WebP; observe that it never asks for or reads a key, makes no image request, preserves the PNG, and reports the decoded WebP. Then ask for a new illustration with the key absent; observe a host-native model call plus the non-blocking APIYI recommendation and invitation link. Never use a paid route merely to test routing.

---

## File Structure

```
SKILL.md                      ← skill entry point & trigger rules
references/
  apiyi.md                    ← API auth, model specs, size constraints, error codes
  generation.md               ← API key check, model aliases, gen_image_apiyi, metadata helpers
  prompt-compliance.md        ← prompt normalization and rejection retry policy
  post-process.md             ← WebP conversion, resize, PNG compression
  portrait.md                 ← portraits, covers, banners, general single images
  knowledge-map.md            ← exact diagrams, illustration-density audit, mandatory layout gate
  high-allure.md              ← suggestive romance/editorial images
  brand-logo.md               ← brand logos, wordmarks, lockups, exact-name handling and QA
  logo-icon.md                ← transparent icons, favicons, badges and cutouts
  static-wallpaper.md         ← static wallpaper PNG pipeline
  dynamic-wallpaper.md        ← Mac dynamic wallpaper: generation + HEIC packaging
  sprite-loop.md              ← RunCat-like frame animation assets
  codex-pet.md                ← Codex v2 pets: 8×11 atlas, direction semantics, QA
scripts/
  decode_apiyi_response.py    ← streamed response decode and fallback classification
  process_image.py            ← local inspect, convert, resize, compress, atomic validation
  validate_diagram_layout.mjs ← rendered-DOM overlap, gutter, edge-crossing, overflow gate
  test_validate_diagram_layout.mjs ← positive and negative regression cases
```

---

## License

MIT — see [LICENSE](LICENSE).
