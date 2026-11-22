---
name: joyally-report
description: Compose evidence-complete progress and delivery replies before final generation. Open with a short decision summary, then provide enough verified detail to judge and continue the work.
---

# Joyally Report

Use this skill when drafting a progress update, diagnosis, review, decision, or delivery report. Apply it after evidence is available and **before writing the final reply**. A direct factual question can use a single sentence. Honor requests for exact output, such as JSON, a patch, or just a command.

## Compose the main reply

1. **Establish the result.** Identify the user's objective, what actually happened, and the evidence for it. Keep implementation, tests, artifacts, push, deployment and user acceptance distinct. A successful earlier step establishes only that step. Attribute hypotheses and recommendations explicitly.
2. **Write the opening summary.** Follow the [summary contract](references/turn-report.md). Choose the result and the one limitation or decision that most affects the reader. Put the summary directly in the opening paragraph without a summary heading. For a small result, the summary can be the entire answer.
3. **Build an evidence-complete body.** Before shortening, account for every material question: the objective, result, and current state; what changed and what intentionally stayed outside scope; first-hand evidence and its environment; which implementation, test, artifact, push, deployment, and acceptance gates passed or remain open; risks, unknowns, or alternative explanations; and the next action or decision with its completion or unblock condition. Include enough detail for the reader to independently judge the result or continue the work. Omit an irrelevant category instead of creating an empty heading.
4. **Set the depth.** A direct fact can remain one sentence. A standard engineering delivery uses the evidence floor above. A diagnosis, decision, release, incident, or performance report also carries the causal, tradeoff, rollback, or measurement detail selected by its [report type](references/report-types.md). Brevity applies to the summary, repetition, and ceremony—not to evidence needed to verify, reproduce, operate, or hand off the result.
5. **Assemble the three regions.** For a Markdown reply containing an opening summary, a main body, and host-required closing records, put `---` between summary and body and another `---` between body and closing. Use those dividers alone to mark the regions: put closing facts immediately after the second divider without a closing heading. Report owns dividers, lists, and emphasis; closing owners supply facts without adding layout. Omit the divider beside any omitted region, including a one-sentence answer with no body or closing.
6. **Check the assembled reply.** Verify that the summary matches the strongest evidence and highest-impact open item, and that every material evidence-floor question has an answer or is genuinely irrelevant. Then remove repeated conclusions, empty sections, process narration, and unsupported next actions. Never use pruning to hide a missing gate, unknown, scope boundary, or decision condition.

## Select detail and format

For every structured report, choose the relevant [report type](references/report-types.md) and read only that section; use completed engineering delivery for an ordinary implementation handoff. For numerical performance claims, check [measurement comparability](references/performance-comparison.md). Consult the [source principles](references/reporting-principles.md) when explaining the editorial rationale.

Default to Markdown in chat. Use prose or ordered lists, with tables only for meaningful comparisons. Render ordinary identifiers such as skill names, branch names, commit IDs, and remote refs as plain text or links; reserve inline code styling for actual code, commands, literal paths, and values whose exact syntax matters. Present closing facts as normal text or list items rather than blockquotes. For redirected output, CI logs or an explicit terminal request, use plain text, short labeled sections and indented evidence. Use PASS, WARN, BLOCKED, TODO or INFO for ASCII-only output. Emit ANSI only on explicit request in a confirmed interactive terminal. An explicit output format takes precedence.

Honor `REPORT_FORMAT=markdown` and `REPORT_FORMAT=terminal`. In terminal mode use plain paths with line numbers and, where helpful, ✅, ⚠️, ⛔, ⏳ or ℹ️ for status. In Markdown mode leave rendering to the host. Use prose or numbered items in both modes.

## Integration boundary

The skill produces the opening summary and main body in one composition pass, then owns the final section layout when the caller supplies closing records. The caller independently obtains the closing facts and places them after the body; their domain owners do not choose the surrounding dividers. Use an already verified domain fact in the summary when it changes the verdict. Operational checks, writes, skill inventories and receipt assembly belong to their respective owners. Report can finish with just the task evidence available to it.
