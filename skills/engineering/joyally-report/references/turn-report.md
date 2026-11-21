# Turn Report

`joyally-report` 把完整汇报压缩成一份人和下游 Agent 都容易接续的回合摘要。它负责信息选择、顺序、措辞、证据边界与最终呈现，不代替主回复中的结论、证据、未完成项、风险和下一步，也不代替蒸馏、工作脉络或 Git 领域检查。

主回复先按 `joyally-report` 的完整工作流汇报，并按任务复杂度缩放；末尾只放一份紧凑 `Report` 供扫读和接续。轻量字段不能代替完整汇报。除非用户明确说“跳过报告”或“只输出”，否则保留该 Report。

## 输入责任

按本轮实际工作取得四类输入：

1. `joyally-report` 从主报告提炼已验证结果、关键边界和确需接续的下一步；没有下一步时不制造待办。
2. `distill-zisheng` 按其 [收尾结果契约](../../../productivity/distill-zisheng/references/turn-report.md) 提供“蒸馏”和“工作脉络”两行。
3. 调用方去重列出本轮真正按流程执行的 Skills；只浏览说明、可用列表或自动路由不计入。
4. `joyally-git` 按其 [收尾结果契约](../../joyally-git/references/turn-report.md) 提供每个实际工作仓库的 Git 与交付行。

`joyally-report` 核对输入是否齐全、相互一致且没有重复，再负责整体顺序、必要取舍与可扫读性。领域行的语义与生命周期边界仍以所属 Skill 的契约为准；状态缺失或失败时保留原状态和下一步，不自行改写为“无新增”、“已提交”或“已交付”。

## 格式

```markdown
> Report
> 结果：<已验证结果与关键边界>
> 下一步：<确需接续的动作与完成条件；没有则省略>
> <distill-zisheng 产出的蒸馏行>
> <distill-zisheng 产出的工作脉络行>
> Skills：<本轮实际使用的 Skills>
> <joyally-git 产出的一行或多行仓库状态>
```

保留上述顺序；没有下一步或 Git 项目时省略对应行。用户要求英文时使用 `Result`、`Next`、`Distillation`、`Workstream`、`Skills` 等价字段。只压缩主报告，不逐句重复；阻塞项在对应行写清对象和解除条件。
