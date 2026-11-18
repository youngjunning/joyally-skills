# Visual routing for articles and books

Choose first by the information the reader must recover, then by the artifact the user must keep using. Exact labels, relationships, arrows, and states always require deterministic semantic authoring. Artifact form decides the overall workflow: `joyally-design` owns diagrams that must remain interactive, editable, zoomable, or explorable; `joyally-image` can own final delivery of static publishable diagram images. Joyally Design still owns the visual direction, composition or geometry, typography, and design acceptance for those static images, while Joyally Image owns pixel production, export, and technical image QA. An export of an existing interactive diagram stays with its source workflow.

## Selection

| Reader need and artifact | Default owner | What stays deterministic |
| --- | --- | --- |
| Interactive, editable, zoomable, or explorable architecture, workflow, sequence, dataflow, or lifecycle diagram | joyally-design with the matching Archify type | Nodes, containment, ordering, edges, labels, states, and evidence |
| Static architecture, knowledge map, flow, sequence, dataflow, or lifecycle image for an article, slide, or share | joyally-image `knowledge-map` overall; joyally-design leads its design phase | Nodes, containment, ordering, edges, labels, states, and evidence |
| Scene-led or identity-led cover, editorial illustration, atmosphere, portrait, texture | joyally-image | Exact titles, figures, identifiers, or captions added outside the raster model when needed |
| Comic article with recurring characters, scene actions, and dialogue | [comic-articles.md](comic-articles.md) owns article integration; joyally-design leads comic design; joyally-image produces pixels | Dialogue, commands, facts, reading order, and any explanatory relationships |
| Statistical charts, scientific plots, numeric comparisons | Standard plotting tools | Data, scales, axes, units, uncertainty, legends |
| Lookup, specifications, small comparisons | Markdown or document table | Values and column meanings; an image is often unnecessary |
| Current product behavior or an observed failure | Real screenshot or recording | Provenance and any annotations; identify a mockup as illustrative |

Read the selected skill before producing the asset. For interactive work, discover the actual available Archify entrypoint, including a project-owned Joyally Design integration when required by that project. Do not hardcode a repository path into this reusable skill. Tool mechanics, schemas, validation commands, styling, and upload procedures remain owned by their respective skills and destination repository.

## Archify boundary

Use Joyally Design with Archify when the requested diagram must remain interactive, editable, zoomable, or explorable, or when an existing Archify source remains the source of truth. Model the entities and relations from evidence first; render and validate them with the selected schema. Keep the editable specification beside every delivered artifact.

When an article includes that interactive artifact, use a readable static export inline and provide the interactive HTML as a companion. This export remains part of the Joyally Design workflow because it is derived from the interactive source; it does not create a second owner. An HTML-only delivery is insufficient for a renderer that strips iframes. Validate both forms and inspect text and arrows at the article's actual reading width. Preserve required relationship labels instead of deleting them to make a layout pass.

A domain taxonomy, annotated illustration, geographic map, or unusual knowledge layout may not fit Archify. Use a deterministic SVG/HTML or specialist renderer when its grammar expresses the subject more accurately. Do not force every labeled visual into a component diagram. A simple relationship may be clearer as one sentence or a table.

## joyally-image boundary

Use joyally-image as the overall delivery workflow when the deliverable is a static publishable image or when its contribution is appearance, scene, identity, mood, or raster artwork. Before pixel production, give any new visual direction, composition or geometry, typography, brand adaptation, and design acceptance criteria to `joyally-design`. Follow the cover brief and acceptance requirements in `article-cover.md` for article covers. Keep covers distinct from explanatory figures.

Its `knowledge-map` workflow uses deterministic HTML/CSS/SVG for every semantic element; the image model supplies only an optional text-free backdrop. Use that workflow for new static architecture, knowledge-map, flow, sequence, dataflow, and lifecycle images after Joyally Design approves the geometry, hierarchy, typography, and design system. Exact semantics remain a hard acceptance condition inside the image workflow.

For a mixed figure, generate only the visual layer that benefits from generation. Render exact labels, numbers, arrows, UI annotations, and state distinctions separately, then check the composite. Skip the generated background when it adds no explanatory value. Existing vector diagrams should normally be edited in their source format.

## Mixed examples

| Request | Route and acceptance |
| --- | --- |
| “写 AnyUse 架构文章，配封面和架构图” | joyally-design approves two separate visual briefs; joyally-image creates both static assets and runs technical QA; verify cover and semantic diagram independently |
| “把白板草图整理成可缩放的框架图” | Recover the intended topology, mark ambiguous handwriting, then use Joyally Design with Archify; do not treat handwriting as confirmed evidence |
| “做一张静态 PNG 的请求时序图” | joyally-design approves geometry and typography; joyally-image `knowledge-map` produces and exports it; keep participants, ordering, direction, and labels deterministic |
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

Routing reviewed on 2026-11-18 against Joyally Design's Archify paths, joyally-image's `portrait`, `text-poster`, and `knowledge-map` references, and this skill's cover contract. This is a writing-layer selection rule, not a fork of those tool manuals; consult their current instructions for generation and validation.
