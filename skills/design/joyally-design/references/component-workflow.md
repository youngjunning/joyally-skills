# React 组件工作流

用于编码 Agent 在 Next.js Web 的中后台、展示页，以及 H5 与 Chrome 扩展中选择、安装和组合组件。Joyally 自有中后台及可交互 Demo 使用 Next.js App Router，基础控件来自项目维护的 Joyally 组件库，Magic UI 必须在代表页面中承担明确的视觉或交互职责。Joyally Design 负责设计语义、状态和页面组合；React Bits 仍按需选用。静态报告、一次性介绍页与 HTML PPT 走各自交付模式，H5 和扩展也须读取平台参考；React Native 沿原生路径。

1. **检查项目。** 先读项目指令、`components.json`、现有 `components/ui`、主题变量和包管理器。列出本次界面需要的操作、输入、数据、导航与反馈部件，以及项目已有实现。完成条件：每个部件有现成组件、待安装组件或明确的组合方案。
2. **选组件。** 在 [shadcn/ui 组件目录](https://ui.shadcn.com/docs/components)按基础部件检索，用项目内 Joyally 组件源码承载按钮、输入、列表、反馈等操作；在 [Magic UI 组件目录](https://magicui.design/docs/components)选能帮助理解任务或反馈的组件，接入实际页面并记录用途，不能只把依赖写进 `package.json`。文字、背景与微交互可按需查 [React Bits 组件目录](https://www.reactbits.dev/)。Magic UI 借鉴 shadcn/ui；两库均可通过 shadcn CLI 按组件接入，但每个依赖、样式、行为与许可仍须逐项核对。已安装组件直接读项目源码与用例。Joyally 自有新界面用官方 CLI 的 `add --all` 建立完整 shadcn/ui 基础；选择[手绘主题](hand-drawn.md)时改用 `@looseleaf/looseleaf` umbrella registry，避免混装默认外观。其他项目沿用现有组件，局部功能只安装选中的组件。先运行当前 CLI 的 `--help` 核对命令和包管理器，再执行安装；安装或更新后逐文件审查本地差异，保留业务变体、可访问行为和项目 tokens。对 Data Table、Date Picker 等组合控件，分别确定底层依赖及数据契约。完成条件：组件来源、文件路径、页面导入与组合依赖可回查；手绘主题另须核对完整 registry coverage。
3. **落地 Joyally。** 读 [React 设计系统](react-design-system.md)与 [token 契约](token-contract.md)，将目标主题的 seed、map、alias、component 角色接入项目。基础控件保留官方键盘和可访问性行为；业务术语、路由、校验和数据源沿用目标项目。已有品牌使用项目品牌派生 tokens，不照搬 Joyally 展示站的色值。完成条件：代表性页面上的基础控件与组合控件共用语义角色。
4. **验收。** 在真实页面检查默认、hover、focus、disabled、loading、empty、error 和 success，以及桌面、窄屏、键盘和 reduced motion。逐个核对本次新增或修改的按钮、输入框、选择器等控件是否真正加载所选组件样式与语义 tokens；若仍呈现浏览器默认外观，修复样式接入或改用对应组件后再交付。手绘主题还要扫描同类组件是否残留默认 shadcn 外观，并检查 seed 生成的 SVG 在 SSR 与 hydration 后一致。浮层需实际打开，表单需触发校验和恢复，表格需操作搜索、排序或分页。源码存在、构建通过和页面可用分别记录证据；目录链接也要点击确认目标可读。完成条件：本次涉及的每个组件都有可见预览或实际页面状态，且关键操作有结果。

给编码 Agent 的任务可以这样写：

> `$joyally-design 在这个 React 中后台实现任务列表。先检查现有组件与主题；选用 Button、Input、Select、Table 和反馈组件，在现有数据层上组合搜索、筛选、分页与空状态。保留项目业务逻辑，验证窄屏、键盘和错误恢复，并列出实际使用的组件源码路径。`

展示站点用于选型参考。编码 Agent 从目标项目中已安装组件、shadcn/ui 官方 CLI、[Magic UI 安装入口](https://magicui.design/docs/installation)或 [React Bits 安装入口](https://www.reactbits.dev/get-started/installation)获取所选组件源码，并在目标项目的真实页面中验收。记录组件名称、上游链接、变体、引入的依赖和许可声明；[React Bits 许可](https://github.com/DavidHDev/react-bits/blob/main/LICENSE.md)使用 MIT + Commons Clause，组件源码留在使用它的应用内，不随 Joyally Design 技能或独立组件包再分发。
