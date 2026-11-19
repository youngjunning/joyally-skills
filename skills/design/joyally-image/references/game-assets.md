# Game-ready 2D assets

Use this route for a game asset family rather than a single decorative illustration: playable characters, NPCs, props, inventory icons, tilesets, environment layers, game UI art, particles, animation clips, sprite atlases, or an import-ready pack. It produces independent source art and metadata for the target game; it does not reproduce another game's assets, UI, copy, art direction, characters, sounds, or game content.

For a game visual system, UI composition, scene language, or art direction that is not already approved, ask `joyally-design` to establish the direction before pixel production. This route owns the generated raster assets, asset contracts, and technical QA. It does not choose an engine or claim that an asset has been imported successfully.

## Lock the asset contract first

Before the first generation, record a short asset brief. Do not let the image model decide runtime semantics.

| Field | Required decision |
| --- | --- |
| Family and use | Character/NPC, prop, tile, environment layer, UI art, effect, or animation; state the gameplay use and audience. |
| Art direction | Approved visual brief or an explicit, original style description; shared palette, line weight, material, camera/projection, and lighting. |
| Runtime contract | Target engine if known, native pixel dimensions, display scale, color space, alpha requirement, and expected import format. Unknown values remain unknown; do not invent Unity, Cocos, Godot, or a platform. |
| Geometry | Canvas size, grid size for pixel art, tile size and tiling axes, character facing/action list, animation frame count/FPS, or UI state list. |
| Placement | Pivot/origin, collision-free safe area, atlas padding/extrusion requirement, 9-slice margins, and whether the asset must be seamless. |
| Rights | Original subject, approved user-owned references, or a verified license. Existing game screenshots are observation references, not source assets to trace or restyle closely. |

For a coordinated family, lock a shared style sheet and create one representative asset before producing variants. Preserve the accepted silhouette, palette, scale, outline and shading rules unless the brief explicitly changes them.

## Route by asset type

| Asset | Deliverable and special checks |
| --- | --- |
| Character / NPC | Transparent source PNG, named directions/actions, consistent origin and apparent scale. Create a turnaround or one representative animation before expanding the action set. |
| Prop / inventory icon | Transparent PNG at native size; readable silhouette at intended in-game size. Use a stable footprint and anchor rather than baking a scene behind it. |
| Tile / autotile / terrain | Native tile PNGs, declared tile size and adjacency convention. Validate a 2×2 or larger assembled preview for seams, edge continuity and unwanted repeated landmarks. |
| Environment / parallax layer | Layered source PNGs with declared scroll axis and safe crop area. Do not claim seamlessness unless an assembled repeat preview has passed. |
| Game UI art | Raster decoration, frames, icons or backgrounds only. Exact copy, interaction states, layout and 9-slice behavior require an approved design contract; never rely on generated text. |
| Effect / particle | Transparent frame sequence or atlas, declared frame order/FPS and loop/one-shot behavior. Check the first/last-frame transition for a loop. |
| Animation atlas | Individual frames plus an atlas and manifest only after all frames share the declared cell size, origin, alpha mode and padding. Do not use whole-sprite rotation or interpolation to fake missing actions. |

For a simple fixed 12-frame mascot or loading loop, use `sprite-loop.md` instead. For a Codex pet, use `codex-pet.md`; neither contract substitutes for a general game asset pack.

## Generate, refine and package

1. Generate or edit a representative asset using the locked contract. Existing user-supplied game art that must stay visually identical always uses `image-edit.md`.
2. Inspect at native size, intended in-game size, and 4× magnification. Reject clipped silhouettes, soft grid edges, alpha halos, inconsistent outline width, drifting proportions, unreadable icons, or accidental text.
3. After acceptance, produce the remaining family one bounded asset at a time. Keep shared palette and geometry fixed; only the declared variation may change.
4. Keep source PNGs even when the target accepts WebP. Export preview/contact-sheet files separately from runtime inputs.
5. Write `game-assets.json` in the package root. It is a contract for review, not a claim that a game engine has imported the assets.

```json
{
  "version": 1,
  "family": "kipka-undercover-ui",
  "styleBrief": "original warm party-game illustration",
  "runtime": { "engine": null, "colorSpace": "sRGB" },
  "assets": [
    {
      "id": "vote-token-blue",
      "kind": "prop",
      "source": "source/vote-token-blue.png",
      "nativeSize": [128, 128],
      "alpha": true,
      "pivot": [0.5, 0.5],
      "status": "reviewed"
    }
  ]
}
```

Use only fields that the target asset needs. For an atlas, add cell size, columns, rows, padding/extrusion, frame order, FPS and loop mode. For tiles, add tile size, tiling axes and the assembled-preview path. For 9-slice UI, add declared slice margins.

## Release gates

- **Identity and rights:** no copied brand, character, level, UI, title treatment, game text, asset file or proprietary reference. Keep source/rights notes in the manifest when a non-generated input is used.
- **Alpha and edges:** transparent assets have real alpha, clean corners and no matte fringe. Pixel art uses hard, unfeathered edges and no semi-transparent anti-aliasing unless the brief explicitly allows it.
- **Geometry:** every frame/tile has the declared dimensions; pivots, cells, padding and direction/action labels are consistent. Inspect assembled atlases rather than only individual frames.
- **Readability:** inspect the native asset, intended display size and 4× view. A pleasing full-size illustration that fails at its runtime size is not accepted.
- **Tiling and motion:** repeat tiles in an assembled preview; animate clips in a preview. Reject seams, jumps, first/last-frame discontinuities, clipped extrema and unexplained scale drift.
- **Package integrity:** manifest paths exist, IDs are unique, runtime inputs are separate from previews and metadata, and the target format has been declared. Engine import, memory budget, compression and in-game behavior remain unverified until the target project runs its own pipeline.
