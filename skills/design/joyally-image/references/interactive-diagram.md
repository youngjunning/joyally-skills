# Interactive diagrams

Use this route when the diagram itself must remain clickable, zoomable, editable, focusable, presentable, or explorable. `joyally-image` owns the complete diagram package and its bundled runtime. Do not expose the upstream implementation name in ordinary replies, artifacts, captions, metadata, or reader-facing documentation; retain it only in licenses, provenance, compatibility internals, or explicit implementation debugging.

## Contract

1. Lock the reader question, evidence, node and boundary names, relationships, direction, ordering, states, uncertainty, and required interactions before styling.
2. Resolve this Skill's own generic entrypoint, `scripts/joyally-diagram.mjs`, relative to the active `joyally-image` directory. Do not discover the runtime through `joyally-design`, and do not hardcode a user or repository path into the artifact.
3. Select the matching typed JSON IR: architecture, workflow, sequence, dataflow, lifecycle, ERD, tree, class, timeline, waterfall, or explainer. Preserve that IR beside the delivered artifact as the editable semantic source.
4. Validate the IR, deliver a self-contained HTML viewer, then create a readable static preview from the same source. The interactive HTML and static preview form one package; do not maintain separate semantics.
5. Inspect the final viewer at desktop and narrow widths. Verify keyboard access, focus and path exploration, zoom, long labels, printing, and Reduced Motion. Re-run browser geometry gates after any coordinate, font, label, edge, or CSS change.

## Acceptance

- Typed validation passes and every visible label, edge, boundary, state, and source marker matches the locked evidence.
- The HTML is self-contained or follows the destination's explicit embed contract; the static preview remains understandable where interaction is unavailable.
- The editable IR, delivered HTML, static preview, browser evidence, upload result, and publication status are reported separately.
- A zero-error schema result is not visual proof. Missing browser measurement, inaccessible interaction, unreadable print output, or untested narrow layout remains explicit.

If the bundled interactive runtime is missing, treat the Skill installation as incomplete. Preserve the same semantic contract with a deterministic HTML/SVG fallback only when that still satisfies the requested interactions, and mark every unsupported interaction as unfinished. Never replace a verified diagram with a plausible generated picture.

## Generic command

Use the public Joyally Image entrypoint for validation and delivery:

```bash
node <joyally-image-dir>/scripts/joyally-diagram.mjs validate architecture input.json --quality showcase --json
node <joyally-image-dir>/scripts/joyally-diagram.mjs deliver architecture input.json output.html --quality showcase --json
```

`scripts/joyally-archify.mjs` remains a filename-only compatibility alias inside Joyally Image. New documentation, examples, CI and callers use only `joyally-diagram.mjs`.

## Migration from Joyally Design

The runtime no longer belongs to Joyally Design. Update callers as follows:

| Deprecated call | Canonical call |
| --- | --- |
| `node <joyally-design>/scripts/design-engine.mjs diagram <args>` | `node <joyally-image>/scripts/joyally-diagram.mjs <args>` |
| `node <joyally-design>/scripts/joyally-diagram.mjs <args>` | `node <joyally-image>/scripts/joyally-diagram.mjs <args>` |
| `node <joyally-design>/scripts/joyally-archify.mjs <args>` | `node <joyally-image>/scripts/joyally-archify.mjs <args>` for temporary filename compatibility, then migrate to `joyally-diagram.mjs` |

Joyally Design retains only a deprecated forwarder for existing callers and never bundles or discovers a diagram runtime of its own. The forwarder requires `joyally-image` to be installed beside it and emits an actionable error when that optional companion is absent. A standalone Joyally Image installation does not require Joyally Design.
