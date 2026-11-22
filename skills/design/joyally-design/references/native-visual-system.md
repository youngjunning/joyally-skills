# Qingshan Lake visual system preset

This file is a concrete theme sample for Joyally's Qingshan Lake identity. Other themes and products reuse the semantic token roles and validation approach with their own palette, material, and imagery.

## Character

Translate landscape layers into interface responsibilities:

| Landscape cue | Product responsibility |
| --- | --- |
| Mist white | canvas, breathing room, soft material |
| Lake teal | primary action, selection, focus, progress |
| Cypress green | success, online, growth, completion |
| Gray-blue hills | secondary text, structure, inactive states |
| Neutral lake-shore ink | primary text without adding another scenic green |
| Duckweed | no more than 5% natural liveliness |
| Dawn light | rare emphasis, warning, reward, edge light |
| Wet wood / clay | grounded separators and restrained danger |

The system must feel quiet, translucent, natural, precise, and useful. It is landscape distillation, not landscape illustration.

## Core tokens

Use Seed → Map → Alias → Component mapping; `semantic` stores Alias roles. Never consume scenic seed names directly inside arbitrary components when a semantic role exists.

| Role | Default | Notes |
| --- | --- | --- |
| Canvas | `#F8F7F3` | warm mist, low noise |
| Surface | `#FFFDFB` | readable content surface |
| Surface muted | `#EDF3F1` | filters, secondary containers |
| Text | `#23393D` | neutral ink, not a scenic green |
| Text secondary | `#52696B` | passes normal-text contrast on canvas |
| Primary | `#63ACA2` | visual accent; do not place small white text on it |
| Primary action | `#78BEB3` | clear lake fill paired with `#23393D` text |
| Focus | `#57958E` | visible boundary without becoming a large dark fill |
| Primary container | `#E1F2EE` | selected or informative background |
| Success | `#356439` | accessible foreground role |
| Warning | `#7A5B1E` | accessible foreground role |
| Error | `#8E493E` | accessible foreground role |
| Border | `#D9E5E2` | subtle division, not primary structure |
| Dark canvas | `#1D3036` | dark-mode neutral, never pure black |
| Dark surface | `#253A40` | lifted dark-mode layer |
| On dark | `#F4F8F6` | mist-white content |

The scenic palette remains available for gradients, illustration, charts, and atmosphere. The light theme has no deep-lake-green seed: large actions and selected surfaces stay in the clear lake range with dark text, while stronger teal is limited to small text, icons, and focus boundaries.

## Type and spacing

- Use the platform system font unless the product already owns a legible brand typeface.
- Use an 8-unit spacing rhythm; allow 4-unit micro gaps and 20–32-unit section separation.
- Keep body copy readable and line lengths controlled. Do not make every section a centered marketing block.
- Default corners: 6–12 for dense controls, 12–20 for touch cards, larger only for a hero or expressive container.
- Use pills only for tags, segmented selections, compact status, or controls whose semantics benefit from the shape.

## Surface rules

- Start with an opaque readable surface. Add transparency only when background context improves orientation or atmosphere.
- Use one material layer per hierarchy boundary. Avoid glass cards inside glass cards.
- Keep borders at one physical pixel where possible; increase contrast rather than thickness for emphasis.
- Keep shadows cool, broad, and faint. Remove them if they create dirty gray edges on light backgrounds.
- For Reduced Transparency, replace glass with an opaque surface while preserving hierarchy.

## Motion rules

- Use motion to explain state, navigation, loading, or spatial continuity.
- Typical interface transitions: 120–220ms. Narrative reveals can extend to about 500–700ms when they happen once.
- Animate compositor-friendly properties on the web. Gate canvas and timeline work by visibility and interaction.
- Under Reduced Motion, replace travel, scale, parallax, and depth animation with no animation or a short fade.
- Atmospheric motion should be noticed after looking away, not while reading.

## Provenance

The language was distilled from working implementations in a native macOS productivity app, a professional AI workspace, a product landing page, and a public design-language atlas. Public examples include Owlet and Design Language Atlas. Source-specific product identifiers, assets, and architecture are intentionally excluded from this reusable specification.
