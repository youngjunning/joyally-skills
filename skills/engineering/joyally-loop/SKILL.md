---
name: joyally-loop
description: 用户明确说“joyally loop”时触发；用一个独立 reviewer 在有限轮次内复审当前改动，直到双方有证据地达成一致或预算耗尽。
---

# Joyally Loop

把“作者自己觉得完成”升级成“作者与独立 reviewer 对当前行为 diff 达成一致”。目标是满足意图的最小改动，不是借评审扩大范围。

## 轮次预算

- 默认最多 3 轮：第一轮审完整行为 diff，后续只审本轮变更和未关闭问题。
- 只有安全、权限、认证、数据丢失、状态或并发风险仍有 blocker / should 证据时，才延长到 5 轮；用户可另行指定预算。
- 一轮只剩 nit 时提前结束。纯格式、注释、文档或与意图无关的小优化通常记为 nit，不为它们开启新一轮。
- 同一时刻只有一个 reviewer。reviewer 只审查，不编辑、不提交、不推送、不评论 PR，也不再启动 reviewer。
- 维护 ledger：稳定 ID、严重度、结论、证据、处理结果、已核实的 reviewer/model 与 usage。未知值保持未知。

## 1. 固定范围

先读取项目约定并检查 `git status --short`。保留无关改动；能按路径或 hunk 分离时只审本任务，无法可靠分离时停止并说明边界。

获取远端最新状态后确定 base：已有 PR 使用 PR 的真实 base 和 head；本地分支使用默认分支的 merge-base；没有远端时使用用户指定 base，或仅审未提交改动。用同一种 diff 定义贯穿所有轮次，并用一两句话写明意图、范围外事项和已运行检查。

## 2. 启动独立 reviewer

使用当前宿主可用的独立 reviewer 上下文。优先选择与作者不同的模型或 provider；至少要与作者上下文隔离。只记录工具真实暴露的身份，不凭产品名猜模型。若当前环境无法启动独立 reviewer，报告阻塞，不能把作者自审写成 loop 通过。

第一轮 brief 必须让 reviewer 能独立读到仓库、base、diff、意图、范围和检查结果，并要求：

```text
只评审，不修改、不提交、不推送、不评论 PR、不启动子 reviewer。
阅读 diff 与必要上下文，寻找意图未满足、调用方破坏和真实回归。
坚持最小改动；与意图无关的稀有边界、小性能收益和额外兼容记为 nit。
按稳定 ID 返回 blocker / should / nit、文件位置、主张与最小修复建议，最后给 APPROVE 或 CHANGES。
```

reviewer 运行时不修改审查范围内文件，不并发启动第二个 reviewer。超时、报错或无回复都不等于通过；确认旧 reviewer 已停止后，才可在同一 ledger 上重启。

## 3. 逐项回应

作者独立核对每个 finding 的事实和严重度：

- 同意：做最小修复；行为需要时补一个缺少修复就会失败的聚焦测试。
- 不同意：用文件位置、测试或可复现输出来说明。
- 范围外或 nit：简短拒绝，可列为 follow-up，不扩展当前 diff。

更新 ledger，重跑受影响检查并比较 diff 大小。评审让改动无必要地变大时，先删减再继续；不能为了结束 loop 而机械接受意见。

## 4. 后续轮次

只有 blocker / should 仍开放、行为代码发生变化，或已有 approval 没覆盖当前行为 diff 时才开启下一轮。复用同一个 reviewer 上下文；若宿主只能新建 reviewer，则仍须一次只运行一个，并提供完整 brief、ledger、当前 base diff 与上轮后的变化。

要求 reviewer 只检查开放 ID 和变更代码，并把旧 ID 标成 resolved 或 still open 及原因。已关闭且未受影响的问题不重新打开。

## 5. 结束条件

- **Agreed：** reviewer 明确 APPROVE 当前行为 diff，且没有 blocker / should 未关闭，作者也没有未解决疑虑。
- **Stuck：** 同一问题经过两次有证据的回应仍有分歧，或预算耗尽。预算耗尽不是 approval；各用两三行保留双方观点和证据，由用户决定。

Loop 期间不推送。用户已授权更新 PR 或后续工作流需要推送时，只在 Agreed 后交给 `joyally-git` 执行。PR 正文追加：`Reviewed with joyally-loop: <N> rounds; reviewer <verified identity>; verdict <approved|stuck>.`

报告轮数、reviewer 身份、diff 前后规模、修复和拒绝的 findings、usage 是否可得，以及提交和推送状态。
