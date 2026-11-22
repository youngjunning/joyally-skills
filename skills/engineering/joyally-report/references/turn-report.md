# Final-answer information architecture

Codex calls the user-visible closeout the **final answer**. Design it as four ordered regions: summary first, body second, distillation third, and status last. These are internal region names, not visible headings.

## The four regions

1. **Summary / decision surface** — one to three sentences that let the reader act without reading further. State the outcome or current landing point first, then the single limitation, decision, or completion condition that most changes the verdict. Put status words inside natural prose; do not open with a label such as “summary”.
2. **Body / evidence surface** — the optional judgment and continuation layer. Organize it by the reader's questions, not the agent's chronology. Each material claim should carry the evidence that supports it and, when incomplete, the boundary or condition that changes it. Use a short heading only for a real topic inside this region; the region itself has no heading.
3. **Distillation strip** — optional host-owned distillation result. Keep the verified distillation fact compact and omit the region when the host does not require it. Do not mix used Skills, Git delivery, deployment, or other operational status into this region.
4. **Status strip** — optional host-owned operational facts such as used Skills, Git delivery, deployment, or other domain receipts. Keep one compact line per applicable owner, preserve the host-defined order, and omit absent domains. For used Skills, give every Skill one concise, task-specific contribution in the form `skill-name（本轮主要作用）`; a bare name list is incomplete. This region records operational provenance; it does not repeat the result, evidence, or distillation result.

When reporting Git delivery, give every repository its own line in the form `[owner/repository](repository URL) …`. Link the stable repository display name to its browsable remote homepage; when no browsable remote exists, link it to the absolute local repository root. Start directly with the linked repository name, without an icon or a `Git:` or `Git：` label. A remote ref, branch, worktree path, or commit hash does not identify the repository and must not stand in for its name.

## Presence and separators

Render only regions that contain useful information, preserve their fixed order, and separate every pair of rendered regions exactly once with a blank line, `---`, and another blank line:

- Summary only: no divider.
- Summary + body: one divider.
- Summary + distillation + status: two dividers.
- Summary + body + distillation + status: three dividers.

Never create an empty region, stacked dividers, a leading divider, or a trailing divider. The dividers are the only region markers; do not add summary, body, distillation, or status headings around the regions. Domain-owned labels such as `蒸馏：` and `使用技能：` remain part of their facts.

## Compression and ownership

- Give each fact one home: verdict and highest-impact caveat in the summary; proof, scope, risks, and next conditions in the body; the distillation result in the distillation strip; operational receipts and delivery metadata in the status strip.
- Keep the decision surface free of file inventories, test lists, commit IDs, and process narration unless one of them changes the verdict.
- Prefer a claim → evidence → boundary sequence inside the evidence surface. Keep implementation, tests, artifacts, push, deployment, and user acceptance as distinct gates.
- Put clickable evidence and file references beside the supported claim. Put commit IDs and operational domain receipts in the status strip unless they are themselves the user's requested result.
- Draft for completeness first, then remove repetition and ceremony. Compression must preserve blockers, unknowns, scope boundaries, and the condition for continuing.

## Complete example

```markdown
目录滚动高亮已修复，Chromium 验收通过。Safari 尚未验收，因此当前可以交接，但还不能声称跨浏览器完成。

---

改动集中在目录激活区间计算与样式；路由和数据结构未变。相关单元测试通过，Chromium 中逐段滚动 6 个标题均正确切换。Safari 的完成条件是同样 6 个标题全部正确切换。

---

蒸馏：无新增。

---

使用技能：joyally-report（整理交付结论与证据）；joy-git（核对并完成提交推送）。
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
