# H5 界面

从 [主入口](../SKILL.md) 进入面向手机浏览器的 H5 页面设计时读取；桌面后台和原生 App 仍走各自平台路径。

Joyally 自有 React H5 新界面使用 [shadcn/ui](https://ui.shadcn.com/docs/components) 作为主组件体系，并同时读取 [React 组件工作流](component-workflow.md)。服务其他产品、非 React 页面或存量改造时，先沿用项目现有组件、Vue 或原生 HTML 结构，以项目语义 tokens 定义主题；只有现有基础无法满足本次需求且已确认迁移范围时才换组件。选择组件时保留表单值、事件与导航行为。

shadcn/ui 的交互组件保留 Radix 等底层行为；项目仍须核对弹层定位、虚拟键盘、safe area、触控热区、返回导航和状态恢复。选择手绘主题时完整使用 Looseleaf registry，不把桌面端倾斜、阴影或装饰密度原样压进窄屏；在真实手机视口和触控设备上验收。
