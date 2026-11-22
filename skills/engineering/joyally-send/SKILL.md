---
name: joyally-send
description: 仅在用户明确说“joyally send”或显式调用本 Skill 时触发；把当前工程任务自主推进到通过安全门并合并 PR。
---

# Joyally Send

这是一次明确的端到端授权：用户不会持续盯着线程，Agent 负责把当前目标推进到已合并 PR，并在等待检查或 review 时保持工作。没有明确触发 `joyally send` 时，不能推导这项授权。

## 授权与边界

明确触发后，Agent 可以在本任务仓库内：

- 创建并更新任务分支和 PR，在 merge gate 通过后按仓库允许的方式合并。
- rebase 后仅对本任务 PR 分支使用 `--force-with-lease`；先核对远端分支和预期旧 SHA。
- 直接执行证明本任务所需的普通测试、构建、应用运行、浏览器或模拟器验收。

这项授权不包含删除数据、触碰生产、发布版本、修改分支保护、绕过审批、使用 admin 权限、force push 默认分支或操作其他人的分支。更高优先级约束、项目明确禁止项和宿主审批仍然有效。若 push 会直接触发生产发布或其他高影响动作，停在可恢复位置并取得对应授权。

## 1. 完成最小改动

读取项目约定和 `joyally-git`，确认仓库、目标分支、并行改动、远端与作者身份。默认分支上不得直接工作；使用任务分支，脏工作区或分叉时按 `joyally-git` 建立隔离 worktree。完成满足当前意图的最小方案，不顺手扩展相邻问题。

## 2. 证明改动

为 diff 中每项行为取得本轮亲自观察的证据：

- 能复现原故障时，先观察失败，再对同一复现观察修复通过。
- 运行仓库 CI 对应的 lint、typecheck、test、build 等检查。
- 现有测试体系能表达回归但缺少覆盖时，补一个没有修复就会失败的聚焦测试。
- UI、runtime、设备或集成行为使用真实可见路径验收；全绿 mock 不能单独证明用户体验。

证据无法覆盖某项改动时，不具有 full confidence，进入“需要用户”分支。

## 3. 独立复审

读取并执行 [joyally-loop](../joyally-loop/SKILL.md)。只有结论为 Agreed 才继续；Stuck 时保留双方证据并进入“需要用户”分支。

## 4. 提交并创建 PR

按 `joyally-git` 只提交本任务文件。创建 PR 前获取默认分支最新状态并安全 rebase，复验有意义的行为与冲突修复。PR 正文先说明问题与用户影响，再说明方案、直接证明、未完成风险和 Joyally Loop 结果；避免只罗列文件。

使用仓库现有 CLI、API 或连接器创建 PR。保存 PR URL、base、head 和最终提交 SHA。没有可用的 PR 能力、认证或远端时，进入“需要用户”分支，不把普通 push 冒充 PR。

## 5. 守候 PR

持续观察 required checks、review bot 和 human review，直到 merge gate 可判断：

- 修复真实 finding 和 CI failure，每次更新前取得对应证明。
- 不采纳的 finding 必须留下书面理由；不能用忽略代替处理。
- reviewer 或检查仍在运行时继续等待。若宿主有 watcher，使用 watcher；没有时以不超过环境限制的间隔回查并保持进度更新。
- 每次 push 前重新核对默认分支与 PR head；需要 rebase 时只对本任务分支使用带租约的强推。

## 6. Merge gate

只有以下条件在最新 head 上全部成立才可合并：

- 直接证明覆盖 diff 中每项改动。
- required checks 全绿。
- 自动 review 已结束，每个 finding 已修复或有书面驳回依据。
- 没有人类 review 仍处于 changes requested。
- PR 与默认分支同步，平台报告可合并。

沿用仓库允许的 merge、queue 或 auto-merge 方式，不绕过保护。进入队列或开启 auto-merge 后继续守候，直到平台确认已合并；“已排队”不等于“已合并”。

## 7. 报告

合并后使用 `joyally-report` 给出 PR 链接、merge commit、直接证明、Loop 结果、review 处理决定，以及代码、测试、合并、部署和真实业务结果各自的状态。合并不证明部署或用户验收。

## 需要用户

只有无法自主继续时才请求用户：目标歧义会改变结果、无法取得直接证明、merge gate 无法自行修复、下一步超出本授权，或其他 PR 已使本任务失效。使用宿主的阻塞式提问能力，并附 PR、阻塞证据、互斥选项和推荐项；普通进度消息不能代替阻塞式提问。

提问能力不可用或没有得到答复时，保留 PR 开放且不合并，取消本任务创建的自动合并或 watcher，并以清晰的阻塞 handoff 结束。不能为了“完成”而降低 merge gate。
