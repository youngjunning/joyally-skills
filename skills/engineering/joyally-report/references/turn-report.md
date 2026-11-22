# Final-answer information architecture

Codex calls the user-visible closeout the **final answer**. Design it as a descending information gradient: decision first, evidence second, operational handoff last. These are internal region names, not visible headings.

## The three regions

1. **Decision surface** — one to three sentences that let the reader act without reading further. State the outcome or current landing point first, then the single limitation, decision, or completion condition that most changes the verdict. Put status words inside natural prose; do not open with a label such as “summary”.
2. **Evidence surface** — the optional judgment and continuation layer. Organize it by the reader's questions, not the agent's chronology. Each material claim should carry the evidence that supports it and, when incomplete, the boundary or condition that changes it. Use a short heading only for a real topic inside this region; the region itself has no heading.
3. **Handoff strip** — optional host-owned closing facts such as distillation, used Skills, Git delivery, deployment, or other domain receipts. Keep one compact line per applicable owner, preserve the host-defined order, and omit absent domains. This region records operational provenance; it does not repeat the result or evidence.

## Presence and separators

Render only regions that contain useful information. Separate adjacent regions exactly once with a blank line, `---`, and another blank line:

- Decision only: no divider.
- Decision + evidence or decision + handoff: one divider.
- Decision + evidence + handoff: two dividers.

Never create an empty region, stacked dividers, a leading divider, or a trailing divider. The dividers are the only region markers; do not add summary, body, or closing headings.

## Compression and ownership

- Give each fact one home: verdict and highest-impact caveat in the decision surface; proof, scope, risks, and next conditions in the evidence surface; receipts and delivery metadata in the handoff strip.
- Keep the decision surface free of file inventories, test lists, commit IDs, and process narration unless one of them changes the verdict.
- Prefer a claim → evidence → boundary sequence inside the evidence surface. Keep implementation, tests, artifacts, push, deployment, and user acceptance as distinct gates.
- Put clickable evidence and file references beside the supported claim. Put commit IDs and domain receipts in the handoff strip unless they are themselves the user's requested result.
- Draft for completeness first, then remove repetition and ceremony. Compression must preserve blockers, unknowns, scope boundaries, and the condition for continuing.

## Complete example

```markdown
目录滚动高亮已修复，Chromium 验收通过。Safari 尚未验收，因此当前可以交接，但还不能声称跨浏览器完成。

---

改动集中在目录激活区间计算与样式；路由和数据结构未变。相关单元测试通过，Chromium 中逐段滚动 6 个标题均正确切换。Safari 的完成条件是同样 6 个标题全部正确切换。

---

蒸馏：无新增。
Skills：joyally-report、joyally-git。
Git：已提交并推送，commit abc1234；未部署。
```

For a direct factual answer, return only the answer. For an exact-format request such as JSON or a command, preserve that format instead of imposing this layout.

## Acceptance examples

| Input | Expected decision surface |
| --- | --- |
| Search results appeared in Debug, signed build passed, release pending | 开发版已经能定位搜索结果。用户安装版需要等新版发布后再验收。 |
| User asks whether a specific test passed, with one verified result | 搜索定位回归测试已通过。 |
| Deployment is blocked by a rejected permission check | 预发部署被权限检查拦住，目标环境验收还在等部署账号获得权限。 |
| User requests only a JSON object | Return the requested JSON object verbatim in structure. |
