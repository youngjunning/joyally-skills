# macOS

Use this reference for SwiftUI/AppKit windows, menu bar surfaces, settings, dashboards, panels, and popovers. It owns design decisions; API availability, state ownership, profiling, and SwiftUI implementation mechanics remain with the macOS engineering workflow.

## Decision boundary

Native behavior and default appearance are different decisions. Preserve the Mac interaction model, then decide whether the product's existing controls, tokens, and brand require styling. A standard control is acceptable when it already fits the product; a custom appearance is acceptable only while its native semantics and input behavior remain intact.

The platform contract is shared. Palette, corner radius, illustration, and atmosphere belong to the product or selected Joyally theme. Qingshan Lake mist and lake tint are a preset, not the default for every Mac app.

Before styling, identify the app archetype, window model, primary commands, content hierarchy, and expected keyboard-only path. Read the repository deployment target and existing components as product facts.

## Mac interaction contract

- Keep windows useful at minimum, typical, and wide sizes; support resize, move, minimize, zoom, fullscreen, and multiple windows when the product model calls for them.
- Use the larger canvas for comfortable information density and fewer nested levels. Keep frequent actions reachable without repeated modality.
- Make the menu bar a complete command map. Preserve standard App, File, Edit, View, Window, and Help conventions where they apply; keep Settings in the App menu with `⌘,`.
- Provide keyboard equivalents for frequent commands without overriding standard editing shortcuts. Preserve focus movement, pointer hover, secondary click, and VoiceOver.
- Use system text components where people expect selection, undo/redo, copy/paste, spell checking, and Services.
- Do not place the only critical action or information at a window's bottom edge; people can move that edge below the screen.

## Component foundation

- Prefer native `Button`, `Toggle`, `TextField`, `Menu`, `Table`, `NavigationSplitView`, sheet, and alert semantics. Apply project styles before rebuilding an interaction primitive.
- When system selection chrome conflicts with an established product theme, keep the native navigation structure and render a custom row with a stable full-width target, hover, pressed, selected, focus, keyboard, accessibility-selected, and non-color states.
- Use the native macOS control size by default. Apple lists 28×28 pt as the default target and 20×20 pt as the minimum; enlarge important or touch-oriented actions without making the surrounding pointer/keyboard layout needlessly sparse.
- Keep body text near platform defaults and use system text styles where they fit. Long localized strings must reflow or truncate deliberately without hiding the action or state.
- Keep icon-only controls labeled for accessibility. Use SF Symbols for system concepts unless the product owns a clearer symbol.
- Keep selection geometry stable: hover, pressed, selected, focused, loading, and validation states must not move surrounding layout.

## Material and branded surfaces

- Treat material as semantic hierarchy, not a color picker. Use it for a real navigation, control, or separation layer and provide an opaque fallback for Reduced Transparency.
- On systems that support Liquid Glass, reserve it for navigation and control layers; use standard materials or opaque surfaces for dense content. Avoid glass-on-glass and repeated translucent cards.
- Prefer spacing, typography, and alignment over extra containers. A highlight belongs to its host surface: reuse the same shape and clip boundary so it cannot read as a second card.
- Keep sidebars quieter than content; make selection unmistakable through foreground/background contrast, focus, and a non-color cue.
- On light desktops, inspect every translucent edge, corner, and shadow. A correct center does not prove a correct window boundary.
- For transparent `NSPanel` or `NSWindow`, align the SwiftUI clip, hosting-view layer corner, and window background. Use one visible boundary rather than a rectangular system shadow around a rounded surface.

## Surface recipes

- **Dashboard:** stable navigation, title or toolbar, local filters, primary content, and a quiet status area. Use whitespace before adding cards.
- **Settings:** native grouping, direct labels, restrained surfaces, and predictable tab and keyboard order.
- **Menu bar/popover:** compact hierarchy, immediate state, one obvious next action, and no decorative background motion.
- **Floating panel:** one visual boundary, legibility over arbitrary desktops, and verified edge and corner rendering.

## Acceptance

Run the shared [validation gate](validation.md) with the real app. At minimum inspect selected, hover, pressed, focused, disabled, loading, empty, error, and success states; minimum and wide windows; long localized text; keyboard-only and VoiceOver paths; Increased Contrast, Differentiate Without Color, Reduced Motion, and Reduced Transparency. Verify foreground/background pairs after material and desktop tinting are composited.

Decision test: with color removed, the interface still behaves like a Mac app and every important state remains understandable; with native behavior preserved, the product's own visual language remains recognizable during interaction.

## Official sources

- [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/)
- [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
- [Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
- [Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/)
