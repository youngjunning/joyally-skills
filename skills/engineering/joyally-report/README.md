# Joyally Report

在生成最终回复之前使用。先从任务目标和现有证据判断结果，再把“摘要”作为独立标题放在顶部，按需展开正文。完整回复由摘要、正文、收尾三块组成，Report 统一设置标题、Markdown 分割线和稳定文本样式；调用方按宿主约定独立提供 Git、蒸馏等收尾事实。简短任务可以只有一句摘要。

例如，搜索修复已通过开发版验收、尚待发布时，第一段可以写成「开发版已能定位搜索结果。用户安装版需要等新版发布后再验收。」正文再说明复现路径、验证环境和剩余条件。

## 维护入口

| 需要调整的行为 | 维护位置 |
| --- | --- |
| 调用时机、证据判断、成文顺序、输出模式 | [主流程](SKILL.md) |
| 顶部摘要、标题、三段布局及稳定文本样式 | [摘要与布局契约](references/turn-report.md) |
| 进度、交付、排障、评审等场景 | [场景参考](references/report-types.md) |
| 性能数据可比性 | [度量规则](references/performance-comparison.md) |
| 汇报原则与公开来源 | [来源说明](references/reporting-principles.md) |

Use `$joyally-report` to draft a summary-first progress or delivery reply and control the headings, dividers, and stable text styling across its summary, body, and closing regions. Markdown and plain-text terminal output share the same evidence and section order.
