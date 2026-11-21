# Opening summary and section layout contract

The input is the user's objective and the verified state at the moment of writing. The output is the first paragraph of the main reply. Use the reader's language. In a structured Chinese report, begin with **摘要**. For a small answer, a single opening sentence carries the summary.

1. State what the user can now do or decide. Qualify the claim to the environment where it was observed.
2. When required work remains, include the highest-impact gap and the next condition that changes the result. Keep the entire summary to one to three sentences.
3. When a main body follows, insert a blank line, `---`, and another blank line between the summary and body.
4. When host-required closing records follow the body, insert the same divider between body and closing. Report inserts both dividers; the closing providers supply facts only. Never place a divider before the first region, after the last region, or beside an omitted region. Keep one copy of the summary.

For a complete Markdown reply, assemble the regions as:

```markdown
**摘要**　一句到三句结论。

---

正文证据与关键未完成项。

---

**收尾**

领域收尾事实。
```

## Acceptance examples

| Input | Expected opening or output |
| --- | --- |
| Search results appeared in Debug, signed build passed, release pending | **摘要**　开发版已经能定位搜索结果。用户安装版需要等新版发布后再验收。 |
| User asks whether a specific test passed, with one verified result | 搜索定位回归测试已通过。 |
| Deployment is blocked by a rejected permission check | **摘要**　预发部署被权限检查拦住，目标环境验收还在等部署账号获得权限。 |
| User requests only a JSON object | Return the requested JSON object verbatim in structure. |
