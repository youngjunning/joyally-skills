# Joyally Design 颜色体系

颜色体系把颜色属性、色阶、语义角色和组件状态分开管理。色值不是最终接口；页面和组件只消费语义或组件 token，并在实际背景、模式和状态中验收。

## 五层关系

| 层 | 回答的问题 | Joyally Design 落点 |
| --- | --- | --- |
| 颜色属性 | 这是什么颜色，深浅和鲜艳程度如何？ | 新建或扩展色板优先在 OKLCH 中调整 `L`、`C`、`H`，同时检查目标色域与 sRGB fallback |
| 色阶 | 同一色系有哪些可复用的浅深层级？ | Seed / Map 层；编号只表示稳定顺序，不冒充明度百分比 |
| 语义角色 | 颜色承担什么界面职责？ | Alias 层；background、surface、text、border、primary、accent、status、overlay 等 |
| 模式与状态 | 在 light/dark、hover/pressed/selected/focus/disabled 下如何变化？ | `mode`、`stateLayer` 与成对的前景／背景／边框角色 |
| 组件映射 | 具体控件使用哪组角色？ | Component 层；按钮、输入、选择、弹窗与状态反馈分别映射 |

`assets/joyally-design.tokens.json` 是可执行样本。现有湖色以 sRGB 十六进制保存以兼容各平台；新增主题应先在 OKLCH 中控制感知明度和彩度，再输出目标平台格式。不要在 HSL 与 OKLCH 中用同名“饱和度／彩度”互换数值。

## 基础语义角色

- **背景与表面**：`background` 是页面底层；`surface` 是卡片、面板或弹窗自身底色；`surfaceElevated` 用于浮层；`surfaceMuted` 用于弱分区。表面角色不等于透明材质，透明度另由 material contract 管理。
- **文字与边界**：`text`、`textSecondary`、`textTertiary` 逐级降低强调；`border` 用于普通分隔，`borderStrong` 用于需要 3:1 可见边界的控件或功能图形。不要用低对比普通分隔线承担控件边界。
- **品牌与强调**：`primary` 表示品牌识别，`primaryAction` 表示主要操作，`accent` 只承担局部强调。三者可以同源，但不能因为色相相同就共用全部状态值。
- **状态**：success、warning、error、info 的含义跨主题和模式保持稳定；颜色必须配合文字、图标或形状，不单独传达结果。
- **遮罩**：`overlay` / scrim / backdrop 是弹窗后的压暗层，不是 surface，也不是把整个容器降低 opacity。遮罩透明度在最终合成背景上验收。

## 双模式角色

light 与 dark 是两套完整语义映射，不是把同一十六进制反相。每套模式至少交付 background、surface、surfaceMuted、surfaceElevated、text、textSecondary、border、borderStrong、primaryAction、onPrimaryAction、primaryContainer、onPrimaryContainer、四种状态色、focus、disabledSurface、disabledText 和 overlay。

切换模式时保持角色含义与组件几何不变，重新检查每一对前景／背景。深色模式中的彩色文字通常需要提高感知明度、降低大面积彩度；阴影不能代替边界，浮层也不能只靠比背景更黑来区分。

## 交互状态矩阵

每个可操作组件都显式处理以下状态；没有某状态时说明原因，不用默认透明度隐式派生：

| 状态 | 含义 | 颜色要求 |
| --- | --- | --- |
| default | 可操作的稳定状态 | 记录 foreground / background / border |
| hover | 指针已移入、尚未激活 | 变化可见但弱于 selected；触屏不依赖 hover |
| pressed | 指针或触控正在按下 | 与 hover 不同，短暂且更强；不能与 selected 混用 |
| selected | 选择在操作结束后持续保留 | 使用容器色并保留文字或图标证据 |
| focus-visible | 键盘焦点 | 独立 focus ring；不能只复用 hover 或 selected |
| disabled | 当前不可操作 | 标签仍可辨认，且行为上真正禁用；不只降低 opacity |
| loading | 操作进行中 | 保持控件尺寸与语义，避免用变淡冒充 disabled |

`stateLayer` 的 alpha 只描述必要的状态叠层强度；组件优先使用已解析的 Component token。半透明叠层必须在合成后的最亮、最暗代表背景上复查，不能只检查源色。

## 对比度与色域门禁

- 普通文字至少 4.5:1；大字、功能图标、焦点环和控件可见边界至少 3:1。
- Joyally Design 的 disabled 标签仍以 3:1 为辨认底线；这不替代真正的禁用行为、辅助技术状态与恢复说明。
- `border` 可以是安静的装饰分隔；承担输入框、按钮或图形边界时必须使用能通过 3:1 的 `borderStrong`。
- 透明表面、渐变、图片和遮罩按运行时合成色验收；至少覆盖最亮和最暗的代表背景。
- OKLCH 调色后检查目标设备色域；超出目标色域时降低 chroma，并验证 sRGB fallback 没有色相跳变、状态混淆或对比度倒退。
- 静态 token 校验只是基础门禁。最终仍需检查真实组件的 default、hover、pressed、selected、focus-visible、disabled、loading，以及 light/dark 和 reduced transparency。

## 术语来源与取舍

术语分组参考公众号“柯基的科”的[《颜色：27 个术语图解》](https://mp.weixin.qq.com/s/y5iWwzbjVPxacIBmhhJ9Tw)：界面角色、品牌与状态、色相／明度／彩度／饱和度、色阶／透明度／遮罩、五种交互状态、明暗主题／对比度，以及颜色值／色板／语义颜色／颜色变量。本文将这份速查表转成 Joyally Design 的 token、模式、组件与验收契约；可访问性阈值和实现规则仍以本 Skill 的验证契约为准，不把术语图解当作完整设计系统规范。
