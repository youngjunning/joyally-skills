# WeChat video source handling

Use this branch for WeChat Channels (视频号), Official Account article videos, and copied WeChat share links.

## Resolve the shared item

1. Preserve the submitted share text and URL. Resolve redirects only through the accessible share page or browser context, and record the stable visible identity: creator/account, title or caption, publication time when available, and selected video.
2. Distinguish a Channels item from an Official Account article containing one or more videos. For an article, identify the exact embedded video rather than treating the article body as its transcript.
3. Treat share tokens and media URLs as potentially short-lived. Do not publish temporary playback URLs as canonical sources; cite the stable share or article page instead.

## Acquire content

- Use subtitles or captions exposed by the accessible player when present. WeChat video often has no reusable public subtitle track, so be prepared to transcribe authorized playback or a user-provided export.
- If the share page is accessible only inside WeChat or an already authenticated browser context, inspect that context without extracting cookies or credentials. When the media still cannot be obtained, ask the user to upload or export the video.
- Inspect frames for burned-in captions, speaker labels, product demonstrations, charts, and end cards. Burned-in captions are visual evidence and may require OCR; verify them against the audio before treating them as quotations.
- Keep likes, comments, recommendations, account profile copy, and Official Account article text separate from the video's own content unless the user asks to analyze those surfaces together.

## Failure modes

- A share card, title, thumbnail, or article summary establishes discovery only, not video coverage.
- An expired share token or playback URL is an access blocker, not evidence that the video was removed.
- Login, friend/region visibility, anti-bot, or app-only playback may prevent extraction. Report the exact accessible layer and request an uploaded media file or screen recording instead of claiming a complete reading.
- If only the visible excerpt or preview played, report the exact covered duration and mark the result partial.
