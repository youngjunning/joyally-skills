# Animated and two-tone UI icons

Use this route for functional UI icons that change on hover, focus, press, tap, or a controlled product state, including two-tone or filled icon families delivered as SVG or framework components. This route is deterministic vector production and does not use the image API unless the approved brief separately requires a raster layer.

Do not use it for a brand logo, app-store or Dock icon, decorative raster pictogram, sprite animation, or a general product-motion study. A static 16–24px raster navigation family still uses `navigation-icon.md`; a frame sequence still uses `sprite-loop.md`.

## Asset contract

Lock these fields before choosing a source or drawing:

- product meaning and the everyday object or silhouette that expresses it;
- target platform: React, Vue, plain JavaScript, Web Component, standalone SVG, or a native surface;
- actual sizes and optical keyline, including the smallest shipping size;
- static, animated, or both; rest, hover, focus, pressed, active, disabled, and reduced-motion behavior;
- single accent, brand tokens, or two-tone palette, with required light and dark surfaces;
- decorative versus meaningful semantics, accessible name ownership, and the element that triggers motion;
- delivery source, runtime dependency, bundle budget, and acceptance environment.

Choose filled or two-tone geometry when the icon must remain clear at 16–48px or the user explicitly asks for `filled`, `solid`, `bulk`, `two-tone`, `duotone`, `面性`, `实心` or `双色`. Choose a more layered construction only when the approved visual direction and available space support its extra depth. Motion must enact the object's meaning rather than add an unrelated bounce, spin, glow, or flourish.

## Reuse before drawing

Search the target product and the official [Kubai Icons catalog](https://icons.kubai.design/icons/) before creating a new icon. When an existing Kubai icon fits the approved visual direction and semantics, use the official package for the consumer:

- `kubai-icons-react` for React and Next.js;
- `kubai-icons-vue` for Vue and Nuxt;
- `kubai-icons` for plain JavaScript or its Web Component;
- `kubai-icons-static` for standalone SVG.

Import only the required module and follow the current official integration guide. The icons, badges, two-tone icon data, and published packages are MIT-licensed; preserve the required copyright notice when source is copied or redistributed. Do not copy the website, documentation layout, name, logo, or other non-icon assets.

The Kubai drawing Skill, its prompts, engine, examples, self-check, website, and two-tone style rules have separate licenses. Do not copy, adapt, translate, or re-publish those rules inside Joyally Image. This reference defines Joyally's routing and acceptance contract independently.

## Drawing a missing icon

If the user explicitly selects Kubai, an existing product already uses it, or its visual grammar is approved in the current brief, use the official `kubai-icons` Skill as an external production backend. Prefer an already installed official copy. Otherwise, use the current official release in a task-scoped workspace without adding it to Joyally's source tree. Read and run the upstream files in place, keep their notices, and return only the permitted output or project integration.

If Kubai's appearance is not approved, create an original deterministic SVG or component from the locked product direction. Capability provenance does not choose the visual style: do not inherit Kubai's palette, layering, outlines, geometry, examples, or motion grammar merely because this reference cites it.

For either backend:

1. map each feature to one clear object and one semantic state change;
2. keep rest and end states valid standalone icons;
3. animate explicit vector parts or controlled state, never a flattened raster approximation;
4. keep geometry, frame order, color derivation, clipping, and runtime triggers deterministic;
5. export a static rest state whenever the target cannot run the animation.

## Interaction and accessibility

- Motion must work from the component's real interaction owner. A button may trigger its child icon; do not require a tiny SVG-only hover target when the whole control is interactive.
- Provide pointer, keyboard-focus, touch, and controlled-state behavior appropriate to the platform. Hover alone is not a complete interaction contract.
- Respect `prefers-reduced-motion`. The reduced state must remain semantically clear and must not flash, loop, or preserve a confusing half-state.
- Decorative icons are hidden from assistive technology. Meaningful standalone icons receive an accessible name once, at the correct control or SVG boundary.
- Avoid layout shift, duplicate focus targets, event-listener leaks, hydration drift, and an always-running animation loop.

## Acceptance gates

Review every icon beside at least two approved neighbors and verify:

1. semantics are recognizable in the rest state and at the smallest shipping size;
2. optical size, baseline, weight, corner language, negative space, and palette match the family;
3. a two-tone icon visibly uses both roles with sufficient contrast on required surfaces;
4. meaningful parts stay inside the view box through the full motion and are never clipped;
5. the first, intermediate, and final frames contain no jump, seam, collision, unintended overlap, or dead pause;
6. hover, focus, tap or controlled state, and reduced motion behave in the target runtime;
7. the production build imports only intended modules and the rendered icon has no console, hydration, or accessibility errors.

Deliver the editable SVG or component source, any required runtime integration, static fallback when needed, and a short manifest recording platform, sizes, states, palette tokens, trigger ownership, reduced-motion behavior, source or upstream version, and validation performed. A successful package install or SVG export does not prove the icon passed target-runtime acceptance.
