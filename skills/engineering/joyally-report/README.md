# Joyally Report

在生成 Codex 的 final answer 之前使用。四段依次是让读者立即行动的摘要、支持判断与继续工作的正文、独立的蒸馏结果，以及技能与 Git/交付等状态。只渲染有内容的区域，每两个实际渲染的区域之间用一条 Markdown 分割线隔开，不显示区域标题。

例如，搜索修复已通过开发版验收、尚待发布时，摘要可以写成「开发版已能定位搜索结果。用户安装版需要等新版发布后再验收。」正文再说明复现路径、验证环境和剩余条件；蒸馏结果与使用技能、Git 等状态回执之间再加一道分割线。

## 维护入口

| 需要调整的行为 | 维护位置 |
| --- | --- |
| 调用时机、正文完整性门槛、成文顺序、输出模式 | [主流程](SKILL.md) |
| 摘要、正文、蒸馏区、状态区、分割线及压缩规则 | [final answer 信息架构](references/turn-report.md) |
| 进度、交付、排障、评审等场景 | [场景参考](references/report-types.md) |
| 性能数据可比性 | [度量规则](references/performance-comparison.md) |
| 汇报原则与公开来源 | [来源说明](references/reporting-principles.md) |

Use `$joyally-report` to compose a decision-first Codex final answer, support it with an evidence-complete body, and keep host-owned distillation and status facts in separate closing regions. Markdown and plain-text terminal output share the same information gradient.
