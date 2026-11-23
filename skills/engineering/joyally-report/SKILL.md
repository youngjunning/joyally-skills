---
name: joyally-report
description: Compose evidence-complete Codex final answers for progress, delivery, diagnosis, review, and decisions. Lead with a decision surface, support it with an evidence surface, then keep host-supplied distillation and status records in separate closing regions.
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# Joyally Report

Use this skill when drafting a progress update, diagnosis, review, decision, or delivery report. Apply it after evidence is available and **before writing the final answer**. A direct factual question can use a single sentence. Honor requests for exact output, such as JSON, a patch, or just a command.

## Compose the main reply

Before composing the verdict, reconcile explicit requests and commitments in the current conversation against their latest correction and observed completion, not just the latest message. Apply the [current-conversation open-work rules](references/turn-report.md#current-conversation-open-work); carry forward required unfinished work without turning optional suggestions into tasks.

1. **Establish the result.** Identify the user's objective, what actually happened, and the evidence for it. Keep implementation, tests, artifacts, push, deployment and user acceptance distinct. A successful earlier step establishes only that step. Attribute hypotheses and recommendations explicitly.
2. **Compose the decision surface.** Follow the [final-answer architecture](references/turn-report.md). Open with the result and the one limitation, decision, or next condition that most changes what the reader can do. A small answer can end here.
3. **Build the evidence surface.** Before shortening, account for every material question: the objective, result, and current state; what changed and what intentionally stayed outside scope; first-hand evidence and its environment; which implementation, test, artifact, push, deployment, and acceptance gates passed or remain open; risks, unknowns, or alternative explanations; and the next action or decision with its completion or unblock condition. Organize this material by reader question, not execution chronology. Omit an irrelevant category instead of creating an empty section.
4. **Set the depth.** A direct fact can remain one sentence. A standard engineering delivery uses the evidence floor above. A diagnosis, decision, release, incident, or performance report also carries the causal, tradeoff, rollback, or measurement detail selected by its [report type](references/report-types.md). Brevity applies to the decision surface, repetition, and ceremony—not to evidence needed to verify, reproduce, operate, or hand off the result.
5. **Assemble the final answer.** Render the decision surface, optional evidence surface, optional host-supplied distillation strip, and optional host-supplied status strip according to the [final-answer architecture](references/turn-report.md). Separate every rendered region exactly once. Report owns the information gradient and dividers; closing owners supply facts without adding layout.
6. **Check the assembled answer.** Verify that the decision surface matches the strongest evidence and highest-impact open item, every material evidence-floor question is answered or genuinely irrelevant, and each fact has one home. Then remove repeated conclusions, empty regions, process narration, and unsupported next actions. Never use pruning to hide a missing gate, unknown, scope boundary, or decision condition.

## Select detail and format

For every structured report, choose the relevant [report type](references/report-types.md) and read only that section; use completed engineering delivery for an ordinary implementation handoff. For numerical performance claims, check [measurement comparability](references/performance-comparison.md). Consult the [source principles](references/reporting-principles.md) when explaining the editorial rationale.

Default to Markdown in chat. Use prose or ordered lists, with tables only for meaningful comparisons. Render ordinary identifiers such as skill names, branch names, commit IDs, and remote refs as plain text or links; reserve inline code styling for actual code, commands, literal paths, and values whose exact syntax matters. Present closing facts as normal text or list items rather than blockquotes. For redirected output, CI logs or an explicit terminal request, use plain text, short labeled sections and indented evidence. Use PASS, WARN, BLOCKED, TODO or INFO for ASCII-only output. Emit ANSI only on explicit request in a confirmed interactive terminal. An explicit output format takes precedence.

Honor `REPORT_FORMAT=markdown` and `REPORT_FORMAT=terminal`. In terminal mode use plain paths with line numbers and, where helpful, ✅, ⚠️, ⛔, ⏳ or ℹ️ for status. In Markdown mode leave rendering to the host. Use prose or numbered items in both modes.

## Integration boundary

The skill produces the decision and evidence surfaces in one composition pass, then owns the final-answer layout when the caller supplies separate distillation and status facts. The caller independently obtains those facts and preserves the host-defined domain order inside each region; domain owners do not choose the surrounding dividers. Use an already verified domain fact in the decision surface when it changes the verdict. Operational checks, writes, skill inventories and receipt assembly belong to their respective owners. Report can finish with only the decision surface when nothing else materially helps the reader.
