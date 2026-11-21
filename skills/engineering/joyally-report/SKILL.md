---
name: joyally-report
description: Compose progress and delivery replies before final generation. Open with a short decision summary, then explain verified results, material gaps, and required action.
---

# Joyally Report

Use this skill when drafting a progress update, diagnosis, review, decision, or delivery report. Apply it after evidence is available and **before writing the final reply**. A direct factual question can use a single sentence. Honor requests for exact output, such as JSON, a patch, or just a command.

## Compose the main reply

1. **Establish the result.** Identify the user's objective, what actually happened, and the evidence for it. Keep implementation, tests, artifacts, push, deployment and user acceptance distinct. A successful earlier step establishes only that step. Attribute hypotheses and recommendations explicitly.
2. **Write the opening summary.** Follow the [summary contract](references/turn-report.md). Choose the result and the one limitation or decision that most affects the reader. Place them at the very top. For a small result, the summary can be the entire answer.
3. **Develop the body as needed.** Put consequential unfinished work first. Distinguish missing implementation from implemented behavior awaiting verification. Identify a present blocker and its unblock condition, or an uncertain risk and its consequence. Follow with only the evidence or explanation needed to judge or continue the work. Include an owner or deadline only when known.
4. **Check the assembled reply.** Compare the first paragraph with the strongest supporting evidence and the most important open item. Remove repeated conclusions, empty sections, process narration and next actions that do not follow from the request.

## Select detail and format

For a complex handoff, diagnosis, decision or release, choose the relevant [report type](references/report-types.md). For numerical performance claims, check [measurement comparability](references/performance-comparison.md). Consult the [source principles](references/reporting-principles.md) when explaining the editorial rationale.

Default to Markdown in chat. Use prose or ordered lists, with tables only for meaningful comparisons. For redirected output, CI logs or an explicit terminal request, use plain text, short labeled sections and indented evidence. Use PASS, WARN, BLOCKED, TODO or INFO for ASCII-only output. Emit ANSI only on explicit request in a confirmed interactive terminal. An explicit output format takes precedence.

Honor `REPORT_FORMAT=markdown` and `REPORT_FORMAT=terminal`. In terminal mode use plain paths with line numbers and, where helpful, ✅, ⚠️, ⛔, ⏳ or ℹ️ for status. In Markdown mode leave rendering to the host. Use prose or numbered items in both modes.

## Integration boundary

The skill produces the opening summary and main body in one composition pass. The caller independently handles any required closing records after the body. Use an already verified domain fact in the summary when it changes the verdict. Operational checks, writes, skill inventories and receipt assembly belong to their respective owners. Report can finish with just the task evidence available to it.
