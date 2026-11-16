# 浏览器 Accessibility Tree 的存在与读取路径

日期：2026-11-16

## 结论

“原生 Accessibility Tree 仅在 CDP 模式下才有”不准确。树是浏览器为辅助技术维护的内部数据结构，不由 CDP 创建；CDP 只是 Chrome/Chromium 自动化客户端直接读取 Blink/Chromium AX Tree 的一条接口。

更精确的说法是：

1. 对常规的 Chrome/Chromium 外部浏览器自动化客户端，CDP `Accessibility` domain 是当前直接取得完整或部分内部 AX 节点图的主要公开接口，但不是 Chromium 内唯一接口。
2. 普通页面 JavaScript 没有读取完整浏览器 AX Tree 的 Web Platform API；DevTools Console 的 `getAccessibleName($0)`、`getAccessibleRole($0)` 也不是页面脚本 API。
3. Chromium 的特权扩展还可通过 `chrome.automation` 取得 browser automation/accessibility tree、遍历 `AutomationNode`、监听事件并执行动作；该 API 依赖 `manifest:automation` 且只对 `privileged_extension` 上下文开放，不是普通网页或普通扩展可随意使用的通用接口。
4. CDP 也不是唯一能读取“无障碍树”的外部机制。桌面程序还可通过 macOS Accessibility、Windows UI Automation、Linux AT-SPI 等平台 API 读取浏览器映射后的平台原生树；它与 Blink 内部树可能经过过滤和映射，不能视为相同快照。
5. WebDriver Classic 能读取单个 DOM Element 的 computed role/label，但没有完整 AX Tree 命令。
6. 当前 WebDriver BiDi Working Draft 已有 `accessibility` locator，可按 computed role/name 定位并返回 DOM nodes；规范算法遍历 DOM Element，并未序列化完整的浏览器原生 AX Tree。
7. 工具名中的“ARIA/Accessibility snapshot”不保证来自浏览器原生 AX Tree。Puppeteer 的 `page.accessibility.snapshot()` 明确调用 CDP `Accessibility.getFullAXTree`；Playwright 的 `ariaSnapshot()` 则由注入页面的脚本遍历 DOM、计算 ARIA role/name 后生成一棵工具自己的树。

因此，若“原生 AX Tree”特指 Chrome 的 Blink/Chromium 内部 AX 节点图，文章可以写成“在常规外部浏览器自动化协议中，目前是 CDP 直接暴露完整/部分原生 AX Tree；WebDriver/BiDi 没有等价的完整树命令”；不要写成“原生 AX Tree 只有 CDP 模式才有”。Chromium 特权扩展的 `chrome.automation` 是浏览器内另一条直接路径；若把平台辅助功能 API 也纳入 Agent 的观察通道，CDP 同样不是唯一读取路径。

## 一手证据

1. [Chromium Accessibility Overview](https://chromium.googlesource.com/chromium/src.git/+/HEAD/docs/accessibility/overview.md) 说明 Chromium 在 renderer 中构建页面 accessibility tree 的数据结构，把它发送到 browser process 缓存，再据此实现各操作系统的 native accessibility APIs。这证明树的存在独立于 CDP。
2. [Chrome DevTools Protocol: Accessibility](https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/) 提供 `getFullAXTree`、`getPartialAXTree`、`getRootAXNode`、`getChildAXNodes`、`queryAXTree` 等命令；`enable` 的说明还指出它会保持 `AXNodeId` 跨调用稳定，并可能带来性能影响。
3. Chromium [`automation.idl`](https://chromium.googlesource.com/chromium/src/+/HEAD/extensions/common/api/automation.idl) 明确说明 `chrome.automation` 可访问 browser automation/accessibility tree，并可检查 name、role、state、监听事件和执行动作；[`_api_features.json`](https://chromium.googlesource.com/chromium/src/+/HEAD/extensions/common/api/_api_features.json) 把它限制为依赖 `manifest:automation` 的 `privileged_extension` API。
4. [Puppeteer `Accessibility.ts`](https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/cdp/Accessibility.ts) 的 `snapshot()` 直接发送 `Accessibility.getFullAXTree`。同一源码把该结果描述为 Blink Accessibility Tree，再自行过滤为“interesting”节点。
5. [WebDriver](https://www.w3.org/TR/webdriver/) 定义 `Get Computed Role` 和 `Get Computed Label` 两个 element-scoped 命令，但没有 full accessibility tree 命令。
6. [当前 WebDriver BiDi Working Draft](https://w3c.github.io/webdriver-bidi/#command-browsingContext-locateNodes) 定义 `accessibility` locator。其算法在 DOM Element 上计算 role/name 并返回 `script.NodeRemoteValue`，所以它提供语义定位，而不是原生 AX 节点图快照。
7. [Playwright `ariaSnapshot.ts`](https://github.com/microsoft/playwright/blob/main/packages/injected/src/ariaSnapshot.ts) 的 `generateAriaTree()` 位于 injected script：遍历 DOM nodes，调用 `roleUtils.getAriaRole()` 与 `getElementAccessibleName()` 并生成 Playwright 自己的 ARIA tree。官方 [ARIA snapshots 文档](https://playwright.dev/docs/aria-snapshots) 也把结果定义为可访问结构的 YAML 表示，而非 CDP `AXNode` 列表。
8. [Windows UI Automation Tree Overview](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-treeoverview) 说明辅助技术和测试脚本可遍历 UI Automation tree；[AT-SPI `Accessible`](https://gnome.pages.gitlab.gnome.org/at-spi2-core/libatspi/class.Accessible.html) 提供 parent/child、role、name、state 等层级 API；Apple 的 [`AXUIElementCopyAttributeValue`](https://developer.apple.com/documentation/applicationservices/1462085-axuielementcopyattributevalue) 可读取 accessibility object 属性。这些是 CDP 之外的平台访问路径。

## 建议术语

| 术语 | 建议含义 |
| --- | --- |
| Blink/Chromium internal AX Tree | 浏览器引擎内部树；CDP `Accessibility` domain 与特权 `chrome.automation` 暴露的层 |
| platform accessibility tree | 浏览器经 macOS AX、Windows UIA、Linux AT-SPI 映射后给辅助技术的树 |
| ARIA snapshot | 自动化框架生成的 role/name/state 语义树；需再确认实现是否读取原生 AX Tree |
| DOM-derived semantic tree | 从 DOM/CSS/ARIA 计算出的工具树，如 Playwright 当前 `ariaSnapshot()` |

## 适用边界

以上结论针对 2026-11-16 可查的一手规范和主干源码。CDP tip-of-tree 与 WebDriver BiDi Working Draft 都会变化；正式引用时应注明版本或日期。平台 accessibility tree 还会受到操作系统、浏览器 accessibility mode、权限、headless 模式及过滤策略影响。
