# Joyally Design 统一 token 契约

采用 `Seed → Map → Alias → Component`。文件中的 `semantic` 就是 Alias；平台示例可以省略没有派生值的 Map 层，但不得另立语义体系。颜色属性、色阶、双模式角色、状态矩阵与色域边界见[颜色体系](color-system.md)。

| 角色 | 语义 token | 使用约定 |
| --- | --- | --- |
| 画布与阅读表面 | background / surface / surfaceElevated / surfaceMuted | 长文、表格、代码和证据用不透明表面 |
| 正文 | text / textSecondary / textTertiary | 在实际背景上验证对比度 |
| 操作 | primaryAction / onPrimaryAction | primary 是视觉强调，不能默认用于小号白字按钮 |
| 选中 | primaryContainer / onPrimaryContainer | 不改变控件几何；配合文字或图标 |
| 焦点 | focus | 保留键盘可见焦点 |
| 状态 | success / warning / error / info | 不仅靠颜色表达 |
| 边界 | border / borderStrong | 普通分隔与需要 3:1 的控件边界分开 |
| 遮罩 | overlay | 与 surface 和组件 opacity 分开管理 |
| 禁用 | disabledSurface / disabledText | 颜色与真实不可操作行为同时成立 |
| 深色 | mode.dark 的完整角色映射 | 不用反相或零散 dark token 代替完整映射 |

## 前景与背景成对

颜色角色以可见配对交付，不把前景色当作能跨表面继承的独立装饰。组件的每个变体和状态都记录实际 `foreground / background / border / focus` 配对；局部覆盖背景时，在同一作用域同时指定匹配的前景色。浅色、半透明、渐变或图片表面使用深色前景，深色表面使用浅色前景，最终以运行时合成后的颜色为准。

默认、hover、pressed、selected、focus、disabled 和 loading 分别核对。普通文字至少 4.5:1；大字、功能图标和控件可见边界至少 3:1。disabled 虽可不计入 WCAG 文本要求，Joyally 仍以 3:1 作为标签辨认底线，并说明状态和恢复条件；白字配浅色表面、深色字配深色表面均视为未完成。半透明组件必须在它实际覆盖的最亮、最暗代表背景上分别检查，不能只验证 token 源色或组件脱离页面时的样子。

## 预设与平台适配

- `assets/joyally-design.tokens.json` 与 `assets/joyally-report-theme.css`：报告和 React 的完整分层、青山湖主题与材质契约；四季画面共同提供取色与构图依据。
- `assets/joyally-native.tokens.json`：现有湖色预设的语义值与对比度声明；`JoyallyPalette.swift`、`JoyallyTheme.kt`、`JoyallyTheme.ts`、`joyally-native.css` 是对应平台的起点。
- `assets/xiaoxiang-theme.tokens.json`：香奈儿风主题的浅色与深色语义色及几何样本；按[主题规则](fashion-xiaoxiang.md)与[20 张参考图](../assets/references/xiaoxiang/README.md)映射到目标产品组件，不自动替换现有平台预设。
- `assets/space-theme.tokens.json`：太空主题的浅色与深色语义色及几何样本；按[主题规则](space.md)映射到目标产品组件，不自动替换现有平台预设。
- `assets/hand-drawn-theme.tokens.json`：手绘主题对 Looseleaf 官方浅色纸张 tokens 的语义映射；按[手绘主题](hand-drawn.md)通过完整 Looseleaf registry 落到 shadcn/ui 组件。上游当前未提供可直接验收的整套深色组件映射，因此样本只声明 `light`。
- 这些 JSON 是同一语义契约的不同预设，不要求色值相同。一次实现先选项目已有预设或明确一种预设，再映射全部相关角色；不要混用不同预设的前景/背景。
- 八套视觉主题各有取材边界；青山湖以春夏秋冬各 5 张授权实拍为收集目标，目前画册保留未完成位置。前五套以景点或景观区域为取景范围，香奈儿风以包袋、山茶花、巴黎夜景、服装细节和编辑呈现为取材范围；太空主题使用原创概念画面表达轨道与行星地平线，不声称这些画面是天文观测照片；手绘主题以 Looseleaf 的官方组件源码、registry 与纸笔视觉语法为实现依据。青山湖主题包含四季，不把季节作为运行时外观维度；`material`（材质）与 `mode`（明暗模式）独立。香奈儿风与太空分别提供独立的 `light` / `dark` 映射，手绘当前只提供 `light`。`style` 和 `mood` 描述视觉语言与意境，不改变交互状态和语义角色。当前平台 token 完整实现青山湖预设；其他主题进入具体产品时仍需映射相关组件并逐项校验。
- 平台尺寸与交互由平台参考决定：桌面紧凑控件与移动端触控热区共存，不把 Web 布局和 32px 控件直接搬到手机。

变更预设时运行对应 token 校验器。交付产品还需核对运行时配色、字体缩放、键盘/触控、辅助技术与降低动态效果；静态 token 通过不代表设备验收。

## 图表配色

`joyally-design.tokens.json` 的 `diagram.light` / `diagram.dark` 是交互图表的配色源。通用画布与文字引用已有 seed，七种图表类别保留可区分的独立色相。四种 preset 使用同一映射，打印以浅色类别配色加白色背景输出。运行 `validate-diagram-theme.py` 检查模板映射及正文、节点和连线对比度。湖色种子保留原有命名，原生 CSS 使用 `joyally-` 前缀。手绘主题中的 Chart 使用 Looseleaf 组件与图表 tokens；需要导出到既有交互图表引擎时另做该引擎的映射，不把组件主题样本冒充现有 diagram preset。
