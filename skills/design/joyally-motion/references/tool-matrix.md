# 20 个开源工具的能力矩阵

本矩阵用于选型，不要求安装全部工具。能力和许可证于 2026-11-21 从各项目官方 GitHub 仓库核对；采用前仍以目标版本的源码、许可证和项目约束为准。视频 [《AI 做动画能有多炫？10 分钟看 20 个开源工具》](https://www.bilibili.com/video/BV1vpWq6xENs/) 是本组项目的发现来源，能力边界与许可结论来自官方仓库。

## 选型顺序

1. 先选输出：产品 UI、网页动态图形、可寻址视频、角色资产、传统 2D/3D 源文件，或实时交互场景。
2. 再选时间模型：状态驱动、wall clock、物理积分、authoring timeline，或任意时间点可 seek 的确定性时钟。
3. 最后选实现：优先沿用现有栈；新增工具必须解决明确缺口。相邻工具可以做概念验证，但生产链路只保留必要角色。

## Web、UI 与动态图形

| 工具 | 最适合 | 选择信号 | 边界 | 官方许可 |
| --- | --- | --- | --- | --- |
| [Anime.js](https://github.com/juliangarnier/anime) | DOM、SVG、对象属性的通用时间线 | 需要轻量 timeline、stagger、路径或多目标编排 | 不负责 React 状态模型或视频渲染 | MIT |
| [Motion](https://github.com/motiondivision/motion) | React 与 JavaScript 的产品动效、手势和 layout animation | React 产品需要声明式状态、presence、drag 或共享布局 | 不因项目使用 React 就自动替换已有 motion 栈 | MIT |
| [React Spring](https://github.com/pmndrs/react-spring) | 由物理感驱动、可中断的 React 状态动画 | 连续输入、拖拽或状态变化需要 spring 响应 | 精确镜头节拍和逐帧复现通常需要额外时间控制 | MIT |
| [mo.js](https://github.com/mojs/mojs) | Web motion graphics、burst、shape 和短促反馈 | 需要图形化爆发、粒子式强调和自定义 easing | 高频产品 UI 不应被装饰性爆发淹没 | MIT |
| [Flubber](https://github.com/veltman/flubber) | SVG path 与形状间平滑插值 | 输入是不同拓扑的 SVG 形状，需要可靠 morph | 只解决形状插值，不是完整动画系统 | MIT |
| [KUTE.js](https://github.com/thednp/kute.js) | 浏览器 tween 与 SVG morph | 需要模块化 tween、路径、颜色和 transform 插值 | 与主 timeline engine 能力重叠时不重复引入 | MIT |
| [AnimXYZ](https://github.com/ingram-projects/animxyz) | 基于 CSS utilities 的组合式进入退出 | 内容站或组件库需要低成本一致预设 | 复杂 choreography、物理和确定性视频不是其主场 | MIT |
| [Lottie Web](https://github.com/airbnb/lottie-web) | 播放 After Effects 导出的矢量 timeline | 设计师交付 JSON 资产，runtime 只需播放、seek 和事件 | After Effects 特性并非全部可导出；资产本身另行授权 | MIT |
| [Rive Web Runtime](https://github.com/rive-app/rive-wasm) | 带状态机、输入和交互的矢量动画 | 资产需要在 runtime 根据 hover、数值或业务状态响应 | runtime 开源不等于 authoring 服务、文件和字体自动获权 | MIT |

## 代码视频与解释动画

| 工具 | 最适合 | 选择信号 | 边界 | 官方许可 |
| --- | --- | --- | --- | --- |
| [Remotion Skills](https://github.com/remotion-dev/skills) | Agent 使用 Remotion 制作 React 视频的指导材料 | 目标链路已经选择 Remotion，并需要其官方 Agent 约定 | 这是 Skills 仓库，不是 renderer；仓库根未声明许可证，保持链接引用，不复制内容；Remotion 产品许可单独核对 | 未声明 |
| [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | TypeScript、Canvas 驱动的可编程解释动画 | 需要 timeline、scene、代码可读性和视觉化调试 | 不是普通产品 UI runtime | MIT |
| [Manim Community](https://github.com/ManimCommunity/manim) | 数学、几何、公式和推导演示 | 核心内容是精确数学对象及其变换 | 产品界面、角色和实时交互需其他工具 | MIT |

## 角色与传统 authoring

| 工具 | 最适合 | 选择信号 | 边界 | 官方许可 |
| --- | --- | --- | --- | --- |
| [Inochi2D](https://github.com/Inochi2D/inochi2d) | 分层 2D 角色绑定和实时 puppet | 已有分层插画，需要参数、网格和实时表情动作 | 需要专门的分层资产与 rig；模型文件另行授权 | BSD-2-Clause |
| [OpenToonz](https://github.com/opentoonz/opentoonz) | 传统 2D、逐帧和扫描上色制作 | 需要完整桌面 authoring、xsheet 和手绘流程 | 桌面制作链，不是 Web runtime；third-party 目录另有许可 | BSD-3-Clause 为主 |
| [Synfig](https://github.com/synfig/synfig) | 矢量 2D cut-out 与补间动画 | 希望减少逐帧绘制并保留可编辑工程 | GPL 约束作用于软件分发与改造，项目集成前单独复核 | GPL-3.0 |
| [Blender](https://github.com/blender/blender) | 3D 建模、绑定、动画、模拟与渲染 | 需要真正的 3D 资产、镜头、材质或复杂模拟 | 高成本 authoring；模型、贴图、插件和输出素材分别核权 | GPL |

## 实时 2D、3D、物理与粒子

| 工具 | 最适合 | 选择信号 | 边界 | 官方许可 |
| --- | --- | --- | --- | --- |
| [Three.js](https://github.com/mrdoob/three.js) | Web 3D、相机、材质、shader 和后处理 | 浏览器场景需要真实深度、光照或 GPU 效果 | 需要自行管理场景、资源、时钟、性能和输入 | MIT |
| [Godot](https://github.com/godotengine/godot) | 完整 2D/3D 游戏与交互应用 | 需要场景树、物理、脚本、编辑器和跨平台导出 | 对单个网页微交互过重；导出平台与第三方组件另查 | MIT |
| [Matter.js](https://github.com/liabru/matter-js) | 浏览器 2D 刚体物理 | 动画必须由碰撞、约束、重力或连续模拟产生 | 物理真实不等于视觉节奏正确；可复现导出需固定步长和 seed | MIT |
| [tsParticles](https://github.com/tsparticles/tsparticles) | 可配置粒子、烟花、confetti 和背景效果 | 需要成熟粒子系统及框架适配 | 控制粒子量、交互监听和后台运行；不替代主叙事 | MIT |

## 组合建议

1. 产品 UI：现有平台能力或 Motion / React Spring 作为主状态动画；Flubber 或 KUTE.js 只补形状插值；Lottie / Rive 作为独立资产 runtime。
2. 数据叙事：主 timeline 加 SVG/Canvas；只有真实深度需要 Three.js，只有真实碰撞需要 Matter.js，只有大量粒子需要 tsParticles。
3. 代码视频：选择 Remotion、Motion Canvas 或 Manim 中一个主 renderer；Web runtime 作为受控子场景时必须接受同一个 seekable clock。
4. 角色：Inochi2D、Rive 或传统 authoring 取决于输入资产和交互需求；不要在没有分层源稿或 rig 计划时承诺实时角色。
5. 游戏与沉浸式体验：Godot 负责完整应用；Three.js 负责浏览器场景。两者互换通常意味着重做运行时，而不是替换一个依赖。
