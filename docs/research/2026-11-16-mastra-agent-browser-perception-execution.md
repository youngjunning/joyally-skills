# Mastra agent-browser 的页面感知与执行闭环

日期：2026-11-16

## 核对范围

本文只讨论以下固定依赖链，不把 Vercel Labs `agent-browser` 当前主干实现倒推到旧版本：

1. `@mastra/agent-browser@0.4.1`
2. `agent-browser@0.19.0`
3. `playwright-core@1.61.1`（`agent-browser@0.19.0` 声明 `^1.57.0`，本次安装解析为 1.61.1）

精确版本以 npm 发布包为准；GitHub 主干只用于理解项目演进，不作为这条调用链的实现证据。

## 结论

`@mastra/agent-browser@0.4.1` 不只是把 `agent-browser` 桥接成 Mastra Tool。它还提供 Agent-facing 的自动化编排层：typed tool schema、thread/shared 浏览器隔离、浏览器状态恢复、动作与导航等待的组合、dialog/tab/drag/evaluate 等高阶动作、结构化错误与恢复提示、截图、录屏和 Studio screencast。

但要分清能力归属：

1. ARIA snapshot 加 `ref`、按 `role/name/nth` 建立定位配方，主要由 `agent-browser@0.19.0` 完成。
2. ARIA 语义树和 Locator 的 actionability、auto-wait、实际点击与输入由 Playwright 完成。
3. Mastra 的 `browser_snapshot` 调用 upstream `BrowserManager.getSnapshot()`，再把 `[ref=e1]` 改写成 `@e1`，补充 URL、title、元素数量和滚动位置；它没有自行生成语义树。
4. 这条 snapshot 路径没有直接读取 CDP `Accessibility.getFullAXTree()`，也不应称为原生 AX Tree 导出。
5. 整套系统不是 AX-only：观察依赖 DOM 派生的 ARIA 语义，执行依赖 DOM Locator 和 Playwright 输入机制，还提供 screenshot、CSS selector、JavaScript evaluate 等非 AX 通道。

所以，更准确的定义是：`@mastra/agent-browser` 是基于 `agent-browser + Playwright` 的 Agent 自动化适配与编排层，而不是单纯桥接器，也不是一个只靠 Accessibility Tree 的浏览器 Agent。

## 感知与执行闭环

```text
模型 / Mastra Agent
  ↓ typed browser_* tools
@mastra/agent-browser 0.4.1
  ↓ lifecycle、thread scope、wait、error、feedback
agent-browser 0.19.0 BrowserManager
  ↓ ariaSnapshot → refMap → Locator recipe
Playwright 1.61.1
  ↓ DOM 派生语义、Locator actionability、浏览器输入
页面
  ↑ 新 URL / 新 snapshot / action result / screenshot
```

### 1. 页面感知

Mastra 的 `browser_snapshot` 调用：

```ts
manager.getSnapshot({
  interactive: input.interactiveOnly ?? true,
  compact: true,
})
```

随后仅做输出格式和反馈增强：把 `[ref=eN]` 改成 `@eN`，计算 `elementCount`，并返回 `url`、`title`、`scroll` 和下一步提示。

`agent-browser@0.19.0` 的 `getEnhancedSnapshot()` 才是快照增强主体：它调用 Playwright `locator.ariaSnapshot()`，逐行解析其 YAML 风格文本，为交互角色及命名内容分配 `eN`，并为同角色同名称的重复元素记录 `nth`。

该版本还有可选 `cursor` 增强：扫描 DOM 中的 `cursor:pointer`、`onclick`、`tabindex` 等线索，为缺少正式 ARIA role 的元素补 ref。但 `@mastra/agent-browser@0.4.1` 上述调用没有传入 `cursor: true`，因此不能把这项可选能力算作本次 Mastra snapshot 路径已经启用的感知输入。

Playwright `ariaSnapshot()` 本身在注入页面的脚本中遍历 DOM，按 HTML/ARIA 规则计算 role、accessible name、状态和文本，生成 Playwright 的 ARIA tree。它不是 CDP 原生 `AXNode[]`。

### 2. 从感知到可执行引用

`agent-browser@0.19.0` 的普通 ref 保存的是定位配方：

```text
ref → role + accessible name + optional nth
```

开启 `cursor` 补全时，ref 才可能保存 CSS selector。Mastra 把 ref 暴露给模型，但没有把原始 ref map 一起放入模型上下文。

这一点决定了旧版本 ref 的可靠性边界：它不是原生 `AXNodeId`、`backendDOMNodeId` 或固定 Element handle。执行时会重新查询当前页面；列表重排、同名元素增删或跨页出现相同名称时，旧 `nth` 或同名配方可能指向不同业务对象。页面感知不能脱离 ref 的身份模型单独评价。

### 3. 动作执行

以 click 为例：

1. Mastra 用 `requireLocator(@eN)` 取得 upstream locator。
2. `BrowserManager.getLocatorFromRef()` 把普通 ref 还原为 `page.getByRole(role, { name, exact: true })`，必要时追加 `.nth(n)`；cursor ref 则使用 `page.locator(css)`。
3. Mastra 调用 `locator.click()`，并传入 button、clickCount、modifiers 和 timeout。
4. Playwright 在动作时解析 Locator，执行可见性、稳定性、事件接收、enabled 等 actionability 检查，滚动目标并派发输入事件。

