---
name: joyally-answer-page
description: Turn a complex explanation, comparison, decision, or plan into a readable one-page HTML answer when a visual artifact helps the reader revisit or share it. Use Joyally Design's static one-pager workflow for layout and rendering. Keep ordinary short answers in chat; formal reports and product pages follow their own workflows.
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# Joyally Answer Page

Answer the question in chat, then provide a portable one-page HTML when the relationships are easier to understand in a page than in prose. The page carries the conclusion, the minimum explanation needed to understand it, source links, and any limits or open decisions. It is an answer artifact, not a new design system.

## Choose the page

Make a page when the user requests one or when a complex explanation, multi-step process, comparison, or decision has a clear reader benefit from adjacent text, diagram, table, and evidence. For a short factual answer, a simple command, or a request for plain text, answer directly. Do not add a page to every final response.

This Skill leads answer selection, factual structure, and the handoff. Use `joyally-design` for its [paper and static output mode](../../design/joyally-design/SKILL.md#纸面与静态成品) and [HTML report path](../../design/joyally-design/references/html-reports.md) to lay out, render, and visually check the page. If a diagram is central, use `joyally-image` for the diagram and its runtime. If the task is to write a standalone article or formal report, let the corresponding writing or report workflow lead; the answer page may be an explicitly requested companion artifact.

## Build the answer

1. Establish the exact question, reader, intended use, and available evidence. Read the relevant sources or project files before composing claims. Preserve source dates, uncertainty, and the difference between observed results and inference.
2. Write the answer as a short content draft before touching layout: title; one-sentence conclusion; two to four sections chosen for the question; each important claim's source; and the decision, next step, or limitation if applicable. Choose a sequence for events, a flow for dependencies, a table for comparable choices, and prose for nuance. Use fewer panels when fewer ideas suffice.
3. Give Joyally Design a brief with the content draft, audience, brand or theme, target format, screen or print priority, required links, and acceptance condition. For a browser answer, use its static HTML/report path. Start from the bundled Joyally report shell when useful:

   ```bash
   node <joyally-design-dir>/scripts/design-engine.mjs report <output-dir> --title "标题" --subtitle "结论"
   ```

   Replace the starter content with the verified answer. Keep the HTML source and its local CSS together. If the user asks for a single standalone file, package local styles into that file and verify it with network access disabled; the default report generator produces a directory, not a single file. If the requested output is A4 or PDF, check actual page count and print layout instead of assuming a browser page fits one sheet.
4. Validate claims against the draft, including numbers, code excerpts, sources, and caveats. Run Joyally Design's HTML validator when the selected output supports it, then inspect the rendered page at desktop and narrow widths and, for print delivery, in print preview. Check reading order, headings, table overflow, link targets, contrast, and any diagram labels. Fix the artifact and recheck the affected view. Treat a generated file as implementation evidence, not visual acceptance.
5. Give the user a concise answer in chat and link the local HTML artifact. State whether the page is a portable directory, a verified standalone HTML, or a print-checked PDF, and name any unverified viewing environment. Publish or upload only when the user or the owning project's rules authorize the destination.

## Example routes

- “解释 TCP 三次握手”：conclusion first, then a sequence, state changes, and a compact flag table; cite the protocol source used for the explanation.
- “Redis 和 Memcached 怎么选”：put the decision and its assumptions first, then a comparison table and the conditions that would change the choice.
- “把这个方案做成一页给同事看”：preserve the approved facts and links, then make a screen-first or A4 print-first one-pager as requested.

The idea of a short draft feeding a readable HTML answer was prompted by [QingYunA/answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) (MIT). This Skill uses Joyally Design's existing static output and does not bundle or claim that project's CLI, templates, performance results, or diagram renderer.
