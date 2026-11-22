# Bilibili source handling

Use this branch for `bilibili.com`, `b23.tv`, BV/AV pages, episodes, and multipart videos.

## Resolve the exact item

1. Follow a `b23.tv` redirect and record both the submitted short link and final page. Normalize the canonical URL to the stable work identity, retaining only parameters needed to select a part or episode; remove share-session, recommendation, device, timestamp, and other tracking parameters.
2. Identify whether the target is a single video, multipart video, playlist, season, or episode. Preserve the selected `p`/episode identity; do not silently analyze only the first part.
3. Capture visible metadata such as title, uploader, publication date, duration, description, chapters, and part list. Treat the description as uploader metadata, not as a substitute for watching or transcribing the video.

## Acquire content

- Prefer subtitles exposed for the selected item and language. Record whether they are creator-provided or automatically generated.
- If subtitles are absent or incomplete, acquire the authorized audio with a currently available downloader or browser path and transcribe it. Inspect the tool's current help before relying on flags that may have changed.
- Inspect frames around the opening claim, chapter transitions, demonstrations, diagrams, on-screen prompts, and the conclusion. For screen recordings, visible text may carry the main argument even when the narration is sparse.
- Keep danmaku and comments outside the author's content. Include them only when the user asks for audience reaction, and label them as audience evidence.

## Failure modes

- A successful page fetch establishes metadata access, not video coverage.
- Search snippets, AI summaries, related-video cards, and repost descriptions are discovery aids, not substitutes for the selected source.
- Login, anti-bot, removed content, or regional restrictions are coverage blockers. Report the blocker and ask for an uploaded media file or subtitle rather than claiming a complete extraction.
- If only part of a long video was processed, give the exact covered time range and mark the result partial.
