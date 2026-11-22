# 宿主接入

安装 `distill-me` 时，同时完成每轮指令接入。安装 Skill 只提供能力，不会自动建立后续每轮回调。

## 写入

1. 找到当前 Agent 确实会在每轮读取的用户级 `AGENTS.md`。其他宿主使用其官方支持的等价长期指令入口；项目级指令不能代替用户级入口。
2. 修改前备份该文件，保留所有已有指令。
3. 用 Skill 安装后的绝对路径替换 `<distill-me-root>`。按 `BEGIN` / `END` 标记幂等写入下面区块：已有区块时整体替换，没有时追加一次。

```markdown
<!-- BEGIN distill-me -->
## 每轮自动蒸馏

每轮主任务完成后、最终回复前，先读取 `<distill-me-root>/references/automatic-gate.md`。门禁未命中时不加载完整 Skill 或历史数据，保留“蒸馏：无新增”作为本轮结果。命中后才读取 `<distill-me-root>/SKILL.md` 和 `<distill-me-root>/references/automatic-distillation.md`，只处理本轮新增内容，写入 `<distill-me-root>/workbench/data/twin.json` 并回读。若宿主已有统一收尾 Report，把蒸馏结果只写入该 Report，不另加结尾段落；没有统一 Report 时才单独报告蒸馏结果。用户要求跳过蒸馏或只输出指定内容时优先遵从。
<!-- END distill-me -->
```

## 回读验收

写入后重新读取长期指令文件，并同时满足：

- `BEGIN distill-me` 和 `END distill-me` 各出现一次；
- 区块中的路径是当前安装目录的绝对路径；
- 不含 `<distill-me-root>` 占位符；
- 原有非 `distill-me` 指令仍然存在。

以上验收通过，才报告“Skill 已安装、自动蒸馏已启用”，并给出 Skill 路径、长期指令路径和回读结果。宿主只能安装 Skill、不能保证每轮读取长期指令时，报告“Skill 已安装、自动蒸馏未启用”，保留手动调用能力。

使用长期指令作为唯一的自动入口，不安装 Stop Hook、UserPromptSubmit Hook 等可见提示注入，也不把宿主对 Skill 的自动匹配当成后续每轮回调。
