---
name: joyally-media
description: Extract evidence-backed content from Bilibili, WeChat Channels or Official Account video links, other hosted video pages, direct media URLs, and uploaded or local audio/video. Use when the user asks for subtitles, transcription, timestamped notes, a summary, a breakdown, or source material for later writing. Not for creating or editing media.
---

# Joyally Media

Turn audio and video into source notes whose coverage and evidence can be judged. Own media intake, transcription, frame inspection, and content extraction; leave fiction, articles, design, and video production to their respective workflows after the source notes are ready.

## Route the input

- **Hosted page:** resolve redirects, identify the canonical page and selected episode or part, then obtain the accessible metadata and media evidence.
  - For Bilibili URLs, read [references/bilibili.md](references/bilibili.md).
  - For WeChat Channels, Official Account, or WeChat share links, read [references/wechat-video.md](references/wechat-video.md).
- **Direct media URL:** verify that the response is audio or video rather than an HTML page before reading it.
- **Uploaded or local media:** preserve the original file and work from a temporary copy when conversion, clipping, or frame extraction is needed.
- **Transcript or subtitle supplied by the user:** treat it as primary text evidence, retain its timestamps when present, and inspect the media only where visuals or transcription quality matter.

Use a host-native media-reading tool when it can read the actual input and return timestamps or grounded detail. Otherwise use available local tools for metadata, subtitles, audio transcription, and frame extraction. Tool availability changes by host, so inspect the current environment instead of promising a specific provider.

## Build the evidence set

1. **Resolve the source.** Record the original URL, canonical URL, platform, title, creator, duration, publication date when available, and the exact part or time range being analyzed. A page title or search result is metadata, not video content.
2. **Choose coverage.** Follow the user's requested range. When unspecified, cover the complete selected item. For long media, process it in sections and state any omitted range rather than silently sampling.
3. **Acquire speech evidence.** Prefer creator-provided subtitles, then platform-generated captions, then transcription from the authorized audio. Record which source was used and its language. Keep automatic speech recognition errors distinguishable from the speaker's words.
4. **Acquire visual evidence.** Inspect frames at chapter changes, demonstrations, diagrams, code, tables, or moments where speech refers to the screen. Fixed-interval sampling is a fallback for discovering such moments, not proof that every important visual was captured.
5. **Cross-check.** Verify that the timeline reaches the requested start and end, timestamps increase coherently, subtitles match the selected item, and important claims are supported by speech, visible text, or both. Separate creator content from comments, recommendations, advertisements, and audience reactions.
6. **Extract meaning.** Reconstruct the argument, procedure, examples, caveats, and conclusions in chronological context. Preserve disagreements and uncertainty; do not turn an inference into something the speaker said.

## Access and copyright boundary

Use publicly accessible or user-authorized material. Respect authentication, paywalls, DRM, regional restrictions, expiring media URLs, and platform controls. When access requires credentials or circumvention, ask the user to provide the media, subtitle, or an accessible export instead of reading credential stores or bypassing the restriction.

Default to summaries and short attributed excerpts. Produce or publish a full verbatim transcript only when the user's rights and requested use support it. Temporary downloads and derived audio or frames are working evidence; do not publish or retain them beyond the task unless the user asks for an artifact.

## Deliver the reading

Use the smallest structure that answers the request. A complete extraction should make these fields judgeable:

```markdown
## Source
- Original URL:
- Canonical source and selected item:
- Title / creator / duration:

## Coverage
- Range analyzed:
- Evidence used: creator subtitles | auto captions | ASR | frames
- Missing or uncertain material:

## Timeline
- [00:00-02:10] Topic — claim, example, or action

## Core content
- Main argument or procedure
- Supporting examples and qualifications

## Visual evidence
- [12:34] What is visible and why it changes the interpretation

## Handoff
- Facts safe to reuse
- Interpretations that require attribution or further verification
```

Omit empty sections, but always report source identity, coverage, and material gaps. Attach timestamps to consequential claims when the source supports them. Label paraphrases, short quotations, and your own interpretation distinctly.

When another skill will consume the result, hand it the structured notes and evidence limits rather than only a polished summary. The downstream skill may transform the material, but it must not erase uncertainty or invent coverage.
