# 手绘主题

手绘主题把产品界面组织成真实的纸上工作空间：桌面承载页面，纸张、便签、索引卡、胶带、印章和笔迹表达层级与状态。它不是线框稿，也不是在标准卡片外加一圈抖动边框。内容顺序、业务动作、键盘行为和语义状态继续遵守 Joyally Design；React Web 的组件实现直接采用 [Looseleaf](https://github.com/kevintngo/looseleaf) 对 shadcn/ui 的完整手绘实现。

## 组件基线

Joyally Design 的 React Web 主组件体系是 shadcn/ui。选择手绘主题时，完整基线切换为 Looseleaf umbrella registry：它保持 shadcn/ui 的 parts、props 与 `data-slot`，并以 Radix 保留组件语义。2026-11-17 核对的官方仓库提交 `4bdb647940e2fefb3cebb394f3bad25c766a27d2` 包含 123 个 `registry:ui` 组件；来源与许可证见[核对记录](../assets/references/looseleaf/README.md)。

先检查目标项目的 `components.json`、Tailwind 版本、现有 `components/ui` 和未提交改动。新建 Joyally React Web 且明确选择本主题时，把官方 registry 加入 `components.json`，再安装完整入口：

```json
{
  "registries": {
    "@looseleaf": "https://kevintngo.github.io/looseleaf/r/{name}.json"
  }
}
```

```bash
npx shadcn@latest add @looseleaf/looseleaf
```

该入口会把主题、字体、ink engine 与全部组件作为本地源码写入项目，并覆盖全局主题变量。安装前查看当前 CLI 帮助和 diff；安装后逐项核对冲突，保留业务逻辑、路由、表单语义和项目独立修改。存量项目只有在用户明确选择整套手绘主题并接受组件替换范围时才执行完整切换。Looseleaf 的 blocks 是页面组合示例，按任务选用，不把示例业务、角色或文案带入产品。

组件完整性以实际 registry 和落地源码为准。主题验收时核对 123 个官方 `registry:ui` 依赖均由 umbrella 入口覆盖；页面不得混入仍呈现默认 shadcn 外观的 Button、Input、Select、Dialog、Table、Sidebar、Toast、Calendar、Chart 或其他同类控件。业务自有组件必须从这些 primitives 组合，并继承同一纸张、笔触、字体、状态与密度变量。

## 空间与视觉语法

1. 桌面是外围画布，主任务落在一张稳定纸面；支持信息可使用便签、索引卡、纸条或软木板。纸张身份用于说明层级，不把每段内容都做成一张倾斜卡片。
2. 导航像笔记本目录、索引页或分隔标签，主要工作区像展开的页、清单或计划板。遮去颜色后，仍能从纸张层次、边缘、装订与标记方式辨认主题。
3. 主要操作使用实色笔迹或印章；选中可使用荧光笔、勾选或手绘下划线；错误、成功和警告保留文字或图标，不只靠红绿墨水。
4. 线条由确定性 seed 生成，服务端与浏览器得到同一形状。真实 DOM 承担文字、输入、命中区和辅助技术语义，`svg[data-ink]` 只负责笔迹层。
5. 贴纸、涂鸦、图钉、胶带和吉祥物只出现在品牌时刻、空状态或解释性内容中；长文、表格、日志和代码保持平整、稳定、可选择的纸面。

具体色值见[手绘主题 token 样本](../assets/hand-drawn-theme.tokens.json)。纸张、桌面、墨水、铅笔、荧光笔和语义色先映射到 Joyally Alias tokens，再由 Looseleaf 组件变量消费；不要在业务页面另写一套“手绘色”。当前官方主题是浅色纸张体系。深色模式需要在目标项目另建完整变量映射并逐组件验证，不能用滤镜或自动反色冒充支持。

## 字体、图标与动效

Looseleaf 的 Kevin Sans 用于 Latin 界面文字、标题和印章，IBM Plex Mono 用于代码。Kevin Sans 不覆盖中文；中文界面优先使用项目已许可、可读性合格的中文手写字体，未配置时使用系统中文字体回退，并保留纸笔组件语言。不要通过逐字随机旋转伪造中文手写感。

通用功能图标优先使用 Looseleaf 随包的 ink icons；品牌图标仍使用品牌方素材。纸张投放、笔迹绘制与按压位移只表达进入、选择和确认，`prefers-reduced-motion` 或 `data-motion="reduced"` 下停止绘制、抖动与循环。组件在关闭纹理、动效和装饰 SVG 后仍须可操作。

## 验收

用同一内容、同一任务和同一视口与其他主题并排检查桌面、导航、主工作区和一条关键操作。完成条件是：主题结构差异不依赖配色；完整组件 inventory 已核对；默认、hover、pressed、selected、focus、disabled、loading、empty、error、success 都由 Looseleaf 组件或同语法组合承载；键盘、触控、窄屏、200% 放大、RTL、forced colors 和 reduced motion 可用；SSR 与 hydration 不因随机笔迹产生差异；字体、源代码和许可证随项目制品保留。源码存在、构建通过、组件预览、真实业务页面与部署分别报告，不互相代替。
