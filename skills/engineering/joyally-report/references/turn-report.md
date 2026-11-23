# Final-answer information architecture

Codex calls the user-visible closeout the **final answer**. Design it as four ordered regions: summary first, body second, a combined distillation-and-Skills closing strip third, and Git delivery last. These are internal region names, not Markdown headings.

## The four regions

1. **Summary / decision surface** — one to three sentences that let the reader act without reading further. In a structured report, start with `**摘要：**`; keep the following text at normal weight. State the outcome and the highest-impact limitation or next condition. Direct factual and exact-format answers may omit the label.
2. **Body / evidence surface** — the optional judgment and continuation layer. Organize it by reader question. Include material evidence, boundaries, and current-conversation open work; use headings only for real topics, not for the region itself.
3. **Combined closing strip** — distillation results followed by used Skills in one group, with no divider between them. Keep each domain on its own line: start with `**蒸馏：**` and `**技能：**` (or the caller's required labels). Give every Skill one concise, task-specific contribution in the form `skill-name（本轮主要作用）`. A bare name list is incomplete. Omit an absent domain rather than creating an empty line or placeholder. Shared layout does not merge domain ownership or turn Skill use into a distillation result.
4. **Git strip** — optional host-owned repository delivery facts, separate from the combined closing strip. Keep one repository per line and preserve the host-defined order. Omit this region when no repository applies; do not repeat the result, evidence, distillation, or Skills receipt.

When reporting Git delivery, use `[owner/repository](repository URL) …` for each repository. Link its browsable remote homepage, or the absolute local root when no browsable remote exists. Start directly with the linked repository name, without an icon or `Git:` label. A branch, path, ref, or commit does not replace repository identity.

## Presence and separators

Render only nonempty regions in the fixed order. Separate adjacent regions exactly once with a blank line, `---`, and another blank line. Within the combined closing strip, put a blank line between the two domain lines, not a divider.

- Summary only: no divider.
- Summary + body: one divider.
- Summary + combined closing + Git: two dividers.
- Summary + body + combined closing + Git: three dividers.

Do not insert a divider between distillation and Skills. If only one domain is present, it alone forms the combined closing strip. Never create empty regions, stacked, leading, or trailing dividers. Structured labels are `**摘要：**`, `**蒸馏：**`, and `**技能：**`; following text stays at normal weight. Honor caller-defined wording without changing the grouping.

## Compression and ownership

- Give each fact one home: verdict and highest-impact caveat in the summary; evidence, risks, and next conditions in the body; separate distillation and Skills facts inside their combined closing strip; repository delivery metadata in the Git strip.
- Keep file inventories, test lists, commit IDs, and process narration out of the decision surface unless they change the verdict.
- Prefer a claim → evidence → boundary sequence. Implementation, tests, artifacts, push, deployment, and user acceptance are separate gates.
- Put clickable evidence beside the supported claim; keep commit IDs in Git receipts unless they are the requested result.
- Compression must preserve blockers, unknowns, scope boundaries, and the condition for continuing.

## Current-conversation open work

Before a progress, delivery, diagnosis, or handoff answer, check the available current conversation for explicit requests and commitments that have not reached their required endpoint. This is a reconciliation step, not a new task manager or an extra closing region.

1. Follow the latest correction, cancellation, deferral, and completion evidence. A side question does not cancel an earlier task. Do not scan other sessions, guess missing history, reopen completed work, or promote optional suggestions into required tasks. Disclose missing context when it prevents a reliable check.
2. Separate pending implementation / 待实现 (required code, configuration, documentation, release, or external action is missing) from pending verification / 待验证 (the result exists but required acceptance evidence is missing). A blocker is a present condition preventing the next step; a risk is a possible adverse outcome, not merely an unrun test.
3. If required work remains, put the highest-impact item in the opening decision surface. In the body, group the other known items under the smallest useful “当前会话未完成” or lifecycle label; give each its next concrete action, known owner, and completion or unblock condition. Do not repeat an item already explained in the same answer.
4. If the check establishes that nothing required remains, a delivery or handoff may say “No known required work remains in the available current conversation.” Do not add an empty checklist to every factual reply. Optional deployment or extra device checks remain evidence boundaries unless the user requested them or an acceptance gate requires them.

Acceptance cases:

| Available conversation | Expected result |
| --- | --- |
| Delete a standalone site after preserving its source; backup prepared; then a keyboard question is answered | Source preservation and deletion are still pending implementation; the keyboard answer must not hide them. In particular, deletion is still pending implementation, not pending verification. |
| The user later says to pause deletion | Preserve the deferral; do not auto-resume or report it as currently actionable work. |
| Source preserved, remote repository and deployment deleted, readback confirms the endpoints | Close the deletion task; do not keep listing it as pending. |
| User asks to save a note; source saved, validated, and pushed; live page has not been checked and no publication check was requested | Saving is complete; disclose the unverified live page as a boundary. Saving a note does not silently add a deployment task. |

## Complete example

```markdown
**摘要：** 目录滚动高亮已修复，Chromium 验收通过。Safari 尚未验收，因此当前可以交接，但还不能声称跨浏览器完成。

---

改动集中在目录激活区间计算与样式；路由和数据结构未变。相关单元测试通过，Chromium 中逐段滚动 6 个标题均正确切换。Safari 的完成条件是同样 6 个标题全部正确切换。

---

**蒸馏：** 无新增。

**技能：** joyally-report（整理交付结论与证据）；joy-git（核对并完成提交推送）。

---

[owner/repository](https://git.example.com/owner/repository) 已提交并推送，commit abc1234；未部署。
[owner/website](https://git.example.com/owner/website) 保留本地改动，尚未提交。
```

For a direct factual answer, return only the answer. For an exact-format request such as JSON or a command, preserve that format instead of imposing this layout.

## Acceptance examples

| Input | Expected decision surface |
| --- | --- |
| Search results appeared in Debug, signed build passed, release pending | 开发版已经能定位搜索结果。用户安装版需要等新版发布后再验收。 |
| User asks whether a specific test passed, with one verified result | 搜索定位回归测试已通过。 |
| Deployment is blocked by a rejected permission check | 预发部署被权限检查拦住，目标环境验收还在等部署账号获得权限。 |
| User requests only a JSON object | Return the requested JSON object verbatim in structure. |
