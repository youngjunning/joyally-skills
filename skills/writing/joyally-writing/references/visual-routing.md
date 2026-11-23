# Visual routing for articles and books

Choose first by the information the reader must recover, then by the artifact the user must keep using. For coordinated inline figures, create the reader-question, placement, caption, alt text, and continuity manifest in [article-illustration-plan.md](article-illustration-plan.md) before selecting production routes. Exact labels, relationships, arrows, and states always require deterministic semantic authoring. `joyally-image` is the single diagram entry point: its static `knowledge-map` branch delivers publishable images, while its `interactive-diagram` branch invokes Archify for editable, zoomable, focusable, or explorable artifacts and produces a static preview from the same source. Joyally Design may supply visual direction, composition or geometry, typography, and design acceptance without becoming a second diagram owner. An existing diagram keeps its editable source as the source of truth.

## Selection

| Reader need and artifact | Default owner | What stays deterministic |
| --- | --- | --- |
| Interactive, editable, zoomable, or explorable architecture, workflow, sequence, dataflow, or lifecycle diagram | joyally-image `interactive-diagram`, using the matching Archify type | Nodes, containment, ordering, edges, labels, states, and evidence |
| Static architecture, knowledge map, flow, sequence, dataflow, or lifecycle image for an article, slide, or share | joyally-image `knowledge-map` | Nodes, containment, ordering, edges, labels, states, and evidence |
| Scene-led or identity-led cover, editorial illustration, atmosphere, portrait, texture | joyally-image | Exact titles, figures, identifiers, or captions added outside the raster model when needed |
| Comic article with recurring characters, scene actions, and dialogue | [comic-articles.md](comic-articles.md) owns article integration; joyally-design leads comic design; joyally-image produces pixels | Dialogue, commands, facts, reading order, and any explanatory relationships |
| Statistical charts, scientific plots, numeric comparisons | Standard plotting tools | Data, scales, axes, units, uncertainty, legends |
| Lookup, specifications, small comparisons | Markdown or document table | Values and column meanings; an image is often unnecessary |
| Current product behavior or an observed failure | Real screenshot or recording | Provenance and any annotations; identify a mockup as illustrative |

Read the selected skill before producing the asset. For interactive work, `joyally-image` discovers the actual available Archify entrypoint, including a project-owned Joyally Design integration when required by that project. Do not hardcode a repository path into this reusable writing rule. Tool mechanics, schemas, validation commands, styling, and upload procedures remain owned by their respective skills and destination repository.

## Archify boundary

Use joyally-image's `interactive-diagram` route when the requested diagram must remain interactive, editable, zoomable, or explorable, or when an existing Archify source remains the source of truth. Model the entities and relations from evidence first; render and validate them with the selected schema. Keep the editable specification beside every delivered artifact.

When an article includes that interactive artifact, use a readable static export inline and provide the interactive HTML as a companion. Both remain part of the same Joyally Image workflow because they are derived from one interactive source. An HTML-only delivery is insufficient for a renderer that strips iframes. Validate both forms and inspect text and arrows at the article's actual reading width. Preserve required relationship labels instead of deleting them to make a layout pass.

A domain taxonomy, annotated illustration, geographic map, or unusual knowledge layout may not fit Archify. Use a deterministic SVG/HTML or specialist renderer when its grammar expresses the subject more accurately. Do not force every labeled visual into a component diagram. A simple relationship may be clearer as one sentence or a table.

## joyally-image boundary

Use joyally-image as the overall delivery workflow for diagrams and when the deliverable's contribution is appearance, scene, identity, mood, or raster artwork. A broader new visual system, brand adaptation, or cross-channel composition contract may use `joyally-design`; a self-contained diagram does not require a second Skill to start. Follow the cover brief and acceptance requirements in `article-cover.md` for article covers. Keep covers distinct from explanatory figures.

Its `knowledge-map` workflow uses deterministic HTML/CSS/SVG for every semantic element; the image model supplies only an optional text-free backdrop. Use that workflow for new static architecture, knowledge-map, flow, sequence, dataflow, and lifecycle images. Apply an existing visual system as locked input, or ask Joyally Design for review only when the task needs a broader design decision. Exact semantics remain a hard acceptance condition inside the image workflow.

For a mixed figure, generate only the visual layer that benefits from generation. Render exact labels, numbers, arrows, UI annotations, and state distinctions separately, then check the composite. Skip the generated background when it adds no explanatory value. Existing vector diagrams should normally be edited in their source format.

## Mixed examples

| Request | Route and acceptance |
| --- | --- |
| “写 AnyUse 架构文章，配封面和架构图” | joyally-image creates both static assets and runs type-specific QA; use joyally-design only if a broader visual system must be established; verify cover and semantic diagram independently |
| “把白板草图整理成可缩放的框架图” | Recover the intended topology, mark ambiguous handwriting, then use joyally-image `interactive-diagram` with Archify; do not treat handwriting as confirmed evidence |
| “做一张静态 PNG 的请求时序图” | joyally-image `knowledge-map` produces and exports it; keep participants, ordering, direction, and labels deterministic |
| “知识体系画成河流或山脉，术语必须准确” | Custom deterministic semantic labels over optional joyally-image scenery; use real coordinates and a legend only if they carry meaning |
| “对比三种执行器的成功率和 P95” | Verified measurements in a table or plotting tool; neither a generated chart nor an architecture diagram supplies evidence |
| “保持这张插画的人物，换背景” | Image-edit workflow with the identity reference; preserve identity rather than rebuilding it as diagram nodes |
| “只改现有 SVG 的一个节点名称” | Edit the existing vector source and revalidate references/layout; image generation is unnecessary |

## Handoff check

1. Each figure answers one named reader question and is placed near the claim it explains. Add another figure when it reduces a real reading burden, without a fixed count or a diagram quota.
2. Compare node names, relationships, ordering, states, numbers, and uncertainty with the source independently of visual polish. A generated backdrop cannot establish a system fact.
3. Inspect the final composite or static export at reading size for legibility, clipping, crossings, and missing fonts. A valid source specification is not proof of a readable export.
4. Keep editable source, exported asset, uploaded asset, article rendering, and publication status separate. Use the destination's existing upload and readback contract only when authorized.
5. If a preferred tool is unavailable, preserve the semantic contract with an available deterministic renderer or keep the affected figure explicitly unfinished. Never silently substitute a plausible raster picture for a verified diagram.

## Basis and maintenance

Routing revised on 2026-11-22 so all diagram requests enter joyally-image, whose static and interactive branches use deterministic Knowledge Map and Archify respectively. This is a writing-layer selection rule, not a fork of those tool manuals; consult their current instructions for generation and validation.
