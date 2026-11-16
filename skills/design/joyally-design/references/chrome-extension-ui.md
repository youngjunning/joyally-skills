# Chrome 扩展界面

从 [主入口](../SKILL.md) 进入 Chrome 扩展的 popup、options、side panel 或独立窗口设计时读取。扩展图标另读 [扩展图标](chrome-extension-icon.md)。

## 组件基础

Joyally 自有 React Chrome 扩展新界面使用 [shadcn/ui](https://ui.shadcn.com/docs/components) 作为主组件体系，并同时读取 [React 组件工作流](component-workflow.md)。服务其他产品、非 React 扩展或改造已有扩展时，先沿用现用组件和 Vue 或原生 HTML/JavaScript 结构并核对交互合同；只有现有基础无法满足本次需求且已确认迁移范围时才换组件。主题从项目语义 tokens 派生。

扩展页面中的生成 CSS、脚本、字体和图标随 Manifest V3 安装包本地提供，不在运行时从 CDN 加载代码。构建产物只包含本扩展实际使用的样式与资源；核对打包清单、CSP 和相对路径。

保留项目已有的值、事件、表单提交和状态恢复语义，在实际 popup、side panel、options 与独立窗口检查控件外观、键盘操作、焦点、读屏名称和弹层裁切。选择手绘主题时完整使用 Looseleaf registry，并把字体、SVG 绘制层和组件依赖一起打入扩展包；不得在运行时从外部站点加载代码或字体。普通文本与只读数据仍可使用语义 HTML。
