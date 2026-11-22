---
name: joyally-stop
description: 仅在用户明确说“joyally stop”或显式调用本 Skill 时触发；把任务推进到 PR 可合并，但把 merge 保留给用户。
---

# Joyally Stop

执行 `joyally-send` 的完整改动、证明、独立复审、提 PR 和守候流程，但把 merge 设为绝对停止线。明确触发 `joyally stop` 已授权这些准备工作，不需要再触发 `joyally send`；其 merge 授权不适用。

先读取 [joyally-send](../joyally-send/SKILL.md)，遵循其中的范围、普通测试授权、Proof、Joyally Loop、PR 创建、review 处理和 merge gate。本文件的规则优先。

## 禁止合并

可以提交、推送、rebase、处理冲突，并仅对本任务 PR 分支使用核对过旧 SHA 的 `--force-with-lease`。不得合并、开启 auto-merge、进入 merge queue、直接 push 默认分支、绕过保护或把这些动作委托给其他 Agent。

开始工作前关闭本 PR 已存在的 auto-merge，并在每次 push 前重新确认 PR 不会自动合并；若已在 merge queue 中则安全退出并记录。无法阻止自动合并时先报告阻塞，不能继续制造新的可自动落地主干的提交。

## 停在门口

把 `joyally-send` 的 merge gate 当作 readiness gate。最终 diff 的行为、冲突修复、直接证明和 reviewer 结论都必须重新覆盖。

获取目标分支最新状态，回读 PR 的真实 head、base、checks、reviews 与 mergeability，并确认 PR 仍开放、不是 draft、没有自动合并安排：

- **Ready to merge：** gate 全部通过，PR 保持开放且未合并，交给用户决定。
- **Waiting for required approval：** 只剩明确的人类审批，核实它确实是唯一阻塞项。
- **Blocked：** 给出阻塞、已尝试动作、恢复入口和所需决定；按 `joyally-send` 的“需要用户”规则处理。

handoff 或提问前停止本任务创建的 watcher。使用 `joyally-report` 报告 PR 链接、最终 head、readiness verdict、直接证明、Loop 结论、未完成风险，并明确 PR 是否仍开放且未合并。
