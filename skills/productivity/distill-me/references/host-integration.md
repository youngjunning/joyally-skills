# 宿主接入

初始化时，把下面区块写入当前 Agent 确实会在每轮读取的用户级长期指令。用 Skill 安装后的绝对路径替换 `<distill-me-root>`，不要把占位符原样写入。

```markdown
<!-- BEGIN distill-me -->
## 每轮自动蒸馏

每轮主任务完成后、最终回复前，先读取 `<distill-me-root>/references/automatic-gate.md`。门禁未命中时不加载完整 Skill 或历史数据，保留“蒸馏：无新增”作为本轮结果。命中后才读取 `<distill-me-root>/SKILL.md` 和 `<distill-me-root>/references/automatic-distillation.md`，只处理本轮新增内容，写入 `<distill-me-root>/workbench/data/twin.json` 并回读。若宿主已有统一收尾 Report，把蒸馏结果只写入该 Report，不另加结尾段落；没有统一 Report 时才单独报告蒸馏结果。用户要求跳过蒸馏或只输出指定内容时优先遵从。
<!-- END distill-me -->
```

Codex 通常使用用户级 `AGENTS.md`。其他宿主应使用其官方支持的长期指令入口。不要为自动蒸馏安装或配置 Stop Hook、UserPromptSubmit Hook 等会把操作提示显示给用户的触发器。如果宿主只能安装 Skill，却不能在每轮收尾时读取这段指令，则自动模式未启用；保留手动调用能力并如实说明。
