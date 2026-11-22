# Interactive diagrams

Use this route when the diagram itself must remain clickable, zoomable, editable, focusable, presentable, or explorable. `joyally-image` stays the user-facing owner for the complete diagram package; Archify is the rendering backend, not a second intake path.

## Contract

1. Lock the reader question, evidence, node and boundary names, relationships, direction, ordering, states, uncertainty, and required interactions before styling.
2. Discover the current Joyally Archify entrypoint from the environment. Prefer the installed `joyally-design/scripts/design-engine.mjs diagram` integration when available; a destination-owned integration may override it. Do not hardcode a user or repository path into the artifact.
3. Select the matching typed JSON IR: architecture, workflow, sequence, dataflow, lifecycle, ERD, tree, class, timeline, waterfall, or explainer. Preserve that IR beside the delivered artifact as the editable semantic source.
4. Validate the IR, deliver a self-contained HTML viewer, then create a readable static preview from the same source. The interactive HTML and static preview form one package; do not maintain separate semantics.
5. Inspect the final viewer at desktop and narrow widths. Verify keyboard access, focus and path exploration, zoom, long labels, printing, and Reduced Motion. Re-run browser geometry gates after any coordinate, font, label, edge, or CSS change.

## Acceptance

- Typed validation passes and every visible label, edge, boundary, state, and source marker matches the locked evidence.
- The HTML is self-contained or follows the destination's explicit embed contract; the static preview remains understandable where interaction is unavailable.
- The editable IR, delivered HTML, static preview, browser evidence, upload result, and publication status are reported separately.
- A zero-error schema result is not visual proof. Missing browser measurement, inaccessible interaction, unreadable print output, or untested narrow layout remains explicit.

If no Archify backend is available, preserve the same semantic contract with a deterministic HTML/SVG implementation and mark unsupported interactions as unfinished. Never replace a verified diagram with a plausible generated picture.
