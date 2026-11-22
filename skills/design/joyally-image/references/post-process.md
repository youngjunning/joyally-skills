# Local Image Processing and Output Conversion

This reference owns two distinct paths:

1. **Local-only processing** of an existing PNG, JPEG or WebP when explicit parameters fully determine the result. It never reads `APIYI_API_KEY`, loads model setup, prints provider promotion, or sends an external request.
2. **Generated-image finishing** after a model route succeeds. The preferred APIYI model remains `gpt-image-2.6-sunburst` with API `quality=high` (see `references/generation.md`). API quality and the encoding quality below are separate settings.

Initialize the project-local environment before either path:

```bash
SKILL_DIR="/path/to/joyally-image"
eval "$("$SKILL_DIR/scripts/ensure_venv.sh")"
```

## Local-only route

Use the bundled script instead of ad hoc one-liners so the input is never overwritten, output is written through a same-directory temporary file, and the result is decoded and measured before promotion:

```bash
# Format, dimensions, bytes, metadata presence and alpha findings.
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" inspect input.png

# Deterministic format conversion.
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" \
  convert input.png output.webp --quality 78

# Aspect-preserving resize inside a 512×512 box.
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" \
  resize input.png output.png --width 512 --height 512 --fit contain

# Pixel art or an integer-scale sprite uses nearest-neighbor explicitly.
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" \
  resize sprite.png sprite-2x.png --width 256 --height 256 \
  --fit stretch --resample nearest

# Re-encode at a requested quality without changing geometry.
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" \
  compress input.jpg output.jpg --quality 80
```

The input and output paths must differ. Existing outputs are preserved unless `--force` is explicit; even then the input can never be replaced. PNG and WebP preserve alpha. JPEG conversion fails when real transparency exists unless the caller explicitly supplies a matte such as `--background '#ffffff'`. EXIF and ICC metadata are preserved when supported and removed only with `--strip-metadata`; `inspect` reports other container metadata without copying it by implication. Animated or multi-frame inputs are rejected by this single-image helper and must use their type-specific workflow.

`contain` preserves the whole image and may produce dimensions smaller than the requested box. `cover` preserves aspect ratio and crops to the exact box. `stretch` forces exact dimensions and must be an explicit choice. Use `nearest` for pixel art and `lanczos` for ordinary artwork.

Flat, edge-connected background removal may use `scripts/ensure_transparent.py` locally when the background identity and tolerance are explicit. Hair, fur, semi-transparent edges, a complex scene, or any request that requires deciding what the subject is belongs to the generative route.

For mixed work, retain the supplied original, write the model result to a new candidate, and run this local path only on that candidate. If generation or any local gate fails, keep the original and previously accepted files, delete only task-owned temporary output, and report the failed stage. Never claim generation success from a conversion result.

---

Every generated image must also be post-processed before being saved as a deliverable.

---

## Target Format

| Use case | Format | Quality | Target dimensions |
|----------|--------|---------|------------------|
| Hero / cover image | lossy WebP | q78 | varies by use case |
| Inline illustration | lossy WebP | q72 | 664×996 (2:3) |
| Logo / favicon | PNG | n/a | resize to 512×512 after generation |

**Never use lossless WebP for photographic content** — it is ~3× larger than lossy. Always use lossy.

---

## WebP Conversion Function

Use the bundled Pillow script for safe source preservation. Keep the WebP even when it is larger than the source: copying a PNG into a `.webp` path produces a mislabeled, invalid deliverable.

```bash
to_webp() {
  local src="$1" dst="$2" q="${3:-78}"
  local before after
  before=$(stat -f%z "$src" 2>/dev/null || stat -c%s "$src")
  "$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/process_image.py" \
    convert "$src" "$dst" --quality "$q" || return 1
  after=$(stat -f%z "$dst" 2>/dev/null || stat -c%s "$dst")
  if [ "$after" -ge "$before" ]; then
    echo "⚠ webp larger than src (${after}B ≥ ${before}B) — retained valid WebP"
  else
    echo "✓ webp q${q}: ${before}B → ${after}B (-$(( (before-after)*100/before ))%)"
  fi
}
```

---

## GPT Image 2.6 Output Post-Processing

Output is already at the requested size (e.g. 848×1280 PNG). No resize needed. Convert directly:

```bash
to_webp "$OUTPUT_PATH" "output.webp" 78
rm -f "$OUTPUT_PATH"
```

---

## Logo Post-Processing

For logo/icon/favicons where transparency is expected, verify alpha before resizing:

```bash
sips -g hasAlpha "$OUTPUT_PATH"
```

If the output has black/white corners, a solid square background, or a baked rounded rectangle tile, remove only the edge-connected background before resizing. For the Argos local tool:

```bash
swift run --package-path <argos-checkout> transparentize-black-background \
  "$OUTPUT_PATH" /tmp/logo-transparent.png --threshold 18
mv /tmp/logo-transparent.png "$OUTPUT_PATH"
sips -g hasAlpha "$OUTPUT_PATH"
```

Do not use a global color erase on logos by default; it can damage black/white details inside the mark. Prefer edge-connected background removal so interior dark/light details remain opaque.

After generating a logo or favicon at 1280×1280:

```bash
# Resize and compress logo
sips -z 512 512 public/logo.png
pngquant --force --quality=80-95 --speed 1 --output public/logo.png public/logo.png

# Resize and compress favicon
sips -z 256 256 public/favicon.png
pngquant --force --quality=80-95 --speed 1 --output public/favicon.png public/favicon.png
```

Target sizes: logo ≤ 100 KB, favicon ≤ 25 KB. Raw generated files are typically 700 KB–1.3 MB without compression.

---

## File Size Budget

| Asset type | Hard limit | Action if exceeded |
|------------|------------|-------------------|
| Cover / hero WebP | 300 KB | Lower quality to q70, retry; or resize to 683×1024 and re-convert |
| Illustration WebP | 300 KB | Lower quality to q65 and re-convert |
| Logo PNG | 100 KB | Re-run `pngquant` at `--quality=60-80` |
| Favicon PNG | 25 KB | Re-run `pngquant` at `--quality=50-70` |
