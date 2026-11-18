# Article illustration production

Use this workflow for a coordinated set of inline figures for an article, ATA, tutorial, report, or document. It supplements the type-specific image references; it does not replace them.

When `joyally-writting` is available, consume its approved illustration manifest and keep its reader question, locked facts, caption, alt text, and insertion anchor unchanged. When this skill is used independently with a source document, first create the smallest equivalent manifest: figure ID, purpose, reader question, anchor, locked semantics, route, brief, caption, alt text, dimensions, continuity group, and status. Do not rewrite the article merely to make image production easier.

## Produce by purpose

- **Explain:** use deterministic diagrams for mechanisms, flows, relationships, boundaries, and states; generate only an optional text-free visual layer.
- **Compare:** lock the comparison basis, categories, order, values, and units before layout. Use a table or chart when imagery would obscure the comparison.
- **Resonate:** build one recognizable scene or analogy from the article's actual friction. Keep humor humane and specific; do not fabricate a user story, metric, failure, quotation, or product behavior.
- **Introduce:** create a section-opening visual that establishes the next question or metaphor without duplicating the article cover.
- **Prove:** use supplied real screenshots, recordings, or verified data. Do not regenerate evidence as plausible-looking UI or imagery.

After choosing the purpose, load the matching type reference from `SKILL.md`. A coordinated set may use several asset types; each asset still follows exactly one production route and its validation gates.

## Lock the set before generating

Create one shared continuity brief for the set: palette, rendering or material style, typography and exact-text method, line and icon treatment, background density, aspect-ratio family, recurring metaphor or cast, and exclusions. Reuse these fields across prompts. Keep each figure's composition responsive to its own reader question instead of cloning a single template.

For every figure, separate:

- **semantic lock:** claims, labels, data, relationships, chronology, comparison basis, evidence provenance, caption, and insertion anchor;
- **visual freedom:** framing, scene staging, texture, lighting, decorative details, and other choices that do not change meaning;
- **continuity lock:** palette, recurring identities or props, illustration language, and typography conventions shared with the set.

Exact text, numbers, arrows, UI annotations, and state distinctions use deterministic HTML/CSS/SVG, a plotting tool, or the destination's native document layer. The image model may produce only the portion that benefits from raster generation.

## Deliver an insertion-ready asset pack

Return each accepted figure with:

1. stable figure ID and final path;
2. actual dimensions, format, file size, generation or edit metadata, and editable/deterministic source when required;
3. approved caption and alt text from the manifest, or clearly marked drafts when no writing owner approved them;
4. exact insertion anchor and placement direction;
5. validation evidence for the selected route;
6. manifest status updated to `produced`, then `inserted` only after the destination document is actually changed and rendered successfully.

Keep the article's cover outside this set unless its separate cover brief is also in scope. A local asset, successful API response, or uploaded URL does not by itself prove correct insertion or publication.

## Revision and continuation

For requests such as “换风格”, “更幽默一点”, “只重做第二张”, or “补一张章节引入图”, update the selected figure IDs and shared continuity fields only as far as requested. Preserve locked semantics, accepted captions, anchors, dimensions, and unaffected assets. If a shared style change affects the whole set, show or generate one representative candidate before replacing every accepted figure unless the user explicitly asked for a full regeneration.

Reject a visually attractive revision when it changes factual content, removes a needed distinction, turns evidence into illustration, breaks identity continuity, or no longer answers the recorded reader question.

## Set-level acceptance

- Every figure passes its type-specific technical gate and a full-resolution plus reading-size visual review.
- The set feels coherent in palette, rendering, typography, and density while compositions remain purpose-specific.
- Captions, alt text, filenames, anchors, and manifest IDs stay aligned.
- Exact semantics are independently compared with the source after compositing.
- The destination document is rendered after insertion and checked for legibility, clipping, broken links, awkward spacing, and duplicate or orphaned figures.
