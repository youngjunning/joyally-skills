# Article illustration planning

Use this workflow when an article, ATA, tutorial, report, or document needs inline figures rather than only a cover. The writing workflow owns why each figure exists, which claims it may express, where it belongs, and the caption and alt text. `joyally-image` owns static or interactive diagram and raster-artwork production; `joyally-design` may supply a broader visual system and design acceptance.

## Plan from reader questions

Read the complete source before proposing figures. Preserve the article's headings, claims, evidence, uncertainty, terminology, and intended audience. For each candidate, name the question that becomes easier to answer with a visual. Keep only figures that reduce a real reading burden.

Choose the figure's primary job:

- **Explain:** make a mechanism, sequence, relationship, boundary, state change, or abstract concept recoverable at a glance.
- **Compare:** expose meaningful similarities, differences, tradeoffs, before/after states, or alternatives on a common basis.
- **Resonate:** use a restrained scene, analogy, or humorous moment to make a genuine reader frustration recognizable without inventing facts or turning the article into decoration.
- **Introduce:** open a major section with a scene or visual metaphor that orients the reader to the next question. Do not repeat the cover or merely restate the heading.
- **Prove:** show verified data, a real product state, or an observed failure with a chart, table, screenshot, or recording rather than generated evidence.

Do not assign a figure quota or illustrate every heading. Merge candidates that answer the same question. Prefer prose or a table when the relationship is already simple; prefer a figure when readers must recover several entities, three or more ordered steps, branches, dependencies, ownership, state, or spatial structure.

## Choose the truthful form

Use [visual-routing.md](visual-routing.md) after the purpose is clear.

- Exact labels, numbers, relationships, arrows, states, or comparisons stay deterministic.
- Real product behavior uses an actual screenshot or recording with provenance; generated UI must be labeled illustrative.
- Scene-led illustrations may carry mood, analogy, recognition, or a section transition, but they do not establish a system fact.
- Charts and tables use verified data and conventional plotting or document tools.
- Covers and inline figures are separate assets with separate briefs and acceptance checks.

## Create the illustration manifest

Before production, write one manifest row per accepted figure. A Markdown table is sufficient for a short article; JSON or YAML is useful when the destination has an automated asset pipeline.

Each row records:

1. stable figure ID and primary job;
2. the reader question it answers;
3. insertion anchor as an exact heading plus `before` or `after`, or a unique surrounding sentence when headings are insufficient;
4. source claims, evidence, labels, data, relationships, and uncertainty that are locked;
5. selected artifact route and why it fits;
6. concise visual brief, aspect ratio or destination width, and must-preserve elements;
7. approved caption and useful alt text;
8. continuity group, if several figures share a visual system, metaphor, or recurring cast;
9. status: `planned`, `approved`, `produced`, `inserted`, or `blocked`.

The manifest is a production contract, not a prompt dump. Do not copy the whole article into every brief. Include only the nearby context and locked facts required to make that figure correct.

## Keep a coherent visual system

For a multi-figure article, define one compact system before production: palette, material or rendering style, typography rules, line and icon treatment, background density, caption convention, and any recurring metaphor or character. Reuse it across the set while allowing composition to follow each figure's job. Consistency does not mean making every figure the same layout.

For a new or changed system that spans several assets or channels, ask `joyally-design` to approve it, then give the approved system and each manifest row to `joyally-image`. For a self-contained figure set, use explicit user constraints, the destination's existing design language, or the image skill's documented default; disclose whether a separate design review occurred.

## Insert and continue

An image file alone is not a finished article illustration. Place every produced asset at its recorded anchor, add the approved caption and alt text in the destination's supported syntax, and inspect the rendered article at its real reading width. Keep local source, exported asset, uploaded asset, and publication status distinct.

For a follow-up such as “换成更克制的风格”, “这一张太严肃”, or “补一张对比图”, preserve accepted figure IDs, locked semantics, captions, insertion anchors, dimensions, and unaffected assets unless the request changes them. Revise only the selected brief or the shared visual-system fields that actually changed. A style change must not silently alter claims, labels, chronology, comparison basis, or product evidence.

## Acceptance gate

- Every figure answers its named reader question and is near the claim it explains.
- Labels, values, relationships, ordering, states, and uncertainty match the source independently of visual polish.
- Caption and alt text describe what the figure proves or illustrates without adding a stronger claim.
- Exact text is rendered deterministically, not trusted to a raster model.
- Figures in the same continuity group feel related at reading size without collapsing into repetitive templates.
- No figure is clipped, illegible, orphaned from its explanation, or left as an uninserted local file while the article is called complete.
- Blocked production, upload, rendering, or publication remains explicit in the manifest and handoff.
