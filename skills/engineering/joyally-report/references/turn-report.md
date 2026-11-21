# Turn Report

`joyally-report` 把已核验的领域结果整理成一份人和下游 Agent 都容易读取、判断和继续执行的简短 `Report`。它负责信息选择、顺序、措辞、证据边界与最终呈现，不代替蒸馏、工作脉络或 Git 领域检查。

主回复先给用户任务结论；末尾只放一份 `Report`。除非用户明确说“跳过报告”或“只输出”，否则保留该 Report。

## 输入责任

按本轮实际工作取得三类输入：

1. `distill-zisheng` 按其 [收尾结果契约](../../../productivity/distill-zisheng/references/turn-report.md) 提供“蒸馏”和“工作脉络”两行。
2. 调用方去重列出本轮真正按流程执行的 Skills；只浏览说明、可用列表或自动路由不计入。
3. `joyally-git` 按其 [收尾结果契约](../../joyally-git/references/turn-report.md) 提供每个实际工作仓库的 Git 与交付行。

`joyally-report` 核对输入是否齐全、相互一致且没有重复，再负责整体顺序、必要取舍与可扫读性。领域行的语义与生命周期边界仍以所属 Skill 的契约为准；状态缺失或失败时保留原状态和下一步，不自行改写为“无新增”、“已提交”或“已交付”。

## 格式

```markdown
> Report
> <distill-zisheng 产出的蒸馏行>
> <distill-zisheng 产出的工作脉络行>
> Skills：<本轮实际使用的 Skills>
> <joyally-git 产出的一行或多行仓库状态>
```

保留上述顺序；没有 Git 项目时省略仓库行。用户要求英文时使用 `Distillation`、`Workstream`、`Skills` 等价字段。阻塞项在对应行写清对象和下一步，不重复主回复正文。
