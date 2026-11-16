# Validation

## Shared acceptance gate

Do not claim completion from source inspection or a successful build alone.

1. Render the real app or page with representative content.
2. Check primary workflow, empty, loading, error, success, disabled, focused, pressed, and selected states.
3. Verify the smallest and largest supported window/viewport plus one intermediate state.
4. Test long text and localization expansion.
5. Test keyboard or hardware-key navigation where supported.
6. Inspect with VoiceOver, TalkBack, or browser accessibility tools as appropriate.
7. Enable Reduced Motion, Reduced Transparency or opaque fallback, Increased Contrast, and Differentiate Without Color/forced colors where available.
8. Check light and dark appearances when supported.
9. Verify every visible component state's foreground/background pair from computed or runtime colors, not only source hex values. Normal text must reach 4.5:1; large text, disabled labels, functional icons, and visible control boundaries must reach 3:1. A local background override must carry its matching foreground override in the same scope.
10. Inspect performance while atmosphere is idle, offscreen, and backgrounded.
11. For rounded interactive containers such as report disclosures, inspect all four corners in default, hover, keyboard focus, and expanded states. The fill must remain clipped inside one continuous border; use the bundled `report-disclosure` pattern for generated reports.

## Style gate

- The screen expresses the product's own brand without relying on a literal scenic image.
- Primary action, navigation, and status are immediately legible.
- Light, translucent, gradient, and image-backed controls use a foreground proven against the rendered surface. White text on a light surface and dark text on a dark surface are incomplete states, including disabled and loading states.
- In Web pages, every new or changed interactive control uses the chosen component foundation and semantic tokens in its rendered default, hover, focus, disabled, and error states. Native HTML may provide semantics and behavior, but browser-default chrome is not a finished component. Verify the actual page visually and inspect computed styles; a class name or imported stylesheet alone is insufficient evidence.
- Where the browser or operating system still draws a control surface, such as a native select menu or file picker, check it in the target browser. If its appearance breaks the intended interface, use an accessible component that owns that surface and preserves keyboard, focus, and form behavior.
- Atmospheric effects never sit between users and dense content.
- Color, imagery, and material choices follow the chosen brand and content.
- Decorative patterns serve hierarchy and meaning rather than filling empty space.
- Custom styling preserves the platform's semantics and input behavior.

## Token gate

Run:

```bash
python3 scripts/validate-native-tokens.py
```

The script validates required roles, hex syntax, token references, and declared WCAG contrast pairs in `assets/joyally-native.tokens.json`.

## Handoff evidence

Report these states independently:

- design contract written;
- source implemented;
- static validation passed;
- build/test passed;
- real UI inspected;
- device/platform accessibility inspected;
- committed and pushed;
- deployed;
- production verified.
