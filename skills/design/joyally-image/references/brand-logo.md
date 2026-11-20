# Brand Logo / Wordmark

Use this workflow for a new brand logo, wordmark, logotype, brand emblem, mascot brand mark, or a family of related logo lockups. This is a brand-identity asset, not merely a favicon or app-icon tile.

Load first:

- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

Use `references/logo-icon.md` instead for a generic icon, favicon, sticker, badge, or cutout that does not need a brand brief or exact name treatment. Use `references/macos-app-icon.md` when the deliverable is a shippable `.icns` or iconset.

## Ownership and design handoff

Joyally image owns candidate generation, pixel production, transparent export and technical image QA. Joyally Design owns a new or changed brand direction, composition system, typography, visual hierarchy and aesthetic acceptance. If the user has not supplied an approved brand direction, obtain that bounded design brief before treating any generated candidate as final.

Do not reproduce an existing third-party logo, distinctive wordmark, mascot or trade dress. A named brand reference may inform abstract traits only when the user is authorized to use it; otherwise translate the request into original, brand-neutral characteristics. Generation does not provide trademark clearance or prove uniqueness.

## Brand brief

Lock the following before production. Preserve unknowns instead of inventing business facts:

- exact brand name, language and capitalization;
- optional subtitle, English name or industry descriptor;
- industry, audience, positioning and intended applications;
- personality keywords and explicit avoidances;
- preferred symbol, metaphor or character, when any;
- required and forbidden colors;
- required lockups: symbol-only, wordmark, horizontal, stacked, monochrome or reversed;
- minimum real display size and target formats.

The brand name is semantic content. A visually plausible but misspelled name is a failed asset.

## Direction routing

Select one coherent direction per candidate. Do not blend every available style into one mark.

| Direction | Use when | Primary design question |
|---|---|---|
| Restrained Eastern symbol | A quiet lifestyle, tea, craft, hospitality or cultural brand needs sparse natural imagery | Can a few strokes and negative space remain identifiable without becoming generic decoration? |
| Fine-line character or wordmark | The brand name itself should carry the identity | Is the lettering distinctive, readable and reproducible rather than pseudo-text? |
| Negative-space mark | A primary symbol can contain a meaningful second reading | Does the hidden shape improve recall without harming the first-read silhouette? |
| Conceptual narrative mark | A creative, cultural or experimental brand needs metaphor rather than a literal industry icon | Can one small visual relationship express the concept at logo scale? |
| Refined animal emblem | A lifestyle brand needs an elegant animal identity | Is the animal simplified into a mark rather than rendered as an illustration? |
| Local craft illustrated wordmark | A place, food or craft brand needs locality and handmade warmth | Do the small pictorial cues support the name without turning the logo into a scene? |
| Folk-art wordmark | A warm independent brand benefits from naive print or vernacular character | Does the irregularity feel intentional while the name stays legible? |
| Playful animal mascot mark | A young consumer or service brand needs a memorable personality | Does the character have a clear silhouette and brand role without becoming generic clip art? |
| Character-integrated wordmark | A shop or product brand needs a mascot and name to read as one unit | Are character and lettering structurally integrated rather than stacked as unrelated assets? |
| Bold-line pop mascot | A social, retail or cultural brand needs a strong sticker-like identity | Does it retain a simple contour and limited palette at avatar and label sizes? |

These directions are exploration routes, not a fixed taxonomy or evidence that any one direction fits the brand. Start with the brief, then choose the smallest useful set of candidates.

## Exact text and editable lockups

Image-model lettering is concept material until every character has been verified. For an exact brand name:

1. Generate the symbol, character or text-free visual idea separately when possible.
2. Build the approved wordmark and lockups with editable vector paths or deterministic SVG/HTML/CSS typography.
3. If the requested value is custom-drawn lettering, treat generated glyphs as a sketch; redraw or vectorize them and compare every character against the locked name.
4. Keep the approved symbol raster unchanged while correcting text-only errors. Do not regenerate the entire logo for a spelling or subtitle correction.

Never deliver pseudo-letters, substituted Chinese characters, missing accents or distorted legal marks as final copy.

## Prompt structure

Translate the approved brief into a compact prompt with these sections:

```text
Create an original brand-logo concept for <brand purpose and audience>.
Direction: <one selected direction and its visual traits>.
Core symbol or metaphor: <approved meaning>.
Composition: <symbol-only or reserved space for deterministic wordmark>; simple first-read silhouette; generous safe area.
Palette: <approved limited palette>; include a monochrome-compatible structure.
Applications: <avatar, label, storefront, packaging, product UI, or other real targets>.
Avoid: copied brand marks, generic stock-logo geometry, poster layout, complex scene, mockup, watermark, pseudo-text, unnecessary decoration.
Transparent background, alpha channel, isolated mark, no background layer.
```

Do not send exact text to the model when deterministic lettering will be added later. A presentation mockup may be produced as a separate preview, but it is never the source logo asset.

## Deliverables

Return only the variants required by the brief. A complete logo-system request commonly includes:

- primary lockup with editable wordmark source;
- symbol-only transparent PNG;
- horizontal and stacked variants when both are required;
- full-color, monochrome and reversed variants;
- SVG or another editable deterministic source for exact lettering;
- PNG previews at the requested production and small-display sizes;
- metadata that separates generated pixels from deterministic typography or vector work.

Default the source mark to transparent PNG. Background color, stationery, storefront and packaging views are separate mockups and must not be baked into the source asset.

## Acceptance gates

Reject the result unless all applicable gates pass:

- the brand name, subtitle and punctuation match the locked copy exactly;
- the first-read silhouette is clear in monochrome;
- the mark remains legible at the brief's minimum size, including 128 px, 32 px and 16 px when those uses apply;
- symbol, wordmark and combined lockups remain visually related without mechanical stacking;
- transparent source files have real alpha and no baked square, mockup, border or outside shadow;
- all meaningful pixels fit inside the safe area without clipped strokes or extremities;
- the result does not visibly imitate a supplied third-party logo or reference composition;
- the final package identifies what was generated, redrawn, typeset and technically verified;
- no claim of trademark availability, originality clearance, production adoption or market performance is made without separate evidence.

## Source note

The direction list was expanded after reviewing the public article [“用 AI 做 Logo，第二篇来了：再分享10种风格，附完整提示词”](https://mp.weixin.qq.com/s/YXgqdS8f-wLoIUhQLwNrbQ) by 像素牧羊人 / 像素空间笔记. This workflow paraphrases the high-level directions and adds independent production, text-fidelity and QA requirements; it does not copy the article's prompts or imply endorsement.
