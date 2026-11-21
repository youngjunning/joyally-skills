---
name: joyally-design
description: 设计和精修 Web、macOS、iOS、Android 与 React Native 界面，也用于 HTML 报告、HTML PPT、社交卡片、可探索图表以及图像任务的视觉方向与构图设计。它主导设计决策与设计验收；文稿交给 joyally-writting，像素生成和图像技术验收交给 joyally-image。三者可独立使用，联合任务仅设一个整体主导 Skill。
---

# Joyally Design

将层级、材质、颜色、间距与证据呈现用于用户的实际主题。保留事实、链接、标题、数据与交互，不植入来源产品的角色、术语或业务流程。

先由用户任务、现有产品和品牌决定界面，再选领域设计方法、组件基础与视觉方向。页面用途先区分中后台与落地页：中后台支持持续的查找、处理与确认，落地页向访客介绍价值并引导下一步。这是界面任务分类，不是前后端架构或部署边界；同一网站可以同时包含两者。通过任务路径、视觉构思、存量改造和真实画面走查形成与检验方案；语义 tokens、跨平台组件状态、主题资产、报告与交互图表能力按任务使用。逐项说明采用什么、保留什么，以及依据。

Joyally Design 是跨平台的设计方法与实现契约：从产品目标、读者、品牌和使用情境出发，形成语义 tokens、组件行为、内容层级和可验证的交付。当前八套并列主题为「青山湖」「西湖」「苏州园林」「马尔代夫」「阿尔卑斯雪山」、[香奈儿风](references/fashion-xiaoxiang.md)、[太空](references/space.md)与[手绘](references/hand-drawn.md)。青山湖正在按四季各 5 张授权实拍重建参考画册，已核实数量和缺口见[参考目录](assets/references/qingshan-lake/README.md)；西湖、苏州园林、马尔代夫、阿尔卑斯雪山、香奈儿风与太空各有 20 张可追溯参考画面。前五套按[景观视觉规则](references/visual-language.md)观察地点，香奈儿风观察包袋、山茶花、巴黎夜景、服装细节与编辑呈现；太空主题从真实拍摄与观测影像中的轨道、行星地平线和空间关系建立视觉方向；多帧拼接或科学波段着色需说明。手绘主题以 [Looseleaf](https://github.com/kevintngo/looseleaf) 的完整 shadcn registry、纸笔视觉语法和可访问状态为实现来源，核对记录见[来源目录](assets/references/looseleaf/README.md)。八套共用操作语义、组件状态与可读性契约。既有参考画面位于[青山湖](assets/references/qingshan-lake/README.md)、[西湖](assets/references/west-lake/README.md)、[苏州园林](assets/references/suzhou-gardens/README.md)、[马尔代夫](assets/references/maldives/README.md)、[阿尔卑斯雪山](assets/references/alpine-snow-mountains/README.md)、[香奈儿风](assets/references/xiaoxiang/README.md)与[太空](assets/references/space/README.md)；苏州园林同时包含[留园画面](assets/references/lingering-garden/README.md)。服务其他品牌时保留设计方法和语义契约，视觉按该品牌派生。方法的唯一维护源为本目录；三位角色的参考素材随包保留，产品服务和上传配置由使用项目管理。

当用户明确需要小界、小萌或小南时，按[角色参考素材](references/character-assets.md)取用随包全身像、上半身图与头像；通用设计不默认植入角色。

设计任务先按[完整设计流程](DESIGN_PROCESS.md)选择领域与阶段，再按[设计方法](references/fused-method.md)组织事实、结构、组件、状态与验收；按[能力路由](references/capability-routing.md)读取本目录的领域参考并调用工具。

创建、重做或扩展整套视觉主题时，同时按[主题制作](../joyally-theme-creation/SKILL.md)检查空间结构、组件细节、同内容差异与真实状态；单点配色微调沿用当前小改动路径。

领域、方向、存量改造、组件、素材、动效、截图、评审与规范构成主流程；[专项质量检查](references/design-quality.md)仅在文字本地化、健壮性或技术审计等实际问题出现时加入。Joyally 的视觉语言、语义 tokens、跨平台行为与验收把这些方法连成同一套输出。明确改法的小改动直接完成，任务范围和交付物仍由用户决定。

## 三技能协作边界

Joyally Design、`joyally-writting` 与 `joyally-image` 是可独立使用的合作技能。单一专业任务只进入匹配的 Skill；只在交付物真实跨越文字、容器、图像中的两个或三个领域时协作，不为凑齐三者而增加流程。

- 每个联合任务只设一个主导 Skill。主导 Skill 按用户要求的最终交付物选定，负责拆分、组装、整体验收与交付；支持 Skill 只完成明确的子产物，不重新规划整个任务。
- `joyally-writting` 是读者、事实、论点、叙事结构与准确文案的责任人；Joyally Design 是视觉方向、构图规则、信息层级、版式与字体、品牌适配、交互、语义 tokens、组件状态与设计验收的责任人；`joyally-image` 是像素落成、角色身份连续性、生图/改图、图像格式与技术质量的责任人。
- 跨域变更回到对应责任人。本 Skill 可调整容器中的排版、换行与展示层级，但不自行改写已核定的事实、论点、长文案或图像内容；需要变更时提出具体约束并请原责任人返回新版。
- 交接使用最小可验收契约：用途与读者、已锁定内容、可变项、尺寸/格式、必须保留项和验收条件。支持产物返回后，主导 Skill 只验证集成与整体效果，不越界重做子产物。

用户明确指定一个 Skill 时，它默认为主导 Skill；同时指定多个时，按最终交付物确定唯一主导 Skill。若指定内容与所需交付物不匹配，保留用户意图并说明建议的交接，不由多个 Skill 并行争夺主导权。

当图像任务需要新建或改变视觉方向、构图体系、品牌语言、版式字体或审美标准时，由 Joyally Design 主导设计阶段，将经验收的设计 brief 交给 `joyally-image` 落成。已有明确设计 brief 的直接生图、局部改图、格式转换与图像技术修复无需重复设计。

## 纸面与静态成品

纸面与静态成品是 Joyally Design 的内建交付模式，不是另一套产品 UI 体系。内容已锁定、以单页或分页阅读为主的 PDF、PNG、可编辑 PPTX 或静态 HTML，先由 Joyally Design 确定读者、信息层级、品牌适配、素材职责和验收，再使用本 Skill 的报告、演示、社交卡片或静态 HTML 路径完成排版与渲染。典型场景包括 one-pager、方案、长文档、信件、简历、作品集、打印型报告、静态演示稿和社交卡片。

静态模式不替代需要持续操作、响应式状态、复杂导航或长期维护的产品网页、工作台、原生 App、交互图表与 HTML PPT；这些仍使用 Joyally Design 的平台路径、组件体系和生成器。一次性的静态产品介绍页只在无需复杂交互、多语言站点结构或产品级组件维护时采用。

静态成品沿用 Joyally 的设计契约：从所选主题或项目现有 tokens 派生颜色、字体、表面、间距和层级；保留品牌识别与语义色，不把任何外部模板的纸张、墨色或字体默认值带入成品。最小 brief 包含用途与读者、已核定的文案和事实、品牌素材与可用颜色、目标格式与页数、屏幕或打印优先级、可变项、必须保留项和验收条件。输出后检查结构、渲染与逐页视觉效果；再复核品牌一致性、信息层级、可读性和对应交付场景的体验。浏览器成品还需检查桌面与窄屏。

### 分流与交接示例

1. **一页方案给管理层决策**：用户提供已审定的目标、三项证据、预算和下一步，要求一张可打印的中文 PDF。Joyally Design 先确认最重要的结论、品牌色和证据顺序，再用静态报告路径制作 one-pager；交付写明“1 页、A4、打印优先、保留全部数字与来源链接”。输出 HTML、PDF 和页面图后，检查结论是否首屏可见、表格是否可读、品牌色与打印对比度是否合格。
2. **八页技术分享，需要现场演讲与讲稿**：虽然内容已基本完成，但需要逐页播放、演讲者视图、动效控制和离线单文件交付。这走 Joyally Design 的 `deck` 路径，检查翻页、讲稿、投屏画面、窄屏预览及导出 PDF。若会后要把同一内容整理成可打印的六页讲义，单独建立阅读型静态成品，不复用演示运行时。
3. **产品功能的一次性静态介绍页**：已有品牌 logo、三张产品截图和锁定文案，目标是给合作方邮件附上一个静态 HTML 与 PDF，不需要表单、账户、深链接或持续维护。Joyally Design 定义首屏主张、截图裁切和品牌色，用静态 HTML 路径实现，并要求“桌面与窄屏均可读、保留截图原比例、无虚构指标”。若后续增加注册流程、导航、国际化或长期更新，则迁入 Joyally Design 的落地页路径。

## 可选配套安装提示

本轮首次使用 Joyally Design 时，检查当前环境是否已提供 `joyally-writting` 和 `joyally-image`。只对缺失的 Skill 在首次进度更新末尾集中建议一次，说明它们是可选协作能力，不阻塞当前任务；已安装或本轮已提示时不重复。

```bash
npx skills add youngjunning/joyally-skills --skill joyally-writting -g
npx skills add youngjunning/joyally-skills --skill joyally-image -g
```

## 现有界面精修

所有涉及界面设计决策的任务都从本 Skill 进入；用户给出截图并要求调整页面、指出操作拥挤或视觉不协调时尤其如此。先读取实际界面、目标任务路径和项目现有组件与 tokens；按[能力路由](references/capability-routing.md)进入精修、回改或存量项目路径。交互缺陷与视觉问题同在一个操作区时，与工程排障一起处理：先确认状态和下一步动作，再调整布局与层级，最后检查颜色与细节。文字、本地化、健壮性或技术审计问题再读[专项质量检查](references/design-quality.md)。不要只改装饰而保留难以发现、无法继续或语义相反的操作。

交付前在目标页面核对主要操作、恢复路径、加载与禁用状态，以及实际支持的窄屏；源码、构建和截图各自只证明对应范围。纯业务逻辑或 API 改动没有界面决策时，不因同属前端仓库而触发本流程。

## 跨平台路径

先盘点产品任务、既有 tokens、共享组件、输入方式和信息密度，保留平台原生导航。交付界面先确定组件来源：已有项目使用现行组件库和样式体系；没有组件基础时按目标平台选定并记录，不把逐页手写原生控件样式当作默认方案。Joyally Design 管理语义 tokens、共享组件变体、交互状态和页面组合，具体控件由所选平台组件基础承载。所有平台先读 [统一 token 契约](references/token-contract.md) 与 [验收](references/validation.md)，再选择对应参考：

| 目标 | 参考 |
| --- | --- |
| macOS / SwiftUI / AppKit | [macOS](references/macos.md) |
| iPhone / iPad | [iOS](references/ios.md) |
| Android 原生 App / Compose | [Android](references/android.md)；使用 Jetpack Compose Material 3 |
| React Native / Expo | [React Native](references/react-native.md) |
| H5 页面 | [H5 界面](references/h5-ui.md)；Joyally 自有 React 新界面使用 shadcn/ui，非 React 或存量项目沿用现有组件基础 |
| 中后台／工作台（React Web） | 新建中后台使用 Next.js App Router，按[官方安装文档](https://nextjs.org/docs/app/getting-started/installation)建立项目；读 [React](references/react-design-system.md) 与[工作台](references/web-dashboard.md)。Joyally Design 的 React Web 主组件体系为完整 shadcn/ui，可按任务加入 Magic UI 或 React Bits 组件；存量项目沿用现有架构和组件，框架迁移单独评估 |
| 落地页（含官网首页、产品介绍页） | [Landing page](references/web-landing-page.md)；按实际平台选组件基础，需要展示或交互动效时再考虑 Magic UI、React Bits；制作产品界面演示、Banner 或 Bento 展示素材时读 [StageShow 接入](references/stageshow.md) |
| Chrome 扩展界面 | [扩展界面](references/chrome-extension-ui.md)；Joyally 自有 React 新界面使用 shadcn/ui，非 React 或存量扩展沿用现有组件基础 |
| Chrome 扩展图标 | [扩展图标](references/chrome-extension-icon.md) |

按交付场景选组件基础：Joyally Design 的 React Web 主组件体系统一为 shadcn/ui，H5 与 Chrome 扩展的 React 新界面仍按各自平台路径处理触控、尺寸、CSP 和打包；非 React 页面、React Native 与其他原生平台沿用对应组件基础。其他项目已有组件体系先沿用并按获准范围升级。

移动端保留原生触控热区与字体缩放；桌面根据任务选择信息密度。先布局与层级，再语义颜色、表面、组件状态，最后加入品牌氛围与动效。原生示例和随包湖色预设见 [平台视觉参考](references/native-visual-system.md)。

## 选择路径

先按交付物确定主导 Skill，再选择视觉风格。用户明确指定 Skill 时优先遵从；未指定时按下表路由：

| 交付物 | 主导 Skill |
| --- | --- |
| 文章、PPT 或分享使用的静态架构图、知识图谱、流程图片 | `joyally-image` |
| 可点击、缩放、聚焦节点或探索路径的交互图表 | `joyally-design` |
| 可折叠、缩放、持续编辑的思维导图 | `joyally-design`；读 [思维导图](references/mindmaps.md)，保留 Markmap 源文件 |
| 可编辑、按职责组织的分层架构图 | `joyally-design`；读 [分层架构图](references/layered-architecture.md)，保留 HTML 源文件 |
| 网页或工作台的新建与局部精修、报告整体设计、跨平台设计系统 | `joyally-design`；其中的静态插图交给 `joyally-image` |
| 内容已锁定的 one-pager、方案、长文档、信件、简历、作品集、打印型报告、静态演示稿或社交卡片 | `joyally-design` 的静态成品模式；按报告、演示、社交卡片或静态 HTML 路径排版、渲染与逐页检查 |
| Chrome 扩展图标的设计、尺寸适配和真实工具栏验收 | `joyally-design` 主导小尺寸识别与使用情境；需要生成源图时调用 `joyally-image` |

仅说“画架构图”且现有交付上下文未要求交互时，默认按静态图片处理。Joyally Design 可提供配色、字体、层级与材质参考；采用这些视觉规范不改变主导 Skill，也不自动增加交互页面。生成工具、绘制方式与视觉风格分别确定；`joyally-image` 的结构图仍按其知识图谱流程完成精确文字和箭头排版。

1. 新建报告：明确读者、决策与证据结构，读取 [设计系统](references/design-system.md)、[报告语言](references/report-language.md)、[布局](references/layout.md) 与 [HTML 报告](references/html-reports.md)。报告只用 Joyally 自有模板和样式。
   制作需要逐页播放、讲稿或现场演示的 HTML PPT 时读[演示文稿](references/presentations.md)，选 Joyally 主题并用独立的 `deck` 命令；阅读型报告继续用 `report`。
   制作社交平台封面、轮播内页或可分享图文时读[社交卡片](references/social-cards.md)，按内容选 `editorial`、`swiss` 或 `poster`，生成单张 HTML 并导出 PNG；这一路径与阅读型报告、演示文稿分别交付。
   当报告或演示转为内容已锁定、纸面优先的静态成品时，按“纸面与静态成品”选择对应 Joyally 输出路径；需要可编辑 PPTX 时在 brief 中明确格式。不要同时以 `report`、`deck` 与静态文档重复出多版，先确定一次明确交付。
2. 改造已有 HTML：先读 [改造约定](references/adapting-existing-html.md)，保留 DOM、锚点、事件与导出功能，优先增加 scoped theme。
3. React 设计系统：读 [React 约定](references/react-design-system.md)，依次核对 tokens、共享 primitives、组件状态和页面组合。
   编码 Agent 需要为 React Web 选用、安装或组合组件时，再读 [React 组件工作流](references/component-workflow.md)，从目标项目或选定来源取得真实源码，并逐项验收预览。
4. 交互图表：读 [交互图表](references/interactive-diagrams.md)；需要表达系统、服务、资源之间的调用和依赖时再读 [系统架构关系图](references/system-architecture-relationships.md)。使用统一入口验证 typed JSON IR，再生成自包含 HTML。既有交互图表的静态导出沿用其源文件。
5. 思维导图：读 [思维导图](references/mindmaps.md)，交付可编辑的 Markmap Markdown 与可阅读的交互视图。它表达主题归属与层级；需要说明调用、数据流或依赖时转用系统架构关系图。
6. 分层架构图：读 [分层架构图](references/layered-architecture.md)，交付可编辑的 HTML 与可阅读的分层视图。它表达职责和技术位置；具体调用与依赖使用系统架构关系图。
7. 界面评审或精修：按[能力路由](references/capability-routing.md)读取评审、精修、回改或存量路径。技术审计再读[专项质量检查](references/design-quality.md)，结论需可复现条件与证据。

新建界面先区分阅读、操作与展示场景，再落实到上述平台路径。按[能力路由](references/capability-routing.md)选择任务与领域参考，处理方向比较、代表性页面、多页扩展、回改和项目设计规范。已有品牌和设计系统是依据，默认配色与第三方审美建议均不覆盖它们。

## 设计契约

内容和可读性先于氛围。正文、表格、日志与证据使用足够清晰的表面；品牌色、材质、字体与图像由具体项目确定。Joyally 品牌先按任务和已有品牌环境选择视觉主题；选用前五套景观主题时读[景观视觉规则](references/visual-language.md)，选用香奈儿风时读[香奈儿风主题](references/fashion-xiaoxiang.md)和[参考画面](assets/references/xiaoxiang/README.md)，选用太空时读[太空主题](references/space.md)，选用手绘时读[手绘主题](references/hand-drawn.md)并让 React Web 的完整组件基线来自 Looseleaf umbrella registry。选用阿尔卑斯雪山时读[雪山主题细则](references/alpine-snow-mountains.md)，[平台视觉参考](references/native-visual-system.md)提供现有青山湖预设的具体映射。青山湖从四季画面提炼一套主题，不按季节切换；随包青瓷釉和玻璃 token 是该主题的材质样本。香奈儿风与太空分别提供独立的浅色与深色[语义 token 样本](assets/xiaoxiang-theme.tokens.json)和[语义 token 样本](assets/space-theme.tokens.json)；手绘提供与 Looseleaf 官方浅色纸张体系对应的[语义 token 样本](assets/hand-drawn-theme.tokens.json)，深色模式须在目标项目另行完成变量、组件和对比度验收。其他主题进入产品时要完整映射相同语义 token 并验证。其他项目从自身品牌素材派生视觉语言。图表与报告共用语义配色。避免嵌套玻璃卡片、持续装饰动画与颜色单独表示状态。

新建界面在写 UI 或生成效果图前，先按[反模板感检查](references/anti-ai-taste.md)的“生成前约束”锁定产品对象、首屏主角与动作、视觉方向和要避免的无职责模板元素；将这些约束与界面需求一起交给生成工具。精修时先从实际画面定位问题，不凭风格标签重起方向。交付前再按同一检查核对任务焦点、内容顺序、容器职责、装饰语义、示例数据与状态反馈。把“AI 味”当作需要定位的可观察问题，不用颜色、圆角或渐变推断界面来源；具体问题和改法对照同一内容与视口验证。

语义 tokens 分为 seed、map、alias、component。Ant Design 提供分层与密度参考，Material 3 提供语义状态角色，Radix 提供无障碍行为，shadcn/ui 是 Joyally Design 的 React Web 主组件体系。Joyally 自有 React 新界面以完整 shadcn/ui 基础组件集建立组件库；手绘主题使用接口兼容的 Looseleaf 完整 registry 替换该基线，而不是只给部分控件加装饰。其他项目先沿用现有组件并按任务补齐。Data Table、Date Picker 等可由基础组件组合，保留升级路径。Magic UI 借鉴 shadcn/ui，React Bits 提供可定制动画与微交互；两者都可通过 shadcn CLI 按组件接入 React 项目，官网与中后台均按任务选用。安装、许可、操作状态和动效验收见 [React 组件工作流](references/component-workflow.md)。

页面按任务组织上下文、局部工具、主要内容与支持信息。只保留一个稳定标题层；selected、focus、loading 不推动布局。组件覆盖 default、hover、pressed、selected、focus、disabled、loading、empty、error、success，以及窄屏、reduced motion 和打印状态。

## 生成与校验

以下 `<skill-dir>` 是当前技能目录，输出使用用户指定位置或临时目录。工具直接位于 `scripts/`，使用方法见[能力路由](references/capability-routing.md)：

```bash
node <skill-dir>/scripts/design-engine.mjs report <output-dir> --title "报告标题" --subtitle "证据与下一步"
node <skill-dir>/scripts/design-engine.mjs social-card <output-dir> --style poster --title "卡片标题" --subtitle "内容说明" --credit "作者或来源"
node <skill-dir>/scripts/design-engine.mjs social-render <output-dir>/index.html --out <output-dir>/card.png
node <skill-dir>/scripts/design-engine.mjs deck <output-dir> --scenario project-report --theme lake
node <skill-dir>/scripts/design-engine.mjs deck <output-dir> --scenario tech-sharing --theme space
node <skill-dir>/scripts/design-engine.mjs deck-gallery <output-dir>
node <skill-dir>/scripts/design-engine.mjs deck-render <output-dir>/index.html --format pdf
node <skill-dir>/scripts/design-engine.mjs deck-bundle <output-dir>/index.html --out <output-dir>/standalone.html
node <skill-dir>/scripts/design-engine.mjs --help
python3 <skill-dir>/scripts/validate-joyally-tokens.py
python3 <skill-dir>/scripts/validate-native-tokens.py
python3 <skill-dir>/scripts/validate-diagram-theme.py
node <skill-dir>/scripts/validate-joyally-html.mjs <output-dir>/index.html
```

静态通过后检查桌面、窄屏、键盘、长文本、空状态、错误与打印输出。动态图表运行 `design-engine.mjs diagram validate` 和 `diagram deliver`；正文保留文字摘要或静态 fallback，分别报告确定性校验与视觉证据。

## 交付与来源

默认交付可用的本地产物。用户明确要求托管时，使用其已配置且获授权的上传方式，上传后读回最终 URL 比较 SHA-256；没有托管配置时直接交付本地文件，不推断上传目标或调用私有服务。保留用户要求的源文件。

Joyally Design 自身源码按 [非商业许可](LICENSE)提供。公开包仅包含已获准的小界、小萌、小南角色参考素材，不包含内部上传代码、账号、真实报告或安装证据。
