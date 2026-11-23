# Evidence-led Chinese tone editing

Use this branch for an explicit Chinese “去 AI 味”, tone audit, or tone rewrite. The existing deslop gates remain the pattern reference; this document governs how a suspected pattern becomes an edit. It is an original workflow extension, not the Lieflat rule bundle or a detector of authorship. Provenance and the upstream reuse boundary are recorded in [attribution.md](attribution.md).

## Match the requested action

- **Audit only:** inspect the original without writing a replacement. Return actionable findings and a bounded recommendation; wait for editing authorization.
- **Rewrite requested:** preserve the source, diagnose, apply the permitted edits, and review the result in this task. Do not require another reply merely because an external workflow does.
- **New prose:** use the ordinary writing workflow. An internal tone check does not require a separate public report, new artifact set, or translated draft.

## Make the diagnosis falsifiable

For each material finding, keep its location, a short source excerpt, the specific reader cost, the proposed change, and the meaning that must survive. Explain why the passage is a problem in this context; “an AI often writes this” is not a sufficient reason. Group related minor findings rather than exposing every candidate to the user.

Separate observable form from interpretation. A search can find a repeated word or punctuation mark; it cannot establish that two names mean the same thing, a transition is unnecessary, or a metaphor misrepresents a mechanism. Read the necessary neighboring context and source definitions. When the meaning is unclear, retain the passage or ask a targeted question instead of manufacturing certainty.

Distinguish changes warranted by a clear reading defect from optional voice choices and protected or useful text. Use the selected author's actual writing as evidence of intended voice when available. Do not turn every preference into a required correction.

## Review information organization

- Follow stable referents through the paragraph. Resolve unnecessary alternate names only after confirming their identity; a plan, its implementation, and its outcome are not interchangeable.
- Check whether introductions and transitions do work beyond repeating what is already visible. Start a new section with its evidence when repetitive setup can be removed safely. Keep explanation, causal links, dependencies, and procedural order; never manufacture a topic jump to look less systematic.
- For a sequence of similarly shaped statements, keep all distinct facts and qualifications. Change their organization only when the repeated scaffolding obscures the comparison or slows comprehension. Instructions and structured comparisons may benefit from consistent syntax.
- Judge punctuation by function before frequency. A colon introducing fields and a dash isolating a needed qualification may be useful even in a punctuation-heavy draft. Changing the punctuation alone may leave the underlying reading problem intact.

## Use measurements within their scope

Ordinary editing needs located evidence, not a numeric score. If measurements are requested or an available tool provides them:

- Record the text version, tool or search method, coverage, included text types, unit, and denominator. Keep prose statistics separate from headings, code, quotations, tables, and lists; inspect those structures separately when relevant.
- Preserve raw candidates and their disposition: actual issues, useful/protected occurrences, and unresolved cases. Report partial or unavailable measurements as such, not as zero. Sampling does not establish complete coverage.
- Rescan using the same definitions after the edit. A removed section changes the denominator; report the content change rather than comparing bare percentages as if the scope were unchanged.
- Describe an external study with its language, genre, model versions, comparison design, and replication limits. A published effect size is not the probability that this draft was generated. Do not transfer a single-model threshold or a withdrawn research finding into an unconditional writing rule.
- Whole-piece rhythm measurements describe a distribution, not individual errors. Improve a located passage rather than adding irregularity to force a target distribution.

This skill ships no Lieflat detector, classifier schema, or commercial integration. External analysis, when explicitly requested and separately authorized, remains subject to that tool's license and data-sharing permissions; it does not replace contextual review.

## Recheck and deliver

Compare each changed passage against the original's facts, agency, polarity, modality, conditions, exceptions, quotations, and terminology. Review any changed paragraph in context. A shorter or lower-count draft fails if it has lost a qualification, introduced an unsupported claim, or confused the reader.

For an audit or requested change report, show representative before/after excerpts, why they changed, what was preserved, and any remaining decision that affects the result. State retained patterns and their function when they explain the outcome. For ordinary rewrite delivery, return the revised prose with only material caveats; do not append raw detector output or an invented “AI percentage”.

## Acceptance cases

These original cases test editorial decisions rather than phrase substitution.

| Situation | Expected behavior |
| --- | --- |
| The source defines “项目方案”, “实施蓝图”, and “行动设计” as one document, then rotates them in a paragraph | Prefer its declared name; preserve an explicit alias definition. Without that identity evidence, do not merge the names. |
| “评审结论如下：只验证了读取接口，写入流程仍待验收。” appears after several repeated conclusion announcements | Remove redundant setup where safe, keeping both the verified scope and unfinished acceptance state. |
| “申请需提交三项材料：身份证明、申请说明、授权文件。” | Preserve all required items and the useful colon/list structure. Three items do not constitute a tone defect. |
| A tutorial explains each step's prerequisite and consequence | Keep the sequence and dependencies; remove only redundant narration, not the links themselves. |
| An exact quotation contains “不是……而是……” | Preserve the quotation and assess the narrator's surrounding prose separately. |
| A preferred metaphor has no demonstrable factual contradiction | Retain it or offer a clearly optional alternative; do not infer bad taste from a classifier vote. |
| A paragraph has no figures and the source provides none | Preserve the supported claim or flag missing evidence; never invent a figure to increase apparent specificity. |
| “只检查 AI 味，先别改。” versus “直接改自然，保留所有限定条件。” | The first returns findings without mutation; the second completes the bounded rewrite and invariant check without a redundant approval turn. |
