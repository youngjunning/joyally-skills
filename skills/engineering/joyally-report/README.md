# Joyally Report

在生成 Codex 的 final answer 之前使用。三段不是三个同权重栏目，而是一条递减的信息梯度：第一段是让读者立即行动的决策面，第二段是支持判断与继续工作的证据面，第三段是由宿主提供的紧凑交接带。只渲染有内容的区域，相邻区域用一条 Markdown 分割线隔开，不显示区域标题。

例如，搜索修复已通过开发版验收、尚待发布时，决策面可以写成「开发版已能定位搜索结果。用户安装版需要等新版发布后再验收。」证据面再说明复现路径、验证环境和剩余条件；交接带只放蒸馏、Skills、Git 等领域回执。

## 维护入口

| 需要调整的行为 | 维护位置 |
| --- | --- |
| 调用时机、正文完整性门槛、成文顺序、输出模式 | [主流程](SKILL.md) |
| 决策面、证据面、交接带、分割线及压缩规则 | [final answer 信息架构](references/turn-report.md) |
| 进度、交付、排障、评审等场景 | [场景参考](references/report-types.md) |
| 性能数据可比性 | [度量规则](references/performance-comparison.md) |
| 汇报原则与公开来源 | [来源说明](references/reporting-principles.md) |

Use `$joyally-report` to compose a decision-first Codex final answer, support it with an evidence-complete judgment surface, and append compact host-owned handoff facts only when applicable. Markdown and plain-text terminal output share the same information gradient.