type、select、hover、wait、drag 也沿用 Locator 执行；press 走 page keyboard；scroll 和 evaluate 直接执行页面 JavaScript；screenshot 走 Playwright 截图。由此可见，执行并不是“对 AX 节点调用 action”。

### 4. 反馈、恢复与重新感知

Mastra 为 click、press、select 增加可选 `waitUntil`，把动作与后续导航完成条件组合起来，避免下一次 snapshot 过早读取旧 DOM 或半加载页面。0.4.1 还修复了导航等待超时可能形成未处理 rejection、导致进程崩溃的问题。

动作结果会返回当前 URL 和下一步提示；stale ref、element not found、pointer interception 等异常被整理成面向 Agent 的错误类型与恢复建议。dialog 工具把“点击触发器”和“接受/拒绝对话框”组合为一个受控动作；tab 切换后会恢复 screencast 并更新 session state。

这些是实质性的自动化增强，因为它们改变了 Agent 如何等待、恢复、隔离会话和继续循环，而不只是改变函数名。但它们仍不等于自主规划：选择下一步动作和是否重新 snapshot，仍由上层 Agent 循环决定。

## 只用 Accessibility Tree 能走多远

若把“只用 AX”严格理解为模型只接收语义树，且所有目标都只能从语义树产生，覆盖面大致如下：

| 页面类型 | AX/ARIA 语义通常能覆盖 | 主要失效点 |
| --- | --- | --- |
| 表单、登录、设置页 | label、textbox、button、checkbox、状态 | 自绘控件、错误标注、同名项歧义 |
| 文档、列表、表格、导航 | heading、link、list、table、cell、文本 | 视觉分组与布局关系可能丢失 |
| 常规业务后台 | 语义良好的 CRUD 与流程表单 | 虚拟列表、复杂拖拽、浮层遮挡、动态重排 |
| Canvas/WebGL、地图、图表、远程桌面 | 少量外围控件 | 像素内容、空间目标、图形关系通常不可见 |
| 图片、icon-only、自定义控件 | 有合格 alt/ARIA 时可用 | 缺 accessible name 时无法识别意图 |

AX/ARIA-first 足以完成大量结构化网页任务，但“纯 AX 感知”不等于“完整浏览器自动化”。动作至少还需要一种从语义目标到可执行对象的可靠绑定，以及可见性、遮挡、滚动、输入和结果复核。CDP `Accessibility` domain 本身是查询接口，不提供通用 click/fill；这条 Mastra 调用链则用 Playwright DOM Locator 补齐执行。

因此判断浏览器 Agent 时，应把以下四项作为一个整体：

1. 它实际读取什么：原生 AX、DOM 派生 ARIA、DOM、截图还是多源组合。
2. observation 如何变成 ref，以及 ref 是否绑定节点身份、是否有版本和失效规则。
3. ref 如何落到动作：DOM Locator、坐标、平台 AX action 或浏览器协议输入。
4. 动作后如何等待、重新观察、核对业务后置条件并处理不确定结果。

## 一手来源

1. [`@mastra/agent-browser@0.4.1` npm 发布包](https://www.npmjs.com/package/@mastra/agent-browser/v/0.4.1)及其精确版本制品 [`dist/index.js`](https://unpkg.com/@mastra/agent-browser@0.4.1/dist/index.js)：tool schema、snapshot 适配、thread manager、动作实现、错误处理、screencast 与录屏入口。
2. [Mastra PR #17426](https://github.com/mastra-ai/mastra/pull/17426)：为 click、press、select 增加 `waitUntil`，明确目标是避免动作后过早 snapshot 读取旧或半加载 DOM。
3. [Mastra PR #18870](https://github.com/mastra-ai/mastra/pull/18870)：0.4.1 对导航等待超时和未处理 rejection 的修复。
4. [`agent-browser@0.19.0` npm 发布包](https://www.npmjs.com/package/agent-browser/v/0.19.0)及其精确版本 [`snapshot.js`](https://unpkg.com/agent-browser@0.19.0/dist/snapshot.js)、[`browser.js`](https://unpkg.com/agent-browser@0.19.0/dist/browser.js)：Playwright ARIA snapshot 解析、ref map、可选 cursor DOM 扫描和 ref → Locator 还原。
5. [Playwright ARIA snapshots](https://playwright.dev/docs/aria-snapshots)及 `playwright-core@1.61.1` 对应提交 [`39e3553`](https://github.com/microsoft/playwright/tree/39e3553a4f283a41134d75d7e404484bd9e6865a)：ARIA snapshot 的页面注入实现与 Locator 行为。
6. [Playwright actionability](https://playwright.dev/docs/actionability)：Locator 动作执行前的 auto-wait 与 actionability 检查。
7. [CDP Accessibility domain](https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/)：原生 AX 查询命令及 `AXNode` 数据，不包含通用 click/fill 动作。

## 适用边界

本文的源码判断只对上述固定版本成立。Vercel Labs `agent-browser` 后续已重写为原生 Rust/CDP 路径，snapshot、ref 生命周期、DOM 补全与输入执行都已发生变化；不能用当前主干证明 0.19.0 的行为，也不能把 0.19.0 的限制推广到当前版本。
